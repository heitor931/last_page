from mongo_connection import open_connection
from datetime import datetime
import pretty_tables as pt
from colorama import Fore, Back, Style


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

def quick_update_book(book):
    client = open_connection()
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.update_one({'id': book['id']}, {'$set': book})

def generate_weekdays(day=False, month=False):
    if day:
        day_code = datetime.now().weekday()
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = weekdays[day_code]
        return day
    if month:
        month_id = datetime.now().month
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        day_month = months[month_id]
        return day_month

def delete_book(book_id):
    client = open_connection()
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.delete_one({'id': book_id})

def delete_all_books():
    client = open_connection()
    database = client.get_database("Book")
    pages = database.get_collection("pages")
    pages.delete_many({})

def show_tables(books, args):
    headers = ["id", "Book_Name", "Curr.Page", "Last time read", "Num.Pages", "Started_Date", "Due_date", "Completed"]
    rows = [[x["id"], x["book_name"], x['current_page'], x['last_page_date'], x["total_pages"], x['start_date'],
             x['due_date'], x['completed']] for x in books]
    if len(args) == 3 and args[2] == 'tab1':
        table = pt.create(
            headers=headers,
            rows=rows,
            colors=[pt.Colors.white, pt.Colors.red, pt.Colors.yellow, pt.Colors.blue, pt.Colors.cyan, pt.Colors.green,
                    pt.Colors.purple, pt.Colors.black],
        )
        # )
        print("-" * 120)
        print(table)
        print("-" * 120)
    elif len(args) == 3:
        if int(args[2]) in [x['id'] for x in books]:
            book = find_one_from_database(int(args[2]))
            table.field_names = headers
            table.add_row([x for x in book.values()])
            table.align['Book_Name'] = 'l'
            table.align['Curr.Page'] = 'c'
            print(table.get_string(border=True))
    # Print to the beautiful tables

    elif len(args) == 2:
        print("Fetching the latest data...")
        table.field_names = headers
        table.add_rows(rows)
        # table.border = True
        table.align['Book_Name'] = 'l'
        table.align['Curr.Page'] = 'c'
        print(table.get_string(border=True))