import sys
import pandas as pd

def corte_pivo_log(user_id,pivo_log):
    mask_c = (pivo_log['User'] == user_id) & (pivo_log['Clicked?'] == 1)

    #rankeando
    categorias_usuario = pivo_log.loc[mask_c, 'Category'].unique()
    mask = pivo_log['Category'].isin(categorias_usuario)

    pivo_log = pivo_log.loc[mask]


    clicks_categorias = pd.DataFrame(pivo_log.Category.value_counts()).reset_index()
    clicks_categorias.columns = ['Category','Clicks']
    clicks_categorias.sort_values(by='Clicks', ascending = False, inplace = True)
    clicks_categorias.drop_duplicates(subset = 'Category', inplace = True)

    #aqui passar o numero de categorias que vc quer q ele corte
    n_categories = 5 #top 5 categorias do usuario
    top_n = clicks_categorias.Category[:n_categories]

    mask_top_n = pivo_log['Category'].isin(top_n)
    pivo_log = pivo_log.loc[mask_top_n, ['User','Products','Clicked?']]


    return pivo_log
