"""
Provide an easy CLI interface for working with the Auth API - in case a web UI is
unavailable. This is unfinished, and just here to make things a bit easier...

It connects to the HTTP RESTful API, and not directly to the database.
"""

import argparse
import requests


def command_to_url_part(command, section, *args, **kwargs):
    """
    If we're looking to read, update, or delete, we need
    the next part of the URL...
    
    :param command:
    :param section:
    :return:
    """
    if command in {'list', 'create'}:
        return None
    return section[:-1]


def command_to_method(command):
    if command in {'list', 'read'}:
        return 'GET'
    elif command == 'update':
        return 'PUT'
    elif command == 'create':
        return 'POST'
    elif command == 'delete':
        return 'DELETE'


def main(username, password, url, section, command='list', object_id=None, *args, **kwargs):
    """
    
    :param url: The base URL for the API (https://auth.something.com/api)
    :param section: applications | groups | organizations | users
    :param command: create, read, update, delete, list
    :param object_id: The object to operate on
    :return:
    """
    
    url_parts = [url, section]
    command_part = command_to_url_part(command=command, section=section)
    if command_part:
        url_parts.append(command_part)
    if object_id:
        url_parts.append(object_id)
    
    method = command_to_method(command)
    
    response = requests.request(method, "/".join(url_parts), auth=(username, password))
    print(response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Auth CLI")
    parser.add_argument('-u', '--username', dest='username', help='Auth User')
    parser.add_argument('-p', '--password', dest='password', help='Auth Password')
    parser.add_argument('--url', dest='url', help='Auth API URL -- https://auth.domain.com/api')
    parser.add_argument('-s', '--section', dest='section', default='users', help='Section to show -- users, organizations, applications, groups')
    parser.add_argument('-o', '--object', dest='object_id', default=None, help='Object ID to view')
    parser.add_argument('-m', '--method', dest='method', default='list', help='Method - list, create, read, update, delete')
    options = parser.parse_args()
    main(
        options.username,
        options.password,
        options.url,
        options.section,
        options.method,
        options.object_id
    )
