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
import boto3
import botocore.exceptions
import hmac
import base64
import hashlib
import os



"""
get_hash_userid(username) =>
It create a hash of (username +client id) and secret id using HMAC library 
return the encode 64 base digest as secert HASH
"""

def get_hash_userid(userid):
    msg = userid+os.environ["app_client_id"]
    msg_digest = hmac.new(str(os.environ["app_client_secret_id"]).encode("UTF-8"),msg = str(msg).encode("UTF-8"),digestmod = hashlib.sha256).digest()
    decoded_digest  = base64.b64encode(msg_digest).decode()
    return decoded_digest

"""
event object structure

{ "header":
    {------}
  "body":
      {"username":username}
  "query":
      {-------}
  "params":
  {-----------}
      
}
cognito_response object structure

{
    'CodeDeliveryDetails': {
        'Destination': 'string',
        'DeliveryMedium': 'SMS'|'EMAIL',
        'AttributeName': 'string'
    }
}
"""

def lambda_handler(event, context):
    #creating a client object of cognito identity pool
    cognito_client = boto3.client('cognito-idp')
    
    try:
        username = event["body"]['username']
        cognito_response = cognito_client.resend_confirmation_code(SecretHash = get_hash_userid(username),
                                                                    Username=username,
                                                                    ClientId=os.environ["app_client_id"])
    except cognito_client.exceptions.UserNotFoundException:
        return {"Error": True,"Message":"deepak:Username doesnt exists"}
    except cognito_client.exceptions.InvalidParameterException:
        return {"Error":True,"Message": "deepaK:User is already confirmed"}
    except Exception as e:
        return {"Error": True, "Message": f"Unknown error {e.__str__()} "}
    return { "Error":False,"Message":"please check your  registered email for OTP "}
