import pickle
import pandas as pd
import streamlit as st
#import surprise
import os

import graphs
from graphs import user_graph
import matplotlib.pyplot as plt
import app_functions
import imp_recomender
import home
offer_title, model, sparse_item_user, sparse_user_item, indice_itens = imp_recomender.loading_files()
sparse_old, category = graphs.loading_sparse_category()

def main():

	paginas = ['Home','EDA-Country', 'User-Analysis', 'KASANDR-DE-USER', 'KASSANDR-USER-USER', 'KASSANDR-DE-ITEM', 'KASSANDR-COLD-START']
	pagina = st.sidebar.radio('Selecione uma pagina', paginas)

	if pagina == 'Home':
		# st.title('KASANDR RECOMMENDATION SYSTEM')
		# st.subheader('Powered by Elias Tolentino & Gabriel Guedes & José Eduardo')
		#
		# st.markdown('WebApp para analise de um sistema de recomendação sobre cliques de compras do site KELKO')

		home.home_page()

# pra deixar mais simples, coloquei a função de grafico em um arquivo.py separado, assim que for construindo as outras vou colocando la, pra não deixar esse arquivo mto grande tbm
# pensar em colocar as 7 tabelas carregadas separadas e quando chamar o filtro ja está feito


#Pensar sobre colocar as funções de loading_data dentro do if ou fora

	elif pagina == 'EDA-Country':
		st.title('Country Distribution')

		de = st.checkbox('Alemanha')
		fr = st.checkbox('França')
		it = st.checkbox('Italia')

		#st.write(de, fr, it)

		italia, franca, alemanha, franca_alemanha, franca_italia, alemanha_italia, union = graphs.loading_union()

		if de and not(fr) and not(it):
			country = 'de'
			st.write('Você escolheu em ver as distribuições da alemanha')
		elif not(de) and fr and not(it):
			country = 'fr'
			st.write('Você escolheu em ver as distribuições da frança')
		elif not(de) and not(fr) and it:
			country = 'it'
			st.write('Você escolheu em ver as distribuições da Italia')
		elif de and fr and not(it):
			country = 'frde'
			st.write('Alemanha e França')
		elif fr and it and not(de):
			country = 'frit'
			st.write('França e Italia')
		elif de and not(fr) and it:
			country = 'deit'
			st.write('Alemanha e Italia')
		elif de and fr and it:
			country = 'all'
			st.write('Combinação dos 3 países')
		elif not(de) and not(fr) and not(it):
			country = False
			st.write('Selecione uma ou mais opções para gerar graficos')
		#st.write(country)


		if country == 'frde':
			graphs.lista_top10_categorias(franca_alemanha)
			selection = pd.Series(franca_alemanha.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, franca_alemanha, n_prods)

		elif country == 'frit':
			graphs.lista_top10_categorias(franca_italia)
			selection = pd.Series(franca_italia.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, franca_italia, n_prods)

		elif country == 'deit':
			graphs.lista_top10_categorias(alemanha_italia)
			selection = pd.Series(alemanha_italia.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, alemanha_italia, n_prods)

		elif country == 'all':
			graphs.lista_top10_categorias(union)
			selection = pd.Series(union.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, union, n_prods)

		elif country == 'fr':
			graphs.lista_top10_categorias(franca)
			selection = pd.Series(franca.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, franca, n_prods)

		elif country == 'it':
			graphs.lista_top10_categorias(italia)
			selection = pd.Series(italia.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, italia, n_prods)

		elif country == 'de':
			graphs.lista_top10_categorias(alemanha)
			selection = pd.Series(alemanha.category_translate.unique()).sort_values().str.title()
			categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

			categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			if st.button('Generate'):
				st.write(categoria_escolhida)
				graphs.filtro_por_categoria(categoria_escolhida, alemanha, n_prods)


			#selection = graphs.corte_union(union, country)
			#graphs.lista_top10_categorias(selection)

			#categorias_disponiveis = selection #pd.Series(selection.c_t.unique()).sort_values().str.title()

			#categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
			#n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

			#if st.button('Generate'):
			#	st.write(categoria_escolhida)
			#	graphs.filtro_por_categoria(categoria_escolhida, selection, n_prods)

	elif pagina == 'User-Analysis':
		st.title('Breve EDA do usuário:')
		#Input Data

		#user_disponiveis = list(sparse_item_user.indices)
		user_disponiveis = sparse_old.User.unique()
		user_id = st.selectbox('Selecione um usuario:', user_disponiveis)

		#Code for prediction
		results = ''

		if st.button('Generate'):
			st.write('grafico do usuario!')
			st.pyplot(user_graph(sparse_old, category, user_id))
			print('hello world')

	elif pagina == 'KASANDR-DE-USER':
		#App Title
		st.title('Product Recommender System Web App - KASANDR (DE)')

		#Input Data

		user_disponiveis = list(sparse_item_user.indices)
		user_id = st.selectbox('Selecione um usuario:', user_disponiveis)


		#n_recs = st.slider('Number of recommentations:', min_value = 1, max_value = 100)

		#Code for prediction
		results = ''

		#Recommendation Button
		if st.button('Recommend'):

			#recommendations_ML, list_of_clicked_items_ML = app_functions.recommendations_from_SVDpp(user_id, df, model, n_recs)
			#mb_1, mb_2 = app_functions.lista_recomendacoes(user_id, sparse, clicks_de, offer_title, n_recs)

			recommended_items, clicked_items = imp_recomender.recommend(user_id, model, sparse_user_item)
			col1, col2 = st.columns(2)
			col1.header('Recommended:')
			col1.write(imp_recomender.print_offers_name_on_streamlit(recommended_items, offer_title))


			col2.header('Clicked:')
			col2.write(imp_recomender.print_offers_name_on_streamlit(clicked_items, offer_title))


			#col3.header('Most Similar Users:')
			#col3.write(app_functions.printa_resultados_no_streamlit2(mb_1, offer_title))
			#results2 = printa_resultados_no_streamlit(user_id, mb_1, mb_2, offer_title)
			#results = recommendations_from_SVDpp(user_id, df, model, n_recs)

	elif pagina == 'KASSANDR-USER-USER':
		st.title('User by User')
		user_disponiveis = list(sparse_item_user.indices)
		user_id = st.selectbox('Selecione um usuario:', user_disponiveis)

		if st.button('Similar Users'):

			similar, common = imp_recomender.most_similar_users(user_id, sparse_user_item,model)
			st.write(similar)
			st.write(common)
			#st.write(imp_recomender.print_offers_name_on_streamlit(common, offer_title))



	elif pagina == 'KASSANDR-DE-ITEM':
		st.title('Itens')


		#itens_disponiveis = indice_itens['Offer_Title']
		itens_disponiveis = list(sparse_user_item.indices)
		item_id = st.selectbox('Selecione um item:', itens_disponiveis)

		if st.button('Recommend'):
			st.write('Select Item:', offer_title[item_id])
			st.write('')
			most_similar_items = imp_recomender.most_similar_items(item_id, model)
			st.write(imp_recomender.print_offers_name_on_streamlit(most_similar_items, offer_title))

	elif pagina == 'KASSANDR-COLD-START':
		st.title('Novos usuários na base de dados do KASSANDR')
		st.write('Escolha as 5 categorias que mais tem interesse')
	#fazer um dicionario com category_name : category_id



	#st.success(results1)
	#st.success(results2)


if __name__ == '__main__':
	main()