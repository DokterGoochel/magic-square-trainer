import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Alleen de CSS voor jouw gele knop blijft over
st.markdown("""
    <style>
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

# We maken het 4x4 raster in het geheugen
if 'magic_grid' not in st.session_state:
    # TRUC: We gebruiken oplopende aantallen spaties als kolomnamen zodat ze onzichtbaar zijn
    st.session_state.magic_grid = pd.DataFrame(
        [[None, None, None, None] for _ in range(4)],
        columns=["", " ", "  ", "   "]
    )

# De data_editor
edited_df = st.data_editor(
    st.session_state.magic_grid,
    hide_index=True,
    use_container_width=True,
    column_config={
        "": st.column_config.NumberColumn(label="", min_value=0, max_value=999, step=1),
        " ": st.column_config.NumberColumn(label="", min_value=0, max_value=999, step=1),
        "  ": st.column_config.NumberColumn(label="", min_value=0, max_value=999, step=1),
        "   ": st.column_config.NumberColumn(label="", min_value=0, max_value=999, step=1),
    }
)

st.write("---")

# De knop
if st.button("CHECK NOW", type="primary", use_container_width=True):
    matrix = edited_df.fillna(0).values.tolist()
    foutmeldingen = []

    doelgetal = sum(matrix[0])
    st.info(f"🎯 Check based on the first row. Target number is: **{int(doelgetal)}**")

    for i in range(4):
        rij_som = sum(matrix[i])
        kolom_som = sum(matrix[r][i] for r in range(4))
        
        if rij_som != doelgetal:
            foutmeldingen.append(f"❌ Row {i+1} is incorrect. (Sum is {int(rij_som)})")
        if kolom_som != doelgetal:
            foutmeldingen.append(f"❌ Column {i+1} is incorrect. (Sum is {int(kolom_som)})")

    diag1 = sum(matrix[i][i] for i in range(4))
    diag2 = sum(matrix[i][3-i] for i in range(4))

    if diag1 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal top-left to bottom-right is incorrect. (Sum is {int(diag1)})")
    if diag2 != doelgetal:
        foutmeldingen.append(f"❌ Diagonal top-right to bottom-left is incorrect. (Sum is {int(diag2)})")

    if not foutmeldingen:
        st.success(f"🎉 Perfect! The square is magic (Sum = {int(doelgetal)})!")
        st.balloons()
    else:
        for fout in foutmeldingen:
            st.error(fout)
