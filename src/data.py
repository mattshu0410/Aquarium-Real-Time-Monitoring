from os import getpgid
import numpy as np
import datetime
import csv 
import random

metric = ["nh3", "no3", "no2", "ph"]

def get_ammonia():
    return round(random.uniform(0, 1), 1)

    # return round(random.random())

def get_nitrate():
    return round(random.uniform(0, 1), 1)

    # return round(random.random())

def get_nitrite():
    if round(random.random()) == 1:
        return random.randrange(40, 100)
    else: 
        return random.randrange(1, 40)

def get_ph():
    if round(random.random()) == 1: 
        if round(random.random()) == 1:
            return round(random.uniform(1, 6.5), 1)
        elif round(random.random()) == 0:
            return round(random.uniform(7.5, 14), 1)
    else: 
        return round(random.uniform(6.5, 7.5), 1)

def get_time():
    start_time = datetime.datetime.now()
    x = 0
    while True:
        y = np.sin(x)

        if (datetime.datetime.now() - start_time).seconds == 1:
            start_time = datetime.datetime.now()
            # choice = random.choice(metric)

            random.shuffle(metric)
            for choice in metric:

                if choice is "nh3":
                    y = get_ammonia()
                elif choice is "no3":
                    y = get_nitrate()
                elif choice is "no2":
                    y = get_nitrite()
                elif choice is "ph":
                    y = get_ph()
                print(start_time, choice, y)
        x += 0.1

# writing into a csv file
def write_to_file(data):

    file = open('./data.csv', 'w')

    # create the csv writer
    writer = csv.writer(file)

    # write a row to the csv file
    writer.writerow(data)

    # close the file
    file.close()

def build_row(timestamp, metric, value):
    return 

if __name__ == "__main__":
    file = open('./data.csv', 'w')
    writer = csv.writer(file)
    
    header = ['Timestamp', 'Metric', 'Value']

    # write the header
    writer.writerow(header)

    file.close()

    print(get_time())
    # print(get_ammonia())
    # print(get_nitrate())
    # print(get_nitrite())
    # print(get_ph())
