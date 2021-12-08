import json
import uuid
import boto3
import time
import datetime

# How to Use this minimally reproducible example
	#1. CD into the directory containing your python script
	#2. Run 'pip install boto3' if you have not already
	#3. Install aws CLI - https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
	#4. Run 'aws configure' and use details from the "Amazon AWS Account Details" page from OneNote
    #5. python kinesis_stream.py to run python script

timestamp =  datetime.datetime.fromtimestamp(time.time())
data = {
    'timestamp': str(timestamp),
    'metric': 'no2',
    'value': '0.4'
}

#print(str(timestamp))
#print(json.dumps(data))

# Create a kinesis client
client = boto3.client('kinesis')

# Send message to Kinesis DataStream
response = client.put_record(
	StreamName = "water-metric-streaming",
	Data = json.dumps(data),
	PartitionKey = str(hash(data['timestamp']))
)

print('Message sent')
#print(response)

# If the message was not successfully sent print an error message
if response['ResponseMetadata']['HTTPStatusCode'] != 200:
	print('Error!')
	print(response)


