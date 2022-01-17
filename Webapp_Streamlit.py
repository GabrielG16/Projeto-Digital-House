

import numpy as np 
import pickle
import pandas as pd
import streamlit as sl
import surprise
from collections import defaultdict

#Loading model
model = pickle.load(open("C:/Users/gabri/Desktop/DH/PI/svdpp.pkl", 'rb'))
offer_title = pickle.load(open('offers.pkl', 'rb'))
df = pd.read_csv('sparse_melt.csv')
#Function for prediction

def recommendations_from_SVDpp(user_id, pivo_log, algo, n_recommendations):
    
    # determine list of unseen itemns by user_id
    list_of_unclicked_items = pivo_log[(pivo_log['User']==user_id) & (pivo_log['Clicked?']==0)]['Products']
    
    # set up user set with unrated movies
    user_set = [[user_id, item_id, 0] for item_id in list_of_unclicked_items]
    
    # generate predictions
    predictions = algo.test(user_set)

    top_n_recommendations = defaultdict(list)
    
    for user_id, item_id, _, est, _ in predictions:

        top_n_recommendations[user_id].append((item_id, est))

        
    for user_id, ratings in top_n_recommendations.items():

        ratings.sort(key=lambda x: x[1], reverse=True)

        top_n_recommendations[user_id] = ratings[:n_recommendations]


    count = 0

    print("Recommendations for user with id {}: ".format(user_id))

    message = ''

    for item_index, score in top_n_recommendations[user_id]: 

        count +=1

        message += (str(count)+'. '+str(offer_title[item_index])+' predicted rating = '+str(round(score,3)))

    return str(offer_title[item_index])

def main():

	#App Title
	sl.title('Recommender System Web App')

	#Input Data
	user_id = sl.text_input('User Id:')
	n_recs = sl.text_input('Number of recommentations:')

	#Code for prediction
	results = ''

	#Recommendation Button
	if sl.button('Recommend'):
	 	results = recommendations_from_SVDpp(user_id, df, model, n_recs)

	sl.success(results)


if __name__ == '__main__':
	main()