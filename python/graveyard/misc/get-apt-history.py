#!/usr/bin/env python

import gzip
import os
import os.path

def main():
apt_log_path = '/var/log/apt'
dirlist = os.listdir(apt_log_path)
# somehow this dict will magically order all the numerical keys
history_files = {}
for filename in dirlist:
    if filename.startswith('history.log'):
        if filename[len('history.log') + 1:-3] == '':
            file_number = 0
        else:
            file_number = int(filename[len('history.log') + 1:-3])
        history_files[file_number] = filename

installed = []
removed = []

# go through the list of history files in reverse order
for index in history_files:
    filename = history_files[len(history_files) - index - 1]
    
    if filename.endswith('gz'):
        history_file = gzip.open(os.path.join(apt_log_path, filename))
    else:
        history_file = open(os.path.join(apt_log_path, filename))
        
    for line in history_file:
        if line.startswith('Commandline'):
            command_words = line.split()[2:]
            if command_words[0].startswith('-'):
                del command_words[0]
            
            if command_words[0] == 'install':
                for package in command_words[1:]:
                    if package.startswith('-'):
                        continue
                    if package not in installed:
                        installed.append(package)
                    if package in removed:
                        removed.remove(package)
                    
            elif (command_words[0] == 'remove' or 
                command_words[0] == 'autoremove'):
                for package in command_words[1:]:
                    if package.startswith('-'):
                        continue
                    if package not in removed:
                        removed.append(package)
                    if package in installed:
                        installed.remove(package)
                    
                
                
            
            '''
                commands.append(line.split()[2])
                
            if command_words[0] not in commands:
                commands.append(command_words[0])
            
            for command_word in command_words:
                if command_word.startswith('-'):
                    continue
            
            
            if line.split()[2] == 'install':
            elif line.split()[2] == 'remove' or line.split()[2] == 'autoremove':
                commands.append(line.split()[2])
            '''
        

'''
Commandline: apt-get install gnote
Commandline: apt-get remove footnote
'''


if __name__ == '__main__':
    main()