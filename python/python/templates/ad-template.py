#!/usr/bin/env python

'''
 Copyright (C) 2011 Bryan Maupin <bmaupincode@gmail.com>
 
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

import ldap
from ldap.controls import SimplePagedResultsControl


# change these as necessary
debug         = True
ad_host       = 'ad.example.com'
# DN used for binding to AD
ad_bind_dn    = 'cn=%s,ou=users,dc=example,dc=com'
# DN used as the search base
ad_base_dn    = 'ou=users,dc=example,dc=com'
ad_filter     = '(objectClass=*)'
ad_attrs      = ['cn', 'distinguishedName']
# Scope needs to be one of ldap.SCOPE_BASE, ldap.SCOPE_ONELEVEL, or  
# ldap.SCOPE_SUBTREE
ad_scope      = ldap.SCOPE_SUBTREE
# How many search results to return at a time (must be less than 1000 for AD)
ad_page_size  = 1000


def main():
    ad_object = ad_connect()
    results = ad_search(ad_object)
    print results


def ad_connect():
    '''Binds to AD
    Returns: AD connection object, used to perform queries
    '''
    
    username = raw_input('Please enter your AD username (or press enter to '
                         'use %s): ' % (getpass.getuser()))
    if username == '':
        username = getpass.getuser()
        
    bind_dn = ad_bind_dn % (username)
    bind_password = getpass.getpass('Please enter your AD password: ')
    
    if debug:  
        print 'Binding with DN: %s' % (bind_dn)
    try:
        # initialize secure connection to AD server
        ad_object = ldap.initialize( 'ldaps://%s' %(ad_host))
        ad_object.simple_bind_s(bind_dn, bind_password)
        if debug:
            print 'Successfully bound to server.\n'
    except ldap.LDAPError, error_message:
        sys.stderr.write('Couldn\'t connect to AD server. %s\n' % 
                         error_message)
    return ad_object


def ad_search(ad_object, filter=ad_filter, attrs=ad_attrs, 
                base=ad_base_dn, scope=ad_scope):
    '''Function to search AD
    It will default to global variables for filter, attributes, base, and 
    scope
    Returns a list of search results.  Each entry itself is a list, where the 
    first item is the DN of the entry, and the second item is a dictionary of
    attributes and values.
    '''
    
    search_results = []
    
    ad_control = SimplePagedResultsControl(
        ldap.LDAP_CONTROL_PAGE_OID, True, (ad_page_size, '')
    )

    try:
        ad_pages = 0
        while True:
            # Send search request
            msgid = ad_object.search_ext(
                ad_base_dn,
                ad_scope,
                ad_filter,
                ad_attrs,
                serverctrls=[ad_control]
            )
            
            ad_pages += 1
            if debug:
                print 'Getting page %d' % (ad_pages)
            unused_code, results, unused_msgid, serverctrls = \
                                                        ad_object.result3(msgid)
            if debug:
                print '%d results' % len(results)
            
            if results and len(results) > 0:
                search_results.extend(results)
        
            for serverctrl in serverctrls:
                if serverctrl.controlType == ldap.LDAP_CONTROL_PAGE_OID:
                    unused_est, cookie = serverctrl.controlValue
                    if cookie:
                        ad_control.controlValue = (ad_page_size, cookie)
                    break
            if not cookie:
                break
        
        return search_results
        
        if debug:
            sys.stderr.write('LDAP search results not found\n'
            'base: %s\n'
            'filter: %s\n'
            'attributes: %s\n\n' % (base, filter, attrs))
            return []
        
    except ldap.LDAPError, error_message:
        print 'search_results:'
        try:
            print search_results
        except NameError:  # if search_results hasn't been declared
            print  # print a blank line
        sys.stderr.write('LDAPError: %s\n' % (error_message))


if __name__ == '__main__':
    main()
