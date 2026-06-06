import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Ultieme CSS-overrule om stapelen en uitlopen te voorkomen
st.markdown("""
    <style>
    /* Verwijder alle zijwaartse witruimte van de Streamlit pagina op mobiel */
    .block-container {
        padding-left: 5px !important;
        padding-right: 5px !important;
        padding-top: 15px !important;
        max-width: 100% !important;
    }
    
    /* Dwing de container om exact 100% van de schermbreedte te pakken */
    [data-testid="stVerticalBlock"] {
        width: 100% !important;
        padding: 0px !important;
    }

    /* FORCEER 4 KOLOMMEN NAAST ELKAAR (NOOIT ONDER ELKAAR) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important; 
        width: 100% !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Geef elke kolom exact een kwart van de beschikbare schermruimte */
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Maak de invoervakken compact en dwing ze binnen de kolom */
    input {
        font-size: 18px !important;
        text-align: center !important;
        height: 50px !important;
        padding: 0px !important;
        width: 100% !important;
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

st.title("🪄 Magic Square Trainer V2")
st.write("Fill in the square. The first row automatically determines the target number against which it is checked.")

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
if st.button("CHECK NOW", type="primary", use_container_width=True):
    veilig_inputs = [x if x is not None else 0 for x in inputs]
    matrix = [veilig_inputs[i:i+4] for i in range(0, 16, 4)]
    foutmeldingen = []

    doelgetal = sum(matrix[0])
    st.info(f"🎯 Check based on the first row. Target number is: **{doelgetal}**")

    for i in range(4):
        rij_som = sum(matrix[i])
        kolom_som = sum(matrix[r][i] for r in range(4))
        
        if rij_som != doelgetal:
            foutmeldingen.append(f"❌ Row {i+1} is incorrect. (Sum is {rij_som})")
        if kolom_som != doelgetal:
            foutmeldingen.append(f"❌ Column {i+1} is incorrect. (Sum is {kolom_som})")

    diag1 = sum(matrix[i][i] for i in range(4))
    diag2 = sum(matrix[i][3-i] for i in range(4))

    if diag1 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal (top left-bottom right) is incorrect. (Sum is {diag1})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal (bottom left-top right) is incorrect. (Sum is {diag2})")

    if not foutmeldingen:
        st.success(f"🎉 Perfect. This square is magical in every way (Sum = {doelgetal})!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
