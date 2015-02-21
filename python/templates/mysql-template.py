#!/usr/bin/env python

import getpass
import sys

import MySQLdb
import MySQLdb.cursors


# change these as necessary
mysql_db = 'mydb'
mysql_host = 'mydbhost'


def main():
    cursor = db_connect()
    
    try:
        cursor.execute('SHOW TABLES')
        
        # get the result set as a dictionary
        result = cursor.fetchall()
        
    except MySQLdb.Error, error:  # if there's an error
        sys.exit('MySQLdb Error: %s' % (error))

    if result:
        for record in result:
            for field_name in record:
                field_content = record[field_name]
                print '%s: %s' % (field_name, field_content)
    
    cursor.close()
        

def db_connect():
    '''Purpose: connects to the database
    Requires: globally defined database, host
    Returns: database cursor
    '''
   
    username = raw_input('Please enter your MySQL username (or press enter to '
                         'use %s): ' % (getpass.getuser()))
    if username == '':
        username = getpass.getuser()
 
    print 'Connecting to %s on %s as %s' % (mysql_db, mysql_host, username)
    mysql_passwd = getpass.getpass('Please enter your MySQL password: ') 
    
    # connect to database
    db = MySQLdb.connect(host=mysql_host, user=username, 
            passwd=mysql_passwd, db=mysql_db, charset='utf8', use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor) # charset = 'utf8' implies use_unicode = True, but we'll write it anyway 
    # create a cursor
    cursor = db.cursor()
    
    return cursor


# calls the main() function when the script runs
if __name__ == '__main__':
    main()

'''
TODO:
-create some kind of wrapper so every time a MySQL query is done we don't have 
to worry about catching exceptions, returning results, etc.
    might as well have it close the cursor while we're at it
'''
