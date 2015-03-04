#!/usr/bin/env python
#
# Library of functions for managing Wordpress MU.
# Currently compatible with Wordpress MU 1.3.3.
#
# Requires: phpserialize from http://pypi.python.org/pypi/phpserialize,
#    modified to handle serialized PHP objects

import getpass
import posixpath
import sys

import MySQLdb
import phpserialize as php

from wpmu_constants import *


def db_connect():
    '''Purpose: connects to the database
    Requires: globally defined database, host
    Returns: database cursor
    '''
    
    mysql_user = raw_input('Please enter the MySQL user: ')
    print 'Connecting to %s on %s as %s' % (mysql_db, mysql_host, mysql_user) 
    mysql_passwd = getpass.getpass('Please enter the MySQL password: ') 

    # connect to database
    db = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, 
            db=mysql_db, charset = 'utf8', use_unicode = True) # charset = 'utf8' implies use_unicode = True, but we'll write it anyway 
    # create a cursor
    cursor = db.cursor()
    
    return cursor


def get_blog_ids():
    '''Purpose: creates a list of all blog IDs from table wp_blogs
    Requires: database cursor
    Returns: list of blog IDs
    '''
    
    blog_ids = []
    try:
        cursor.execute('SELECT blog_id FROM wp_blogs')
        
        # get the resultset as a tuple
        result = cursor.fetchall()
        
        for top_element in result:  # parse through the list containing lists of results of records
            for element in top_element:  # parse through list for each record
                blog_ids.append(element)

    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit( 1 )
    
    return blog_ids


def get_blog_logins():
    '''Purpose: Get user logins from Wordpress database
    Returns: a dictionary containing the blog user login and email where the 
    key is the uid number 
    '''
    blog_logins = {}
    try:
        cursor.execute("SELECT ID, user_login, user_email from wp_users")
        result = cursor.fetchall()
        
        for record in result:
            blog_uid_number = record[0]
            blog_login = record[1]
            blog_email = record[2]
            
            blog_logins[blog_uid_number] = {}
            blog_logins[blog_uid_number]['blog_login'] = blog_login
            blog_logins[blog_uid_number]['blog_email'] = blog_email
    
    except MySQLdb.Error, error:  # if there's an error
        # print the error and exit the script
        sys.exit('ERROR:\t%s\n' % (error))
    
    return blog_logins


def get_blog_paths():
    '''Purpose: gets all the blog paths and puts them in a dictionary where
            the key is the blog ID and the value is the blog path
    Requires: nothing
    Returns: dictionary containing blog paths
    '''
    
    blog_paths = {}
    try:
        cursor.execute('SELECT blog_id, path FROM wp_blogs')
        result = cursor.fetchall()
        
        for record in result:
            blog_id = record[0]
            blog_path = record[1]
            blog_paths[blog_id] = blog_path
        
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit(1)
    
    return blog_paths


def get_optional_blog_tables():
    '''Purpose: gets all of the blog tables that aren't required.  Puts those
            optional blog tables into a dictionary where the key is the table
            name, the value is a list of 
    '''
        
    optional_blog_tables = {}
    try:
        cursor.execute('SHOW TABLES')
        result = cursor.fetchall()  # get the result set as a tuple
        
        for record in result:  # parse through each record
            for field in record:  # parse through each field
                if field in site_tables: continue  # don't process site tables
                values = field.split('_', 2)  # the first value will be 'wp', the next, the blog ID, the third, the table name
                table_name = values[2]  # the third element of values is the table name
                blog_id = values[1]  # the second element of values is the blog ID
                if table_name not in required_blog_tables:  # don't process required blog tables
                    if not table_name in optional_blog_tables:  # if the current table name isn't in optional_blog_tables
                        optional_blog_tables[table_name] = []  # define value as a list
                    optional_blog_tables[table_name].append(blog_id)

    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit(1)
        
    return optional_blog_tables

'''
def get_all_tables():
    all_tables = []
    try:
        cursor.execute('SHOW TABLES')
        result = cursor.fetchall()  # get the result set as a tuple
        
        for record in result:  # parse through each record
            table = record[0]
            all_tables.append(table)
            
            
            for field in record:  # parse through each field
                if field in site_tables: continue  # don't process site tables
                values = field.split('_', 2)  # the first value will be 'wp', the next, the blog ID, the third, the table name
                table_name = values[2]  # the third element of values is the table name
                blog_id = values[1]  # the second element of values is the blog ID
                if table_name not in required_blog_tables:  # don't process required blog tables
                    if not table_name in optional_blog_tables:  # if the current table name isn't in optional_blog_tables
                        optional_blog_tables[table_name] = []  # define value as a list
                    optional_blog_tables[table_name].append(blog_id)
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit(1)
        
    return all_tables   
'''

