import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(
    page_title="DengueRadar — Informação para Prevenção",
    page_icon="🦟",
    layout="wide"
)

# Estilização da Identidade Visual (Cores oficiais do projeto)
PRIMARY_COLOR = "#592A82"  # Roxo
SECONDARY_COLOR = "#17918F"  # Verde-azulado
ALERT_COLOR = "#DA4B52"      # Vermelho

# Dados Mockados Simulados (Bases públicas estruturadas)
@st.cache_data
def carregar_dados():
    dados = [
        {"Região": "Zona Norte", "Mes": "Jan", "Casos": 120, "Indice_Risco": "Médio"},
        {"Região": "Zona Norte", "Mes": "Fev", "Casos": 250, "Indice_Risco": "Alto"},
        {"Região": "Zona Norte", "Mes": "Mar", "Casos": 310, "Indice_Risco": "Alto"},
        {"Região": "Zona Norte", "Mes": "Abr", "Casos": 190, "Indice_Risco": "Médio"},
        {"Região": "Zona Sul", "Mes": "Jan", "Casos": 80, "Indice_Risco": "Baixo"},
        {"Região": "Zona Sul", "Mes": "Fev", "Casos": 140, "Indice_Risco": "Médio"},
        {"Região": "Zona Sul", "Mes": "Mar", "Casos": 200, "Indice_Risco": "Alto"},
        {"Região": "Zona Sul", "Mes": "Abr", "Casos": 110, "Indice_Risco": "Médio"},
        {"Região": "Zona Leste", "Mes": "Jan", "Casos": 150, "Indice_Risco": "Médio"},
        {"Região": "Zona Leste", "Mes": "Fev", "Casos": 290, "Indice_Risco": "Alto"},
        {"Região": "Zona Leste", "Mes": "Mar", "Casos": 380, "Indice_Risco": "Alto"},
        {"Região": "Zona Leste", "Mes": "Abr", "Casos": 220, "Indice_Risco": "Alto"},
        {"Região": "Zona Oeste", "Mes": "Jan", "Casos": 60, "Indice_Risco": "Baixo"},
        {"Região": "Zona Oeste", "Mes": "Fev", "Casos": 95, "Indice_Risco": "Baixo"},
        {"Região": "Zona Oeste", "Mes": "Mar", "Casos": 130, "Indice_Risco": "Médio"},
        {"Região": "Zona Oeste", "Mes": "Abr", "Casos": 85, "Indice_Risco": "Baixo"},
    ]
    return pd.DataFrame(dados)

df = carregar_dados()

# Barra Lateral (Filtros)
st.sidebar.markdown(f"<h2 style='color: {PRIMARY_COLOR};'>🧭 DengueRadar</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Painel interativo para monitoramento e prevenção comunitária.")

st.sidebar.divider()
regioes_disponiveis = df["Região"].unique()
regiao_selecionada = st.sidebar.selectbox("Selecione a Localidade (Região):", regioes_disponiveis)

meses_disponiveis = ["Jan", "Fev", "Mar", "Abr"]
meses_selecionados = st.sidebar.multiselect("Selecione o Período (Meses):", meses_disponiveis, default=meses_disponiveis)

# Filtragem de dados
df_filtrado = df[(df["Região"] == regiao_selecionada) & (df["Mes"].isin(meses_selecionados))]

# Corpo Principal
st.markdown(f"<h1 style='color: {PRIMARY_COLOR};'>🦟 DengueRadar — Painel de Monitoramento</h1>", unsafe_allow_html=True)
st.markdown("> **Checkpoint 2 — Protótipo Funcional** | ODS 3: Saúde e Bem-Estar[cite: 8]")

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
else:
    # Indicadores Metrização (Métricas)
    total_casos = df_filtrado["Casos"].sum()
    media_casos = int(df_filtrado["Casos"].mean())
    risco_atual = df_filtrado.iloc[-1]["Indice_Risco"] if not df_filtrado.empty else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total de Casos Registrados", f"{total_casos}")
    col2.metric("📈 Média Mensal de Casos", f"{media_casos}")
    col3.metric("⚠️ Nível de Alerta Atual", f"{risco_atual}")

    st.divider()

    # Gráfico de Evolução Temporal
    st.subheader(f"Evolução Temporal de Casos — {regiao_selecionada}")
    fig = px.bar(
        df_filtrado, 
        x="Mes", 
        y="Casos", 
        text="Casos",
        color="Casos",
        color_continuous_scale=["#17918F", "#592A82", "#DA4B52"],
        labels={"Casos": "Número de Registros", "Mes": "Mês"}
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    # Seção de Orientações de Prevenção
    st.divider()
    st.subheader("🛡️ Orientações Oficiais de Prevenção")
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        * **Elimine água parada:** Tampe caixas d'água, mantenha calhas limpas e verifique vasos de plantas.
        * **Descarte correto de resíduos:** Lixeiras tampadas e garrafas viradas para baixo.
        * **Uso de repelentes:** Aplicar conforme recomendação nas áreas expostas da pele.
        """)
    with p2:
        st.markdown("""
        * **Sintomas de Alerta:** Febre alta, dores musculares intensas, manchas vermelhas na pele.
        * **Procure atendimento:** Em caso de sintomas, dirija-se ao posto de saúde mais próximo.
        * **Importante:** Este painel tem caráter exclusivamente educativo e informativo.
        """)

# Rodapé com Transparência de Dados
st.divider()
st.caption("DengueRadar © 2026 | Dados simulados para fins acadêmicos integrados com diretrizes de fontes públicas abertas.")