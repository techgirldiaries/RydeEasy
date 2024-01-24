# Author: Oluwakemi Toluwalase Obadeyi
# Date: 03/10/2023

import sqlite3
import time
from Data import *

current_user = None

# Creating the driver's signin form function
print("RydeEasy Driver")

while True:

    def signin_driver():
        global current_user
        print("Sign In")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        with sqlite3.connect("tbs.db3") as db:
            cursor = db.cursor()
        find_email = "SELECT * FROM Drivers WHERE email = ? AND password = ?"
        cursor.execute(find_email, [email, password])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Successfully signed in! Welcome.")
                current_user = i[0]
                driver_menu()

        else:
            print("Invalid email or password!")
            retry = input("Would you like to try again? yes/no: ")
            if retry in ("y", "Y", "yes", "Yes"):
                signin_driver()
            elif retry in ("n", "N", "no", "No"):
                print("Goodbye")

    break


# Creating the Driver's menu function
def driver_menu():
    print("Driver Menu")
    print("1. View Bookings")
    print("2. Sign Out")

    menu_input = input("Please Indicate: ")
    if menu_input == "1":
        bookings_menu(current_user)
    elif menu_input == "2":
        exit()
    else:
        print("Invalid details.")
        driver_menu()


# Creating the Booking menu function
def bookings_menu(customerid):
    global current_user
    print("\n")
    print("Booking Menu")

    with sqlite3.connect("tbs.db3") as db:
        cursor = db.cursor()

        # Current user bookings
        sql = """ SELECT * FROM Bookings WHERE driverid=?"""
        cursor.execute(sql, (customerid,))
        bookings = cursor.fetchall()
        if not bookings:
            print("No Available Bookings, Redirecting to Driver Menu...")
            time.sleep(2)
            driver_menu()
        else:
            # Available Bookings
            for i, b in enumerate(bookings, 1):
                print(
                    str(i) + ") "
                    "Pick-up Address: "
                    "" + str(b[4]) + " Postcode: "
                    "" + str(b[5]) + " Pick-up Time: "
                    "" + str(b[9]),
                    """ -> Destination Address: """ + str(b[6]) + " Postcode: "
                    "" + str(b[7]),
                )
                input("Press any key to redirect to the Driver Menu")
                driver_menu()


signin_driver()
