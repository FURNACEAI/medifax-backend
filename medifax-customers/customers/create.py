import json
import logging
import os
import time
import uuid
from passlib.hash import pbkdf2_sha256
import random
from random import randint
import string
import boto3
from boto3.dynamodb.conditions import Key, Attr

def value_exists(table, column, val):
    result = table.scan(
        FilterExpression=Attr(column).eq(val)
    )
    if result['Items']:
        # If the query succeeds then the value already exists in the database
        return True
    else:
        return False

def generate_pw(length):
    pwd = []
    pwd.append(random.choice(string.ascii_lowercase))
    pwd.append(random.choice(string.ascii_uppercase))
    pwd.append(str(random.randint(1,9)))
    # fill out the rest of the characters
    # using whatever algorithm you want
    # for the next "length" characters
    random.shuffle(pwd)
    return ''.join(pwd)

def create(event, context):
    """
    Creates a new Customer record that is capable of logging into their account via the frontend
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

    # Generate a seven-digit access code for the dog tags
    valid_acode = False
    while not valid_acode:
        accesscode = randint(1000000000, 9999999999)
        if not value_exists(table, 'access_code', accesscode):
            valid_acode = True

    # Check if email address already exists
    if value_exists(table, 'email', data['email']):
        val_exists_response = {
            "statusCode": 200,
            "body": json.dumps({"message":"Error", "messageDesc":"Email address is currently taken by another customer."})
        }
        return val_exists_response

    cleartext_pwd = generate_pw(8)
    usrpwd = pbkdf2_sha256.encrypt(cleartext_pwd, rounds=200000, salt_size=16)
    uid = str(uuid.uuid1())
    timestamp = int(time.time())

    item = {
        'id': uid,
        'name': {'first': data['first_name'], 'middle_initial': data['middle_initial'], 'last': data['last_name']},
        'home_address': {
            'street_address': data['street_address'],
            'street_address_2': data['street_address_2'],
            'city': data['city'],
            'state': data['state'],
            'zipcode': data['zipcode']
            },
        'dob': data['dob'],
        'phone': { 'home': data['home_phone'], 'mobile': data['mobile_phone'] },
        'email': data['email'],
        'access_code': accesscode,
        'password': usrpwd,
        'active': 'true',
        'status': 'Awaiting HIPAA Consent',
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
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    payload = {
        "body": json.dumps({
            "first_name": 'form.first_name.data',
            "last_name": 'form.last_name.data',
            "email": 'xxxform.email.data',
            "home_phone": None,
            "mobile_phone": '8019539821',
            "street_address": '3356 S 1100 E',
            "street_address_2": 'z',
            "city": 'Los Angeles',
            "state": 'CA',
            "zipcode": '90245',
            "dob": '10/10/1910'
        })
    }

    data = json.loads(json.dumps(payload))
    res = create(data, '')
    print(res)
