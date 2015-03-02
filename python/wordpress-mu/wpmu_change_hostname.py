#!/usr/bin/env python
#
# Purpose: modifies the Wordpress MU database to reflect the new hostname of the blog server
#        when the software is moved to a different server

import wpmu


def main():
    blog_ids = wpmu.get_blog_ids()
    print 'Highest blog ID: %d' % blog_ids[-1]
    print 'Number of blogs: %d' % len(blog_ids)
    
    fix_site_tables()
    
    fix_blog_tables(blog_ids, ('http://%s' % (wpmu.old_blog_hostname)), 
            ('http://%s' % (wpmu.current_blog_hostname)))
    fix_blog_tables(blog_ids, ('https://%s' % (wpmu.old_blog_hostname)), 
            ('https://%s' % (wpmu.current_blog_hostname)))


def fix_site_tables():
    """Purpose: changes the site tables in the database to reflect the new 
            hostname of the Wordpress MU blog server
    Requires: nothing
    Returns: nothing
    """
    
    print '\nFixing site tables...'
    
    # fix wp_blogs, wp_site, wp_usermeta, wp_users
    to_fix = {'wp_blogs': 'domain',
                     'wp_site': 'domain',
                     'wp_usermeta': 'meta_value',
                     'wp_users': 'user_url',
                     } # dictionary containing tables to fix as keys and columns to fix as values
    
    for table in to_fix:
        column = to_fix[table]
        records_changed = wpmu.nonserialized_table_replace(table, column, 
                wpmu.old_blog_hostname, wpmu.current_blog_hostname)

        print "%s:\t%s record(s) modified" % (table, records_changed)
    
    
    # fix wp_sitemeta
    records_changed = wpmu.serialized_table_replace('wp_sitemeta', 
            'meta_value', 'meta_id', wpmu.old_blog_hostname, 
            wpmu.current_blog_hostname)
    print 'wp_sitemeta:\t%s record(s) modified' % (records_changed)
        

def fix_blog_tables(blog_ids, old_blog_url, current_blog_url):
    """Purpose: changes the blog-specific tables in the database to reflect the new hostname of the
            Wordpress MU blog server
    Requires: a list of all of the blog IDs, the old blog URL, the current blog URL
    Returns: nothing
    """
    
    print '\nFixing blog-specific tables...'
    
    # fix wp_###_comments, wp_###_links, and wp_###_posts
    to_fix = {'comments': ['comment_author_url', 'comment_content', 'comment_agent'],
              'links': ['link_url', 'link_name'],
              'posts': ['post_content', 'guid'],
             }
    
    for table in to_fix:
        records_changed = 0  # reset number of records changed for each set of tables scanned
        for column in to_fix[table]:
            for blog_id in blog_ids:
                records_changed += wpmu.nonserialized_table_replace(
                        ('wp_%s_%s' % (blog_id, table)), column, old_blog_url,
                         current_blog_url)
    
        print 'wp_###_%s:\t%s record(s) modified' % (table, records_changed)

    
    # fix wp_###_postmeta and wp_###_options
    to_fix = {'postmeta': ['meta_id', 'meta_value'],
              'options': ['option_id', 'option_value'],
              }
    
    for table in to_fix:
        records_changed = 0  # reset number of records changed for each set of tables scanned
        id_column = to_fix[table][0]
        value_column = to_fix[table][1]
        
        for blog_id in blog_ids:
            records_changed += wpmu.serialized_table_replace(('wp_%s_%s' % 
                    (blog_id, table)), value_column, id_column, old_blog_url, 
                    current_blog_url)
    
        print "wp_###_%s:\t%s record(s) modified" % (table, records_changed)


# calls the main() function
if __name__=='__main__':
    main()
    
    
# TODO:
#   clean up