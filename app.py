import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Gecorrigeerde CSS die voorkomt dat kolommen onder elkaar klappen op mobiel
st.markdown("""
    <style>
    /* Maak de invoervelden groter en centreer de tekst */
    input {
        font-size: 22px !important;
        text-align: center !important;
        height: 55px !important;
        padding: 0px !important;
    }
    /* Verwijder de pijltjes (spinners) bij de getallen */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    /* FORCEER 4 KOLOMMEN NAAST ELKAAR OP MOBIEL */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
    }
    [data-testid="column"] {
        width: 23% !important;
        flex: 1 1 23% !important;
        min-width: 0px !important;
        padding: 0px !important;
    }

    /* HIER MAKEN WE DE CONTROLEKNOP GEEL */
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border-color: #FFDE00 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        height: 50px !important;
        margin-top: 15px;
    }
    div.stButton > button[kind="primary"]:hover, 
    div.stButton > button[kind="primary"]:active, 
    div.stButton > button[kind="primary"]:focus {
        background-color: #E6C600 !important;
        border-color: #E6C600 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer V2")
st.write("Fill in the square. The first row automatically determines the target number against which it is checked.")

st.write("---")

# Het 4x4 raster - Geforceerd in grid-layout
with st.container():
    inputs = []
    for r in range(4):
        # We maken per rij 4 kolommen aan
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
