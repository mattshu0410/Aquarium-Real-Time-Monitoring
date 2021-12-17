# NOTE: change the cloudwatch interval from 1 min to 1 hour 
import json
import boto3
from boto3.dynamodb.conditions import Key 
import datetime as dt
from statistics import mean

# Constants for thresholds 
ACCEPTABLE_NH3 = 0.0
ACCEPTABLE_NO3 = 0.0
ACCEPTABLE_NO2 = 40.0
ACCEPTABLE_PH_LOWER = 6.5
ACCEPTABLE_PH_UPPER = 7.5

def lambda_handler(event, context):
    """ 
        Function connects to database, for-loops the columns and tests 
        whether these values are acceptable.
        
        Note: can possibly split this into multiple functions later
        
    """
    # connect to the database 
    client = boto3.resource("dynamodb")
    table = client.Table("water-metric-data")
    
    # section off the last hour of values 
    time_to = dt.datetime.now()
    # hours = dt.timedelta(hours=1)
    mins = dt.timedelta(seconds= 60)
    # time_from = time_to - hours
    time_from = time_to - mins

    str_time_from = str(dt.datetime.strftime(time_from, '%Y-%m-%dT%H:%M:%SZ'))
    str_time_to = str(dt.datetime.strftime(time_to, '%Y-%m-%dT%H:%M:%SZ'))
    
    # use query (instead of scan) to "slice" the table 
    #response = table.query(
    #    KeyConditionExpression=Key('metric').eq('nh3') & Key('time_stamp').between(str_time_from, str_time_to)
    #    )['Items']
    
    
    def query_data(metric, str_time_from, str_time_to):
        response = table.query(
            KeyConditionExpression=Key('metric').eq(metric) & Key('time_stamp').between(str_time_from, str_time_to)
            )['Items']
        return(response)
    
    def calculate_mean(response):
        metric_values = []
        for item in response:
            metric_values.append(item['metric_value'])
        return(mean(metric_values))
    
    
    # metric lists to calculate averages 
    nh3_list = query_data('nh3', str_time_from, str_time_to)
    print(nh3_list)
    no3_list = query_data('no3', str_time_from, str_time_to)
    print(no3_list)
    no2_list = query_data('no2', str_time_from, str_time_to)
    print(no2_list)
    ph_list = query_data('ph', str_time_from, str_time_to)
    print(ph_list)

    # get the averages of each list 
    # TODO: format to 5 decimal places
    no3_avg = calculate_mean(no3_list)
    print(no3_avg)
    no2_avg = calculate_mean(no2_list)
    print(no2_avg)
    nh3_avg = calculate_mean(nh3_list)
    print(nh3_avg)
    ph_avg = calculate_mean(ph_list)
    print(ph_avg)
    
    # formatting means
    no3_avg_form = round(no3_avg,5)
    # print(f" formatted! : {no3_avg_form} ")
    no2_avg_form = round(no2_avg,5)
    # print(f" formatted! : {no2_avg_form} ")
    nh3_avg_form = round(nh3_avg,5)
    # print(f" formatted! : {nh3_avg_form} ")
    ph_avg_form = round(ph_avg,5)
    # print(f" formatted! : {ph_avg_form} ")
    
    # default values
    nh3_acceptable = True
    no3_acceptable = True
    no2_acceptable = True
    ph_acceptable = True
    
    # compare averages vs conditions 
    if nh3_avg_form > ACCEPTABLE_NH3:
        nh3_acceptable = False
    if no3_avg_form > ACCEPTABLE_NO3:
        no3_acceptable = False
    if no2_avg_form != ACCEPTABLE_NO2:
        no2_acceptable = False
    if ph_avg_form < ACCEPTABLE_PH_LOWER or ph_avg_form > ACCEPTABLE_PH_UPPER:
        ph_acceptable = False

    # put into a list
    thresholdsMet = [nh3_acceptable, no3_acceptable, no2_acceptable, ph_acceptable]
    chemicals = ["Ammonia (nh3)", "Nitrate (no3)", "Nitrite (no2)" , "pH" ]
    averages = [nh3_avg_form, no3_avg_form, no2_avg_form, ph_avg_form]

    # check whether to return an email
    if all(thresholdsMet): # if all are true
        print("fine")
        return "Your aquarium water quality is fine!"
        
    else:
        print("notfine")
        false_dict = {}
        i = 0
        for chem in thresholdsMet:
            if chem is False:
                false_dict[chemicals[i]] = averages[i]
            i += 1

        false_str = ""
        for key in false_dict:
            false_str += " " + key + ","
        adjusted_str =  false_str[:-1]
        
        subject = f"Abnormal {adjusted_str} levels detected!"
        main_message = "Please adjust your aquarium's water quality!\n"
        for chemical, average in false_dict.items():
            if chemical == "pH":
                message = f"The {chemical} is at an unacceptable level measured at {average} pH. Add 1 teaspoon of baking soda per 20 litres of water into your tank incrementally and closely monitor your dashboard. "
            else:
                message = f"The {chemical} is at an unacceptable level measured at {average} ppm. "
                
            if chemical == "Ammonia (nh3)" or chemical == "Nitrate (no3)":
                expected_msg = f"The expected level of {chemical} should be 0.0 ppm. \n"
            elif chemical == "Nitrite (no2)":
                expected_msg = f"The expected level of {chemical} should be 40 ppm. \n"
            elif chemical == "pH":
                expected_msg = f"The expected pH is between 6.5 and 7.5 \n "
                
            main_message += message + expected_msg

        # insert the subject line and main message into the database
        email_table = client.Table("ses_message")
        email_response = email_table.put_item(
            Item={
                'time_stamp':str_time_to,
                'subject':subject , 
                'message':main_message
            }
        )

        return "Email has been sent!"

# To Do:
# acceptable anomalies? 
