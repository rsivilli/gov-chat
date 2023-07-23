from langchain.document_loaders import SeleniumURLLoader

import json
import uuid
from pathlib import Path
import re

import requests
from bs4 import BeautifulSoup
import os


class SiteScanner:
    scanned:list[str] = []
    skipped_websites:list[str]= []
    safety_count:int = 500
    base_domain:str
    website:str
    def __init__(self, website:str,base_domain:str=None,safety_count:int = 500) -> None:
        self.website = website
        if self.website[-1] == "/":
            self.website = self.website[:-1]
        self.base_domain = base_domain or re.search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]",website).group(0)
        self.safety_count = safety_count
    def clean(self,a_eles):
        links = []
        skip_links = []
        for a in a_eles:
            link = a['href']
            if link.startswith('#') or link.startswith('mailto:') or link == '/':
                skip_links.append(link)
                continue

            if link.startswith('/'):
                link = '{}{}'.format(self.website, link)

            if link.startswith('http://') != True and link.startswith('https://') != True:
                link = '{}/{}'.format(self.website, link)

            if link.find(self.base_domain) == -1:
                continue

            if link not in links:
                links.append(link)

        return [links, skip_links]


    def get_next_scan_urls(self,urls):
        links = []
        for u in urls:
            if u not in self.scanned:
                links.append(u)
        return links


    def scan(self,url=None):
        if url is None:
            url = self.website
        if len(self.scanned) > self.safety_count:
            return []
        if url not in self.scanned and ".pdf" not in url and ".jpg" not in url:
            print('Scan url: {}'.format(url))
            self.scanned.append(url)
            try: 
                data = requests.get(url)
            except Exception as e:
                print("Hit an exception")
                print(e)
                return []
            soup = BeautifulSoup(data.text, 'html5lib')
            a_eles = soup.find_all('a', href=True)
            links, skip_links = self.clean(a_eles)

            next_scan_urls = self.get_next_scan_urls(links)
            print('Count next scan: {}'.format(len(next_scan_urls)))
            if len(next_scan_urls) != 0:
                for l in next_scan_urls:
                    self.scan(l)
        return self.scanned

def save_site_map(sitemap_dir:str, sitemap_name:str,site_links:list[str]):
    """
    Saves provided site_links. Will create directories if they don't exist
    """
    out_dir = Path(sitemap_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_file = Path(sitemap_dir,sitemap_name)
    with open(out_file,"w") as fp:
        json.dump(site_links,fp)

def generatre_site_map(target_domain:str, safety_count:int = 200, sitemap_dir="./outputs",sitemap_name="sitemap.json"):
    """
    Walks links within the target domain to generate and save a sitemap
    """
    scanner = SiteScanner(target_domain,safety_count=safety_count)
    links = scanner.scan()

    save_site_map(
        sitemap_dir=sitemap_dir,sitemap_name=sitemap_name,site_links=links
    )
    return links, len(links)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]   
        
def scan_sitemap(site_map_file:str,batch_count:int = 10, doc_directory="./outputs/docs"):
    urls:list[str] =[]
    lookup = {}
    with open(site_map_file,"r") as fp:
        urls = json.load(fp)
    print(f"{len(urls)} urls loaded")
    os.makedirs(doc_directory,exist_ok=True)
    
    for url in batch(urls,int(batch_count)):
        #Selenium URLLoader doesn't support lazy_load so this basically grabs all pages into memory. We don't want to do that
        for doc in SeleniumURLLoader(urls=url).load():
            file_id =uuid.uuid4().hex
            lookup[doc.metadata.get("source")] = file_id
            with open(Path(doc_directory,file_id+".json"),"w") as fp:
                
                json.dump(doc.json(),fp,default=str)
    with open(Path(doc_directory,"..","lookup.json"),"w") as fp:
        json.dump(lookup,fp)
    return lookup
    

if __name__ == '__main__':
    sitemap_dir = "./outputs"
    sitemap_file= "sitemap.json"
    generatre_site_map(
        "https://www.maryland.gov/",
        sitemap_dir=sitemap_dir,
        sitemap_name=sitemap_file
    )
    scan_sitemap(site_map_file=Path(sitemap_dir,sitemap_file))
      



# sitemap_loader = SitemapLoader(web_path=out_file, is_local=True)