#!/usr/bin/env python

import getpass
import smtplib
import sys


current_user = getpass.getuser()

# change these as necessary
sender = current_user + '@example.com'
smtp_server = 'mail.example.com'
authrequired = 0 # if you need to use SMTP AUTH set to 1
smtpuser = ''  # for SMTP AUTH, set SMTP username here
smtppass = ''  # for SMTP AUTH, set SMTP password here


def main():
    # put your recipients in a list here, like this:
    # recipients = ['test@hotmail.com', 'test2@hotmail.com']
    recipients = []
    send_email(recipients)


def send_email(recipients):    
    email_message = (
            'To: ' + ', '.join(recipients) + '\n' + 
            'From: ' + sender + '\n' + 
            'Subject: PUT YOUR SUBJECT HERE\n\n' +
'''
PUT YOUR EMAIL MESSAGE HERE

You could even add a signature if you want, like this:

--
Bubba F. User
System Admin
Your Department
Your Institution
bubba@example.com
''')
    
    session = smtplib.SMTP(smtp_server)
    if authrequired:
        session.login(smtpuser, smtppass)
    try:
        # if you wish to BCC yourself uncomment the next line 
#        recipients.append(sender)
        smtpresult = session.sendmail(sender, recipients, email_message)

        if smtpresult:
            errstr = ''
            for recip in smtpresult.keys():
                errstr = 'Could not deliver mail to: %s\n\n' + \
                         'Server said: %s\n' + \
                         '%s\n\n' + \
                         '%s' % (recip, smtpresult[recip][0], 
                                 smtpresult[recip][1], errstr)
            raise smtplib.SMTPException, errstr
    except smtplib.SMTPRecipientsRefused, error:
        sys.stderr.write('Error sending email to %s:\t%s\n' % (recipients, 
                                                               error))
    except UnboundLocalError, error:
        sys.stderr.write('ERROR:\t%s\n' % (error))
    

# calls the main() function when the script runs
if __name__ == '__main__':
    main()
