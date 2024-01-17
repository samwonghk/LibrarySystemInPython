"""
L.H. Wong 2024-01-17
This is sample Library system utilises Class, List and Dictionary in Python
"""
import library

# Book Inventory
books = {
    'Book A': library.Book(5),
    'Book B': library.Book(4),
    'Book C': library.Book(3),
    'Book D': library.Book(1)
}

# User Database
users = {
    'User A': library.User('John'),
    'User B': library.User('Peter'),
    'User C': library.User('Matt')
}

NO_BOOK_PER_USER = library.NO_BOOK_PER_USER
FINE_PER_DAY = library.FINE_PER_DAY

def checkout_book(book_name, user_name) -> None:
    """
    Check out book for specific user.
    """
    if len(books[book_name].borrowers) < books[book_name].copies and len(users[user_name].books) < NO_BOOK_PER_USER:
        if user_name in [borrower.user_name for borrower in books[book_name].borrowers]:
            print(f'{users[user_name].name} has already borrowed the book {book_name}.')
        else:
            # Randomise the expiry date for simulation
            expiry = books[book_name].checkout(user_name)
            users[user_name].borrow_book(book_name)
            print(f'{book_name} is borrowed by {users[user_name].name} successfully.')
            print(f'The book must be return on or before {str(expiry)}.')
    else:
        print(f'Checkout failed. {book_name} is not available or {users[user_name].name} cannot borrow more books.')

def checkin_book(book_name, user_name) -> None:
    """
    Check in book for specific user.
    It also calculates the fine for days overdued.
    """
    if book_name in users[user_name].books:
        users[user_name].return_book(book_name)
        for borrower in books[book_name].borrowers:
            if borrower.user_name == user_name:
                (overdue, fine) = books[book_name].checkin(user_name)
                print(f'{book_name} is returned successfully.')
                if overdue > 0:
                    print(f'Expired for {overdue} days.')
                    users[user_name].fine += fine
                break
        if users[user_name].fine > 0:
            print(f'Please pay the fine £{users[user_name].fine}.')
    else:
        print(f'Error: {book_name} is not borrowed by {users[user_name].name}.')

def pay_fine(user_name, amount):
    """
    Pay the find for specific user.
    """
    if users[user_name].fine == 0:
        print('There is no fine overdued.')
    elif amount > users[user_name].fine:
        diff = round(amount - users[user_name].fine,2)
        users[user_name].fine = 0
        print(f'Fine paid. Please collect the change £{diff}.')
    else:
        users[user_name].fine = round(users[user_name].fine - amount, 2)
        if users[user_name].fine > 0:
            print(f'Fine paid. There is still £{users[user_name].fine} dued.')

if __name__ == '__main__':
    # Test on the concept
    checkout_book('Book A', 'User A')
    checkout_book('Book A', 'User A')
    checkout_book('Book D', 'User A')
    checkout_book('Book B', 'User A')
    checkout_book('Book C', 'User A')
    checkout_book('Book D', 'User C')

    checkin_book('Book D', 'User C')
    checkin_book('Book D', 'User A')
    pay_fine('User A', 0.55)
    pay_fine('User A', 0.1)
