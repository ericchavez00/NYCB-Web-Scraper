import requests, time
while True:
    data = requests.get('https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json').json()
    #write = open("test.txt","a")
    for station in data['data']['stations']:
        if station['station_id']=="66dde103-0aca-11e7-82f6-3863bb44ef7c":
            print(station)
            #write.write(","+str(station))
    time.sleep(60)