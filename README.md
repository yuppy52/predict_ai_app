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
```

### フロントエンド

```bash
cd frontend
npm install
```

## 開発状況

- [x] 要件定義
- [ ] プロジェクト構造作成
- [ ] データ取得テスト
- [ ] AIモデル開発
- [ ] バックエンドAPI開発
- [ ] フロントエンド開発
