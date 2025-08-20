from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    
    for page in reader.pages:
        text += page.extract_text() + '\n'
    
    return text 

if __name__ == '__main__': 
    text = extract_text_from_pdf()
    
    print(text)
    
