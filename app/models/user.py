from sqlalchemy import Column, Integer, String, Enum
from app.db import Base
import enum
from sqlalchemy.orm import relationship


class Role(str, enum.Enum):
    client = "client"
    auditor = "auditor"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(Enum(Role), default=Role.client)
    
    uploaded_files = relationship("UploadedFile", back_populates="owner", cascade="all, delete")
