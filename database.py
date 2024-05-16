from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://db_postgres:5XaRR2QIOaIatg7mrFX6DY1Co6EwfttE@dpg-cp2u0d21hbls7384vgug-a.oregon-postgres.render.com:5432/db_postgres_30ma'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()