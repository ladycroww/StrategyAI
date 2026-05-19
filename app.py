import streamlit as st
try:
    from google import genai
except ImportError:
    st.error("Por favor, adicione 'google-genai' ao seu arquivo requirements.txt")

# Configuração da página
st.set_page_config(
    page_title="StrategyAI — Estratégias Gratuitas",
    page_icon="⚡",
    layout="centered"
)

# Estilização visual (Mantendo o seu design escuro/neon original)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');
    .stApp { background: #080818; color: #e0e0ff; font-family: 'Syne', sans-serif; }
    div[data-testid="stForm"], .stAlert { background-color: #0f0f22 !important; border: 1px solid #1e1e38 !important; border-radius: 20px !important; }
    textarea, input { background-color: #14142a !important; color: #e0e0ff !important; border: 1.5px solid #252545 !important; border-radius: 12px !important; }
    .main-title { font-size: 52px; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .accent { background: linear-gradient(90deg, #a78bfa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .subtitle { color: #666666; font-size: 15px; text-align: center; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

PLATFORMS = {"Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️", "LinkedIn": "💼", "Facebook": "👥", "Pinterest": "📌"}
GOALS = {"Crescer seguidores": "📈", "Vender produto/serviço": "💰", "Gerar leads": "🎯", "Reconhecimento de marca": "✨", "Tráfego para site": "🌐", "Construir comunidade": "🤝"}
BUDGETS = ["Só orgânico 🌱", "R$300–1k/mês 💵", "R$1k–5k/mês 💳", "R$5k+/mês 💎"]

st.markdown('<div class="main-title">Strategy<span class="accent">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estratégias de redes sociais gratuitas usando inteligência artificial</div>', unsafe_allow_html=True)

# Inicializa o cliente do Gemini puxando a chave direto dos Secrets de forma segura
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Erro ao carregar a chave GEMINI_API_KEY dos Secrets do Streamlit.")

# Formulário Principal
with st.form("strategy_form"):
    st.markdown("### 01. Plataformas *")
    platforms = st.multiselect("Selecione uma ou mais opções:", list(PLATFORMS.keys()))
    
    st.markdown("### 02. Objetivos *")
    goals = st.multiselect("Selecione um ou mais objetivos:", list(GOALS.keys()))
    
    st.markdown("### 03. Seu Nicho / Produto / Serviço *")
    niche = st.text_area("", placeholder="Ex: Curso de sublimação para iniciantes...", height=100)
    
    st.markdown("### 04. Orçamento para Tráfego Pago")
    budget = st.selectbox("Escolha o nível de investimento:", BUDGETS)
    
    st.markdown("### 05. Contexto Adicional (opcional)")
    extra = st.text_area("", placeholder="Ex: Já tenho 1.200 seguidores...", height=70)
    
    can_generate = len(platforms) > 0 and len(goals) > 0 and len(niche.strip()) > 3
    submit_button = st.form_submit_button("✦ Gerar Estratégia com IA", disabled=not can_generate)

if submit_button:
    with st.spinner("🔮 O Gemini está analisando o mercado e gerando sua estratégia..."):
        try:
            platform_names = ", ".join(platforms)
            goal_names = ", ".join(goals)
            
            # Unimos as instruções do sistema e o prompt do usuário para o Gemini
            full_prompt = f"""Você é um especialista sênior em marketing digital, redes sociais e mídia paga com profundo conhecimento das atualizações de algoritmos mais recentes.
Sua missão: gerar estratégias PRÁTICAS, ATUALIZADAS e DETALHADAS baseadas nas últimas tendências e mudanças de algoritmo de cada plataforma.

SEMPRE estruture a resposta com os tópicos:
1. Análise do nicho e contexto
2. Estratégia Orgânica (formatos que o algoritmo prioriza AGORA, frequência ideal)
3. Estratégia de Tráfego Pago (campanhas, segmentação, criativos)
4. Calendário de Conteúdo (sugestão prática para 30 dias)
5. KPIs e métricas para acompanhar

Dados do cliente:
🎯 NICHO/PRODUTO: {niche}
📱 PLATAFORMAS: {platform_names}
🏆 OBJETIVOS: {goal_names}
💰 ORÇAMENTO PARA ADS: {budget}
{f'📝 CONTEXTO ADICIONAL: {extra}' if extra else ''}

Seja específico, prático e acionável. Use listas e formatação clara."""

            # Chamando o modelo gratuito e rápido do Google (Gemini 2.5 Flash)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
            )
            
            st.markdown("---")
            st.markdown("### ✦ Estratégia Gerada")
            st.info(f"**Configuração:** {platform_names} • {goal_names}")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Erro ao gerar com o Gemini: {e}")
