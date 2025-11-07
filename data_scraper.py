import requests, time
import sqlite3
lastReportedTime = {}
while True:
    with sqlite3.connect("records.db") as conn:
        cursor = conn.cursor()
        insertStatement = """INSERT INTO records(station_id, last_reported, is_installed, is_renting, is_returning, num_bikes_available, num_bikes_disabled, num_ebikes_available, num_docks_available, num_docks_disabled)
        VALUES(?,?,?,?,?,?,?,?,?,?)"""
        response = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json')
        if response.ok:
            data=response.json()
            for station in data['data']['stations']:
                stationID = station['station_id']
                if stationID not in lastReportedTime:
                    lastReportedTime[stationID] = station['last_reported']
                if station['last_reported'] != lastReportedTime[stationID]:
                    lastReportedTime[stationID] = station['last_reported']
                    record = (station['station_id'], station['last_reported'], station['is_installed'], station['is_renting'], station['is_returning'], station['num_bikes_available'], station['num_bikes_disabled'], station['num_ebikes_available'], station['num_docks_available'], station['num_docks_disabled'])
                    cursor.execute(insertStatement, record)
        conn.commit() 
    time.sleep(60)