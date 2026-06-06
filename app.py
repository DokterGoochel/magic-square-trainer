import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS om de invoervelden groter en 'mobiel-vriendelijker' te maken
st.markdown("""
    <style>
    /* Maak de invoervelden groter en centreer de tekst */
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
    /* Zorg dat de kolommen op mobiel goed aansluiten */
    [data-testid="column"] {
        padding: 5px !important;
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
                    value=0,
                    key=f"cell_{r}_{c}",
                    label_visibility="collapsed"
                )
                inputs.append(val)

st.write("---")

# Grote knop voor mobiel gebruik
if st.button("CHECK NOW", type="primary", use_container_width=True):
    # Waarden omzetten naar een 4x4 matrix
    matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
    foutmeldingen = []

    # De allereerste rij (Rij 1) bepaalt de controle-uitkomst (het doelgetal)
    doelgetal = sum(matrix[0])
    
    st.info(f"🎯 Controleren op basis van de eerste rij. Doelgetal is: **{doelgetal}**")

    # Check alle rijen en kolommen
    for i in range(4):
        rij_som = sum(matrix[i])
        kolom_som = sum(matrix[r][i] for r in range(4))
        
        if rij_som != doelgetal:
            foutmeldingen.append(f"❌ Row {i+1} is incorrect. (Sum is {rij_som})")
        if kolom_som != doelgetal:
            foutmeldingen.append(f"❌ Column {i+1} is incorrect. (Sum is {kolom_som})")

    # Check diagonalen
    diag1 = sum(matrix[i][i] for i in range(4))
    diag2 = sum(matrix[i][3-i] for i in range(4))

    if diag1 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal (top left-bottom right) is incorrect. (Sum is {diag1})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal (bottom left-top right) is incorrect. (Sum is {diag2})")

    # Het eindoordeel tonen
    if not foutmeldingen:
        st.success(f"🎉 Perfect! All rows, columns, corners, diagonals and inner squares add up to {doelgetal}!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
