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

import ldap


# change these as necessary
debug           = True
ldap_host       = 'ldap.example.com'
ldap_base_dn    = 'ou=groups,dc=example,dc=com'
ldap_filter     = 'cn=somegroup'
ldap_attrs      = ['member',
                   'description',
                  ]
# Scope needs to be one of ldap.SCOPE_BASE, ldap.SCOPE_ONELEVEL, or  
# ldap.SCOPE_SUBTREE
ldap_scope      = ldap.SCOPE_SUBTREE


def main():
    ldap_object = ldap_connect()
    results = ldap_search(ldap_object)
    print results


def ldap_connect():
    '''Binds to LDAP
    Returns: LDAP connection object, used to perform queries
    '''
    
    current_user = getpass.getuser()
    if current_user == 'root':
        sys.exit('Do not run this script as root.  Change users and try'
                 'again.')
    # binds with the current logged-in user
    bind_dn = 'uid=' + current_user + ',ou=accounts,dc=example,dc=com'
    bind_password = getpass.getpass('Please enter your LDAP password: ')
    
    if debug:  
        print 'Binding with DN: %s' % (bind_dn)
    try:
        # initialize secure connection to LDAP server
        ldap_object = ldap.initialize( 'ldaps://%s' %(ldap_host))
        ldap_object.simple_bind_s(bind_dn, bind_password)
        if debug:
            print 'Successfully bound to server.\n'
    except ldap.LDAPError, error_message:
        sys.stderr.write('Couldn\'t connect to LDAP server. %s\n' % 
                         error_message)
    return ldap_object


def ldap_search(ldap_object, filter=ldap_filter, attrs=ldap_attrs, 
                base=ldap_base_dn, scope=ldap_scope):
    '''Function to search LDAP
    It will default to global variables for filter, attributes, base, and 
    scope
    Returns a dictionary where the keys are the searched-for attributes and 
    the values are the values of those attributes
    '''
    
    results_dict = {}
    try:
        # perform a synchronous LDAP search
        search_results = ldap_object.search_s(base, scope, filter, attrs)
        if search_results and len(search_results) > 0:
            for attr in search_results[0][1]:
                results_dict[attr] = search_results[0][1][attr]
            return results_dict
            
        if debug:
            sys.stderr.write('LDAP search results not found\n'
            'base: %s\n'
            'filter: %s\n'
            'attributes: %s\n\n' % (base, filter, attrs))
        
    except ldap.LDAPError, error_message:
        print 'search_results:'
        try:
            print search_results
        except NameError:  # if search_results hasn't been declared
            print  # print a blank line
        sys.stderr.write('LDAPError: %s\n' % (error_message))


def ldap_search_one(ldap_object, filter, attrs=ldap_attrs, base=ldap_base_dn, 
                    scope=ldap_scope):
    ''' Function to search just one LDAP attribute
    '''
    
    attr = attrs[0]
    search_results = {}
    try:
        # perform a synchronous LDAP search
        search_results = ldap_object.search_s(base, scope, filter, [attr])
        if search_results:
            if len(search_results) > 0:
                if attr in search_results[0][1]:
                    # return the first email address of the first user found
                    return search_results[0][1][attr][0]
        if debug:
            sys.stderr.write('LDAP search results not found\n'
            'base: %s\n'
            'filter: %s\n'
            'attribute: %s\n\n' % (base, filter, attr))
        
    except ldap.LDAPError, error_message:
        print 'search_results:'
        print search_results
        sys.stderr.write('LDAPError: %s\n' % (error_message))


if __name__ == '__main__':
    main()
