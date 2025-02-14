from mongo_connection import open_connection

def post_to_database(data):
    client =  open_connection()
    
    database = client.get_database("Book")
    pages = database.get_collection("pages")
   # result = pages.update_one({'id': data['id']}, {'$set': data}, upsert=True)
    result = pages.update_one({'id': data['id']}, {'$set': data}, upsert=True)