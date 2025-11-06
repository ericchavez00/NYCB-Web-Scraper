import sqlite3
import json
def batch_reader(file_obj, batch_size):
    batch = []
    for line in file_obj:
        batch.append(line)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

with open("records.txt", "r") as file:
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
            #N = sum(1 for _ in file)
            for batch in batch_reader(file, batch_size=10000):
                for row in batch:     
                    row = row.replace("'", '"')
                    row = json.loads(row)
                    record = (row['station_id'], row['last_reported'], row['is_installed'], row['is_renting'], row['is_returning'], row['num_bikes_available'], row['num_bikes_disabled'], row['num_ebikes_available'], row['num_docks_available'], row['num_docks_disabled'])
                    cursor.execute(insertStatement, record)
                    print(f"Inserted row {i} of total")
                    i+=1
            conn.commit()


    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)