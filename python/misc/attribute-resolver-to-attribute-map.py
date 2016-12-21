#!/usr/bin/env python

''' Converts list of attributes in Shibboleth IdP attribute-resolver.xml to list
of attributes for Shibboleth SP attribute-map.xml
'''

import lxml.etree
import sys

def main():
    if len(sys.argv) < 2:
        sys.exit('USAGE: %s /path/to/attribute-resolver.xml' % (sys.argv[0]))

    root = lxml.etree.parse(sys.argv[1])

    attributes = {}

    for attribute_definition in root.iter('{urn:mace:shibboleth:2.0:resolver}AttributeDefinition'):
        attribute_id = attribute_definition.attrib['id']
        attribute_name = attribute_definition.find('{urn:mace:shibboleth:2.0:resolver}AttributeEncoder').attrib['name']

        attributes[attribute_id] = attribute_name

    print('<Attributes xmlns="urn:mace:shibboleth:2.0:attribute-map" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')

    for attribute_id in sorted(attributes):
        print('    <Attribute name="{}" id="{}"/>'.format(attributes[attribute_id], attribute_id))

    print('</Attributes>')

if __name__ == '__main__':
    main()
