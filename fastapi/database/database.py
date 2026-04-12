import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# ENV CONFIG: Use MONGODB_URI if defined (for Render/Heroku), else use current string
uri = os.environ.get("MONGODB_URI", "mongodb+srv://bukkerohithmarthandanaik_db_user:1234@cluster0.o9ub8xs.mongodb.net/?appName=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)