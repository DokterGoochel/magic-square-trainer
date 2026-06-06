import streamlit as st

# Pagina-instellingen voor mobiel (Uit jouw stabiele basis)
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS gebaseerd op jouw stabiele versie, met de fix tegen het onder elkaar stapelen
st.markdown("""
    <style>
    /* Maak de invoervelden groter en centreer de tekst (Uit jouw basis) */
    input {
        font-size: 24px !important;
        text-align: center !important;
        height: 60px !important;
    }
    /* Verwijder de pijltjes (spinners) bij de getallen */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    /* DE FIXED LOGICA TEGEN HET VERTICAAL STAPELEN */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* Dwingt te allen tijde een horizontale rij af */
        flex-wrap: nowrap !important;   /* Voorkomt dat kolommen naar een nieuwe regel springen */
        gap: 6px !important;            /* Ruimte tussen de vakjes op mobiel */
        width: 100% !important;
    }
    
    [data-testid="column"] {
        padding: 2px !important;         /* Iets compacter dan 5px zodat het makkelijker past */
        min-width: 0px !important;       /* Strijkt de minimale breedte van Streamlit glad */
        flex: 1 1 0% !important;        /* Verdeelt de kolommen exact gelijk over het scherm */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer V2")
st.write("Fill in the square. The first row automatically determines the target number against which it is checked.")

st.write("---")

# Het 4x4 raster - Geoptimaliseerd voor touch
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

# De knop (Uit jouw stabiele basis)
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
        foutmeldingen.append(f"❌ Diagonal top-left to bottom-right is incorrect. (Sum is {diag1})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal top-right to bottom-left is incorrect. (Sum is {diag2})")

    if not foutmeldingen:
        st.success(f"🎉 Perfect! The square is magic (Sum = {doelgetal})!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
