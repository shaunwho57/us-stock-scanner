FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建目录结构
RUN mkdir -p /app/logs /app/data /app/static

# 复制后端代码
COPY ./src/backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/backend/app /app/app

# 复制前端构建文件
COPY ./src/frontend/dist /app/static

# 设置环境变量
ENV PYTHONPATH=/app
ENV DATA_DIR=/app/data
ENV LOGS_DIR=/app/logs

# 暴露端口
EXPOSE 8888

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]
