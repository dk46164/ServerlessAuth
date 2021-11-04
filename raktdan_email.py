import json
import boto3

def lambda_handler(event, context):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "mail@deepakumar.de"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = event["profile2"]
    mail_id = event["profile1"]
    mobile_no = event["contactno"]

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "User Details\r\n"
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("User Details\r\n"
           "THis is to notify that someone has requested your help.You can check following details,if you think it is genuine\n or go Under MyProfile->Requested profile\n.Thank You.")
            
    # The HTML body of the email.
    BODY_HTML ="""<html>
                            <head></head>
                                <body>
                                <h1>User Details</h1>
                                <table >
                                <tr>
                                <th>User's Email &ensp;&ensp;</th>
                                <th>Contact Number</th>
                                </tr>
                                <tr>
                                <td>{user1}&ensp;&ensp;</td>
                                <td>{no}</td>
                                </tr>
                                </table>
                                <p>Thank You </p>
                                </body>
                                </html>""".format(user1=mail_id,no=mobile_no )         

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
    #Provide the contents of the email.
        response = client.send_email(Destination={'ToAddresses': [RECIPIENT,]},
                                        Message={'Body': {
                                                    'Html': {
                                                        'Charset': CHARSET,
                                                    'Data': BODY_HTML,
                                                            },
                                                            'Text': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT,
                            },
                        },
                        'Subject': {
                            'Charset': CHARSET,
                            'Data': SUBJECT,
                        },
                    },
                    Source=SENDER,
                       
           
        )
        
    # Display an error if something goes wrong.	
    except Exception as e:
        return {"Error":True,"Message":"deepak:"+str(e)}
    else:
        return {"Error":False,"Message":"deepak:Email has been sent to Your Registered Email"}
   