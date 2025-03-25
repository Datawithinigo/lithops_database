# initial solution: export PYTHONPATH=$PYTHONPATH:/home/bigrobbin/Desktop/git/lithops_database
 

import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.backend.models import Processor, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Rest of your existing code remains the same
engine = create_engine("postgresql://user:password@localhost:5432/xeon_processors")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Create a new processor
new_processor = Processor(
    product="Intel Xeon E-inigo",
    status="Launched",
    release_date="Q2'19",
    code_name="Coffee Lake",
    cores=8,
    threads=16,
    lithography=14.0,
    max_turbo_freq=5.0,
    base_freq=2.4,
    tdp=45,
    cache=16.0,
    cache_info="Intel Smart Cache",
    max_memory_size=128,
    memory_types="DDR4-2666, LPDDR3-2133",
    max_memory_speed=2666,
    integrated_graphics="Intel UHD Graphics P630"
)

# Add and commit
db.add(new_processor)
db.commit()
db.close()