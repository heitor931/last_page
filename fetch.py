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
