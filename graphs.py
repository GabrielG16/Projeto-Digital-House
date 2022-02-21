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

origin_path = os.getcwd()
et_path = ''

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_union():

    path_union = origin_path + et_path + '/.csv/.novo/all_countries.csv'
    df_all = pd.read_csv(path_union)

    return df_all

def lista_categorias_do_usuario(df, user):
    fig = plt.figure(figsize=(12, 8))
    df = df[df.User == user]
    sns.countplot(y='Translate', data = df)
    plt.title('Categorias clicadas pelo Usuário')
    plt.xlabel('Cliques')
    plt.ylabel('Categorias')
    st.pyplot(fig)

def lista_produtos_do_usuario(df, user):
    fig = plt.figure(figsize=(12, 8))
    filtro = df[(df.UserId == user)]
    #order_filt = filtro.OfferTitle.value_counts().iloc[:10].index
    #sns.countplot(y='OfferTitle', hue='CountryCode', data=filtro, order=order_filt)
    sns.countplot(y='OfferTitle', hue='Translate', data=filtro)

def lista_produtos_por_categoria_usuario(choose, df, user):
    fig = plt.figure(figsize=(12, 8))
    filtro = df[(df.UserId == user) & (df.category_translate == choose)]
    sns.countplot(y='OfferTitle', data=filtro)


#EDA_country


def lista_top10_categorias(df):
    fig = plt.figure(figsize=(12,8))
    order_filt = df.filha_1_name.value_counts().iloc[:10].index
    sns.countplot(y='filha_1_name', hue = 'CountryCode',data = df, order = order_filt)
    plt.ylabel('Super Categorias')
    plt.xlabel('Contagem')
    #plt.show()
    st.pyplot(fig)


def lista_top10_categorias_1_pais_eda_country(choose, df):
    fig = plt.figure(figsize=(12, 8))
    filtro = df.loc[df.category_translate == choose]
    order_filt = filtro.OfferTitle.value_counts().iloc[:10].index
    sns.countplot(y='OfferTitle', data=filtro, order=order_filt)
    st.pyplot(fig)

def filtro_por_categoria_eda_country(choose, df):
    fig = plt.figure(figsize=(15, 15))
    filtro = df.loc[df.filha_1_name == choose]
    #order_filt = filtro.Translate.value_counts().iloc[:10].index
    order_filt = filtro.Translate.value_counts().index
    sns.countplot(y='Translate', hue='CountryCode', data=filtro, order=order_filt)
    plt.ylabel('Sub Categorias')
    plt.xlabel('Contagem')
    st.pyplot(fig)

def filtro_por_produtos_por_super_categorias_eda_country(choose, df):
    fig = plt.figure(figsize=(15, 15))
    filtro = df.loc[df.filha_1_name == choose]
    order_filt = filtro.OfferTitle.value_counts().iloc[:10].index
    #order_filt = filtro.OfferTitle.value_counts().index
    sns.countplot(y='OfferTitle', hue='CountryCode', data=filtro, order=order_filt)
    plt.ylabel('Sub Categorias')
    plt.xlabel('Contagem')
    st.pyplot(fig)

def lista_produtos_sub_categorias():
    return