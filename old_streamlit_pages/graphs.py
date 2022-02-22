import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#carregar os dados deixando no cache

#quando usamos o st.cache não pdoemos mudar o dado no progresso do meu codigo

#tentar mudar os ponteiros das variaveis com o .copy

#juntar funções de carregamento

#pensar em loading data separadamente no cache para debugar e ver se a performance melhora

#filtrar por categoria e jogar a regra de associação dentro da categoria


def loading_sparse_category():
    origin_path = os.getcwd()
    et_path = '/DH/Projeto/KASSANDR/GIT/Projeto-Digital-House'

    path_sparse = '/.csv/sparse_melt.csv'
    sparse = pd.read_csv(origin_path + et_path + path_sparse)

    path_category = '/.csv/translations.csv'
    category = pd.read_csv(origin_path + et_path + path_category, sep=';')

    return sparse, category

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_union():

    #df = pd.read_csv(r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\all_countries.csv')

    #vou tentar coemçar a trabalhar com os novos samples

    # path_it = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\italia.csv'
    # italia = pd.read_csv(path_it)
    #
    # path_fr = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\franca.csv'
    # franca = pd.read_csv(path_fr)
    #
    # path_de = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\alemanha.csv'
    # alemanha = pd.read_csv(path_de)
    #
    # path_de_it = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\alemanha_italia.csv'
    # alemanha_italia = pd.read_csv(path_de_it)
    #
    # path_fr_de = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\franca_alemanha.csv'
    # franca_alemanha = pd.read_csv(path_fr_de)
    #
    # path_fr_it = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\franca_italia.csv'
    # franca_italia = pd.read_csv(path_fr_it)


    path_union = r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\user_graphs_csv\union.csv'
    df_all = pd.read_csv(path_union)

    '''if country == 'frde':
        mask = (df['country'] == 'fr') | (df['country'] == 'de')
        franca_alemanha = df.loc[mask, :]
    elif country == 'frit':
        mask = (df['country'] == 'fr') | (df['country'] == 'it')
        franca_italia = df.loc[mask, :]
    elif country == 'deit':
        mask = (df['country'] == 'de') | (df['country'] == 'it')
        alemanha_italia = df.loc[mask, :]
    elif country == 'fr':
        franca = df.loc[df['country'] == 'fr', :]
    elif country == 'de':
        alemanha = df.loc[df['country'] == 'de', :]
    elif country == 'it':
        italia = df.loc[df['country'] == 'it', :]
    elif country == 'all':
        # essa condicional não seria necessária, só esta aqui para compreensão
        # mask = (df['country'] == 'de') | (df['country'] == 'it') | (df['country'] == 'fr')
        df_all = df.copy()'''

    #return italia, franca, alemanha, franca_alemanha, franca_italia, alemanha_italia, df_all
    return df_all

def user_graph_old_bkp(sparse, category, usuario):

    sparse['c_name'] = sparse.Category.map(dict(zip(category.Category, category.Translate)))
    tentativa = (sparse['User'] == usuario) & (sparse['Clicked?'] == 1)
    df_user = sparse.loc[tentativa, :]
    pt = pd.DataFrame(df_user['c_name'].value_counts()).reset_index()
    pt.columns = ['c', 'qt']
    pt = dict(zip(pt.c, pt.qt))
    df_user['most_clicked_categories'] = df_user['c_name'].map(pt)
    df_user.sort_values(by=['most_clicked_categories'], inplace=True, ascending=False)

    fig, ax = plt.subplots(figsize=(15, 8))
    plt.title('Most Clicked Categories')
    ax.bar(df_user.c_name, df_user.most_clicked_categories)
    plt.xticks(rotation=80)

    return fig

def lista_categorias_do_usuario(df, user):
    fig = plt.figure(figsize=(12, 8))
    df = df[df.UserId == user]
    order_filt = df.category_translate.value_counts().iloc[:10].index
    sns.countplot(y='category_translate', hue='CountryCode', data=df, order=order_filt)

def lista_produtos_do_usuario(df, user):
    fig = plt.figure(figsize=(12, 8))
    filtro = df[(df.UserId == user)]
    #order_filt = filtro.OfferTitle.value_counts().iloc[:number].index
    #sns.countplot(y='OfferTitle', hue='CountryCode', data=filtro, order=order_filt)
    sns.countplot(y='OfferTitle', hue='category_translate', data=filtro)

def lista_produtos_por_categoria_usuario(choose, df, user):
    fig = plt.figure(figsize=(12, 8))
    filtro = df[(df.UserId == user) & (df.category_translate == choose)]
    sns.countplot(y='OfferTitle', data=filtro)

# def corte_union(df, country):
#     if country == 'frde':
#         mask = (df['country'] == 'fr') | (df['country'] == 'de')
#         df = df.loc[mask, :]
#     elif country == 'frit':
#         mask = (df['country'] == 'fr') | (df['country'] == 'it')
#         df = df.loc[mask, :]
#     elif country == 'deit':
#         mask = (df['country'] == 'de') | (df['country'] == 'it')
#         df = df.loc[mask, :]
#     elif country == 'all':
#         # essa condicional não seria necessária, só esta aqui para compreensão
#         mask = (df['country'] == 'de') | (df['country'] == 'it') | (df['country'] == 'fr')
#         df = df.loc[mask, :]
#     else:
#         df = df.loc[df['country'] == country, :]
#     # elif country == 'fr':
#     #     df = df.loc[df['country'] == 'fr', :]
#     # elif country == 'de':
#     #     df = df.loc[df['country'] == 'de', :]
#     # elif country == 'it':
#     #     df = df.loc[df['country'] == 'it', :]
#     return df


def filtro_por_categoria(choose, df, number):
    fig = plt.figure(figsize=(12, 8))
    filtro = df.loc[df.category_translate == choose]
    order_filt = filtro.OfferTitle.value_counts().iloc[:number].index
    sns.countplot(y='OfferTitle', hue='CountryCode', data=filtro, order=order_filt)
    st.pyplot(fig)


def lista_top10_categorias(df):
    fig = plt.figure(figsize=(12, 8))
    order_filt = df.category_translate.value_counts().iloc[:10].index
    sns.countplot(y='category_translate', hue='CountryCode', data=df, order=order_filt)
    st.pyplot(fig)