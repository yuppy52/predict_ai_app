"""
AIモデル学習スクリプト
転移学習（Transfer Learning）を使用してローソク足画像から株価動向を予測
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlowの警告を抑制

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0, MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import json
from datetime import datetime

print(f"TensorFlow version: {tf.__version__}")
print(f"GPU available: {tf.config.list_physical_devices('GPU')}")

class StockPredictionModel:
    """株価予測モデルクラス"""

    def __init__(self, model_type='efficientnet', input_shape=(224, 224, 3)):
        """
        Args:
            model_type: ベースモデル ('efficientnet' or 'mobilenet')
            input_shape: 入力画像サイズ
        """
        self.model_type = model_type
        self.input_shape = input_shape
        self.model = None
        self.history = None

    def build_model(self, learning_rate=0.001):
        """
        転移学習モデルを構築

        Args:
            learning_rate: 学習率
        """
        print(f"\n{'='*60}")
        print(f"モデル構築: {self.model_type}")
        print(f"{'='*60}")

        # ベースモデルの選択
        if self.model_type == 'efficientnet':
            base_model = EfficientNetB0(
                include_top=False,
                weights='imagenet',
                input_shape=self.input_shape
            )
        elif self.model_type == 'mobilenet':
            base_model = MobileNetV2(
                include_top=False,
                weights='imagenet',
                input_shape=self.input_shape
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        # ベースモデルの重みを凍結
        base_model.trainable = False

        # モデル構築
        inputs = keras.Input(shape=self.input_shape)

        # データ拡張（オプション）
        # x = layers.RandomFlip("horizontal")(inputs)
        # x = layers.RandomRotation(0.1)(x)

        # ベースモデル
        x = base_model(inputs, training=False)

        # Global Average Pooling
        x = layers.GlobalAveragePooling2D()(x)

        # Dropout（過学習防止）
        x = layers.Dropout(0.3)(x)

        # 全結合層
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.2)(x)

        # 出力層（2値分類: 上昇 or 下降）
        outputs = layers.Dense(1, activation='sigmoid')(x)

        # モデル作成
        model = keras.Model(inputs, outputs)

        # コンパイル
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )

        self.model = model
        print("\n✓ モデル構築完了")
        print(f"  パラメータ数: {model.count_params():,}")

        return model

    def prepare_dataset(self, image_dir, validation_split=0.2, batch_size=32):
        """
        データセットを準備

        Args:
            image_dir: 画像ディレクトリ
            validation_split: 検証データの割合
            batch_size: バッチサイズ

        Returns:
            (train_dataset, val_dataset, class_names)
        """
        print(f"\n{'='*60}")
        print("データセット準備")
        print(f"{'='*60}")

        # メタデータから画像パスとラベルを収集
        all_images = []
        all_labels = []

        image_path = Path(image_dir)
        metadata_files = list(image_path.glob('**/metadata.csv'))

        print(f"  メタデータファイル数: {len(metadata_files)}")

        for metadata_file in metadata_files:
            df = pd.read_csv(metadata_file)
            all_images.extend(df['image_path'].tolist())
            all_labels.extend(df['label'].tolist())

        print(f"  総画像数: {len(all_images)}")
        print(f"  上昇: {sum(all_labels)}枚 ({sum(all_labels)/len(all_labels)*100:.1f}%)")
        print(f"  下降: {len(all_labels)-sum(all_labels)}枚 ({(len(all_labels)-sum(all_labels))/len(all_labels)*100:.1f}%)")

        # 訓練/検証データに分割
        train_images, val_images, train_labels, val_labels = train_test_split(
            all_images, all_labels,
            test_size=validation_split,
            random_state=42,
            stratify=all_labels
        )

        print(f"\n  訓練データ: {len(train_images)}枚")
        print(f"  検証データ: {len(val_images)}枚")

        # データジェネレータ
        def create_dataset(image_paths, labels, batch_size, is_training=True):
            """データセット作成"""

            def load_and_preprocess_image(image_path, label):
                # 画像読み込み
                img = tf.io.read_file(image_path)
                img = tf.image.decode_png(img, channels=3)
                img = tf.image.resize(img, self.input_shape[:2])
                img = tf.cast(img, tf.float32) / 255.0  # 正規化

                return img, label

            # データセット作成
            dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
            dataset = dataset.map(load_and_preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)

            if is_training:
                dataset = dataset.shuffle(1000)

            dataset = dataset.batch(batch_size)
            dataset = dataset.prefetch(tf.data.AUTOTUNE)

            return dataset

        train_dataset = create_dataset(train_images, train_labels, batch_size, is_training=True)
        val_dataset = create_dataset(val_images, val_labels, batch_size, is_training=False)

        return train_dataset, val_dataset, {'up': 1, 'down': 0}

    def train(self, train_dataset, val_dataset, epochs=20, model_save_path='models/stock_model.keras'):
        """
        モデルを学習

        Args:
            train_dataset: 訓練データセット
            val_dataset: 検証データセット
            epochs: エポック数
            model_save_path: モデル保存先

        Returns:
            history: 学習履歴
        """
        print(f"\n{'='*60}")
        print("モデル学習開始")
        print(f"{'='*60}")

        # コールバック設定
        callbacks = [
            keras.callbacks.ModelCheckpoint(
                model_save_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
        ]

        # 学習
        history = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )

        self.history = history
        print("\n✓ 学習完了")

        return history

    def evaluate(self, test_dataset):
        """モデルを評価"""
        results = self.model.evaluate(test_dataset, verbose=1)
        metrics = dict(zip(self.model.metrics_names, results))
        return metrics

    def save_training_history(self, save_path='models/training_history.json'):
        """学習履歴を保存"""
        if self.history:
            history_dict = {k: [float(v) for v in vals] for k, vals in self.history.history.items()}
            history_dict['timestamp'] = datetime.now().isoformat()
            history_dict['model_type'] = self.model_type

            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'w') as f:
                json.dump(history_dict, f, indent=2)
            print(f"  学習履歴を保存: {save_path}")


def main():
    """メイン処理"""
    print("\n" + "=" * 60)
    print("株価予測AIモデル学習")
    print("=" * 60)

    # ハイパーパラメータ
    CONFIG = {
        'model_type': 'efficientnet',  # 'efficientnet' or 'mobilenet'
        'input_shape': (224, 224, 3),
        'batch_size': 32,
        'epochs': 20,
        'learning_rate': 0.001,
        'validation_split': 0.2,
        'image_dir': 'data/stock_images',
        'model_save_path': 'models/stock_prediction_model.keras'
    }

    # モデル構築
    model_trainer = StockPredictionModel(
        model_type=CONFIG['model_type'],
        input_shape=CONFIG['input_shape']
    )

    model_trainer.build_model(learning_rate=CONFIG['learning_rate'])

    # データセット準備
    train_dataset, val_dataset, class_names = model_trainer.prepare_dataset(
        image_dir=CONFIG['image_dir'],
        validation_split=CONFIG['validation_split'],
        batch_size=CONFIG['batch_size']
    )

    # 学習
    history = model_trainer.train(
        train_dataset=train_dataset,
        val_dataset=val_dataset,
        epochs=CONFIG['epochs'],
        model_save_path=CONFIG['model_save_path']
    )

    # 学習履歴保存
    model_trainer.save_training_history('models/training_history.json')

    # 最終評価
    print(f"\n{'='*60}")
    print("最終評価")
    print(f"{'='*60}")
    metrics = model_trainer.evaluate(val_dataset)
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

    print("\n" + "=" * 60)
    print("学習完了！")
    print(f"モデル保存先: {CONFIG['model_save_path']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
