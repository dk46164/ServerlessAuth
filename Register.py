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
import random
import os
import string

#user_pool_id  from congito userpool you get pool id
#app_client_id  #under cognito/App client these  
#app_client_secret_id #field can be found

#creating a client object of cognito identity pool

cognito_client = boto3.client("cognito-idp")

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

#generating random password
def password_genrator(n):
    chars=string.ascii_letters + string.digits +string.punctuation
    return ''.join(random.choice(chars) for _ in range(n))
"""
event object structure

{ "header":
    {------}
  "body":
      {"username":username, 
       "email":email
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
    'UserConfirmed': True|False,
    'CodeDeliveryDetails': {
        'Destination': 'string',
        'DeliveryMedium': 'SMS'|'EMAIL',
        'AttributeName': 'string'
    },
    'UserSub': 'string'
}
          
"""
def lambda_handler(event, context):
    # TODO implement
    name = event["body"]["name"]
    pre_username = event["body"]["city"]
    phonenumber = "+91"+event["body"]["phonenumber"]
    gender = event["body"]["gender"]
    familyname = event["body"]["bloodgroup"]
    givenname=event["body"]["age"]
    password = password_genrator(8)+"X1!y"
    email=event["body"]["email"]
    
    
    try:
        response = cognito_client.sign_up(ClientId = os.environ["app_client_id"],
                                          SecretHash = get_hash_userid(email),
                                          Username = email,
                                          Password = password,
                                          
                                          UserAttributes = [
                                                        {"Name":"name","Value":name},
                                                        {"Name":"email","Value":email},
                                                        {"Name":"phone_number","Value":phonenumber},
                                                        {"Name":"gender","Value":gender},
                                                        {"Name":"family_name","Value":familyname},
                                                        {"Name":"given_name","Value":givenname},
                                                        {"Name":"preferred_username","Value":pre_username}
                                                       
                                                        
                                                        ],
                                          ValidationData = [
                                                             {"Name":"phone_number","Value":phonenumber},
                                                             {"Name":"email","Value":email}
                                                            ]
                                        )
    
    except cognito_client.exceptions.UserLambdaValidationException as e:
        return {"Error":True,"Message":"Deepak:Mobile Number is  already registered"}
    except cognito_client.exceptions.UsernameExistsException as e:
        return {"Error":True,"Message":"Deepak:Username already registered","msg_code":0}
        
    except Exception as e:
        return {"Error":True,"Message":str(e)}
    
    """
    In the last return ,we can either return reponse object or customized message
    
    """
    
    print(event,response)
     
    return {"Error":False,"Message":"Please Verfiy email."}
