import json
import os
import time
from passlib.hash import pbkdf2_sha256
import boto3
from boto3.dynamodb.conditions import Key, Attr

def update(event, context):
    data = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    # Update time
    timestamp = int(time.time() * 1000)
    # Check if a password was passed to the event param. If not, use the existing password.
    if not data['password']:
        result = table.get_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )
        data['password'] = result['Item']['password']
    else:
        usrpwd = pbkdf2_sha256.encrypt(data['password'], rounds=200000, salt_size=16)
        data['password'] = usrpwd

    # Critical for DynamoDB: Replace any empty values with Python 'None' type
    for key, value in data.items():
        if not value:
            data[key] = None

    attr_names = {
        '#name': "name",
        '#first': "first",
        '#middle_initial': "middle_initial",
        '#home_address': "home_address",
        '#phone': "phone",
        '#home': "home",
        '#mobile': "mobile",
        '#street_address': "street_address",
        '#street_address_2': "street_address_2",
        '#city': "city",
        '#state': "state",
        '#zipcode': "zipcode",
        '#last': "last",
        '#email': 'email',
        '#password': 'password',
        '#dob': 'dob',
        '#height': 'height',
        '#weight': 'weight',
        '#heart_rate': 'heart_rate',
        '#active': 'active',
        '#status': 'status',
        '#gender': 'gender',
        '#patient_preferences': 'patient_preferences',
        '#patient_consents': 'patient_consents',
        '#family_history': 'family_history',
        '#allergies': 'allergies',
        '#referrals': 'referrals',
        '#lab_results': 'lab_results',
        '#care_plan': 'care_plan',
        '#lifestyle_history': 'lifestyle_history',
        '#social_history': 'social_history',
        '#bmi': 'bmi',
        '#blood_pressure_systolic': 'blood_pressure_systolic',
        '#blood_pressure_diastolic': 'blood_pressure_diastolic',
        '#blood_type': 'blood_type',
        '#current_problems_0': 'current_problems_0',
        '#current_problems_1': 'current_problems_1',
        '#current_problems_2': 'current_problems_2',
        '#current_problems_3': 'current_problems_3',
        '#current_problems_4': 'current_problems_4',
        '#current_problems_5': 'current_problems_5',
        '#current_problems_6': 'current_problems_6',
        '#current_problems_7': 'current_problems_7',
        '#current_problems_8': 'current_problems_8',
        '#current_problems_9': 'current_problems_9',
        '#medication_name_0': 'medication_name_0',
        '#medication_name_1': 'medication_name_1',
        '#medication_name_2': 'medication_name_2',
        '#medication_name_3': 'medication_name_3',
        '#medication_name_4': 'medication_name_4',
        '#medication_name_5': 'medication_name_5',
        '#medication_name_6': 'medication_name_6',
        '#medication_name_7': 'medication_name_7',
        '#medication_name_8': 'medication_name_8',
        '#medication_name_9': 'medication_name_9',
        '#medication_dose_0': 'medication_dose_0',
        '#medication_dose_1': 'medication_dose_1',
        '#medication_dose_2': 'medication_dose_2',
        '#medication_dose_3': 'medication_dose_3',
        '#medication_dose_4': 'medication_dose_4',
        '#medication_dose_5': 'medication_dose_5',
        '#medication_dose_6': 'medication_dose_6',
        '#medication_dose_7': 'medication_dose_7',
        '#medication_dose_8': 'medication_dose_8',
        '#medication_dose_9': 'medication_dose_9',
        '#medication_freq_0': 'medication_freq_0',
        '#medication_freq_1': 'medication_freq_1',
        '#medication_freq_2': 'medication_freq_2',
        '#medication_freq_3': 'medication_freq_3',
        '#medication_freq_4': 'medication_freq_4',
        '#medication_freq_5': 'medication_freq_5',
        '#medication_freq_6': 'medication_freq_6',
        '#medication_freq_7': 'medication_freq_7',
        '#medication_freq_8': 'medication_freq_8',
        '#medication_freq_9': 'medication_freq_9',
        '#ins_planid_dental': 'ins_planid_dental',
        '#ins_provider_dental': 'ins_provider_dental',
        '#ins_street_addr_dental': 'ins_street_addr_dental',
        '#ins_city_dental': 'ins_city_dental',
        '#ins_state_dental': 'ins_state_dental',
        '#ins_zipcode_dental': 'ins_zipcode_dental',
        '#ins_phone_dental': 'ins_phone_dental',
        '#ins_email_dental': 'ins_email_dental',
        '#ins_planid_med': 'ins_planid_med',
        '#ins_provider_med': 'ins_provider_med',
        '#ins_street_addr_med': 'ins_street_addr_med',
        '#ins_city_med': 'ins_city_med',
        '#ins_state_med': 'ins_state_med',
        '#ins_zipcode_med': 'ins_zipcode_med',
        '#ins_phone_med': 'ins_phone_med',
        '#ins_email_med': 'ins_email_med',
        '#dentist_name': 'dentist_name',
        '#dentist_phone': 'dentist_phone',
        '#dentist_email': 'dentist_email',
        '#dental_condition': 'dental_condition',
        '#updated_on': 'updated_on'
    }

    attr_values = {
        ':email': data['email'],
        ':password': data['password'],
        ':first_name': data['first_name'],
        ':last_name': data['last_name'],
        ':middle_initial': data['middle_initial'],
        ':home_phone': data['home_phone'],
        ':mobile_phone': data['mobile_phone'],
        ':street_address': data['street_address'],
        ':street_address_2': data['street_address_2'],
        ':city': data['city'],
        ':state': data['state'],
        ':zipcode': data['zipcode'],
        ':dob': data['dob'],
        ':height': data['height'],
        ':weight': data['weight'],
        ':heart_rate': data['heart_rate'],
        ':active': data['active'],
        ':status': data['status'],
        ':gender': data['gender'],
        ':patient_preferences': data['patient_preferences'],
        ':patient_consents': data['patient_consents'],
        ':family_history': data['family_history'],
        ':allergies': data['allergies'],
        ':referrals': data['referrals'],
        ':lab_results': data['lab_results'],
        ':care_plan': data['care_plan'],
        ':lifestyle_history': data['lifestyle_history'],
        ':social_history': data['social_history'],
        ':bmi': data['bmi'],
        ':blood_type': data['blood_type'],
        ':current_problems_0': data['current_problems_0'],
        ':current_problems_1': data['current_problems_1'],
        ':current_problems_2': data['current_problems_2'],
        ':current_problems_3': data['current_problems_3'],
        ':current_problems_4': data['current_problems_4'],
        ':current_problems_5': data['current_problems_5'],
        ':current_problems_6': data['current_problems_6'],
        ':current_problems_7': data['current_problems_7'],
        ':current_problems_8': data['current_problems_8'],
        ':current_problems_9': data['current_problems_9'],
        ':medication_name_0': data['medication_name_0'],
        ':medication_name_1': data['medication_name_1'],
        ':medication_name_2': data['medication_name_2'],
        ':medication_name_3': data['medication_name_3'],
        ':medication_name_4': data['medication_name_4'],
        ':medication_name_5': data['medication_name_5'],
        ':medication_name_6': data['medication_name_6'],
        ':medication_name_7': data['medication_name_7'],
        ':medication_name_8': data['medication_name_8'],
        ':medication_name_9': data['medication_name_9'],
        ':medication_dose_0': data['medication_dose_0'],
        ':medication_dose_1': data['medication_dose_1'],
        ':medication_dose_2': data['medication_dose_2'],
        ':medication_dose_3': data['medication_dose_3'],
        ':medication_dose_4': data['medication_dose_4'],
        ':medication_dose_5': data['medication_dose_5'],
        ':medication_dose_6': data['medication_dose_6'],
        ':medication_dose_7': data['medication_dose_7'],
        ':medication_dose_8': data['medication_dose_8'],
        ':medication_dose_9': data['medication_dose_9'],
        ':medication_freq_0': data['medication_freq_0'],
        ':medication_freq_1': data['medication_freq_1'],
        ':medication_freq_2': data['medication_freq_2'],
        ':medication_freq_3': data['medication_freq_3'],
        ':medication_freq_4': data['medication_freq_4'],
        ':medication_freq_5': data['medication_freq_5'],
        ':medication_freq_6': data['medication_freq_6'],
        ':medication_freq_7': data['medication_freq_7'],
        ':medication_freq_8': data['medication_freq_8'],
        ':medication_freq_9': data['medication_freq_9'],
        ':ins_planid_dental': data['ins_planid_dental'],
        ':ins_provider_dental': data['ins_provider_dental'],
        ':ins_street_addr_dental': data['ins_street_addr_dental'],
        ':ins_city_dental': data['ins_city_dental'],
        ':ins_state_dental': data['ins_state_dental'],
        ':ins_zipcode_dental': data['ins_zipcode_dental'],
        ':ins_phone_dental': data['ins_phone_dental'],
        ':ins_email_dental': data['ins_email_dental'],
        ':ins_planid_med': data['ins_planid_med'],
        ':ins_provider_med': data['ins_provider_med'],
        ':ins_street_addr_med': data['ins_street_addr_med'],
        ':ins_city_med': data['ins_city_med'],
        ':ins_state_med': data['ins_state_med'],
        ':ins_zipcode_med': data['ins_zipcode_med'],
        ':ins_phone_med': data['ins_phone_med'],
        ':ins_email_med': data['ins_email_med'],
        ':blood_pressure_systolic': data['blood_pressure_systolic'],
        ':blood_pressure_diastolic': data['blood_pressure_diastolic'],
        ':dentist_name': data['dentist_name'],
        ':dentist_email': data['dentist_email'],
        ':dentist_phone': data['dentist_phone'],
        ':dental_condition': data['dental_condition'],
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
                         '#name.#middle_initial= :middle_initial, '
                         '#home_address.#street_address= :street_address, '
                         '#home_address.#street_address_2= :street_address_2, '
                         '#home_address.#city= :city, '
                         '#home_address.#state= :state, '
                         '#home_address.#zipcode= :zipcode, '
                         '#phone.#home= :home_phone, '
                         '#phone.#mobile= :mobile_phone, '
                         '#email= :email, '
                         '#dob= :dob, '
                         '#height= :height, '
                         '#weight= :weight, '
                         '#heart_rate= :heart_rate, '
                         '#blood_type= :blood_type, '
                         '#active= :active, '
                         '#status= :status, '
                         '#gender= :gender, '
                         '#patient_consents= :patient_consents, '
                         '#patient_preferences= :patient_preferences, '
                         '#family_history= :family_history, '
                         '#allergies= :allergies, '
                         '#referrals= :referrals, '
                         '#lab_results= :lab_results, '
                         '#care_plan= :care_plan, '
                         '#lifestyle_history= :lifestyle_history, '
                         '#social_history= :social_history, '
                         '#bmi= :bmi, '
                         '#current_problems_0= :current_problems_0, '
                         '#current_problems_1= :current_problems_1, '
                         '#current_problems_2= :current_problems_2, '
                         '#current_problems_3= :current_problems_3, '
                         '#current_problems_4= :current_problems_4, '
                         '#current_problems_5= :current_problems_5, '
                         '#current_problems_6= :current_problems_6, '
                         '#current_problems_7= :current_problems_7, '
                         '#current_problems_8= :current_problems_8, '
                         '#current_problems_9= :current_problems_9, '
                         '#medication_name_0= :medication_name_0, '
                         '#medication_name_1= :medication_name_1, '
                         '#medication_name_2= :medication_name_2, '
                         '#medication_name_3= :medication_name_3, '
                         '#medication_name_4= :medication_name_4, '
                         '#medication_name_5= :medication_name_5, '
                         '#medication_name_6= :medication_name_6, '
                         '#medication_name_7= :medication_name_7, '
                         '#medication_name_8= :medication_name_8, '
                         '#medication_name_9= :medication_name_9, '
                         '#medication_dose_0= :medication_dose_0, '
                         '#medication_dose_1= :medication_dose_1, '
                         '#medication_dose_2= :medication_dose_2, '
                         '#medication_dose_3= :medication_dose_3, '
                         '#medication_dose_4= :medication_dose_4, '
                         '#medication_dose_5= :medication_dose_5, '
                         '#medication_dose_6= :medication_dose_6, '
                         '#medication_dose_7= :medication_dose_7, '
                         '#medication_dose_8= :medication_dose_8, '
                         '#medication_dose_9= :medication_dose_9, '
                         '#medication_freq_0= :medication_freq_0, '
                         '#medication_freq_1= :medication_freq_1, '
                         '#medication_freq_2= :medication_freq_2, '
                         '#medication_freq_3= :medication_freq_3, '
                         '#medication_freq_4= :medication_freq_4, '
                         '#medication_freq_5= :medication_freq_5, '
                         '#medication_freq_6= :medication_freq_6, '
                         '#medication_freq_7= :medication_freq_7, '
                         '#medication_freq_8= :medication_freq_8, '
                         '#medication_freq_9= :medication_freq_9, '
                         '#blood_pressure_systolic= :blood_pressure_systolic, '
                         '#blood_pressure_diastolic= :blood_pressure_diastolic, '
                         '#dental_condition= :dental_condition, '
                         '#dentist_name= :dentist_name, '
                         '#dentist_email= :dentist_email, '
                         '#dentist_phone= :dentist_phone, '
                         '#ins_planid_dental= :ins_planid_dental, '
                         '#ins_provider_dental= :ins_provider_dental, '
                         '#ins_street_addr_dental= :ins_street_addr_dental, '
                         '#ins_city_dental= :ins_city_dental, '
                         '#ins_state_dental= :ins_state_dental, '
                         '#ins_zipcode_dental= :ins_zipcode_dental, '
                         '#ins_phone_dental= :ins_phone_dental, '
                         '#ins_email_dental= :ins_email_dental, '
                         '#ins_planid_med= :ins_planid_med, '
                         '#ins_provider_med= :ins_provider_med, '
                         '#ins_street_addr_med= :ins_street_addr_med, '
                         '#ins_city_med= :ins_city_med, '
                         '#ins_state_med= :ins_state_med, '
                         '#ins_zipcode_med= :ins_zipcode_med, '
                         '#ins_phone_med= :ins_phone_med, '
                         '#ins_email_med= :ins_email_med, '
                         '#updated_on= :updated_on ',
        ReturnValues='ALL_NEW',
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({"message":"Success", "id":event['pathParameters']['id']})
    }
    return response

if __name__ == '__main__':
    ## Configure boto for local environment
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'

    response = {
        "pathParameters": {
            "id": "5da5294a-36d7-11e8-8eae-2687762a2f75"
        },
        "body": json.dumps({
		"first_name": "Bryan",
		"last_name": "Richard",
        "middle_initial": "J",
		"email": "bryan@furnaceai.com",
		"password": "",
        "home_phone": "",
        "mobile_phone": "8019539821",
		"street_address": "3356 S 1100 E",
        "street_address_2": "",
        "city": "St. George",
        "state": "UT",
        "zipcode": "84106",
        "dob": "10/17/1972",
        "gender": 'Male',
        "blood_pressure_systolic": '120',
        "blood_pressure_diastolic": '80',
        "height": '70',
        "heart_rate": '64',
        "active": 'Yes',
        "status": 'Awaiting HIPAA Consent',
        "weight": '164'
	})
    }
    # testing_data = json.dumps({'body':})
    data = json.loads(json.dumps(response))
    print(update(data, ''))
