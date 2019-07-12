import sqlite3

# Joins based off Filename (the link from edgar) and processes raw data from the page
def join_company_index_to_data_from_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''SELECT CIK, Company_Name, Form_Type, Date_Filed, ci.Filename, Raw_Text FROM company_index ci JOIN company_data cd ON ci.Filename = cd.Filename;''')
    rows = c.fetchall()
    return rows

def insert_into_sentiment_data(filename, polarity, subjectivity, wordcount, noun_phrases):
    return '''INSERT INTO sentiment_data (Filename, Polarity, Subjectivity, WordCount, Noun_Phrases) VALUES
                 ('{}', '{}', '{}', '{}', '{}');\n'''.format(filename, polarity, subjectivity, wordcount, noun_phrases)