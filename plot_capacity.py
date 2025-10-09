import json
import matplotlib.pyplot as plt

timestamps = []
maxCapacities = []
with open("records.txt", "r") as file:
    data = file.read()   
rows=data.split('\n')
for row in rows:
    row = row.replace("'", '"')
    row =json.loads(row)
    if row['station_id'] == '0f45bcf6-7028-4584-a51e-4129847dbebc':
        maxCapacity = row['num_docks_available']+row['num_bikes_available']+row['num_docks_disabled']+row['num_bikes_disabled']
        timestamps.append(row['last_reported'])
        maxCapacities.append(maxCapacity)
plt.scatter(timestamps,maxCapacities)
plt.plot(timestamps, maxCapacities, color='red', label='Connecting Line')
plt.show()