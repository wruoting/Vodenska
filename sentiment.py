import urllib
from urllib import request
import http.client
import sqlite3
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
import json
from SENTIMENT_DATA import SentimentData
from SENTIMENT_DATA_QUERY_LAYER import *

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# Takes a url (theoretically)
# Makes a request to EDGAR and inserts the data into the database into company_data
def insert_into_company_data():
    
    data = urllib.request.urlopen("https://www.sec.gov/Archives/edgar/data/22099/0000893220-95-000847.txt")
    datastring = process_online_data(data.read().decode('utf-8'))
    
    insert_string = '''INSERT INTO company_data (Filename, Raw_Text) VALUES ("{}", "{}")'''.format("https://www.sec.gov/Archives/edgar/data/22099/0000893220-95-000847.txt", datastring)
    conn = sqlite3.connect('hellothere.db')
    c = conn.cursor()
    c.execute(insert_string)
    conn.commit()

# Replaces new line with space
def process_online_data(datastring):
    datastring = datastring.replace('\n', ' ')
    return datastring
    
# Inserts a test into hellothere db
def test_insert_into_company_index():
    conn = sqlite3.connect('hellothere.db')
    c = conn.cursor()
    insert_string = '''INSERT INTO company_index (CIK, Company_Name, Form_Type, Date_Filed, FileName, IndexFile) VALUES
                 ('123456', 'Banana', 'Test', '08-08-2015', "https://www.sec.gov/Archives/edgar/data/22099/0000893220-95-000847.txt", "https://www.sec.gov/Archives/edgar/data/22099/0000893220-95-000847.html");\n'''
    c.execute(insert_string)
    conn.commit()


# Creates the tables for company
def load_and_insert_data(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS company_index (CIK text, Company_Name text, Form_Type text, Date_Filed text, Filename text UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS company_data (Filename text UNIQUE, Raw_Text text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_data (Filename text UNIQUE, Polarity text, Subjectivity text, WordCount text, Noun_Phrases text)''')
    conn.commit()
    

def sentiment_data_analysis(filename, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    rows = join_company_index_to_data_from_db(db_name)
    query_string = ''
    for row in rows:
        sentiment = SentimentData(filename)
        query_string += sentiment.return_query(row)
    c.execute(query_string)
    conn.commit()
    print('Insert into {} successful'.format(db_name))
    


sentiment_data_analysis("https://www.sec.gov/Archives/edgar/data/22099/0000893220-95-000847.txt", 'hellothere.db')
