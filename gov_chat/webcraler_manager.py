import django


import os
from gov_chat_management import settings as app_settings

from django.conf import settings
import datetime
from django.utils.timezone import now

from datetime import timedelta
import re

from pathlib import Path

from webscrape import save_site_map, SiteScanner, scan_sitemap

from splitandstore import split_and_load_docs

if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE']= 'gov_chat_management.settings'
    django.setup()

from customer_management.models import Website

def get_sitemap_targets(time_delta_seconds:int =3600*24):
    current_time = now()
    time_threshold = current_time - timedelta(seconds=time_delta_seconds)
    out = set()
    #all websites that that are flagged to create a sitemap but have never been scanned
    out.update(Website.objects.filter(create_site_map=True,site_map_last_scanned=None ))
    #all websites that are flagged to be maintained, and have not be scanned in the timedelta
    out.update(Website.objects.filter(update_site_map=True,site_map_last_scanned__lt=time_threshold ))
    return out

def get_root_name(site:Website):
     return re.search(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]",site.base_site).group(0)

def get_index_targets(time_delta_seconds:int = 3600*24):
    current_time = now()
    time_threshold = current_time - timedelta(seconds=time_delta_seconds)
    out = set()
    out.update(Website.objects.filter(site_last_indexed=None,site_map__isnull=False ))
    out.update(Website.objects.filter(site_last_indexed__lt=time_threshold,site_map__isnull=False ))
    return out


     
def save_and_update_sitemap(base_site:str,sitemap:list[str], s3_bucket:str =None, sitemap_dir="./outputs"):
    website = Website.objects.filter(base_site=base_site).first()
    
    if website is None:
            raise ValueError(f"Could not find website {base_site} in db")
    root_name = get_root_name(website)
    file_name = f"{root_name}-{website.customer.name}.json"

    if s3_bucket is None:
        
        
        save_site_map(sitemap_dir=sitemap_dir,sitemap_name=file_name,site_links=sitemap)
        
    else:
        raise NotImplementedError("S3 upload support for sitemaps has not been implemented yet")

    website.site_map_last_scanned = now()
    website.site_map = Path(sitemap_dir,file_name).as_posix()

    website.save()

def index_site(base_site, batch_count:int=10, base_doc_directory="./outputs/docs"):
     website = Website.objects.filter(base_site=base_site).first()
     if website is None:
        raise ValueError(f"Could not find website {base_site} in db")
     if website.site_map is None:
        print(f"Warning: could not find sitemap for {base_site}")
        return     
    
     root_name = get_root_name(website)
     output_directory = Path(base_doc_directory,root_name)
     os.makedirs(output_directory, exist_ok=True)
     scan_sitemap(site_map_file=website.site_map,doc_directory=output_directory,batch_count=batch_count)
     
     website.site_doc_staging = output_directory.as_posix()
     website.save()

def generate_site_map(target_domain:str, safety_count:int=200, sitemap_dir="./outputs"):
    scanner = SiteScanner(target_domain,safety_count=safety_count)
    links = scanner.scan()

    save_and_update_sitemap(
         target_domain,links,sitemap_dir=sitemap_dir
    )
    return links, len(links)


def update_vs(base_site:str,chunk_size:int=500,chunk_overlap:int=0,clean_collection:bool=True):
    website = Website.objects.filter(base_site=base_site).first()
    if website is None:
        raise ValueError(f"Could not find website {base_site} in db")
  
    split_and_load_docs(
        document_dir=website.site_doc_staging,
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        clean_collection=clean_collection,
        collection_name=[site.name for site in website.target_collections.all()]
        )
    website.save()

if __name__ == "__main__":
    for site in get_sitemap_targets():
        generate_site_map(site.base_site)

    updated = []
    for site in get_index_targets():
        index_site(site.base_site)
        update_vs(site.base_site)
        site.site_last_indexed = now()
        site.save()



