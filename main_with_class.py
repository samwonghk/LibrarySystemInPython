"""
L.H. Wong 2024-01-17
This is sample Library system utilises Class, List and Dictionary in Python
"""
import library

# Book Inventory
books = {
    'Alice in Wonderland': library.Book(2),
    '1984': library.Book(1),
    'Animal Farm': library.Book(1),
    'Illid': library.Book(1),
    'Lord of the Rings': library.Book(1),
    'Hobbits': library.Book(1)
}

# User Database
users = {
    '00001': library.User('John'),
    '00002': library.User('Peter'),
    '00003': library.User('Matt'),
    '00004': library.User('Colin'),
    '00005': library.User('Eger')
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
    elif len(books[book_name].borrowers) >= books[book_name].copies:
        print(f'Checkout failed. {book_name} is not available.')
    else:
        print(f'{users[user_name].name} cannot borrow more books.')

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
            pay_fine_info(user_name)
    else:
        print(f'Error: {book_name} is not borrowed by {users[user_name].name}.')

def pay_fine(user_name, amount):
    """
    Pay the fine for specific user.
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
        else:
            print('All fine paid.')

def show_menu():
    """
    Show the main menu and ask for selection
    """
    try:
        print('=' * 50)
        print('\t\tBookworm Library')
        print('=' * 50)
        for key, value in menu.items():
            print(f'\t\t{key} - {value["desc"]}')
        print('=' * 50)
        selection = int(input('Selection: '))
        function = menu[selection]['function']
        # print(function)
        function()
    except ValueError:
        print('Please enter a valid menu number')
    except KeyError:
        print('System malfunctioning...')
    return

def checkout_info():
    """
    Ask for the user id and the book to be borrowed
    """
    print()
    print()
    user_id = None
    while not user_id:
        user_id = input('Please input your user id (5-digit number): ')
        if not user_id in users:
            user_id = None
    print(f'Welcome, {users[user_id].name}.')
    book_title = None
    while not book_title:
        book_title = input('Please input the book title (-1 to list all books, bye to exit): ').strip()
        if book_title == '-1':
            book_title = None
            for key in books:
                print(key)
        elif book_title.lower() == 'bye':
            book_title = None
            break
        if not book_title in books:
            book_title = None
    if book_title:
        checkout_book(book_title, user_id)
    print()
    print()
    return

def checkin_info():
    """
    Ask for the user id and the book to be returned
    """
    print()
    print()
    user_id = None
    while not user_id:
        user_id = input('Please input your user id (5-digit number): ')
        if not user_id in users:
            user_id = None
    print(f'Welcome, {users[user_id].name}.')
    if len(users[user_id].books) > 0:
        print('Books borrowed:')
        for book in users[user_id].books:
            print(book)
        book_title = None
        while not book_title:
            book_title = input('Please input the book title to be returned (-1 to list, bye to exit): ').strip()
            if book_title == '-1':
                book_title = None
                for book in users[user_id].books:
                    print(book)
            elif book_title.lower() == 'bye':
                book_title = None
                break
            if not book_title in users[user_id].books:
                book_title = None
        if book_title:
            checkin_book(book_title, user_id)
    else:
        print("You have not borrowed any book.")
    print()
    print()
    return

def pay_fine_info(user_id = None):
    """
    Ask for the user id and the fine to be repaid
    """
    print()
    print()
    while not user_id:
        user_id = input('Please input your user id (5-digit number): ')
        if not user_id in users:
            user_id = None
    print(f'Welcome, {users[user_id].name}.')
    print(f'Fine dued: £{users[user_id].fine}')
    try:
        payment = -1
        while payment < 0:
            payment = float(input('How much would you pay: £'))
            if payment < 0:
                print('Please enter 0 or a positive value.')
        pay_fine(user_id, payment)
    except ValueError:
        print('Invalid input.')

    print()
    print()
    return

# Menu Items: desc is item description, function is the function to be called with exec()
menu = {
    1: { 'desc': 'Borrow a Book', 'function': checkout_info },
    2: { 'desc': 'Return a Book', 'function': checkin_info },
    3: { 'desc': 'Pay fine', 'function': pay_fine_info },
    4: { 'desc': 'Exit', 'function': quit }
}

# Main program
if __name__ == '__main__':
    while True:
        show_menu()
