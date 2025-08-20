import pandas as pd
import streamlit as st

st.title("INFORMAÇÕES DE ROTAS DE VISITAS")

st.text_input("Código G.A:",label_visibility='visible')
st.text_input("Código do RCA:", label_visibility="visible")
st.selectbox("Roteiro do Dia:",['PARCIAL','COMPLETO'])
st.selectbox("Qual Foi o Desenpenho do RCA:",['RUIM','REGULAR','BOM'],label_visibility='visible')
st.text_input("Qual a Quantidade de Pedidos Realizados:",label_visibility='visible')
st.text_input("Qual o Valor de Pedidos Realizados:")
st.text_input("Pontos Fortes do RCA:")
st.text_input("Pontos Descoberto a Realizar:")
st.text_input("Observações:")
st.button("Gravar Informações")
