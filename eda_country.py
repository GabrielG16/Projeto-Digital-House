import streamlit as st
import pandas as pd
import graphs
#import SessionState

#MUDAR TODA A PAGINA PARA MULTISELECT E USAR AS FUNÇÕES ISIN PARA TESTAR PERFORMANCE

def nova_pagina_eda_country():

    st.title('Análise do comportamento dos consumidores por país')
    st.caption('Perfil de comportamento de compra com base nas categorias acessadas por país.')
    st.subheader('Distribuições das categorias mais populares por país')
    union = graphs.loading_union()


    select_country = st.multiselect('País', union.CountryCode.unique(), union.CountryCode.unique())
    union_corte = union[union.CountryCode.isin(select_country)]

    try:
        graphs.lista_top10_categorias(union_corte)
    except:
        st.write("Selecione pelo menos um país.")

    selection = pd.Series(union_corte.filha_1_name.unique()).sort_values()
    categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()
    st.subheader('Produtos mais clicados entre as categorias disponíveis')
    st.caption('Países selecionados:')

    #display dos países selecionados
    for i in select_country:
        if i == 'fr':
            st.write('-','França')
        elif i =='de':
            st.write('-','Alemanha')
        elif i == 'it':
            st.write('-','Itália')

    #st.write(select_country)
    super_categoria_escolhida = st.selectbox('Seleciona uma categoria', categorias_disponiveis)


    union_corte_2 = union_corte[union_corte.filha_1_name == super_categoria_escolhida]

    if st.button('Gerar'):
        graphs.filtro_por_produtos_por_super_categorias_eda_country(super_categoria_escolhida, union_corte_2)
        st.write('Categoria ', super_categoria_escolhida, 'tem como categorias filhas: \n')
        tabela_gerada = pd.DataFrame(union_corte_2.Translate.unique())
        tabela_gerada.columns = ['Categorias Filhas']
        st.table(tabela_gerada)


