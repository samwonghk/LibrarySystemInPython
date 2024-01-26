"""
Class Definition of Library System
"""
import datetime
import random

FINE_PER_DAY = 0.05
NO_BOOK_PER_USER = 3

class Book():
    """
    Book Class to store number of copies and list of borrowers
    """
    def __init__(self, copies):
        self.copies = copies
        self.borrowers = []

    def checkout(self, user_name) -> datetime.date:
        """
        Check out function
        """
        if len(self.borrowers) < self.copies:
            borrower = Borrower(user_name)
            expiry_date = datetime.date(datetime.date.today().year, datetime.date.today().month, random.randint(1,datetime.date.today().day))
            borrower.set_expiry(expiry_date)
            self.borrowers.append(borrower)
            return expiry_date
        return None

    def checkin(self, user_name) -> (int, float):
        """
        Check in function
        """
        borrower = None
        overdue = None
        for borrow in self.borrowers:
            if user_name in [borrower.user_name for borrower in self.borrowers]:
                borrower = borrow
                overdue_diff = datetime.date.today() - borrower.expiry_date
                overdue = overdue_diff.days
                self.borrowers.remove(borrower)
                return (overdue, round(overdue * FINE_PER_DAY, 2))
        return None

class Borrower():
    """
    Borrower class to store borrower's id and the date of expiry date of the borrow
    """
    def __init__(self, user_name):
        self.user_name = user_name
        self.expiry_date = None

    def set_expiry(self, expiry_date):
        """
        Set Expiry Date
        """
        self.expiry_date = expiry_date

class User():
    """
    User class to store User information
    """
    def __init__(self, name):
        self.name = name
        self.books = []
        self.fine = 0.0

    def borrow_book(self, book):
        """
        To add a book to the borrow list
        """
        self.books.append(book)

    def return_book(self, book):
        """
        To remove a book from the borrow list
        """
        self.books.remove(book)

