from newsapi import NewsApiClient
from collections import defaultdict
import json

with open("config.json") as f:
    config=json.load(f)

class Newschannel():
    COUNTRY_CODE={"India": 'in',"USA": 'us',"Australia": "au"}
    def __init__(self,id):
        self.id=id
        
        
    @property
    def details(self):
        client=NewsApiClient(api_key=config["newsapikey"])

        det=next(filter(lambda x: x["id"]==self.id,client.get_sources()["sources"]))
        if len(det):
            return det
        return {}

    
    @staticmethod
    def get_all_srcs(*args):
        client=NewsApiClient(api_key=config["newsapikey"])
        sources=defaultdict(list)
        for arg in args:
            sources[arg]=[src['id'] for src in client.get_sources(country=Newschannel.COUNTRY_CODE.get(arg,"us"))["sources"]]
        return sources    
    
    def get_top_news(self,n,search=None):
        client=NewsApiClient(api_key=config["newsapikey"])
        topnews=client.get_top_headlines(q=search,sources=self.id)
        return topnews['articles'][:n]






        
    def __repr__(self):
        return f"Newschannel({self.id},{self.details['country']},{self.details['category']})" 





    