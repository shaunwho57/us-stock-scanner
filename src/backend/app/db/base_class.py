import os
from app.db.session import Base
from app.models import models

# 导入所有模型，确保它们被注册到Base中
__all__ = ["Base"]
