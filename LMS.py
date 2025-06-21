import os
from datetime import datetime, timedelta

# File Paths
BOOKS_FILE = "books.txt"
MEMBERS_FILE = "members.txt"
TRANSACTIONS_FILE = "transactions.txt"

# Book Class
class Book:
    def __init__(self, book_id, title, author, total_books, available_books):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_books = total_books
        self.available_books = available_books

    def borrow(self):
        if self.available_books > 0:
            self.available_books -= 1
            return True
        return False

    def return_book(self):
        if self.available_books < self.total_books:
            self.available_books += 1
            return True
        return False

    def __str__(self):
        return f"{self.book_id}|{self.title}|{self.author}|{self.total_books}|{self.available_books}"

# Member Class
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def __str__(self):
        return f"{self.member_id}|{self.name}"

   

# Library Management System
class Library:
    def __init__(self):
        self.books = self.load_books()
        self.members = self.load_members()
        self.transactions = self.load_transactions()

    def display_members(self):
        if not self.members:
            print("No registered members.")
        else:
            print("Registered Members:")
            for member in self.members:
                print(f"Member ID: {member.member_id}, Name: {member.name}")

    def load_books(self):
        books = []
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, "r") as file:
                for line in file:
                    book_id, title, author, total, available = line.strip().split("|")
                    books.append(Book(int(book_id), title, author, int(total), int(available)))
        return books

    def load_members(self):
        members = []
        if os.path.exists(MEMBERS_FILE):
            with open(MEMBERS_FILE, "r") as file:
                for line in file:
                    member_id, name = line.strip().split("|")
                    members.append(Member(int(member_id), name))
        return members

    def load_transactions(self):
        transactions = []
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "r") as file:
                transactions = [line.strip() for line in file]
        return transactions

    def save_books(self):
        with open(BOOKS_FILE, "w") as file:
            for book in self.books:
                file.write(str(book) + "\n")

    def save_members(self):
        with open(MEMBERS_FILE, "w") as file:
            for member in self.members:
                file.write(str(member) + "\n")

    def save_transactions(self):
        with open(TRANSACTIONS_FILE, "w") as file:
            for transaction in self.transactions:
                file.write(transaction + "\n")

    def insert_book(self):
        book_id = len(self.books) + 1
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        total_books = int(input("Enter Total Copies: "))
        new_book = Book(book_id, title, author, total_books, total_books)
        self.books.append(new_book)
        self.save_books()
        print("Book added successfully!")

    def update_book(self):
        book_id = int(input("Enter Book ID to update: "))
        for book in self.books:
            if book.book_id == book_id:
                book.title = input("Enter new title: ") or book.title
                book.author = input("Enter new author: ") or book.author
                book.total_books = int(input("Enter new total copies: "))
                book.available_books = book.total_books  # Reset available books
                self.save_books()
                print("Book updated successfully!")
                return
        print("Book not found.")

    def delete_book(self):
        book_id = int(input("Enter Book ID to delete: "))
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_books()
        print("Book deleted successfully!")

    def register_member(self):
        member_id = len(self.members) + 1
        name = input("Enter Name: ")
        new_member = Member(member_id, name)
        self.members.append(new_member)
        self.save_members()
        print("Member registered successfully!")

    def borrow_book(self):
        member_id = int(input("Enter Member ID: "))
        book_id = int(input("Enter Book ID: "))
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not member:
            print("Member not found. Please register first.")
            return
        if not book:
            print("Book not found.")
            return
        if book.borrow():
            self.transactions.append(f"{member.name} borrowed {book.title} on {datetime.now().strftime('%Y-%m-%d')}")
            self.save_books()
            self.save_transactions()
            print("Book borrowed successfully!")
        else:
            print("Book is not available.")

    def return_book(self):
        book_id = int(input("Enter Book ID to return: "))
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book and book.return_book():
            self.transactions.append(f"{book.title} was returned on {datetime.now().strftime('%Y-%m-%d')}")
            self.save_books()
            self.save_transactions()
            print("Book returned successfully!")
        else:
            print("Invalid return attempt.")

    def display_books(self):
        for book in self.books:
            print(f"{book.book_id}. {book.title} by {book.author} - {book.available_books}/{book.total_books} available")

    def display_transactions(self):
        for transaction in self.transactions:
            print(transaction)

# Run Library System
library = Library()
while True:
    print("\nLibrary Management System")
    print("1. Display Books")
    print("2. Insert Book")
    print("3. Update Book")
    print("4. Delete Book")
    print("5. Register Member")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. Display Transactions")
    print("9. Display Members")
    print("10. Exit")
    
    choice = input("Enter choice: ")
    if choice == '1':
        library.display_books()
    elif choice == '2':
        library.insert_book()
    elif choice == '3':
        library.update_book()
    elif choice == '4':
        library.delete_book()
    elif choice == '5':
        library.register_member()
    elif choice == '6':
        library.borrow_book()
    elif choice == '7':
        library.return_book()
    elif choice == '8':
        library.display_transactions()
    elif choice == '9':
        library.display_members()
    elif choice == '10':
        break
    else:
        print("Invalid choice. Try again.")
