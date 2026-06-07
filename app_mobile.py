import streamlit as st
import pandas as pd

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

# CSS voor de gele knop
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important;
        color: #000000 !important;
        border: 2px solid #FFDE00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Magic Square Trainer")

# Initialiseer dataframe met gehele getallen (0)
def reset_grid():
    st.session_state.magic_grid = pd.DataFrame(
        [[0] * 4 for _ in range(4)],
        columns=["", " ", "  ", "   "]
    )

if 'magic_grid' not in st.session_state:
    reset_grid()
if 'reset' not in st.session_state: 
    st.session_state.reset = 0

# Keuze voor controle methode (Engels)
controle_methode = st.radio("Target value:", ["Automatic (sum of first row)", "Manual input"])

# Dynamische invoer voor handmatig doelgetal met een strak kader
doelgetal_handmatig = 0
if controle_methode == "Manual input":
    with st.container(border=True):
        doelgetal_handmatig = st.number_input(
            "Enter your target number:", min_value=0, step=1, format="%d", 
            key=f"doel_{st.session_state.reset}"
        )

# Data editor voor gehele getallen geoptimaliseerd voor mobiel
edited_df = st.data_editor(
    st.session_state.magic_grid, 
    hide_index=True, 
    use_container_width=True,
    column_config={col: st.column_config.NumberColumn(label="", min_value=0, max_value=999, step=1, format="%d") 
                   for col in st.session_state.magic_grid.columns}
)

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Delete All"):
        reset_grid()
        st.session_state.reset += 1
        st.rerun()

with col2:
    if st.button("CHECK NOW", type="primary"):
        # Dwing matrix om naar pure integers te gaan
        matrix = edited_df.fillna(0).astype(int).values.tolist()
        
        # Bepaal het doelgetal op basis van de gekozen methode
        if controle_methode == "Automatic (sum of first row)":
            doel = sum(matrix[0])
        else:
            doel = doelgetal_handmatig
        
        st.info(f"🎯 Target: **{int(doel)}**")
        
        foutmeldingen = []
        for i in range(4):
            if sum(matrix[i]) != doel: foutmeldingen.append(f"❌ Row {i+1} is incorrect.")
            if sum(matrix[r][i] for r in range(4)) != doel: foutmeldingen.append(f"❌ Column {i+1} is incorrect.")
        if sum(matrix[i][i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonal (top left-bottom right) is incorrect.")
        if sum(matrix[i][3-i] for i in range(4)) != doel: foutmeldingen.append("❌ Diagonal (bottom left-top right) is incorrect.")
        
        if not foutmeldingen:
            st.success(f"🎉 Perfect. This square is magical in every way. It all adds up to {int(doel)}.")
            st.balloons()
        else:
            # Schone for-loop voorkomt de dropdown-fout op mobiel
            for fout in foutmeldingen:
                st.error(fout)
