import streamlit as st
import pandas as pd
import graphs


#MUDAR TODA A PAGINA PARA MULTISELECT E USAR AS FUNÇÕES ISIN PARA TESTAR PERFORMANCE
def eda_country_page():
    st.title('Country Distribution')

    de = st.checkbox('Alemanha')
    fr = st.checkbox('França')
    it = st.checkbox('Italia')

    # st.write(de, fr, it)

    # italia, franca, alemanha, franca_alemanha, franca_italia, alemanha_italia, union = graphs.loading_union()

    if de and not (fr) and not (it):
        country = 'de'
        st.write('Você escolheu em ver as distribuições da alemanha')
    elif not (de) and fr and not (it):
        country = 'fr'
        st.write('Você escolheu em ver as distribuições da frança')
    elif not (de) and not (fr) and it:
        country = 'it'
        st.write('Você escolheu em ver as distribuições da Italia')
    elif de and fr and not (it):
        country = 'frde'
        st.write('Alemanha e França')
    elif fr and it and not (de):
        country = 'frit'
        st.write('França e Italia')
    elif de and not (fr) and it:
        country = 'deit'
        st.write('Alemanha e Italia')
    elif de and fr and it:
        country = 'all'
        st.write('Combinação dos 3 países')
    elif not (de) and not (fr) and not (it):
        country = False
        st.write('Selecione uma ou mais opções para gerar graficos')
    # st.write(country)

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


def nova_pagina_eda_country():
    st.title('Country Distribution')
    union = graphs.loading_union()

    select_country = st.multiselect('Position', union.CountryCode.unique(), union.CountryCode.unique())
    union_corte = union[union.CountryCode.isin(select_country)]
    graphs.lista_top10_categorias(union_corte)

    selection = pd.Series(union_corte.category_translate.unique()).sort_values().str.title()
    categorias_disponiveis = selection  # pd.Series(selection.c_t.unique()).sort_values().str.title()

    categoria_escolhida = st.selectbox('Select a category', categorias_disponiveis)
    n_prods = st.slider('Number of Products:', min_value=10, max_value=20)

    if st.button('Generate'):
        graphs.filtro_por_categoria(categoria_escolhida, union_corte, n_prods)


