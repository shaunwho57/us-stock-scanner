from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import TechnicalAnalysisRequest
from app.data_sources.stock_data import get_stock_historical_data

router = APIRouter()

@router.post("/technical", response_model=Dict[str, Any])
async def technical_analysis(
    request: TechnicalAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    进行技术指标分析
    """
    # 获取历史数据
    historical_data = get_stock_historical_data(request.symbol, period="1y", interval="1d")
    if not historical_data:
        raise HTTPException(status_code=404, detail="历史数据未找到")
    
    # 转换为DataFrame
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # 计算技术指标
    result = {
        "symbol": request.symbol,
        "indicators": {}
    }
    
    for indicator in request.indicators:
        if indicator == "MA":
            result["indicators"]["MA"] = calculate_ma(df)
        elif indicator == "RSI":
            result["indicators"]["RSI"] = calculate_rsi(df)
        elif indicator == "MACD":
            result["indicators"]["MACD"] = calculate_macd(df)
        elif indicator == "BBANDS":
            result["indicators"]["BBANDS"] = calculate_bbands(df)
        elif indicator == "STOCH":
            result["indicators"]["STOCH"] = calculate_stoch(df)
    
    return result

def calculate_ma(df):
    """计算移动平均线"""
    result = {}
    for period in [5, 10, 20, 60]:
        ma = df['close'].rolling(window=period).mean()
        result[f"MA{period}"] = ma.tolist()
    return result

def calculate_rsi(df, period=14):
    """计算RSI"""
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return {"RSI": rsi.tolist()}

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """计算MACD"""
    exp1 = df['close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    hist = macd - signal
    
    return {
        "MACD": macd.tolist(),
        "MACD_signal": signal.tolist(),
        "MACD_hist": hist.tolist()
    }

def calculate_bbands(df, period=20, nbdevup=2, nbdevdn=2):
    """计算布林带"""
    ma = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper = ma + nbdevup * std
    lower = ma - nbdevdn * std
    
    return {
        "BBANDS_upper": upper.tolist(),
        "BBANDS_middle": ma.tolist(),
        "BBANDS_lower": lower.tolist()
    }

def calculate_stoch(df, fastk_period=14, slowk_period=3, slowd_period=3):
    """计算随机指标"""
    highest_high = df['high'].rolling(window=fastk_period).max()
    lowest_low = df['low'].rolling(window=fastk_period).min()
    fastk = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
    slowk = fastk.rolling(window=slowk_period).mean()
    slowd = slowk.rolling(window=slowd_period).mean()
    
    return {
        "STOCH_K": slowk.tolist(),
        "STOCH_D": slowd.tolist()
    }

@router.post("/backtest", response_model=Dict[str, Any])
async def backtest_strategy(
    strategy_params: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    回测交易策略
    """
    # 这里应该实现回测交易策略的逻辑
    # 由于逻辑较复杂，这里简化为返回一些示例数据
    
    # 示例数据
    backtest_result = {
        "strategy_name": strategy_params.get("strategy_name", "默认策略"),
        "symbol": strategy_params.get("symbol", "AAPL"),
        "start_date": "2022-01-01",
        "end_date": "2022-12-31",
        "initial_capital": 10000,
        "final_capital": 12500,
        "total_return": 25.0,
        "annualized_return": 22.5,
        "max_drawdown": 15.2,
        "sharpe_ratio": 1.35,
        "trades": [
            {
                "date": "2022-02-15",
                "type": "buy",
                "price": 150.25,
                "shares": 10
            },
            {
                "date": "2022-04-20",
                "type": "sell",
                "price": 165.75,
                "shares": 10
            },
            {
                "date": "2022-07-10",
                "type": "buy",
                "price": 145.50,
                "shares": 12
            },
            {
                "date": "2022-11-05",
                "type": "sell",
                "price": 170.25,
                "shares": 12
            }
        ]
    }
    
    return backtest_result
