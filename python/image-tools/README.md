⚠ It's probably better to use exiftool when possible: https://bmaupin.github.io/wiki/applications/multimedia/organizing-files.html


- remove-all-exif-data.py
  - Remove all EXIF data from a jpeg image file
  - Prerequisites:
    - piexif
    
            sudo apt-get -y install python3-pip
            sudo pip3 install piexif
  - To run on one file:
  
          python3 remove-all-exif-data.py /path/to/file.jpg
  - To run on a folder and its subfolders:
  
          for file in /path/to/files/*.@([jJ][pP]*([eE])[gG]); do echo $file; python3 remove-all-exif-data.py "$file"; done
    
- set-exif-timestamp.py
  - Set the EXIF timestamps of a jpeg image file
  - Prerequisites:
    - piexif
    
            sudo apt-get -y install python3-pip
            sudo pip3 install piexif
  - To run on one file:
  
          python3 set-exif-timestamp.py /path/to/file.jpg
  - To run on a folder and its subfolders:
  
          for file in /path/to/files/*.@([jJ][pP]*([eE])[gG]); do echo $file; python3 set-exif-timestamp.py "$file"; done
