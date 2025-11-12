'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url="mysql+pymysql://root:12345@localhost:3306/pythoncrud"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)'''

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://faisalammad78_db_user:12345@cluster0.fyuur6w.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(MONGO_URI)
db = client["fastapi"]  
task_collection = db["record"]  