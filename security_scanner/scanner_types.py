from json import load, loads
from enum import Enum, auto
from os import walk
from requests import get
from time import sleep


class ScannerTypes(Enum):
    AGENT_PULL = auto()
    NFS_READ = auto()


def scan_agent_pull(ip_list: list, max_agent_pull_retries=10) -> dict:
    results = dict()
    for ip_address in ip_list:
        response = get(f"https://{ip_address}/portdiscovery' % ip)")
        if response.status_code != 200:
            raise Exception(f"non-200 status code: {response.status_code}")
        data = loads(response.text)
        agent_url = f"{data['agenturl']}/api/2.0/status"
        response = get(agent_url)
        retries = 0
        while response.status_code == 503:
            if retries > max_agent_pull_retries:
                raise Exception(f"max retries exceeded for ip {ip_address}")
            retries += 1
            time_to_wait = float(response.headers['retry-after'])
            sleep(time_to_wait)
            response = get(agent_url)
        if response.status_code != 200:
            raise Exception(f"non-200 status code: {response.status_code}")
        results[ip_address] = data['status']
    return results


def scan_nfs_read(ip_list: list, nfs_read_dir: str) -> dict:
    results = dict()
    for ip in ip_list:
        agent_nfs_path = '%s/%s' % (nfs_read_dir, ip)
        for dir_name, subdir_list, file_list in walk(agent_nfs_path):
            for file in file_list:
                with open(file) as fd:
                    data = load(fd)
                if 'schema' not in data or float(data['schema']) < 2.0:
                    result = data
                else:
                    result = data['status']
                results[ip] = result
    return results
