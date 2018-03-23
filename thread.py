import time
#import multiprocessing
#from multiprocessing import Process, Pipe
from threading import Thread
import boto3
import json


s3_resource = boto3.resource('s3')
aws_region = 'us-east-1'

def read_ec2_list_from_s3():
    #This function can put in Multiprocessing
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/ec2_default_document.json')
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    print(loads_data)

def read_asg_list_from_s3():
    #This function can put in Multiprocessing
    obj = s3_resource.Object('limliht-config','config/'+aws_region+'/asg_default_document.json')
    read_data = obj.get()['Body'].read()
    loads_data = json.loads(read_data)
    print(loads_data)
    
if __name__ == "__main__":
    
    t1 = time.time()
    p_read_ec2_list = Thread(target=read_ec2_list_from_s3)
    p_read_asg_lsit = Thread(target=read_asg_list_from_s3)
    
    p_read_ec2_list.start()
    p_read_asg_lsit.start()
    
    p_read_ec2_list.join()
    p_read_asg_lsit.join()
    print('total time spend = ', time.time()-t1 )
    
    t2 = time.time()
    read_asg_list_from_s3()
    read_ec2_list_from_s3()
    print('total time spend = ', time.time()-t2)
    
    print('Done')