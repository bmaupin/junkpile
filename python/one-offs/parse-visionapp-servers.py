#!/usr/bin/env python3

''' Parses hosts from Visionapp Remote Desktop export and outputs them in Ansible inventory format
'''

import lxml.etree
import socket
import re

INPUT_FILENAME = 'export.vre'
OUTPUT_FILENAME = 'inventory'

def main():
    connections, folders, parent_ids = parse_visionapp_xml()
    parent_names = get_parent_names(connections, folders, parent_ids)
    write_ansible_inventory(parent_names)


def parse_visionapp_xml():
    root = lxml.etree.parse(INPUT_FILENAME)

    connections = parse_connections(root)
    folders = parse_folders(root)
    parent_ids = parse_parent_ids(root)

    return connections, folders, parent_ids


def parse_connections(root):
    connections = {}

    for connection in root.find('Connections'):
        connections[connection.get('Id')] = connection.find('ServerName').text.lower().strip()

    return connections


def parse_folders(root):
    folders = {}

    for folder in root.find('Folders'):
        folder_name = re.sub('[^0-9a-zA-Z]+', '-', folder.find('Name').text.lower().strip())
        if folder_name[0] == '-':
            folder_name = folder_name[1:]
        if folder_name[-1] == '-':
            folder_name = folder_name[:-1]
        folders[folder.get('Id')] = folder_name

    return folders


def parse_parent_ids(root):
    parent_ids = {}

    for item in root.find('IndexTable'):
        if item.get('Type') == 'Connection':
            if item.get('ParentItemId') not in parent_ids:
                parent_ids[item.get('ParentItemId')] = []

            parent_ids[item.get('ParentItemId')].append(item.get('Id'))

    return parent_ids


def get_parent_names(connections, folders, parent_ids):
    parent_names = {}

    for folder_id in parent_ids.keys():
        if folder_id == '0':
            parent_name = ''
        else:
            parent_name = folders[folder_id]

        # Folders can have duplicate names; don't overwrite them
        if parent_name not in parent_names:
            parent_names[parent_name] = []

        for connection_id in parent_ids[folder_id]:
            # Don't add duplicate hostnames, just add them to the first group they're in
            if not is_in_parent_names(connections[connection_id], parent_names):
                parent_names[parent_name].append(connections[connection_id])

    return parent_names


def is_in_parent_names(connection_name, parent_names):
    for parent_name in parent_names:
        if connection_name in parent_names[parent_name]:
            return True

    return False


def write_ansible_inventory(parent_names):
    with open(OUTPUT_FILENAME, 'w') as output_file:
        for folder_name in sorted(parent_names.keys()):
            output_file.write('\n[{}]\n'.format(folder_name))

            for connection_name in sorted(parent_names[folder_name]):
                if connection_name != '':
                    if not connection_name.endswith('mcgill.ca'):
                        connection_name = socket.getfqdn(connection_name)

                    output_file.write('{}\n'.format(connection_name))


if __name__ == '__main__':
    main()
