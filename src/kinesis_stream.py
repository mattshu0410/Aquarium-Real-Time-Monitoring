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




#print(str(timestamp))
#print(json.dumps(data))

# Create a kinesis client
client = boto3.client('kinesis')

# Send message to Kinesis DataStream
for i in range(1,100):
	time_stamp =  datetime.strftime((datetime.now(timezone.utc)), '%Y-%m-%dT%H:%M:%SZ')
	print(time_stamp)
	data = {
		'metric': random.choice(['no3', 'no2', 'ph', 'nh3']),
    	'time_stamp': str(time_stamp),
    	'metric_value': random.random()
	}
	response = client.put_record(
		StreamName = "water-metric-streaming",
		Data = json.dumps(data),
		PartitionKey = str(data['metric'])
	)
	# If the message was not successfully sent print an error message
	if response['ResponseMetadata']['HTTPStatusCode'] != 200:
		print('Error!')
	else:
		print('Message sent')
		print(data)
	time.sleep(0.5)


#data = {
#'timestamp': str(timestamp),
#'metric': 'no2',
#'value': str(random.random())
#}
#
#response = client.put_record(
#		StreamName = "water-metric-streaming",
#		Data = json.dumps(data),
#		PartitionKey = str(data['timestamp'])
#)
#print(response)



