import streamlit as st
from scrape_job import ScrapeJob
from chain import Chain
from utils import clean_text
from repos import Repos
from scrape_repos import ScrapeRepos
from scrape_CV import extract_text_from_pdf
import urllib.parse

def streamlit_app(llm, clean_text):     
    st.title('📧 Career Email Generation Tool')
    st.write('This tool helps you to generate a cold email for job applications by scraping job postings and your Github repositories.')
    
    job_url = st.text_input('Enter the URL of the job posting: ', placeholder='https://example.com/job-posting')
    github_username = st.text_input('Enter your Github username: ', placeholder='dextermadh')
    CV_file = st.file_uploader('Upload your CV (PDF)', type='pdf')
    submit_button = st.button('Generate Email')
    
    scraper_job = ScrapeJob(job_url)
    
    if CV_file: 
        CV_text = extract_text_from_pdf(CV_file)
         
    
    if submit_button: 
        try: 
            page_text = scraper_job.selenium_scrape()
            jobs = llm.extract_jobs(clean_text(page_text))
            
            if github_username != '':
                scraper_repos = ScrapeRepos(github_username)
                scraped_repos = scraper_repos.fetch_repos() 
                df = scraper_repos.repo_dataframe(scraped_repos)
            
                repos = Repos(df)
                repos.load_repos()
            
            for job in jobs: 
                skills = job.get('skills', [])
                if github_username != '':
                    relavant_repos = repos.query_links(skills) 
                else: 
                    relavant_repos = []
                CV_info = llm.extract_CV_info(cv_text=CV_text)
                email = llm.write_email(job, relavant_repos, CV_info)
                st.code(email, language='markdown')
                
                if repos:
                    repos.delete_collection()
                
                recipient = urllib.parse.quote(job['recruiter_email'])
                subject = urllib.parse.quote(f"Application for {job['role']}")
                body = urllib.parse.quote(email)
                
                params = {
                    'subject': subject, 
                    'body': body
                }
                query_string = urllib.parse.urlencode(params)
                
                mail_to_url = f"mailto:{recipient}?{query_string}"
                
                st.link_button('Send Email', mail_to_url)
                
                                
            if not jobs: 
                st.warning('No jobs found in the provided url.')
                    
        except Exception as e: 
            st.error(f'An error occurred: {e}')
        
    

if __name__ == '__main__': 
    llm = Chain()

    st.set_page_config(page_icon='📧', page_title='Career Email Generation Tool')
    
    streamlit_app(llm, clean_text) 
    
    
    
    
