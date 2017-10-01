import csv
import os.path

with open('contacts.csv') as f:
    mydict = dict(filter(None, csv.reader(f)))


def menu_choices():  # initiating an instance of menu choices to loop in the cli
    print("1. Add new user")
    print("2. Login user")
    return input("Please enter your choice (1-2): ")


def registration():
    email = input('Your email: ')
    password = input('Your password')
    file_exist = os.path.exists('contacts.csv')
    with open('contacts.csv', 'a') as csv_file:
        headers = ['email', 'password']
        writer = csv.DictWriter(csv_file, headers)

        if not file_exist:
            writer.writeheader()

        writer.writerow({'email': email, 'password': password})
    mydict[email] = password


def login():
    email = input("Enter email: ")
    password = input("Enter password: ")

    # check if user exists and login matches password
    if email in mydict and mydict[email] == password:
        print("\nLogin successful!\n")
    else:
        print("\nUser doesn't exist or wrong password!\n")


choice = menu_choices()
while choice != "3":
    if choice == "1":
        registration()

    if choice == "2":
        login()
    choice = menu_choices()
