import streamlit as st
import os
try:
    from anthropic import Anthropic
except ImportError:
    st.error("Por favor, adicione 'anthropic' ao seu arquivo requirements.txt")

# Configuração da página
st.set_page_config(
    page_title="StrategyAI — Estratégias com IA",
    page_icon="⚡",
    layout="centered"
)

# Injeção de CSS para manter o design futurista/escuro do seu app original
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');
    
    .stApp {
        background: #080818;
        color: #e0e0ff;
        font-family: 'Syne', sans-serif;
    }
    
    /* Customização dos blocos e cards */
    div[data-testid="stForm"], .stAlert {
        background-color: #0f0f22 !important;
        border: 1px solid #1e1e38 !important;
        border-radius: 20px !important;
    }

    /* Inputs e Textareas */
    textarea, input {
        background-color: #14142a !important;
        color: #e0e0ff !important;
        border: 1.5px solid #252545 !important;
        border-radius: 12px !important;
    }
    
    /* Título estilizado */
    .main-title {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    .accent {
        background: linear-gradient(90deg, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #666666;
        font-size: 15px;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Estrutura de dados original do seu código
PLATFORMS = {
    "Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️", 
    "LinkedIn": "💼", "Facebook": "👥", "Pinterest": "📌"
}
GOALS = {
    "Crescer seguidores": "📈", "Vender produto/serviço": "💰", "Gerar leads": "🎯",
    "Reconhecimento de marca": "✨", "Tráfego para site": "🌐", "Construir comunidade": "🤝"
}
BUDGETS = ["Só orgânico 🌱", "R$300–1k/mês 💵", "R$1k–5k/mês 💳", "R$5k+/mês 💎"]

# Título do App
st.markdown('<div class="main-title">Strategy<span class="accent">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estratégias de redes sociais baseadas nas últimas atualizações de algoritmo</div>', unsafe_allow_html=True)

# Input da Chave da API (Pode ser colocada nos Secrets do Streamlit depois)
api_key = st.sidebar.text_input("Anthropic API Key", type="password", help="Insira sua chave para rodar o app.")

# Formulário Principal (Card)
with st.form("strategy_form"):
    st.markdown("### 01. Plataformas *")
    platforms = st.multiselect("Selecione uma ou mais opções:", list(PLATFORMS.keys()))
    
    st.markdown("### 02. Objetivos *")
    goals = st.multiselect("Selecione um ou mais objetivos:", list(GOALS.keys()))
    
    st.markdown("### 03. Seu Nicho / Produto / Serviço *")
    niche = st.text_area("", placeholder="Ex: Curso de sublimação para iniciantes, focado em mulheres empreendedoras que querem renda extra em casa...", height=100)
    
    st.markdown("### 04. Orçamento para Tráfego Pago")
    budget = st.selectbox("Escolha o nível de investimento:", BUDGETS)
    
    st.markdown("### 05. Contexto Adicional (opcional)")
    extra = st.text_area("", placeholder="Ex: Já tenho 1.200 seguidores, posto 3x por semana, já tentei Reels mas não engajou...", height=70)
    
    # Validação do botão de envio
    can_generate = len(platforms) > 0 and len(goals) > 0 and len(niche.strip()) > 3
    submit_button = st.form_submit_button("✦ Gerar Estratégia com IA", disabled=not can_generate)

# Lógica de Geração (Executada após o clique)
if submit_button:
    if not api_key:
        st.warning("⚠️ Por favor, insira sua Anthropic API Key na barra lateral para prosseguir.")
    else:
        with st.spinner("🔮 Consultando fontes e gerando estratégia em tempo real..."):
            try:
                # Inicializa o cliente Anthropic
                client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                
                # Montagem dos Prompts estruturados do seu código original
                platform_names = ", ".join(platforms)
                goal_names = ", ".join(goals)
                
                system_prompt = """Você é um especialista sênior em marketing digital, redes sociais e mídia paga com profundo conhecimento das atualizações de algoritmos de 2024 e 2025. 
Sua missão: gerar estratégias PRÁTICAS, ATUALIZADAS e DETALHADAS baseadas nas últimas tendências e mudanças de algoritmo de cada plataforma.

SEMPRE estruture a resposta assim:
1. Análise do nicho e contexto
2. Estratégia Orgânica (com táticas específicas por plataforma, formatos que o algoritmo prioriza AGORA, frequência de postagens ideal)
3. Estratégia de Tráfego Pago (tipos de campanha, segmentação, orçamento, criativos)
4. Calendário de Conteúdo (sugestão prática para 30 dias)
5. KPIs e métricas para acompanhar
6. Alertas importantes sobre mudanças recentes de algoritmo"""

                user_prompt = f"""Crie uma estratégia completa e detalhada para:
🎯 NICHO/PRODUTO: {niche}
📱 PLATAFORMAS: {platform_names}
🏆 OBJETIVOS: {goal_names}
💰 ORÇAMENTO PARA ADS: {budget}
{f'📝 CONTEXTO ADICIONAL: {extra}' if extra else ''}

Considere as mudanças mais recentes de algoritmo de 2025 em cada plataforma. Seja específico, prático e acionável."""

                # Chamada oficial da API Anthropic com a ferramenta de busca ativada
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2000,
                    system=system_prompt,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": user_prompt}]
                )
                
                # Extraindo o texto retornado
                result_text = "".join([block.text for block in message.content if block.type == "text"])
                
                # Exibição do Resultado formatado
                st.markdown("---")
                st.markdown("### ✦ Estratégia Gerada")
                st.info(f"**Configuração:** {platform_names} • {goal_names}")
                st.markdown(result_text)
                
            except Exception as e:
                st.error(f"Erro ao gerar estratégia: {e}")