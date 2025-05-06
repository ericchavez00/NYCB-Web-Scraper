from time import localtime
import json
from scipy.stats import kstest
def helper(row):
    row =json.loads(row)
    timestamp = localtime(row['last_reported'])
    if timestamp.tm_hour == 17 and timestamp.tm_min <= 15:
        return [timestamp.tm_hour,timestamp.tm_min,timestamp.tm_sec, row['num_docks_available'], row['num_bikes_available'], row['last_reported']]
with open("records.txt", "r") as file:
    data = file.read()   
rows = data.split('#')
extractedData = [x for x in map(helper, rows) if x is not None]
start = 0
end = 1
rentInterArrivals = []
returnInterArrivals = []
while start < len(extractedData)-1 and end < len(extractedData):
    #check if start and end rows are on the same date
    if extractedData[start][1] > extractedData[end][1]:
        start = end
        end +=1
    #check successive rows and see if both docks available and bikes available changed, compute interarrival time and add to appropriate list
    elif extractedData[start][3] > extractedData[end][3] and extractedData[start][4] < extractedData[end][4]:
        diff = extractedData[end][5] - extractedData[start][5]
        returnInterArrivals.append(diff)
        start = end
        end += 1
    elif extractedData[start][3] < extractedData[end][3] and extractedData[start][4] > extractedData[end][4]:
        diff = extractedData[end][5] - extractedData[start][5]
        rentInterArrivals.append(diff)
        start = end
        end += 1 
    #if not, keep current start row and check next row to see if changed
    else:
        end += 1
#Calculate sample lambda from interarrival times
returnParam = len(returnInterArrivals)/sum(returnInterArrivals)
rentParam = len(rentInterArrivals)/sum(rentInterArrivals)
#Run K-S test for goodness of fit
D, p_value = kstest(returnInterArrivals, 'expon', args=(0, 1/returnParam))
print(returnInterArrivals)
print(f"K-S statistic: {D}")
print(f"p-value: {p_value}")