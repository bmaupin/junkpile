#!/usr/bin/env python

'''Spits out URLs of blogs that weren't successfully upgraded.
Run the script and go to each URL to manually upgrade the blog.
'''

import wpmu
import MySQLdb
import sys

#current_db_version = '7796'  # WPMU 1.5.1
#current_db_version = '8204'  # WPMU 2.6.5
current_db_version = '9872'  # WPMU 2.7.1


blog_ids = wpmu.get_blog_ids()
blog_paths = wpmu.get_blog_paths()


def main():
    blogs_to_upgrade = {}
    
    try:
        wpmu.cursor.execute("SELECT * FROM wp_blog_versions ORDER BY blog_id")
        result = wpmu.cursor.fetchall()
        
        for record in result:
            blog_id = record[0]
            db_version = record[1]
            
            if db_version != current_db_version:  # if the blog DB hasn't been updated
                if blog_id in blog_ids:  # make sure it's in the list of blog IDs; we don't care about other entries
                    blogs_to_upgrade[blog_id] = [db_version]
        
        
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))
        sys.exit(1)
        
    for blog_id in blogs_to_upgrade:
        db_version = blogs_to_upgrade[blog_id]
        print '%s\t%s\t%s' % (blog_id, db_version, wpmu.fix_joined_url('http://%s/%s/wp-admin/upgrade.php' % (wpmu.get_site_path(), blog_paths[blog_id])))


# calls the main() function
if __name__=='__main__':
    main()
