import pickle
import pandas as pd
import streamlit as st
import surprise
import os
from sk import corte_pivo_log
from graphs import user_graph
from collections import defaultdict
import matplotlib.pyplot as plt


#Loading model and dataframes, seria legal colocar os caminhos online, pra sempre fazer a requisicao online

origin_path = os.getcwd() + '\DH\Projeto\KASSANDR\GIT\Projeto-Digital-House'
path_model = '\.pkl\svdpp.pkl'
model = pickle.load(open((origin_path+path_model), 'rb'))

path_offer = '\.pkl\offers.pkl'
offer_title = pickle.load(open(origin_path+path_offer, 'rb'))

path_df = '/.csv/sparse_melt.csv'
df = pd.read_csv(origin_path+path_df)

path_sparse = '/.csv/sparse.csv'
sparse = pd.read_csv(origin_path+path_sparse, index_col = 0)

path_clicks_de = '/.csv/clicks_de.csv'
clicks_de = pd.read_csv(origin_path+path_clicks_de)

path_category = '/.csv/translations.csv'
category = pd.read_csv(origin_path+path_category, sep = ';')



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

	msg = "Because you clicked items like:\n\n"
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



def main():

	paginas = ['Home','User-Analysis','KASANDR-DE']
	pagina = st.sidebar.radio('Selecione uma pagina', paginas)

	if pagina == 'Home':
		st.title('KASANDR RECOMMENDATION SYSTEM')
		st.subheader('Powered by Gabriel Guedes')

		st.markdown('WebApp para analise de um sistema de recomendação sobre cliques de compras do site KELKO')

# pra deixar mais simples, coloquei a função de grafico em um arquivo.py separado, assim que for construindo as outras vou colocando la, pra não deixar esse arquivo mto grande tbm
	elif pagina == 'User-Analysis':
		st.title('Breve EDA do usuário:')
		#Input Data

		user_disponiveis = df.User.unique()
		user_id = st.selectbox('Selecione um usuario:', user_disponiveis)

		#Code for prediction
		results = ''

		if st.button('Generate'):

			st.pyplot(user_graph(df, category, user_id))



	elif pagina == 'KASANDR-DE':
		#App Title
		st.title('Product Recommender System Web App - KASANDR (DE)')

		#Input Data

		user_disponiveis = df.User.unique()
		user_id = st.selectbox('Selecione um usuario:', user_disponiveis)

		#user_id = st.text_input('User Id:')


		n_recs = st.text_input('Number of recommentations:')

		#Code for prediction
		results = ''

		#Recommendation Button
		if st.button('Recommend'):

			recommendations_ML, list_of_clicked_items_ML = recommendations_from_SVDpp(user_id, df, model, n_recs)
			mb_1, mb_2 = lista_recomendacoes(user_id, sparse, clicks_de, offer_title, n_recs)

			col1, col2, col3 = st.columns(3)
			col1.header('Clicked:')
			col1.write(clicked_items(user_id, list_of_clicked_items_ML, offer_title))


			col2.header('ML model:')
			col2.write(printa_resultados_no_streamlit(user_id, recommendations_ML, offer_title))
			#results1 = printa_resultados_no_streamlit(user_id, recommendations_ML, list_of_clicked_items_ML, offer_title)


			col3.header('Memory Based Model')
			col3.write(printa_resultados_no_streamlit2(mb_1, offer_title))
			#results2 = printa_resultados_no_streamlit(user_id, mb_1, mb_2, offer_title)
			#results = recommendations_from_SVDpp(user_id, df, model, n_recs)



		#st.success(results1)
		#st.success(results2)


if __name__ == '__main__':
	main()