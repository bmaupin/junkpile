#!/usr/bin/env python

import sys

import lxml.etree

def main():
    if len(sys.argv) < 3:
        sys.stderr.write('ERROR: Must provide at least 2 KML files to merge\n')
        sys.exit('Usage: {} FILE1 FILE2 ...'.format(sys.argv[0]))
    
    first_kml_root = lxml.etree.parse(sys.argv[1]).getroot()
    first_kml_ns = first_kml_root.nsmap[None]
    first_kml_document = first_kml_root.find('{{{}}}Document'.format(
            first_kml_ns))
    
    for filename in sys.argv[2:]:
        kml_root = lxml.etree.parse(filename).getroot()
        kml_ns = kml_root.nsmap[None]
        kml_document = kml_root.find('{{{}}}Document'.format(kml_ns))
        # Add the Document node's child elements to the first KML file
        for element in kml_document.iterchildren():
            first_kml_document.append(element)
            
        print(lxml.etree.tostring(
                first_kml_root,
                encoding='utf-8',
                xml_declaration=True,
                pretty_print=True,
        # .decode('utf-8') is required for Python 3
        ).decode('utf-8'))


if __name__ == '__main__':
    main()
