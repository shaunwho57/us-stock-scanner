from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# 用户相关模型
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

# 股票相关模型
class StockBase(BaseModel):
    symbol: str
    name: str
    exchange: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: str = "US"
    market_cap: Optional[float] = None

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class StockInDBBase(StockBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class Stock(StockInDBBase):
    pass

# 股票价格相关模型
class StockPriceBase(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float
    volume: float

class StockPriceCreate(StockPriceBase):
    stock_id: int

class StockPriceUpdate(StockPriceBase):
    pass

class StockPriceInDBBase(StockPriceBase):
    id: int
    stock_id: int

    class Config:
        orm_mode = True

class StockPrice(StockPriceInDBBase):
    pass

# 技术指标相关模型
class TechnicalIndicatorBase(BaseModel):
    date: datetime
    indicator_type: str
    value: float
    parameters: str

class TechnicalIndicatorCreate(TechnicalIndicatorBase):
    stock_id: int

class TechnicalIndicatorUpdate(TechnicalIndicatorBase):
    pass

class TechnicalIndicatorInDBBase(TechnicalIndicatorBase):
    id: int
    stock_id: int

    class Config:
        orm_mode = True

class TechnicalIndicator(TechnicalIndicatorInDBBase):
    pass

# 用户自选股相关模型
class WatchlistBase(BaseModel):
    name: str

class WatchlistCreate(WatchlistBase):
    user_id: int

class WatchlistUpdate(WatchlistBase):
    pass

class WatchlistInDBBase(WatchlistBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Watchlist(WatchlistInDBBase):
    pass

# 认证相关模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

# 股票筛选请求模型
class StockFilterRequest(BaseModel):
    market: str = "US"  # 市场: US, HK, CN
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_volume: Optional[float] = None
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    price_change_percent: Optional[float] = None  # 价格变动百分比
    ma_trend: Optional[str] = None  # 均线趋势: up, down, cross
    rsi_min: Optional[float] = None
    rsi_max: Optional[float] = None
    macd_signal: Optional[str] = None  # MACD信号: bullish, bearish

# 技术分析请求模型
class TechnicalAnalysisRequest(BaseModel):
    symbol: str
    indicators: List[str]  # 例如: ["MA", "RSI", "MACD"]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
# 市场趋势请求模型
class MarketTrendRequest(BaseModel):
    market: str = "US"  # 市场: US, HK, CN
    period: str = "1d"  # 周期: 1d, 5d, 1mo, 3mo, 6mo, 1y
    sectors: Optional[List[str]] = None
