"""
ローソク足チャート画像生成スクリプト
株価データからローソク足の画像を生成し、学習用データを準備
"""

import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from datetime import datetime

class CandlestickImageGenerator:
    """ローソク足画像生成クラス"""

    def __init__(self, image_size=(224, 224), style='charles'):
        """
        Args:
            image_size: 画像サイズ (width, height)
            style: mplfinanceのスタイル
        """
        self.image_size = image_size
        self.style = style

    def generate_candlestick_image(self, df, save_path=None, show_volume=False):
        """
        ローソク足画像を生成

        Args:
            df: 株価データ (OHLCV形式)
            save_path: 保存先パス (Noneの場合は保存しない)
            show_volume: 出来高を表示するか

        Returns:
            画像が保存されたパス
        """
        # カスタムスタイル設定
        mc = mpf.make_marketcolors(
            up='red',      # 陽線: 赤
            down='blue',   # 陰線: 青
            edge='inherit',
            wick='inherit',
            volume='in',
        )

        s = mpf.make_mpf_style(
            marketcolors=mc,
            gridstyle='',
            y_on_right=False,
            rc={
                'font.size': 8,
                'axes.labelsize': 8,
                'axes.titlesize': 10,
                'xtick.labelsize': 7,
                'ytick.labelsize': 7,
                'figure.facecolor': 'white',
                'axes.facecolor': 'white'
            }
        )

        # プロット設定
        kwargs = dict(
            type='candle',
            style=s,
            volume=show_volume,
            figsize=(self.image_size[0]/100, self.image_size[1]/100),
            tight_layout=True,
            returnfig=True,
            show_nontrading=False,
            scale_padding={'left': 0.1, 'right': 0.1, 'top': 0.3, 'bottom': 0.3}
        )

        # 画像生成
        fig, axes = mpf.plot(df, **kwargs)

        if save_path:
            # 軸やラベルを非表示にしてシンプルな画像に
            for ax in axes:
                ax.set_xticks([])
                ax.set_yticks([])
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)

            fig.savefig(save_path, dpi=100, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            return save_path

        return fig

    def create_training_dataset(self, df, window_size=20, output_dir='data/stock_images'):
        """
        学習用データセットを作成
        スライディングウィンドウで画像とラベルを生成

        Args:
            df: 株価データ
            window_size: ローソク足の本数
            output_dir: 出力ディレクトリ

        Returns:
            dict: {'images': [...], 'labels': [...], 'metadata': [...]}
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        dataset = {
            'images': [],
            'labels': [],
            'metadata': []
        }

        total_samples = len(df) - window_size
        if total_samples <= 0:
            print(f"  ⚠ データが不足しています（必要: {window_size + 1}本, 実際: {len(df)}本）")
            return dataset

        for i in range(total_samples):
            # window_size本のローソク足を切り出し
            window_df = df.iloc[i:i+window_size].copy()

            # 次の足（予測対象）
            next_candle = df.iloc[i+window_size]

            # ラベル生成: 次の終値が上昇したら1、下降したら0
            current_close = window_df['Close'].iloc[-1]
            next_close = next_candle['Close']
            label = 1 if next_close > current_close else 0

            # 画像ファイル名
            timestamp = window_df.index[-1].strftime('%Y%m%d_%H%M%S') if hasattr(window_df.index[-1], 'strftime') else f'sample_{i}'
            label_str = 'up' if label == 1 else 'down'
            filename = f'{timestamp}_{label_str}.png'
            filepath = output_path / filename

            # 画像生成
            self.generate_candlestick_image(window_df, save_path=filepath)

            dataset['images'].append(str(filepath))
            dataset['labels'].append(label)
            dataset['metadata'].append({
                'window_start': str(window_df.index[0]),
                'window_end': str(window_df.index[-1]),
                'current_close': float(current_close),
                'next_close': float(next_close),
                'change_rate': float((next_close - current_close) / current_close * 100)
            })

        return dataset


def process_stock_data(symbol, csv_path, timeframe='daily'):
    """
    個別銘柄のデータを処理して画像生成

    Args:
        symbol: 銘柄コード
        csv_path: CSVファイルパス
        timeframe: 時間軸 ('daily', 'hourly', '5min')
    """
    print(f"\n【{symbol} - {timeframe}】")

    # データ読み込み
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    print(f"  データ読み込み: {len(df)}件")

    # 画像生成
    generator = CandlestickImageGenerator(image_size=(224, 224))
    output_dir = f'data/stock_images/{symbol.replace(".", "_")}/{timeframe}'

    dataset = generator.create_training_dataset(
        df=df,
        window_size=20,
        output_dir=output_dir
    )

    print(f"  ✓ 画像生成完了: {len(dataset['images'])}枚")
    print(f"  上昇: {sum(dataset['labels'])}枚, 下降: {len(dataset['labels']) - sum(dataset['labels'])}枚")

    # メタデータ保存
    metadata_df = pd.DataFrame(dataset['metadata'])
    metadata_df['image_path'] = dataset['images']
    metadata_df['label'] = dataset['labels']
    metadata_df.to_csv(f'{output_dir}/metadata.csv', index=False)
    print(f"  ✓ メタデータ保存: {output_dir}/metadata.csv")

    return dataset


def main():
    """メイン処理"""
    print("=" * 60)
    print("ローソク足画像生成スクリプト")
    print("=" * 60)

    # モックデータのパス設定
    stocks = [
        '7203_T',  # トヨタ
        '6758_T',  # ソニー
        '9984_T',  # ソフトバンクG
        '6861_T',  # キーエンス
        '8306_T',  # 三菱UFJFG
    ]

    timeframes = {
        'daily': '_daily.csv',
        'hourly': '_hourly.csv',
        '5min': '_5min.csv'
    }

    total_images = 0

    for stock in stocks:
        for tf_name, tf_suffix in timeframes.items():
            csv_path = f'data/{stock}{tf_suffix}'

            # ファイルが存在するか確認
            if not Path(csv_path).exists():
                print(f"  ⚠ ファイルが見つかりません: {csv_path}")
                continue

            dataset = process_stock_data(stock, csv_path, tf_name)
            total_images += len(dataset['images'])

    print("\n" + "=" * 60)
    print(f"全体の生成画像数: {total_images}枚")
    print("画像生成完了！")
    print("=" * 60)


if __name__ == "__main__":
    main()
