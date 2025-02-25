import sys
from datetime import date, datetime
from colorama import Fore, Back, Style
from prettytable.colortable import ColorTable, Themes
from utils import post_to_database, get_all_books, insert_to_database, delete_book, find_one_from_database, \
    quick_update_book, generate_weekdays, delete_all_books, show_tables

args = sys.argv
books = get_all_books()
current_date_time = f"{datetime.now().day}/{generate_weekdays(False, True)},{datetime.now().hour}:{datetime.now().minute},{generate_weekdays(True)}"
table = ColorTable(theme=Themes.HIGH_CONTRAST)


# List all
if args[1] == 'list':
    # Print table
    show_tables(books, args)


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


