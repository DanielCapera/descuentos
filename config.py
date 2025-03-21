from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "discount_detector"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
