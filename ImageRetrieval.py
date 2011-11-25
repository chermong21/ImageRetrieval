#!/usr/bin/python
'''
Created on 2011-9-11

@author: You Qiang
'''

'''
@note    
Need extra modules as follows:
    BeautifulSoup, PIL
'''
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import chardet
import urllib2
class PageInitializer(object):
    def __init__(self, url):
        '''
        Constructor
        '''
        self.url = url
    def getHtml(self):
        html = ""
        try:
            request = urllib2.urlopen(self.url)
            html = request.read()
        except:
            print "get html source failed!"
        return html
    
    def detectEncoding(self):
        html = self.getHtml()
        encodingInfo = chardet.detect(html)
        return encodingInfo['encoding']       
        
#==============================================
#        class: ImageUrlLister
#==============================================
class ImageUrlLister(PageInitializer):
    def __init__(self, url):
        PageInitializer.__init__(self, url)
        self.url = url
    def listImageUrls(self):
        html = self.getHtml()
        soup = BeautifulSoup(html)
        imageSoups = soup.findAll('img')
        imageUrls = [s['src'] for s in imageSoups]
        return set(imageUrls)

#====================================
#        class: ImageInfo 
#        using PIL.Image
#====================================
import Image
from cStringIO import StringIO
class ImageInfo(object):
    def __init__(self, url):
        imFile = urllib2.urlopen(url)
        imStr = StringIO(imFile.read())
        self.im = Image.open(imStr)
    def __str__(self):
        print self.im.info
        print self.im.size
        print self.im.format
    def getSize(self):
        return self.im.size
    def getFormat(self):
        return self.im.format

#==============================================
#    Main function
#==============================================
import sys
def help():
    print 'python ImageRetrieval.py url [sizeX] [sizeY] [folderPath]'
def main(): 
    if len(sys.argv) < 2:
        help()
    else:
        url = sys.argv[1]
        sizeX = 0
        sizeY = 0
        imagefolder = r'.'  
        if len(sys.argv) == 2: 
            sizeX = 0
            sizeY = 0
            imagefolder = r'.'           
        elif len(sys.argv) == 3 :
            sizeX = sys.argv[2]
        elif len(sys.argv) == 4:
            sizeX = sys.argv[2]
            sizeY = sys.argv[3]
        else:
            sizeX = sys.argv[2]
            sizeY = sys.argv[3]
            imagefolder = sys.argv[4]
        lister = ImageUrlLister(url)
        imageUrls = lister.listImageUrls()
        i=0
        for imageUrl in imageUrls:
            info = ImageInfo(imageUrl)
            size = info.getSize()
            print int(size[0]) >=  int(sizeX) and int(size[1]) >= int(sizeY)
            if int(size[0]) >=  int(sizeX) and int(size[1]) >= int(sizeY):
                i+=1
                imagepath = imagefolder+'/'+str(i)+'.'+info.im.format
                info.im.save(imagepath, info.im.format)
                print '%s downloaded successfully!' % imagepath
     
        
#==================================
#    MAIN Entry point
#==================================   
if __name__ == '__main__':
    main()