import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def loading_union():
    df = pd.read_csv(r'C:\Users\Elias-Acer\DH\Projeto\KASSANDR\ET_notebooks\all_countries.csv')

    origin_path = os.getcwd()
    et_path = '/DH/Projeto/KASSANDR/GIT/Projeto-Digital-House'

    path_sparse = '/.csv/sparse_melt.csv'
    sparse = pd.read_csv(origin_path + et_path + path_sparse)

    path_category = '/.csv/translations.csv'
    category = pd.read_csv(origin_path + et_path + path_category, sep=';')

    return df, sparse, category

def user_graph(sparse, category, usuario):

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


def corte_union(df, country):
    if country == 'frde':
        mask = (df['country'] == 'fr') | (df['country'] == 'de')
        df = df.loc[mask, :]
    elif country == 'frit':
        mask = (df['country'] == 'fr') | (df['country'] == 'it')
        df = df.loc[mask, :]
    elif country == 'deit':
        mask = (df['country'] == 'de') | (df['country'] == 'it')
        df = df.loc[mask, :]
    elif country == 'all':
        # essa condicional não seria necessária, só esta aqui para compreensão
        mask = (df['country'] == 'de') | (df['country'] == 'it') | (df['country'] == 'fr')
        df = df.loc[mask, :]
    else:
        df = df.loc[df['country'] == country, :]
    # elif country == 'fr':
    #     df = df.loc[df['country'] == 'fr', :]
    # elif country == 'de':
    #     df = df.loc[df['country'] == 'de', :]
    # elif country == 'it':
    #     df = df.loc[df['country'] == 'it', :]
    return df


def filtro_por_categoria(choose, df, number):
    fig = plt.figure(figsize=(12, 8))
    filtro = df.loc[df.c_t == choose]
    order_filt = filtro.OfferTitle.value_counts().iloc[:number].index
    sns.countplot(y='OfferTitle', hue='country', data=filtro, order=order_filt)
    st.pyplot(fig)


def lista_top10_categorias(df):
    fig = plt.figure(figsize=(12, 8))
    order_filt = df.c_t.value_counts().iloc[:10].index
    sns.countplot(y='c_t', hue='country', data=df, order=order_filt)
    st.pyplot(fig)