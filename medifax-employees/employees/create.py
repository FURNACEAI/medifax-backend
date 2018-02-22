import json
import logging
import os
import time
import uuid
from passlib.hash import pbkdf2_sha256

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

if __name__ == '__main__':
    json = """{"body":{
    "first-name": "EEFirstName-{{$randomInt}}",
    "last-name": "EEFirstName-{{$randomInt}}",
    "email": "emailadd-{{$randomInt}}@domain.com",
    "password": "{{$guid}}",
    "role": "admin",
    "active": true
    }}"""
    create(json, '')
