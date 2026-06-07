import streamlit as st

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

# Sessie-beheer
if 'reset' not in st.session_state: st.session_state.reset = 0

# Keuze voor controle methode
controle_methode = st.radio("Target value:", ["Automatic (sum of first row)", "Manual input"])

# Dynamische invoer voor handmatig doelgetal
doelgetal_handmatig = 0
if controle_methode == "Manual input":
    # Een strak kader zonder extra titels, alleen de invoerbalk
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

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
        
        # Bepaal het doelgetal op basis van de gekozen methode
        if controle_methode == "Automatic (sum of first row)":
            doel = sum(matrix[0])
        else:
            doel = doelgetal_handmatig
        
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
            # GEWIZIGD: Nette for-loop in plaats van list comprehension voorkomt de dropdown weergave
            for fout in foutmeldingen:
                st.error(fout)
