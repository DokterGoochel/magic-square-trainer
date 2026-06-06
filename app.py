import streamlit as st

st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* STANDAARD (DESKTOP & LANDSCAPE) - Jouw stabiele weergave */
    input {
        font-size: 24px !important;
        text-align: center !important;
        height: 60px !important;
        width: 100% !important;
    }
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    /* SPECIFIEKE FIX VOOR MOBIEL PORTRAIT (< 600px breed) */
    @media (max-width: 600px) {
        /* 1. Haal de uiterste zijranden van het scherm weg */
        .block-container {
            padding-left: 2px !important;
            padding-right: 2px !important;
        }
        
        /* 2. Dwing de horizontale rij af en maak de tussenruimte heel klein (2px) */
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important; 
            width: 100% !important;
        }
        
        /* 3. Dwing de kolommen om flexibel te krimpen */
        [data-testid="column"] {
            flex: 1 1 0% !important;
            min-width: 0px !important;
            padding: 0px !important;
        }
        
        /* 4. DE ULTIEME OPLOSSING: Dwing ELK verborgen Streamlit-laagje om mee te krimpen */
        [data-testid="column"] * {
            min-width: 0px !important;
        }
        
        /* 5. Maak het vakje en de tekst iets compacter zodat het fysiek in de breedte past */
        input {
            font-size: 18px !important;
            height: 48px !important;
            padding: 0px !important;
        }
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
        foutmeldingen.append(f"❌ Diagonal top-left to bottom-right is incorrect. (Sum is {diag1})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal top-right to bottom-left is incorrect. (Sum is {diag2})")

    if not foutmeldingen:
        st.success(f"🎉 Perfect! The square is magic (Sum = {doelgetal})!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
