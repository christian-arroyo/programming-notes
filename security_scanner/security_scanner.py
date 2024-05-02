#!/usr/bin/env python

from input_types import InputTypes
from input_types import get_ip_list_from_api, get_ip_list_from_nfs
from scanner_types import ScannerTypes
from scanner_types import scan_agent_pull, scan_nfs_read
from storage_types import store_in_s3, store_in_nfs_write
from storage_types import StorageTypes
from network_utils import is_valid_ipv4_list

"""
At first, I thought of creating classes for each input type, scanner type, and storage type, and maybe adding a layer
of abstraction. But I then figured out that I would be over-complicating readability and usability. Since the 
security scanner is more "Action" focused rather than "State" focused, having modules with functions make more
sense than having multiple classes.

I separated the functions into their specific modules, which will simplify addition of code, if new types need to be
added. I also created functions for each specific type, with their corresponding input parameters, so they can be 
easily testable. I also created a storage utilities and a network utilities files. These are modules that can be 
reused outside of the context of this application.

The security_scanner main class could be improved by adding a command line parser, such as argparse, that would allow
users to execute specific utilities. Commandline errors could be raised if there are incorrect inputs typed during
the execution of the argument parser.
"""

# TODO: Add docstrings to all functions with function description, parameters, and return values
# TODO: Commandline tool can be created in security scanner using argparse to handle different input, scanner, and storage types
# TODO: Exception handling could be improved in security scanner
# TODO: Raising of exceptions could be improved in utils functions
# TODO: Exception names should be more specific


def main(
    input_type=InputTypes.NFS,
    path='path-to-ip-lists.txt',
    api_endpoint="https://api/iplist",
    scan_type=ScannerTypes.AGENT_PULL,
    max_agent_pull_retries=10,
    nfs_read_dir='/nfs/agent-output',
    storage_type=StorageTypes.S3,
    s3_region='eu-west-1',
    s3_bucket_prefix='ip-scanner-results',
    nfs_write_dir='/nfs/ip-scanner-results',
):
    # Input type step
    if input_type == InputTypes.API:
        ip_list = get_ip_list_from_api(path)
    elif input_type == InputTypes.NFS:
        ip_list = get_ip_list_from_nfs(api_endpoint)
    else:
        raise Exception('unrecognized input_type "%s"' % input_type)

    if not is_valid_ipv4_list(ip_list):
        raise Exception("List of IP addresses is invalid")

    # Scanner type step
    if scan_type == ScannerTypes.AGENT_PULL:
        results = scan_agent_pull(ip_list, max_agent_pull_retries)
    elif scan_type == ScannerTypes.NFS_READ:
        results = scan_nfs_read(ip_list, nfs_read_dir)
    else:
        raise Exception('unrecognized scan_type %s' % scan_type)

    # Storage step
    if storage_type == StorageTypes.S3:
        store_in_s3(results, s3_region)
    if storage_type == StorageTypes.NFS_WRITE:
        store_in_nfs_write(results, nfs_write_dir)


if __name__ == '__main__':
    main()
