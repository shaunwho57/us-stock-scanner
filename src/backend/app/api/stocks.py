from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.models import User, Stock, StockPrice
from app.schemas.schemas import Stock as StockSchema, StockFilterRequest
from app.data_sources.stock_data import get_stock_info, get_stock_historical_data, search_stocks

router = APIRouter()

@router.get("/search", response_model=List[dict])
async def search_stock(
    query: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    搜索股票
    """
    results = search_stocks(query)
    return results

@router.get("/{symbol}", response_model=dict)
async def get_stock(
    symbol: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取股票信息
    """
    stock_info = get_stock_info(symbol)
    if not stock_info:
        raise HTTPException(status_code=404, detail="股票未找到")
    
    return stock_info

@router.get("/{symbol}/historical", response_model=List[dict])
async def get_stock_historical(
    symbol: str,
    period: str = "1y",
    interval: str = "1d",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取股票历史数据
    """
    historical_data = get_stock_historical_data(symbol, period, interval)
    if not historical_data:
        raise HTTPException(status_code=404, detail="历史数据未找到")
    
    return historical_data

@router.post("/filter", response_model=List[dict])
async def filter_stocks(
    filter_params: StockFilterRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    筛选股票
    """
    # 这里应该实现股票筛选逻辑
    # 由于筛选逻辑较复杂，这里简化为返回一些示例数据
    
    # 示例数据
    filtered_stocks = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "current_price": 175.23,
            "change_percent": 1.25,
            "volume": 65432100,
            "market_cap": 2850000000000
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "current_price": 325.45,
            "change_percent": 0.75,
            "volume": 23456700,
            "market_cap": 2420000000000
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "current_price": 142.89,
            "change_percent": 1.05,
            "volume": 18765400,
            "market_cap": 1850000000000
        }
    ]
    
    return filtered_stocks

@router.get("/market/movers", response_model=dict)
async def get_market_movers(
    market: str = "US",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取市场涨跌幅排行
    """
    # 这里应该实现获取市场涨跌幅排行的逻辑
    # 由于逻辑较复杂，这里简化为返回一些示例数据
    
    # 示例数据
    market_movers = {
        "gainers": [
            {
                "symbol": "XYZ",
                "name": "XYZ Company",
                "change_percent": 8.75,
                "current_price": 45.67
            },
            {
                "symbol": "ABC",
                "name": "ABC Corporation",
                "change_percent": 7.25,
                "current_price": 32.45
            },
            {
                "symbol": "DEF",
                "name": "DEF Industries",
                "change_percent": 6.50,
                "current_price": 78.90
            }
        ],
        "losers": [
            {
                "symbol": "UVW",
                "name": "UVW Inc.",
                "change_percent": -5.80,
                "current_price": 12.34
            },
            {
                "symbol": "RST",
                "name": "RST Technologies",
                "change_percent": -4.75,
                "current_price": 56.78
            },
            {
                "symbol": "MNO",
                "name": "MNO Group",
                "change_percent": -4.20,
                "current_price": 23.45
            }
        ]
    }
    
    return market_movers

@router.get("/market/sectors", response_model=List[dict])
async def get_sector_performance(
    period: str = "1d",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取板块表现
    """
    # 这里应该实现获取板块表现的逻辑
    # 由于逻辑较复杂，这里简化为返回一些示例数据
    
    # 示例数据
    sectors = [
        {
            "name": "科技",
            "change_percent": 1.45,
            "ytd_change_percent": 15.75
        },
        {
            "name": "医疗健康",
            "change_percent": 0.32,
            "ytd_change_percent": 8.25
        },
        {
            "name": "金融",
            "change_percent": -0.21,
            "ytd_change_percent": 5.50
        },
        {
            "name": "能源",
            "change_percent": -0.67,
            "ytd_change_percent": -3.25
        },
        {
            "name": "消费品",
            "change_percent": 0.89,
            "ytd_change_percent": 7.80
        }
    ]
    
    return sectors
