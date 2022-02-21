import streamlit as st
import pandas as pd
import graphs
#import SessionState

#MUDAR TODA A PAGINA PARA MULTISELECT E USAR AS FUNÇÕES ISIN PARA TESTAR PERFORMANCE

def nova_pagina_eda_country():

    st.title('Distribuições dos Países')
    union = graphs.loading_union()


    select_country = st.multiselect('País', union.CountryCode.unique(), union.CountryCode.unique())
    union_corte = union[union.CountryCode.isin(select_country)]
    graphs.lista_top10_categorias(union_corte)


    selection = pd.Series(union_corte.filha_1_name.unique()).sort_values().str.title()
    categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

    super_categoria_escolhida = st.selectbox('Seleciona uma categoria', categorias_disponiveis)
    #n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

    #contador = len(select_country)

    #st.session_state.super_categoria_escolhida = super_categoria_escolhida
    union_corte_2 = union_corte[union_corte.filha_1_name == super_categoria_escolhida]

    if st.button('Gerar'):
        graphs.filtro_por_produtos_por_super_categorias_eda_country(super_categoria_escolhida, union_corte_2)
        st.write('Categoria ', super_categoria_escolhida, 'tem como categorias filhas: \n')
        st.table(pd.DataFrame(union_corte_2.Translate.unique()))

