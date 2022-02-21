import os
import pickle
from scipy.sparse import load_npz
import random
import pandas as pd
import streamlit as st

origin_path = os.getcwd()
et_path = ''
#et_path = '/DH/Projeto/KASSANDR/Streamlit_finalversion/' # no caso pode deixar em branco ''

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_model():

    path_model_de = '/.pkl/alemanha/alemanha_als_model.pkl'
    de_model = pickle.load(open((origin_path + et_path + path_model_de), 'rb'))

    path_model_it = '/.pkl/italia/italia_als_model.pkl'
    it_model = pickle.load(open((origin_path + et_path + path_model_it), 'rb'))

    path_model_fr = '/.pkl/france/france_als_model.pkl'
    fr_model = pickle.load(open((origin_path + et_path + path_model_fr), 'rb'))



    return de_model, it_model, fr_model

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_sparse():
    path_sparse_de = origin_path + et_path + '/.npz/alemanha/sparse_user_item_alemanha.npz'
    sparse_de = load_npz(path_sparse_de)

    path_sparse_it = origin_path + et_path + '/.npz/italia/sparse_user_item_italia.npz'
    sparse_it = load_npz(path_sparse_it)

    path_sparse_fr = origin_path + et_path + '/.npz/france/sparse_user_item_france.npz'
    sparse_fr = load_npz(path_sparse_fr)


    return sparse_de, sparse_it, sparse_fr

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_offers():
    path_offer_de = '/.pkl/alemanha/offers_alemanha.pkl'
    offer_de = pickle.load(open((origin_path + et_path + path_offer_de),'rb'))

    path_offer_it =  '/.pkl/italia/offers_italia.pkl'
    offer_it = pickle.load(open((origin_path + et_path + path_offer_it),'rb'))

    path_offer_fr = '/.pkl/france/offers_france.pkl'
    offer_fr = pickle.load(open((origin_path + et_path + path_offer_fr),'rb'))

    return offer_de, offer_it, offer_fr

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_offer_cat():
    path_offer_de = '/.pkl/alemanha/offers_cat_alemanha.pkl'
    offer_cat_de = pickle.load(open((origin_path + et_path + path_offer_de), 'rb'))

    path_offer_it = '/.pkl/italia/offers_cat_italia.pkl'
    offer_cat_it = pickle.load(open((origin_path + et_path + path_offer_it), 'rb'))

    path_offer_fr = '/.pkl/france/offers_cat_france.pkl'
    offer_cat_fr = pickle.load(open((origin_path + et_path + path_offer_fr), 'rb'))

    return offer_cat_de, offer_cat_it, offer_cat_fr

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_products_info():
    path_products_de = origin_path + et_path + '/.products/alemanha/products_info_alemanha.csv'
    products_de = pd.read_csv(path_products_de)

    path_products_it = origin_path + et_path + '/.products/italia/products_info_italia.csv'
    products_it = pd.read_csv(path_products_it)

    path_products_fr = origin_path + et_path + '/.products/france/products_info_france.csv'
    products_fr = pd.read_csv(path_products_fr)


    return products_de, products_it, products_fr


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_cat_name():
    path_cat_name_de = '/.pkl/alemanha/cat_name_alemanha.pkl'
    cat_name_de = pickle.load(open((origin_path + et_path + path_cat_name_de), 'rb'))

    path_cat_name_it = '/.pkl/italia/cat_name_italia.pkl'
    cat_name_it = pickle.load(open((origin_path + et_path + path_cat_name_it), 'rb'))

    path_cat_name_fr = '/.pkl/france/cat_name_france.pkl'
    cat_name_fr = pickle.load(open((origin_path + et_path + path_cat_name_fr), 'rb'))


    return cat_name_de, cat_name_it, cat_name_fr

