#!/usr/bin/env python3
"""
DAT Detective — Search Engine Instant Indexing & Ping Utility
Pings Google, Bing, and submits 45 URLs via IndexNow API for instant crawling.
"""

import urllib.request
import json
import xml.etree.ElementTree as ET

SITE_HOST = 'www.datdetective.com'
SITEMAP_URL = f'https://{SITE_HOST}/sitemap.xml'
INDEXNOW_KEY = 'c7a8b9f1d2e34567890abcdef1234567'
KEY_LOCATION = f'https://{SITE_HOST}/{INDEXNOW_KEY}.txt'

def ping_google():
    url = f'https://www.google.com/ping?sitemap={SITEMAP_URL}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'DAT-Detective-PingBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f'[Google Ping] Status: {resp.status}')
            return True
    except Exception as e:
        print(f'[Google Ping] Notice: {e}')
        return False

def ping_bing():
    url = f'https://www.bing.com/ping?sitemap={SITEMAP_URL}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'DAT-Detective-PingBot/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f'[Bing Ping] Status: {resp.status}')
            return True
    except Exception as e:
        print(f'[Bing Ping] Notice: {e}')
        return False

def submit_indexnow():
    try:
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            tree = ET.fromstring(f.read())
        
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        url_list = [loc.text for loc in tree.findall('.//sm:loc', ns)]
        
        payload = {
            'host': SITE_HOST,
            'key': INDEXNOW_KEY,
            'keyLocation': KEY_LOCATION,
            'urlList': url_list
        }
        
        req = urllib.request.Request(
            'https://api.indexnow.org/indexnow',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f'[IndexNow Submission] Submitted {len(url_list)} URLs. Status: {resp.status}')
            return True
    except Exception as e:
        print(f'[IndexNow Submission] Notice: {e}')
        return False

if __name__ == '__main__':
    print(f'Starting Search Engine Notification for {SITE_HOST}...')
    ping_google()
    ping_bing()
    submit_indexnow()
    print('Notification routine finished.')
