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

# Cabeçal
