import sqlite3
import json
with open("records.txt", "r") as file:
    data = file.read()
try:
    with sqlite3.connect("my.db") as conn:
        createStatement = """CREATE TABLE IF NOT EXISTS records(
        station_id varchar, 
        last_reported int, 
        is_installed int,
        is_renting int, 
        is_returning int,
        num_bikes_available int,
        num_bikes_disabled int,
        num_ebikes_available int,
        num_docks_available int,
        num_docks_disabled int
        );"""
        insertStatement = """INSERT INTO records(station_id, last_reported, is_installed, is_renting, is_returning, num_bikes_available, num_bikes_disabled, num_ebikes_available, num_docks_available, num_docks_disabled)
        VALUES(?,?,?,?,?,?,?,?,?,?)"""
        cursor = conn.cursor()
        cursor.execute(createStatement)
        i=1
        N = len(data.split('\n'))
        for row in data.split('\n'):
            row = row.replace("'", '"')
            row = json.loads(row)
            record = (row['station_id'], row['last_reported'], row['is_installed'], row['is_renting'], row['is_returning'], row['num_bikes_available'], row['num_bikes_disabled'], row['num_ebikes_available'], row['num_docks_available'], row['num_docks_disabled'])
            cursor.execute(insertStatement, record)
            print(f"Inserted row {i} of {N}")
            i+=1
        conn.commit()


except sqlite3.OperationalError as e:
    print("Failed to open database:", e)