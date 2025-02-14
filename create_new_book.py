from mongo_connection import open_connection

def insert_to_database(data):
    client =  open_connection()
    
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.insert_one(data)