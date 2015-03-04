#!/usr/bin/env python

'''Displays blog plugin and theme usage.
'''

import wpmu
import MySQLdb
import sys

blog_ids = wpmu.get_blog_ids()
blog_paths = wpmu.get_blog_paths()


def main():
    print 'Please make a selection:'
    print '\t1. Search all blogs to see what themes are being used'
    print '\t2. Search to see which blogs are using a specific theme'
    print '\t3. Search to see which blogs are using a specific plugin'
    choice = raw_input()
    if choice == '1':
        search_all_themes()
    if choice == '2':
        search_one_theme()
    if choice == '3':
        search_one_plugin()

    
def search_all_themes():    
    # search all blogs to see what themes are being used
    themes = {}

    for blog_id in blog_ids:
        try:
            wpmu.cursor.execute("SELECT option_value FROM wp_%s_options \
                    WHERE option_name = 'template'" % (blog_id))
            result = wpmu.cursor.fetchall()
            
            theme = result[0][0]
            # if we haven't already seen this theme
            if theme not in themes:
                # define this dictionary entry as a list
                themes[theme] = [0,[]]
            # increment the theme count
            themes[theme][0] += 1
            
            # save the first 10 occurrences of the theme as the second list entry of the dictionary
            if len(themes[theme][1]) < 11:
                themes[theme][1].append(blog_id)
            
        except MySQLdb.Error, error:
            sys.stderr.write('ERROR:\t%s\n' % (error))
    
    for theme in sorted(themes):
        theme_count = themes[theme][0]
        # make the output purty
        spacing = ' ' * (30 - len(theme)) 
        print '%s%s%s' % (theme, spacing, themes[theme][0])
        # if there were less than 10 instances of that theme
        if theme_count < 15:
            for blog_id in themes[theme][1]:
                # print the blog URLs of the blogs using that theme
                print wpmu.fix_joined_url('\thttp://%s/%s' % (wpmu.get_site_path(), blog_paths[blog_id]))
        else:
            for blog_id in themes[theme][1][0:5]:
#            blog_id = themes[theme][1][0]
                print wpmu.fix_joined_url('\thttp://%s/%s' % (wpmu.get_site_path(), blog_paths[blog_id]))

 
def search_one_theme():
    # search all blogs to see which blogs are using a specific theme
    search_string = raw_input( 'Enter theme folder name: ' )
    total_finds = 0

    for blog_id in blog_ids:
        try:
            wpmu.cursor.execute("SELECT option_value FROM wp_%s_options \
                    WHERE option_name = 'template'" % (blog_id))
            result = wpmu.cursor.fetchall()
            
            theme = result[0][0]
            
            found = -1  # reset value of found; not found yet
            found = theme.find(search_string)
            if found != -1:  # it's there
                total_finds += 1
                print wpmu.fix_joined_url('\thttp://%s/%s' % (wpmu.get_site_path(), blog_paths[blog_id]))
#                print wpmu.fix_joined_url('\thttp://%s%s/wp-admin/themes.php' % (wpmu.get_site_path(), blog_paths[blog_id]))
            
        except MySQLdb.Error, error:
            sys.stderr.write('ERROR:\t%s\n' % (error))
    
    print '\nFound in %s blogs' % (total_finds)
    
    
def search_one_plugin():
    # search all blogs to see which blogs are using a given plugin
    search_string = raw_input( 'Enter plugin URL: ' )
    total_finds = 0

    for blog_id in blog_ids:
        try:
            wpmu.cursor.execute("SELECT option_value FROM wp_%s_options \
                    WHERE option_name = 'active_plugins'" % (blog_id))
            result = wpmu.cursor.fetchall()
            
            active_plugins = result[0][0]
            found = -1  # reset value of found; not found yet
            found = active_plugins.find(search_string)
            if found != -1:  # it's there
                total_finds += 1
                print wpmu.fix_joined_url('\thttp://%s/%s' % (wpmu.get_site_path(), blog_paths[blog_id])))
#                print wpmu.fix_joined_url('\thttp://%s%s/wp-admin/plugins.php' % (wpmu.get_site_path(), blog_paths[blog_id]))
            
        except MySQLdb.Error, error:
            sys.stderr.write('ERROR:\t%s\n' % (error))
    
    print '\nFound in %s blogs' % (total_finds)


# calls the main() function
if __name__=='__main__':
    main()
