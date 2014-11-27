Wrapper script for [msgconvert.pl](http://www.matijs.net/software/msgconv/)

To install:

    sudo apt-get -y install libemail-localdelivery-perl libemail-outlook-message-perl libemail-sender-perl
    sudo wget http://www.matijs.net/software/msgconv/msgconvert.pl -O /usr/local/bin/msgconvert.pl
    sudo wget https://raw.githubusercontent.com/bmaupin/misc-python/master/fix-encoding/fix-cp1252-encoding.py -O /usr/local/bin/fix-cp1252-encoding.py
    sudo wget https://raw.githubusercontent.com/bmaupin/misc-shell/master/msgconvert/msgconvert -O /usr/local/bin/msgconvert
    sudo chmod +x /usr/local/bin/msgconvert
    
To use:

    msgconvert /path/to/email.msg
