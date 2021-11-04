import json
import boto3
from datetime import datetime
import os 


    

def lambda_handler(event, context):
    #return event
    paginationToken=event["params"]["querystring"]["PaginationToken"]
    searchfield = event["params"]["querystring"]["searchtext"]
    cognito_clinet = boto3.client('cognito-idp')
    cognito_response = dict()
    #return event
    
    
    if paginationToken=="123456789":
        if event["params"]['querystring']["city"]=="1":
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                          Filter="preferred_username=\"{citys}\"".format(citys=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name","user"],
                                                          Limit=7)
        elif event["params"]['querystring']["bloodgroup"]=="1":
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                          Filter="family_name=\"{bloodgroup}\"".format(bloodgroup=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name"],
                                                          Limit=7)
        else:
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                          Filter="name^=\"{NAME}\"".format(NAME=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name"],
                                                          Limit=7)
                                                          
            
    else:
        if event["params"]['querystring']["city"]=="1":
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                          PaginationToken=paginationToken,
                                                          Filter="preferred_username=\"{citys}\"".format(citys=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name"],
                                                          Limit=15)
        elif event["params"]['querystring']["bloodgroup"]=="1":
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                            PaginationToken=paginationToken,
                                                          Filter="family_name=\"{bloodgroup}\"".format(bloodgroup=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name"],
                                                          Limit=15)
        else:
            cognito_response = cognito_clinet.list_users( UserPoolId=os.environ['user_pool_id'],
                                                          PaginationToken=paginationToken,
                                                          Filter="name^=\"{NAME}\"".format(NAME=searchfield),
                                                          AttributesToGet=["family_name","gender","email","family_name","given_name","preferred_username", "phone_number_verified","name"],
                                                          Limit=15)
    del cognito_response["ResponseMetadata"]
    
    for User in cognito_response['Users']:
        User.pop('UserLastModifiedDate','MFAOptions')
        User['UserCreateDate']=User['UserCreateDate'].strftime("%A, %d %B, %Y")
        
    
    return {
        'statusCode': 200,
        'body': cognito_response,
        "deepak":event["params"]['querystring']
    }
