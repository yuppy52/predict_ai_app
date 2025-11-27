# 株価予測AIアプリ

ローソク足チャートの画像からAIが短期的な株価動向を予測するWebアプリケーション

## 概要

- **対象**: 日本株5銘柄（トヨタ、ソニー、ソフトバンクG、キーエンス、三菱UFJ）
- **時間軸**: 日足・1時間足・5分足
- **予測**: 直近20本のローソク足から次の1本の終値の上昇/下降を予測
- **技術スタック**: React + Django + TensorFlow

## 免責事項

⚠️ **このアプリケーションは個人的な学習・研究目的であり、実際の投資判断には使用しないでください。**

## プロジェクト構成

```
predict_ai_app/
├── backend/              # Djangoバックエンド
│   ├── api/             # REST API
│   ├── ml_model/        # AIモデル
│   ├── data/            # データ取得・処理
│   └── requirements.txt
├── frontend/            # Reactフロントエンド
├── ml_training/         # モデル学習スクリプト
├── models/              # 学習済みモデル
└── data/                # データ保存
```

## セットアップ

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

### フロントエンド

```bash
cd frontend
npm install
```

## 起動方法

### バックエンド起動

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```

バックエンドは `http://localhost:8000` で起動します。

### フロントエンド起動

別のターミナルを開いて：

```bash
cd frontend
npm start
```

フロントエンドは `http://localhost:3000` で起動し、ブラウザが自動で開きます。

## API エンドポイント

- `GET /api/health/` - ヘルスチェック
- `GET /api/stocks/` - 銘柄リスト・時間軸取得
- `POST /api/predict/` - 株価予測（現在はダミーデータ）
  - Request: `{"stock_code": "7203.T", "timeframe": "daily"}`
  - Response: `{"stock_code": "7203.T", "stock_name": "トヨタ自動車", "prediction": {"up_probability": 60, "down_probability": 40}}`

## 開発状況

- [x] 要件定義
- [x] プロジェクト構造作成
- [x] モックデータ生成
- [x] ローソク足画像生成
- [x] バックエンドAPI開発（Django REST Framework）
- [x] フロントエンド開発（React）
- [ ] AIモデル学習と統合

## 次のステップ

### AIモデルの学習（ローカル環境で実行）

```bash
# 学習データ画像生成（既に7,149枚生成済み）
python ml_training/generate_candlestick_images.py

# モデル学習
python ml_training/train_model.py
```

学習が完了したら、`models/stock_prediction_model.keras` に保存されます。
その後、バックエンドの `views.py` を修正して、ダミー予測から実際のAIモデルを使った予測に切り替えます。
