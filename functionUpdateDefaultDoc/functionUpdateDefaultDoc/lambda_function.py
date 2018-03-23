# ***Event :– (Trigger points to update List of Prod AccountPF instance ID and ASG resource ID) 
# ASG or Non-ASG launched new instance/s with tagging Service:account and Env:production and Maintainer:DXC (RunInstances and eventsource :ec2)
# ASG or Non-ASG terminated instance/s with tagging Service:account and Env:production and Maintainer:DXC (TerminateInstances and eventsource :ec2 or asg)
# Create tags on instance that make instance/s fulfill tagging condition : Service:account and Env:production and Maintainer:DXC (CreateTags and eventsource :ec2 or asg)
# (Notification will be generated) Delete tags on instance/s that make instance lost the tagging fulfillment condition : Service:account and Env:production and Maintainer:DXC
# Create tags on ASG that make ASG fulfill tagging condition : Service:account and Env:production and Maintainer:DXC (createorUpdateTags)
# (Notification will be generated) Delete tags on ASG that make ASG lost the tagging fulfillment condition : Service:account and Env:production and Maintainer:DXC
# Delete ASG 
# Create ASG

from multiprocessing import Process, Pipe
import boto3
import json
import datetime
import time

now = datetime.datetime.now()
current_month = str(now.month)
current_day = str(now.day)

#Boto
s3_resource = boto3.resource('s3')
ec2client = boto3.client('ec2')
ec2res = boto3.resource('ec2')

#Global variables
aws_region = 'us-east-1'

#Functions
def check_ec2_tag(e, e_req):
    pass

def check_asg_tag(e, e_req):
    pass

def get_resource_id_from_e():
    pass
                
#baseline tree structure
#-baseline/default-config.json
#-month/day/event-id.json

def update_to_s3_bucket():
    pass

def read_ec2_list_from_s3():
    #This function can put in Multiprocessing
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/'+'ec2_default_document.json')
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    return loads_data

def read_asg_list_from_s3():
    #This function can put in Multiprocessing
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/'+'asg_default_document.json')
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    return loads_data

def check_with_accountpf_list(e_req):
    pass

def lambda_handler(event, context):
    #print(event)
    # Wait for 15 seconds
    # This is to wait the Create Tags event happen for ASG runInstances.
    # This will help to ensure the Tags value fully populated
    p_ec2list_r = Process(target=read_ec2_list_from_s3)
    
    e_name = event['detail']['eventName']
    e_source = event['detail']['eventSource']
    e_requestParameters = event['detail']['requestParameters']
    
    if e_name == 'RunInstances' and e_source == 'ec2.amazonaws.com':
        check_ec2_tag(event, e_requestParameters)
        print('This is EC2 RunInstances event')
    elif e_name == 'TerminateInstances':
        check_with_accountpf_list(e_requestParameters)
    elif e_name == 'CreateAutoScalingGroup':
        check_asg_tag(event, e_requestParameters)
    elif e_name == 'DeleteAutoScalingGroup':
        check_with_accountpf_list(e_requestParameters)
    else:
        print('No related event')
        
           

    return 'Complete'