import json
import boto3
from datetime import datetime
import os 


    

def lambda_handler(event, context):
    # TODO implement
    paginationToken=event["params"]['querystring']["PaginationToken"]
    
    cognito_clinet = boto3.client('cognito-idp')
    cognito_response =dict()
    
    if paginationToken=="123456789":
        cognito_response = cognito_clinet.list_users(
            UserPoolId=os.environ['user_pool_id'],
            Limit=15
            )
    else:
        cognito_response = cognito_clinet.list_users(
            UserPoolId=os.environ['user_pool_id'],
            PaginationToken=paginationToken,
            Limit=15,
           
            )
    for User in cognito_response['Users']:
        User.pop('UserLastModifiedDate','MFAOptions')
        User['UserCreateDate']=User['UserCreateDate'].strftime("%A, %d %B, %Y")
    
    del cognito_response["ResponseMetadata"]

    for each_users in cognito_response["Users"]:
        del each_users["Enabled"]
        del each_users["UserStatus"]
        temp =[]
        for each_attributes in range(10):
            if each_users["Attributes"][each_attributes]["Name"] not in  ["phone_number_verified","email_verified","sub","phone_number"]:
                t = {each_users["Attributes"][each_attributes]["Name"]:each_users["Attributes"][each_attributes]["Value"]}
                temp.append(t)
        each_users["Attributes"]=temp

        
    
    return {
        'statusCode': 200,
        'body': cognito_response
    }
