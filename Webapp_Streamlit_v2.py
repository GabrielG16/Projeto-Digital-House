import pickle
import pandas as pd
import streamlit as st
import surprise
import os
from graphs import user_graph
import matplotlib.pyplot as plt
import app_functions

#Loading model and dataframes, seria legal colocar os caminhos online, pra sempre fazer a requisicao online

model, offer_title, df, sparse, clicks_de, category = app_functions.loading_files()

def main():

	paginas = ['Home','User-Analysis','KASANDR-DE']
	pagina = st.sidebar.radio('Selecione uma pagina', paginas)

	if pagina == 'Home':
		st.title('KASANDR RECOMMENDATION SYSTEM')
		st.subheader('Powered by Elias Tolentino & Gabriel Guedes')

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


		n_recs = st.slider('Number of recommentations:', min_value = 1, max_value = 100)

		#Code for prediction
		results = ''

		#Recommendation Button
		if st.button('Recommend'):

			recommendations_ML, list_of_clicked_items_ML = app_functions.recommendations_from_SVDpp(user_id, df, model, n_recs)
			mb_1, mb_2 = app_functions.lista_recomendacoes(user_id, sparse, clicks_de, offer_title, n_recs)

			col1, col2, col3 = st.columns(3)
			col1.header('Clicked:')
			col1.write(app_functions.clicked_items(user_id, list_of_clicked_items_ML, offer_title))


			col2.header('ML model:')
			col2.write(app_functions.printa_resultados_no_streamlit(user_id, recommendations_ML, offer_title))
			#results1 = printa_resultados_no_streamlit(user_id, recommendations_ML, list_of_clicked_items_ML, offer_title)


			col3.header('Memory Based Model:')
			col3.write(app_functions.printa_resultados_no_streamlit2(mb_1, offer_title))
			#results2 = printa_resultados_no_streamlit(user_id, mb_1, mb_2, offer_title)
			#results = recommendations_from_SVDpp(user_id, df, model, n_recs)



		#st.success(results1)
		#st.success(results2)


if __name__ == '__main__':
	main()