import os
import pandas as pd
from config import data_folder, src_folder, data_file_path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.model_selection import train_test_split
import nltk
nltk.download('stopwords')
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

pd.set_option('display.max_colwidth', 40000)

class process_data:

    def __init__(self):
        self.file = data_file_path
        self.columns = ['id' , 'title' , 'text', 'label']
        self.data = pd.read_csv(self.file)
        self.data.columns = self.columns
        self.labels = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def print_data_stats(self):
        '''
        Print the Dataset Statistics such as number of rows,columns in the dataset.
        :return: None
        '''
        print("Total rows in the data : ", self.data.shape[0])
        print("Number of columns in the data : ", self.data.shape[1])
        print("The data columns are : ", self.data.columns)

    def stemmer_stop_word_remover(self, text):
        '''
        Stem the words in the dataset. Stem and then remove the stop words.
        :param text: String to be processed
        :return: return string after processing is completed.
        '''
        word_list = text.split(" ")

        # Stemming and removing stop words from the text
        language = "english"
        stemmer = SnowballStemmer(language)
        stop_words = stopwords.words(language)
        filtered_text = [stemmer.stem(word) for word in word_list if stemmer.stem(word) not in stop_words]
        return ' '.join(filtered_text)

    def clean_data(self):
        '''
        Clean the data and split it on test and training dataframes.
        :return: None
        '''
        self.data.text = self.data.text.apply(lambda val: val.replace("\n", ""))
        self.data['text'] = self.data['text'].apply(self.stemmer_stop_word_remover)
        self.data.dropna(axis = 0 , how = 'any' , inplace = True)
        self.labels = self.data['label']
        self.x_train, self.x_test , self.y_train, self.y_test = train_test_split(self.data['text'], self.labels,
                                                                    test_size=0.33, random_state=123)



    def generate_count_vectorizer(self):
        count_vectorizer = CountVectorizer(stop_words='english')
        count_train = count_vectorizer.fit_transform(self.x_train)
        count_test = count_vectorizer.transform(self.x_test)
        return (count_train , count_test)

    def generate_tfidf_vectorizer(self):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.2, ngram_range=(1, 4))
        tfidf_train = tfidf_vectorizer.fit_transform(self.x_train)
        tfidf_test = tfidf_vectorizer.transform(self.x_test)
        return (tfidf_train, tfidf_test)

    def generate_hashing_vectorizer(self):
        hash_vectorizer = HashingVectorizer(stop_words='english', non_negative=True)
        hash_train = hash_vectorizer.fit_transform(self.x_train)
        hash_test = hash_vectorizer.transform(self.x_test)
        return (hash_train, hash_test)
