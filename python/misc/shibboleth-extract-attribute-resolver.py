#!/usr/bin/env python

''' Extracts attributes from Shibboleth IdP attribute-resolver.xml and formats
them for Shibboleth IdP attribute-filter.xml and Shibboleth SP attribute-map.xml
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

    print_attribute_rules(attributes)
    print()
    print_attribute_map(attributes)


def print_attribute_map(attributes):
    print('<Attributes xmlns="urn:mace:shibboleth:2.0:attribute-map" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')

    for attribute_id in sorted(attributes):
        print('    <Attribute name="{}" id="{}"/>'.format(attributes[attribute_id], attribute_id))

    print('</Attributes>')


def print_attribute_rules(attributes):
    ATTRIBUTE_RULE_TEMPLATE = '''        <AttributeRule attributeID="{}">
            <PermitValueRule xsi:type="ANY" />
        </AttributeRule>'''

    for attribute_id in sorted(attributes):
        print(ATTRIBUTE_RULE_TEMPLATE.format(attribute_id))


if __name__ == '__main__':
    main()
