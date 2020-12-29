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
"""

def get_hash_userid(userid):
    msg = userid+os.environ['app_client_id']
    msg_digest = hmac.new(str(os.environ['app_client_secret_id']).encode("UTF-8"),msg = str(msg).encode("UTF-8"),digestmod = hashlib.sha256).digest()
    decoded_digest  = base64.b64encode(msg_digest).decode()
    return decoded_digest

#generating random password
def password_genrator(n):
    chars=string.ascii_letters + string.digits +string.punctuation
    return ''.join(random.choice(chars) for _ in range(n))
    
"""
event object structure

{ 
      {"username":username }

      
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
        password = password_genrator(8)+"Xy1@"
        code = event['code']
        cognito_client.confirm_forgot_password(
            ClientId=os.environ['app_client_id'],
            SecretHash=get_hash_userid(username),
            Username=username,
            ConfirmationCode=code,
            Password=password,
           )
    except cognito_client.exceptions.UserNotFoundException as e:
        return {"Error": True, 
                "message": "Deepak:Username doesnt exists"}
    except cognito_client.exceptions.CodeMismatchException as e:
        return {"Error": True, 
               "message": "Deepak:Invalid Verification code"}
    except cognito_client.exceptions.LimitExceededException as e:
        return {"Error":True,"message":"Deppa:Too many login attempt.Please try after some time"}
    except Exception as e:
        return {"Error": True, 
                "message":str(e)}
      
    lambda_client = boto3.client('lambda')
    lambdainput={"username":username,"password":password}
    lambda_response = lambda_client.invoke(
                            FunctionName='arn:aws:lambda:us-east-1:121627579590:function:raktdan_login',
                            InvocationType='RequestResponse',
                            Payload=json.dumps(lambdainput))
        #print(lambda_response)
    lambda_response_return = json.load(lambda_response["Payload"])

    return {"statusCode":200,
    "body":lambda_response_return,
    "usergroup":False,
     "isBase64Encoded": False
               }
    
    
    