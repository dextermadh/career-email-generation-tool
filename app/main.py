import streamlit as st
from scrape_job import ScrapeJob
from chain import Chain
from utils import clean_text
from repos import Repos
from scrape_repos import ScrapeRepos 

def streamlit_app(llm, clean_text):     
    st.title('📧 Career Email Generation Tool')
    st.write('This tool helps you to generate a cold email for job applications by scraping job postings and your Github repositories.')
    
    job_url = st.text_input('Enter the URL of the job posting: ', placeholder='https://example.com/job-posting')
    # github_username = st.text_input('Enter your Github username: ', placeholder='dextermadh')
    submit_button = st.button('Generate Email')
    
    scraper_job = ScrapeJob(job_url)
    
    if submit_button: 
        try: 
            st.write('Scraping job posting...')
            page_text = scraper_job.selenium_scrape()
            jobs = llm.extract_jobs(clean_text(page_text))
            
            st.write('Fetching repositories from Github...') 
            scraper_repos = ScrapeRepos()
            scraped_repos = scraper_repos.fetch_repos() 
            df = scraper_repos.repo_dataframe(scraped_repos)
            st.success('Repositories fetched successfully!')
            
            repos = Repos(df)
            repos.load_repos()
            
            for job in jobs: 
                skills = job.get('skills', [])
                relavant_repos = repos.query_links(skills)
                email = llm.write_email(job, relavant_repos)
                st.code(email, language='markdown')
            if not jobs: 
                st.warning('No jobs found in the provided url.')
                    
        except Exception as e: 
            st.error(f'An error occurred: {e}')
        
    

if __name__ == '__main__': 
    llm = Chain()

    st.set_page_config(page_icon='📧', page_title='Career Email Generation Tool')
    
    streamlit_app(llm, clean_text) 
    
    
    
    
