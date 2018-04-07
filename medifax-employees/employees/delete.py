import json
import os
import boto3
from boto3.dynamodb.conditions import Key

def delete(event, context):
    """
    Deletes a customer from the database
    """
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
