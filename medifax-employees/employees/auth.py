import os
import json
from passlib.hash import pbkdf2_sha256
import boto3
from boto3.dynamodb.conditions import Key, Attr

def auth(event, context):
    """
    Attempts to verify a user's login credentials
    Fetches the hashed version of the password via the username and attempts to verify it with pbkdf2_sha256.verify()

    Returns a JSON response with either "Success" or "Error".
    """
    data = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.scan(
        FilterExpression=Attr("email").eq(data['email'])
    )

    ## Set the default response to failure and then test for success.
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Error", "messageDesc": "Username or password is incorrect."})
    }

    if len(result['Items']) > 0: # Sanity check to see if the username was correct
        if pbkdf2_sha256.verify(data['password'], result['Items'][0]['password']):
            response = {
                "statusCode": 200,
                "body": json.dumps({"message": "Success", "messageDesc": "Log successful.", "id": result['Items'][0]['id']})
            }


    return response

if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-employees-dev'
    response = {
        "body": json.dumps({
		"email": "www555@domain.com",
		"password": "newpwd"
	})
    }
    data = json.loads(json.dumps(response))
    res = auth(data, '')
    print(res)
