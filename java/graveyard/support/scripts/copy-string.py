#!/usr/bin/env python

import os
import os.path
import sys

import lxml.etree

source_path = os.path.expanduser('~/workspace/git/android/packages/apps/Mms')
#source_path = os.path.expanduser('~/workspace/git/android/platform/packages/apps/Mms')
#source_path = os.path.expanduser('~/workspace/git/android/frameworks/base/core/res')
dest_path = os.path.expanduser('~/workspace/git/android-sms-merge/android_sms_merge')

def main():
    def xml_element_compare(element1, element2):
        for key in element1.attrib:
            if element1.attrib[key] != element2.attrib[key]:
                return False
        return True

    if len(sys.argv) < 2:
        sys.exit('Error: STRING is required')
    
    string_to_copy = sys.argv[1]
    
    source_res_path = os.path.join(source_path, 'res')
    dest_res_path = os.path.join(dest_path, 'res')
    
    # This allows lxml to output much nicer looking output
    parser = lxml.etree.XMLParser(remove_blank_text=True)
    
    for values_folder in os.listdir(source_res_path):
        source_values_path = os.path.join(source_res_path, values_folder)
        
        if (os.path.isdir(source_values_path)
            and values_folder.startswith('values')):
            source_strings_path = os.path.join(source_values_path, 'strings.xml') 
            
            if (os.path.isfile(source_strings_path)):
                source_root = lxml.etree.parse(source_strings_path, parser)
                
                for source_element in source_root.iter('string'):
                    if source_element.get('name') == string_to_copy:
                        dest_values_path = os.path.join(dest_res_path, values_folder)
                        # Create the destination values folder if necessary
                        if not os.path.exists(dest_values_path):
                            os.mkdir(dest_values_path)
                        
                        dest_strings_path = os.path.join(dest_values_path, 'strings.xml')
                        
                        if not os.path.exists(dest_strings_path):
                            root = lxml.etree.Element(
                                source_root.getroot().tag,
                                nsmap=source_root.getroot().nsmap)
                            root.append(source_element)
                            dest_root = lxml.etree.ElementTree(root)
                        
                        else:
                            dest_root = lxml.etree.parse(dest_strings_path, parser)
                            
                            # Iterate over the elements in the destination file
                            it = dest_root.iter('string')
                            while True:
                                try:
                                    dest_element = it.next()
                                    # Don't insert duplicate elements
                                    if xml_element_compare(
                                        dest_element,
                                        source_element) == True:
                                        break
                                    
                                    # Insert the new string alphabetically
                                    if string_to_copy < dest_element.get('name'):
                                        dest_element.addprevious(source_element)
                                        # Don't process any more destination elements
                                        break
                                    
                                except StopIteration:
                                    # If we made it this far, add it to the end
                                    dest_element.addnext(source_element)
                                    break
                        
                        # Write the updated XML file
                        dest_root.write(
                            dest_strings_path, 
                            encoding='utf-8',
                            pretty_print=True,
                            xml_declaration=True,
                            )


if __name__ == '__main__':
    main()
