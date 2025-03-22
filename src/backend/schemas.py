from pydantic import BaseModel
from typing import Optional

class ProcessorBase(BaseModel):
    product: str
    status: str
    release_date: str
    code_name: str
    cores: Optional[int]
    threads: Optional[int]
    lithography: Optional[float]
    max_turbo_freq: Optional[float]
    base_freq: Optional[float]
    tdp: Optional[int]
    cache: Optional[float]
    cache_info: Optional[str]
    max_memory_size: Optional[int]
    memory_types: str
    max_memory_speed: Optional[int]
    integrated_graphics: str

class Processor(ProcessorBase):
    id: int

    class Config:
        from_attributes = True