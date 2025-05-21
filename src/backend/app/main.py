from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

import os
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from app.api import stocks, users, auth, analysis
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db import base_class, init_db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(settings.LOGS_DIR, "app.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="US Stock Scanner API",
    description="美股分析系统API",
    version="1.0.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
@app.on_event("startup")
async def startup_event():
    logger.info("应用启动，初始化数据库...")
    init_db.init_db(engine)
    logger.info("数据库初始化完成")

# 包含API路由
app.include_router(auth.router, prefix="/api", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["股票"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["分析"])

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 挂载静态文件（前端构建后的文件）
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 处理404错误，返回前端应用
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Not Found"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8888, reload=True)
