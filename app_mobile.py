import streamlit as st
import random
from datetime import date, timedelta

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

# CSS voor de gele knop én grotere cijfers
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
# Bewaar de gegenereerde datum en het getal in het geheugen zodat deze niet verspringen tijdens het typen
if 'random_date' not in st.session_state:
    st.session_state.random_date = genereer_random_datum()
if 'random_target' not in st.session_state:
    st.session_state.random_target = genereer_random_getal()

# Keuze voor controle methode (nu 4 opties)
controle_methode = st.radio(
    "Target value:", 
    ["Automatic (sum of first row)", "Manual input", "Random Date", "Random Number (22-99)"]
)

doelgetal_handmatig = 0
doelgetal_datum = 0

if controle_methode == "Manual input":
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

elif controle_methode == "Random Date":
    with st.container(border=True):
        # Format de datum naar DD/MM/YYYY en toon deze groot op het scherm
        datum_string = st.session_state.random_date.strftime("%d/%m/%Y")
        st.markdown(f"<div class='large-display'>{datum_string}</div>", unsafe_allow_html=True)
        
        # Berekening van de controlesom (Nu onzichtbaar voor de gebruiker)
        dag = st.session_state.random_date.day
        maand = st.session_state.random_date.month
        jaar_volledig = st.session_state.random_date.year
        
        eeuw = jaar_volledig // 100       # Eerste twee cijfers jaartal
        jaar_kort = jaar_volledig % 100    # Laatste twee cijfers jaartal
        
        doelgetal_datum = dag + maand + eeuw + jaar_kort

elif controle_methode == "Random Number (22-99)":
    with st.container(border=True):
        # Toon het willekeurige getal groot op het scherm
        st.markdown(f"<div class='large-display'>{st.session_state.random_target}</div>", unsafe_allow_html=True)

# Raster tekenen
inputs = []
for r in range(4):
    cols = st.columns(4)
    for c in range(4):
        val = cols[c].number_input(
            f"R{r}K{c}", value=0, 
            key=f"c{r}{c}_{st.session_state.reset}", 
            label_visibility="collapsed", format="%d"
        )
        inputs.append(int(val))

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Delete All"):
        st.session_state.reset += 1
        # Genereer direct nieuwe random waarden als je het bord wist
        st.session_state.random_date = genereer_random_datum() 
        st.session_state.random_target = genereer_random_getal()
        st.rerun()

with col2:
    if st.button("CHECK NOW", type="primary"):
        matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
        
        if controle_methode == "Automatic (sum of first row)":
            doel = sum(matrix[0])
        elif controle_methode == "Manual input":
            doel = doelgetal_handmatig
        elif controle_methode == "Random Date":
            doel = doelgetal_datum
        else: # Random Number (22-99)
            doel = st.session_state.random_target
        
        st.info(f"🎯 Target: **{int(doel)}**")
        
        foutmeldingen = []
        for i in range(4):
            if sum(matrix[i]) != doel: foutmeldingen.append(f"❌ Row {i+1} is incorrect.")
            if sum(matrix[r][i] for r in range(4)) != doel: foutmeldingen.append(f"❌ Column {i+1} is incorrect.")
        if sum(matrix[i][i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonal (top left-bottom right) is incorrect.")
        if sum(matrix[i][3-i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonal (bottom left-top right) is incorrect.")
        
        if not foutmeldingen:
            st.success(f"🎉 Perfect. This square is magical in every way. It all adds up to {int(doel)}.")
            st.balloons()
        else:
            for fout in foutmeldingen:
                st.error(fout)
