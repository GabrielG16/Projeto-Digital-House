import pandas as pd
import streamlit as st
import os

origin_path = os.getcwd()
et_path = ''

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading_data():
    path_de = origin_path + et_path + '/.csv/.novo/antecedents_to_consequents_alemanha.csv'
    alemanha = pd.read_csv(path_de)

    path_fr = origin_path + et_path + '/.csv/.novo/antecedents_to_consequents_france.csv'
    france = pd.read_csv(path_de)

    path_it = origin_path + et_path + '/.csv/.novo/antecedents_to_consequents_italia.csv'
    italia = pd.read_csv(path_de)

    return alemanha, france, italia


def item_exploration_page():
    st.title('Comparação de Itens')
    alemanha, france, italia = loading_data()

    pais_selecionado = st.selectbox('Selecione um pais:', ['França','Alemanha','Itália'])

    #aqui a ideia é a pessoa escolher o pais e ser apresentado as categorias disponiveis naquele país!

    if pais_selecionado == 'França':
        #st.write('frança')
        df = france

    elif pais_selecionado == 'Alemanha':
        df = alemanha

    elif pais_selecionado == 'Itália':
        df = italia

    select_item = st.selectbox('Selecione um item para ver seu comparativo: ', pd.Series(df.antecedents_offertitle.unique()).sort_values())

    if st.button('Gerar'):
        df.columns = ['Antecedentes', 'Consequentes']
        st.table(df[df.Antecedentes == str(select_item)].Consequentes)


    st.write('Aqui foi utilizado o algoritmo apriori, que tenta traçar comparações entre os itens para ver quais são os itens que normalmente são clicados em sequencia um do outro ')