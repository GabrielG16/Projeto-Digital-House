import implicit
import implicit.evaluation
import numpy as np
import pandas as pd


def model_evaluation(train, test, model, k=10):

    """Avaliação do modelo treinado com as funções da biblioteca Implicit.
    Retorna dicionário com p@k, map@k, ndcg@k e auc@k."""

    p_at_k = implicit.evaluation.precision_at_k(model,
                                                train_user_items=train,
                                                test_user_items=test,
                                                int_K=k,
                                                show_progress=False)

    m_at_k = implicit.evaluation.mean_average_precision_at_k(model,
                                                             train_user_items=train,
                                                             test_user_items=test,
                                                             int_K=k,
                                                             show_progress=False)

    ndcg_at_k = implicit.evaluation.ndcg_at_k(model,
                                              train_user_items=train,
                                              test_user_items=test,
                                              int_K=k,
                                              show_progress=False)

    auc_at_k = implicit.evaluation.AUC_at_k(model,
                                            train_user_items=train,
                                            test_user_items=test,
                                            int_K=k,
                                            show_progress=False)
    metrics = {'p@K': p_at_k,
               'map@K': m_at_k,
               'ndcg@K': ndcg_at_k,
               'auc@K': auc_at_k}

    return metrics


def get_k_most_popular(sparse_item_user, k):
    """Retorna um array com os códigos dos itens clicados por mais clientes da base de dados"""

    new_sparse = sparse_item_user.copy()
    interaction = np.ones_like(new_sparse.data)
    new_sparse.data = interaction
    pop_items = np.array((new_sparse).sum(axis=1)).reshape(-1)
    most_popular = pd.Series(pop_items).sort_values(ascending=False)[:k]

    return most_popular.index


def get_top_k(userid, sparse_user_item, k=10):

    """Retorna os top-K produtos clicados por um usuário de acordo
    com o nível de confiança obtido através das suas interações"""

    top_K = pd.Series(sparse_user_item[userid].data, index=sparse_user_item[userid].indices).sort_values(
        ascending=False)[:k]
    return top_K.index


def baseline_precision_at_k(sparse_item_user, k=10, test_pct=0.2):

    """Avalia a precisão caso o modelo recomendasse apenas os itens mais populares a todos os clientes.
    A métrica é calculada com base em uma seleção aleatória de 20% dos clientes."""

    # Seleção aleatória de 20% dos usuários para testagem por popularidade
    test_sample = np.random.choice(sparse_item_user.indices,
                                   size=int(test_pct * len(sparse_item_user.indices)),
                                   replace=False)

    most_popular = (get_k_most_popular(sparse_item_user, k))  # lista de 10 itens mais populares

    total_precision = 0
    sparse_user_item = sparse_item_user.T.tocsr()

    for user in test_sample:
        relevance = 0
        top_K = get_top_k(user, sparse_user_item, k)

        for item in most_popular:
            if item in top_K:  # Alteração do pesoa das interações para 0 e 1. Assim, será contabilizado apenas se o usuário interagiu com o item ou não.
                interact = 1
            else:
                interact = 0
            relevance += interact

        relevance /= k
        total_precision += relevance

    total_precision /= len(test_sample)

    return total_precision