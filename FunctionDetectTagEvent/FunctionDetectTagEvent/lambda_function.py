from datetime import datetime
import json
import os
import boto3

ec2_resource = boto3.resource('ec2')
asg_client = boto3.client('autoscaling')
s3_resource = boto3.resource('s3')
aws_region = 'us-east-1'
env_tag_key = 'Env'
env_tag_value = 'production'
service_tag_key = 'Service'
service_tag_value = 'account'

def construct_sns_general_msg(e):
    
    build_dict = {}
    build_dict['accesskey_id'] = e['userIdentity']['accessKeyId']
    build_dict['username'] = e['userIdentity']['userName']
    build_dict['event_name'] = e['eventName']
    build_dict['aws_region'] = e['awsRegion']
    build_dict['source_ip'] = e['sourceIPAddress']
    build_dict['event_id'] = e['eventID']
    
    str_e = json.dumps(e)
    str_e_data = json.loads(str_e)
    event_time_json = str_e_data['eventTime']
    #Transform the JSON time format to datetime format
    build_dict['event_time_datetime_format'] = str(datetime.strptime(event_time_json, '%Y-%m-%dT%H:%M:%SZ'))

    print(build_dict)
    return build_dict
    
def construct_sns_msg_ec2(e, msg):
    pass

def construct_sns_msg_asg(e, msg):
    pass

# def check_ec2_service(e,req):
#     instance_id = req['resourcesSet']['items'][0]['resourceId']
#     instance = ec2_resource.Instance(instance_id)
#     # #The following logic might not suitable, the tagging value will change and result will inaccurate
#     tagging = instance.tags
#     #print(tagging)
#     dict_service_value = next(item for item in tagging if item['Key'] == 'Service' )
#     dict_env_value = next(item for item in tagging if item['Key'] == 'Env' )
#     this_ec2_service_value = dict_service_value['Value']
#     this_ec2_env_value = dict_env_value['Value']
#     print(this_ec2_service_value)
#     print(this_ec2_env_value)
#     return True

def read_list_from_s3():
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/default_document.json')
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    # print(ready_data)
    return loads_data


def check_ec2_owner(e,req):
    instance_id = req['resourcesSet']['items'][0]['resourceId']
    list_account_ec2 = read_list_from_s3()
    if instance_id in list_account_ec2:
        return True
    else:
        return False
        
def check_asg_owner(e,req):
    list_resource_id = req['tags']
    dict_resource_id = next(item for item in list_resource_id if item['resourceType'] == 'auto-scaling-group' )
    resource_id = dict_resource_id['resourceId']
    if resource_id in list_account_asg:
        return True
    else:
        return False
    #print(resource_id)
    #if resource_id in l
    
    
def check_asg_service(e,req):
    pass
    # event_resource_id = req['tags'][0]['resoureId']
    # autoscaling_group = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[event_resource_id])
    # tagging_key = autoscaling_group['AutoScalingGroups'][0]['Tags']
    #     if tagging_key == env_tag_key:
    #         if tagging_value = 
    
    # if event_resource_id == autoscaling_resource_id:
    #     return True
    # else:
    #     print('This is not an AccountPF autoscaling group')
            
def lambda_handler(event, context):
    # TODO implement
    #print(event)
    read_list_from_s3()
    request_parameters = event['detail']['requestParameters']
    if event['detail']['eventSource'] == 'ec2.amazonaws.com':
        if (event['detail']['eventName'] == 'CreateTags' or 'DeleteTags'):
            if check_ec2_owner(event, request_parameters) is True: 
                print('This is Production AccountPF EC2 Tagging event')
                general_msg = construct_sns_general_msg(event['detail'])
                construct_sns_msg_ec2(event['detail'], general_msg)
            else:
                print('This is not a Production AccountPF EC2 Tagging event')
            
    elif event['detail']['eventSource'] == 'autoscaling.amazonaws.com':
        if event['detail']['eventName'] == 'CreateOrUpdateTags':
            if check_asg_owner(event, request_parameters) is True:
                print('This is Production AccountPF AutoScaling Tagging event')
                general_msg = construct_sns_general_msg(event['detail'])
                construct_sns_msg_asg(event['detail'], general_msg)
    else:
        print('No matching event reported')
    return 'Success'