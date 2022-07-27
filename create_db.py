import sqlite3

connection = sqlite3.connect('houses.db')
cursor = connection.cursor()

create_table_users = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,3
        username TEXT,
        password TEXT
    )
 '''


cursor.execute(create_table_users)


create_table_houses = '''
    CREATE TABLE IF NOT EXISTS houses (
        name TEXT, 
        address TEXT,
        square_feet INT, 
        beds INT, 
        baths INT, 
        price REAL
    )
'''

cursor.execute(create_table_houses)
