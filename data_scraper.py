import requests, time
lastReportedTime = {}
while True:
    response = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json')
    if response.ok:
        data=response.json()
        records = open("records.txt","a")
        for station in data['data']['stations']:
            stationID = station['station_id']
            if stationID not in lastReportedTime:
                lastReportedTime[stationID] = station['last_reported']
            if station['last_reported'] != lastReportedTime[stationID]:
                lastReportedTime[stationID] = station['last_reported']
                records.write("\n"+str(station))
    time.sleep(60)