import pandas as pd
import streamlit as st
import plotly.express as plt

# Funções
def categorize_imc(row):
  if row > 40:
    return 'Obesidade classe III'
  elif row >= 35:
    return 'Obesidade classe II'
  elif row >= 30:
    return 'Obesidade classe I'
  elif row >= 25:
    return 'Pré Obeso'
  elif row >= 18.5:
    return 'Normal'
  elif row >= 16.5:
    return 'Peso abaixo do normal'
  else:
    return 'Peso severamente abaixo do normal'

# Leitura do arquivo
df = pd.read_csv('despesas_medicas.csv')

# Criação das colunas
df['cat_imc'] = df['imc'].apply(lambda x: categorize_imc(x))

df['obeso'] = df['imc'].apply(lambda x: 'sim' if x > 30 else 'não')
df['possui_filhos'] = df['qtd_filhos'].apply(lambda x: "não" if x == 0 else 'Sim')
df['qtd_filhos'] = df['qtd_filhos'].astype('str')

# st.write(df)

# "with" notation
with st.sidebar:
    sexo = st.selectbox('Sexo', df['sexo'].unique())
    obeso = st.selectbox('Obeso', df['obeso'].unique())
    idade = st.slider('Idade', min_value=int(df['idade'].min()), max_value=int(df['idade'].max()), value=int(df['idade'].mean()), step=1)
    
# Filtro de Linhas
conditions = (
    (df['sexo'] == sexo) &
    (df['obeso'] == obeso) & 
    (df['idade'] >= idade) 
)

# Criação de Gráficos
dfg = (
    df.loc[conditions, ['regiao', 'despesas_medicas']]
    .groupby(['regiao'])
    .mean()
    .reset_index()
    .rename(columns={'despesas_medicas': 'despesas'})
)

dfg['despesas'] = dfg['despesas'].apply(lambda x: round(x, 2))

st.dataframe(data=dfg)




# st.write(dfg)

fig = plt.bar(
    data_frame=dfg,
    x='regiao',
    y='despesas',
    # color='possui_filhos',
    text="despesas",
    barmode="group",
    title=f"Média de despesas médicas para pessoas do sexo {sexo}, com idade de {idade} ou mais, {obeso} obesos",
    labels={
        'regiao': 'Região',
        'despesas': 'Média Desp. Médicas',
        # 'possui_filhos': 'Possui Filhos'
    },
)
st.plotly_chart(fig)
# # fig.show()