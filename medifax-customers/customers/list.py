# Local invoke workaround
if __name__ == '__main__':
    import sys
    sys.path.append("/Users/bryan/Work/FURNACE/Projects/Medifax/src/medifax-lambda/medifax-customers")

import json
import os
import decimal
# import decimalencoder
import boto3

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

def list(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all todos from the database
    result = table.scan()
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }

    return response

if __name__ == '__main__':
    ## Configure boto for local environment
    boto3.setup_default_session(profile_name='serverless')
    os.environ["DYNAMODB_TABLE"] = 'medifax-backend-customers-dev'
    print(list('', ''))
