import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np


def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}
    time = []
    with open(file, "r") as f:
        for line in f:

            r = json.loads(line)
            room = list(r.keys())[0]
            currtime = datetime.fromisoformat(r[room]["time"])

            temperature[currtime] = {room: r[room]["temperature"][0]}
            occupancy[currtime] = {room: r[room]["occupancy"][0]}
            co2[currtime] = {room: r[room]["co2"][0]}
            time += [currtime]
    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }


    return data, time




file = '/Users/ybaker661/2020-sensor-miniproject/data.txt'

data, time = load_data(file)

#Class1 chosen for task 2.1-2.3
temp = data['temperature'].class1
temp = temp.dropna()
temp_med = temp.median()
temp_var = temp.var()
print('The temperature variance is: ' + str(temp_var) +'\n')
print('The temperature median is: ' + str(temp_med) +'\n')

occ = data['occupancy'].class1
occ = occ.dropna()
occ_med = occ.median()
occ_var = occ.var()
print('The occupancy variance is: ' + str(occ_var) +'\n')
print('The occupancy median is: ' + str(occ_med) +'\n')

co2 = data['co2'].class1
co2 = co2.dropna()
#histogram for each sensor type

names = ['Temperature', 'Occupancy', 'Carbon Dioxide']
dats = [temp, occ, co2]
units = ['$^\circ$C', 'No. People', '?']

for n,i in enumerate(names):

    ax = plt.figure().gca()
    dats[n].hist()
    ax.set_ylabel("# of occurences")
    ax.set_xlabel(i +  units[n])
    ax.set_title("Class1 " + i)

# plt.show()

deltime = []
for i in range(len(time)-1):

    currdel = time[i+1] - time[i]
    currdel = currdel.total_seconds()
    deltime += [currdel]

#to be able to use built in pandas functions
deltime = pandas.DataFrame(deltime, columns=['Del_Time'])

deltime_mean = deltime.mean()
deltime_var = deltime.var()

print('The Delta_T variance is: ' + str(deltime_var) +'\n')
print('The Delta_T mean is: ' + str(deltime_mean) +'\n')


ax = plt.figure().gca()
deltime.hist()
ax.set_ylabel("# of occurences")
ax.set_xlabel("Delta T [s]")

plt.show()
