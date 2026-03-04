from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # ===== SAAS FIELDS =====
    role = Column(String, default="customer")  # admin / customer
    subscription_status = Column(String, default="free")  # free / pro
    subscription_expiry = Column(DateTime, nullable=True)

    daily_usage = Column(Integer, default=0)
    last_usage_date = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    projects = relationship(
        "DesignProject",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class DesignProject(Base):
    __tablename__ = "design_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user_type = Column(String)
    room_type = Column(String)
    area = Column(Float)
    style = Column(String)
    budget = Column(Float)

    summary = Column(Text)           # Nội dung tóm tắt
    result_json = Column(Text)       # JSON AI trả về (có thể rất dài)
    image_path = Column(String)      # Lưu path file local

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
