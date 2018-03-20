from datetime import datetime
import json
import os
import boto3

ec2_resource = boto3.resource('ec2')
asg_client = boto3.client('autoscaling')
s3_resource = boto3.resource('s3')
sns_client = boto3.client('sns')
aws_region = 'us-east-1'
env_tag_key = 'Env'
env_tag_value = 'production'
service_tag_key = 'Service'
service_tag_value = 'account'
sns_topic_arn = 'arn:aws:sns:us-east-1:751611215147:limliht_gmail'

def construct_sns_general_msg(e):
    
    build_dict = {}
    build_dict['accesskey_id'] = e['userIdentity']['accessKeyId']
    build_dict['username'] = e['userIdentity']['userName']
    build_dict['event_name'] = e['eventName']
    build_dict['aws_region'] = e['awsRegion']
    build_dict['source_ip'] = e['sourceIPAddress']
    build_dict['event_id'] = e['eventID']
    build_dict['user_agent'] = e['userAgent']
    
    str_e = json.dumps(e)
    str_e_data = json.loads(str_e)
    event_time_json = str_e_data['eventTime']
    #Transform the JSON time format to datetime format
    build_dict['event_time_datetime_format'] = str(datetime.strptime(event_time_json, '%Y-%m-%dT%H:%M:%SZ'))

    print(build_dict)
    return build_dict
    
def construct_sns_msg(e, e_name, msg, resource_id):
    print(e_name)
    if e_name == 'CreateTags' or e_name == 'DeleteTags':
        activity = e['requestParameters']['tagSet']
        email_subject = 'Notification AccountPF EC2 tagging event!'
    else:
        activity = e['requestParameters']['tags']
        email_subject = 'Notification AccountPF ASG tagging event!'
    
    str_e = json.dumps(e)
    body_msg = 'Event summary: \
    \n\nEvent name : ' + msg['event_name'] + \
    '\nResource Id : ' + resource_id + \
    '\nChange Items : ' + json.dumps(activity) + \
    '\nEvent Id : ' + msg['event_id'] + \
    '\nEvent time (UTC) : ' + msg['event_time_datetime_format'] + \
    '\nUser Access Key : ' + msg['accesskey_id'] + \
    '\nUsername : ' + msg['username'] + \
    '\nAWS Region : ' + msg['aws_region'] + \
    '\nSource IP : ' + msg['source_ip'] + \
    '\nUser Agent :' + msg['user_agent'] + \
    '\n\n\n' + 'Raw event: ' + \
    '\n\n' + str_e
    
    trigger_notification(body_msg,email_subject)
    

def read_list_from_s3(default_document):
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/'+default_document)
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    # print(ready_data)
    return loads_data


def check_ec2_owner(e,req):
    ec2_json = 'ec2_default_document.json'
    instance_id = req['resourcesSet']['items'][0]['resourceId']
    list_account_ec2 = read_list_from_s3(ec2_json)
    result = next((item for item in list_account_ec2 if item["id"] == instance_id), False)
    if result is False:
        print('This is not in scope')
    else:
        return instance_id

def check_asg_owner(e,req):
    asg_json = 'asg_default_document.json'
    list_resource_id = req['tags']
    dict_resource_id = next(item for item in list_resource_id if item['resourceType'] == 'auto-scaling-group' )
    resource_id = dict_resource_id['resourceId']
    list_account_asg = read_list_from_s3(asg_json)
    result = next((item for item in list_account_asg if item["id"] == resource_id), False)
    if result is False:
        print('This is not in scope')
    else:
        return resource_id

def trigger_notification(event_detail, subject):
    sns_client.publish(TargetArn = sns_topic_arn, MessageStructure = 'string', \
    Message = event_detail, Subject = subject)
    
            
def lambda_handler(event, context):
    # TODO implement
    #print(event)
    #read_list_from_s3()
    request_parameters = event['detail']['requestParameters']
    if event['detail']['eventSource'] == 'ec2.amazonaws.com':
        if event['detail']['eventName'] == 'CreateTags' or event['detail']['eventName'] == 'DeleteTags':
            if check_ec2_owner(event, request_parameters) is not None: 
                print('This is DXC in scope Production AccountPF EC2 Tagging event')
                general_msg = construct_sns_general_msg(event['detail'])
                resource = check_ec2_owner(event, request_parameters)
                construct_sns_msg(event['detail'], event['detail']['eventName'], general_msg, resource)
            else:
                print('This is not a DXC in-scope Production AccountPF EC2 Tagging event')
            
    elif event['detail']['eventSource'] == 'autoscaling.amazonaws.com':
        if event['detail']['eventName'] == 'CreateOrUpdateTags':
            if check_asg_owner(event, request_parameters) is not None:
                print('This is Production AccountPF AutoScaling Tagging event')
                general_msg = construct_sns_general_msg(event['detail'])
                resource = check_asg_owner(event, request_parameters)
                construct_sns_msg(event['detail'], event['detail']['eventName'], general_msg, resource)
            else:
                print('This is not a DXC in-scope Production AccountPF ASG Tagging event')
    else:
        print('No matching event reported')
    return 'Success'