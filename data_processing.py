from time import localtime
import json
from scipy.stats import kstest

def extractData(row):
    row =json.loads(row)
    timestamp = localtime(row['last_reported'])
    if timestamp.tm_hour == 17 and timestamp.tm_min <= 15:
        return [timestamp.tm_mday,timestamp.tm_hour,timestamp.tm_min,timestamp.tm_sec, row['num_docks_available'], row['num_bikes_available'], row['last_reported']]
with open("records.txt", "r") as file:
    data = file.read()   
rows = data.split('\n')
extractedData = [x for x in map(extractData, rows) if x is not None]
start = 0
end = 1
rentInterArrivals = []
returnInterArrivals = []
while start < len(extractedData)-1 and end < len(extractedData):
    #check if start and end rows are on the same date
    if extractedData[start][0] != extractedData[end][0]:
        start = end
        end +=1
    #check successive rows and see if both docks available and bikes available changed, compute interarrival time and add to appropriate list
    elif extractedData[start][4] > extractedData[end][4] and extractedData[start][5] < extractedData[end][5]:
        #Check if bike count was not updated at the same time as dock count and correct interarrival time
        if extractedData[end][5] - extractedData[end-1][5] == 1 and extractedData[end][4] == extractedData[end-1][4]:
            diff = extractedData[end-1][6] - extractedData[start][6]
            returnInterArrivals.append(diff)
            start = end - 1
            end += 1
        else: 
            diff = extractedData[end][6] - extractedData[start][6]
            returnInterArrivals.append(diff)
            start = end
            end += 1
    elif extractedData[start][4] < extractedData[end][4] and extractedData[start][5] > extractedData[end][5]:
        #Check if bike count was not updated at the same time as dock count and correct interarrival time
        if extractedData[end-1][5] - extractedData[end][5] == 1 and extractedData[end][4] == extractedData[end-1][4]:
            diff = extractedData[end-1][6] - extractedData[start][6]
            rentInterArrivals.append(diff)
            start = end - 1
            end += 1
        else:
            diff = extractedData[end][6] - extractedData[start][6]
            rentInterArrivals.append(diff)
            start = end
            end += 1
    #if not, keep current start row and check next row to see if changed
    else:
        end += 1
#Calculate sample lambda values from interarrival times
returnParam = len(returnInterArrivals)/sum(returnInterArrivals)
rentParam = len(rentInterArrivals)/sum(rentInterArrivals)
#Run K-S test for goodness of fit on return and rent interarrival times
returnKS, returnPValue = kstest(returnInterArrivals, 'expon', args=(0, 1/returnParam))
rentKS, rentPValue = kstest(rentInterArrivals, 'expon', args=(0,1/rentParam))
print(f"Return K-S statistic: {returnKS}")
print(f"Return p-value: {returnPValue}")
print(f"Rent K-S statistic: {rentKS}")
print(f"Rent p-value: {rentPValue}")