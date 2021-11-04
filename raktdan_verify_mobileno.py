import json
import boto3
import botocore.exceptions
import hmac
import base64
import hashlib
import os

def lambda_handler(event, context):
    # TODO implement
    #return event
    cognito_client = boto3.client("cognito-idp")
    if event.get('msg_code')==3:
        try:
            cognito_response = cognito_client.get_user_attribute_verification_code(AccessToken=event['AccessToken'],AttributeName='phone_number')
        except Exception as e:
            return {"Message":str(e),"Error":True}
    else:
        try:
            cognito_response = cognito_client.verify_user_attribute(AccessToken=event['AccessToken'],AttributeName='phone_number',Code=event['code'])
        except Exception as e:
            return {"Message":e,"Error":True}
        
    return {"msg":"hello"}
