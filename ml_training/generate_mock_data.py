"""
モック株価データ生成スクリプト
リアルな株価の動きをシミュレートしたデータを生成
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class StockDataSimulator:
    """株価データシミュレーター"""

    def __init__(self, initial_price=1000, volatility=0.02):
        """
        Args:
            initial_price: 初期株価
            volatility: ボラティリティ（価格変動の大きさ）
        """
        self.initial_price = initial_price
        self.volatility = volatility

    def generate_daily_data(self, days=252, start_date=None):
        """
        日足データを生成

        Args:
            days: 生成する日数
            start_date: 開始日（Noneの場合は1年前から）

        Returns:
            pandas.DataFrame: OHLCV形式の株価データ
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)

        dates = pd.date_range(start=start_date, periods=days, freq='B')  # B = business days

        data = []
        current_price = self.initial_price

        for date in dates:
            # ランダムウォークで株価を生成
            change = np.random.normal(0, self.volatility)
            current_price = current_price * (1 + change)

            # OHLC生成（Open, High, Low, Close）
            open_price = current_price * (1 + np.random.uniform(-0.01, 0.01))
            close_price = current_price * (1 + np.random.uniform(-0.01, 0.01))
            high_price = max(open_price, close_price) * (1 + abs(np.random.uniform(0, 0.02)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.uniform(0, 0.02)))

            # 出来高
            volume = int(np.random.uniform(1000000, 10000000))

            data.append({
                'Date': date,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume
            })

        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df

    def generate_hourly_data(self, hours=480, start_datetime=None):
        """1時間足データを生成（約20営業日分）"""
        if start_datetime is None:
            start_datetime = datetime.now() - timedelta(hours=hours)

        dates = pd.date_range(start=start_datetime, periods=hours, freq='H')

        data = []
        current_price = self.initial_price

        for date in dates:
            # 時間足は日足より変動が小さい
            change = np.random.normal(0, self.volatility * 0.3)
            current_price = current_price * (1 + change)

            open_price = current_price * (1 + np.random.uniform(-0.005, 0.005))
            close_price = current_price * (1 + np.random.uniform(-0.005, 0.005))
            high_price = max(open_price, close_price) * (1 + abs(np.random.uniform(0, 0.01)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.uniform(0, 0.01)))
            volume = int(np.random.uniform(100000, 1000000))

            data.append({
                'Datetime': date,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume
            })

        df = pd.DataFrame(data)
        df.set_index('Datetime', inplace=True)
        return df

    def generate_5min_data(self, periods=288, start_datetime=None):
        """5分足データを生成（約1日分）"""
        if start_datetime is None:
            start_datetime = datetime.now() - timedelta(minutes=5*periods)

        dates = pd.date_range(start=start_datetime, periods=periods, freq='5T')

        data = []
        current_price = self.initial_price

        for date in dates:
            # 5分足は更に変動が小さい
            change = np.random.normal(0, self.volatility * 0.1)
            current_price = current_price * (1 + change)

            open_price = current_price * (1 + np.random.uniform(-0.002, 0.002))
            close_price = current_price * (1 + np.random.uniform(-0.002, 0.002))
            high_price = max(open_price, close_price) * (1 + abs(np.random.uniform(0, 0.005)))
            low_price = min(open_price, close_price) * (1 - abs(np.random.uniform(0, 0.005)))
            volume = int(np.random.uniform(10000, 100000))

            data.append({
                'Datetime': date,
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume
            })

        df = pd.DataFrame(data)
        df.set_index('Datetime', inplace=True)
        return df


# 5銘柄のモックデータ設定
MOCK_STOCKS = {
    '7203.T': {'name': 'トヨタ自動車', 'initial_price': 2500, 'volatility': 0.025},
    '6758.T': {'name': 'ソニーグループ', 'initial_price': 12000, 'volatility': 0.030},
    '9984.T': {'name': 'ソフトバンクグループ', 'initial_price': 5000, 'volatility': 0.035},
    '6861.T': {'name': 'キーエンス', 'initial_price': 65000, 'volatility': 0.020},
    '8306.T': {'name': '三菱UFJフィナンシャル・グループ', 'initial_price': 1200, 'volatility': 0.022}
}


def generate_all_mock_data():
    """全銘柄のモックデータを生成"""
    print("モック株価データ生成開始\n")

    for symbol, config in MOCK_STOCKS.items():
        print(f"【{config['name']} ({symbol})】")

        simulator = StockDataSimulator(
            initial_price=config['initial_price'],
            volatility=config['volatility']
        )

        # 日足データ（過去5年分）
        daily_df = simulator.generate_daily_data(days=252*5)
        print(f"  ✓ 日足: {len(daily_df)}日分")

        # 1時間足データ（過去60日分）
        hourly_df = simulator.generate_hourly_data(hours=60*24)
        print(f"  ✓ 1時間足: {len(hourly_df)}時間分")

        # 5分足データ（過去5日分）
        five_min_df = simulator.generate_5min_data(periods=288*5)
        print(f"  ✓ 5分足: {len(five_min_df)}個")

        # CSV保存
        daily_df.to_csv(f'data/{symbol.replace(".", "_")}_daily.csv')
        hourly_df.to_csv(f'data/{symbol.replace(".", "_")}_hourly.csv')
        five_min_df.to_csv(f'data/{symbol.replace(".", "_")}_5min.csv')
        print(f"  ✓ CSVファイル保存完了\n")

    print("=" * 60)
    print("モックデータ生成完了！")
    print("data/ ディレクトリにCSVファイルを保存しました。")


if __name__ == "__main__":
    generate_all_mock_data()
