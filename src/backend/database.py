import os
from sqlalchemy import create_engine, Column, BigInteger, String, Text, DateTime, Integer, UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import uuid

# データベースファイルのパス
DATABASE_URL = "sqlite:///chat365.db"

# SQLAlchemyの基本設定
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# `broadcasts`テーブルのモデル定義
class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    content_hash = Column(String(256), index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_seconds = Column(Integer)
    priority = Column(Integer, nullable=False, default=0, index=True)
    task_type = Column(String(50), nullable=False, default='REGULAR')
    status = Column(String(50), nullable=False, default='SCHEDULED', index=True)
    source = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    retry_count = Column(Integer, default=0)
    error_log = Column(Text)

    def __repr__(self):
        return f"<Broadcast(id={self.id}, status='{self.status}')>"

def get_db():
    """データベースセッションを提供する"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
