from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Processor(Base):
    __tablename__ = "processors"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    status = Column(String)
    release_date = Column(String)
    code_name = Column(String)
    cores = Column(Integer)
    threads = Column(Integer)
    lithography = Column(Float)
    max_turbo_freq = Column(Float)
    base_freq = Column(Float)
    tdp = Column(Integer)
    cache = Column(Float)
    cache_info = Column(String)
    max_memory_size = Column(Integer)
    memory_types = Column(String)
    max_memory_speed = Column(Integer)
    integrated_graphics = Column(String)