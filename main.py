"""
L.H. Wong 2024-01-17
This is sample Library system utilises List and Dictionary in Python
"""

import datetime
import random
# Book Inventory
books = {
    'Book A': { 'copies': 5, 'borrowers': [] },
    'Book B': { 'copies': 4, 'borrowers': [] },
    'Book C': { 'copies': 3, 'borrowers': [] },
    'Book D': { 'copies': 1, 'borrowers': [] }
}

# User Database
users = {
    'User A': { 'name': 'John', 'books': [], 'fine': 0.0 },
    'User B': { 'name': 'Peter', 'books': [], 'fine': 0.0 },
    'User C': { 'name': 'Matt', 'books': [], 'fine': 0.0 }
}

NO_BOOK_PER_USER = 3
FINE_PER_DAY = 0.05

def checkout_book(book_name, user_name) -> None:
    """
    Check out book for specific user.
    """
    if len(books[book_name]['borrowers']) < books[book_name]['copies'] and len(users[user_name]['books']) < NO_BOOK_PER_USER:
        if user_name in [borrower['user'] for borrower in books[book_name]['borrowers']]:
            print(f'{users[user_name]["name"]} has already borrowed the book {book_name}.')
        else:
            # Randomise the expiry date for simulation
            expiry = datetime.date(2024, 1, random.randint(1,datetime.date.today().day))
            books[book_name]['borrowers'].append({ 'user': user_name, 'expiry_date': expiry })
            users[user_name]['books'].append(book_name)
            print(f'{book_name} is borrowed by {users[user_name]["name"]} successfully.')
            print(f'The book must be return on or before {str(expiry)}.')
    else:
        print(f'Checkout failed. {book_name} is not available or {users[user_name]["name"]} cannot borrow more books.')

def checkin_book(book_name, user_name) -> None:
    """
    Check in book for specific user.
    It also calculates the fine for days overdued.
    """
    if book_name in users[user_name]['books']:
        users[user_name]['books'].remove(book_name)
        for borrower in books[book_name]['borrowers']:
            if borrower['user'] == user_name:
                if borrower['expiry_date'] < datetime.date.today():
                    datediff = datetime.date.today() - borrower["expiry_date"]
                    print(f'Expired for {datediff.days} days.')
                    users[user_name]['fine'] += round(datediff.days * FINE_PER_DAY, 2)
                books[book_name]['borrowers'].remove(borrower)
                break
        print(f'{book_name} is returned successfully.')
        if users[user_name]['fine'] > 0:
            print(f'Please pay the fine £{users[user_name]["fine"]}.')
    else:
        print(f'Error: {book_name} is not borrowed by {users[user_name]["name"]}.')

def pay_fine(user_name, amount):
    """
    Pay the find for specific user.
    """
    if users[user_name]['fine'] == 0:
        print('There is no fine overdued.')
    elif amount > users[user_name]['fine']:
        diff = round(amount - users[user_name]['fine'],2)
        users[user_name]['fine'] = 0
        print(f'Fine paid. Please collect the change £{diff}.')
    else:
        users[user_name]['fine'] = round(users[user_name]['fine'] - amount, 2)
        if users[user_name]['fine'] > 0:
            print(f'Fine paid. There is still £{users[user_name]["fine"]} dued.')

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
