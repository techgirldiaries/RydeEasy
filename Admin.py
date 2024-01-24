# Author: Oluwakemi Toluwalase Obadeyi
# Date: 03/10/2023

from Data import *
import sqlite3
import time

# pointing to database file
database = "tbs.db3"

# creating database connection
conn = create_connection(database)

if not conn:
    print("Error! cannot create the database connection.")
    exit()

# Admin Sign In function
print("RydeEasy Admin Sign In")
print(
    "For testing purposes: the customer name is John Doe, the email is johndoe@rydeeasy.com "
    "and the password is admin, this line is to be removed in a final version"
)

while True:

    def admin_signin():
        print("Please Sign In")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        with sqlite3.connect("tbs.db3") as db:
            cursor = db.cursor()
        find_email = "SELECT * FROM Admins WHERE email = ? AND password = ?"
        cursor.execute(find_email, [email, password])
        results = cursor.fetchall()

        if results:
            print("Successfully signed in!")
            admin_menu()

        else:
            print("Invalid email or password!")
            retry = input("Would you like to try again? y/n: ")
            if retry in ("y", "Y", "yes", "Yes"):
                admin_signin()
            elif retry in ("n", "N", "no", "No"):
                print("Goodbye.")

    break


# Admin menu function
def admin_menu():
    print("Admin Menu")
    print("1. View all bookings")
    print("2. Create a new driver")
    print("3. Cancel a booking")
    print("4. View available drivers")
    print("5. Logout")

    menu_input = input("How can I assist you?: ")
    if menu_input == "1":
        view_bookings()
    if menu_input == "2":
        create_new_driver()
    if menu_input == "3":
        cancel_booking()
    if menu_input == "4":
        available_drivers()
    if menu_input == "5":
        exit()
    else:
        print("Invalid Details.")
        admin_menu()


# Create new driver function
def create_new_driver():
    print("Create new driver")
    found = 0
    while found == 0:
        firstname = input("Please enter the Driver's first name: ")
        with sqlite3.connect("tbs.db3") as db:
            cursor = db.cursor()
            find_customer = "SELECT * FROM Drivers WHERE firstname = ?"
            cursor.execute(find_customer, [firstname])

            if cursor.fetchall():
                try_again_or_signin = input(
                    "a driver with the name "
                    + firstname
                    + " already exists, please add a "
                    "number at the end of his/her name "
                    "to continue, enter r to retry, "
                    "enter n if you "
                    "no longer wish to add a driver: "
                )
                if try_again_or_signin in ("r", "R"):
                    create_new_driver()
                elif try_again_or_signin in ("n", "N"):
                    print()
                    admin_menu()
                else:
                    print("Invalid Entry, Redirecting...")
                    create_new_driver()

            else:
                found = 1

    lastname = input("Please enter the Driver's last name: ")
    title = input("Please enter the Driver's title: ")
    phone_number = input("Please enter the Driver's phone number: ")
    car_colour = input("Please enter the Driver's car colour: ")
    car_brand = input("Please enter the Driver's car brand : ")
    reg_number = input("Please enter the Driver's car registration number: ")
    email = input("Please enter email: ")
    password = input("Create password (Case Sensitive): ")
    cpassword = input("Please confirm password: ")

    while password != cpassword:
        print("Passwords does not match!")
        password = input("Create password (Case Sensitive): ")
        cpassword = input("Confirm your password: ")

    input_data = """INSERT INTO Drivers(title, firstname, lastname, phone_number, 
    car_colour, car_brand, reg_number, email, password) VALUES(?,?,?,?,?,?,?,?,?) """

    cursor.execute(
        input_data,
        [
            title,
            firstname,
            lastname,
            phone_number,
            email,
            car_colour,
            car_brand,
            reg_number,
            password,
        ],
    )
    db.commit()


# View bookings from customers
def view_bookings():
    print("View Bookings")
    with sqlite3.connect("tbs.db3") as db:
        cursor = db.cursor()

    # Bookings which belong to the current customer
    sql = """ SELECT * FROM Bookings """
    cursor.execute(sql)
    booking = cursor.fetchall()
    if not booking:
        print("No bookings, redirecting to admin Menu...")
        time.sleep(2)
        admin_menu()
    else:
        # Showing all the available bookings
        for i, b in enumerate(booking, 1):
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

    # Function to return to previous menu
    print("\n")
    return_to_menu = input(
        "Select R To return to the main menu or select C to cancel booking(s): "
    )
    if return_to_menu in ("r", "R", "return", "Return"):
        print("\n")
        admin_menu()
    elif return_to_menu in ("c", "C", "cancel", "Cancel"):
        print("\n")
        cancel_booking()
    else:
        print("Invalid input, redirecting to main menu...")
    admin_menu()


# Cancel Booking Function
def cancel_booking():
    print("Cancel a booking")
    booking = get_bookings(conn)  # connection to database

    if not booking:
        print("There is no booking yet, redirecting to Admin Menu...")
        time.sleep(2)
        admin_menu()
    else:
        # Showing all the available bookings
        for i, b in enumerate(booking, 0):
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
        b = booking[index]
        bookingid = b[0]

        cancel_previous_booking(conn, bookingid)
        print("Booking cancelled.")
        print("Redirecting to Main Menu...")
        time.sleep(3)
        admin_menu()


# View available drivers function
def available_drivers():
    print("\n")

    drivers = get_drivers(conn)
    print("Available drivers:")
    for i, driver in enumerate(drivers, 0):
        print(
            str(i) + "." + str(driver[1]) + " " + str(driver[2]) + " " + str(driver[3])
        )

    # Return to previous menu function
    print("\n")
    input("Press 'Enter' to return to the Admin Menu...")
    print("\n")
    admin_menu()


admin_signin()
