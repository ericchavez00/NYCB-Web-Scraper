from time import localtime
import json
from scipy.stats import kstest
import sqlite3

def extractData(row):
    row =json.loads(row)
    timestamp = localtime(row['last_reported'])
    if timestamp.tm_hour == 17 and timestamp.tm_min <= 15:
        return [timestamp.tm_mday,timestamp.tm_hour,timestamp.tm_min,timestamp.tm_sec, row['num_docks_available'], row['num_bikes_available'], row['last_reported']]
with sqlite3.connect("records.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    stationId = 'ca5cc034-a95d-446e-8314-6691589886b1'
    selectStatement = '''SELECT * FROM records WHERE station_id=? AND strftime('%H:%M', datetime(last_reported, 'unixepoch'))
      BETWEEN '16:00' AND '16:15' '''
    cursor.execute(selectStatement, (stationId,))
    extractedData = cursor.fetchall()
    # for row in rows:
    #     print(row)
def calculateRentInterArrivals(extractedData):
    start = 0
    end = 1
    rentInterArrivals = [] 
    while start < len(extractedData)-1 and end < len(extractedData):
        #check if start and end rows are on the same date
        startTimestamp = localtime(extractedData[start]['last_reported'])
        endTimestamp = localtime(extractedData[end]['last_reported'])
        if startTimestamp.tm_mday != endTimestamp.tm_mday:
            start = end
            end +=1
        #check successive rows and see if the dock number went up and bike number went down, then compute interarrival time
        elif extractedData[start]['num_docks_available'] < extractedData[end]['num_docks_available'] and extractedData[start]['num_bikes_available'] > extractedData[end]['num_bikes_available']:
            diff = extractedData[end]['last_reported'] - extractedData[start]['last_reported']
            rentInterArrivals.append(diff)
            start = end
            end += 1
        #if not, keep current start row and check next row to see if changed
        else:
            end += 1
    return rentInterArrivals
def calculateReturnInterArrivals(extractedData):
    start = 0
    end = 1
    returnInterArrivals = []
    while start < len(extractedData)-1 and end < len(extractedData):
        startTimestamp = localtime(extractedData[start]['last_reported'])
        endTimestamp = localtime(extractedData[end]['last_reported'])
        #check if start and end rows are on the same date
        if startTimestamp.tm_mday != endTimestamp.tm_mday:
            start = end
            end +=1
        #check successive rows and see if the dock number went down and bike number went up, then compute interarrival time
        elif extractedData[start]['num_docks_available'] > extractedData[end]['num_docks_available'] and extractedData[start]['num_bikes_available'] < extractedData[end]['num_bikes_available']:
            diff = extractedData[end]['last_reported'] - extractedData[start]['last_reported']
            returnInterArrivals.append(diff)
            start = end
            end += 1
        #if not, keep current start row and check next row to see if changed
        else:
            end += 1
    return returnInterArrivals

#Calculate sample lambda values from interarrival times
rentInterArrivals = calculateRentInterArrivals(extractedData)
returnInterArrivals = calculateReturnInterArrivals(extractedData)
# print(rentInterArrivals)
# print(returnInterArrivals)
returnParam = len(returnInterArrivals)/sum(returnInterArrivals)
rentParam = len(rentInterArrivals)/sum(rentInterArrivals)
#Run K-S test for goodness of fit on return and rent interarrival times
returnKS, returnPValue = kstest(returnInterArrivals, 'expon', args=(0, 1/returnParam))
rentKS, rentPValue = kstest(rentInterArrivals, 'expon', args=(0,1/rentParam))
print(f"Return K-S statistic: {returnKS}")
print(f"Return p-value: {returnPValue}")
print(f"Rent K-S statistic: {rentKS}")
print(f"Rent p-value: {rentPValue}")