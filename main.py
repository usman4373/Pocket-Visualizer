import streamlit as st
import os
import tempfile
from config.settings import COLOR_PRESETS, EMOJI_MAPPING
from visualization.pymol_viz import visualize_interactions, surface_visualizations
from data_handling.file_io import write_interacting_residues_csv
from utils.helpers import update_log

# Initialize session state
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []

# Page layout
col1, col2 = st.columns([2, 5])
with col1:
    st.markdown("<h1 style='text-align: left;'>Pocket<br>Visualizer</h1>", unsafe_allow_html=True)
with col2:
    st.image("icon/complex.png", width=200)

# Sidebar controls
st.sidebar.header("Upload or Select Directory")
uploaded_files = st.sidebar.file_uploader("Upload PDB Files", type=['pdb'], accept_multiple_files=True)
input_dir = st.sidebar.text_input("Or Enter Input Directory Path")
output_dir = st.sidebar.text_input("Enter Output Directory Path", "PocketVisualizer_Complexes")

# Color presets
st.sidebar.markdown("**Color Palettes**")
selected_preset = st.sidebar.radio(
    label="Choose visualization style:",
    options=list(COLOR_PRESETS.keys()),
    index=0,
    format_func=lambda x: f"{EMOJI_MAPPING[x]} {x}",
    help=
    "Ocean (protein: blue, ligand: green, interacting residues: pink)  \n\n"
    "Verdant (protein: green, ligand: ruby, interacting residues: marine)  \n\n"
    "Crimson (protein: red, ligand: green cyan, interacting residues: deep teal)  \n\n"
    "Ash (protein: gray, ligand: deep teal, interacting residues: orange)  \n\n"
    "Blossom (protein: pink, ligand: orange, interacting residues: deep teal)  \n\n")

# Quality settings
st.sidebar.markdown("**Image Settings**")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    width = st.number_input("Width", min_value=100, max_value=10000, value=2000, step=100)
with col2:
    height = st.number_input("Height", min_value=100, max_value=10000, value=1400, step=100)
with col3:
    dpi = st.number_input("DPI", min_value=200, max_value=1000, value=600, step=50)

# Main processing
processed_files = {}
if st.sidebar.button("Run Visualizations"):
    output_dir = "PocketVisualizer_Complexes"
    os.makedirs(output_dir, exist_ok=True)
    selected_preset_config = COLOR_PRESETS[selected_preset]
    log_placeholder = st.empty()
    st.session_state.log_messages.clear()
    processed_files.clear()

    # Process files
    def process_files(file_list, temp_dir=None):
        for file_info in file_list:
            if temp_dir:  # Uploaded files
                pdb_path = os.path.join(temp_dir, file_info.name)
                display_name = file_info.name
            else:  # Directory files
                pdb_path = file_info
                display_name = os.path.basename(pdb_path)

            update_log(f"🚀 Processing: {display_name}", log_placeholder)
        
            try:
                # Interaction visualization
                interaction_image, interaction_session = visualize_interactions(
                    pdb_path, output_dir, selected_preset,
                    ligand_colors=selected_preset_config["interaction_ligand"],
                    residues_color=selected_preset_config["residues"],
                    width=width, height=height, dpi=dpi
                )
            
                if interaction_image:
                    update_log(f"   ├─ 📷 Interaction image saved: {os.path.basename(interaction_image)}", log_placeholder)
                    update_log(f"   └─ 💾 Session file saved: {os.path.basename(interaction_session)}", log_placeholder)
                else:
                    raise Exception("❌ Interaction visualization failed")

                # Surface visualization
                surface_image, surface_session = surface_visualizations(
                    pdb_path, output_dir, selected_preset,
                    ligand_color=selected_preset_config["surface_ligand"],
                    residues_color=selected_preset_config["residues"],
                    width=width, height=height, dpi=dpi
                )
            
                if surface_image:
                    update_log(f"   ├─ 📷 Surface image saved: {os.path.basename(surface_image)}", log_placeholder)
                    update_log(f"   └─ 💾 Surface session saved: {os.path.basename(surface_session)}", log_placeholder)
                else:
                    raise Exception("❌ Surface visualization failed")

                processed_files[display_name] = {
                    "interaction_image": interaction_image,
                    "surface_image": surface_image
                }
                update_log(f"✅ {display_name} complete!  \n", log_placeholder)

            except Exception as e:
                update_log(f"❌ Error processing {display_name}: {str(e)}", log_placeholder)
                update_log(f"⚠️ Skipping {display_name}  \n", log_placeholder)

    # Handle input source
    if uploaded_files:
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_files:
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            process_files(uploaded_files, temp_dir)
    elif input_dir and os.path.isdir(input_dir):
        pdb_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".pdb")]
        process_files(pdb_files)

# Display results
if processed_files:
    st.success("Visualizations Completed! 🎉")
    st.markdown("""
        <style>
            .scrollable-container {
                max-height: 600px;
                overflow-y: auto;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
    for file_name, data in processed_files.items():
        col1, col2 = st.columns(2)
        with col1:
            st.image(data['interaction_image'], caption=f"{file_name} - Interaction View", width=200)
        with col2:
            st.image(data['surface_image'], caption=f"{file_name} - Surface View", width=200)
        
        with st.expander(f"🔍 Enlarge {file_name}"):
            st.image(data['interaction_image'], use_column_width=True)
            st.image(data['surface_image'], use_column_width=True)
        st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)
