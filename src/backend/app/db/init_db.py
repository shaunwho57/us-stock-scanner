from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, engine
from app.models.models import User
from app.core.security import get_password_hash
from app.core.config import settings

def init_db(engine):
    Base.metadata.create_all(bind=engine)
    
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # 检查是否已有管理员用户
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    # 如果没有管理员用户，则创建一个
    if not admin_user:
        admin_password = settings.LOGIN_PASSWORD
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
    
    db.close()
