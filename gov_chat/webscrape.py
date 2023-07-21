from langchain.document_loaders.sitemap import SitemapLoader

target_site = "https://www.maryland.gov/"
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

        if link.startswith(base_url) is False:
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
    if url not in scanned:
        print('Scan url: {}'.format(url))
        scanned.append(url)
        data = requests.get(url)
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

    f = open('sitemap.xml', 'w')
    f.write(xml)
    f.close()


# if __name__ == '__main__':
#     main()



sitemap_loader = SitemapLoader(web_path=out_file, is_local=True)
for doc in sitemap_loader.load():
    with open(Path(doc_dir,uuid.uuid4().hex+".json"),"w") as fp:
        json.dump(doc,fp,default=str)