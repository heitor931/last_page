import sys
from datetime import date, datetime
import time

# import uuid
import pretty_tables as pt
from utils import post_to_database, get_all_books, insert_to_database


args = sys.argv
books = get_all_books()
current_time = f"{datetime.now().hour}: {datetime.now().minute}"  


if len(args) == 1:
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
    print("-" * 97)

    print(table)

    print("-" * 97)

    # Get the latest data
elif args[1] == "update":

    for book in books:
        choice = int(input(f"{book['book_name']}: "))
        if choice:
            book["last_page"] = choice
            # book['id'] = len(books) + 1
    for book in books:
        post_to_database(book)
    print("Updated successfully!")

elif args[1] == "create":
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
            break

elif args[1].lower() == "usage":
    print("USAGE:")
    print("=" * 30)
    print("Without arguments, get updated page numbers")
    print("options: update | create")
    print("update: Update the page numbers of the books")
    print("create: Create new books")
    

