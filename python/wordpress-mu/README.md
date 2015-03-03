**Prerequisites:**
- Python MySQLdb module
  - To install on Ubuntu/Debian:

            sudo apt-get -y install python-mysqldb

  - To install on RHEL/CentOS 6:
  
            sudo yum install -y MySQL-python
  
- [Python phpserialize module](https://pypi.python.org/pypi/phpserialize)
  - To install on Ubuntu/Debian:

            sudo apt-get -y install python-pip
            sudo pip install phpserialize
            
  - To install on RHEL/CentOS 6:

            sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
            sudo yum install -y python-pip
            sudo pip install phpserialize

**To run:**  
First configure constants in wpmu_constants.py.

Sample output:

    $ python wpmu_change_hostname.py 
    Please enter the MySQL user: wordpress
    Connecting to wordpress on localhost as wordpress
    Please enter the MySQL password: 
    Highest blog ID: 4066
    Number of blogs: 758
    
    Fixing site tables...
    wp_users:	155 record(s) modified
    wp_usermeta:	1837 record(s) modified
    wp_site:	1 record(s) modified
    wp_blogs:	758 record(s) modified
    wp_sitemeta:	1 record(s) modified
    
    Fixing blog-specific tables...
    wp_###_posts:	58072 record(s) modified
    wp_###_links:	370 record(s) modified
    wp_###_comments:	1181 record(s) modified
    wp_###_postmeta:	269 record(s) modified
    wp_###_options:	4357 record(s) modified
    
    Fixing blog-specific tables...
    wp_###_posts:	39 record(s) modified
    wp_###_links:	2 record(s) modified
    wp_###_comments:	0 record(s) modified
    wp_###_postmeta:	0 record(s) modified
    wp_###_options:	0 record(s) modified
