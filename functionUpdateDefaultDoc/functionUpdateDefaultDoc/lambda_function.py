import boto3
import json
import datetime
import time
import re

now = datetime.datetime.now()
s3res = boto3.resource('s3')
ec2client = boto3.client('ec2')
ec2res = boto3.resource('ec2')
current_month = str(now.month)
current_day = str(now.day)
aws_region = 'us-east-1'

def evaluate_instanceId_owner(ec2id):
    all_account_ec2 = ec2client.describe_instances(InstanceIds=[ec2id])
    list_account_ec2 = all_account_ec2['Reservations']
    for each_account_ec2 in list_account_ec2:
        account_ec2 = each_account_ec2['Instances']
        for each_account_ec2_id in account_ec2:
            ec2_tags = each_account_ec2_id['Tags']
            ec2_service = next(item for item in ec2_tags if item['Key'] == 'Service' )
            ec2_env = next(item for item in ec2_tags if item['Key'] == 'Env')
            if ec2_service['Value'] == 'account' and ec2_env['Value'] == 'production':
                #print(ec2_service['Value'] + ' ' + ec2_env['Value'])
                #print(ec2id)
                return ec2id
                #Call write2S3 function to update default document
                
#baseline tree structure
#-baseline/default-config.json
#-month/day/event-id.json

def update_to_s3_bucket():
    pass

def lambda_handler(event, context):
    #print(event)
    # Wait for 60 seconds
    # This is to wait the Create Tags event happen for ASG runInstances.
    # This will help to ensure the Tags value fully populated
    time.sleep(60)
    
    if event['detail']['eventName'] == 'RunInstances':
        list_res_elements = event['detail']['responseElements']['instancesSet']['items']
        #ec2regex = filter(r.match, list_res_elements)
        #print(str(ec2regex))
        for res_element in list_res_elements:
             instanceId = res_element['instanceId']
             result = evaluate_instanceId_owner(instanceId)
            
    #obj = s3res.Object('limliht-config','config/'+aws_region+'/'+current_month+'/'+current_day+'/RunInstancesByASG.json')
    #obj.put(Body=json.dumps(event))
    return 'Complete'