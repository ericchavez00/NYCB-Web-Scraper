from time import localtime
import json
from scipy.stats import kstest
import numpy as np
import sqlite3

with sqlite3.connect("records.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    stationId = 'ca5cc034-a95d-446e-8314-6691589886b1'
    selectStatement = '''SELECT * FROM records WHERE station_id=? AND strftime('%H:%M', datetime(last_reported, 'unixepoch'))
      BETWEEN '16:00' AND '16:15' '''
    cursor.execute(selectStatement, (stationId,))
    extractedData = cursor.fetchall()

def calculateSkellamParams(extractedData):
    start = 0
    end = 1
    skellamSamples = []
    while start < len(extractedData)-1 and end < len(extractedData):
        startTimestamp = localtime(extractedData[start]['last_reported'])
        endTimestamp = localtime(extractedData[end]['last_reported'])
        #check if start and end rows are on the same date
        if startTimestamp.tm_mday != endTimestamp.tm_mday:
            bikeDiff = extractedData[end-1]['num_bikes_available'] - extractedData[start]['num_bikes_available']
            timeDiff = extractedData[end-1]['last_reported'] - extractedData[start]['last_reported']
            skellamSamples.append(bikeDiff/timeDiff)
            start = end 
            end += 1
        #Check if number of available docks close to zero for end row
        elif extractedData[start]['num_docks_available'] <= 1 and extractedData[end]['num_docks_available'] <=1:
            start += 1
            end += 1
        elif extractedData[start]['num_docks_available'] > 1 and extractedData[end]['num_docks_available'] <=1:
            bikeDiff = extractedData[end-1]['num_bikes_available'] - extractedData[start]['num_bikes_available']
            timeDiff = extractedData[end-1]['last_reported'] - extractedData[start]['last_reported']
            start = end
            end += 1
        #Check if number of available bikes close to zero for end row
        elif extractedData[start]['num_bikes_available'] <= 1 and extractedData[end]['num_bikes_available'] <=1:
            start += 1
            end += 1
        elif extractedData[start]['num_bikes_available'] > 1 and extractedData[end]['num_bikes_available'] <=1:
            bikeDiff = extractedData[end-1]['num_bikes_available'] - extractedData[start]['num_bikes_available']
            timeDiff = extractedData[end-1]['last_reported'] - extractedData[start]['last_reported']
            start = end
            end += 1
        else:
            end +=1
    mean = np.mean(skellamSamples)
    var = np.var(skellamSamples)
    lambda1 = (var+mean)/2 
    lambda2 = (var-mean)/2
    return lambda1, lambda2 

print(calculateSkellamParams(extractedData))