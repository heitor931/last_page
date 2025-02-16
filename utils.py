from mongo_connection import open_connection


def get_all_books():
    """Get all the books from the database
    Raises:
        Exception: _description_
    """
    try:
        client = open_connection()
        database = client.get_database("Book")
        pages = database.get_collection("pages")

        # Query for a movie that has the title 'Back to the Future'
        
        list_of_books = pages.find({}).to_list()

        client.close()
        
        return list_of_books


    except ConnectionError as e:
        raise ConnectionError("There was a connection error: ") from e
    
def insert_to_database(data):
    """insert to database

    Args:
        data (_type_): _object_
    """
    client =  open_connection()
    
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.insert_one(data)
    client.close()

def post_to_database(data):
    """post to database

    Args:
        data (_type_): _description_
    """
    client =  open_connection()
    
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.update_one({'id': data['id']}, {'$set': data}, upsert=True)
    client.close()

def find_one_from_database(query):
    client = open_connection()
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    book = pages.find_one({'id': query},{'_id': 0})
    client.close()
    return book