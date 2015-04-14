import datetime
import os
import os.path
import shutil
import sys
import tempfile
import uuid
import zipfile

import lxml.etree


class Epub(object):
    CONTENT_CONTAINER = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
'''
    CONTENT_MIMETYPE = 'application/epub+zip'
    FILENAME_CONTAINER = 'container.xml'
    FILENAME_CONTENT = 'content.opf'
    FILENAME_MIMETYPE = 'mimetype'
    FILENAME_TEXT_TEMPLATE = 'Section{0:04d}.xhtml'
    FILENAME_TOC = 'toc.ncx'
    FOLDER_IMAGES = 'Images'
    FOLDER_METAINF = 'META-INF'
    FOLDER_OEBPS = 'OEBPS'
    FOLDER_TEXT = 'Text'
    TEMPLATE_CONTENT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>{title}</dc:title>
        <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uuid}</dc:identifier>
        <dc:date opf:event="modification">{date}</dc:date>
    </metadata>
    <manifest>
        <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
    </manifest>
    <spine toc="ncx">
    </spine>
    <guide/>
</package>
'''
    TEMPLATE_TOC = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="urn:uuid:{uuid}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle>
        <text>{title}</text>
    </docTitle>
    <navMap>
    </navMap>
</ncx>
'''
    TMPDIR_PREFIX = '/tmp/python-epub-'
    
    def __init__(self, title, dest_path):
        self.pages = []
        self.dest_path = dest_path
        self.title = title
    
    def addBasicImagePage(self, title = '', heading = '', image_path = '', text = ''):
        page = EpubBasicImagePage(title, heading, image_path, text)
        self.pages.append(page)
    
    def addPage(self, title = '', heading = '', text = ''):
        page = EpubPage(title, heading, text)
        self.pages.append(page)
    
    def build(self):
        # keep track of files and folders to add for zipping and remove for cleanup
        files_to_add = []
        folders_to_add = []
        
        try:
            tmp_path = tempfile.mkdtemp(prefix=Epub.TMPDIR_PREFIX)
            os.mkdir(os.path.join(tmp_path, Epub.FOLDER_METAINF))
            folders_to_add.append(
                os.path.join(tmp_path, Epub.FOLDER_METAINF))
            os.mkdir(os.path.join(tmp_path, Epub.FOLDER_OEBPS))
            folders_to_add.append(os.path.join(tmp_path, Epub.FOLDER_OEBPS))
            os.mkdir(
                os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_IMAGES))
            folders_to_add.append(
                os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_IMAGES))
            os.mkdir(
                os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_TEXT))
            folders_to_add.append(
                os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_TEXT))
        except OSError, error:
            sys.exit('OSError: %s' % (error))
        
        # add the mimetype file
        mimetype_file = open(
            os.path.join(tmp_path, Epub.FILENAME_MIMETYPE), 'w')
        files_to_add.append(os.path.join(tmp_path, Epub.FILENAME_MIMETYPE))
        mimetype_file.write(Epub.CONTENT_MIMETYPE)
        mimetype_file.close()
        
        # add the container.xml file
        container_file = open(
            os.path.join(
                tmp_path, Epub.FOLDER_METAINF, Epub.FILENAME_CONTAINER), 'w')
        files_to_add.append(
            os.path.join(
                tmp_path, Epub.FOLDER_METAINF, Epub.FILENAME_CONTAINER))
        container_file.write(Epub.CONTENT_CONTAINER)
        container_file.close()
        
        # prepare the content metadata
        this_uuid = str(uuid.uuid4())
        content_file_root = lxml.etree.fromstring(
            Epub.TEMPLATE_CONTENT.format(
                title=self.title,
                date=datetime.datetime.now().strftime('%Y-%m-%d'),
                uuid=this_uuid
            )
        )
        manifest = content_file_root.find(
            '{{{0}}}manifest'.format(content_file_root.nsmap[None]))
        spine = content_file_root.find(
            '{{{0}}}spine'.format(content_file_root.nsmap[None]))
        
        # prepare the toc metadata
        toc_file_root = lxml.etree.fromstring(
            Epub.TEMPLATE_TOC.format(
                title=self.title,
                uuid=this_uuid
            )
        )
        navmap = toc_file_root.find(
            '{{{0}}}navMap'.format(toc_file_root.nsmap[None]))
        
        # build the pages
        page_number = 1
        for page in self.pages:
            # add the image
            if hasattr(page, 'image_path'):
                shutil.copy2(
                    page.image_path,
                    os.path.join(
                        tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_IMAGES, 
                        page.image_filename)
                )
                files_to_add.append(
                    os.path.join(
                        tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_IMAGES, 
                        page.image_filename))
                
                # add the image content metadata
                item = lxml.etree.Element('item')
                item.set('href', os.path.join(
                    Epub.FOLDER_IMAGES, page.image_filename))
                item.set('id', 'x{0}'.format(page.image_filename))
                item.set('media-type', 'image/jpeg')
                manifest.append(item)
            
            # add the page
            page_filename = Epub.FILENAME_TEXT_TEMPLATE.format(page_number)
            
            page_file = open(
                os.path.join(
                    tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_TEXT, page_filename
                ), 
                'w'
            )
            files_to_add.append(os.path.join(
                tmp_path, Epub.FOLDER_OEBPS, Epub.FOLDER_TEXT, page_filename
            ))
            page_file.write(page.getContent())
            page_file.close()
            
            # add the page content metadata
            item = lxml.etree.Element('item')
            item.set('href', os.path.join(Epub.FOLDER_TEXT, page_filename))
            item.set('id', page_filename)
            item.set('media-type', 'application/xhtml+xml')
            manifest.append(item)
            
            itemref = lxml.etree.Element('itemref')
            itemref.set('idref', page_filename)
            spine.append(itemref)
            
            # add the page toc metadata
            navpoint = lxml.etree.Element('navpoint')
            navpoint.set('id', 'navPoint-{0}'.format(page_number))
            navpoint.set('playOrder', str(page_number))
            navlabel = lxml.etree.SubElement(navpoint, 'navLabel')
            text = lxml.etree.SubElement(navlabel, 'text')
            text.text = page.heading
            content = lxml.etree.SubElement(navpoint, 'content')
            content.set('src', os.path.join(Epub.FOLDER_TEXT, page_filename))
            navmap.append(navpoint)
            
            page_number += 1
        
        # add the content.opf file
        content_file = open(
            os.path.join(
                tmp_path, Epub.FOLDER_OEBPS, Epub.FILENAME_CONTENT), 'w')
        files_to_add.append(
            os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FILENAME_CONTENT))
        content_file.write(lxml.etree.tostring(
            content_file_root,
            encoding='utf-8',
            standalone='yes',
            xml_declaration=True,
            pretty_print=True))
        content_file.close()
        
        # add the toc.ncx file
        toc_file = open(
            os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FILENAME_TOC), 'w')
        files_to_add.append(
            os.path.join(tmp_path, Epub.FOLDER_OEBPS, Epub.FILENAME_TOC))
        toc_file.write(lxml.etree.tostring(
            toc_file_root,
            encoding='utf-8',
            standalone='no',
            xml_declaration=True,
            pretty_print=True))
        toc_file.close()

        # change to the temporary folder so we can add stuff relative to the zip file
        os.chdir(tmp_path)
        # make the zip file
        zoutfile = zipfile.ZipFile(
            os.path.join(self.dest_path, self.title + '.epub'), 'w')
        for folder in folders_to_add:
            # split the tmp_path part off of the absolute path
            zoutfile.write(os.path.relpath(folder, tmp_path))
        for file in files_to_add:
            zoutfile.write(os.path.relpath(file, tmp_path))
        zoutfile.close()
        
        # clean up after ourselves
        for file in files_to_add:
            os.remove(file)
        
        # remove folders in reverse order they were added
        folders_to_add.reverse()
        for folder in folders_to_add:
            os.rmdir(folder)
            
        # finally, remove the temp folder
        os.rmdir(tmp_path)
        

class EpubPage(object):
    BASIC_PAGE_TEMPLATE = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
</head>

<body>
  <h2>{heading}</h2>

  <p>{text}</p>
</body>
</html>
'''
    def __init__(self, title = '', heading = '', text = ''):
        self.title = title
        self.heading = heading
        self.text = text
        
    def getContent(self):
        return EpubBasicImagePage.BASIC_PAGE_TEMPLATE.format(
            title = self.title,
            heading = self.heading,
            text = self.text
        )

