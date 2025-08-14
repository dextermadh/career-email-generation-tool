from langchain_groq import ChatGroq 
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv() 

class Chain: 
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model='openai/gpt-oss-120b'
        )
    
    def extract_jobs(self, cleaned_text): 
        extract_prompt = PromptTemplate.from_template(
            '''
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON. Output Should be valid JSON not a LIST or DICT.
            ### VALID JSON (NO PREAMBLE): 
       
            '''
        )
        
        chain_extract = extract_prompt | self.llm 
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        
        try: 
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e: 
            raise e('context too big. unable to parse the output')
        return res if isinstance(res, list) else [res]  
    
    def write_email(self, job, repos): 
        email_prompt = PromptTemplate.from_template(
            '''
                ### JOB DESCRIPTION:
                {job_description}
                
                ### INSTRUCTION:
                You are Madhuka Abhishek Wijesundara, a software engineering undergraduate at Open University of Sri Lanka,
                
                ### Your information: 
                degree - Bachelor of Software Engineering (Hons)
                gpa - 3.36/4.0
                phone number - +94710928025
                email - madhukaabhishek.business@gmail.com
                
                You are passionate about Machine Learning and AI, and you have hand on experience in Machine Learning,
                Deep Learning, and Natural Language Processing. You are currently seeking an internship opportunity in the field of AI/ML.
                Your job is to write a cold email to the hiring team regarding the job mentioned above describing the capability of you.
                Also add the most relevant ones from the following repositories to showcase your projects: {repo_list} (Only include projects that you think that good for this role). 
                Remember you are Madhuka Abhishek, a software engineering undergraduate at Open University of Sri Lanka. 
                Do not provide a preamble. Make the email simple and more human-like. 
                
                ### Sugeested Email Format:
                Dear Hiring Team, 

                I'm currently pursuing a bachelor's degree in software engineering at the Open University of Sri Lanka, and I'm interested in applying for (position) at (the company). 

                I have a solid foundation in Natural Language Processing (NLP), Deep Learning and Machine Learning. I'm available for a full time internship. 

                I have attached my CV for your review. I would appreciate the opportunity to contribute to your team.

                Find my work:
                madhukaabhishek.vercel.app

                Sincerely,
                L.B.D.M.A. Wijesundara
                +94710928025
                madhukaabhishek.business@gmail.com

                
                ### EMAIL (NO PREAMBLE):  
                
                ### IF NO REPOSITORIES ARE PROVIDED, DO NOT MENTION ANY REPOSITORIES IN THE EMAIL.
                
                ### IF You cannot write an email, just return "I cannot write an email for this job."
                ### DO NOT RETURN ANYTHING ELSE.
            '''
        )
        
        chain_email = email_prompt | self.llm 
        res = chain_email.invoke({'job_description': str(job), 'repo_list': repos})
        return res.content