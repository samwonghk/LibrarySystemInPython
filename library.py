import datetime
import random

FINE_PER_DAY = 0.05
NO_BOOK_PER_USER = 3

class Book():
    def __init__(self, copies):
        self.copies = copies
        self.borrowers = []

    def checkout(self, user_name) -> datetime.date:
        if len(self.borrowers) < self.copies:
            borrower = Borrower(user_name)
            expiry_date = datetime.date(2024, 1, random.randint(1,datetime.date.today().day))
            borrower.set_expiry(expiry_date)
            self.borrowers.append(borrower)
            return expiry_date
        else:
            return None

    def checkin(self, user_name) -> (int, float):
        borrower = None
        overdue = None
        for borrow in self.borrowers:
            if user_name in [borrower.user_name for borrower in self.borrowers]:
                borrower = borrow
                overdue_diff = datetime.date.today() - borrower.expiry_date
                overdue = overdue_diff.days
                return (overdue, round(overdue * FINE_PER_DAY, 2))
        return None

class Borrower():
    def __init__(self, user_name):
        self.user_name = user_name
        self.expiry_date = None

    def set_expiry(self, expiry_date):
        self.expiry_date = expiry_date

class User():
    def __init__(self, name):
        self.name = name
        self.books = []
        self.fine = 0.0

    def borrow_book(self, book):
        self.books.append(book)

    def return_book(self, book):
        self.books.remove(book)

