import os
from serpapi import GoogleSearch
import json

def search_entity(entity, query_input):
    try:
        search_query = f"{query_input} {entity}"
        
        #SerpAPI search
        search = GoogleSearch({
            "q": search_query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 5  
        })
        
        results = search.get_dict()
        
        #Top 5 organic results
        if "organic_results" in results:
            return [
                {
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "link": result.get("link", "")
                }
                for result in results["organic_results"][:5]
            ]
        return []
        
    except Exception as e:
        print(f"Error searching for {entity}: {str(e)}")
        return []