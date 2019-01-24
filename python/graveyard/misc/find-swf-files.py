import os
import os.path
import sys

def main():
    if len(sys.argv) < 2:
        sys.exit('ERROR: must provide path')

    if os.path.isdir(sys.argv[1]):
        for entry in sorted(os.listdir(sys.argv[1])):
            file_full_path = os.path.join(sys.argv[1], entry)
            if os.path.isfile(file_full_path):
                with open(file_full_path, 'rb') as infile:
                    if infile.read(3) == 'CWS':
                        print file_full_path
    

if __name__ == '__main__':
    main()
