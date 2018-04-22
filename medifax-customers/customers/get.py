import os
import json
from libs import decimalencoder
import boto3
from boto3.dynamodb.conditions import Key
from boto.s3.connection import S3Connection


def get(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # Add a key for the images
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name="medifax-images")
    result['Item']['images'] = {}
    IMG_TYPES = ['medical', 'dental']

    # Fetch the two types of images and append them to the JSON response
    for img in IMG_TYPES:
        result['Item']['images'][img] = []
        # Fetch Medical Images
        prefix = "%s/%s/" % (event['pathParameters']['id'], img)
        FilesNotFound = True
        for obj in bucket.objects.filter(Prefix=prefix):
            result['Item']['images'][img].append('https://s3.amazonaws.com/{0}/{1}'.format(bucket.name, obj.key))
            FilesNotFound = False
        if FilesNotFound:
            pass
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
            "id": "c85cf638-3aa0-11e8-8bb4-5e566f9ab6c7"
        }
    }
    data = json.loads(json.dumps(payload))
    res = get(data, '')
    print(res)
