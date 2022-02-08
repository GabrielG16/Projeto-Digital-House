import implicit
from implicit.evaluation import train_test_split, ndcg_at_k, AUC_at_k, mean_average_precision_at_k, precision_at_k
from scipy.sparse import csr_matrix, save_npz, load_npz
import pickle
import os
import pandas as pd


def loading_files():
    origin_path = os.getcwd()
    et_path = '/DH/Projeto/KASSANDR/Streamlit_finalversion/'

    path_model = 'de_als_model.pkl'
    model = pickle.load(open((origin_path + et_path + path_model), 'rb'))

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

    recommended, _ = model.recommend(user, sparse_user_item[user])

    original_user_items = list(sparse_user_item[user].indices)

    return recommended, original_user_items


def most_similar_items(item_id, model, n_similar=10):
    '''computes the most similar items'''

    # with open(model_path, 'rb') as pickle_in:
    #     model = pickle.load(pickle_in)

    similar, score = model.similar_items(item_id, n_similar)

    return similar


def most_similar_users(user_id, sparse_user_item, model, n_similar=10):
    '''computes the most similar users'''

    similar, _ = model.similar_users(user_id, n_similar)

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