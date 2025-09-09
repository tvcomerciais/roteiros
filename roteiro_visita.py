import pandas as pd
import streamlit as st
import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================
# TÍTULO
# =========================
st.markdown(
    "<h1 style='font-size:20px; font-family:Arial;'>🎯 INFORMAÇÕES DE ROTAS DE VISITAS</h1>",
    unsafe_allow_html=True
)

# =========================
# GOOGLE SHEETS VIA SECRETS
# =========================
try:
    service_account_info = st.secrets["google_service_account"]

    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("roteiro_visitas").sheet1
except Exception as e:
    st.error(f"❌ Erro ao conectar com Google Sheets: {e}")

# =========================
# FORMULÁRIO
# =========================
with st.form("formulario_visita", clear_on_submit=True):
    data = st.date_input("📅 Informe a Data:", datetime.date.today())
    st.write("Data selecionada:", data.strftime("%d/%m/%Y"))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        codigo_ga = st.text_input("👁️‍🗨️ Código G.A:")
        observacoes = st.text_input("🤖 Observações:")

    with col2:
        codigo_rca = st.text_input("👩‍💻 Código do RCA:")
        roteiro = st.selectbox("🕧 Roteiro do Dia:", [' ', 'PARCIAL', 'COMPLETO'])

    with col3:
        quantidade_pedidos = st.text_input("🤳 Pedidos Realizados:")

    with col4:
        valor_pedidos = st.text_input("💲 Valor de Pedidos:")

    pontos_fortes = st.multiselect(
        "💪 Pontos Fortes:",
        ['Planejamento do Dia','Apresentação Pessoal','Leitura de Gôndula',
         'Iniciativa de Vendas','Fechamento da Visita','Catalago',
         'Campanha']
    )

    pontos_a_melhorar = st.multiselect(
        "💡 Pontos a Desenvolver:",
        ['Planejamento do Dia','Apresentação Pessoal','Leitura de Gôndula',
         'Iniciativa de Vendas','Fechamento da Visita','Catalago',
         'Campanha']
    )

    # BOTÃO DE ENVIO
    enviar = st.form_submit_button("💾 Gravar Informações")

    if enviar:
        campos = [
            codigo_ga, observacoes, codigo_rca, roteiro,
            quantidade_pedidos, valor_pedidos,
            ";".join(pontos_a_melhorar), ";".join(pontos_fortes)
        ]

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
            try:
                sheet.append_row(nova_linha)
                st.success("🤖 Informações gravadas com sucesso!")
            except Exception as e:
                st.error(f"❌ Falha ao gravar no Google Sheets: {e}")



