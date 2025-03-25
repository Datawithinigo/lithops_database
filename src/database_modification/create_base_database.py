import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Database connection
DATABASE_URL = "postgresql://user:password@localhost:5432/intel_processors"
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Utility function to clean column names
def clean_column_name(col_name):
    """
    Convert column names to valid SQLAlchemy column names
    - Remove special characters
    - Replace spaces with underscores
    """
    # Remove parentheses and replace with nothing
    cleaned = col_name.replace('(', '').replace(')', '')
    # Replace spaces and other special characters with underscores
    cleaned = cleaned.replace(' ', '_').replace('.', '_')
    # Ensure the name starts with a letter
    if not cleaned[0].isalpha():
        cleaned = 'col_' + cleaned
    return cleaned

# Define a dynamic Processor model
class Processor(Base):
    __tablename__ = 'processors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_file = Column(String, nullable=False)
    
    @classmethod
    def create_dynamic_columns(cls, df):
        # Create columns dynamically
        for col in df.columns:
            cleaned_col = clean_column_name(col)
            
            # Determine column type
            if df[col].dtype == 'object':
                column_type = Text
            elif df[col].dtype == 'int64':
                column_type = Integer
            elif df[col].dtype == 'float64':
                column_type = Float
            else:
                column_type = String
            
            # Create column with original name as metadata
            setattr(cls, cleaned_col, Column(column_type, comment=col))

# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)

# Path to the CSV files
csv_directory = '/home/bigrobbin/Desktop/git/lithops_database/src/resources/v1_8'

def import_csv_files(directory):
    # Create a session
    session = Session()
    
    try:
        # List all CSV files in the directory
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            # Full path to the CSV file
            file_path = os.path.join(directory, csv_file)
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Dynamically create columns based on the first file
            Processor.create_dynamic_columns(df)
            Base.metadata.create_all(engine)
            
            # Rename columns to cleaned versions
            df.columns = [clean_column_name(col) for col in df.columns]
            
            # Add source file column
            df['source_file'] = csv_file
            
            # Convert DataFrame to list of dictionaries
            records = df.to_dict('records')
            
            # Insert records into the database
            for record in records:
                # Create a processor instance
                processor = Processor(**record)
                session.add(processor)
            
            # Commit after each file to track progress
            session.commit()
            print(f"Imported {csv_file}: {len(records)} records")
        
        print("All CSV files imported successfully!")
    
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        session.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        session.rollback()
    finally:
        session.close()

# Verify import
def verify_import():
    session = Session()
    try:
        # Get column names with their original names
        inspector = inspect(engine)
        columns = inspector.get_columns('processors')
        original_column_names = {
            col['name']: col['comment'] or col['name'] 
            for col in columns if 'comment' in col and col['comment'] is not None
        }
        
        total_processors = session.query(Processor).count()
        unique_sources = session.query(Processor.source_file).distinct().all()
        
        print(f"Total processors imported: {total_processors}")
        print("Source files imported:")
        for source in unique_sources:
            print(source[0])
        
        print("\nColumn Mappings:")
        for cleaned, original in original_column_names.items():
            print(f"{cleaned}: {original}")
    
    except SQLAlchemyError as e:
        print(f"Error during verification: {e}")
    finally:
        session.close()

# Run the import and verification
if __name__ == "__main__":
    import_csv_files(csv_directory)
    verify_import()