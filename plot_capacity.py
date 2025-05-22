import json
import matplotlib.pyplot as plt

timestamps = []
maxCapacities = []
with open("records.txt", "r") as file:
    data = file.read()   
rows=data.split('\n')
for row in rows:
    row =json.loads(row)
    maxCapacity = row['num_docks_available']+row['num_bikes_available']
    timestamps.append(row['last_reported'])
    maxCapacities.append(maxCapacity)
plt.scatter(timestamps,maxCapacities)
plt.plot(timestamps, maxCapacities, color='red', label='Connecting Line')
plt.show()