class EpubBasicImagePage(EpubPage):
    BASIC_IMAGE_PAGE_TEMPLATE = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
</head>

<body>
  <h2>{heading}</h2>

  <p><img alt="{image}" src="../Images/{image}" /><br/>

  {text}</p>
</body>
</html>
'''
    def __init__(self, title = '', heading = '', image_path = '', text = ''):
        image_basepath, self.image_filename = os.path.split(image_path)
        self.title = title
        self.heading = heading
        if os.path.isfile(image_path):
            self.image_path = image_path
        else:
            sys.stderr('ERROR: Image {0} does not exist\n'.format(image_path))
        self.text = text
        
    def getContent(self):
        return EpubBasicImagePage.BASIC_IMAGE_PAGE_TEMPLATE.format(
            title = self.title,
            heading = self.heading,
            image = self.image_filename,
            text = self.text
        )

'''
myEpub = Epub('myEpub title', '/home/bmaupin/Desktop')
myEpub.addBasicImagePage('Page 1 title', 'Page 1 heading', '/home/bmaupin/Desktop/1.jpg', 'Some text.')
myEpub.addBasicImagePage('Page 2 title', 'Page 2 heading', '/home/bmaupin/Desktop/2.jpg, 'Some text.<br />Such fancy.')
myEpub.build()
'''
