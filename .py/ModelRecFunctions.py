import os
import pickle
from scipy.sparse import load_npz
import random
import pandas as pd


def recommend(user, k=10, country='de'):

    """Retorna uma lista de itens recomendados para o usuário dado de acordo com a biblioteca Implicit.
        Também é retornado uma lista com os itens já clicados por esse usuário"""

    if country == 'de':
        model = 'x'
        sparse_user_item = 'y'
    elif country == 'fr':
        model = 'x'
        sparse_user_item = 'y'
    else:
        model = 'x'
        sparse_user_item = 'y'

    if user not in sparse_user_item.T.tocsr().indices:
        return "Invalid User"

    recommended, scores = (model.recommend(user, sparse_user_item[user], k))

    original_user_items = list(sparse_user_item[user].indices)

    return recommended, original_user_items


def most_similar_users(user_id, n_similar=10, country='de'):

    """computes the most similar users and which items they have in common with the user"""

    model_path = os.getcwd()+'/.pkl/'+country+'/offer_cat.pkl'
    sparse_path = os.getcwd()+'/.npz/'+country+'/sparse_user_item.npz'

    with open(model_path, 'rb') as path:
        model = pickle.load(path)
    sparse_user_item = load_npz(sparse_path)

    similar, scores = model.similar_users(user_id, n_similar, filter_users=[user_id])

    # original users items
    original_user_items = list(sparse_user_item[user_id].indices)
    common_items_users = {}

    # now we want to add the items that a similar user has rated
    for user in similar:

        common_items_users[user] = set(list(sparse_user_item[user].indices)) & set(original_user_items)

    return similar, common_items_users


def most_similar_items(item_id, n_similar=10, country='de'):

    """computes the most similar items"""

    model_path = os.getcwd()+'/.pkl/'+country+'/offer_cat.pkl'
    with open(model_path, 'rb') as path:
        model = pickle.load(path)

    similar, score = model.similar_items(item_id, n_similar, filter_items=[item_id])

    return similar


def suggestions(user_id, k=500, n_best_seller=2, country='de'):

    """
    Retorna recomendações segmentadas de acordo com as categorias clicadas pelo usuário passado.
    À lista de recomendações são adicionados dois top 10 best-sellers da categoria em questão

      Inputs:

       user_id -> ID categórico do usuário

       k -> Quantidade de sugestões que serão retornadas somente pelo modelo

       n_best_seller -> Quantidade de sugestões que serão retornadas por popularidade em cada categoria considerada

       Output:

       cat_suggestions -> Dicionário com as sugestões agrupadas por categoria já clicada pelo usuário

       original -> Array com os clicks originais do usuário selecionado
    """
    sparse_path = os.getcwd()+'/.npz/'+country+'/sparse_user_item.npz'
    with open(sparse_path, 'rb') as path:
        sparse_user_item = pickle.load(path)

    offer_cat_path = os.getcwd()+'/.pkl/'+country+'/offer_cat.pkl'
    with open(offer_cat_path, 'rb') as path:
        offer_cat = pickle.load(path)

    products_info_path = os.getcwd()+'/.csv/'+country+'/products_info.csv'
    with open(products_info_path, 'rb') as path:
        products_info = pickle.load(path)

    if not len(sparse_user_item[user_id].indices):
        return "Invalid User"

    cat_suggestions = {}
    recs, original = recommend(user_id, k)
    pd_recs = pd.DataFrame((recs, [offer_cat.get(key) for key in recs])).T.rename({0: 'Offer', 1: 'Category'}, axis=1)

    best_cat = pd.Series(offer_cat[cat] for cat in original).value_counts().index

    for i in range(len(best_cat)):

        if len(pd_recs[pd_recs.Category == best_cat[i]]) != 0:  #
            pop_recs = products_info[products_info.Category == best_cat[i]][:20]
            pop_recs = pop_recs[pop_recs.Offer.isin(original) is False]

            pop_recs = random.sample(pop_recs.Offer.values.tolist(), pop_recs.shape[0])[:n_best_seller]

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
