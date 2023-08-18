from langchain.document_loaders import SeleniumURLLoader
# from gov_chat.CustomSeleniumURLLoader import SeleniumURLLoader

import json
import uuid
from pathlib import Path
import re

import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document

LOADER_MAPPING:dict[str,tuple[BaseLoader,dict[str,str]]] = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


EXTENSIONS_NOT_SCANNED = [".jpg", ".png", ".pdf",".jpeg",".gif",".webp",".tiff",".bmp",".heif",".svg",".eps",".psd",".ai",".xcf",".indd"]
EXTENSIONS_NOT_SCANNED.extend(LOADER_MAPPING.keys())
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
        if url not in self.scanned:
            print('Scan url: {}'.format(url))
            self.scanned.append(url)
            #For the sitemap, we want all links, but we don't need to scan images, pdfs, etc,.
            if not any(ext in url for ext in EXTENSIONS_NOT_SCANNED):
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

def split_targets(urls:list[str])->dict[str,list[str]]:
    out:dict[str,list[str]] = {}
    out["webpage"] = []
    for url in urls:
        for ext in EXTENSIONS_NOT_SCANNED:
            if ext in url:
                if out.get(ext) is None:
                    out[ext] = [url]
                else:
                    out[ext].append(url)
                continue
            else:
                out["webpage"].append(url)
    return out
                
def download_file(url:str, file_path:Path ):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def load_single_document(file_path: str) -> list[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")

def load_documents(source_dir: Path,) -> list[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files:list[Path] = []
    for ext in LOADER_MAPPING:
        all_files.extend( source_dir.glob(f"**/*{ext}"))

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        
        for _, docs in enumerate(pool.imap_unordered(load_single_document, [f.as_posix() for f in all_files])):
            results.extend(docs)
                

    return results

def scan_downloaded_artifacts(doc_directory = "./outputs/docs",staging_folder = "staging"):
    
    parsed_docs = load_documents(Path(doc_directory,staging_folder))

    for doc in parsed_docs:
        filename = doc.metadata["source"]
        dir_name = os.path.dirname(filename)
        base_name  = os.path.basename(filename)
        metadata_path = Path(dir_name,base_name.split(".")[0]+".metadata")

        with open(metadata_path,"r") as fp:
            metadata_dict = json.load(fp)
        doc.metadata["source"] = metadata_dict["metadata"]["source"]
        file_id =uuid.uuid4().hex
        with open(Path(doc_directory,file_id+".json"),"w") as fp: 
            json.dump(doc.json(),fp,default=str)
        




def scan_sitemap(site_map_file:str,batch_count:int = 10, doc_directory="./outputs/docs"):
    
    with open(site_map_file,"r") as fp:
        targets = split_targets(json.load(fp))

    os.makedirs(doc_directory,exist_ok=True)
    for doc in SeleniumURLLoader(urls=targets["webpage"],arguments=["disable-dev-shm-usage"]).load():
            file_id =uuid.uuid4().hex
            with open(Path(doc_directory,file_id+".json"),"w") as fp:
                
                json.dump(doc.json(),fp,default=str)
    del targets["webpage"]
    staging_directory = Path(doc_directory,"staging")
    
    os.makedirs(staging_directory, exist_ok=True)
    for target_ext in targets.keys():
        for dl_target in targets[target_ext]:
            file_id =uuid.uuid4().hex
            try: 
                download_file(url=dl_target,file_path=Path(staging_directory,file_id+target_ext))
                #ensuring metadata gets saved along with file
                with open(Path(staging_directory,file_id+".metadata"),"w") as fp:
                    json.dump({
                        "metadata":{
                            "source":dl_target
                        }
                    },fp,default=str)
            except Exception as e:
                print(f"Error downloading {targets[target_ext]}")
                print(e)

    

    

    

    


if __name__ == '__main__':
    sitemap_dir = "./outputs"
    sitemap_file= "www.maryland.gov-Maryland.json"
    doc_directory = "./outputs/docs/www.maryland.gov"
    generatre_site_map(
        "https://www.maryland.gov/",
        sitemap_dir=sitemap_dir,
        sitemap_name=sitemap_file
    )
    scan_sitemap(site_map_file=Path(sitemap_dir,sitemap_file),doc_directory=doc_directory)
    scan_downloaded_artifacts(doc_directory=doc_directory)
      



# sitemap_loader = SitemapLoader(web_path=out_file, is_local=True)