#!/usr/bin/env python
#
# Constants for the python wpmu tools package.

#CHANGE THESE VALUES AS NECESSARY:
mysql_host = 'localhost'
mysql_db = 'wordpress'

old_blog_hostname = 'myoldblog.example.org'  # must be the FQDN
current_blog_hostname = 'myblog.example.org'  # must be the FQDN

old_filesystem_path = '/var/www/html/wordpress'
current_filesystem_path = '/var/www/html'  # should be the value of <?php echo dirname(__FILE__).'/'; ?>


#DO NOT CHANGE:
required_blog_tables = ['comments', 'links', 'postmeta', 'posts', 
                        'term_relationships', 'term_taxonomy', 'terms', 
                        'options']  # we put options last because it takes the longest to scan

site_tables = ['wp_blog_versions', 'wp_blogs', 'wp_groupmeta', 
               'wp_registration_log', 'wp_signups', 'wp_site', 
               'wp_sitecategories', 'wp_sitemeta', 'wp_usermeta', 'wp_users']
