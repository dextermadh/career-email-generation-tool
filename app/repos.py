import chromadb
import pandas as pd

class Repos: 
    def __init__(self, data):
        self.data = data
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name='repos')
        
    def load_repos(self): 
        if not self.collection.count(): 
            for _, row in self.data.iterrows(): 
                self.collection.add(
                    ids=[row["repo_name"]],
                    documents=[f"Repository: {row['repo_name']}, Language: {row['language']}, URL: {row['url']}"],
                    metadatas=[{
                        "name": row["repo_name"],
                        "url": row["url"],
                        "language": row["language"]
                    }]
                )
    
    def query_links(self, skills): 
        return self.collection.query(
            query_texts=skills,
            n_results=5
        ).get('metadatas', [])
        
    def delete_collection(self): 
        self.chroma_client.delete_collection(name="repos")

