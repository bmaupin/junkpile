Merge KML files based on this post: http://www.gps-data-team.com/pda-gps-navigation/topic/318.html#20729

**Requirements:**
- Python 3
- python-lxml

        sudo apt-get -y install python-lxml

**To run:**

    python3 merge-kml-files.py file1.kml file2.kml ... > output.kml
    
Ex:

    python3 merge-kml-files.py 11-01-2014\ 15-22.kml 11-01-2014\ 18-56.kml 12-01-2014\ 8-54.kml 12-01-2014\ 9-21.kml > mytrip.kml
