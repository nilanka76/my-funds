from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:Admin2026@localhost:5432/fund_tracker"
engine = create_engine(db_url)
localSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
