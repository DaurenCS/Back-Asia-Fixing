from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# url = 'postgresql://postgres:postgres@86.107.45.160:5432/postgres'
url = "postgresql://dbpostgres:DdGj3VTAEiK4Z60aCw2ntAYpQAqFcwxw@dpg-cpbas77sc6pc73a58r00-a.oregon-postgres.render.com:5432/dbpostgres_8o0i"
# url = 'postgresql://db_postgres:5XaRR2QIOaIatg7mrFX6DY1Co6EwfttE@dpg-cp2u0d21hbls7384vgug-a.oregon-postgres.render.com:5432/db_postgres_30ma'
engine = create_engine(url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()