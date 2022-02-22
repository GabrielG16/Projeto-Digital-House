import streamlit as st
import pandas as pd
import ModelRecFunctions as MRF

de_model, it_model, fr_model = MRF.loading_model()
sparse_de, sparse_it, sparse_fr = MRF.loading_sparse()
offer_de, offer_it, offer_fr = MRF.loading_offers()
offer_cat_de, offer_cat_it, offer_cat_fr = MRF.loading_offer_cat()
products_info_de, products_info_it, products_info_fr = MRF.loading_products_info()
cat_name_de, cat_name_it, cat_name_fr = MRF.loading_cat_name()

def kassandr_user_page():

    st.title('Product Recommender System Web App - KASANDR (DE)')

    country = st.selectbox('Selecione um país:', ['França','Alemanha','Italia'])


#ajeitando os ponteiros para o modelo escolhido!

    if country == 'França':
        model = fr_model
        sparse_user_item = sparse_fr
        offer = offer_fr
        offer_cat = offer_cat_fr
        products_info = products_info_fr
        cat_name = cat_name_fr

    elif country == 'Alemanha':
        model = de_model
        sparse_user_item = sparse_de
        offer = offer_de
        offer_cat = offer_cat_de
        products_info = products_info_de
        cat_name = cat_name_de


    elif country == 'Italia':
        model = it_model
        sparse_user_item = sparse_it
        offer = offer_it
        offer_cat = offer_cat_it
        products_info = products_info_it
        cat_name = cat_name_it



    #Input Data

    user_disponiveis = list(sparse_user_item.T.tocsr().indices)
    user_disponiveis.sort()
    user_disponiveis = list(dict.fromkeys(user_disponiveis))
    st.write('Usuários Disponíveis: ', len(user_disponiveis))

    user_id = st.selectbox('Selecione um usuario:', user_disponiveis)

    #n_recs = st.slider('Number of recommentations:', min_value = 1, max_value = 100)

    #Code for prediction
    results = ''

    #Recommendation Button
    if st.button('Recommend'):

        recommended_items, clicked_items = MRF.suggestions(user_id, model, sparse_user_item, offer_cat, products_info)
        #col1, col2 = st.columns(2)
        #col1.header('Recommended:')
        #col1.write(MRF.print_offers_name_on_streamlit(recommended_items, offer))
        MRF.print_streamlit(recommended_items, clicked_items, cat_name, offer, offer_cat, products_info)


def kassandr_userbyuser_page():
    return
    # st.title('User by User')
    # user_disponiveis = list(sparse_user_item.T.tocsr().indices)
    # user_id = st.selectbox('Selecione um usuario:', user_disponiveis)
    # #
    # if st.button('Similar Users'):
    #     similar, common = MRF.most_similar_users(user_id, sparse_user_item,model)
    #     st.write(similar)
    #     st.write(common)
    #     #st.write(imp_recomender.print_offers_name_on_streamlit(common, offer_title))