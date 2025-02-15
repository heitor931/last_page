import sys
from datetime import date, datetime
#import time

# import uuid
import pretty_tables as pt
from utils import post_to_database, get_all_books, insert_to_database


args = sys.argv
books = get_all_books()
current_date_time = f"{date.today()}-{datetime.now().hour}:{datetime.now().minute}"  


if args[1] == 'list':
    # Get updated data from database
    print("Fetching the latest data...")

    headers = ["id", "Book_Name","Curr.Page","Last time read", "Num.Pages","Started_Date", "Due_date", "Completed" ]
    rows = [[x["id"], x["book_name"],x['current_page'],x['last_page_date'], x["total_pages"],x['start_date'], x['due_date'],x['completed']] for x in books]

    table = pt.create(
        headers=headers,
        rows=rows,
        colors=[pt.Colors.white, pt.Colors.red, pt.Colors.yellow, pt.Colors.blue, pt.Colors.cyan, pt.Colors.green, pt.Colors.purple,pt.Colors.black],
    )
    # )
    print("-" * 120)
    print(table)
    print("-" * 120)

    # Get the latest data
elif args[1] == "update":
    if len(args) == 2:
        for book in books:
            choice = (input(f"{book['book_name']} - [Current page]: "))
            if not choice:
                continue
            else:
                sanitized_choice = int(choice)
            try:
                book["current_page"] = sanitized_choice
                book["last_page_date"] = current_date_time
                if book['last_page_date'] == book['total_pages']:
                    book['completed'] = True
                post_to_database(book)
                print("Updated successfully!")
            except ValueError as e:
                print('Not a valid choice')
    elif len(args) >= 3:
        indexes = args[2:]
        print(indexes)
        for idx in indexes:
            if int(idx) in [x['id'] for x in books]:
                for book in books:
                    if int(idx) == book['id']:
                        try:
                            choice = (input(f"{book['book_name']} - [Current page]: "))
                            if not choice:
                                continue
                            else:
                                sanitized_choice = int(choice)
                            book["current_page"] = sanitized_choice
                            book["last_page_date"] = current_date_time
                            if book['last_page_date'] == book['total_pages']:
                                book['completed'] = True
                            post_to_database(book)
                            print("Updated successfully!")
                            break
                        except ValueError as e:
                            print('Not a valid choice')
            else:
                print("There is no book with this Id")

# Create new Books for reading
elif args[1] == "add":
    track_list = books.copy()
    while True:
        book_name = input("What is the name of the Book? ")
        total_pages = int(input("Whats the number of pages?: "))
        due_date = input('What is the scheduled due date?:')
        print('-'*70)
        more = input('Do you want to add more books?[Y/N]')
        
        book = {
            "book_name": book_name,
            "current_page": 0,
            "id": len(track_list) + 1,
            'start_date': str(date.today()),
            'due_date': due_date,
            'completed': False,
            'total_pages': total_pages,
            #'last_page_date': f"{date.today}-{current_time}" 
            'last_page_date': "" 
        }
        track_list.append(book)
        insert_to_database(book)
        if more.lower() == 'n':
            get_all_books()
            break

# Delete books from the list

# Usage of the application
elif args[1].lower() == "usage":
    print("USAGE:")
    print("=" * 30)
    print("Without arguments, get updated page numbers")
    print("options: list | add | update | to_excel | to_pdf")
    print("update: update the page numbers of the books")
    print("create: Create new books")
    

