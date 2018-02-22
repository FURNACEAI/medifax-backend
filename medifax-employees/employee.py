import os
import json
import time
import uuid
from passlib.hash import pbkdf2_sha256
from boto3.dynamodb.conditions import Key, Attr
from todos import decimalencoder
import boto3

def get(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response

def delete(event, context):
    """ Deletes an Employee from the database """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Success"})
    }

    return response

def list(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response

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
                "body": json.dumps({"message": "Success", "messageDesc": "Log successful."})
            }

    return response


if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-employees-dev'

    test_data = {
        "pathParameters": {
            "id": "248f670c-1796-11e8-94ff-aac4be946e9b"
        },
        "body": json.dumps({
		"email": "www555@domain.com",
        "password": "XXXsome_guid"
	})
    }
    test_json = json.loads(json.dumps(test_data))
    print(auth(test_json, ''))
