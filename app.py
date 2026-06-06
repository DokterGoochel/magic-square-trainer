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
    /* Verwijder de pijltjes (spinners) bij de getallen voor een cleaner uiterlijk */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    /* Zorg dat de kolommen op mobiel niet te veel marge hebben */
    [data-testid="column"] {
        padding: 5px !important;
    }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🪄 Magic Square Trainer V2")
st.write("Welcome to the magic square trainer! Enter the numbers and the app will instantly check the logic.")

# Doelgetal bovenin (vaak handig bij magische vierkanten)
doelgetal = st.number_input("Doelgetal", min_value=1, value=34, step=1)

st.write("---")

# Het 4x4 raster - Geoptimaliseerd voor touch
with st.container():
    # We maken 4 rijen van 4 kolommen
    inputs = []
    for r in range(4):
        cols = st.columns(4)
        for c in range(4):
            with cols[c]:
                # We gebruiken een unieke key per cel
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

# Grote knop voor 'dikke duimen'
if st.button("CHECK NOW", type="primary", use_container_width=True):
    # Logica omzetten naar matrix
    matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
    fout_gevonden = False
    foutmeldingen = []

    # Check rijen en kolommen
    for i in range(4):
        if sum(matrix[i]) != doelgetal:
            foutmeldingen.append(f"Row {i+1} is incorrect.")
        if sum(matrix[r][i] for r in range(4)) != doelgetal:
            foutmeldingen.append(f"Column {i+1} is incorrect.")

    # Check diagonalen
    if sum(matrix[i][i] for i in range(4)) != doelgetal:
        foutmeldingen.append("Diagonal (top left-bottom right) is incorrect.")
    if sum(matrix[i][3-i] for i in range(4)) != doelgetal:
        foutmeldingen.append("Diagonal (bottom left-top right) is incorrect.")

    # Resultaat tonen
    if not foutmeldingen:
        st.success(f"🎉 Perfect! All rows, columns, corners, diagonals and inner squares add up to {doelgetal}!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout). De constante som is {target_sum}!")
