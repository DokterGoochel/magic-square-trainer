import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Ultieme CSS-injectie om Streamlit's minimale pixelbreedte volledig te slopen
st.markdown("""
    <style>
    /* 1. Verwijder alle marges en borders van de hoofdcontainer op mobiel */
    .block-container {
        padding-left: 4px !important;
        padding-right: 4px !important;
        padding-top: 10px !important;
        max-width: 100% !important;
    }
    
    /* 2. Dwing de rij om exact de breedte van het scherm te zijn zonder overflow */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 3px !important; 
        width: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* 3. Geef elke kolom exact een kwart van het scherm minus de gap */
    [data-testid="column"] {
        width: calc(25% - 3px) !important;
        flex: 1 1 calc(25% - 3px) !important;
        min-width: 0px !important;
        max-width: 25% !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 4. OVERSCHRIJF DE MINIMALE BREEDTE VAN HET STREAMLIT ELEMENT */
    div[data-testid="stNumberInput"] {
        width: 100% !important;
        min-width: 0px !important;
        max-width: 100% !important;
    }
    div[data-testid="stNumberInput"] > div {
        width: 100% !important;
        min-width: 0px !important;
        max-width: 100% !important;
    }
    div[data-testid="stNumberInput"] input {
        width: 100% !important;
        min-width: 0px !important;
        max-width: 100% !important;
    }

    /* 5. Stijl het daadwerkelijke invoervak super compact voor portrait modus */
    input {
        font-size: 18px !important;
        text-align: center !important;
        height: 45px !important; /* Iets minder hoog voor betere verhouding */
        padding: 0px !important;
        margin: 0px !important;
        box-sizing: border-box !important;
    }
    
    /* Verwijder alle pijltjes en extra padding aan de binnenkant */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    .stNumberInput div div {
        padding-right: 0px !important; /* Verwijdert de verborgen ruimte voor de pijltjes */
    }

    /* DE GELE CONTROLEKNOP */
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border-color: #FFDE00 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        height: 50px !important;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Trainer V2")
st.write("De eerste rij bepaalt automatisch het doelgetal.")

st.write("---")

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
                    max_value=999,
                    value=None, 
                    step=1,
                    key=f"cell_{r}_{c}",
                    label_visibility="collapsed"
                )
                inputs.append(val)

st.write("---")

# De knop
if st.button("CONTROLEER NU", type="primary", use_container_width=True):
    veilig_inputs = [x if x is not None else 0 for x in inputs]
    matrix = [veilig_inputs[i:i+4] for i in range(0, 16, 4)]
    foutmeldingen = []

    doelgetal = sum(matrix[0])
    st.info(f"🎯 Controle op basis van eerste rij. Doelgetal: **{doelgetal}**")

    for i in range(4):
        rij_som = sum(matrix[i])
        kolom_som = sum(matrix[r][i] for r in range(4))
        
        if rij_som != doelgetal:
            foutmeldingen.append(f"❌ Rij {i+1} klopt niet (Som is {rij_som})")
        if kolom_som != doelgetal:
            foutmeldingen.append(f"❌ Kolom {i+1} klopt niet (Som is {kolom_som})")

    diag1 = sum(matrix[i][i] for i in range(4))
    diag2 = sum(matrix[i][3-i] for i in range(4))

    if diag1 != doelgetal:
        foutmeldingen.append(f"❌ Diagonaal linksboven-rechtsonder klopt niet (Som is {diag1})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonaal rechtsboven-linksonder klopt niet (Som is {diag2})")

    if not foutmeldingen:
        st.success(f"🎉 Perfect! Het vierkant is magisch (Som = {doelgetal})!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
