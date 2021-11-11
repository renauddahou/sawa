
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import io
import docx2txt
from docx import Document
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import pandas as pd
import textwrap
from deep_translator import GoogleTranslator
import textwrap
from pyresparser import ResumeParser

# Fonction list to string
def listToString(s): 
    str1 = " "  
    return (str1.join(s))

#lecture et traduction pdf
def read_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True): 
        interpreter.process_page(page)
    text = retstr.getvalue()
    text = " ".join(text.replace(u"\xa0", " ").strip().split())
    lines = textwrap.wrap(text, 4999, break_long_words=False)
    textlist=[]
    for line in lines:
        transtext=line
        text= GoogleTranslator(source='auto', target='en').translate(transtext)
        textlist.append(text)
    text=listToString(textlist)    
    fp.close()
    device.close()
    retstr.close()
    return text

#lecture et traduction docx doc
def docx2txtrans(dirfile):
    text=docx2txt.process(dirfile)
    text = " ".join(text.replace(u"\xa0", " ").strip().split())
    lines = textwrap.wrap(text, 4999, break_long_words=False)
    textlist=[]
    for line in lines:
        transtext=line
        text= GoogleTranslator(source='auto', target='en').translate(transtext)
        textlist.append(text)
    text=listToString(textlist)    
    return text

#détecteur de format
def read_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        dirfile=resume_directory+res
        if (dirfile.endswith('.docx')):
            text = docx2txtrans(dirfile)
        elif (dirfile.endswith('.doc')):
            text = docx2txtrans(dirfile)
        elif (dirfile.endswith('.pdf')):
            text = read_pdf(dirfile)
        temp.append(text)
        placeholder.append(temp)
    return placeholder


#traducteur text venant de dataframe
def translator(lines):
    textlist=[]
    for line in lines:
        transtext=line
        text= GoogleTranslator(source='auto', target='en').translate(transtext)
        textlist.append(text)
    text=listToString(textlist)    
    return text


# fonction d'extraction des compétence d'un CV
def skill_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        dirfile=resume_directory+res
        if (dirfile.endswith('.docx')):
            text = ResumeParser(dirfile).get_extracted_data()
        elif (dirfile.endswith('.doc')):
            text = ResumeParser(dirfile).get_extracted_data()
        elif (dirfile.endswith('.pdf')):
            text = ResumeParser(dirfile).get_extracted_data()
        temp.append(text)
        placeholder.append(temp)
    return placeholder


#fonction de récupération  des skill d'un job description

def skills_doc(text):
    skill_job=[]
    document = Document()
    document.add_paragraph(text)
    document.save('docx_file.docx')
    text = ResumeParser('docx_file.docx').get_extracted_data()
    skill_job.append(text)
    os.remove("docx_file.docx")
    return skill_job

# itération pour recupéré les skills et le nom du job et resum
def get_skjob_resum(dict_job_resum):
    L="skills"
    M="name"
    sklst=[]
    nmlst=[]
    for i in dict_job_resum:
        l=i
        res = None
        resn=None
        if all(L in sub for sub in [l]):
            res = l[L]
        if all(M in sub for sub in [l]):
            resn = l[M]

        sklst.append(res)
        nmlst.append(resn)

    #Creation de la dataframe Nom et skill

    df = pd.DataFrame({'Nom': nmlst,'Skills': sklst})

    def listToStringWithoutBrackets(list1):
        return str(list1).replace('[','').replace(']','').replace("'",'')

    df['Skills']=df['Skills'].apply(listToStringWithoutBrackets)
    return df
