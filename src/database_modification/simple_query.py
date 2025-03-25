from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create database connection
engine = create_engine("postgresql://user:password@localhost:5432/xeon_processors")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 1. Simple Select Query
def simple_select_query():
    sql = text("SELECT * FROM processors")
    result = db.execute(sql)
    for row in result:
        print(row)

# 2. Filtered Query
def filtered_query():
    sql = text("SELECT * FROM processors WHERE cores = 8")
    result = db.execute(sql)
    for row in result:
        print(row)

# 3. Parameterized Query (Recommended for security)
def parameterized_query(min_cores):
    sql = text("SELECT * FROM processors WHERE cores >= :cores")
    result = db.execute(sql, {"cores": min_cores})
    for row in result:
        print(row)

# 4. Sorting and Limiting Results
def sorted_query():
    sql = text("SELECT * FROM processors ORDER BY max_turbo_freq DESC LIMIT 5")
    result = db.execute(sql)
    for row in result:
        print(row)

# 5. Aggregation Query
def aggregation_query():
    sql = text("""
        SELECT 
            COUNT(*) as total_processors, 
            AVG(cores) as average_cores, 
            MAX(max_turbo_freq) as max_frequency
        FROM processors
    """)
    result = db.execute(sql).fetchone()
    print(f"Total Processors: {result.total_processors}")
    print(f"Average Cores: {result.average_cores}")
    print(f"Max Frequency: {result.max_frequency}")

# 6. Complex WHERE Clause
def complex_filter_query():
    sql = text("""
        SELECT product, cores, max_turbo_freq 
        FROM processors 
        WHERE cores > 6 AND lithography <= 14.0 AND status = 'Launched'
    """)
    result = db.execute(sql)
    for row in result:
        print(row)

# Examples of how to use these functions
if __name__ == "__main__":
    print("Simple Select:")
    simple_select_query()
    
    print("\nFiltered Query:")
    filtered_query()
    
    print("\nParameterized Query:")
    parameterized_query(6)
    
    print("\nSorted Query:")
    sorted_query()
    
    print("\nAggregation Query:")
    aggregation_query()
    
    print("\nComplex Filter:")
    complex_filter_query()

# Close the database session
db.close()