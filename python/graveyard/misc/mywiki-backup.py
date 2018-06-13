#!/usr/bin/env python

import os
import os.path
import sys
import time
import urllib2
import urlparse

import lxml.etree
import lxml.html

debug = False

def main():
    site_url = 'http://sites.google.com/site/bmaupinwiki'
    #dest_path = '%s/Documents/misc/bmaupinwiki' % (home)
    dest_path = '{0}/Desktop/bmaupinwiki'.format(os.getenv('HOME'))
    
    ensure_folder_exists(dest_path)
    
    link_paths = []
    
    parsed_url = urlparse.urlsplit(site_url)
    
    outfile_name = 'home'
    
    write_url_to_file(
        site_url, 
        '{0}.html'.format(
            os.path.join(dest_path, outfile_name)
        ),
        site_url,
        dest_path,
        check_timestamp=True,
        insert_encoding=True
    )
    
    # attempt to alleviate encoding issues
    parser = lxml.html.HTMLParser(encoding='utf-8')
    
    try:
        page = lxml.html.parse(site_url, parser).getroot()
    # in case there's a bug in lxml (http://stackoverflow.com/q/3116269/399105)
    except IOError:
        page = lxml.html.parse(urllib2.urlopen(site_url), parser).getroot()
    
    # iterate through all of the div elements in the main index page
    for element in page.iter('div'):
        # get the table of contents
        if element.get('class') == 'nav-toc-content':
            toc = element.find('ul')
            break
    
    # iterate through all of the links ("a" elements) in the table of contents
    for element in toc.iter('a'):
        link = element.get('href')
        # if the path of the URL is in the link
        if link.startswith(parsed_url.path):
            # remove it
            link = link.replace(parsed_url.path, '')
            # remove a starting slash
            if link.startswith('/'):
                link = link[1:]
            link_paths.append(link)
    
    if debug:
        link_paths.sort()
        print link_paths

    for link_path in link_paths:
        # drop everything after the final /, and that's the path
        path = link_path.rsplit('/', 1)[0]
        full_path = os.path.join(dest_path, path)
        
        ensure_folder_exists(full_path)
        
        url = '%s/%s' % (site_url, link_path)
        if debug:
            print url
            print '%s/%s.html' % (dest_path, link_path)
        
        write_url_to_file(
            url, 
            '{0}.html'.format(
                os.path.join(dest_path, link_path)
            ),
            site_url,
            dest_path,
            check_timestamp=True,
            insert_encoding=True
        )


def ensure_folder_exists(path):
    # make sure the path isn't an existing file
    if os.path.isfile(path):
        sys.exit('ERROR: folder %s is an existing file' % (path))
    # create the path if necessary
    elif not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError, error:
            sys.exit('OSError: %s' % (error))


def write_url_to_file(url, outfile_path, site_url, dest_path,
        check_timestamp=False, insert_encoding=False):
    try:
        infile = urllib2.urlopen(url)
    except urllib2.HTTPError, error:
        sys.exit('HTTPError: %s' % (error))
    except urllib2.URLError, error:
        sys.exit('URLError: %s' % (error))
    
    # only check the timestamp if the destination file already exists
    if check_timestamp == True and os.path.isfile(outfile_path):
        # if local file modification time is greater than URL mod time
        if (os.path.getmtime(outfile_path) > 
            time.mktime(infile.info().getdate('last-modified'))):
            infile.close()
            # exit the function and don't overwrite the local file
            return
    
    
    parser = lxml.html.HTMLParser(encoding='utf-8')
    page = lxml.html.parse(infile, parser)
    
    if insert_encoding == True:
        head = page.getroot().find('head')
        meta = lxml.etree.SubElement(head, 'meta')
        meta.set('charset', 'utf-8')   
        
    ''' TODO: make the path relative
    
    from this page:
    /home/user/Desktop/pile/bmaupinwiki/home/operating-systems/gnu-linux/rhel.html
    this link:
    /site/bmaupinwiki/home/operating-systems/gnu-linux/rhel/rhel-init-script-template
    converts to (absolute):
    /home/user/Desktop/pile/bmaupinwiki/home/operating-systems/gnu-linux/rhel/rhel-init-script-template.html
    relative: 
    rhel/rhel-init-script-template.html
    '''
    
    old_link_prefix = '{0}/'.format(urlparse.urlparse(site_url).path)
    
    '''
    The links normally look like this:
    /site/bmaupinwiki/home/operating-systems/gnu-linux/rhel/rhel-init-script-template
    so update them
    '''
    for element in page.iter('a'):
        if 'href' not in element.attrib:
            continue
        link = element.get('href')
        if link.startswith(old_link_prefix):
            element.set(
                'href',
                '{0}.html'.format(
                    os.path.join(
                        dest_path,
                        link.replace(old_link_prefix, '')
                    )
                )
            )
    
    outfile = open(outfile_path, 'w')
    outfile.write(
        lxml.etree.tostring(
            page.getroot(),
            pretty_print=True, 
            method='html',
            doctype=page.docinfo.doctype
        )
    )
    outfile.close()
    infile.close()


if __name__ == '__main__':
    main()

'''
TODO:
- Make links relative so we can move the wiki
- Update write_url_to_file and make it more modular
- Add way to delete old pages
- Download page css and images so they work too
'''
