from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_engine = create_engine('mysql://root:root@localhost:3306/products')
Session = sessionmaker(bind=db_engine)
Base = declarative_base()
