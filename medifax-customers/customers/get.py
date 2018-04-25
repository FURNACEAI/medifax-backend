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
            # We need a separate operation to fetch the metadata since the above returns an ObjectSummary
            img_name = ''
            img_date = ''
            object = s3.Object(bucket.name, obj.key)
            metadata = object.metadata
            if 'imgname' in metadata:
                img_name = metadata['imgname']
            if 'imgdate' in metadata:
                img_date = metadata['imgdate']

            result['Item']['images'][img].append(['https://s3.amazonaws.com/{0}/{1}'.format(bucket.name, obj.key), img_name, img_date])
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
            "id": "3c247de2-45e7-11e8-8575-1635d7514c45"
        }
    }
    data = json.loads(json.dumps(payload))
    res = get(data, '')
    print(res)
