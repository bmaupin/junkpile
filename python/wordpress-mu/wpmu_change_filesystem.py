#!/usr/bin/env python
#
# Purpose: modifies the filesystem locations of the Wordpress MU software
#    location which are unfortunately hardcoded in the database.  It's
#    necessary to change these when the software is moved to another location.
# Requires: python wpmu tools library, wpmu_constants with old_filesystem_path
#    and current_filesystem_path defined

import wpmu


def main():
    blog_ids = wpmu.get_blog_ids()
    
    fix_filesystem_paths(blog_ids)    


def fix_filesystem_paths(blog_ids):
    print '\nFixing blog-specific tables...'
    
    to_fix = {'postmeta': ['meta_id', 'meta_value'],
              'options': ['option_id', 'option_value']
              }
    
    for table in to_fix:
        # reset number of records changed for each set of tables scanned
        records_changed = 0
        id_column = to_fix[table][0]
        value_column = to_fix[table][1]
        
        for blog_id in blog_ids:
            records_changed += wpmu.serialized_table_replace(('wp_%s_%s' % 
                    (blog_id, table)), value_column, id_column, 
                    wpmu.old_filesystem_path, wpmu.current_filesystem_path)
    
        print "wp_###_%s:\t%s record(s) modified" % (table, records_changed)
    
    
# calls the main() function
if __name__=='__main__':
    main()
