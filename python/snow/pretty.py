#!/usr/bin/env python

# stdlib imports
import base64
import hashlib
import json
import os
import time
import uuid
# third party imports
import boto3
import requests


class InputTypes:
    def __init__(self, input_type: str, ip_lists_file: str):
        self.input_type = input_type
        self.ip_lists_file = ip_lists_file
        self.data = []

    def validate_input(self, input_type: str, ip_lists_file: str) -> None:
        """Executes validation depending on input type, it allows addition of validation types easily
        :param ip_lists_file: list of IP addresses
        :param input_type: Input type such as nfs, api, etc
        """
        if input_type == "nfs":
            self.validate_input_nfs(ip_lists_file)
        if input_type == "api":
            self.validate_input_api()
        else:
            raise Exception('unrecognized input_type "%s"' % input_type)

    def validate_input_api(self) -> None:
        response = requests.get('https://api/iplist')
        if response.status_code != 200:
            raise Exception('non-200 status code: %d' % response.status_code)
        self.data = json.loads(response.text)
        ip_list = self.data['iplist']
        page_counter = 0
        while self.data['more'] is True:
            page_counter += 1
            response = requests.get(
                'https://api/iplist?page=%d' %
                page_counter)
            if response.status_code != 200:
                raise Exception(
                    'non-200 status code: %d' %
                    response.status_code)
            self.data = json.loads(response.text)
            ip_list.extend(self.data['iplist'])
            # if input is not valid, raise exception
            self.validate_ip_list(ip_list)

    def validate_input_nfs(self, ip_lists_file) -> None:
        """
        Function to validate NFS input in IP lists file
        :param ip_lists_file:
        """
        ip_list = []
        with open(ip_lists_file) as fd:
            path_to_ip_lists = fd.read()

        for dir_name, subdir_list, file_list in os.walk(path_to_ip_lists):
            for file in file_list:
                with open(file) as fd:
                    data = json.load(fd)
                ip_list.extend(data['iplist'])
                for ip in ip_list:
                    self.validate_ip_address(ip)

    def validate_ip_list(self, ip_list):
        for ip in ip_list:
            if not self.validate_ip_address(ip):
                return False
        return True

    @staticmethod
    def validate_ip_address(ip_address: str) -> bool:
        """
        Function to validate if string is in IPv4 format

        :param ip_address:
        :return: True if IP address is a valid IPv4 format, False otherwise
        """
        if not isinstance(ip_address, str):
            return False
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for num_s in parts:
            try:
                num = int(num_s)
            except ValueError:
                return False
            if num < 0 or num > 255:
                return False
        return True


class Scanner:
    def __init__(self, scan_type: str, ip_list: list,
                 max_agent_pull_retries: int) -> None:
        self.scan_type = scan_type
        self.ip_list = ip_list
        self.results = []

    def scan_agent_pull(self, max_agent_pull_retries=10):
        for ip in self.ip_list:
            response = requests.get('https://%s/portdiscovery' % ip)
            if response.status_code != 200:
                raise Exception(
                    'non-200 status code: %d' %
                    response.status_code)
            data = json.loads(response.text)
            agent_url = '%s/api/2.0/status' % data['agenturl']
            response = requests.get(agent_url)
            retries = 0
            while response.status_code == 503:
                if retries > max_agent_pull_retries:
                    raise Exception('max retries exceeded for ip %s' % ip)
                retries += 1
                time_to_wait = float(response.headers['retry-after'])
                time.sleep(time_to_wait)
                response = requests.get(agent_url)
            if response.status_code != 200:
                raise Exception(
                    'non-200 status code: %d' %
                    response.status_code)
            self.results[ip] = data['status']

    def scan_nfs_read(self, nfs_read_dir):
        results = dict()
        for ip in self.ip_list:
            agent_nfs_path = '%s/%s' % (nfs_read_dir, ip)
            for dir_name, subdir_list, file_list in os.walk(agent_nfs_path):
                for file in file_list:
                    with open(file) as fd:
                        data = json.load(fd)
                    if 'schema' not in data or float(data['schema']) < 2.0:
                        result = data
                    else:
                        result = data['status']
                    results[ip] = result


class Storage:
    def __init__(self, storage_type: str, s3_region, s3_bucket_prefix: str, nfs_write_dir: str):
        self.storage_type = storage_type
        self.s3_region = s3_region
        self.s3_bucket_prefix = s3_bucket_prefix
        self.nfs_write_dir = nfs_write_dir
        self.results = []

    def store_in_s3(self):
        self.storeResultsInS3(self.results, self.s3_region)

    def store_nfs_write(self, nfs_write_dir):
        file_name = time.strftime('%y-%m-%d-%h:%m:%s', time.localtime())
        file_full_path = '/'.join([nfs_write_dir, file_name]) + '.json'
        v2schema = {
            'schema': 2.0,
            'results': self.results,
        }
        data = json.dumps(v2schema)
        with open(file_full_path, 'w') as fd:
            fd.write(data)

    def get_existing_bucket_name(self, client, s3_bucket_prefix):
        response = client.list_buckets()
        for bucket in response['buckets']:
            if s3_bucket_prefix in bucket['name']:
                return bucket['name']
        return None

    def createBucket(self, client, region):
        bucket_name = self.genBucketName()
        if region is None:
            client.create_bucket(Bucket=bucket_name)
        else:
            location = {'locationconstraint': region}
            client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location)
        return bucket_name

    def genBucketName(self, s3_bucket_prefix):
        return s3_bucket_prefix + str(uuid.uuid4())

    def storeResultsInS3(self, results, region):
        client, bucketname = self.getorcreatebucketandclient(region)
        self.dosS3Storage(client, bucketname, results)

    def getorcreatebucketandclient(self, region):
        client = self.genS3client(region)
        bucket = self.get_existing_bucket_name(client)
        if bucket is None:
            bucket = self.createBucket(client)
        return client, bucket

    def dosS3Storage(self, client, bucket_name, results, file_name):
        data, data_hash = marshal_results_to_bject(results)
        client.put_object(
            ACL='bucket-owner-full-control',
            Body=data,
            Bucket=bucket_name,
            ContentEncoding='application/json',
            ContentMD5=data_hash,
            Key=file_name,
        )

    def genS3client(self, region=None):
        if region is None:
            return boto3.client('s3')
        else:
            return boto3.client('s3', region_name=region)


def marshal_results_to_bject(results):
    v2schema = {
        'schema': 2.0,
        'results': results,
    }
    data = json.dumps(v2schema)
    hash = hashlib.md5(str.encode(data))
    b64hash = base64.encode(hash.digest())
    return data, b64hash


def genFileKey():
    return time.strftime('%y-%m-%d-%h:%m:%s', time.localtime())


def main():
    i = InputTypes("nfs")
    i.validate_input_nfs("path-to-ip-lists.txt")
    scanner = Scanner('agent-pull', [], 10)
    nfs_read_dir = '/nfs/agent-output'
    scanner.scan_nfs_read(nfs_read_dir)

    storage_type = 's3'
    s3_region = 'eu-west-1'
    s3_bucket_prefix = 'ip-scanner-results'
    nfs_write_dir = '/nfs/ip-scanner-results'
    storage = Storage(storage_type, s3_region, s3_bucket_prefix, nfs_write_dir)
    storage.storeResultsInS3([], s3_region)


if __name__ == '__main__':
    main()
