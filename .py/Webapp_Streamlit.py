import pickle
import pandas as pd
import streamlit as st
import surprise
import os
from sk import corte_pivo_log
from collections import defaultdict

#Loading model and dataframes
model = pickle.load(open(os.getcwd()+"/.pkl/svdpp.pkl", 'rb'))
offer_title = pickle.load(open(os.getcwd()+'/.pkl/offers.pkl', 'rb'))
df = pd.read_csv(os.getcwd()+'/sparse_melt.csv')

#Function for prediction

def recommendations_from_SVDpp(user_id, pivo_log, algo, n_recommendations):

	#Casting inputs for integers
	try:
		user_id = int(user_id)
	except:
		return "Invalid User Input"

	try:
		n_recommendations = int(n_recommendations)
	except:
		return "Invalid Recommendations Number"

	#Determining Categories clicked by selected user
	pivo_log = corte_pivo_log(user_id, pivo_log)

	# determine list of unseen itemns by user_id
	list_of_unclicked_items = pivo_log[(pivo_log['User'] == user_id) & (pivo_log['Clicked?'] == 0)]['Products']
	list_of_clicked_items = pivo_log[(pivo_log['User'] == user_id) & (pivo_log['Clicked?'] == 1)]['Products']

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


	#print("Recommendations for user with id {}: ".format(user_id))

	msg = "Because you clicked items like:\n\n"
	for item in list_of_clicked_items.sample(5):
		msg = msg+offer_title[item]+'\n\n'

	msg+=' We recommend:\n\n'

	count = 0

	for item_index, score in top_n_recommendations[user_id]:
		count += 1

		msg += (str(count) + '. ' + str(offer_title[item_index]) + ' predicted rating = ' + str(round(score, 3)))
		msg += '\n'
	return msg


def main():

	#App Title
	st.title('Product Recommender System Web App - KASANDR (DE)')

	#Input Data
	user_id = st.text_input('User Id:')
	n_recs = st.text_input('Number of recommentations:')

	#Code for prediction
	results = ''

	#Recommendation Button
	if st.button('Recommend'):
		with st.spinner('Wait for it...'):
			try:
				results = recommendations_from_SVDpp(user_id, df, model, n_recs)
			except ValueError:
				results = "Usuário inexistente"



	st.success(results)


if __name__ == '__main__':
	main()