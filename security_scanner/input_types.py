#!/usr/bin/env python

from enum import Enum, auto
from json import load, loads
from os import walk
from requests import get


class InputTypes(Enum):
    API = auto()
    NFS = auto()


def get_ip_list_from_nfs(file_name: str) -> list:
    ip_list = []
    with open(file_name) as fd:
        path_to_ip_lists = fd.read()
    for dir_name, subdir_list, file_list in walk(path_to_ip_lists):
        for file in file_list:
            with open(file) as fd:
                data = load(fd)
            ip_list.extend(data['iplist'])
    return ip_list


def get_ip_list_from_api(api_endpoint: str) -> list:
    response = get(api_endpoint)
    if response.status_code != 200:
        raise Exception('non-200 status code: %d' % response.status_code)
    data = loads(response.text)
    ip_list = data['iplist']
    page_counter = 0
    while data['more'] is True:
        page_counter += 1
        response = get('https://api/iplist?page=%d' % page_counter)
        if response.status_code != 200:
            raise Exception('non-200 status code: %d' % response.status_code)
        data = loads(response.text)
        ip_list.extend(data['iplist'])
    return ip_list

