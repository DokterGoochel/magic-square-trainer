import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# De ultieme CSS-injectie om de minimale breedte van Streamlit te vernietigen
st.markdown("""
    <style>
    /* 1. Verwijder alle marges van de hoofdpagina zodat we de breedte optimaal benutten */
    .block-container {
        padding-left: 8px !important;
        padding-right: 8px !important;
        padding-top: 15px !important;
        max-width: 100% !important;
    }
    
    /* 2. Forceer de horizontale rij om ALTIJD 100% van het scherm te zijn, zonder scrollbalk */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important; 
        width: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* 3. Dwing elke kolom op exact 25% van de beschikbare schermruimte */
    [data-testid="column"] {
        width: calc(25% - 3px) !important;
        flex: 1 1 calc(25% - 3px) !important;
        min-width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* 4. VERNIETIG DE MINIMALE BREEDTE VAN HET STREAMLIT ELEMENT */
    div[data-testid="stNumberInput"] {
        width: 100% !important;
        min-width: 0px !important;
    }
    div[data-testid="stNumberInput"] > div {
        width: 100% !important;
        min-width: 0px !important;
    }

    /* 5. Stijl het daadwerkelijke invoervak (de input tag zelf) */
    input {
        font-size: 20px !important;
        text-align: center !important;
        height: 50px !important;
        padding: 0px !important;
        width: 100% !important;
        min-width: 0px !important;
        box-sizing: border-box !important;
    }
    
    /* Verwijder de pijltjes bij de getallen */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
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
