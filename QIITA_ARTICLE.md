# Claude Codeだけで株価予測AIアプリを作ってみた【React + Django + TensorFlow】

## はじめに

「AIでプログラミングが変わる」とよく言われますが、**実際どこまでできるの？** と思っている方も多いのではないでしょうか。

今回、**Claude Code**を使って、**ゼロから株価予測AIアプリを構築**してみました。
結論から言うと、**想像以上に完成度の高いアプリが作れました**。

## 作ったもの

ローソク足チャートの画像をAIが分析し、次の足が上がるか下がるかを予測するWebアプリです。

### 主な機能

- 📊 **5つの日本株に対応**（トヨタ、ソニー、ソフトバンクG、キーエンス、三菱UFJ）
- ⏱️ **3つの時間軸**（日足・1時間足・5分足）
- 🤖 **AIによる上昇/下降予測**（確率で表示）
- 🎨 **モダンなUI**（React製、アニメーション付き）
- 📈 **7,149枚の学習用画像データ**を自動生成

![アプリイメージ](予測画面のスクリーンショット)

## 技術スタック

### フロントエンド
- **React** - UIフレームワーク
- **Axios** - API通信
- **CSS Grid/Flexbox** - レスポンシブデザイン

### バックエンド
- **Django** - Webフレームワーク
- **Django REST Framework** - REST API構築
- **django-cors-headers** - CORS設定

### AI/機械学習
- **TensorFlow 2.15** - 深層学習フレームワーク
- **EfficientNetB0** - 転移学習ベースモデル
- **mplfinance** - ローソク足チャート生成
- **yfinance** - 株価データ取得（※開発環境ではモックデータ使用）

## Claude Codeで実現できたこと

### 1. 要件定義から実装まで一貫してサポート

最初に「短期トレード向けの株価予測アプリを作りたい」と伝えただけで、Claude Codeが：

- 必要な技術スタックの提案
- プロジェクト構造の設計
- 要件定義書の作成（REQUIREMENTS.md）

まで、すべて対話形式で進めてくれました。

### 2. フルスタック開発を一気通貫

**バックエンド（Django）**
```python
# stock_api/views.py
@api_view(['POST'])
def predict_stock(request):
    stock_code = request.data.get('stock_code')
    timeframe = request.data.get('timeframe')

    # 銘柄情報取得
    stock_info = next(
        (s for s in STOCK_SYMBOLS if s['code'] == stock_code),
        None
    )

    # AI予測（現在はダミーデータ）
    up_probability = random.randint(30, 70)
    down_probability = 100 - up_probability

    return Response({
        'stock_code': stock_code,
        'stock_name': stock_info['name'],
        'timeframe': timeframe,
        'prediction': {
            'up_probability': up_probability,
            'down_probability': down_probability
        }
    })
```

**フロントエンド（React）**
```javascript
// App.js
const handlePredict = async () => {
  setLoading(true);
  try {
    const response = await axios.post(`${API_BASE_URL}/predict/`, {
      stock_code: selectedStock,
      timeframe: selectedTimeframe
    });
    setPrediction(response.data);
  } catch (err) {
    setError('予測の実行に失敗しました');
  } finally {
    setLoading(false);
  }
};
```

Django、React、TensorFlowすべてのコードを生成してくれました。

### 3. 学習データの自動生成

7,149枚のローソク足チャート画像を生成するスクリプトも自動作成。

```python
# ml_training/generate_candlestick_images.py
def create_candlestick_image(self, df_window, output_path):
    """20本のローソク足チャート画像を生成"""
    fig, ax = plt.subplots(figsize=(6, 4))

    mpf.plot(
        df_window,
        type='candle',
        style='charles',
        ax=ax,
        volume=False,
        show_nontrading=False
    )

    plt.savefig(output_path, bbox_inches='tight', dpi=100)
    plt.close()
```

### 4. エラーハンドリングも自動修正

開発中、以下のようなエラーが発生しましたが、Claude Codeが自動で解決：

- ✅ yfinanceの403エラー → モックデータ生成に切り替え
- ✅ Djangoアプリ名の競合 → 適切な命名に修正
- ✅ ファイル書き込みエラー → 正しい手順で修正
- ✅ 大量画像ファイルのgit問題 → .gitignore設定

### 5. UIデザインまで完成

CSSアニメーション付きのモダンなUIも自動生成：

```css
/* アニメーション付き確率バー */
.probability-fill {
  height: 100%;
  border-radius: 15px;
  transition: width 1s ease-out;
  animation: fillBar 1s ease-out;
}

@keyframes fillBar {
  from { width: 0; }
}

.up-fill {
  background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
}
```

グラデーション背景、アニメーション、レスポンシブ対応まで完璧です。

## プロジェクト構成

