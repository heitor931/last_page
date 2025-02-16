import sys
from datetime import date, datetime
from colorama import Fore, Back, Style
#import time

# import uuid
from prettytable.colortable import ColorTable, Themes
import pretty_tables as pt
from utils import post_to_database, get_all_books, insert_to_database, delete_book, find_one_from_database, \
    quick_update_book, generate_weekdays, delete_all_books

args = sys.argv
books = get_all_books()
current_date_time = f"{datetime.now().day}/{generate_weekdays(False, True)},{datetime.now().hour}:{datetime.now().minute},{generate_weekdays(True)}"
table = ColorTable(theme=Themes.HIGH_CONTRAST)

if args[1] == 'list':
    headers = ["id", "Book_Name", "Curr.Page", "Last time read", "Num.Pages", "Started_Date", "Due_date", "Completed"]
    rows = [[x["id"], x["book_name"], x['current_page'], x['last_page_date'], x["total_pages"], x['start_date'],
             x['due_date'], x['completed']] for x in books]
    if len(args) == 3 and args[2] == 'tab1':
        table = pt.create(
            headers=headers,
            rows=rows,
            colors=[pt.Colors.white, pt.Colors.red, pt.Colors.yellow, pt.Colors.blue, pt.Colors.cyan, pt.Colors.green, pt.Colors.purple,pt.Colors.black],
        )
        # )
        #print("-" * 120)
        print(table)
        #print("-" * 120)
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

    # Get updated data from database
    # Get the latest data

# Updating the pages
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
                if book['current_page'] == sanitized_choice:
                    book['completed'] = True
                post_to_database(book)
                print("Updated successfully!")
            except ValueError as e:
                print('Not a valid choice')
    elif len(args) == 3:
        pass
        if int(args[2]) in [x['id'] for x in books]:
            for book in books:
                if int(args[2]) == book['id']:
                    try:
                        choice = (input(f"{book['book_name']} - [Current page]: "))
                        if not choice:
                            continue
                        else:
                            sanitized_choice = int(choice)
                        book["current_page"] = sanitized_choice
                        book["last_page_date"] = current_date_time
                        if book['current_page'] == book['total_pages']:
                            book['completed'] = True
                        post_to_database(book)
                        print("Updated successfully!")
                        break
                    except ValueError as e:
                        print('Not a valid choice')
        else:
            print(Fore.RED + "There is no book with this Id")
    elif len(args) == 4:
        if int(args[2]) in [x['id'] for x in books]:
            for book in books:
                if int(args[2]) == book['id']:
                    try:
                        sanitized_choice = int(args[3])
                        book["current_page"] = sanitized_choice
                        book["last_page_date"] = current_date_time
                        if book['current_page'] == sanitized_choice:
                            book['completed'] = True
                        quick_update_book(book)
                        print(Fore.LIGHTGREEN_EX +  f"{book['book_name']} updated current page successfully!")
                        find_one_from_database(book['id'])
                        break
                    except ValueError as e:
                        print('Not a valid choice')
        else:
            print(Fore.RED + "There is no book with this Id")

# Create new Books for reading
elif args[1] == "add":
    track_list = [0] if len(books) == 0 else [int(x['id']) for x in books]
    while True:
        book_name = input("What is the name of the Book? ")
        total_pages = int(input("Whats the number of pages?: "))
        due_date = input('What is the scheduled due date?:')
        book = {
            "id": max(track_list) + 1,
            "book_name": book_name,
            "current_page": 0,
            'last_page_date': "",
            'total_pages': total_pages,
            'start_date': str(date.today()),
            'due_date': due_date,
            'completed': False,
            #'last_page_date': f"{date.today}-{current_time}"
        }
        print(book)
        track_list.append(book)
        insert_to_database(book)
        print(Fore.BLUE + "Book created successfully")
        print('-'*70)
        more = input('Do you want to add more books?[Y/N]')

        if more.lower() == 'n':
            break
        get_all_books()

# Delete books from the list
elif args[1] == 'delete':
    if args[2] == 'all':
        delete_all_books()
        print(Fore.RED + "All books deleted successfully")
    else:
        for book in books:
            if int(args[2]) in [x['id'] for x in books]:
                delete_book(int(args[2]))
                print(Fore.RED + f"{book['Book_name'] } book deleted successfully")
                break
            else:
                print(Fore.RED + "There is no book with this Id")
                break



# Usage of the application
elif args[1].lower() == "usage":
    print("USAGE:")
    print("=" * 30)
    print("Without arguments, get updated page numbers")
    print("options: list | add | update | to_excel | to_pdf")
    print("update: update the page numbers of the books")
    print("create: Create new books")


