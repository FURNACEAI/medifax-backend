from __future__ import print_function
import traceback
import os
import json
import boto3


def onetimes3url(event, context):
    """ Generates a one-time upload URL. """
    data = json.loads(event['body'])
    print(data)
    # print(event)
    # print(data)
    key = data['s3key']
    # key = "c85cf638-3aa0-11e8-8bb4-5e566f9ab6c7/aljdfljdjfjdllf.jpg"
    url = "n/a"
    try:
        s3_con = boto3.client('s3')
        url = s3_con.generate_presigned_url(
            'put_object', Params={
                'Bucket':'medifax-images',
                'Key':key
            },
            HttpMethod='PUT'
        )
    except Exception as e:
        print(traceback.format_exc())

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Success", "s3url": url})
    }

    return response

""" Local test script """
if __name__ == '__main__':
    boto3.setup_default_session(profile_name='serverless')
    payload = {
        "body": json.dumps({
            "s3key": "c85cf638-3aa0-11e8-8bb4-5e566f9ab6c7/aljdfljdjfjdllf.jpg",
        })
    }
    data = json.loads(json.dumps(payload))
    # print(data)
    res = onetimes3url(data, '')
    print(res)
