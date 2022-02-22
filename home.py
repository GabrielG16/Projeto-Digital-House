import streamlit as st
import pandas as pd
import os

origin_path = os.getcwd()
et_path = '/DH/Projeto/KASSANDR/Streamlit_finalversion/' # no caso pode deixar em branco ''


def home_page():
    st.title('KASSANDR RECOMMENDATION SYSTEM')
    st.subheader('Elias Tolentino & Gabriel Guedes & José Eduardo')

    st.write('''Dado o crescente número de escolhas possíveis para usuários,
     especialmente quando se trata de compras online, começamos a notar a necessidade de Sistemas de Recomendação como essenciais para vivência e experiência online.''')
    st.write('''Os sistemas de recomendações têm como foco capturar as preferencias de um determinado usuário ou grupo de usuários,
      conforme essas preferências sugerir uma lista de itens ou produtos que podem ser do interesse do usuário.''')

    #st.write('Resolvemos usar os dados disponibilizados pelo projeto KASANDR - Kelkoo lArge ScAle juNe Data for Recommendation')


    #st.image()

    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image("https://4fle1816f3va1wuk891mb5nk-wpengine.netdna-ssl.com/wp-content/uploads/2020/01/kelkoo-logo-600-new.png")
        with text_col:
            st.write('Resolvemos usar os dados disponibilizados pelo projeto KASANDR - Kelkoo lArge ScAle juNe Data for Recommendation')
            st.write('Contemplando mais de 20 paises Europeus, com dados disponíveis de 3 países - Alemanha, França e Itália')
            st.write('16M de cliques - 123M de clientes - 56M de ofertas - dados não restritos')


    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image('https://upload.wikimedia.org/wikipedia/commons/b/ba/Flag_of_Germany.svg')
        with text_col:
            st.write('Alemanha')
            st.write('270 categorias diversas, mais de 607 mil produtos diversos e com mais de 800 mil cliques')

    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/1024px-Flag_of_Italy.svg.png')
        with text_col:
            st.write('Itália')
            st.write('288 categorias diversas, mais de 700mil produtos e quase 2M de cliques')

    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_France_%281794%E2%80%931815%2C_1830%E2%80%931974%2C_2020%E2%80%93present%29.svg/1024px-Flag_of_France_%281794%E2%80%931815%2C_1830%E2%80%931974%2C_2020%E2%80%93present%29.svg.png')
        with text_col:
            st.write('França')
            st.write('311 categorias diversas, mais de 725 mil produtos diversos e com mais de 2M de cliques')


    st.write('\n\n dimensões dos dados disponibilizados: ')

    #st.image(origin_path + et_path + '.images\dimensoes_dados.PNG')
    dimensoes = pd.DataFrame({'File_name': ['Page_View','Search','Offers','Click','Product_Cat','train_set','test_set'],
                              'Format': ['csv','csv','csv','csv','xml','csv','csv'],
                              'Features':['UserId, CountryCode, Timestamp,Url','SearchId, UserId, CountryCode, isPrompt, Timestamp, QueryString', 'OfferId,OfferViewId, UserId, OfferRank, Merchant, price,Timestamp, CountryCode',
                                          'ClickId, UserId, OfferId, OfferViewId, CountryCode, Category, Source, Timestamp, Keywords, OfferTitle',
                                          'id and labels of prodct category presented as a tree',
                                          'UserId, OfferId, Service Type, ProductCategory, Country, Merchant, Feedback (1 or -1)',
                                          'UserId, OfferId, Service Type, ProductCategory, Country, Merchant, Feedback (1 or -1)']
                              })
    st.table(dimensoes)
    st.write('\n\n Foi usado cortes dos dataframes originais para facilitar o processamento de dados e melhora das métricas usadas \n\n')
    # st.markdown('Criado por: '
    #             Elias Tolentino')
    # st.write('Elias Tolentino ')
    # st.write('Gabriel Guedes')
    # st.write('José Eduardo  \n\n')
    #st.markdown('WebApp para analise de um sistema de recomendação sobre cliques de compras do mês de junho de 2016 do site KELKO')