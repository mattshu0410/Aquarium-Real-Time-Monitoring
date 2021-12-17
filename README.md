# Aquarium Real Time Monitoring

## STEM Leaders Program

Our task was to take the guesswork out of aquarium maintenance and make it simple again. We had 1.5 weeks to build a MVP solution for aquarium maintenance. 

## Solution

1.    Water sensor for NH3, pH, NO2, NO3 measures water quality and sends data to AWS cloud
2.    Data is ingested in real-time by AWS Kinesis Data Streams
3.    Data is stored in a DynamoDB NOSQL database for historical access
4.    A CRON job is set to 1 hour to check the aggregate of water quality data over the last hour. Extended periods of water abnormality are of concern - more so then second-to-second fluctuations.
5.    When abnormal levels are found, users are sent an email notification of a problem and how to rectify it.

There is potential to extend this to connection with other IoT aquarium maintenance equipment to create a fully automated solution where monitoring is tied in with response mechanisms.

## Infographics

![image](/presentation/Infographic.png)
![image](/presentation/aws-architecture.png)
