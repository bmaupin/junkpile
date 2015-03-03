#!/usr/bin/env python

'''Get all the users from the blog who use LDAP for authentication.
Then search and see if they're in LDAP.
'''


import getpass
import ldap
import MySQLdb
import sys

import wpmu


# LDAP connection settings
ldap_host = 'ldap.example.org'
base_dn = 'cn=accounts,dc=example,dc=org'
bind_dn_pattern = 'uid=%s,%s'
    
ldap_user = raw_input('Please enter the LDAP user: ')
ldap_passwd = getpass.getpass('Please enter the LDAP password: ')

bind_dn = bind_dn_pattern % (ldap_user, base_dn)


def main():
    count = 0
    blog_logins = get_blog_logins()
    blog_ldap_users = get_blog_ldap_users()
    
    print '\nUsers not in LDAP:'
    for user_id_number in blog_logins:
        user_login = blog_logins[user_id_number]
        # We only want to process users that are using LDAP to login
        if user_id_number in blog_ldap_users:
            sys.stdout.write('Searching %s: %s     \r' % (user_id_number, user_login))
            sys.stdout.flush()
            result = ldap_search_uid(user_login)
            if not result:
                print '%s: %s               ' % (user_id_number, user_login)


def get_blog_logins():
    blog_logins = {}
    try:
        wpmu.cursor.execute("SELECT ID, user_login from wp_users order by ID")
        result = wpmu.cursor.fetchall()
        
        for record in result:
            user_id_number = record[0]
            user_login = record[1]
            
            blog_logins[user_id_number] = user_login
    
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        sys.exit(1)  # exit the script

    return blog_logins


def get_blog_ldap_users():
    blog_ldap_users = []
    try:
        wpmu.cursor.execute("SELECT user_id FROM wp_usermeta WHERE meta_key \
                = 'ldap_login' AND meta_value = 'true' ORDER BY user_id")
        result = wpmu.cursor.fetchall()
        
        for record in result:
            user_id_number = record[0]
            blog_ldap_users.append(user_id_number)
    
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        sys.exit(1)  # exit the script
    
    return blog_ldap_users


def ldap_search_uid(blog_login):
    filter = 'uid=%s' % (blog_login)
    attributes = ['uid']
    
#    ldap_object = ldap_connect()
    
    # do the search
    try:
        search_result = ldap_object.search_s(base_dn, ldap.SCOPE_SUBTREE, filter, attributes)  # performs a synchronous LDAP search
        if search_result:
            ldap_uid = search_result[0][1]['uid'][0]
            if ldap_uid == blog_login:
                return True
            else: return False
        else: return False
        
        """
        for a in range(len(search_result)):  # iterate through top level of list containing entries for LDAP accounts
            print "\n--------dn: " + search_result[a][0] + ":--------"  # print dn
            for keys in search_result[a][1].keys():  # iterate through dictionary containing results for entries
                print keys + ":",  # print searched for attributes
                for b in range(len(search_result[a][1][keys])):  # print results of searched for attributes
                    if b == 0: print search_result[a][1][keys][b]   # first result on same line
                    else: print "\t" + search_result[a][1][keys][b]   # following results on new lines with tab
        """
    except ldap.LDAPError, error_message:
        print error_message


def ldap_connect():
#    print 'Binding with DN: %s' % (bind_dn)
    
    try:
        ldap_object = ldap.initialize('ldaps://%s' % (ldap_host))
        ldap_object.simple_bind_s(bind_dn, ldap_passwd)
#        print "Successfully bound to server.\n"
    except ldap.LDAPError, error_message:
        print "Couldn't connect to LDAP server. %s " % error_message
        
    return ldap_object

# Go ahead and connect to LDAP
ldap_object = ldap_connect()


# calls the main() function
if __name__=='__main__':
    main()
