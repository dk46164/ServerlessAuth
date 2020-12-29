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
import os


user_pool_id = os.environ['user_pool_id']
app_client_id = os.environ['app_client_id']
app_client_secret_id = os.environ['app_client_secret_id']




"""
get_hash_userid(username) =>
It create a hash of (username +client id) and secret id using HMAC library 
return the encode 64 base digest as secert HASH
"""

def get_hash_userid(userid):
    msg = userid+app_client_id
    msg_digest = hmac.new(str(app_client_secret_id).encode("UTF-8"),msg = str(msg).encode("UTF-8"),digestmod = hashlib.sha256).digest()
    decoded_digest  = base64.b64encode(msg_digest).decode()
    return decoded_digest



"""
event object structure

{ "header":
    {------}
  "body":
      {"username":username, 
       "password":password
      }
  "query":
      {-------}
  "params":
  {-----------}
      
}

All fields under params of event object are of string type
       
response object structure

{
    'ChallengeName': 'SMS_MFA'|'SOFTWARE_TOKEN_MFA'|'SELECT_MFA_TYPE'|'MFA_SETUP'|'PASSWORD_VERIFIER'|'CUSTOM_CHALLENGE'|'DEVICE_SRP_AUTH'|'DEVICE_PASSWORD_VERIFIER'|'ADMIN_NO_SRP_AUTH'|'NEW_PASSWORD_REQUIRED',
    'Session': 'string',
    'ChallengeParameters': {
        'string': 'string'
    },
    'AuthenticationResult': {
        'AccessToken': 'string',
        'ExpiresIn': 123,
        'TokenType': 'string',
        'RefreshToken': 'string',
        'IdToken': 'string',
        'NewDeviceMetadata': {
            'DeviceKey': 'string',
            'DeviceGroupKey': 'string'
        }
    }
}

"""

def login(event, context):
    #creating a client object of cognito identity pool
    cognito_client = boto3.client("cognito-idp")
    refresh_token = event["refreshToken"]
    username=event['username']
    try:
        login_response = cognito_client.admin_initiate_auth(
                 UserPoolId=user_pool_id,
                 ClientId=app_client_id,
                 AuthFlow='REFRESH_TOKEN_AUTH',
                 AuthParameters={'SECRET_HASH': get_hash_userid(username),'REFRESH_TOKEN': refresh_token},
               
                )

    except Exception as e:
        return {"Message":str(e),"Error":True}
    
    return [login_response,False]