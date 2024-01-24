# Author: Oluwakemi Toluwalase Obadeyi
# Date: 03/10/2023

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_drivers(conn):
    sql = """ SELECT * FROM Drivers"""
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_bookings(conn):
    sql = """ SELECT * FROM Bookings"""
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def cancel_previous_booking(conn, id):
    sql = "DELETE FROM Bookings WHERE bookingid=?"
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()
