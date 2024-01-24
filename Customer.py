# Author: Oluwakemi Toluwalase Obadeyi
# Date: 03/10/2023

# Import Libraries
import sqlite3
import time
import datetime
from datetime import datetime
from Data import create_connection, cancel_previous_booking, get_bookings, get_drivers


# Indicating the Database Connection File
database = "tbs.db3"

# Creating database connection to the SQLite database
conn = create_connection(database)

if not conn:
    print("Error! cannot create the database connection.")
    exit()

existing_customer = None

print("Welcome to RydeEasy")


# Defining function for customer sign in data entry
def signin_customer():
    check_customer = input("Have you previously signed up with us? (yes/no): ")
    if check_customer in ("y", "Y", "yes", "Yes"):
        current_customer()
    elif check_customer in ("n", "N", "no", "No"):
        new_customer()
    else:
        print("Invalid email address or password. please enter y for yes or n for no")
        signin_customer()


# Defining function for new customer data entry and writing to database
def new_customer():
    global existing_customer
    print("Sign Up")
    found = 0
    while found == 0:
        email = input("Please enter your email address: ")
        with sqlite3.connect("tbs.db3") as db:
            cursor = db.cursor()
            find_customer = "SELECT * FROM customers WHERE email = ?"
            cursor.execute(find_customer, [email])

            if cursor.fetchall():
                try_again_or_signin = input(
                    "An account has already been created using this email address., "
                    "enter t to try again or enter s to signin: "
                )
                if try_again_or_signin in ("t", "T"):
                    new_customer()
                elif try_again_or_signin in ("s", "S"):
                    print()
                    current_customer()
                else:
                    print("Invalid email address or password. Redirecting...")
                    signin_customer()

            else:
                found = 1

    title = input("Enter your title: ")
    firstname = input("Enter your first name: ")
    lastname = input("Enter your last name: ")
    phone_number = input("Enter your phone number: ")
    address = input("Enter your address: ")
    town = input("Enter your town: ")
    county = input("Enter your county: ")
    postcode = input("Enter your postcode: ")
    payment_method = input("Enter your payment method: ")
    password = input("Create password (Case Sensitive): ")
    cpassword = input("Confirm your password: ")
    while password != cpassword:
        print("Passwords does not match!")
        password = input("Create password (Case Sensitive): ")
        cpassword = input("Confirm your password: ")

    input_data = """INSERT INTO Customers(title, firstname, lastname, phone_number, 
    email, password, address, town, county, postcode, payment_method)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(
        input_data,
        [
            title,
            firstname,
            lastname,
            phone_number,
            email,
            password,
            address,
            town,
            county,
            postcode,
            payment_method,
        ],
    )
    db.commit()

    sql = """ SELECT * FROM Customers WHERE email=? AND password=?"""

    cursor.execute(sql, (email, password))
    first = cursor.fetchall()[0]

    # Current customer ID
    existing_customer = first[0]
    print("You have successfully created an account")
    time.sleep(1)
    customer_menu()


# Reading from database, existing Customer Sign In function
while True:

    def current_customer():
        global existing_customer
        print("Please Sign In")
        email = input("Enter your email address: ")
        password = input("Enter your password: ")
        with sqlite3.connect("tbs.db3") as db:
            cursor = db.cursor()
        find_signin = "SELECT * FROM Customers WHERE email = ? AND password = ?"
        cursor.execute(find_signin, [email, password])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Successfully signed in! Welcome " + i[2])
                # current customer ID for later use
                existing_customer = i[0]
                customer_menu()
                break

        else:
            print("Invalid email or password!")
            retry = input("Would you like to try again? yes/no: ")
            if retry in ("y", "Y", "yes", "Yes"):
                current_customer()
            elif retry in ("n", "N", "no", "No"):
                print("Goodbye!")

    break


# Defining function to view customer menu after signup or signin
def customer_menu():
    print("Main Menu")
    global existing_customer
    print("1. Book RydeEasy")
    print("2. View Previous Bookings")
    print("3. Cancel Booking")
    print("4. Sign Out")

    menu_input = input("Please indicate: ")
    if menu_input == "1":
        book_new_taxi()
    if menu_input == "2":
        previous_bookings(existing_customer)
    if menu_input == "3":
        cancel_booking()
    if menu_input == "4":
        exit()


# Taxi Booking form function
def book_new_taxi():
    global existing_customer
    print("\n")
    print("RydeEasy Booking Menu")

    drivers = get_drivers(conn)
    print("Available Drivers:")
    for i, driver in enumerate(drivers):
        print(str(i) + "." + str(driver[1]) + " " + str(driver[3]))

    # UniqueID for entities
    _input = input("Select option: ")
    index = int(_input)
    driver = drivers[index]
    driverid = driver[0]
    customerid = existing_customer

    # Date and time when the booking was made.
    print("Enter the date booked: ")
    now = datetime.now()  # Current date and time
    datebooked = now.strftime("%d/%m/%Y, %H:%M:%S")
    print("Date and time when the booking was made:", datebooked)

    # Addresses and postcodes
    print("Your current address is")
    start_address = input("Enter your pick-up address: ")
    start_postcode = input("Enter your pick-up postcode: ")
    print("Your destination address is")
    destination_address = input("Enter your drop-off address: ")
    destination_postcode = input("Enter your drop-off postcode: ")

    # Date of Pick-up
    print("Enter the pick-up date: ")
    date = input("DD/MM/YYYY: ")

    # Time of pick-up
    print("Time: ")
    time1 = int(time.time())
    print(time1)

    # Confirmation of booking status
    print("Booking status: Approved/Pending/Cancelled")
    status = input("Enter your booking status: ")

    # Confirmation of payment status
    print("Payment status confirmation ")
    paid = input("Yes/No: ")

    print("Thank you for choosing RydeEasy!")
    print(
        "Your pick-up address is: number "
        + start_address
        + ", postcode "
        + start_postcode
        + ""
    )
    print(
        "Booking RydeEasy to: number "
        + destination_address
        + ", postcode "
        + destination_postcode
        + ""
    )

    # Customer Information Verification
    while True:
        answer = input("Verify if this information is correct? y/n: ")
        if answer in ("n", "N", "no", "No"):
            print("Please start again")
            print("__________________")
            customer_menu()
        elif answer in ("y", "Y", "yes", "Yes"):
            # Adding Booking to Database
            with sqlite3.connect("tbs.db3") as db:
                cursor = db.cursor()

            sql = """INSERT INTO Bookings (driverid, customerid, datebooked, start_address, start_postcode,
            destination_address, destination_postcode, date, time1, status, paid) VALUES(?,?,?,?,?,?,?,?,?,?,?) """
            data = (
                driverid,
                customerid,
                datebooked,
                start_address,
                start_postcode,
                destination_address,
                destination_postcode,
                date,
                time1,
                status,
                paid,
            )
            cursor.execute(sql, data)
            db.commit()
            print(
                "Your ride has been successfully booked. Have a great experience with RydeEasy!"
            )
            time.sleep(3)
            print("Redirecting to RydeEasy Customer main menu")
            customer_menu()


# Defining function to view available booking(s)
def previous_bookings(customerid):
    print("\n")
    print("Previous Bookings")
    with sqlite3.connect("tbs.db3") as db:
        cursor = db.cursor()

    # Bookings which belong to the current customer
    sql = """ SELECT * FROM Bookings WHERE customerid=?"""
    cursor.execute(sql, (customerid,))
    bookings = cursor.fetchall()
    if not bookings:
        print("No bookings available, Redirecting to RydeEasy Customer main menu")
        time.sleep(2)
        customer_menu()
    else:
        # Show available booking function
        for i, b in enumerate(bookings, 1):
            print(
                str(i) + ") "
                "Start Address: "
                "" + str(b[4]) + " Postcode: "
                "" + str(b[5]) + " Time: "
                "" + str(b[6]),
                """ -> Destination Address: """ + str(b[7]) + " Postcode: "
                "" + str(b[8]) + " Date: "
                "" + str(b[9]),
            )

    # Previous menu function
    print("\n")
    return_menu = input(
        " Enter r to return to the main menu or enter c to cancel booking: "
    )
    if return_menu in ("r", "R", "return", "Return"):
        print("\n")
        customer_menu()
    elif return_menu in ("c", "C", "cancel", "Cancel"):
        print("\n")
        cancel_booking()
    else:
        print(
            "Invalid email address or password. Redirecting to RydeEasy Customer main menu"
        )
    customer_menu()


# Defining function to cancel or delete booking(s)
def cancel_booking():
    print("Cancel a booking")
    bookings = get_bookings(conn)  # connection to database

    if not bookings:
        print("There is no booking yet, redirecting to Admin Menu...")
        time.sleep(2)
        customer_menu()
    else:
        # Show all available bookings
        for i, b in enumerate(bookings, 0):
            print(
                str(i) + ") "
                "Start Address: "
                "" + str(b[4]) + " Postcode: "
                "" + str(b[5]) + " Time: "
                "" + str(b[6]),
                """ -> Destination Address: """ + str(b[7]) + " Postcode: "
                "" + str(b[8]) + " Date: "
                "" + str(b[9]),
            )

        _input = input("Select which booking you would like to cancel: ")
        index = int(_input)
        b = bookings[index]
        bookingid = b[0]

        cancel_previous_booking(conn, bookingid)
        print("Your booking has been cancelled successfully.")
        print("Redirecting to RydeEasy Customer main menu")
        time.sleep(3)
    customer_menu()


signin_customer()