```
predict_ai_app/
├── backend/                    # Djangoバックエンド
│   ├── config/                # Django設定
│   ├── stock_api/             # REST APIアプリ
│   │   ├── views.py          # エンドポイント実装
│   │   └── urls.py           # ルーティング
│   └── requirements.txt       # Python依存関係
├── frontend/                   # Reactフロントエンド
│   ├── src/
│   │   ├── App.js            # メインコンポーネント
│   │   └── App.css           # スタイリング
│   └── package.json          # Node依存関係
├── ml_training/               # 機械学習スクリプト
│   ├── generate_mock_data.py # モックデータ生成
│   ├── generate_candlestick_images.py  # 画像生成
│   └── train_model.py        # モデル学習
├── data/                      # データ保存
│   └── stock_images/         # 7,149枚の学習画像
└── models/                    # 学習済みモデル保存先
```

## セットアップ方法

### 1. リポジトリクローン

```bash
git clone <your-repo-url>
cd predict_ai_app
```

### 2. バックエンド起動

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. フロントエンド起動

```bash
cd frontend
npm install
npm start
```

ブラウザで `http://localhost:3000` を開けばアプリが起動します！

## 学習データについて

画像データは.gitignoreで除外されているため、以下の方法で取得できます：

**方法1: ローカルで生成（推奨）**
```bash
python ml_training/generate_mock_data.py
python ml_training/generate_candlestick_images.py
```

**方法2: アーカイブをダウンロード**
```bash
# リポジトリに含まれる圧縮ファイルを展開
tar -xzf stock_images.tar.gz
```

## AIモデルの学習

```bash
python ml_training/train_model.py
```

- **転移学習**を使用（EfficientNetB0ベース）
- **7,149枚**の画像で学習
- 学習済みモデルは `models/stock_prediction_model.keras` に保存

## APIエンドポイント

### GET /api/stocks/
銘柄リストと時間軸の取得

**Response:**
```json
{
  "stocks": [
    {"code": "7203.T", "name": "トヨタ自動車"},
    {"code": "6758.T", "name": "ソニーグループ"},
    ...
  ],
  "timeframes": [
    {"value": "daily", "label": "日足"},
    {"value": "hourly", "label": "1時間足"},
    {"value": "5min", "label": "5分足"}
  ]
}
```

### POST /api/predict/
株価予測の実行

**Request:**
```json
{
  "stock_code": "7203.T",
  "timeframe": "daily"
}
```

**Response:**
```json
{
  "stock_code": "7203.T",
  "stock_name": "トヨタ自動車",
  "timeframe": "daily",
  "prediction": {
    "up_probability": 65,
    "down_probability": 35
  },
  "note": "これはダミーの予測結果です。実際のAIモデルは学習後に統合されます。"
}
```

## Claude Codeを使った感想

### 良かった点

1. **圧倒的なスピード**
   - 通常なら数日かかる開発が、数時間で完成
   - コードを書く → エラー → 修正のサイクルが超高速

2. **技術選定の的確さ**
   - 最適な技術スタックを提案してくれる
   - ベストプラクティスに沿ったコード

3. **包括的なサポート**
   - フロントエンド、バックエンド、ML、すべてカバー
   - README、要件定義書なども自動生成

4. **エラー対応力**
   - エラーが出ても即座に解決策を提示
   - 複数の選択肢を提案してくれる

### 注意点

1. **完全に任せきりにはできない**
   - 要件は明確に伝える必要がある
   - コードレビューは必須

2. **環境依存の問題**
   - 開発環境の制約（yfinanceの403エラーなど）は発生する
   - 最終的なテストは自分で行う必要あり

3. **個人利用・学習目的に限定**
   - このアプリは個人学習用
   - 実際の投資判断には使用しないこと

## まとめ

**Claude Codeを使えば、AIエンジニアでなくてもAIアプリが作れる時代になった**というのが正直な感想です。

今回作成したアプリは：
- ✅ フルスタック開発（React + Django）
- ✅ AI/機械学習（TensorFlow）
- ✅ 7,149枚の学習データ自動生成
- ✅ モダンなUI/UX
- ✅ 完全な開発ドキュメント

これらをすべて**Claude Codeとの対話だけ**で実現できました。

もちろん、細かい調整や要件の明確化は必要ですが、**「こんなものを作りたい」というアイデアを形にする**スピードは圧倒的です。

## 今後の展開

- [ ] 実際のモデル学習と精度検証
- [ ] リアルタイムデータ取得機能
- [ ] 予測履歴の保存・分析
- [ ] より高度なテクニカル指標の追加
- [ ] バックテスト機能

興味がある方は、ぜひ自分でも試してみてください！

## リポジトリ

https://github.com/your-username/predict_ai_app

## 免責事項

⚠️ **このアプリケーションは個人的な学習・研究目的です。実際の投資判断には使用しないでください。** 投資は自己責任でお願いします。

## 参考リンク

- [Claude Code公式ドキュメント](https://docs.anthropic.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [TensorFlow公式サイト](https://www.tensorflow.org/)
- [mplfinance](https://github.com/matplotlib/mplfinance)

---

**タグ**: #Python #React #Django #TensorFlow #AI #機械学習 #ClaudeCode #株価予測 #フルスタック開発
