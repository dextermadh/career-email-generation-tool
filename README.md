# 📧 Career Email Generation Tool

Actually I am currently looking for a job, so I built this tool to help me generate personalized cold emails for job applications.
I write a lot of cold emails, and I wanted to automate the process of generating them based on job postings and my GitHub repositories.

A smart, interactive tool that generates **personalized cold emails** for job applications by combining scraped job postings with your GitHub repositories and an LLM.  
Built with **Streamlit** for the UI, it scrapes job pages, fetches GitHub repositories, matches skills to repos, and uses an LLM to generate a professional cold email tailored to each job.

---

## 🔧 Tech Stack

- **Streamlit** — Web UI
- **Selenium + BeautifulSoup** — Job posting scraping
- **Requests** — GitHub API requests
- **Pandas** — Repo data management
- **ChromaDB** — Vector DB to index repo embeddings
- **openai/gpt-oss-120b** — Generate natural language emails
- **Python-Dotenv** — Environment variable management

---

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
streamlit
selenium
beautifulsoup4
pandas
requests
groq
python-dotenv
chromadb     
langchain    

```

---

## 🚀 Running the Streamlit App

```bash
streamlit run app/main.py
```
---

## 🧪 Example Usage

1. Enter the job posting URL.
2. Click Generate Email
3. The tool will scrape the job details, fetch your GitHub repositories, and generate a personalized email.
4. The generated email appears in a code block, ready to copy.

---

## 📁 Project Structure

```
.
├── app/
│   └── data
    └── .env
    └── chain.py
    └── main.py
    └── repos.py
    └── scrape_job.py
    └── scrape_repos.py
    └── utils.py
├── vectorstore/
│   └── test.csv
├── requirements.txt
└── README.md
```

---

## 🔐 Environment Variables

Create a `.env` file with the following:

```
GROQ_API_KEY=your_groq_api_key
```

---

## ✍️ Author

- **Madhuka Abhishek**
- Open to feedback and collaboration!

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

