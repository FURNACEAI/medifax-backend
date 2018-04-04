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

    # Creation and modify timestamp
    timestamp = int(time.time())

    # Replace any empty values with Python 'None' type
    for key, value in data.items():
        if not value:
            data[key] = None

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
        'blood_pressure_systolic': None,
        'blood_pressure_diastolic': None,
        'height': None,
        'weight': None,
        'heart_rate': None,
        'bmi': None,
        'gender': None,
        'current_problems_0': None,
        'current_problems_1': None,
        'current_problems_2': None,
        'current_problems_3': None,
        'current_problems_4': None,
        'current_problems_5': None,
        'current_problems_6': None,
        'current_problems_7': None,
        'current_problems_8': None,
        'current_problems_9': None,
        'medication_name_0': None,
        'medication_name_1': None,
        'medication_name_2': None,
        'medication_name_3': None,
        'medication_name_4': None,
        'medication_name_5': None,
        'medication_name_6': None,
        'medication_name_7': None,
        'medication_name_8': None,
        'medication_name_9': None,
        'medication_dose_0': None,
        'medication_dose_1': None,
        'medication_dose_2': None,
        'medication_dose_3': None,
        'medication_dose_4': None,
        'medication_dose_5': None,
        'medication_dose_6': None,
        'medication_dose_7': None,
        'medication_dose_8': None,
        'medication_dose_9': None,
        'medication_freq_0': None,
        'medication_freq_1': None,
        'medication_freq_2': None,
        'medication_freq_3': None,
        'medication_freq_4': None,
        'medication_freq_5': None,
        'medication_freq_6': None,
        'medication_freq_7': None,
        'medication_freq_8': None,
        'medication_freq_9': None,
        'patient_preferences': None,
        'patient_consents': None,
        'family_history': None,
        'allergies': None,
        'referrals': None,
        'lab_results': None,
        'care_plan': None,
        'lifestyle_history': None,
        'social_history': None,
        'dentist_name': None,
        'dentist_phone': None,
        'dentist_email': None,
        'dental_condition': None,
        'ins_planid_dental': None,
        'ins_provider_dental': None,
        'ins_street_addr_dental': None,
        'ins_city_dental': None,
        'ins_state_dental': None,
        'ins_zipcode_dental': None,
        'ins_phone_dental': None,
        'ins_email_dental': None,
        'ins_planid_med': None,
        'ins_provider_med': None,
        'ins_street_addr_med': None,
        'ins_city_med': None,
        'ins_state_med': None,
        'ins_zipcode_med': None,
        'ins_phone_med': None,
        'ins_email_med': None,
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
            "first_name": 'James',
            "middle_initial": 'T',
            "last_name": 'Matt',
            "email": 'testing@example.com',
            "home_phone": None,
            "mobile_phone": '8019539821',
            "street_address": '3356 S 1100 E',
            "street_address_2": 'z',
            "city": 'Los Angeles',
            "state": 'CA',
            "zipcode": '90245',
            "dob": '10/10/1910',
            "active": 'true'
        })
    }

    data = json.loads(json.dumps(payload))
    res = create(data, '')
    print(res)
