import os
import pickle
import pandas as pd
from sk import corte_pivo_log
from collections import defaultdict

def loading_files():

    origin_path = os.getcwd()
    path_model = '\.pkl\svdpp.pkl'
    model = pickle.load(open((origin_path + path_model), 'rb'))

    path_offer = '\.pkl\offers.pkl'
    offer_title = pickle.load(open(origin_path + path_offer, 'rb'))

    path_df = '/.csv/sparse_melt.csv'
    df = pd.read_csv(origin_path + path_df)

    path_sparse = '/.csv/sparse.csv'
    sparse = pd.read_csv(origin_path + path_sparse, index_col=0)

    path_clicks_de = '/.csv/clicks_de.csv'
    clicks_de = pd.read_csv(origin_path + path_clicks_de)

    path_category = '/.csv/translations.csv'
    category = pd.read_csv(origin_path + path_category, sep=';')

    return model, offer_title, df, sparse, clicks_de, category

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

	return (top_n_recommendations, list_of_clicked_items)

def lista_recomendacoes(user, sparse, clicks_de, offer_title,n_recommendations):  # Função que calcula as recomendações para um usuário user qualquer e retorna o top5 de ofertas mais relevantes

	# Seleção de usuários com maior correlação com o usuário selecionado
	sparse = sparse.T
	# mask = sparse.loc[sparse.index == user, :]
	topmatch_users = (sparse.corrwith(sparse[user]).sort_values(ascending=False))[1:]
	clicks_selected_user = clicks_de[clicks_de['User'] == user]['Offer'].drop_duplicates().values

	# Os weights é quanto aquele novo produto é relevante para o usuário em relação ao nível de correlação entre usuários
	weights = topmatch_users.values

	recommendations = []  # Lista de possíveis indicações com base nos clicks dos usuários semelhantes
	for user_id in range(len(topmatch_users[:5])):  # Loop pelos usuários mais semelhantes

		if weights[user_id] < 0:
			continue

		clicks_user = clicks_de[clicks_de['User'] == topmatch_users.index[user_id]]['Offer']  # Clicks de cada usuário da lista top5
		for offer in clicks_user:  # Cliques do usuário
			if offer in clicks_selected_user:  # Se já foi um clique do usuário-alvo, não é considerado
				pass
			else:
				recommendations.append((offer, weights[user_id], user_id))

	rec_set = pd.DataFrame(recommendations, columns=['Offer', 'Weight', 'User']).drop_duplicates()  # Dropar Duplicatas
	top_rec = rec_set.groupby('Offer')['Weight'].sum().sort_values(ascending=False)[:int(n_recommendations)]

	return (top_rec.index, clicks_selected_user)

def clicked_items(user_id, list_of_clicked_items, offer_title):

	msg = ""
	for item in list_of_clicked_items[:5]:
		msg = msg + offer_title[item] + '\n\n'

	return msg

def printa_resultados_no_streamlit(user_id, top_n_recommendations, offer_title):

	msg = 'We recommend: \n\n'
	count = 0
	for item_index, score in top_n_recommendations[user_id]:

		count += 1

		msg += (str(count) + '. ' + str(offer_title[item_index]) + ' predicted rating = ' + str(round(score, 3)))
		msg += '\n'
	return msg


def printa_resultados_no_streamlit2(top_n_recommendations, offer_title):

	msg = 'We recommend: \n\n'
	count = 0
	for item in top_n_recommendations:
		count += 1
		msg += (str(count) +'. ' + str(offer_title[item]) + '\n')

	return msg