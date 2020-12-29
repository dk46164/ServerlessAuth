"""
Package required for doing signup

1.json => 
For Parsing the Json data

2.boto3 =>
 It provide api to call aws service on behalf of users.if you are calling boto3 sdk make sure 
 you have permission to do so. for e.g.
 
-> if lambda is calling certian aws service like creating s3 bucket then it have permission assigned
 from IAM to creating Bucket
->you are calling it from outside aws then see the documentation for configuring boto3 with dekstop/laptop
 
3.botocore.exceptions =>
Handling exceptions while user trying to registered

4. hmac =>
HMAC is a mechanism for message authentication using cryptographic hash functions.

5. base64 =>
It provides data encoding and decoding in base64.

6. haslib =>
Implements a common interface to many different secure hash and message digest algorithms
 

"""
import json
import boto3
import botocore.exceptions
import hmac
import base64
import hashlib
import string
import random
import os


"""
get_hash_userid(username) =>
It create a hash of (username +client id) and secret id using HMAC library 
return the encode 64 base digest as secert HASH

event object structure

{ "header":
    {------}
  "body":
      {"username":username 
      }
  "query":
      {-------}
  "params":
  {-----------}
      
}

All fields under params of event object are of string type
       
response object structure

{
    'CodeDeliveryDetails': {
        'Destination': 'string',
        'DeliveryMedium': 'SMS'|'EMAIL',
        'AttributeName': 'string'
    }
}

"""
def lambda_handler(event, context):
    cognito_client = boto3.client('cognito-idp')
    
    
    try:
        username = event['username']
        cognito_response = cognito_client.admin_reset_user_password(UserPoolId=os.environ['user_pool_id'],
                                                  Username=username)
    except cognito_client.exceptions.UserNotFoundException:
        return {"Error": True, 
                "Message": "Deepak:Username doesnt exists"}
    except cognito_client.exceptions.InvalidParameterException:
        return {"Error": True, 
              "Message": " Deepak:User is not confirmed yet.","msg_code":1}
        
    
    except Exception as e:
        return {"Error": True, 
                "Message": f"{e.__str__()}"}
     
    return {"Error": False, "Message": f"Please check your Registered Mobile Number for validation code"}

   