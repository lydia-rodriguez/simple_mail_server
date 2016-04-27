from sqlalchemy import Column, Text, Integer, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    source = Column(Text)
    sender = Column(Text)
    recipients = Column(Text)
    body = Column(Text)
    message_read = Column(Boolean, default=False)
    time_received = Column(Float, default=0)
    time_parsed = Column(Float)
    ttl_ts = Column(Float, default=0)
