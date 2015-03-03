#!/usr/bin/env python

'''Prints out information for blog users using local auth
'''


import wpmu


def clean_output(output, length):
    # return spaces in case variable is empty
    if output == None:
        return ' ' * length
    # convert connection times to integer strings for easier and cleaner output
    elif type(output) == float or type(output) == int or type(output) == long:
        output = '%i' % (output)
    if length > 0:
        # shorten the output if it's more than 1 less than the length of the column
        short_output = output[0:length - 1]
        return short_output + (' ' * (length - len(short_output)))
    else:
        return output + (' ' * (length - len(output)))

def main():
    def add_to_local_blog_logins():
        local_blog_logins[user_id_number] = blog_logins[user_id_number]
        wpmu.cursor.execute("SELECT meta_value FROM wp_usermeta \
                WHERE meta_key = 'description' AND user_id = '%s'" % 
                (user_id_number))
        result = wpmu.cursor.fetchall()
        if result:
            description = result[0][0]
        else:
            description = ''
        local_blog_logins[user_id_number]['description'] = description
        
    
    local_blog_logins = {}
    
    blog_logins = get_blog_logins()
    for user_id_number in blog_logins:
        user_login = blog_logins[user_id_number]['user_login']
        wpmu.cursor.execute("SELECT meta_value FROM wp_usermeta WHERE \
                meta_key = 'ldap_login' AND user_id = '%s'" % 
                (user_id_number))
        result = wpmu.cursor.fetchall()
        
        if result:
            if result[0][0] != 'true':
                add_to_local_blog_logins()
        else:
            add_to_local_blog_logins()

    for user_id_number in sorted(local_blog_logins):
        print '%s%s%s%s' % (clean_output(user_id_number, 7), 
                clean_output(blog_logins[user_id_number]['user_login'], 36), 
                #clean_output(blog_logins[user_id_number]['user_pass'], 36),
                clean_output(blog_logins[user_id_number]['user_email'], 36),
                clean_output(blog_logins[user_id_number]['user_url'], 0))
#                clean_output(local_blog_logins[user_id_number]['description'], 0))

    print '%s local users' % (len(local_blog_logins))

#    for user_id_number in sorted(local_blog_logins):
#        print '%shttp://blog.example.org/wp-admin/wpmu-users.php?s=%s' \
#                % (clean_output(user_id_number, 7),
#                clean_output(blog_logins[user_id_number]['user_login'], 0)) 

#    for user_id_number in sorted(local_blog_logins):
#        if blog_logins[user_id_number]['user_url'] == 'http://blog.example.org/someblog/':
#            print '%s%shttp://blog.example.org/wp-admin/wpmu-users.php?s=%s' \
#                    % (clean_output(user_id_number, 7),
#                    clean_output(blog_logins[user_id_number]['user_url'], 29),
#                    clean_output(blog_logins[user_id_number]['user_login'], 0)) 
    
#    for user_id_number in sorted(local_blog_logins):
#        print '%s:%s:%s::::' % (blog_logins[user_id_number]['user_login'],
#                blog_logins[user_id_number]['user_pass'],
#                user_id_number)
    
def get_blog_logins():
    blog_logins = {}
    try:
        wpmu.cursor.execute("SELECT ID, user_login, user_pass, user_email, \
                user_url from wp_users order by ID")
        result = wpmu.cursor.fetchall()
        
        for record in result:
            user_id_number = record[0]
            user_login = record[1]
            user_pass = record[2]
            user_email = record[3]
            user_url = record[4]
            
            blog_logins[user_id_number] = {}
            blog_logins[user_id_number]['user_login'] = user_login
            blog_logins[user_id_number]['user_pass'] = user_pass
            blog_logins[user_id_number]['user_email'] = user_email
            blog_logins[user_id_number]['user_url'] = user_url
    
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        sys.exit(1)  # exit the script

    return blog_logins


# calls the main() function
if __name__=='__main__':
    main()
