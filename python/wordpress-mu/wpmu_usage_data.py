#!/usr/bin/env python

import MySQLdb
import os
import sys

import wpmu

home = os.getenv('HOME')

daily_filename = '%s/Desktop/daily.txt' % (home)
total_filename = '%s/Desktop/total.txt' % (home)

daily_users_filename = '%s/Desktop/daily_users.txt' % (home)
total_users_filename = '%s/Desktop/total_users.txt' % (home)

blog_deletions = {'2009-06-03': 2350,
                  '2009-07-01': 22,
                  '2009-08-03': 9,
                  '2009-09-01': 26,
                  '2009-10-01': 47,
                  '2009-11-05': 21}

def main():
#    output_daily_user_registrations()
#    output_total_users()
    output_daily_registrations()
    output_total_registrations()


def get_daily_blog_registrations():
    daily_blog_registrations = {}
    try:
        wpmu.cursor.execute("SELECT date_registered FROM wp_registration_log")
        result = wpmu.cursor.fetchall()
        for record in result:
            date_registered = record[0].strftime('%Y-%m-%d')
            if date_registered not in daily_blog_registrations:
                daily_blog_registrations[date_registered] = 0
            daily_blog_registrations[date_registered] += 1
        
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        sys.exit(1)  # exit the script
    
    return daily_blog_registrations


def get_daily_user_registrations():
    daily_user_registrations = {}
    try:
        wpmu.cursor.execute("SELECT user_registered FROM wp_users")
        result = wpmu.cursor.fetchall()
        for record in result:
            user_registered = record[0].strftime('%Y-%m-%d')
            if user_registered not in daily_user_registrations:
                daily_user_registrations[user_registered] = 0
            daily_user_registrations[user_registered] += 1
        
    except MySQLdb.Error, error:  # if there's an error
        sys.stderr.write('ERROR:\t%s\n' % (error))  # write to the error log
        sys.exit(1)  # exit the script
    
    return daily_user_registrations


def get_daily_registrations():
    """The key for daily_registrations is the day, the value is a list where
    the first element is the number of blog registrations that day and the 
    second is the number of user registrations that day
    """
    daily_registrations = {}
    daily_blog_registrations = get_daily_blog_registrations()
    daily_user_registrations = get_daily_user_registrations()
    
    # update daily registrations with blog data
    for day in daily_blog_registrations:
        daily_registrations[day] = []
        daily_registrations[day].append(daily_blog_registrations[day])
    
    # update daily registrations with user data
    for day in daily_user_registrations:
        if day not in daily_registrations:
            daily_registrations[day] = [0]
        daily_registrations[day].append(daily_user_registrations[day])
    
    # insert 0 values for missing user data
    for day in daily_registrations:
        if len(daily_registrations[day]) < 2:
            daily_registrations[day].append(0)
    
    return daily_registrations


def output_daily_registrations():
    daily_registrations = get_daily_registrations()
        
    daily_file = open(daily_filename, 'w')
    for day in sorted(daily_registrations):
        daily_file.write('%s\t%s\t%s\n' % (day, daily_registrations[day][0], 
                daily_registrations[day][1]))
    daily_file.close()


def output_total_registrations():
    total_registrations = {}
    daily_registrations = get_daily_registrations()
    
    blog_total = 0
    user_total = 0
    for day in sorted(daily_registrations):
        total_registrations[day] = [blog_total + daily_registrations[day][0],
                                    user_total + daily_registrations[day][1]]
        if day in blog_deletions:
            total_registrations[day][0] = total_registrations[day][0] - blog_deletions[day]
        blog_total = total_registrations[day][0]
        user_total = total_registrations[day][1]
        
    
    
    total_file = open(total_filename, 'w')
    for day in sorted(total_registrations):
        total_file.write('%s\t%s\t%s\n' % (day, total_registrations[day][0], 
                total_registrations[day][1]))
    total_file.close()


def output_daily_user_registrations():
    daily_user_registrations = get_daily_user_registrations()
    daily_users_file = open(daily_users_filename, 'w')
    for day in sorted(daily_user_registrations):
        daily_users_file.write('%s\t%s\n' % (day, daily_user_registrations[day]))
    daily_users_file.close()


def output_total_users():
    total_users = {}
    daily_user_registrations = get_daily_user_registrations()
    
    current_total = 0
    for day in sorted(daily_user_registrations):
        total_users[day] = current_total + daily_user_registrations[day]
        current_total = total_users[day]
        
    total_users_file = open(total_users_filename, 'w')
    for day in sorted(total_users):
        total_users_file.write('%s\t%s\n' % (day, total_users[day]))
    total_users_file.close()
    

def output_daily_blog_registrations():
    daily_blog_registrations = get_daily_blog_registrations()
    daily_users_file = open(daily_users_filename, 'w')
    for day in sorted(daily_user_registrations):
        daily_users_file.write('%s\t%s\n' % (day, daily_user_registrations[day]))
    daily_users_file.close()


def output_total_blogs():
    total_users = {}
    daily_user_registrations = get_daily_user_registrations()
    
    current_total = 0
    for day in sorted(daily_user_registrations):
        total_users[day] = current_total + daily_user_registrations[day]
        current_total = total_users[day]
        
    total_users_file = open(total_users_filename, 'w')
    for day in sorted(total_users):
        total_users_file.write('%s\t%s\n' % (day, total_users[day]))
    total_users_file.close()

# calls the main() function
if __name__=='__main__':
    main()