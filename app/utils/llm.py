import os
import groq
from typing import List, Dict

def process_with_llm(search_results: List[Dict], entity: str, query_input: str) -> str:
    client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    context = "\n\n".join([  #Combine each search result into context
        f"Title: {result['title']}\nSnippet: {result['snippet']}\nURL: {result['link']}"
        for result in search_results
    ])
    
    #Prepare the prompt based on dynamic user input
    prompt = f"""
    Based on the following search results for {entity}, answer the query: "{query_input}"
    
    Search Results:
    {context}
    
    Provide the most relevant and concise information. If no relevant information is found, respond with "Information not found."
    Do not include any fillers in your response, directly start with the answer for the given query.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="mixtral-8x7b-32768",  
            temperature=0.1,
            max_tokens=150
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error processing with LLM for {entity}: {str(e)}")
        return "Error processing with LLM"