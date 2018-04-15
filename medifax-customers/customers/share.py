import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def send_email(sender, recipient, subject, msgbody):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Medifax <bryan@furnaceai.com>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "contact@furnaceai.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': msgbody,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': msgbody,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        # return False
        print(e.response['Error']['Message'])
    else:
        return True
        #print("Email sent! Message ID:"),
        #print(response['ResponseMetadata']['RequestId'])

def share(event, context):
    data = json.loads(event['body'])
    subject = "%s Would Like to Share Their Medifax Records" % data['name']
    recipient = data['email']
    sender = 'Medifax <bryan@furnaceai.com>'
    fullname = data['name']
    userid = event['pathParameters']['id']
    subject = "%s Wants to Share Their Medifax Records With You" % fullname
    msgbody = """<h2>%s has requested to share their Medifax records with you.</h2>

    <p>To access their records, please click <a href="http://dev-env.gsuvdcrfpg.us-east-1.elasticbeanstalk.com/medical/%s">here</a>.</p>

    <p>If the above link is not clickable, copy and paste this URL into your browser's titlebar: http://dev-env.gsuvdcrfpg.us-east-1.elasticbeanstalk.com/medical/%s</p>
    """ % (fullname, userid, userid)

    # def send_email(sender, recipient, subject, msgbody):
    msg = send_email(sender, recipient, subject, msgbody)
    if msg:
        response = {
            "statusCode": 200,
            "body": json.dumps({"message":msg})
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps({"message":"Error"})
        }
    return response

if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    payload = {
        "pathParameters": {
            "id": "c85cf638-3aa0-11e8-8bb4-5e566f9ab6c7"
        },
        "body": json.dumps({
            "email": "contact@furnaceai.com",
            "name": "Bryan Richard"
        })
    }
    data = json.loads(json.dumps(payload))
    print(data)
    res = share(data, '')
    print(res)
