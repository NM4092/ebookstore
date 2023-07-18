# Import sqlite3
import sqlite3

# Exception if database doesnt't exist
try:
 
# Connecting to 
# Database called 'ebookstore'
 book_connection = sqlite3.connect('ebookstore.db')
 c = book_connection.cursor()

except sqlite3.Error as e:
    print(e)

# Create table books
c.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, Title TEXT , Author TEXT , Qty INTEGER)')

# Insert book_data in table 
book_data = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]

# Insert book_data into books 
c.executemany("INSERT or IGNORE INTO books (id, Title, Author, Qty) VALUES (?,?,?,?)", book_data)

# Commit connection 
book_connection.commit()




# Function for viewing books currently in table 
def view_library():
    
    # Fetch all books in books table
    c.execute ('''SELECT * FROM books''')
    view_library = c.fetchall()
    print("\n Books currrently in the library: ")
    
    # Print each book present 
    for book in view_library:
                
                print(f'''
                ==============================
                ID: {book[0]} 
                Title: {book[1]}
                Author: {book[2]}
                Qty: {book[3]}
                ==============================
                ''')




# Fucntion for entering a new book into table 
def enter_book():

    print("You have selected to enter a new book, please follow the steps below: ")
    print("\n")
    
    # Id number to be incremented by 1 from the max value present in table
    # User to enter title of new book
    # User to enter author of new book
    id_max = c.execute('''SELECT MAX (id) FROM books''')
    id_new = id_max.fetchone()[0] +1
    title_new = input("Enter the book title:\n")
    author_new = input("Enter the author's name:\n")
    
    # Exception for ValueError
    try: 
         # User to enter the quantity of books
         qty_new = int(input("Enter the quantity of books:\n")) 
            
    except ValueError as Error:
         print(Error)
         print ("\nYou must enter a number quantity. Please try again.\n")
         return 
    
    # Check if title is already present in books
    for title in c.execute('''SELECT title FROM books'''):
         if title[0] == title_new:
             print("\nThis title is already present in the database. Please enter new title and try again.\n")
             return
         
    # Insert new book into books table
    c.execute('''INSERT INTO books (id, Title, Author, Qty)
      VALUES (?,?,?,?)''', (id_new, title_new, author_new, qty_new))
    # Commit connection
    book_connection.commit()

    print("\nNew book entry has been successfully added.\n")




# Function if user needs to update book details
def update_book():

    print("You have selected to update an existing book, please follow the steps below:\n ")
     
    # Exception for Value Error
    try: 
     
     # User to input an option from the menu below
     update_book = int(input("""\nPlease select from the following options:
                         
                           1- Update the quantity of a book
                           2- Change author name 
                           3- Change title name 
                           4- Return to main menu 
                           : """))

    except ValueError as Error:
        print(Error)
        print ("\nYou must enter a number quantity. Please try again.\n")
        return  
    
    # Call function
    view_library()
  
    # Exception handling ValueError
    try: 

        # User to enter the book id for updating 
        book_id = int(input("\nPlease enter the id of the book you wish to update: \n"))

    except ValueError as Error:
        print(Error)
        return
     
    # If user enters 1 
    if  update_book == 1:

        # Exception handling for ValueError
        try:

        # User to update the quantity of book relating the id entered
         update_qty = int(input("Please enter the new quantity of the selected book: "))
        
        except ValueError as Error:
         print(Error)
         return
        
        # Update book table with updated quantity
        c.execute('''UPDATE books SET Qty = ? WHERE id = ?''',(update_qty,book_id))
        # Commit connection
        book_connection.commit()

        print(f"\nYou have updated the book quantity by {update_qty}\n")
               
    # Elif user enters 2 
    elif update_book == 2:
        
          change_author = input("Please enter the authors name: ")
          c.execute('''UPDATE books SET Author= ? WHERE id= ? ''', (change_author, book_id))
          # Commit connection
          book_connection.commit()

          print(f"\nYou have updated the authors name.\n")

    # Elif user enter 3
    elif update_book == 3:
         # User to enter the title they want to update
         change_title = input( "Please enter the title of the book: ")
         # Books table to be updated with change of title 
         c.execute('''UPDATE books SET Author = ? WHERE id = ? ''', (change_title, book_id))
         # Commit connection
         book_connection.commit()

         print(f"\nYou have updated the title.\n")
    
    # Elif user enters 4
    elif update_book == 4:
         # User has chosen to leave update_menu
         # Return to book_menu
         return book_menu

    # Else:           
    else: 
         
         # User has not entered any of the options 
         # Return update_book menu
         print("You have chosen incorrectly, please try again.")
         return update_book




# Function for user to delete book from books
def delete_book(): 
    
    # Get all books from table present so far
    c.execute ('''SELECT * FROM books''')
    del_data = c.fetchall()
    
    # Print out each book
    for book in del_data:
        
        
        print(f'''
                ==============================
                ID: {book[0]} 
                Title: {book[1]}
                Author: {book[2]}
                Qty: {book[3]}
                ==============================
                ''')
        
    # Exception handling ValueError
    try:
        # User to enter the id of book they want to delete 
        del_book = int(input("Please enter the book id you wish to delete: "))

    except ValueError as Error:
        print(Error)
        return
    
    # User input is the same as index[0]
    del_book == book[0] 
    # Selected book to be deleted from the table 
    c.execute('''DELETE FROM books WHERE id = ?''', (del_book,))
    # Commit connection
    book_connection.commit()

    print(f"\n{book[1]} has been delete from the dataframe.\n")
    



# Function for user to search book in table
def search_book():
    # User to input the title of book they want to search
    search_title = input("Please enter the title of the book you wish to search: ")

    # Title of book to be selected from the table books
    # All the relevant information relating to the book title is produced
    c.execute('''SELECT * FROM books WHERE Title = ?''', (search_title,))
    book_search = c.fetchone()
    title_search = str(book_search).strip("()")
    book_connection.commit()

    print(f"\nThese are the details of the book you are looking for: {title_search}.\n")





""" eBookstore Database Menu """

print("Welcome to the ebookstore menu !")
print("\n")

# While statement for book menu
while True:
 
 # Exception handling 
 try:
     # User to input an option
     book_menu = int(input('''Select one of the following options below:
               
               
1 - Enter Book
2 - Update Book
3 - Delete Book
4 - Search Books
5 - View library
0 - Exit :    '''))


 except ValueError as Error:
     print(Error)
     book_menu()

# If statements based on user selection in book menu 
# Approproate functions are called based on selection
 if book_menu == 1:
    print("\n")
    enter_book()
        
 elif book_menu == 2:
     print("\n")
     update_book()
               
 elif book_menu == 3:
    print("\n")
    delete_book()
               
 elif book_menu == 4:
    print("\n")
    search_book()

 elif book_menu == 5:
     print("\n")
     view_library()
                       
 elif book_menu == 0:
    # Close database
    book_connection.close()

    print("\nThe database has been closed. Goodbye.")
    # Exit program
    exit()
  
 else:
     print("\nYou have not selected an option. Please try again.\n ")
              

# References - https://imudatascience.medium.com/importing-data-into-sqlite-via-python-f248cc23ebc2
#How to Import data into SQLite via Python (Json file/ MS Excel/ MS Access)?
#How to Import data into SQLite via Python (Json file/ MS Excel/ MS Access)?
#imudatascience.medium.com
# file:///C:/Users/naomi/Dropbox/NB22100004467/2%20-%20Data%20Analytics%20and%20Exploration/L2T05/DS%20L2T05%20-%20SQLite.pdf
# https://stackoverflow.com/questions/211501/using-sqlite-in-a-python-program
