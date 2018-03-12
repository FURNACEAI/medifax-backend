# Local invoke workaround
if __name__ == '__main__':
    import sys
    sys.path.append("/Users/bryan/Work/FURNACE/Projects/Medifax/src/medifax-lambda/medifax-customers")

import json
import os
from libs import decimalencoder
import boto3

def list(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all todos from the database
    result = table.scan()
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response

if __name__ == '__main__':
    ## Configure boto for local environment
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    print(list('', ''))
