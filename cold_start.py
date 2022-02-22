import pandas as pd
import streamlit as st
import os
import pickle

origin_path = os.getcwd()
et_path = ''

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_dataset():
    path_de = origin_path + et_path + '/.csv/.novo/all_countries.csv'
    all_countries = pd.read_csv(path_de)

    # top3_path = origin_path + et_path + '/.csv/top3_per_category_de.csv'
    # top3_de = pd.read_csv(top3_path)

    # path_it = origin_path + et_path + '/.csv/clicks_de.csv'
    # italia = pd.read_csv(path_it)
    #
    # path_fr = origin_path + et_path + '/.csv/clicks_de.csv'
    # franca = pd.read_csv(path_it)

    #aqui possivelmente vai ter as sparsas dos 3 paises

    return all_countries

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_dicionarios():

    path_de = origin_path + et_path + '/.pkl/alemanha/dicionario_super_sub_categorias_cold_start_alemanha.pkl'
    alemanha = pickle.load(open(path_de, 'rb'))

    path_fr = origin_path + et_path + '/.pkl/france/dicionario_super_sub_categorias_cold_start_france.pkl'
    france = pickle.load(open(path_fr, 'rb'))

    path_it = origin_path + et_path + '/.pkl/italia/dicionario_super_sub_categorias_cold_start_italia.pkl'
    italia = pickle.load(open(path_it, 'rb'))


    return alemanha, france, italia
# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
# def recebe_categorias(lista_categorias, df):
#     import warnings
#     warnings.filterwarnings('ignore')
#
#     df = df.loc[df.category_translate.isin(lista_categorias), :]
#     contagem = pd.DataFrame(df.OfferTitle.value_counts().reset_index())
#     contagem.columns = ['oferta', 'contagem']
#     contagem = dict(zip(contagem.oferta, contagem.contagem))
#     df['popularidade_clicks'] = df.OfferTitle.map(contagem)
#     df.sort_values(by=['popularidade_clicks'], inplace=True)
#
#     best_itens = []
#     scores = pd.DataFrame(columns=['Category', 'OfferTitle'])
#     for item in lista_categorias:
#         listinha = []
#         # print(item)
#         listinha = list(df.loc[df.category_translate == item, ['OfferTitle']].drop_duplicates().OfferTitle)
#         listinha = listinha[:3]
#         for i in listinha:
#             # print(item)
#             # print(i)
#             dict_itens = {'Category': item, 'OfferTitle': i}
#             scores = scores.append(dict_itens, ignore_index=True)
#
#     return scores

def recebe_categorias_retorna_produtos(categorias_selecionadas, dicionario_categorias, df):
    for categoria in categorias_selecionadas:
        st.write('Porque você tem interesse em --', str(categoria), '-- achamos que gostaria destes produtos: \n')
        for cat in dicionario_categorias[categoria]:
            #         print('Porque você tem interesse em ', categoria, 'achamos que gostaria destes produtos em: ',cat)
            if len(dicionario_categorias[categoria]) == 1:
                for i in range(4):
                    st.write('-', df[df.Translate == cat].OfferTitle.unique()[i])
            elif len(dicionario_categorias[categoria]) == 2:
                for i in range(2):
                    st.write('-', df[df.Translate == cat].OfferTitle.unique()[i])
            elif len(dicionario_categorias[categoria]) == 3:
                for i in range(2):
                    st.write('-', df[df.Translate == cat].OfferTitle.unique()[i])
            elif len(dicionario_categorias[categoria]) == 4:
                for i in range(1):
                    st.write('-', df[df.Translate == cat].OfferTitle.unique()[i])
            elif len(dicionario_categorias[categoria]) == 5:
                if df[df.Translate == cat].OfferTitle.unique().size != 0:
                    st.write('-', df[df.Translate == cat].OfferTitle.unique()[0])
        st.write('\n')
        st.write('\n')

def cold_start_page():
    union = loading_dataset()
    dicionario_alemanha, dicionario_france, dicionario_italia = loading_dicionarios()

    pais_selecionado = st.selectbox('Selecione um pais:', ['França','Alemanha','Itália'])

    #aqui a ideia é a pessoa escolher o pais e ser apresentado as categorias disponiveis naquele país!

    if pais_selecionado == 'França':
        #st.write('frança')
        df = union[union.CountryCode == 'fr']
        dicionario_categorais = dicionario_france
    elif pais_selecionado == 'Alemanha':
        df = union[union.CountryCode == 'de']
        dicionario_categorais = dicionario_alemanha
    elif pais_selecionado == 'Itália':
        df = union[union.CountryCode == 'it']
        dicionario_categorais = dicionario_italia


    st.title('Insira as categorias que o usuario mais tem interesse')
    # st.title('Novos usuários na base de dados do KASSANDR')
    #st.write('Escolha as 5 categorias que mais tem interesse')

    categorias = df.filha_1_name.unique()
    select_category = st.multiselect('Categorias', categorias)#, categorias)

    if st.button('Gerar'):
        recebe_categorias_retorna_produtos(select_category, dicionario_categorais, df)


# essa função de cold start, está pegando as categorias "mães" e selecionando as sub_categorias mais clicadas
# com isso, eu pego 1 produto ou dois, dependendo de quantas categorias existem dentro da supercategoria


