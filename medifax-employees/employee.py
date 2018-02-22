import os
import json
import time
import uuid
from passlib.hash import pbkdf2_sha256

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create(event, context):

    """ Creates a new Employee record that is capable of logging into the backend/admin panel. """
    data = json.loads(event['body'])
    usrpwd = pbkdf2_sha256.encrypt(data['password'], rounds=200000, salt_size=16)
    uid = str(uuid.uuid1())
    """
    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
        return
    """

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


    item = {
        'id': uid,
        'name': {'first': data['first-name'], 'last': data['last-name']},
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

def get(event, context):
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

def update(event, context):
    data = json.loads(event['body'])
    #if data['password']:
    usrpwd = pbkdf2_sha256.encrypt(data['password'], rounds=200000, salt_size=16)
    #else:
    data['password'] = usrpwd

    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    attr_names = {
        '#name': "name",
        '#firstname': "first",
        '#active': "active",
        '#email': 'email',
        '#udpated_on': 'updated_on'
    }

    ## Set the attribute values
    attr_values = {
        ':active': data['active'],
        ':email': data['email'],
        ':password': data['password'],
        ':user_role': data['user_role'],
        ':updated_on': timestamp
    }

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames=attr_names,
        ExpressionAttributeValues=attr_values,
        UpdateExpression='SET password = :password, '
                         '#email = :email, '
                         'user_role = :user_role, '
                         '#active = :active, '
                         '#updated_on = :updated_on',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response

def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