def nonserialized_table_replace(table, column, old_value, new_value):
    '''Purpose: replaces values in a given table and given column only for tables without serialized data
    Requires: database cursor, table to replace values in, column to replace values in,
            the value to be replaced, and the value to replace it with
    Returns: the number of records changed
    '''
    
    try:
        records_changed = cursor.execute("UPDATE %s SET %s = REPLACE(%s, '%s', '%s')" 
                % (table, column, column, old_value, new_value))
            
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        records_changed = 0
#        sys.exit(1)  # exit the script
        
    return records_changed


def serialized_table_replace(table, value_column, id_column, old_value, new_value):
    '''Purpose: replaces values in a given table and given column for tables containing
            serialized data which may or may not contain nonserialized data
    Requires: database cursor, table to replace values in, column to replace values in,
            column containing record IDs, the value to be replaced, and the value to replace it with
    Returns: the number of records changed
    '''
    
    def unserialized_data_replace(unserialized):
        '''Purpose: recursively goes through elements of unserialized data and replaces old value
        Requires: unserialized data.  Can be a string, dictionary, or an object
        Returns: the same unserialized data with the old value replaced
        '''
        
        if type(unserialized) == type:  # if unserialized is an object
            for attr in unserialized.__dict__:
                if not attr.startswith('__') and not attr.endswith('__'):  # only process non-built-in attributes
                    setattr(unserialized, attr, unserialized_data_replace(getattr(unserialized, attr)))  # recursively process attributes
        elif type(unserialized) == dict:  # if unserialized is a dictionary
            for key in unserialized:
                unserialized[key] = unserialized_data_replace(unserialized[key])  # recursively process each key of the dictionary
        elif type(unserialized) == str:  # only process strings; only they'll contain the old value
            if unserialized.find(old_value) != -1:  # if the old value is found
                unserialized = unserialized.replace(old_value, new_value)
        
        return unserialized
    
    def maybe_unserialize(maybe_serialized):
        '''Purpose: recursively attemps to unserialize given data.  Some of
                the data in the Wordpress database is serialized multiple
                times and so must be deserialized multiple times.
        Requires: data that may or may not be serialized.
        Returns: unserialized data.
        '''
        try:
            maybe_serialized = php.loads(maybe_serialized)
            return maybe_unserialize(maybe_serialized)
        except ValueError:
            return maybe_serialized
    
    records_changed = 0  # must be defined in case there aren't any results
    
    try:
        cursor.execute("SELECT %s, %s FROM %s WHERE %s LIKE '%%%s%%'" 
                % (id_column, value_column, table, value_column, old_value))
        # get the result set as a list containing records containing list of fields: 0=id_column, 1=value_column
        result = cursor.fetchall()  # we want a list because we want to modify the results
            
        # convert result tuple to nested list so it can be modified:
        result_list = []
        for subtuple in result:
            result_list.append(list(subtuple))
        
        for record in result_list:  # parses through each record in the result list
            if record[1].startswith('a:') or record[1].startswith('s:') or record[1].startswith('O:'):  # record contains serialized data
                #--------DEBUGGING:-------
#                print "blog_id: %s, %s_id: %s" % (blog_id, column, record[0])  # print option_id of serialized data
                    
#                unserialized = php.loads(record[1].encode('utf_8'))  # result is in unicode, convert to utf_8 or will break serialization
                
                unserialized = maybe_unserialize(record[1].encode('utf_8'))

                unserialized = unserialized_data_replace(unserialized)
                    
                serialized = php.dumps(unserialized)
                record[1] = serialized
                    
                records_changed += cursor.execute("UPDATE %s SET %s = '%s' WHERE %s = '%s'"
                        % (table, value_column, MySQLdb.escape_string(record[1]).decode('utf8'), id_column, record[0]))
                
            else:  # record isn't serialized
                records_changed += cursor.execute("UPDATE %s SET %s = REPLACE(%s, '%s', '%s') \
                        WHERE %s = '%s'" % (table, value_column, value_column, 
                        old_value, new_value, id_column, record[0]))

    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        records_changed = 0
#        sys.exit(1)  # exit the script
        
    return records_changed


def get_site_path():
    try:
        cursor.execute('SELECT domain, path FROM wp_site')
        
        # get the resultset as a tuple
        result = cursor.fetchall()
        
        record = result[0]
        
        return result[0][0] + result[0][1]

    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit( 1 )
        

def fix_joined_url(joined_url):
    fixed_url = posixpath.normpath(joined_url)
    fixed_url = fixed_url.replace('http:/', 'http://')
    fixed_url = fixed_url.replace('https:/', 'https://')
    
    return fixed_url


cursor = db_connect()

'''TODO:
reimplement using SQL Alchemy
'''
