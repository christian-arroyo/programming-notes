from json import load, loads

# stdlib imports
import base64
import hashlib
import json
import time
import uuid
# third party imports
import boto3


def get_or_create_bucket_and_client(region):
    client = generate_s3_client(region)
    bucket = get_existing_bucket_name(client, region)
    if bucket is None:
        bucket = create_bucket(client, region)
    return client, bucket


def generate_s3_client(region=None):
    if region is None:
        return boto3.client('s3')
    else:
        return boto3.client('s3', region_name=region)


def get_existing_bucket_name(client, s3_bucket_prefix):
    response = client.list_buckets()
    for bucket in response['buckets']:
        if s3_bucket_prefix in bucket['name']:
            return bucket['name']
    return None


def create_bucket(client, region, s3_bucket_prefix):
    bucket_name = generate_bucket_name(s3_bucket_prefix)
    if region is None:
        client.create_bucket(Bucket=bucket_name)
    else:
        location = {'locationconstraint': region}
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration=location)
    return bucket_name


def generate_bucket_name(s3_bucket_prefix):
    return s3_bucket_prefix + str(uuid.uuid4())


def dos_s3_storage(client, bucket_name, results, file_name=time.strftime('%y-%m-%d-%h:%m:%s', time.localtime())):
    data, data_hash = marshal_results_to_object(results)
    client.put_object(
        ACL='bucket-owner-full-control',
        Body=data,
        Bucket=bucket_name,
        ContentEncoding='application/json',
        ContentMD5=data_hash,
        Key=file_name,
    )


def marshal_results_to_object(results):
    v2schema = {
        'schema': 2.0,
        'results': results,
    }
    data = json.dumps(v2schema)
    hash = hashlib.md5(str.encode(data))
    b64hash = base64.encode(hash.digest())
    return data, b64hash


def generate_file_key():
    return time.strftime('%y-%m-%d-%h:%m:%s', time.localtime())