def recommend(user, model, sparse_user_item, k=10):

    """Retorna uma lista de itens recomendados para o usuário dado de acordo com a biblioteca Implicit.
        Também é retornado uma lista com os itens já clicados por esse usuário"""

    # if country == 'de':
    #     model = 'x'
    #     sparse_user_item = 'y'
    # elif country == 'fr':
    #     model = 'x'
    #     sparse_user_item = 'y'
    # else:
    #     model = 'x'
    #     sparse_user_item = 'y'
    #
    # if user not in sparse_user_item.T.tocsr().indices:
    #     return "Invalid User"

    recommended, scores = (model.recommend(user, sparse_user_item[user], k))

    original_user_items = list(sparse_user_item[user].indices)

    return recommended, original_user_items


def most_similar_users(user_id, model, sparse_user_item, n_similar=10):

    """computes the most similar users and which items they have in common with the user"""

    similar, scores = model.similar_users(user_id, n_similar, filter_users=[user_id])

    # original users items
    original_user_items = list(sparse_user_item[user_id].indices)
    common_items_users = {}

    # now we want to add the items that a similar user has rated
    for user in similar:

        common_items_users[user] = set(list(sparse_user_item[user].indices)) & set(original_user_items)

    return similar, common_items_users


def most_similar_items(item_id, model, n_similar=10):

    """computes the most similar items"""

    # model_path = os.getcwd()+'/.pkl/'+country+'/offer_cat.pkl'
    # with open(model_path, 'rb') as path:
    #     model = pickle.load(path)

    similar, score = model.similar_items(item_id, n_similar, filter_items=[item_id])

    return similar


def suggestions(user_id, model, sparse, offer_cat, products_info):
    cat_suggestions = {}
    recs, original = recommend(user_id, model, sparse, k=300)

    pd_recs = pd.DataFrame((recs, [offer_cat.get(key) for key in recs])).T.rename({0: 'Offer', 1: 'Category'}, axis=1)

    best_cat = pd.Series(offer_cat[cat] for cat in original).value_counts().index

    for i in range(len(best_cat)):

        if len(pd_recs[pd_recs.Category == best_cat[i]]) != 0:  #
            pop_recs = products_info[products_info.Category == best_cat[i]][:20]
            pop_recs = pop_recs[pop_recs.Offer.isin(original) == False]

            pop_recs = random.sample(pop_recs.Offer.values.tolist(), pop_recs.shape[0])[:2]

            pop_recs.extend(pd_recs[pd_recs.Category == best_cat[i]].Offer.values[:3].tolist())
            cat_suggestions[best_cat[i]] = pop_recs

    others = []  # Verificar sugestões de categorias que nunca foram clicadas pelo usuário
    for row in pd_recs.index[:15]:
        if pd_recs.Category.values[row] not in best_cat.values:
            others.append(pd_recs.Offer.values[row])
    random.shuffle(others)
    others = others[:5]

    cat_suggestions['Others'] = others

    return cat_suggestions, original

def print_offers_name_on_streamlit(list_of_items, offer_title):

	lista = []
	for item in list_of_items:
		 lista.append(offer_title[item])

	return lista


def print_streamlit(cat_suggestions, original, cat_name, offer):
    for c in cat_suggestions.keys():
        if len(cat_suggestions[c]) > 0 and c!='Others':
            st.write('\n**Porque você clicou na seção**', '**_'+cat_name[c]+'_**', "**em:** \n")
            st.write(pd.Series(print_offers_name_on_streamlit(original[:5],offer), name='Items'))
            # for item in original[:5]:
            #     st.write(offer[item])
            st.write("\n", '**Achamos que você talvez também goste:**', "\n")
            st.write('')
            st.write(print_offers_name_on_streamlit(cat_suggestions[c], offer))
            # for item in cat_suggestions[c]:
            #     st.write(offer[item])
    if len(cat_suggestions['Others']) > 0:
        st.write("\n", 'Achamos que você talvez também pode gostar:', "\n")
        st.write('')
        st.write(print_offers_name_on_streamlit(cat_suggestions['Others'][:5], offer))
        # for item in cat_suggestions['Others']:
        #     st.write(offer[item])


