import json
import time
import json
import os
import time
from passlib.hash import pbkdf2_sha256

import boto3

def update(event, context):
    data = json.loads(event['body'])
    usrpwd = pbkdf2_sha256.encrypt(data['password'], rounds=200000, salt_size=16)
    data['password'] = usrpwd

    timestamp = int(time.time() * 1000)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


    attr_names = {
        '#user_role': "user_role",
        '#name': "name",
        '#first': "first",
        '#last': "last",
        '#active': "active",
        '#email': 'email',
        '#password': 'password',
        '#updated_on': 'updated_on'
    }

    attr_values = {
        ':active': data['active'],
        ':email': data['email'],
        ':password': data['password'],
        ':user_role': data['user_role'],
        ':first_name': data['first_name'],
        ':last_name': data['last_name'],
        ':updated_on': timestamp
    }

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames=attr_names,
        ExpressionAttributeValues=attr_values,
        UpdateExpression='SET #password= :password, '
                         '#name.#first= :first_name, '
                         '#name.#last= :last_name, '
                         '#email= :email, '
                         '#active= :active, '
                         '#updated_on= :updated_on, '
                         '#user_role= :user_role ',
        ReturnValues='ALL_NEW',
    )

    # create a response
    #response = {
    #    "statusCode": 200,
    #    "body": json.dumps(result['Attributes'],
    #                       cls=decimalencoder.DecimalEncoder)
    #}


    response = {
        "statusCode": 200,
        "body": json.dumps(event['pathParameters']['id'])
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
		"last_name": "456RICHARD-RIC",
		"email": "www555@domain.com",
		"password": "some_guid",
		"user_role": "dataentry",
		"active": "yes"
	})
    }
    # testing_data = json.dumps({'body':})
    data = json.loads(json.dumps(response))
    update(data, '')
