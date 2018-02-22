import os
import json
import time

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    try:
        result = table.get_item(
            Key={
                'id': event['pathParameters']['id']
            }
        )
    #except boto3.dynamodb.exceptions.DynamoDBKeyNotFoundError:
    #    response = {
    #        "statusCode": 200,
    #        "body": json.dumps(event,
    #                           cls=decimalencoder.DecimalEncoder)
    #    }
    except ClientError as e:
        response = {
            "statusCode": 200,
            "body": json.dumps(event,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
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
        "body":{json.dumps({"message": "Success"}}
    }

    return response

def update(event, context):
    data = json.loads(event['body'])
    #if 'text' not in data or 'checked' not in data:
    #    logging.error("Validation Failed")
    #    raise Exception("Couldn't update the todo item.")
    #    return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#todo_text': 'text',
        },
        ExpressionAttributeValues={
          ':text': data['text'],
          ':user_role': data['checked'],
          ':updated_on': timestamp,
        },
        UpdateExpression='SET #todo_text = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Success"})
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

