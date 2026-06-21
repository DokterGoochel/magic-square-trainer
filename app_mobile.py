import streamlit as st
from datetime import date

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
        font-size: 24px !important;
        font-weight: bold !important;
        text-align: center !important;
        height: 45px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer")

# Sessie-beheer
if 'reset' not in st.session_state: st.session_state.reset = 0

# Keuze voor controle methode (Nu met 3 opties)
controle_methode = st.radio(
    "Target value:", 
    ["Automatic (sum of first row)", "Manual input", "Date input"]
)

# Initialiseer de variabelen voor het doelgetal
doelgetal_handmatig = 0
doelgetal_datum = 0

# OPTIE 1: Handmatige invoer
if controle_methode == "Manual input":
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

# OPTIE 2: Datum invoer (Nieuw!)
elif controle_methode == "Date input":
    with st.container(border=True):
        # Invoerveld voor datum: van 01-01-1900 tot vandaag
        gekozen_datum = st.date_input(
            "Select a date:",
            value=date(1980, 1, 1), # Standaard startwaarde in de kalender
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key=f"datum_{st.session_state.reset}"
        )
        
        # Berekening van de controlesom volgens jouw formule
        dag = gekozen_datum.day
        maand = gekozen_datum.month
        jaar_volledig = gekozen_datum.year
        
        eeuw = jaar_volledig // 100       # Eerste twee cijfers van het jaartal (bijv. 19)
        jaar_kort = jaar_volledig % 100    # Laatste twee cijfers van het jaartal (bijv. 84)
        
        doelgetal_datum = dag + maand + eeuw + jaar_kort
        
        # Subtiele visuele controle voor jezelf zodat je de som direct ziet
        st.caption(f"Calculation: {dag} + {maand} + {eeuw} + {jaar_kort} = **{doelgetal_datum}**")

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
        st.rerun()

with col2:
    if st.button("CHECK NOW", type="primary"):
        matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
        
        # Bepaal het doelgetal op basis van de 3 methodes
        if controle_methode == "Automatic (sum of first row)":
            doel = sum(matrix[0])
        elif controle_methode == "Manual input":
            doel = doelgetal_handmatig
        else:
            doel = doelgetal_datum
        
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
