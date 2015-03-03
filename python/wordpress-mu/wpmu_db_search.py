#!/usr/bin/env python
#
# Purpose: searches Wordpress MU database for given string(s)

import wpmu
import sys
import MySQLdb


def main():
    search_selection = raw_input('\nPlease enter search string(s), separated by commas:\n')
    search_selections = search_selection.split(',')
    search_strings = []
    for search_selection in search_selections:
        search_strings.append(search_selection.strip())
    
    print """\nWhich tables do you wish to search?
1. site tables
2. required blog tables
3. optional blog tables
4. all blog tables
5. all tables
    """
    
    selection = raw_input('or, type in the name of the table(s) you wish to search, separated by commas:\n')
    
    blog_ids = wpmu.get_blog_ids()

    optional_blog_tables = wpmu.get_optional_blog_tables()
    
    try:
        selection = int(selection)
        if selection < 1 or selection > 5:
            print 'Selection must be between 1 and 5; %s is invalid!' % (selection)
            sys.exit(1)
        if selection == 1 or selection == 5:
            for table in wpmu.site_tables:
                check_site_tables(table, search_strings)
        if selection > 2:
            for table in sorted(optional_blog_tables):
                check_blog_tables(table, search_strings, blog_ids, optional_blog_tables)
        if selection == 2 or selection > 3:
            for table in wpmu.required_blog_tables:
                check_blog_tables(table, search_strings, blog_ids, optional_blog_tables)

    except ValueError:  # do the following if a string is typed (int(selection will throw a ValueError in that case)
        selections = selection.split(',')  # split input in case it contains a comma-separated list of tables
        tables = []
        for selection in selections:
            tables.append(selection.strip())  # strip whitespace from each element of input and append to tables list
        is_table = False
        for table in tables:
            if table in wpmu.site_tables:
                is_table = True
                check_site_tables(table, search_strings)
            elif (table in wpmu.required_blog_tables) or (table in optional_blog_tables):
                is_table = True
                check_blog_tables(table, search_strings, blog_ids, optional_blog_tables)
            else:
                print '%s is not a valid table!' % (table)
                sys.exit(1)


def search_table(table_name, search_strings, search_results):
    found_in_table = False
    
    try:
        # brute force search; search all fields in the given tables
        wpmu.cursor.execute("SELECT * from %s" % (table_name))
        result = wpmu.cursor.fetchall()
        
        for record in result:  # search each record of each table
            for field_index in range(len(record)):  # search each field of each record
                field_name = wpmu.cursor.description[field_index][0]
                field = record[field_index]
                found = -1
                if type(field) == unicode:  # only search strings (unicode in this case) not long, date, etc.
                    """# find serialized data
                    if field.startswith('a:') or field.startswith('s:') or field.startswith('O:'):
                        found_in_table = True
    
                        if field_index not in search_results:
                            search_results[field_index] = [0,[]]  # define nested list in the dictionary
                        if field_index not in dirty_columns:
                            dirty_columns[field_index] = None  # define key of dirty columns, to be assigned later
                        if str(blog_id) not in search_results[field_index][1]:
                            if (blog_id) and (len(search_results[field_index][1]) < 5):  # we only want the first 5 blog IDs
                                search_results[field_index][1].append(str(blog_id))  # set the current blog_id to element 0
                        search_results[field_index][0] += 1  # increment element 1
                    """
                    
                
                    for search_string in search_strings:
                        found = field.find(search_string)
                        if found != -1: break  # move on if a search string's already been found
                
                if found != -1:  # if the search string was found
                    found_in_table = True
    
                    if field_name not in search_results:
                        search_results[field_name] = [0, []]  # make sure key is defined
                    search_results[field_name][0] += 1  # increment occurrences
                    
                    # blog-specific table stuff
                    if table_name not in wpmu.site_tables:  # only process blog-specific tables
                        values = table_name.split('_', 2)  # the first value will be 'wp', the next, the blog ID, the third, the table name
                        blog_id = values[1]
                    
                        if str(blog_id) not in search_results[field_name][1]:
                            if (blog_id) and (len(search_results[field_name][1]) < 5):  # we only want the first 5 blog IDs
                                search_results[field_name][1].append(str(blog_id))  # set the current blog_id to element 0
                    
                    
    except MySQLdb.Error, error:  # if there's an error
#        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to log and keep going (some tables may be missing)
        pass  # ignore; some tables may be missing and will throw errors           
    
    # -----------DEBUGGING:----------
#    if found_in_table:
    # print which searched tables were found
#        print "Found %s in %s." % (search_strings, table_name)
#    else:
#        print "%s: Not found!" % (table_name)
    
    return found_in_table


def check_site_tables(table_to_check, search_strings):
    found_in_table = False
    search_results = {}
    
    print '\n\nChecking %s:' % (table_to_check)
    
    found_in_table = search_table(table_to_check, search_strings, search_results)
    
    if found_in_table:
        print '\nfound in fields:'
        print 'field\t\toccurrences'
        for field in search_results:
            print '%s:\t\t%s' % (field, search_results[field][0])
    else:
        print '\nclean'


def check_blog_tables(table_to_check, search_strings, blog_ids, 
        optional_blog_tables):
    found_in_tables = 0  # number of tables where search_string is found
    search_results = {}  # dictionary where key is field index, value is a 
            # nested list where element 0 is the name of the field, element 1 
            # is the number of times the particular field contained the 
            # searched-for value and element 2 is a nested list containing 
            # first 5 blog IDs where value occurs in field
    
    print '\n\nChecking wp_###_%s:' % (table_to_check)
    
    if table_to_check not in wpmu.required_blog_tables:
        blog_ids = optional_blog_tables[table_to_check]

    for blog_id in blog_ids:
        table_name = 'wp_%s_%s' % (blog_id, table_to_check)
        #---------DEBUGGING:----------
#        print table_name
            
        found_in_tables += search_table(table_name, search_strings, 
                search_results)

    if found_in_tables:
        print '\nfound in tables: %s/%s' % (found_in_tables, len(blog_ids))
        print 'found in fields:'
        print 'field\t\toccurrences\tblog IDs'
        for field in search_results:
            print '%s:\t\t%s\t\t%s' % (field, search_results[field][0], 
                    ', '.join(search_results[field][1]))
    else:
        print '\nclean'


# calls the main() function
if __name__=='__main__':
    main()
    
# TODO:
#    use wpmu.get_all_tables for get_optional_blog_tables
#   object to contain all information for found search results for each group of tables, i.e. wp_###_options
#   cleaner output?
#