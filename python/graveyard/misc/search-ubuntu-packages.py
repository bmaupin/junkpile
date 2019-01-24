#!/usr/bin/env python

import gzip
import os
import os.path

def main():
    distro_to_search = 'trusty'
    package_lists_path = os.path.join(os.getenv('HOME'), 'Desktop/lists')
    
    packages = {}
    
    for filename in os.listdir(package_lists_path):
        # don't search package list files from other distros
        if filename.find(distro_to_search) == -1:
            continue
        if filename.endswith('gz'):
            package_file = gzip.open(os.path.join(package_lists_path, filename))
        else:
            package_file = open(os.path.join(package_lists_path))
        
        for line in package_file:
            if line.startswith('Package'):
                package = line.split()[1]
                if package not in packages:
                    packages[package] = '' 
                else:
                    continue
            elif line.startswith('Version'):
                if packages[package] == '':
                    packages[package] = line.split()[1]
    
    # get the longest package name
    longest_name = 0
    for package in packages:
        if len(package) > longest_name:
            longest_name = len(package)
    
    for package in packages:
        print('{0:{1}} {2}'.format(
            package + ':',
            longest_name + 1,
            packages[package]
        )
    )


if __name__ == '__main__':
    main()