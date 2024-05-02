from enum import Enum, auto
from json import dumps
from time import localtime, strftime

from storage_utils import get_or_create_bucket_and_client, dos_s3_storage


class StorageTypes(Enum):
    NFS_WRITE = auto()
    S3 = auto()


def store_in_s3(data: dict, region: str) -> None:
    client, bucket_name = get_or_create_bucket_and_client(region)
    dos_s3_storage(client, bucket_name, data)


def store_in_nfs_write(data: dict, nfs_write_dir) -> None:
    file_name = strftime('%y-%m-%d-%h:%m:%s', localtime())
    file_full_path = '/'.join([nfs_write_dir, file_name]) + '.json'
    v2schema = {
        'schema': 2.0,
        'results': data,
    }
    data = dumps(v2schema)
    with open(file_full_path, 'w') as fd:
        fd.write(data)
