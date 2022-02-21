#REVISAR PAGINA INTEIRA

import pandas as pd
import graphs
import streamlit as st
import os

origin_path = os.getcwd()
et_path = ''


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_dataset():
    path_union = origin_path + et_path + '/.csv/.novo/all_countries.csv'
    df_all = pd.read_csv(path_union)
    return df_all

def write_list_streamlit(lista):
    msg = ""
    for item in lista:
        msg = msg + item + '\n\n'
    return msg

def user_analise_page():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    union = loading_dataset()

    st.title('Análise Exploratória do usuário:')
    st.caption('Perfil do usuário gerado a partir das suas interações recentes e descrição dos produtos acessados.')
    # Input Data

    select_country = st.selectbox('Selecione um país: ', ['França', 'Alemanha', 'Itália'])


    if select_country == 'França':
        select_country = 'fr'

    elif select_country == 'Alemanha':
        select_country = 'de'

    elif select_country == 'Italia':
        select_country = 'it'


    union_corte = union[union.CountryCode == select_country]
    st.write('Usuário Disponíveis: ', len(union_corte.UserId.unique()))



    # user_disponiveis = list(sparse_item_user.indices)
    user_disponiveis = union_corte.User.unique()
    user_id = st.selectbox('Selecione um usuário:', user_disponiveis)

    # Code for prediction
    results = ''

    if st.button('Generate'):

        graphs.lista_categorias_do_usuario(union_corte, user_id)

        st.subheader('Lista dos itens clicados pelo usuário em cada categoria: ')
        produtos_nas_categorias = union_corte.loc[(union_corte.User == user_id),['Translate','OfferTitle']]
        produtos_nas_categorias.columns = ['Category', 'Products']
        st.table(produtos_nas_categorias.sort_values(by=['Category']).reset_index(drop = True))
