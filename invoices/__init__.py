from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/dynobay_db')
Session = sessionmaker(bind=db_engine)
Base = declarative_base()
