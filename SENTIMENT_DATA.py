from SENTIMENT_DATA_QUERY_LAYER import *
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
import sqlite3
import json
from textblob import TextBlob
import xmltodict

class SentimentData(object):
    def __init__(self, filename):
        self.filename = filename
        self.polarity = None
        self.subjectivity = None
        self.total_words = None
        self.noun_phrases = None
        
    def return_query(self, row):
        self.total_words = word_count(row[5])
        self.polarity, self.subjectivity, self.noun_phrases = sentiment_analysis(row[5])
        return insert_into_sentiment_data(row[4], self.polarity, self.subjectivity, self.total_words, self.noun_phrases)

# Does the sentiment analysis
def sentiment_analysis(row_text):
    blob = TextBlob(row_text)
    # print(xmltodict.parse(row_text))
    noun_phrase_array = []
    for np in blob.noun_phrases:
        if remove_stop_words(np) != '':
            noun_phrase_array.append(np)
    sanitize_noun_phrase = json.dumps(str_sanitize_for_db(str(noun_phrase_array)))
    return blob.sentiment.polarity, blob.sentiment.subjectivity, sanitize_noun_phrase

# Does a word count on the row of text, and returns an array of words
def word_count(row_text):
    tokenizer = TreebankWordTokenizer()
    tokenize_by_word = tokenizer.tokenize(row_text)
    word_map = {}
    arraylist = []
    for word in tokenize_by_word:
        if word_map.get(word) is None:
            word_map[word] = 1
        else:
            word_map[word] += 1
    for index, key in enumerate(word_map):
        if remove_stop_words(key) != '':
            new_key = str_sanitize_for_db(key)
            arraylist.append((new_key, word_map[key]))
    arraylist.sort(key=sortSecond, reverse=True)
    return json.dumps(arraylist)

def remove_stop_words(row_text):
    english_stop_words = stopwords.words('english')
    additional_list = ['</TEXT>', '', '<DOCUMENT>', '</DOCUMENT>', '<SEC-DOCUMENT>', '</SEC-DOCUMENT>', '-----END', 'PRIVACY-ENHANCED', 'MESSAGE-----', 
                        '----------------------------', '&', '/s/', '<PAGE>', '</PAGE>', '--------------', '<TEXT>', '<TYPE>', '</TYPE>', '</SEC-HEADER>', '<SEC-HEADER>',
                        '<SEQUENCE>', '</SEQUENCE>', '<DESCRIPTION>', '</DESCRIPTION>', '-----BEGIN', '--', ':']
    english_stop_words.extend(additional_list)
    removed_stop_words = []
    row_text = row_text.split(' ')
    for review in row_text:
        if review not in english_stop_words:
            removed_stop_words.append(review)
    string_removed_stop_words = ' '.join(removed_stop_words)
    return string_removed_stop_words

def str_sanitize_for_db(string_value):
    return string_value.replace("\'", "\'\'")
    
def sortSecond(val):
    return val[1]        