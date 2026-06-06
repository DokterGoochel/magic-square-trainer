import streamlit as st

# Pagina-instellingen
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Ultieme CSS om het 4x4 raster in portrait-stand te dwingen
st.markdown("""
    <style>
    /* 1. Verwijder alle zijwaartse marges van de hoofdcontainer */
    .block-container {
        padding-left: 5px !important;
        padding-right: 5px !important;
        padding-top: 10px !important;
        max-width: 100% !important;
    }
    
    /* 2. Zorg dat de rijen geen extra padding hebben */
    [data-testid="stHorizontalBlock"] {
        gap: 2px !important; 
        width: 100% !important;
    }
    
    /* 3. Dwing kolommen naar exact 25% en verbied elke vorm van uitloop */
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0px !important;
    }

    /* 4. Maak het invoerveld extreem compact */
    div[data-testid="stNumberInput"] {
        width: 100% !important;
        min-width: 0px !important;
    }
    
    input {
        font-size: 18px !important; /* Iets kleiner voor portrait */
        text-align: center !important;
        height: 45px !important;   /* Iets minder hoog voor betere fit */
        padding: 0px !important;
        margin: 0px !important;
        width: 100% !important;
        min-width: 0px !important;
        border-radius: 4px !important;
    }
    
    /* Verwijder de knoppen in de input die ruimte innemen */
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }

    /* DE GELE CONTROLEKNOP */
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border-color: #FFDE00 !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Trainer V2")
st.write("Eerste rij = doelgetal.")

# Het 4x4 raster
with st.container():
    inputs = []
    for r in range(4):
        cols = st.columns(4)
        for c in range(4):
            with cols[c]:
                val = st.number_input(
                    label=f"R{r}K{c}",
                    min_value=0,
                    value=None, 
                    key=f"cell_{r}_{c}",
                    label_visibility="collapsed"
                )
                inputs.append(val)

st.write("---")

if st.button("CONTROLEER NU", type="primary", use_container_width=True):
    veilig_inputs = [x if x is not None else 0 for x in inputs]
    matrix = [veilig_inputs[i:i+4] for i in range(0, 16, 4)]
    
    doelgetal = sum(matrix[0])
    st.info(f"🎯 Doelgetal: **{doelgetal}**")

    foutmeldingen = []
    for i in range(4):
        if sum(matrix[i]) != doelgetal: foutmeldingen.append(f"❌ Rij {i+1}")
        if sum(matrix[r][i] for r in range(4)) != doelgetal: foutmeldingen.append(f"❌ Kolom {i+1}")

    if sum(matrix[i][i] for i in range(4)) != doelgetal: foutmeldingen.append("❌ Diagonaal 1")
    if sum(matrix[i][3-i] for i in range(4)) != doelgetal: foutmeldingen.append("❌ Diagonaal 2")

    if not foutmeldingen:
        st.success("🎉 Perfect!")
        st.balloons()
    else:
        st.error(f"Fouten in: {', '.join(foutmeldingen)}")
