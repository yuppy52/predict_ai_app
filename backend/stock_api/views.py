from rest_framework.decorators import api_view
from rest_framework.response import Response
import random

# 対象銘柄リスト
STOCK_SYMBOLS = [
    {'code': '7203.T', 'name': 'トヨタ自動車'},
    {'code': '6758.T', 'name': 'ソニーグループ'},
    {'code': '9984.T', 'name': 'ソフトバンクグループ'},
    {'code': '6861.T', 'name': 'キーエンス'},
    {'code': '8306.T', 'name': '三菱UFJフィナンシャル・グループ'},
]

TIMEFRAMES = [
    {'value': 'daily', 'label': '日足'},
    {'value': 'hourly', 'label': '1時間足'},
    {'value': '5min', 'label': '5分足'},
]


@api_view(['GET'])
def get_stock_list(request):
    """銘柄リストを取得"""
    return Response({
        'stocks': STOCK_SYMBOLS,
        'timeframes': TIMEFRAMES
    })


@api_view(['POST'])
def predict_stock(request):
    """
    株価予測API（ダミー実装）

    Request body:
    {
        "stock_code": "7203.T",
        "timeframe": "daily"
    }
    """
    stock_code = request.data.get('stock_code')
    timeframe = request.data.get('timeframe')

    if not stock_code or not timeframe:
        return Response({'error': 'stock_code and timeframe are required'}, status=400)

    # ダミーの予測結果を生成（実際はAIモデルで予測）
    # 上昇確率と下降確率をランダムに生成（合計100%）
    up_probability = random.randint(30, 70)
    down_probability = 100 - up_probability

    stock_name = next((s['name'] for s in STOCK_SYMBOLS if s['code'] == stock_code), '不明')

    return Response({
        'stock_code': stock_code,
        'stock_name': stock_name,
        'timeframe': timeframe,
        'prediction': {
            'up_probability': up_probability,
            'down_probability': down_probability,
        },
        'note': '※ これはダミーデータです。実際のAIモデルは後で統合されます。'
    })


@api_view(['GET'])
def health_check(request):
    """ヘルスチェックエンドポイント"""
    return Response({'status': 'ok', 'message': 'Stock Prediction API is running'})
