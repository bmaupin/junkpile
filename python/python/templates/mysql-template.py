#!/usr/bin/env python

'''
 Copyright (C) 2011 bmaupin <bmaupin@users.noreply.github.com>
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


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
    
    current_user = getpass.getuser()
    if current_user == 'root':
        sys.exit('Do not run this script as root.  Change users and try '
                 'again.')
    print 'Connecting to %s on %s as %s' % (mysql_db, mysql_host, current_user)
    mysql_passwd = getpass.getpass('Please enter your MySQL password: ') 
    
    # connect to database
    db = MySQLdb.connect(host=mysql_host, user=current_user, 
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