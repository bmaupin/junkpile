#!/usr/bin/env python3

''' Deletes old messages from a backup file created by Titanium Backup Pro
'''

import datetime
import lxml.etree
import shutil
import sys

MAXIMUM_MESSAGE_AGE_IN_DAYS = 365

if len(sys.argv) < 2:
    sys.exit('USAGE: %s /path/to/com.keramidas.virtual.XML_MESSAGES-XXXXXXXX-XXXXXX.xml' % (sys.argv[0]))

infile_name = sys.argv[1]

# Create a backup copy since we'll modify the original
outfile_name = infile_name + '.bak'
shutil.copy2(infile_name, outfile_name)

# Remove any SMS/MMS messages older than MAXIMUM_MESSAGE_AGE_IN_DAYS
root = lxml.etree.parse(infile_name)

elements_to_remove = []

for element in root.iter():
    if element.tag == '{http://www.titaniumtrack.com/ns/titanium-backup/messages}sms' \
        or element.tag == '{http://www.titaniumtrack.com/ns/titanium-backup/messages}mms':
            message_date = datetime.datetime.strptime(element.get('date'), '%Y-%m-%dT%H:%M:%S.%fZ')
            if datetime.datetime.now() - message_date > datetime.timedelta(MAXIMUM_MESSAGE_AGE_IN_DAYS):
                # We can't remove elements while we're iterating through them
                elements_to_remove.append(element)

for element in elements_to_remove:
    element.getparent().remove(element)

with open(infile_name, 'wb') as infile:
    infile.write(lxml.etree.tostring(root, pretty_print=True, xml_declaration=True))
