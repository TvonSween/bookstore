import sqlite3
import math
#user: bookstore clerk

class Book:
    def __init__(self, title, author, qty):
        super().__init__()
        #self.id = id
        self.title = title
        self.author = author
        self.qty = qty


def populate_table(filename):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                line = line.split(", ")
                if line[0] not in book_data:
                    book_data.append(line)
    except:
        print("Something went wrong when opening the file")
    
    # Clean up data - convert ID and quantity to integers
    book_data[2][1] = "The Lion, the Witch and the Wardrobe"
    book_data[1][1] = "Harry Potter and the Philosoper's Stone"
    for book in book_data:
        book[0] = int(book[0])
        book[3] = int(book[3])
    
    cursor.executemany('''INSERT or IGNORE INTO book(id, title, author, qty) VALUES(?,?,?,?)''', book_data)
    db.commit()
    
    
def input_number():
    while True:
        try:
            num = int(input("\n    Enter number: ").strip())
            break
        except ValueError:
            print("\n   Oops! That was not a valid entry. Try again...\n")
    return num


def confirm_choice(user_confirmation):
    user_confirmation = user_confirmation.upper()
    if user_confirmation == 'Y':
        return True
    elif user_confirmation == 'N': 
        return False
    else:
       print("\n    No book was updated or deleted. You must enter Y or N only")

def search_database(query):
    if query.isnumeric():
        cursor.execute('''SELECT * FROM book WHERE id LIKE ?''', (query,))
        search_result = cursor.fetchall()
        if search_result == []:
            return None
        else:
            return search_result
    elif query.isnumeric() == False:
        db_search_query = f'%{query}%'
        cursor.execute('''SELECT * FROM book WHERE title LIKE ?''', (db_search_query,))
        search_result = cursor.fetchall()
        if search_result == []:
            return None
        else:
            return search_result
    else:
        print("    Value entered not recognised. Try searching again.")
            
    
# Initialise an empty list to store imported book data
book_data = []

#Create a db called ebookstore and a table called book
#title is primary key to prevent duplicate entries of same title
try:
    db = sqlite3.connect('ebookstore_db')
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS book(id INTEGER NOT NULL PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)
                    ''')
    db.commit()
except Exception as DatabaseError:
    raise DatabaseError

# Call the function to populate the database book table for further use in your program.
populate_table("book_input.txt") 

while True:
    #present the user with choice menu
    print('''\nWould you like to:
    1. Enter a book
    2. Update book
    3. Delete a book
    4. Search books
    0. Exit
   ''')
    user_choice = input_number()
       
    if user_choice == 1:
        #add new books to the database
        book_title = input("    Enter the book title: ")
        search_result = search_database(book_title)
        if search_result == None:
            author_name = input("    Enter the author's name: ")
            print("    How many copies of the book are there? ")
            num_of_books = input_number()
            new_book = Book(book_title, author_name, num_of_books)
            print(new_book.title)
            cursor.execute('''INSERT or IGNORE INTO book(title, author, qty) VALUES(?,?,?)''', (new_book.title, new_book.author, new_book.qty))
            db.commit()
            print('\n   Book added!')
        else:
            print("    Sorry a title matching this already exists: ")
            for book in search_result:
                print('     {0} : {1} : {2} : {3}'.format(book[0], book[1], book[2], book[3]))
        db.commit()
       
    elif user_choice == 2:
        #update book info
        user_confirmation = input('\n   Do you know the ID number of the book you wish to update, Y or N? ').strip()
        choice = confirm_choice(user_confirmation)
        if choice: 
            book_id = input("    Enter the correct book id: ")
            #  check id given by user is in db
            search_result = search_database(book_id)
            if search_result == None:
                print("    Sorry, no matches found with that book ID. Try again.")
            else: 
                while True: 
                    print('''\nWould you like to:
                    1. Update title only
                    2. Update author only
                    3. Update quantity only
                    4. Update all
                    0. Exit
                    ''')
                    update_choice = input_number()
                
                    if update_choice == 1:
                        book_title =  input("    Enter the correct book title: ")
                        cursor.execute('''UPDATE book SET title = ? WHERE id = ? ''', (book_title, book_id))
                        db.commit()
                        print('\n    Title updated!')
                        
                    if update_choice == 2:
                        author_name = input("    Enter the correct author's name: ")
                        cursor.execute('''UPDATE book SET author = ? WHERE id = ? ''', (author_name, book_id))
                        db.commit()
                        print('\n    Author updated!')
                    
                    if update_choice == 3: 
                        print("    Enter the correct quantity of books: ")
                        num_of_books = input_number()
                        cursor.execute('''UPDATE book SET qty = ? WHERE id = ? ''', (num_of_books, book_id))
                        db.commit()
                        print('\n   Quantity updated!')
                
                    if update_choice == 4:
                        book_title =  input("    Enter the correct book title: ")
                        author_name = input("    Enter the correct author's name: ")
                        print("    Enter the correct quantity of books: ")
                        num_of_books = input_number()
                        cursor.execute('''UPDATE book SET title = ?, author = ?, qty = ? WHERE id = ? ''', (book_title, author_name, num_of_books, book_id))
                        db.commit()
                        print('\n    Book entry updated!')
                        
                    if update_choice == 0:
                        print("    Exiting updates. Returning to main menu.")
                        break   
                        
        elif choice == False:
            print("   If you don't know the ID, first search the database using Option 4.")
            
        else:
            print("\n   Oops! Something went wrong. Try again.")
    
    
    elif user_choice == 3:
        #delete a book
        book_id = input('''  Enter ID of book you wish to delete. 
        (If you don't know the ID, first search the database using Option 4):
        ''').strip()
        user_confirmation = input("\n   Are you sure you want to delete this book? Enter Y or N: ").strip()
        choice = confirm_choice(user_confirmation)
        if choice:
            #  check id given by user is in db
            search_result = search_database(book_id)
            if search_result == None: 
                print("   Sorry, no matches found with that book ID. Try again.")
            else: 
                cursor.execute('''DELETE FROM book WHERE id = ? ''', (book_id,))
                print('\n    Book deleted!')
        elif choice == False:
             print('\n  Book not deleted')
        else:
            print("\n   Oops! Something went wrong. Try again.")
    
    elif user_choice == 4:
        #search the db for a specific book - adding % wildcards around search term to allow user to enter any phrase
        search_query = input("    Enter search query: ")
        print('\n      ****SEARCH RESULTS****: \n')
        print('\n      ** ID ** TITLE ** AUTHOR **  QUANTITY **')
        print('      _______________________________________________________________')
        search_result = search_database(search_query)
        if search_result == None:
            print("    Sorry, no matches for your search")
        else:
            for book in search_result:
                print('     {0} : {1} : {2} : {3}'.format(book[0], book[1], book[2], book[3]))
        db.commit()
    
    elif user_choice == 0:
        print("\nClosing database connection. Goodbye")
        db.close()
        break
    
    else:
        print("    Oops - Incorrect input.")


