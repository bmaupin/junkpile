- remove-all-exif-data.py
  - Remove all EXIF data from a jpeg image file
  - Prerequisites:
    - piexif
    
            sudo apt-get -y install python3-pip
            sudo pip3 install piexif
  - To run on one file:
  
          python3 remove-all-exif-data.py /path/to/file.jpg
  - To run on a folder and its subfolders:
  
          find /path/to/files -type f \( -iname *.jpg -o -iname *.jpeg \) -exec echo {} \; -exec python3 remove-all-exif-data.py {} \;
    
- set-exif-timestamp.py
  - Set the EXIF timestamps of a jpeg image file
  - Prerequisites:
    - piexif
    
            sudo apt-get -y install python3-pip
            sudo pip3 install piexif
  - To run on one file:
  
          python3 set-exif-timestamp.py /path/to/file.jpg
  - To run on a folder and its subfolders:
  
          find /path/to/files -type f \( -iname *.jpg -o -iname *.jpeg \) -exec echo {} \; -exec python3 set-exif-timestamp.py {} \;
