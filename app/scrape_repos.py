import requests 
import pandas as pd 

class ScrapeRepos: 
    def __init__(self, username = 'dextermadh'):
        self.username = username 
        self.url = f'https://api.github.com/users/{username}/repos'
    
    def fetch_repos(self): 
        response = requests.get(self.url)
        
        if response.status_code == 200: 
            repos = response.json()
        else: 
            raise Exception(f'Failed to fetch repositories for user {self.username}. Status code: {response.status_code}')
        return repos
    
    def repo_dataframe(self, repos):
        repo_dict = {}
        
        for repo in repos: 
            repo_dict[repo['name']] = {
                'url': repo['html_url'], 
                'language': repo['language']
            }
        
        df = pd.DataFrame.from_dict(repo_dict, orient='index').reset_index().rename(columns={'index': 'repo_name'})
        df = df.dropna()
        df.to_csv('app/data/repos.csv', index=False)
        
        return df 
    
    