import streamlit as st

# Garante que a biblioteca do Gemini está instalada
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
    
    .stApp { 
        background: #080818; 
        color: #e0e0ff; 
        font-family: 'Syne', sans-serif; 
    }
    
    /* Customização dos blocos, cards e alertas */
    div[data-testid="stForm"], .stAlert, div[data-testid="stNotification"] { 
        background-color: #0f0f22 !important; 
        border: 1px solid #1e1e38 !important; 
        border-radius: 20px !important; 
    }
    
    /* Inputs, Selectbox e Textareas */
    textarea, input, div[data-baseweb="select"] { 
        background-color: #14142a !important; 
        color: #e0e0ff !important; 
    }
    
    /* Ajuste de bordas dos campos */
    textarea, input {
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

# Dicionários de dados para mapeamento
PLATFORMS = {"Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️", "LinkedIn": "💼", "Facebook": "👥", "Pinterest": "📌"}
GOALS = {"Crescer seguidores": "📈", "Vender produto/serviço": "💰", "Gerar leads": "🎯", "Reconhecimento de marca": "✨", "Tráfego para site": "🌐", "Construir comunidade": "🤝"}
BUDGETS = ["Só orgânico 🌱", "R$300–1k/mês 💵", "R$1k–5k/mês 💳", "R$5k+/mês 💎"]

# Cabeçalho do App
st.markdown('<div class="main-title">Strategy<span class="accent">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estratégias de redes sociais baseadas nas últimas atualizações de algoritmo</div>', unsafe_allow_html=True)

# Inicializa o cliente do Gemini puxando a chave direto dos Secrets de forma segura
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Erro ao carregar a chave GEMINI_API_KEY dos Secrets do Streamlit. Verifique as configurações do app.")

# Formulário Principal
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
    
    # O botão fica sempre habilitado no formulário para capturar o clique do usuário
    submit_button = st.form_submit_button("✦ Gerar Estratégia com IA")

# A validação e o processamento acontecem AGORA, após o clique do botão:
if submit_button:
    # Verifica se os campos obrigatórios foram preenchidos corretamente
    if not platforms or not goals or len(niche.strip()) <= 3:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios: selecione pelo menos 1 plataforma, 1 objetivo e descreva seu nicho (mínimo 4 caracteres).")
    else:
        with st.spinner("🔮 O Gemini está analisando o mercado e gerando sua estratégia..."):
            try:
                platform_names = ", ".join(platforms)
                goal_names = ", ".join(goals)
                
                # Prompt unificado para o modelo Gemini
                full_prompt = f"""Você é um especialista sênior em marketing digital, redes sociais e mídia paga com profundo conhecimento das atualizações de algoritmos mais recentes de 2025 e 2026.
Sua missão: gerar estratégias PRÁTICAS, ATUALIZADAS e DETALHADAS baseadas nas últimas tendências e mudanças de algoritmo de cada plataforma.

SEMPRE estruture a resposta com os tópicos abaixo:
1. Análise do nicho e contexto
2. Estratégia Orgânica (formatos que o algoritmo prioriza AGORA, frequência ideal de postagens)
3. Estratégia de Tráfego Pago (tipos de campanha recomendados, segmentação, criativos)
4. Calendário de Conteúdo (sugestão prática estruturada para 30 dias)
5. KPIs e métricas cruciais para acompanhar
6. Alertas importantes sobre mudanças recentes de algoritmo nas plataformas escolhidas

Dados do cliente:
🎯 NICHO/PRODUTO: {niche}
📱 PLATAFORMAS: {platform_names}
🏆 OBJETIVOS: {goal_names}
💰 ORÇAMENTO PARA ADS: {budget}
{f'📝 CONTEXTO ADICIONAL: {extra}' if extra else ''}

Seja específico, prático, direto e acionável. Use listas, tópicos e formatação clara com emojis estratégicos."""

                # Chamando o modelo oficial atualizado do Google
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                )
                
                # Exibição do resultado na tela
                st.markdown("---")
                st.markdown("### ✦ Estratégia Gerada")
                st.info(f"**Configuração atual:** {platform_names} • {goal_names}")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Erro ao gerar conteúdo com o Gemini: {e}")
