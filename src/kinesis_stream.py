import simplejson as json # instead of import json
import uuid
import boto3
import time
from datetime import datetime
from datetime import timezone
import random
from decimal import Decimal

# How to Use this minimally reproducible example
	#1. CD into the directory containing your python script
	#2. Run 'pip install boto3' if you have not already
	#3. Install aws CLI - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
	#4. Run 'aws configure' and use details from the "Amazon AWS Account Details" page from OneNote
    #5. python kinesis_stream.py to run python script


def get_nh3():
    return round(random.uniform(0, 1), 1)

    # return round(random.random())

def get_no3():
    return round(random.uniform(0, 1), 1)

    # return round(random.random())

def get_no2():
    if round(random.random()) == 1:
        return random.randrange(40, 100)
    else:
        return random.randrange(1, 40)

def get_ph():
	n = random.choice([1]*10 + [2]*80 + [3]*10)
	#if n == 1:
	#	return round(random.uniform(1, 6.5), 1)
	#elif n==2:
	#	return round(random.uniform(7.5, 14), 1)
	#else:
	#	return round(random.uniform(6.5, 7.5), 1)
	return round(random.uniform(1, 6.5), 1)

client = boto3.client('kinesis')
while True:
	for metric in ['no3', 'no2', 'ph', 'nh3']:
		time_stamp =  datetime.strftime((datetime.now(timezone.utc)), '%Y-%m-%dT%H:%M:%SZ')
		record = {
			'metric': metric,
			'time_stamp': str(time_stamp),
			'metric_value': eval("get_"+metric+"()")
			}
		response = client.put_record(
			StreamName = "water-metric-streaming",
			Data = json.dumps(record),
			PartitionKey = str(record['metric'])
		)	
		print(f'Record added for {record["metric"]}')
		time.sleep(1)

# Create a kinesis client
#client = boto3.client('kinesis')
#def create_data():
#	Records = []
#	time_stamp =  datetime.strftime((datetime.now(timezone.utc)), '%Y-%m-%dT%H:%M:%SZ')
#	print(time_stamp)
#	for metric in ['no3', 'no2', 'ph', 'nh3']:
#		record = {
#			'metric': metric,
#    		'time_stamp': str(time_stamp),
#    		'metric_value': eval("get_"+metric+"()")
#		}
#		Records.append(record)
#	return Records
#
## Send message to Kinesis DataStream
#while True:
#	Records = create_data()
#	for record in Records:
#		response = client.put_record(
#			StreamName = "water-metric-streaming",
#			Data = json.dumps(record),
#			PartitionKey = str(record['metric'])
#		)
#		print(f'Record added for {record["metric"]}')
#		time.sleep(1)
#	# If the message was not successfully sent print an error message
#	if response['ResponseMetadata']['HTTPStatusCode'] != 200:
#		print('Error!')
#	else:
#		print('Message sent')
#		print(Records)
#	time.sleep(2)


