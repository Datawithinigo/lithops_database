from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.models import Processor, Base

# Create database connection
engine = create_engine("postgresql://user:password@localhost:5432/xeon_processors")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 1. Basic Query: Retrieve All Processors
all_processors = db.query(Processor).all()
for processor in all_processors:
    print(f"Product: {processor.product}, Cores: {processor.cores}")

# 2. Filter Queries
# Find processors with 8 cores
eight_core_processors = db.query(Processor).filter(Processor.cores == 8).all()
for processor in eight_core_processors:
    print(f"8-Core Processor: {processor.product}")

# 3. Query with Multiple Conditions
high_performance_processors = db.query(Processor).filter(
    Processor.cores >= 8, 
    Processor.max_turbo_freq > 4.0
).all()
for processor in high_performance_processors:
    print(f"High Performance Processor: {processor.product}")

# 4. Order Results
# Sort processors by max turbo frequency
sorted_processors = db.query(Processor).order_by(Processor.max_turbo_freq.desc()).all()
for processor in sorted_processors:
    print(f"Processor: {processor.product}, Max Turbo: {processor.max_turbo_freq} GHz")

# 5. Count Processors
processor_count = db.query(Processor).count()
print(f"Total Processors in Database: {processor_count}")

# 6. First Result
first_processor = db.query(Processor).first()
if first_processor:
    print(f"First Processor: {first_processor.product}")

# 7. Complex Filtering
advanced_processors = db.query(Processor).filter(
    Processor.cores > 6,
    Processor.lithography <= 14.0,
    Processor.status == "Launched"
).all()
for processor in advanced_processors:
    print(f"Advanced Processor: {processor.product}")

# Close the database session
db.close()