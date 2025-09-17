from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(String)
    tokens = Column(Integer)
