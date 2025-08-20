import pandas as pd
import streamlit as st
import datetime
import gspread
from google.oauth2.service_account import Credentials

# Título
st.markdown("<h1 style='font-size:20px; font-family:Arial;'>🎯 INFORMAÇÕES DE ROTAS DE VISITAS</h1>", unsafe_allow_html=True)

# Campo de data
data = st.date_input("📅 Informe a Data:", datetime.date.today())
st.write("Data selecionada:", data.strftime("%d/%m/%Y"))

# Colunas
col1, col2, col3, col4 = st.columns(4)

# Campos de texto e seleção
with col1:
    codigo_ga = st.text_input("👁️‍🗨️ Código G.A:")
    observacoes = st.text_input("🤖 Observações:")

with col2:
    codigo_rca = st.text_input("👩‍💻 Código do RCA:")
    roteiro = st.selectbox("🕧 Roteiro do Dia:", [' ','PARCIAL','COMPLETO'])

with col3:
    quantidade_pedidos = st.text_input("🤳 Pedidos Realizados:")

with col4:
    valor_pedidos = st.text_input("💲 Valor de Pedidos:")

pontos_fortes = st.multiselect(
    "💪 Pontos Fortes:",
    ['Planejamento do Dia','Apresentação Pessoal','Leitura de Gôndula',
     'Iniciativa de Vendas','Cinco Passos da Visita','Catalago',
     'Rotina Comercial','Campanha']
)

pontos_a_melhorar = st.multiselect(
    "💡 Pontos a Desenvolver:",
    ['Planejamento do Dia','Apresentação Pessoal','Leitura de Gôndula',
     'Iniciativa de Vendas','Cinco Passos da Visita','Catalago',
     'Rotina Comercial','Campanha']
)

# Lista de campos para validação
campos = [
    codigo_ga, observacoes, codigo_rca, roteiro, quantidade_pedidos,
    valor_pedidos, ";".join(pontos_a_melhorar), ";".join(pontos_fortes)
]

# Configurar Google Sheets
creds_json = "cescomroteiro-a975e8ef9939.json"  # caminho relativo para seu JSON
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    creds = Credentials.from_service_account_file(creds_json, scopes=scope)
    client = gspread.authorize(creds)

    # Testar autenticação e listar planilhas disponíveis
    planilhas = client.openall()
    st.success("✅ Autenticação bem-sucedida.")
    st.write("🔎 Planilhas disponíveis:")
    for p in planilhas:
        st.write(f"📄 {p.title}")

    # Abrir a planilha específica
    sheet = client.open("roteiro_visitas").sheet1

    # Botão para gravar
    if st.button("💾 Gravar Informações"):
        if any(campo.strip() == "" for campo in campos):
            st.warning("⚠️ Todos os Campos do Formulário São Obrigatórios.") 
        else:
            nova_linha = [
                data.strftime("%d/%m/%Y"),
                codigo_ga,
                observacoes,
                codigo_rca,
                roteiro,
                quantidade_pedidos,
                valor_pedidos,
                ";".join(pontos_fortes),
                ";".join(pontos_a_melhorar)
            ]
            sheet.append_row(nova_linha)
            st.success("🤖 Informações gravadas com sucesso!")

except Exception as e:
    st.error(f"❌ Erro ao conectar com o Google Sheets: {e}")
