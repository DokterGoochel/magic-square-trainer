import streamlit as st
import random
from datetime import date, timedelta

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

# CSS voor de gele knop én grotere cijfers in het vierkant
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
        font-size: 24px !important;    /* Pas dit getal aan voor groter/kleiner (standaard is ~16px) */
        font-weight: bold !important;  /* Maakt de cijfers dikgedrukt voor betere zichtbaarheid */
        text-align: center !important; /* Zet het getal netjes in het midden van het vakje */
        height: 45px !important;       /* Maakt het vakje zelf iets hoger zodat het grote cijfer goed past */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer")

# Helper functies
def genereer_random_datum():
    start_date = date(1900, 1, 1)
    end_date = date.today()
    verschil_dagen = (end_date - start_date).days
    random_dagen = random.randrange(verschil_dagen)
    return start_date + timedelta(days=random_dagen)

# Sessie-beheer
if 'reset' not in st.session_state: st.session_state.reset = 0
if 'random_date' not in st.session_state: st.session_state.random_date = genereer_random_datum()
if 'random_target' not in st.session_state: st.session_state.random_target = random.randint(22, 99)

# Keuze voor controle methode
controle_methode = st.radio("Target value:", ["Automatic (sum of first row)", "Manual input", "Random Date (01/01/1900 - Today)", "Random Number (22-99)"])

# Variabelen voor de doelgetallen
doelgetal_handmatig = 0
doelgetal_datum = 0
doelgetal_random = st.session_state.random_target

# Dynamische weergave per methode
if controle_methode == "Manual input":
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

elif controle_methode == "Random Date (01/01/1900 - Today)":
    with st.container(border=True):
        datum_string = st.session_state.random_date.strftime("%d/%m/%Y")
        st.write(f"### {datum_string}")
        # Berekening
        d = st.session_state.random_date.day
        m = st.session_state.random_date.month
        y = st.session_state.random_date.year
        doelgetal_datum = d + m + (y // 100) + (y % 100)

elif controle_methode == "Random Number (22-99)":
    with st.container(border=True):
        st.write(f"### {doelgetal_random}")

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
        st.session_state.random_date = genereer_random_datum()
        st.session_state.random_target = random.randint(22, 99)
        st.rerun()

with col2:
    if st.button("CHECK NOW", type="primary"):
        matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
        
        # Bepaal het doelgetal
        if controle_methode == "Automatic (sum of first row)":
            doel = sum(matrix[0])
        elif controle_methode == "Manual input":
            doel = doelgetal_handmatig
        elif controle_methode == "Random Date (01/01/1900 - Today)":
            doel = doelgetal_datum
        else:
            doel = doelgetal_random
        
        st.info(f"🎯 Doel: **{int(doel)}**")
        
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
