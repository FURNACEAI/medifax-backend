import json
import logging
import os
import time
import uuid
from passlib.hash import pbkdf2_sha256
import boto3
from boto3.dynamodb.conditions import Key, Attr

def create(event, context):
    """
    Creates a new Employee record that is capable of logging into the backend/admin panel
    """

    """
    TODO: Data validation routines
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
        return
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    data = json.loads(event['body'])

    result = table.scan(
        FilterExpression=Attr("email").eq(data['email'])
    )
    if result['Items']:
        # If the query succeeds then the email address already exists in the database.
        email_exists_response = {
            "statusCode": 200,
            "body": json.dumps({"message":"Error", "messageDesc":"Email address exists"})
        }
        return email_exists_response

    usrpwd = pbkdf2_sha256.encrypt(data['password'], rounds=200000, salt_size=16)
    uid = str(uuid.uuid1())

    timestamp = int(time.time())

    item = {
        'id': uid,
        'name': {'first': data['first_name'], 'last': data['last_name']},
        'email': data['email'],
        'password': usrpwd,
        'user_role': data['user_role'],
        'active': data['active'],
        'created_on': timestamp,
        'updated_on': timestamp,
    }

    ## Write the record to the database
    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps({"message":"Success", "id":uid})
    }

    return response

if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-employees-dev'

    response = {
        "pathParameters": {
            "id": "248f670c-1796-11e8-94ff-aac4be946e9b"
        },
        "body": json.dumps({
		"first_name": "123BRYAN-BRY",
		"last_name": "RICHARD-RIC",
		"email": "xefoobar555@domain.com",
		"password": "some_guid",
		"user_role": "dataentry",
		"active": "yes"
	})
    }
    data = json.loads(json.dumps(response))
    res = create(data, '')
    print(res)
