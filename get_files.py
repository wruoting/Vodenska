import subprocess
from os import path
import sqlite3

aapl_ticker = 320193

def create_insert_index_string():
    try:
         open("index_insert.txt", "r")
         return True
    except FileNotFoundError:
        n_lines_str = subprocess.Popen(['wc', '-l', './Edgar_Data/company_tabular_1993.tsv'], stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        number_of_lines = int(n_lines_str.split(' ')[0]) # 18874819
        # We can do this via subprocess but fuck that takes a long time
        insert_string = ''
        for line_number in range(1, number_of_lines+1):
            data_out = subprocess.Popen(['sed', '-n', "{}p;{}q".format(line_number, line_number), './Edgar_Data/company_tabular_1993.tsv'], stdout=subprocess.PIPE).stdout.read()
            new_columns = data_out.decode('utf-8').strip().split('|')
            if len(new_columns) == 6:
                print ('''INSERT INTO company_index (CIK, Company_Name, Form_Type, Date_Filed, Filename) VALUES
                             ('{}', '{}', '{}', '{}', '{}');\n'''.format(new_columns[0], new_columns[1], new_columns[2], new_columns[3], new_columns[4]))
                insert_string += '''INSERT INTO company_index (CIK, Company_Name, Form_Type, Date_Filed, Filename) VALUES
                             ('{}', '{}', '{}', '{}', '{}');\n'''.format(new_columns[0], new_columns[1], new_columns[2], new_columns[3], new_columns[4])
        with open("index_insert.txt","w+") as index_file:
            index_file.write(insert_string)
    return True
    # search(aapl_ticker, './Edgar_Data/company_tabular_1993.tsv', './Edgar_Data/AAPL')


def load_and_insert_data():
    conn = sqlite3.connect('company_data.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS company_index (CIK text, Company_Name text, Form_Type text, Date_Filed text,  FileName text, IndexFile text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS company_data (Filename text, Raw_Text text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_data (Filename text, Raw_Text text)''')
    c.commit()
                
                
def download_index(year):
    if not path.exists("index"):
        subprocess.call(["mkdir", "index"])
    subprocess.call(["python3", "./python-edgar/run.py", "-y {}".format(year), "-d index"])
    return

def search(company_ticker, data_path , output_path):
    subprocess.call(["q", '"SELECT * FROM {} where c1= {}"'.format(data_path, company_ticker), ">", "test.txt"])



if __name__ == '__main__':
    create_insert_index_string()
