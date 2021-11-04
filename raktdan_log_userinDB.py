import json
import boto3
from boto3.dynamodb.conditions import Key
import datetime
import time
import os


def lambda_handler(event, context):
    cognito_client = boto3.client('cognito-idp')
    profile1 = event["profile1"].replace("@","")
    timestamp = datetime.datetime.fromtimestamp(float(event["timestamp"])/1000.0).strftime("%a,%dth%b,%Y-%H:%M:%S")
    profile2 = event["profile2"].replace("@","")
    
    log_string_for_profile1 =  event["profile2"]+"`"+timestamp+"`"
    log_string_for_profile2 =  event["profile1"]+"`"+timestamp+"`"
    mobile1 = ""
    mobile2=""
    get_user_details1 = cognito_client.admin_get_user(UserPoolId=os.environ['user_pool_id'],Username=profile2)
    get_user_details2 = cognito_client.admin_get_user(UserPoolId=os.environ['user_pool_id'],Username=profile1)
    for each1,each2 in zip(get_user_details1["UserAttributes"],get_user_details2["UserAttributes"]):
        if each1['Name']=='phone_number':
            log_string_for_profile1+=each1["Value"]
            mobile1 = each1['Value']
        if each2['Name']=='phone_number':
            mobile2 = each2["Value"]
            log_string_for_profile2+=each2['Value']
    try:
        dynamodb_client =boto3.client('dynamodb')
        
        dynamodb_client.update_item(TableName='phone_log_request',
               Key={'email':{'S':event["profile1"]}},
                    ExpressionAttributeNames={'#attrbnam':'tujhe_kisne_dekha'},
                    ExpressionAttributeValues={':attrbval':{'L':[{'S':log_string_for_profile1}]},
                               ":empty_list":{"L": []}
                    },
                    UpdateExpression="set #attrbnam = list_append(if_not_exists(#attrbnam, :empty_list), :attrbval)"
                    )
        dynamodb_client.update_item(TableName='phone_log_request',
               Key={'email':{'S':event["profile2"]}},
                    ExpressionAttributeNames={'#attrbnam':'tumne_kise_dekha'},
                    ExpressionAttributeValues={':attrbval':{'L':[{'S':log_string_for_profile2}]},
                               ":empty_list":{"L": []}
                    },
                    UpdateExpression="set #attrbnam = list_append(if_not_exists(#attrbnam, :empty_list), :attrbval)"
                    )
    except Exception as e:
        return {"Error":True}
    try:
        # TODO: write code...
        lambda_client = boto3.client("lambda")
        lambda_response= lambda_client.invoke(
                            FunctionName='arn:aws:lambda:us-east-1:121627579590:function:test123',
                            InvocationType='RequestResponse',
                            Payload=json.dumps({"profile1":event["profile1"],"profile2":event["profile2"],"contactno":mobile1}))
    
    except Exception as e:
        return {"Error":True,"Message":str(e)}
    
    return {"satuscode":200,"Message":"Email has been sent to Your Registered Email","Error":False}
    
