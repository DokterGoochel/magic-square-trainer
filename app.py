import streamlit as st

st.set_page_config(page_title="Magic Square Trainer", layout="centered")

st.title("🪄 Magic Square Trainer")
st.write("Welkom bij je persoonlijke trainer! Vul de getallen in en de app controleert direct de logica.")

# Wij maken een container voor het magische vierkant
with st.container():
    cols = st.columns(4)
    inputs = []
    
    # We genereren een 4x4 grid voor de invoer
    for i in range(16):
        col_idx = i % 4
        with cols[col_idx]:
            val = st.number_input(
                label=f"Cel {i+1}", 
                min_value=0, 
                max_value=999, 
                value=0, 
                key=f"magic_cell_{i}", 
                label_visibility="collapsed"
            )
            inputs.append(val)

st.write("---")

# De controleknop (als vervanger van het automatische doorrekenen in Excel)
if st.button("Controleer Vierkant", type="primary", use_container_width=True):
    # We zetten de 16 losse inputs om naar een 2D matrix (4 rijen van 4)
    matrix = [inputs[i:i+4] for i in range(0, 16, 4)]
    
    # Excel ALS-logica vertaling:
    # We pakken de som van de eerste rij als het referentie-doelgetal
    target_sum = sum(matrix[0])
    fout_gevonden = False
    
    # 1. Controleer alle rijen en kolommen
    for i in range(4):
        rij_som = sum(matrix[i])
        kolom_som = sum(matrix[r][i] for r in range(4))
        
        if rij_som != target_sum:
            st.error(f"❌ Rij {i+1} klopt niet (Som is {rij_som}, moet {target_sum} zijn)")
            fout_gevonden = True
        if kolom_som != target_sum:
            st.error(f"❌ Kolom {i+1} klopt niet (Som is {kolom_som}, moet {target_sum} zijn)")
            fout_gevonden = True

    # 2. Controleer de diagonalen
    diag1 = sum(matrix[i][i] for i in range(4))
    diag2 = sum(matrix[i][3-i] for i in range(4))
    
    if diag1 != target_sum:
        st.error(f"❌ Diagonaal linksboven naar rechtsonder klopt niet (Som is {diag1})")
        fout_gevonden = True
    if diag2 != target_sum:
        st.error(f"❌ Diagonaal rechtsboven naar linksonder klopt niet (Som is {diag2})")
        fout_gevonden = True

    # 3. Het eindoordeel (De ultieme ALS/DAN plakkaat)
    if not fout_gevonden:
        st.success(f"🎉 Perfect! Het vierkant is magisch. De constante som is {target_sum}!")