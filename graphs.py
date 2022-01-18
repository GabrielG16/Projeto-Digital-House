import pandas as pd
import matplotlib.pyplot as plt


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
