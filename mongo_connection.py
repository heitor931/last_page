import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv('MONGODB_URL')


def open_connection():
    client = MongoClient("mongodb+srv://heitor:TbfZGr604XbKxGjs@cluster0.slqbvjt.mongodb.net/Book?retryWrites=true&w=majority")
    return client