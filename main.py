import sys
from post import post_to_database
from fetch import get_all_books
import uuid


args = sys.argv

if len(args) == 1:
    # Get updated data from database
    print('Fetching the latest data...')
    books_from_db = get_all_books()
    print('-'*20)
    for book in books_from_db:
        print(f"{book['book_name']}: {book['last_page']}")
    print('-'*20)
    
    # Get the latest data
elif args[1] == 'update':
    books = [{'book_name': 'Web Security', 'id': "fdfgdfj", 'last_page': 0}, {'book_name': 'LPIC2', 'id': 'dhgchfchgdf7u65', 'last_page': 0} ]
    for book in books:
        choice = int(input(f"{book['book_name']}: "))
        if choice:
            book['last_page'] = choice
            #book['id'] = uuid.uuid4()
    for book in books:
        post_to_database(book)
    print("Updated sucessfully!")


