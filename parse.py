import csv
import getopt
import os
import re
import sys
import urllib2
from cStringIO import StringIO
from urllib2 import urlopen

import numpy as np
import pandas as pd
import spacy
from bs4 import BeautifulSoup
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file('Resumes/{}'.format(fname),'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def extract_name(text):
    reload(sys)
    sys.setdefaultencoding('utf8')
    nlp = spacy.load('xx')
    doc = nlp(unicode(text))
    for ent in doc.ents:
        if ent.label_ == 'PER':
            return ent.text

def extract_skills(lookup,text):
    skills = []
    for word in text.split(' '):
        if word in lookup.keys():
            skills.append(word)
    return skills

def main():
    # Reads CSV and creates dictionary of technical skills and their skills type.
    skills_dict = {}
    with open('techskills.csv','r') as ts:
        for skill in ts:
            line = skill.split(',')
            skills_dict[line[1].replace('\r\n','')] = line[0]
    # Parse each candidate's resume.
    for f in os.listdir('Resumes'):
        if f != '.DS_Store':
            # Convert to raw text
            text = convert(f)
            name = extract_name(text).rstrip()
            text = text.lower()
            # Candidate name
            print 'Candidate: {}'.format(name) 
            # Contact information
            print 'Email: ' + re.findall('\S+@\S+', text)[0]
            # Technical skills
            print 'Technical skills: '
            print extract_skills(skills_dict,text)
            print '\n'

if __name__ == '__main__': main()
