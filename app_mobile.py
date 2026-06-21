import streamlit as st
import random
from datetime import date, timedelta

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

# CSS voor styling én de mobiele grid-fix
st.markdown("""
    <style>
    /* 1. Maak de Check Now knop mooi geel */
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border: 2px solid #FFDE00 !important;
    }
    
    /* 2. Vergroot de tekst/cijfers in de invoervelden van het magische vierkant */
    div[data-testid="stNumberInput"] input {
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 45px !important;
    }
    
    /* 3. Maak de weergegeven random datum en het random getal mooi groot en gecentreerd */
    .large-display {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        color: #31333F;
        margin-bottom: 5px;
    }

    /* 4. FIX VOOR MOBIEL: Voorkom dat de 4 kolommen onder elkaar gaan staan */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important; /* Voorkom dat vakjes te veel tegen elkaar plakken op smalle schermen */
    }
    
    /* Zorg dat alle 4 de kolommen evenveel ruimte (25%) krijgen */
    [data-testid="column"] {
        min-width: 20% !important; 
    }
    
    /* Extra: optimaliseer de schermmarges op mobiel zodat het vierkant goed past */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer")

# Helper functies om willekeurige data en getallen te genereren
def genereer_random_datum():
    start_date = date(1900, 1, 1)
    end_date = date.today()
    verschil_dagen = (end_date - start_date).days
    random_dagen = random.randrange(verschil_dagen)
    return start_date + timedelta(days=random_dagen)

def genereer_random_getal():
    return random.randint(22, 99)

# Sessie-beheer
if 'reset' not in st.session_state: 
    st.session_state.reset = 0
if 'random_date' not in st.session_state:
    st.session_state.random_date = genereer_random_datum()
if 'random_target' not in st.session_state:
    st.session_state.random_target = genereer_random_getal()

# Keuze voor controle methode (Met aangepaste tekst)
controle_methode = st.radio(
    "Target value:", 
    ["Automatic (sum of first row)", "Manual input", "Random Date (01/01/1900 - Today)", "Random Number (22-99)"]
)

doelgetal_handmatig = 0
doelgetal_datum = 0

if controle_methode == "Manual input":
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

elif controle_methode
