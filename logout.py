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


import os
import boto3
import botocore.exceptions



user_pool_id = os.environ['user_pool_id']
    

def lambda_handler(event, context):
    cognito_client = boto3.client("cognito-idp")
    access_token = event["AccessToken"]
    try:
        login_response = cognito_client.global_sign_out(
                 AccessToken=access_token)

    except Exception as e:
        return {"Message":str(e),"Error":True,}
    
    return {"Error":False}