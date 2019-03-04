# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os, re
import sys, traceback  


L = [
'http://salery.livejournal.com/2006',
'http://salery.livejournal.com/2007',
'http://salery.livejournal.com/2008',
'http://salery.livejournal.com/2009',
'http://salery.livejournal.com/2010',
'http://salery.livejournal.com/2011',
'http://salery.livejournal.com/2012',
'http://salery.livejournal.com/2013',
'http://salery.livejournal.com/2014',
'http://salery.livejournal.com/2015',
'http://salery.livejournal.com/2016',
'http://salery.livejournal.com/2017',
'http://salery.livejournal.com/2018',
'http://salery.livejournal.com/2019'
]

def get_post_urls_monthly():
  #returns a list of lj monthly entries links
    post_urls = []
    try:
        for link in L:
            r = requests.get(link, 'html.parser')
            soup = BeautifulSoup(r.content, 'html.parser')
            for link in soup.find_all('td', class_='caption', align='right'):
                post_link = link.a.get('href')           
                post_urls.append(post_link)
        return post_urls
    except Exception:
        print(traceback.format_exception(*sys.exc_info())[1])
        input()        


def get_post_urls(): 
  #returns a list of all lj links    
    try:
        links = []
        post_urls = get_post_urls_monthly()
        for url in post_urls:
            r = requests.get(url, 'html.parser')
            soup = BeautifulSoup(r.content, 'html.parser')
            for i in soup.find_all('dd'):
                link = i.a.get('href')
                links.append(link)
        return links
    except Exception:
        print(traceback.format_exception(*sys.exc_info())[1])
        input()


def write_posts():
  #writes down all lj posts to txt file
    f = open('/home/o/python/Volkov/lj.txt', 'w')
    posts_urls = get_post_urls()
    try: 
        for link in posts_urls:
            r = requests.get(link, 'html.parser')
            soup = BeautifulSoup(r.content, 'html.parser')
        #1. write post header + date
            h = soup.find('td', class_='caption post-title').text 
            if h == '':
                h = 'No subject'

            d = (
                  soup.find('table', class_='s2-entrytext')
                  .find('td', align='right', class_='index')
                  .text
                )
            
            t = (
                  soup.find('table', class_='entrybox') 
                  .find('td', colspan='2')
                  .text
                )
            
            f.write('\n' + h + '\n' + d + link + t + '\n\n\n')

    except Exception:
        print(traceback.format_exception(*sys.exc_info())[1])
        input()


write_posts()

