from fastapi import FastAPI, Depends, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import engine, get_db
import csv
from io import StringIO

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

@app.get("/processors/", response_model=List[schemas.Processor])
def get_processors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    processors = db.query(models.Processor).offset(skip).limit(limit).all()
    return processors

@app.get("/processor/tdp/{processor_name}")
def get_processor_tdp(processor_name: str, db: Session = Depends(get_db)):
    processor = db.query(models.Processor).filter(models.Processor.product == processor_name).first()
    if processor is None:
        raise HTTPException(status_code=404, detail="Processor not found")
    
    # Return a simple string response
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(f"The TDP of {processor.product} is {processor.tdp} watts")

@app.get("/api/processor/tdp/{processor_name}")
def get_processor_tdp_json(processor_name: str, db: Session = Depends(get_db)):
    processor = db.query(models.Processor).filter(models.Processor.product == processor_name).first()
    if processor is None:
        raise HTTPException(status_code=404, detail="Processor not found")
    
    # Return a JSON response using JSONResponse
    import json
    from fastapi.responses import JSONResponse
    from fastapi.encoders import jsonable_encoder
    
    data = {
        "processor": processor.product,
        "tdp": processor.tdp
    }
    
    json_data = json.dumps(data)
    return JSONResponse(content=json.loads(json_data))

@app.get("/processors/{processor_id}", response_model=schemas.Processor)
def get_processor(processor_id: int, db: Session = Depends(get_db)):
    processor = db.query(models.Processor).filter(models.Processor.id == processor_id).first()
    if processor is None:
        raise HTTPException(status_code=404, detail="Processor not found")
    return processor

@app.post("/upload-csv/")
async def upload_csv(file: bytes = File(...), db: Session = Depends(get_db)):
    content = file.decode('utf-8')
    csv_file = StringIO(content)
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        processor = models.Processor(
            product=row['Product'],
            status=row['Status'],
            release_date=row['Release Date'],
            code_name=row['Code Name'],
            cores=int(row['Cores']) if row['Cores'] != 'N/A' else None,
            threads=int(row['Threads']) if row['Threads'] != 'N/A' else None,
            lithography=float(row['Lithography(nm)']) if row['Lithography(nm)'] != 'N/A' else None,
            max_turbo_freq=float(row['Max. Turbo Freq.(GHz)']) if row['Max. Turbo Freq.(GHz)'] != 'N/A' else None,
            base_freq=float(row['Base Freq.(GHz)']) if row['Base Freq.(GHz)'] != 'N/A' else None,
            tdp=int(float(row['TDP(W)'])) if row['TDP(W)'] != 'N/A' else None,
            cache=float(row['Cache(MB)']) if row['Cache(MB)'] != 'N/A' else None,
            cache_info=row['Cache Info'],
            max_memory_size=int(float(row['Max Memory Size(GB)'])) if row['Max Memory Size(GB)'] != 'N/A' else None,
            memory_types=row['Memory Types'],
            max_memory_speed=int(row['Max Memory Speed(MHz)']) if row['Max Memory Speed(MHz)'] != 'N/A' else None,
            integrated_graphics=row['Integrated Graphics']
        )
        db.add(processor)
    
    db.commit()
    return {"message": "CSV data uploaded successfully"}
