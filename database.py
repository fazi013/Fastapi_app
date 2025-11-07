from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url="mysql+pymysql://root:12345@localhost:3306/pythoncrud"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)