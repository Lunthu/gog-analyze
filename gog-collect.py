# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 18:39:21 2025

@author: valno
"""

import requests
import json
import pandas as pd
import time
import os

def games_basic_data(pages):
    df = pd.DataFrame()
    
    
    for i in range(1, pages):
    
        basic_request = requests.get('https://embed.gog.com/games/ajax/filtered?mediaType=game&page={}'.format(i))
        raw_data = pd.DataFrame(json.loads(basic_request.text)['products'])
        
        df= pd.concat([df, raw_data], ignore_index = True)
        time.sleep(0.33)
        
    price_data = pd.json_normalize(df['price'])
    df = df.join(price_data, lsuffix = "_main")
    
    return df


def reviews_agg_data(game_id):
    
    aggregated_data = {}
    
    basic_request = requests.get('https://reviews.gog.com/v1/products/{}/reviews?language=in:en-US&order=desc:votes'.format(game_id))
    buf = json.loads(basic_request.text)
    aggregated_data['game_id'] = game_id
    aggregated_data['filteredAvgRating'] = buf['filteredAvgRating']
    aggregated_data['overallAvgRating'] = buf['overallAvgRating']
    aggregated_data['reviewCount'] = buf['reviewCount']
    aggregated_data['isReviewable'] = buf['isReviewable']
    aggregated_data['pages'] = buf['pages']
    pages = buf['pages']
    return aggregated_data, pages


def reviews_agg_data_plus(game_id):
    
    aggregated_data = {}
    full_data = pd.DataFrame()
    
    basic_request = requests.get('https://reviews.gog.com/v1/products/{}/reviews?language=in:en-US&order=desc:votes'.format(game_id))
    buf = json.loads(basic_request.text)
    aggregated_data['game_id'] = game_id
    aggregated_data['filteredAvgRating'] = buf['filteredAvgRating']
    aggregated_data['overallAvgRating'] = buf['overallAvgRating']
    aggregated_data['reviewCount'] = buf['reviewCount']
    aggregated_data['isReviewable'] = buf['isReviewable']
    aggregated_data['pages'] = buf['pages']
    pages = buf['pages']

    raw_data = pd.DataFrame(json.loads(basic_request.text)['_embedded']['items'])
    if len(full_data) > 0:
        raw_data = raw_data.join(pd.json_normalize(raw_data['content']), rsuffix = '_content')
        raw_data = raw_data.join(pd.json_normalize(raw_data['reviewer']), rsuffix = '_reviewer')
        raw_data = raw_data.join(pd.json_normalize(raw_data['rating']), rsuffix = '_rating')
        raw_data = raw_data.join(pd.json_normalize(raw_data['votes']), rsuffix = '_votes')
        raw_data = raw_data.drop(['content', 'reviewer','rating', '_links', 'votes'], axis=1)
        raw_data = raw_data.rename(columns = {'value': 'rating'})
        raw_data = raw_data.drop(list(raw_data.filter(regex = 'avatar')), axis = 1)
    full_data= pd.concat([full_data, raw_data], ignore_index = True)
    
    
    
    return aggregated_data, full_data, pages

def reviews_full_data(game_id, pages):
    full_data = pd.DataFrame()
    
    for i in range(1, pages):
        try:
            
            basic_request = requests.get('https://reviews.gog.com/v1/products/{}/reviews?language=in:en-US&order=desc:votes&page={}'.format(game_id,i))
            raw_data = pd.DataFrame(json.loads(basic_request.text)['_embedded']['items'])
            raw_data = raw_data.join(pd.json_normalize(raw_data['content']), rsuffix = '_content')
            raw_data = raw_data.join(pd.json_normalize(raw_data['reviewer']), rsuffix = '_reviewer')
            raw_data = raw_data.join(pd.json_normalize(raw_data['rating']), rsuffix = '_rating')
            raw_data = raw_data.join(pd.json_normalize(raw_data['votes']), rsuffix = '_votes')
            raw_data = raw_data.drop(['content', 'reviewer','rating', '_links', 'votes'], axis=1)
            raw_data = raw_data.rename(columns = {'value': 'rating'})
            raw_data = raw_data.drop(list(raw_data.filter(regex = 'avatar')), axis = 1)
            full_data= pd.concat([full_data, raw_data], ignore_index = True)
        except:
            pass
    
        time.sleep(0.33)
        
    return full_data
