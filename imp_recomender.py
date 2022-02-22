import implicit
from implicit.evaluation import train_test_split, ndcg_at_k, AUC_at_k, mean_average_precision_at_k, precision_at_k
from scipy.sparse import csr_matrix, save_npz, load_npz
import pickle
import os
import pandas as pd


def loading_files():
    origin_path = os.getcwd()
    et_path = '/DH/Projeto/KASSANDR/Streamlit_finalversion/'

    path_model_de = 'de_als_model.pkl'
    model_de = pickle.load(open((origin_path + et_path + path_model), 'rb'))



    path_item_user = 'sparse_item_user.npz'
    sparse_item_user = load_npz(open((origin_path + et_path + path_item_user), 'rb'))

    path_user_item = 'sparse_user_item.npz'
    sparse_user_item = load_npz(open((origin_path + et_path + path_user_item), 'rb'))

    path_offer = '\.pkl\offers.pkl'
    offer_title = pickle.load(open(origin_path + et_path + path_offer, 'rb'))

    indice_path = 'indice_items.csv'
    indice_itens = pd.read_csv(origin_path + et_path + indice_path)

    return offer_title, model, sparse_item_user, sparse_user_item, indice_itens

def recommend(user, model, sparse_user_item):
    ''' Retorna uma lista de itens recomendados para o usuário dado de acordo com a biblioteca Implicit.
        Também é retornado uma lista com os itens já clicados por esse usuário'''

    #sparse_user_item = load_npz("sparse_user_item.npz")

    # with open(model_path, 'rb') as pickle_in:
    #     model = pickle.load(pickle_in)

    # if user not in sparse_user_item.T.tocsr().indices:
    #     return "invalid user"

    recommended, _ = model.recommend(user, sparse_user_item[user])

    original_user_items = list(sparse_user_item[user].indices)

    return recommended, original_user_items


def most_similar_items(item_id, model, n_similar=10):
    '''computes the most similar items'''

    # with open(model_path, 'rb') as pickle_in:
    #     model = pickle.load(pickle_in)

    similar, score = model.similar_items(item_id, n_similar, filter_items = [item_id])

    return similar


def most_similar_users(user_id, sparse_user_item, model, n_similar=10):
    '''computes the most similar users'''

    similar, scores = model.similar_users(user_id, n_similar, filter_users = [user_id])

    # original users items
    original_user_items = list(sparse_user_item[user_id].indices)

    common_items_users = {}

    # now we want to add the items that a similar user has rated
    for user in similar:
        # Verifica em cada usuário considerado similar quais são os itens que estes
        # tem em comum com o usuário selecionado
        common_items_users[user] = set(list(sparse_user_item[user].indices)) & set(original_user_items)

    # retorna usuários similares, e quais são os itens comuns correspondentes a cada um desses usuários
    return similar, common_items_users


def recalculate_user(user_ratings):
    '''adds new user and its liked items to sparse matrix and returns recalculated recommendations
       Receives the user clicked products vector (user_ratings)'''

    alpha = 40
    m = load_npz('sparse_user_item.npz')
    n_users, n_movies = m.shape

    ratings = [alpha for i in range(len(user_ratings))]

    m.data = np.hstack((m.data, ratings))
    m.indices = np.hstack((m.indices, user_ratings))
    m.indptr = np.hstack((m.indptr, len(m.data)))
    m._shape = (n_users + 1, n_movies)

    # recommend N items to new user
    with open(model_path, 'rb') as pickle_in:
        model = pickle.load(pickle_in)

    recommended, _ = zip(*model.recommend(n_users, m, recalculate_user=True))

    return recommended

def print_offers_name_on_streamlit(list_of_items, offer_title):

	msg = ""
	for item in list_of_items:
		msg = msg + offer_title[item] + '\n\n'

	return msg


def suggestions(user_id, sparse_user_item, K=500, n_best_seller=2):
    '''
    Retorna recomendações segmentadas de acordo com as categorias clicadas pelo usuário passado.
    À lista de recomendações são adicionados dois top 10 best-sellers da categoria em questão

      Inputs:

       user_id -> ID categórico do usuário

       K -> Quantidade de sugestões que serão retornadas somente pelo modelo

       n_best_seller -> Quantidade de sugestões que serão retornadas por popularidade em cada categoria considerada

       Output:

       cat_suggestions -> Dicionário com as sugestões agrupadas por categoria já clicada pelo usuário

       original -> Array com os clicks originais do usuário selecionado
    '''

    if len(sparse_user_item[user_id].indices) == False:
        return "Invalid User"

    cat_suggestions = {}  ### Dicionario de sugestões agrupadas por categoria. Retornoda função
    recs, original = recommend(user_id, K)  # Resposta original do modelo de recomendações e clicks originais
    pd_recs = (pd.DataFrame((recs, [offer_cat.get(key) for key in recs])).T).rename({0: 'Offer', 1: 'Category'},
                                                                                    axis=1)  # Dataframe p rastrear a categoria da oferta

    best_cat = pd.Series(
        offer_cat[cat] for cat in original).value_counts().index  # Filtra as categorias mais clicadadas pelo usuário

    for i in range(len(best_cat)):  # percorrer as categorias de acordo com os clicks do usuários

        if len(pd_recs[pd_recs.Category == best_cat[
            i]]) != 0:  ## Se não houver nenhuma recomendação da categoria em questão, não adicionar à lista

            pop_recs = products_info[products_info.Category == best_cat[i]][:20]  # seleciona os 10 itens mais populares
            pop_recs = pop_recs[
                pop_recs.Offer.isin(original) == False]  # Filtra para manter apenas os que ainda não foram clicados

            pop_recs = random.sample(pop_recs.Offer.values.tolist(), pop_recs.shape[0])[
                       :n_best_seller]  # Seleciona 2 ofertas mais populares da categoria

            pop_recs.extend(pd_recs[pd_recs.Category == best_cat[i]].Offer.values[
                            :3].tolist())  # Soma aos best sellers as sugestões do modelo de acordo com a categoria
            cat_suggestions[best_cat[i]] = pop_recs

    others = []  # Verificar sugestões de categorias que nunca foram clicadas pelo usuário
    for row in pd_recs.index[:15]:
        if pd_recs.Category.values[row] not in best_cat.values:
            # print(cat_name[pd_recs.Category.values[row]]) #Ver quais são as categorias que não se encaixaram
            others.append(pd_recs.Offer.values[row])
    random.shuffle(others)
    others = others[:5]

    cat_suggestions['Others'] = others

    return cat_suggestions, original