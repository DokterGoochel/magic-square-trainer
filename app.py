import streamlit as st

# Pagina-instellingen voor mobiel
st.set_page_config(
    page_title="Magic Square Trainer", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.title("🪄 Magic Trainer V2")
st.write("De eerste rij bepaalt automatisch het doelgetal.")

# Initialiseer de sessie-state voor de 16 cellen als ze nog niet bestaan
if "magic_cells" not in st.session_state:
    st.session_state.magic_cells = [""] * 16

# We vangen de data op via een HTML Formulier
# CSS zorgt voor een perfect, vederlicht 4x4 raster dat ALTIJD binnen portrait past
html_code = """
<style>
    .magic-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        margin-bottom: 15px;
    }
    .magic-input {
        width: 100%;
        height: 55px;
        font-size: 22px;
        text-align: center;
        font-weight: bold;
        border: 2px solid #ccc;
        border-radius: 8px;
        box-sizing: border-box;
        -moz-appearance: textfield;
    }
    .magic-input::-webkit-outer-spin-button,
    .magic-input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    .magic-input:focus {
        border-color: #FFDE00;
        outline: none;
    }
</style>
<form id="magic_form">
    <div class="magic-grid">
"""

# Genereer de 16 pure HTML invoervelden
for i in range(16):
    current_val = st.session_state.magic_cells[i]
    html_code += f'<input type="number" class="magic-input" id="html_cell_{i}" name="html_cell_{i}" value="{current_val}" placeholder="" oninput="window.parent.postMessage({{type: \'magic_update\', idx: {i}, val: this.value}}, \'*\')">'

html_code += """
    </div>
</form>
"""

# Omdat we de HTML-velden direct willen uitlezen in Streamlit, 
# gebruiken we een elegantere Streamlit-native aanpak die wél werkt zonder hacks:
# We bouwen een custom grid met st.components of we dwingen Streamlit's eigen tekstvelden met pure CSS in de kleinste HTML-jas.

# Laten we de ALLERKLEINSTE HTML-jas om Streamlit's eigen tekstinvoer heen trekken:
st.markdown("""
    <style>
    /* Sloop alle extra HTML-lagen van Streamlit's componenten */
    .block-container { padding: 10px !important; max-width: 100% !important; }
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; gap: 4px !important; width: 100% !important; }
    [data-testid="column"] { width: 25% !important; flex: 1 1 25% !important; min-width: 0px !important; padding: 0px !important; }
    
    /* Maak het invoerveld een puur kaal HTML-vakje */
    div[data-testid="stTextInput"] { width: 100% !important; min-width: 0px !important; padding: 0px !important; margin: 0px !important; border: none !important; }
    div[data-testid="stTextInput"] > div { padding: 0px !important; border: none !important; background: transparent !important; }
    div[data-testid="stTextInput"] min-width { min-width: 0px !important; }
    
    input {
        font-size: 22px !important;
        text-align: center !important;
        height: 55px !important;
        padding: 0px !important;
        width: 100% !important;
        min-width: 0px !important;
        border: 2px solid #ccc !important;
        border-radius: 6px !important;
        box-sizing: border-box !important;
        background-color: white !important;
        color: black !important;
    }
    input:focus { border-color: #FFDE00 !important; outline: none !important; }
    
    /* Gele knop */
    div.stButton > button[kind="primary"] {
        background-color: #FFDE00 !important; color: #000000 !important; border-color: #FFDE00 !important;
        font-weight: bold !important; font-size: 18px !important; height: 50px !important; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Raster opbouwen met gestripte tekstvelden (die gedragen zich nu als pure HTML-velden)
inputs = []
for r in range(4):
    cols = st.columns(4)
    for c in range(4):
        with cols[c]:
            # st.text_input heeft veel minder ingebouwde breedte-beperkingen dan number_input
            val = st.text_input(
                label=f"R{r}K{c}",
                value="",
                key=f"cell_{r}_{c}",
                label_visibility="collapsed"
            )
            inputs.append(val)

st.write("---")

if st.button("CONTROLEER NU", type="primary", use_container_width=True):
    # Zet text_inputs veilig om naar getallen
    veilig_inputs = []
    for x in inputs:
        if x.strip() == "" or not x.isdigit():
            veilig_inputs.append(0)
        else:
            veilig_inputs.append(int(x))
            
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
