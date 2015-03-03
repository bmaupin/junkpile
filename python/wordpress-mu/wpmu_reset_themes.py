#!/usr/bin/env python
#
# Purpose: reset the theme for all blogs to the default

import wpmu

def main():
    for blog_id in wpmu.get_blog_ids():
        try:
            wpmu.cursor.execute("UPDATE wp_%s_options SET option_value = \
                    'default' WHERE option_name = 'stylesheet'" % (blog_id))
            wpmu.cursor.execute("UPDATE wp_%s_options SET option_value = \
                    'default' WHERE option_name = 'template'" % (blog_id))
            
        except MySQLdb.Error, error:
            sys.stderr.write('ERROR:\t%s\n' % (error))
    

if __name__=='__main__':
    main()
