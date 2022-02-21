import pandas as pd
import streamlit as st
import os


origin_path = os.getcwd()
et_path = ''

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_dataset():
    path_de = origin_path + et_path + '/.csv/.novo/all_countries.csv'
    all_countries = pd.read_csv(path_de)

    top3_path = origin_path + et_path + '/.csv/top3_per_category_de.csv'
    top3_de = pd.read_csv(top3_path)

    # path_it = origin_path + et_path + '/.csv/clicks_de.csv'
    # italia = pd.read_csv(path_it)
    #
    # path_fr = origin_path + et_path + '/.csv/clicks_de.csv'
    # franca = pd.read_csv(path_it)

    #aqui possivelmente vai ter as sparsas dos 3 paises

    return all_countries, top3_de#, franca, italia

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

def cold_start_page():
    union, top3 = loading_dataset()

    pais_selecionado = st.selectbox('Selecione um pais:', ['França','Alemanha','Itália'])

    #aqui a ideia é a pessoa escolher o pais e ser apresentado as categorias disponiveis naquele país!

    if pais_selecionado == 'França':
        #st.write('frança')
        df = union[union.CountryCode == 'fr']
    elif pais_selecionado == 'Alemanha':
        df = union[union.CountryCode == 'de']
    elif pais_selecionado == 'Itália':
        df = union[union.CountryCode == 'it']


    st.title('Insira as categorias que o usuario mais tem interesse')
    # st.title('Novos usuários na base de dados do KASSANDR')
    #st.write('Escolha as 5 categorias que mais tem interesse')

    categorias = df.filha_1_name.unique()
    select_category = st.multiselect('Categorias', categorias)#, categorias)

    #if st.button('recommend'):
        #aqui chamo a função para retornar as categorias em um dataframe
        #retornando_categorias_selecionadas = recebe_categorias(select_category, alemanha)
        #st.write(retornando_categorias_selecionadas)
        # st.write('Data Dimension: ' + str(retornando_categorias_selecionadas.shape[0]) + ' rows and ' + str(retornando_categorias_selecionadas.shape[1]) + ' columns.')
        #st.dataframe(retornando_categorias_selecionadas, 1000, 1000)
        #st.write('você selecionou ', select_category)

        #nova tentativa, carregando o dataset com os itens populares

    #aqui poderia ser feito um n_recomendations, que lista quantos produtos a pessoa quer por categoria
    #deixando limitado para 10 o numero maximo
    #e fazendo um csv, com as top10 produtos por categoria de cada pais, e não 3

    df_top3_desejado = top3[top3.Category.isin(select_category)]
    # st.write('Dimensão dos dados: ')
    # st.write(df_top3_desejado.shape[0], ' linhas')
    # st.write(df_top3_desejado.shape[1], ' colunas')
    st.table(df_top3_desejado)


