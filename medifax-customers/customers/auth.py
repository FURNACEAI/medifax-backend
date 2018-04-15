import os
import json
from passlib.hash import pbkdf2_sha256
import boto3
from boto3.dynamodb.conditions import Key, Attr

def auth(event, context):
    """
    Attempts to verify a customer's access code.

    Returns a JSON response with either "Success" or "Error".
    """
    data = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan(
        FilterExpression=Attr("access_code").eq(data['access_code'])
    )

    ## Set the default response to failure and then test for success.
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Error", "messageDesc": "Could not locate Customer record."})
    }

    if len(result['Items']) > 0: # Sanity check to see if the access_code was correct
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": "Success", "messageDesc": "Log successful.", "id": "%s" % result['Items'][0]['id']})
        }

    return response

if __name__ == '__main__':
    ## Configure boto for local environment
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    ac = "4310640963"
    response = {
        "body": json.dumps({
		"access_code": ac
	})
    }
    # testing_data = json.dumps({'body':})
    data = json.loads(json.dumps(response))
    print(auth(data, ''))
