import streamlit as st

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

st.title("🪄 Magic Square Trainer")

# Reset logica voor de input-versie
if 'inputs' not in st.session_state:
    st.session_state.inputs = [None] * 16

controle_methode = st.radio("Controle:", ["Automatisch (1e rij)", "Handmatig getal"])
doelgetal_handmatig = 0
if controle_methode == "Handmatig getal":
    doelgetal_handmatig = st.number_input("Doelgetal:", min_value=0, step=1)

# Raster tekenen
inputs = []
for r in range(4):
    cols = st.columns(4)
    for c in range(4):
        val = cols[c].number_input(f"R{r}K{c}", value=st.session_state.inputs[r*4+c], 
                                   key=f"c{r}{c}", label_visibility="collapsed")
        inputs.append(val if val is not None else 0)

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Delete All"):
        st.session_state.inputs = [None] * 16
        st.rerun()

with col2:
    if st.button("CHECK NOW", type="primary"):
        matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
        doel = sum(matrix[0]) if controle_methode == "Automatisch (1e rij)" else doelgetal_handmatig
        
        st.info(f"🎯 Doel: **{int(doel)}**")
        foutmeldingen = []
        for i in range(4):
            if sum(matrix[i]) != doel: foutmeldingen.append(f"❌ Rij {i+1} klopt niet.")
            if sum(matrix[r][i] for r in range(4)) != doel: foutmeldingen.append(f"❌ Kolom {i+1} klopt niet.")
        if sum(matrix[i][i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonaal 1 klopt niet.")
        if sum(matrix[i][3-i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonaal 2 klopt niet.")
        
        if not foutmeldingen: st.success("🎉 Perfect!")
        else: [st.error(f) for f in foutmeldingen]
