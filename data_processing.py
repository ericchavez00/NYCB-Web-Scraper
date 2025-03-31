import requests, time
currentTime = 0
while True:
    data = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json').json()
    records = open("records.txt","a")
    for station in data['data']['stations']:
        #Station id corresponding to 88th St and Park Ave
        if station['station_id']=="66dde103-0aca-11e7-82f6-3863bb44ef7c":
            if station['last_reported'] != currentTime:
                currentTime = station['last_reported']
                stationInformation = {}
                stationInformation['station_id'] = "66dde103-0aca-11e7-82f6-3863bb44ef7c"
                stationInformation['last_reported'] = currentTime 
                stationInformation['is_installed'] = station['is_installed']
                stationInformation['is_renting'] = station['is_renting']
                stationInformation['is_returning'] = station['is_returning']
                stationInformation['num_docks_available'] = station['num_docks_available']
                stationInformation['num_ebikes_available'] = station['num_ebikes_available']
                stationInformation['num_bikes_available'] = station['num_bikes_available']
                records.write(","+str(stationInformation))
    time.sleep(60)