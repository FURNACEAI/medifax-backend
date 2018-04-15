import os
import json
from libs import decimalencoder
import boto3
from boto3.dynamodb.conditions import Key

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

if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    payload = {
        "pathParameters": {
            "id": "dba29cee-23d4-11e8-bd8a-acbc3294be4b"
        }
    }
    data = json.loads(json.dumps(payload))
    res = get(data, '')
    print(res)
