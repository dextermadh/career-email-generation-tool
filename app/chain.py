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
            following keys: `role`, `experience`, `skills`, `recruiter_email` and `description`.
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
    
    def extract_CV_info(self, cv_text): 
        extract_prompt = PromptTemplate.from_template(
            '''
                You are an AI assistant that extracts structured information from resumes or CVs.  

                ### Rules
                - Read the provided CV text carefully.
                - Always return a **valid JSON object**.
                - Do not include explanations or extra commentary.
                - If some fields are missing, return them as null or an empty string.
                - Extract as much detail as possible while following the schema.

                ### JSON Schema
                {{
                "name": "string",
                "contact": {{
                    "email": "string",
                    "phone": "string",
                    "linkedin": "string",
                    "github": "string",
                    "location": "string"
                }},
                "summary": "string",
                "skills": ["string"],
                "education": [
                    {{
                    "degree": "string",
                    "field_of_study": "string",
                    "institution": "string",
                    "start_date": "string",
                    "end_date": "string"
                    }}
                ],
                "experience": [
                    {{
                    "job_title": "string",
                    "company": "string",
                    "start_date": "string",
                    "end_date": "string",
                    "responsibilities": ["string"]
                    }}
                ],
                "projects": [
                    {{
                    "name": "string",
                    "description": "string",
                    "technologies": ["string"],
                    "link": "string"
                    }}
                ],
                "certifications": [
                    {{
                    "name": "string",
                    "issuer": "string",
                    "date": "string"
                    }}
                ],
                "languages": ["string"]
                }}

                ### Input CV Text:
                <<<
                {CV_TEXT}
                >>>

            '''
        )
        
        chain_extract = extract_prompt | self.llm 
        res = chain_extract.invoke(input={'CV_TEXT': cv_text})
        
        try: 
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e: 
            raise e('context too big. unable to parse the output')
        return res if isinstance(res, list) else [res]  
        
        
    
    def write_email(self, job, repos, cvinfo): 
        email_prompt = PromptTemplate.from_template(
            '''
                ### JOB DESCRIPTION:
                {job_description}
                
                ### INSTRUCTION:
                ### Your information: 
                {CV_INFO}
                
                You are passionate about skills in (area of expertise). You are currently seeking an internship opportunity in the (position).
                Your job is to write a cold email to the hiring team regarding the job mentioned above describing the capability of you.
                Also add the most relevant ones from the following repositories to showcase your projects: {repo_list} (Only include projects that you think that good for this role, don't include learning projects, Real world projects ONLY). 
                Do not provide a preamble. Make the email simple and more human-like. 
                
                ### Sugeested Email Format:
                Dear Hiring Team, 

                I'm currently pursuing a bachelor's degree in (area) at the (University), and I'm interested in applying for (position) at (the company). 

                I have a solid foundation in (Area of Expertise). I'm available for a full time internship. 

                I have attached my CV for your review. I would appreciate the opportunity to contribute to your team.

                Find my work:
                (website if the CV have)

                Sincerely,
                (name)
                (phone number)
                (email)

                
                ### EMAIL (NO PREAMBLE):  
                
                ### IF NO REPOSITORIES ARE PROVIDED, DO NOT MENTION ANY REPOSITORIES IN THE EMAIL.
                
                ### IF You cannot write an email, just return "I cannot write an email for this job."
                ### DO NOT RETURN ANYTHING ELSE.
            '''
        )
        
        chain_email = email_prompt | self.llm 
        res = chain_email.invoke({'job_description': str(job), 'repo_list': repos, 'CV_INFO': str(cvinfo)})
        return res.content