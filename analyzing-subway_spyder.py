# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 16:18:58 2017

@author: josec
"""

import urllib
from bs4 import BeautifulSoup
import pandas as pd

page = urllib.request.urlopen('http://web.mta.info/developers/turnstile.html')
pagehtml = page.read()

soup = BeautifulSoup(pagehtml, "html.parser")
links = soup.find_all('a')

for link in links:
    href = link.get('href')
    if (not(href == None) and ('1706' in href)):
        filename = href.split("/")[-1]
        url = ('http://web.mta.info/developers/'+href)
        path = ('C:/Users/josec/Google Drive/Udacity/Fundamentos_Data_Science_II/NDFDSII-NYC-subway-data_analysis/%s' %(filename))
        urllib.request.urlretrieve(url, path)
        
        
def create_master_turnstile_file(filenames, output_file):
    with open(output_file, 'w') as master_file:
        master_file.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
        for filename in filenames:
            with open(filename, 'r') as r:
                count = 1
                for line in r:
                    if count == 1:
                        count += 1
                        continue
                    
                    CA = line.find(',')
                    UNIT = line.find(',', CA+1)
                    SPC = line.find(',', UNIT+1)
                    STATION = line.find(',', SPC+1)
                    LINE = line.find(',', STATION+1)
                    DIVISION = line.find(',', LINE+1)
                    master_file.write(line[0:SPC] + line[DIVISION:100] + '\n')
               
            
filenames = ["turnstile_170603.txt", "turnstile_170610.txt", "turnstile_170617.txt", "turnstile_170624.txt"]
output_file = "turnstile_all.txt"
create_master_turnstile_file(filenames, output_file)


def filter_by_regular(filename):
    
    turnstile_data = pd.read_csv(filename)
    turnstile_data = turnstile_data[(turnstile_data['DESCn'] == 'REGULAR')]
    return turnstile_data

turnstile_regular = filter_by_regular('turnstile_all.txt')


def return_hours(x):
    return x - x.shift(1)

def get_hourly_entries(df):    
    
    df['ENTRIESn_hourly'] = df[['ENTRIESn']].apply(return_hours) 
    df.fillna(1, inplace=True)
                        
    return df


turnstile_regular_hourlyEntries = get_hourly_entries(turnstile_regular)

    










        