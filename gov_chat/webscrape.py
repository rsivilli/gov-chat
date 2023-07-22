from langchain.document_loaders.sitemap import SitemapLoader
from langchain.document_loaders import SeleniumURLLoader
target_site = "https://www.maryland.gov/"
base_domain = "maryland.gov"
out_file = "./outputs/sitemap.xml"
doc_dir = "./outputs/docs"
import json
import uuid
from pathlib import Path

def generate_sitemap(target_site:str, output_location:str):
    pass

#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

website =target_site
base_url = website
if website.endswith('/'):
    base_url = website[:-1]

scanned = []

safety_count = 500


def clean(a_eles):
    links = []
    skip_links = []
    for a in a_eles:
        link = a['href']
        if link.startswith('#') or link.startswith('mailto:') or link == '/':
            skip_links.append(link)
            continue

        if link.startswith('/'):
            link = '{}{}'.format(base_url, link)

        if link.startswith('http://') != True and link.startswith('https://') != True:
            link = '{}/{}'.format(base_url, link)

        if link.find(base_domain) == -1:
            continue

        if link not in links:
            links.append(link)

    return [links, skip_links]


def get_next_scan_urls(urls):
    links = []
    for u in urls:
        if u not in scanned:
            links.append(u)
    return links


def scan(url):
    if len(scanned) > safety_count:
        return []
    if url not in scanned and ".pdf" not in url and ".jpg" not in url:
        print('Scan url: {}'.format(url))
        scanned.append(url)
        try: 
            data = requests.get(url)
        except Exception as e:
            print("Hit an exception")
            print(e)
            return []
        soup = BeautifulSoup(data.text, 'html5lib')
        a_eles = soup.find_all('a', href=True)
        links, skip_links = clean(a_eles)

        next_scan_urls = get_next_scan_urls(links)
        print('Count next scan: {}'.format(len(next_scan_urls)))
        if len(next_scan_urls) != 0:
            for l in next_scan_urls:
                scan(l)
    return scanned


def main():
    links = scan(website)

    urls = ''
    for l in links:
        urls += f"""
    <url>
      <loc>{l}</loc>
      <lastmod>2022-07-27T02:24:08.242Z</lastmod>
      <priority>0.6</priority>
    </url>
        """

    xml = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {urls}
</urlset>
    """

    # f = open(out_file, 'w')
    # f.write(xml)
    # f.close()
    with open(out_file,"w") as fp:
        json.dump(links,fp)


if __name__ == '__main__':
    main()



# sitemap_loader = SitemapLoader(web_path=out_file, is_local=True)
    
    
    urls:list[str] =[]
    with open(out_file,"r") as fp:
        urls = json.load(fp)
    print(f"{len(urls)} urls loaded")
    loader = SeleniumURLLoader(urls=urls)
    
    for url in urls:
        #Selenium URLLoader doesn't support lazy_load so this basically grabs all pages into memory. We don't want to do that
        for doc in SeleniumURLLoader(urls=[url]).load():
            with open(Path(doc_dir,uuid.uuid4().hex+".json"),"w") as fp:
                
                json.dump(doc.json(),fp,default=str)
        break