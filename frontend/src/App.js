import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [stocks, setStocks] = useState([]);
  const [timeframes, setTimeframes] = useState([]);
  const [selectedStock, setSelectedStock] = useState('');
  const [selectedTimeframe, setSelectedTimeframe] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // API base URL
  const API_BASE_URL = 'http://localhost:8000/api';

  // 銘柄リストを取得
  useEffect(() => {
    const fetchStockList = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/stocks/`);
        setStocks(response.data.stocks);
        setTimeframes(response.data.timeframes);

        // デフォルト選択
        if (response.data.stocks.length > 0) {
          setSelectedStock(response.data.stocks[0].code);
        }
        if (response.data.timeframes.length > 0) {
          setSelectedTimeframe(response.data.timeframes[0].value);
        }
      } catch (err) {
        console.error('銘柄リスト取得エラー:', err);
        setError('銘柄リストの取得に失敗しました');
      }
    };

    fetchStockList();
  }, []);

  // 予測を実行
  const handlePredict = async () => {
    if (!selectedStock || !selectedTimeframe) {
      setError('銘柄と時間軸を選択してください');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict/`, {
        stock_code: selectedStock,
        timeframe: selectedTimeframe
      });
      setPrediction(response.data);
    } catch (err) {
      console.error('予測エラー:', err);
      setError('予測の実行に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>📈 株価予測AI</h1>
          <p className="subtitle">短期トレンド予測システム</p>
        </header>

        <div className="selection-panel">
          <div className="form-group">
            <label htmlFor="stock-select">銘柄</label>
            <select
              id="stock-select"
              value={selectedStock}
              onChange={(e) => setSelectedStock(e.target.value)}
              className="select-input"
            >
              {stocks.map((stock) => (
                <option key={stock.code} value={stock.code}>
                  {stock.name} ({stock.code})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="timeframe-select">時間軸</label>
            <select
              id="timeframe-select"
              value={selectedTimeframe}
              onChange={(e) => setSelectedTimeframe(e.target.value)}
              className="select-input"
            >
              {timeframes.map((tf) => (
                <option key={tf.value} value={tf.value}>
                  {tf.label}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="predict-button"
          >
            {loading ? '予測中...' : '予測実行'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {prediction && (
          <div className="prediction-result">
            <h2>予測結果</h2>
            <div className="stock-info">
              <p className="stock-name">{prediction.stock_name}</p>
              <p className="stock-code">({prediction.stock_code})</p>
              <p className="timeframe-label">
                {timeframes.find(tf => tf.value === prediction.timeframe)?.label}
              </p>
            </div>

            <div className="probabilities">
              <div className="probability-item up">
                <div className="probability-header">
                  <span className="label">📈 上昇確率</span>
                  <span className="value">{prediction.prediction.up_probability}%</span>
                </div>
                <div className="probability-bar">
                  <div
                    className="probability-fill up-fill"
                    style={{ width: `${prediction.prediction.up_probability}%` }}
                  ></div>
                </div>
              </div>

              <div className="probability-item down">
                <div className="probability-header">
                  <span className="label">📉 下降確率</span>
                  <span className="value">{prediction.prediction.down_probability}%</span>
                </div>
                <div className="probability-bar">
                  <div
                    className="probability-fill down-fill"
                    style={{ width: `${prediction.prediction.down_probability}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {prediction.note && (
              <div className="note">
                {prediction.note}
              </div>
            )}
          </div>
        )}

        <footer className="footer">
          <p>本システムは教育・個人利用目的です</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
