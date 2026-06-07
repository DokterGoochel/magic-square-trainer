import streamlit as st

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

# We halen de ingewikkelde CSS voor de invoervelden weg en behouden alleen de gele knop
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border: 2px solid #FFDE00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer")

# Sessie-beheer
if 'reset' not in st.session_state: st.session_state.reset = 0

# Keuze voor controle methode
controle_methode = st.radio("Controle:", ["Automatisch (1e rij)", "Handmatig getal"])

# Dynamische invoer voor handmatig doelgetal
doelgetal_handmatig = 0
if controle_methode == "Handmatig getal":
    # TRUC: We dwingen via een gerichte inline stijl specifiek DIT blok naar een gele achtergrond
    st.markdown("""
        <style>
        /* We zoeken het invoerveld dat direct volgt op de radioknop */
        div[data-testid="stWidgetFormSubmitButton"] {  } /* negeer knoppen */
        .stRadio + div div[data-testid="stNumberInput"] input {
            background-color: #FFF9C4 !important;
            border: 2px solid #FBC02D !important;
            font-weight: bold !important;
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    doelgetal_handmatig = st.number_input(
        "Voer je doelgetal in:", min_value=0, step=1, format="%d", 
        key=f"doel_{st.session_state.reset}"
    )

# Raster tekenen (deze behouden nu hun eigen, standaard grijze look)
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
        
        if controle_methode == "Automatisch (1e rij)":
            doel = sum(matrix[0])
        else:
            doel = doelgetal_handmatig
        
        st.info(f"🎯 Doel: **{int(doel)}**")
        
        foutmeldingen = []
        for i in range(4):
            if sum(matrix[i]) != doel: foutmeldingen.append(f"❌ Rij {i+1} klopt niet.")
            if sum(matrix[r][i] for r in range(4)) != doel: foutmeldingen.append(f"❌ Kolom {i+1} klopt niet.")
        if sum(matrix[i][i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonaal 1 klopt niet.")
        if sum(matrix[i][3-i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonaal 2 klopt niet.")
        
        if not foutmeldingen:
            st.success(f"🎉 Perfect! De som is {int(doel)}.")
            st.balloons()
        else:
            for fout in foutmeldingen:
                st.error(fout)
