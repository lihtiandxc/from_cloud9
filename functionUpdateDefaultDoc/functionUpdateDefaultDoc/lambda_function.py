# ***Event :– (Trigger points to update List of Prod AccountPF instance ID and ASG resource ID) 
# ASG or Non-ASG launched new instance/s with tagging Service:account and Env:production and Maintainer:DXC (RunInstances and eventsource :ec2)
# ASG or Non-ASG terminated instance/s with tagging Service:account and Env:production and Maintainer:DXC (TerminateInstances and eventsource :ec2 or asg)
# Create tags on instance that make instance/s fulfill tagging condition : Service:account and Env:production and Maintainer:DXC (CreateTags and eventsource :ec2 or asg)
# (Notification will be generated) Delete tags on instance/s that make instance lost the tagging fulfillment condition : Service:account and Env:production and Maintainer:DXC
# Create tags on ASG that make ASG fulfill tagging condition : Service:account and Env:production and Maintainer:DXC (createorUpdateTags)
# (Notification will be generated) Delete tags on ASG that make ASG lost the tagging fulfillment condition : Service:account and Env:production and Maintainer:DXC
# Delete ASG 
# Create ASG


import boto3
import json
import datetime
import time
import re
import threading

now = datetime.datetime.now()
s3res = boto3.resource('s3')
ec2client = boto3.client('ec2')
ec2res = boto3.resource('ec2')
current_month = str(now.month)
current_day = str(now.day)
aws_region = 'us-east-1'

def check_ec2_tag():
    pass

def check_asg_tag():
    pass

def get_resource_id_from_e():
    pass
                
#baseline tree structure
#-baseline/default-config.json
#-month/day/event-id.json

def update_to_s3_bucket():
    pass

def read_list_from_s3():
    pass

def 

def lambda_handler(event, context):
    #print(event)
    # Wait for 15 seconds
    # This is to wait the Create Tags event happen for ASG runInstances.
    # This will help to ensure the Tags value fully populated
    time.sleep(15)
    
    e_name = event['detail']['eventName']
    e_source = event['detail']['eventSource']
    e_requestParameters = event['detail']['requestParameters']
    
    if e_name == 'RunInstances':
           

    return 'Complete'