"""
株価データ取得テストスクリプト
yfinanceを使って日本株5銘柄のデータを取得
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 対象銘柄（東京証券取引所の銘柄コード.T）
STOCK_SYMBOLS = {
    '7203.T': 'トヨタ自動車',
    '6758.T': 'ソニーグループ',
    '9984.T': 'ソフトバンクグループ',
    '6861.T': 'キーエンス',
    '8306.T': '三菱UFJフィナンシャル・グループ'
}

def test_daily_data():
    """日足データの取得テスト"""
    print("=" * 60)
    print("日足データ取得テスト")
    print("=" * 60)

    for symbol, name in STOCK_SYMBOLS.items():
        print(f"\n【{name} ({symbol})】")
        try:
            # 過去3ヶ月のデータを取得
            stock = yf.Ticker(symbol)
            df = stock.history(period="3mo", interval="1d")

            if not df.empty:
                print(f"  ✓ データ取得成功: {len(df)}日分")
                print(f"  期間: {df.index[0].date()} ～ {df.index[-1].date()}")
                print(f"  最新終値: ¥{df['Close'].iloc[-1]:,.2f}")
            else:
                print(f"  ✗ データが空です")
        except Exception as e:
            print(f"  ✗ エラー: {str(e)}")

def test_hourly_data():
    """1時間足データの取得テスト"""
    print("\n" + "=" * 60)
    print("1時間足データ取得テスト")
    print("=" * 60)

    for symbol, name in STOCK_SYMBOLS.items():
        print(f"\n【{name} ({symbol})】")
        try:
            stock = yf.Ticker(symbol)
            # 直近60日の1時間足データ
            df = stock.history(period="60d", interval="1h")

            if not df.empty:
                print(f"  ✓ データ取得成功: {len(df)}時間分")
                print(f"  期間: {df.index[0]} ～ {df.index[-1]}")
                print(f"  最新終値: ¥{df['Close'].iloc[-1]:,.2f}")
            else:
                print(f"  ✗ データが空です")
        except Exception as e:
            print(f"  ✗ エラー: {str(e)}")

def test_5min_data():
    """5分足データの取得テスト"""
    print("\n" + "=" * 60)
    print("5分足データ取得テスト")
    print("=" * 60)

    for symbol, name in STOCK_SYMBOLS.items():
        print(f"\n【{name} ({symbol})】")
        try:
            stock = yf.Ticker(symbol)
            # 直近5日の5分足データ
            df = stock.history(period="5d", interval="5m")

            if not df.empty:
                print(f"  ✓ データ取得成功: {len(df)}個の5分足")
                print(f"  期間: {df.index[0]} ～ {df.index[-1]}")
                print(f"  最新終値: ¥{df['Close'].iloc[-1]:,.2f}")
            else:
                print(f"  ✗ データが空です")
        except Exception as e:
            print(f"  ✗ エラー: {str(e)}")

def test_data_structure():
    """データ構造の確認"""
    print("\n" + "=" * 60)
    print("データ構造の確認（トヨタ）")
    print("=" * 60)

    stock = yf.Ticker('7203.T')
    df = stock.history(period="5d", interval="1d")

    print(f"\nカラム: {list(df.columns)}")
    print(f"\nサンプルデータ（最新3日分）:")
    print(df.tail(3))

if __name__ == "__main__":
    print("\n株価データ取得テスト開始")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 各種データ取得テスト
    test_daily_data()
    test_hourly_data()
    test_5min_data()
    test_data_structure()

    print("\n" + "=" * 60)
    print("テスト完了")
    print("=" * 60)
