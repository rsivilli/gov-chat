from CustomSeleniumURLLoader import SeleniumURLLoader
import uuid
from pathlib import Path
import requests
import json

urls = [
        "https://www.mylongview.com/DocumentCenter/View/1808/2019-to-2020-Complete-Budget-Document-PDF"
]



for doc in SeleniumURLLoader(urls=urls).load():
            file_id = "pdf_test"
            with open(Path("outputs",file_id+".json"),"w") as fp:
                
                json.dump(doc.json(),fp,default=str)