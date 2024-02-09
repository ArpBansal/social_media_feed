from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)
Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()