import pickle
import pandas as pd
import streamlit as st

import os

import matplotlib.pyplot as plt
import app_functions

#importando as paginas, funções, tudo que criamos em outros arquivos .py

#import imp_recomender
import home
import cold_start
import eda_country
import graphs
import item_exploration
import kassandr_de_user_page
import user_analise
import kassandr_de_user_page
import item_exploration



#offer_title, model, sparse_item_user, sparse_user_item, indice_itens = imp_recomender.loading_files()

def main():

	paginas = ['Início','Análise Exploratória por País', 'Análise por Usuário',
			   'Recomendação para usuário escolhido',
			   'Itens Clicados Juntos', 'Novo Usuário']

	pagina = st.sidebar.radio('Selecione uma página: ', paginas)

	if pagina == 'Início':
		home.home_page()

# pra deixar mais simples, coloquei a função de grafico em um arquivo.py separado, assim que for construindo as outras vou colocando la, pra não deixar esse arquivo mto grande tbm
# pensar em colocar as 7 tabelas carregadas separadas e quando chamar o filtro ja está feito


#Pensar sobre colocar as funções de loading_data dentro do if ou fora

	elif pagina == 'Análise Exploratória por País':
		eda_country.nova_pagina_eda_country()

	elif pagina == 'Análise por Usuário':
		user_analise.user_analise_page()

	elif pagina == 'Recomendação para usuário escolhido':
		kassandr_de_user_page.kassandr_user_page()

	# elif pagina == 'KASSANDR-USER-USER':
	# 	st.title('User by User')



	elif pagina == 'Itens Clicados Juntos':
		item_exploration.item_exploration_page()

	elif pagina == 'Novo Usuário':
		cold_start.cold_start_page()
	#fazer um dicionario com category_name : category_id



	#st.success(results1)
	#st.success(results2)


if __name__ == '__main__':
	main()