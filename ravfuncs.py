import http.client
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import re

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
    # def getpattern_notes(self, idlist): #right now this just works for one pattern
    #     #searching for pattern with id search
    #     description = self.patternid_search(idlist)['notes']
    #     return description 