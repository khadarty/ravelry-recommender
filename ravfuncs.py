import http.client
import json
import requests
import pandas as pd
# from pandas.io.json import json_normalize 
import numpy as np
import matplotlib.pyplot as plt
from transformers import DistilBertTokenizer, DistilBertModel, DistilBertForSequenceClassification
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
# from pandas.io.json._table_schema import build_table_schema
import torch
import re
# import tensorflow as tf


authUsername = 	'39589cfb8dbfa66f26be148b1f5dc17a'
authPassword = 'bXzsSC457MZAKS4KLqFUq-GC139GBWbKtzsxFU1k'
baseurl = 'https://api.ravelry.com'

class ravutils:
    def __init__(self, authUsername, authPassword):
        self.authUsername = authUsername
        self.authPassword = authPassword
        
    def pattern_search(self, query = '',  page = 1, page_size = 100, craft = 'knitting'):
        #returns dataframe
        #remember to search by permalink to get an exact result
        url = baseurl + f'/patterns/search.json?query={query}&page={page}&page_size={page_size}&craft={craft}'
        response = requests.get(url, auth = requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        response.close()
        norm = response.json()['patterns']
        df = pd.json_normalize(data = norm)
        return df
        
    def patternid_search(self, idlist):
        #returns dataframe 
        stridlist = [str(i) for i in idlist]
        idstring = ''
        plus = '+'
        
        if len(idlist) == 1:
            idstring += stridlist[0]
        else:
            idstring = plus.join(stridlist)
        url = baseurl + f'/patterns.json?ids={idstring}'
        response = requests.get(url, auth = requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        response.close()

        norm = response.json()['patterns'].values()
        df = pd.json_normalize(data = norm)

        cols = []
        count = 1
        for column in df.columns:
            if 'name' in column:
                cols.append(f'name_{count}')
                count+=1
                continue
            cols.append(column)
        df.columns = cols 
        return df
        
    def get_id(self, url):
        pass
        
    def get_favorites(self, rav_username = 'khadarty', types = 'pattern', query = '', deep_search = '', page = 1, page_size = 100):
        #gets list of pattern favorites
        url = baseurl + f"/people/{rav_username}/favorites/list.json?types={types}&query={query}&deep_search={deep_search}&page={page}&page_size={page_size}"
        response= requests.get(url, auth = requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        response.close()
        
        norm = response.json()['favorites']
        df = pd.json_normalize(data = norm)
        return df
    def get_queue(self, rav_username = 'khadarty', query = '', page = 1, page_size = 100):
        #define URL
        url = baseurl + f'/people/{rav_username}/queue/list.json?query={query}&page={page}&page_size={page_size}' 
        #make the request
        response = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        response.close()
        norm = response.json()['queued_projects']
        df = pd.json_normalize(data = norm)
        return df
    def get_user(self, rav_username = 'khadarty'):
        #define URL
        url = baseurl + f'/people/{rav_username}.json' 
        #make the request
        response = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        response.close()
        norm = response.json()['user']
        df = pd.json_normalize(data = norm)
        return df
    def get_projects(self, rav_username = 'khadarty', page = 1, page_size = 100, collections = '', sort = ''):
        #define URL
        url = baseurl + f'/projects/{rav_username}/list.json?page={page}&page_size={page_size}&sort={sort}&include={collections}' 
        #make the request
        response = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.authUsername, self.authPassword))
        #close the connection
        response.close()
        norm = response.json()['projects']
        df = pd.json_normalize(data = norm)
        return df
    


def get_embeddings(descriptions):
        # if isinstance(descriptions,str):
        inputs = tokenizer(descriptions, return_tensors="pt", truncation=True, padding=True) #, max_length=128
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)
def dropcols_cleannotes(new_df):
        def rmurls(text):
            if isinstance(text, str):
                #removing urls, [1]:, and non english characters from text 
                #i'm gonna have to hard code special characters r'[^a-zA-Z\s\.,!?;:]' --> so i'll leave this out for now
                patterns = [r'\[\d+\]:', r'https?://\S+|www\.\S+', r'\[\d+\]']
                combined_pattern = '|'.join(patterns)
                cleaned_text = re.sub(combined_pattern, '', text)
                # url_patt = re.compile(r'https?://\S+|www\.\S+')
                return cleaned_text
            else:
                return ''
    
        new_df['notes'] = new_df['notes'].str.replace('\r', ' ').str.replace('\n', ' ').str.replace('*', ' ').str.replace('>', ' ') #i removed '#' from this list
        # new_df['notes'] = new_df['notes'].apply(rmbracurls)
        new_df['notes'] = new_df['notes'].apply(rmurls)
        new_df['combo'] = new_df['gauge_pattern'] + ' ' + new_df['name_1'] + ' ' + new_df['sizes_available'] + ' ' + new_df['gauge_description'] + ' ' + new_df['yardage_description'] + ' ' + new_df['notes'] + ' ' + new_df['name_2'] + ' ' + new_df['name_3'] + ' '  + new_df['name_5'] 
        # + new_df['name_4'] + ' '
        return new_df

def get_recs(user_embedding, pattern_embeddings):
    score = cosine_similarity(user_embedding, pattern_embeddings)
    return score[0][0]

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')