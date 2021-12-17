import json
import csv
import boto3

#This activates on csv upload to water-metrics-data S3 bucket and update water-metrics DynamoDB table
def lambda_handler(event, context):
    region = 'ap-southeast-2'
    record_list = []
    try:
        s3 = boto3.client('s3') #s3 client
        dynamodb = boto3.client('dynamodb', region_name = region) #dynamodb client
        bucket = event['Records'][0]['s3']['bucket']['name'] #grabs bucket name from event object
        key = event['Records'][0]['s3']['object']['key'] #grabs key name from event object
        #print('Bucket: ', bucket, ' Key: ', key)

        csv_file = s3.get_object(Bucket = bucket, Key = key) #get s3 object
        record_list = csv_file['Body'].read().decode('utf-8').split('\n') #process csv
        csv_reader = csv.reader(record_list, delimiter=',', quotechar='"') #csv reader

        for row in csv_reader:
            timestamp = row[0]
            metric = row[1]
            value = row[2]
            #print("Timestamp: ", timestamp, "Metric: ", metric, "Value: ", value)

            #Add record to table
            add_to_db = dynamodb.put_item(
                TableName = 'water-metrics',
                Item = {
                    'timestamp': {'S': timestamp},
                    'metric': {'S': metric},
                    'value': {'N': value},
                },
                )
            print('Successfully added the records to the table.')
    except Exception as e:
        print(str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('CSV to DynamoDB Success')
    }
