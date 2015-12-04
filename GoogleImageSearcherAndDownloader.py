# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 13:41:40 2015

@author: qyou
"""

import os
import urllib
import re
import requests

class WrongArgumentTypeException(Exception):
    pass

def check_image_url(imgurl, schemas=None, formats=None):
    imgurl = imgurl.lower()
    schemas = schemas or ("http", "https")
    formats = formats or ('jpg', 'png', 'gif')
    if any(map(imgurl.startswith, schemas)):
        if any(map(imgurl.endswith, formats)):
            return True
    return False    

def download(resource_url, save_dir=None, filename=None, N=100):
    save_dir = save_dir or '.'
    filename = filename or resource_url.split('/')[-1]
    filepath = os.path.join(save_dir, filename)
    i = 0
    if os.path.exists(filepath):
        i+=1
        filep, ext = os.path.splitext(filepath)
        filepath = filep+str(i)+ext
        
    print "Start downloading ", resource_url
#    def reporthook(blocks_read, block_size, total_size):
#        if not blocks_read:    
#            s = '-' * N
#            return
#        if total_size <= 0:
#            s = '*' * blocks_read
#        else:
#            read_blocks_norm = blocks_read * N * block_size / total_size
#            s = '*' * read_blocks_norm + (N-read_blocks_norm) * '-'
#        print s
    try:
        urllib.urlretrieve(resource_url, filepath)
        print "Finish downloading ", resource_url
    except:
        "Error to download ", resource_url

class GoogleImageSearcher(object):
    SEARCHER_TEMPLATE = r'https://www.google.com.hk/search?q=%s&newwindow=1&safe=strict&tbm=isch&tbo=u&source=univ&start=%d'
    HEADERS = {
        "host":"www.google.com.hk", 
        "schema":"scheme", 
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "x-chrome-variations": "CKW2yQEIqbbJAQjBtskB"
        }
    IS_OVER = False
    def __init__(self, keywords, start=0):
        if isinstance(keywords, str):
            keywords = keywords.split(' ')
        if not isinstance(keywords, (tuple, list)):
            raise WrongArgumentTypeException
        query_str = '+'.join(keywords)
        self.url = self.SEARCHER_TEMPLATE % (query_str, start)
    def get_entry_html(self):
        response = requests.get(self.url, headers=self.HEADERS)
        unicode_text = response.text
        return unicode_text
    
    def parse_image_urls(self, html=None):
        if html is None:
            html = self.get_entry_html()
        pattern = re.compile(ur"imgres\?imgurl=(?P<imgurl>\S+?)&amp;imgrefurl=")
        img_urls = []        
        for m in pattern.finditer(html):
            if m is None:
                self.IS_OVER = True
                break
            imgurl = m.group('imgurl')
            if check_image_url(imgurl):
                img_urls.append(imgurl)
        return img_urls
    
    def download_images(self, save_dir=None, img_urls=None):
        html = self.get_entry_html()
        img_urls = self.parse_image_urls(html)
        for imgurl in img_urls:
            download(imgurl, save_dir=save_dir)
            
