import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo bixado com sucesso!',icon="✅")
    time.sleep(5)
    sucesso.empty()

st.title('Dados Brutos')
url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados ['Data da Compra']=  pd.to_datetime(dados['Data da Compra'], format= '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as Colunoa', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do preduto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(),dados['Produto'].unique()) 

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0,5000)) 

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

with st.sidebar.expander('Frete do produto'):
    frete_produto = st.slider('Frete', 0, 250, (0,250))

with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())

with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(), dados['Local da compra'].unique())

with st.sidebar.expander('Avaliaçao da compra'):
    avaliacao_compra = st.slider('Selecione a avaliação da compra', 1, 5,(1,5))

with st.sidebar.expander('Tipo de pagamento'):
    pagamento = st.multiselect('Especifique o tipo de pagamento',dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

with st.sidebar.expander('Quantidade de parcelas'):
    parcelas = st.slider('Informe a quantidade de parcela',1,24, (1,24))

query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao_compra[0]<= `Avaliação da compra` <= @avaliacao_compra[1] and \
`Tipo de pagamento` in @pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]


'''


dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]
                                 
st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva o nome para o arquivo')

coluna1, coluna2 = st.columns(2)

with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o download da tabela em csv', data = converte_csv(dados_filtrados), file_name = nome_arquivo, mime = 'text/csv', on_click = mensagem_sucesso)