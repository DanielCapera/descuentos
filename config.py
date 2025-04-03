from pymongo import MongoClient

MONGO_URI = "mongodb+srv://descuentos:Descuentos@cluster0.zdyuqay.mongodb.net/descuentos?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client.get_database()  # O db = client["descuentos"]
