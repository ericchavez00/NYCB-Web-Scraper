from time import localtime
import json
from scipy.stats import kstest

def extractData(row):
    row =json.loads(row)
    timestamp = localtime(row['last_reported'])
    if timestamp.tm_hour == 17 and timestamp.tm_min <= 15:
        return [timestamp.tm_mday,timestamp.tm_hour,timestamp.tm_min,timestamp.tm_sec, row['num_docks_available'], row['num_bikes_available'], row['last_reported']]
with open("records_23.txt", "r") as file:
    data = file.read()   
rows = data.split('\n')
extractedData = [x for x in map(extractData, rows) if x is not None]
def calculateRentInterArrivals(extractedData):
    start = 0
    end = 1
    rentInterArrivals = [] 
    currentDocks = extractedData[start][4]
    currentBikes = extractedData[start][5]
    while start < len(extractedData)-1 and end < len(extractedData):
        #check if start and end rows are on the same date
        if extractedData[start][0] != extractedData[end][0]:
            start = end
            end +=1
            currentDocks = extractedData[start][4]
            currentBikes = extractedData[start][5]
        #check successive rows and see if the dock number went up and bike number went down, then compute interarrival time
        elif extractedData[start][4] < extractedData[end][4] and extractedData[start][5] > extractedData[end][5]:
            diff = extractedData[end][6] - extractedData[start][6]
            rentInterArrivals.append(diff)
            start = end
            end += 1
            currentDocks = extractedData[start][4]
            currentBikes = extractedData[start][5]
        #if not, keep current start row and check next row to see if changed
        else:
            currentDocks = extractedData[end][4]
            currentBikes = extractedData[end][5]
            end += 1
    return rentInterArrivals
def calculateReturnInterArrivals(extractedData):
    start = 0
    end = 1
    returnInterArrivals = []
    currentDocks = extractedData[start][4]
    currentBikes = extractedData[start][5]
    while start < len(extractedData)-1 and end < len(extractedData):
        #check if start and end rows are on the same date
        if extractedData[start][0] != extractedData[end][0]:
            start = end
            end +=1
            currentDocks = extractedData[start][4]
            currentBikes = extractedData[start][5]
        #check successive rows and see if the dock number went down and bike number went up, then compute interarrival time
        elif currentDocks > extractedData[end][4] and currentBikes < extractedData[end][5]:
            diff = extractedData[end][6] - extractedData[start][6]
            returnInterArrivals.append(diff)
            start = end
            end += 1
            currentDocks = extractedData[start][4]
            currentBikes = extractedData[start][5]
        #if not, keep current start row and check next row to see if changed
        else:
            currentDocks = extractedData[end][4]
            currentBikes = extractedData[end][5]
            end += 1
    return returnInterArrivals

#Calculate sample lambda values from interarrival times
rentInterArrivals = calculateRentInterArrivals(extractedData)
returnInterArrivals = calculateReturnInterArrivals(extractedData)
returnParam = len(returnInterArrivals)/sum(returnInterArrivals)
rentParam = len(rentInterArrivals)/sum(rentInterArrivals)
#Run K-S test for goodness of fit on return and rent interarrival times
returnKS, returnPValue = kstest(returnInterArrivals, 'expon', args=(0, 1/returnParam))
rentKS, rentPValue = kstest(rentInterArrivals, 'expon', args=(0,1/rentParam))
print(f"Return K-S statistic: {returnKS}")
print(f"Return p-value: {returnPValue}")
print(f"Rent K-S statistic: {rentKS}")
print(f"Rent p-value: {rentPValue}")