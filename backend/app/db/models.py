from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    
    UserId = Column(Integer, primary_key=True, index=True)
    Username = Column(String(255), unique=True, nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())
