import streamlit as st
import py3Dmol
from stmol import showmol
import requests
import json
from datetime import datetime, timedelta
from python_styles.visualizer_style import (MAIN_CSS, 
                                            COL_5_CSS,
                                            TAB_OUTER_DIV,
                                            TAB_KEY_DIV,
                                            TAB_VALUE_DIV,
                                            TAB_VALUE_DIV_MONOSPACE,
                                            TAB_VALUE_DIV_OVERFLOW_WRAP 
                                            )
from python_styles.sidebar_style import SIDEBAR_CSS
# Set page layout to wide
# st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown(MAIN_CSS, unsafe_allow_html=True)

def render_protein_structure(pdb_string, style="cartoon", color="spectrum"):
    """Render protein structure using py3Dmol with specified style and color and auto-rotation"""
    view = py3Dmol.view(width=800, height=600)
    view.setBackgroundColor('black')
    view.addModel(pdb_string, "pdb")
    
    # Create style dictionary based on selected style and color
    style_dict = {}
    if style == "cartoon":
        style_dict = {'cartoon': {'color': color}}
    elif style == "stick":
        style_dict = {'stick': {'color': color}}
    elif style == "sphere":
        style_dict = {'sphere': {'color': color}}
    elif style == "surface":
        # Enhanced surface visualization settings
        view.setStyle({}, {'cartoon': {'color': 'spectrum'}})
        view.addSurface(py3Dmol.VDW, {
            'opacity': 0.9,
            'color': color if color != "spectrum" else "white"
        })
        style_dict = None
    
    if style_dict:
        view.setStyle({}, style_dict)
    
    view.zoomTo()
    view.spin('y', 1)
    
    return view

@st.cache_data(ttl=timedelta(hours=24))
def fetch_pdb_structure(pdb_id):
    """Fetch PDB structure from RCSB with caching"""
    url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

@st.cache_data(ttl=timedelta(hours=24))
def get_protein_info(pdb_id):
    """Fetch detailed protein information from PDB API with caching"""
    base_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    entity_url = f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/1"
    assembly_url = f"https://data.rcsb.org/rest/v1/core/assembly/{pdb_id}/1"
    
    try:
        response = requests.get(base_url)
        entity_response = requests.get(entity_url)
        assembly_response = requests.get(assembly_url)
        
        data = {}
        if response.status_code == 200:
            data['core'] = response.json()
        if entity_response.status_code == 200:
            data['entity'] = entity_response.json()
        if assembly_response.status_code == 200:
            data['assembly'] = assembly_response.json()
            
        return data
    except Exception as e:
        st.error(f"Error fetching protein information: {str(e)}")
        return None

def format_date(date_str):
    if date_str == 'N/A':
        return date_str
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%B %d, %Y')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')
        except ValueError:
            return date_str

def display_protein_info(pdb_id, data):
    if data:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Basic Info", "🧬 Structure Details", "🔬 Sequence & Composition", "📚 References"])
        
        with tab1:
            core_data = data.get('core', {})
            basic_items = [
                ("PDB ID", pdb_id),
                ("Title", core_data.get('struct', {}).get('title', 'N/A')),
                ("Classification", core_data.get('struct', {}).get('pdbx_descriptor', 'N/A')),
                ("Deposition Date", format_date(core_data.get('rcsb_accession_info', {}).get('deposit_date', 'N/A'))),
                ("Resolution", f"{core_data.get('rcsb_entry_info', {}).get('resolution_combined', 'N/A')} Å")
            ]
            
            for key, value in basic_items:
                st.markdown(f"""
                    <div style="{TAB_OUTER_DIV}">
                        <div style="{TAB_KEY_DIV}">{key}</div>
                        <div style="{TAB_VALUE_DIV}">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            entity_data = data.get('entity', {})
            structure_items = [
                ("Experimental Method", core_data.get('exptl', [{}])[0].get('method', 'N/A')),
                ("Structure Type", entity_data.get('entity_poly', {}).get('rcsb_entity_polymer_type', 'N/A')),
                ("Molecular Weight", f"{core_data.get('rcsb_entry_info', {}).get('molecular_weight', 'N/A')} Da"),
                ("Number of Chains", len(core_data.get('entity_poly', {}).get('pdbx_strand_id', []))),
                ("Release Date", core_data.get('rcsb_accession_info', {}).get('initial_release_date', 'N/A')),
                ("Structure Determination", core_data.get('rcsb_entry_info', {}).get('structure_determination_methodology', 'N/A'))
            ]
            
            for key, value in structure_items:
                st.markdown(f"""
                    <div style="{TAB_OUTER_DIV}">
                        <div style="{TAB_KEY_DIV}">{key}</div>
                        <div style="{TAB_VALUE_DIV}">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            entity_data = data.get('entity', {})
            sequence = entity_data.get('entity_poly', {}).get('pdbx_seq_one_letter_code', 'N/A')
            if sequence != 'N/A':
                st.markdown(f"""
                    <div style="{TAB_OUTER_DIV}">
                        <div style="{TAB_KEY_DIV}">Protein Sequence</div>
                        <div style="{TAB_VALUE_DIV_OVERFLOW_WRAP}">{sequence}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            composition = entity_data.get('rcsb_entity_polymer_monomer_counts', {})
            if composition:
                st.markdown(f"""
                    <div style="{TAB_OUTER_DIV}">
                        <div style="{TAB_KEY_DIV}">Amino Acid Composition</div>
                        <div style="{TAB_VALUE_DIV_OVERFLOW_WRAP}">{json.dumps(composition, indent=2)}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            citations = core_data.get('citation', [])
            
            # Add custom CSS for scrollable container with !important flags
            st.markdown("""
                <style>
                .scrollable-references {
                    max-height: 600px !important;
                    overflow-y: auto !important;
                    border-radius: 5px !important;
                    display: block !important;
                    position: relative !important;
                }
                
                /* Target the Streamlit tab content */
                .stTabs [data-baseweb="tab-panel"] {
                    max-height: 500px !important;
                    overflow-y: auto !important;
                }
                </style>
            """, unsafe_allow_html=True)
            
            # Create a container div
            st.markdown('<div class="scrollable-references">', unsafe_allow_html=True)
            
            # Rest of the citation display code remains the same
            for citation in citations:
                citation_items = [
                    ("Title", citation.get('title', 'N/A')),
                    ("Authors", ', '.join(citation.get('rcsb_authors', ['N/A']))),
                    ("Year", citation.get('year', 'N/A')),
                    ("DOI", f"[Link to paper](https://doi.org/{citation.get('pdbx_database_id_DOI', 'N/A')})" if citation.get('pdbx_database_id_DOI') else 'N/A')
                ]
                
                for key, value in citation_items:
                    st.markdown(f"""
                        <div style="{TAB_OUTER_DIV};">
                            <div style="{TAB_KEY_DIV}">{key}</div>
                            <div style="{TAB_VALUE_DIV_OVERFLOW_WRAP}">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        div.stmol-container > iframe {
            border-radius: 25px !important;
            border: 2px solid #42d64f !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            background-color: black !important;
        }
        
        div.stmol-container {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            background-color: black !important;
            padding: 20px !important;
        }
        
        iframe {
            border-radius: 25px !important;
            border: 2px solid #42d64f !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>🧬 Bio-Molecular Conformational Explorer 🧬</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
            @keyframes gradient-flow {
                0% { background-position: 0% 50%; }
                100% { background-position: 200% 50%; }
            }
        </style>
        <div style='
            height: 3px;
            background: linear-gradient(to right, #006400, #9370DB, #006400);
            background-size: 200% 100%;
            margin: -5px auto 20px auto;
            width: 80%;
            border-radius: 20px;
            animation: gradient-flow 3s linear infinite;
        '></div>
    """, unsafe_allow_html=True)
    
    example_pdbs = {
        "Hemoglobin": "1HHB",
        "Insulin": "4INS",
        "Green Fluorescent Protein": "1EMA",
        "Myoglobin": "1MBO",
        "Lysozyme": "1AKI"
    }
    
    # Initialize session state for visualization
    if 'current_pdb_id' not in st.session_state:
        st.session_state.current_pdb_id = None
        st.session_state.pdb_string = None
        st.session_state.protein_data = None
        st.session_state.show_visualization = False


    with st.expander("About Bio-Molecular Conformational Explorer", expanded=True):
        st.markdown("""
        ### 🧬 An Interactive Bio-Molecular Structures and Conformations Viewer
        - Visualize 3D protein structures from PDB database
        - Multiple visualization styles (cartoon, stick, sphere, surface)
        - Customizable color schemes
        - Detailed protein information in organized tabs
        - Download structures for offline use
        """)

        # Create two main columns for better organization
        input_col, viz_options_col = st.columns([1, 1])

        with input_col:
            st.markdown("""
                <div style='background-color: rgba(66, 214, 79, 0.1); 
                           border-left: 3px solid #42d64f; 
                           padding: 10px; 
                           border-radius: 5px;
                           margin-bottom: 15px;'>
                    <span style='color: #42d64f; font-weight: bold;'>STEP 1</span>
                    <span style='margin-left: 8px;'>Select Protein Structure</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Add key to radio to trigger rerun when changed
            input_method = st.radio("Input Method", ["Select Example", "Enter PDB ID"], horizontal=True, key="input_method")
            
            # Reset visualization state when input method changes
            if "last_input_method" not in st.session_state:
                st.session_state.last_input_method = input_method
            elif st.session_state.last_input_method != input_method:
                st.session_state.current_pdb_id = None
                st.session_state.pdb_string = None
                st.session_state.protein_data = None
                st.session_state.show_visualization = False
                st.session_state.last_input_method = input_method
            
            if input_method == "Select Example":
                # Add key to selectbox to detect changes
                selected_protein = st.selectbox("Select a protein", list(example_pdbs.keys()), key="protein_selector")
                # Reset state when a new protein is selected
                if "last_selected_protein" not in st.session_state:
                    st.session_state.last_selected_protein = selected_protein
                elif st.session_state.last_selected_protein != selected_protein:
                    st.session_state.current_pdb_id = None
                    st.session_state.pdb_string = None
                    st.session_state.protein_data = None
                    st.session_state.show_visualization = False
                    st.session_state.last_selected_protein = selected_protein
                
                pdb_id = example_pdbs[selected_protein]
            else:
                pdb_id = st.text_input("Enter PDB ID", placeholder="e.g., 1HHB").strip().upper()

        with viz_options_col:
            st.markdown("""
                <div style='background-color: rgba(66, 214, 79, 0.1); 
                           border-left: 3px solid #42d64f; 
                           padding: 10px; 
                           border-radius: 5px;
                           margin-bottom: 15px;'>
                    <span style='color: #42d64f; font-weight: bold;'>STEP 2</span>
                    <span style='margin-left: 8px;'>Visualization Options</span>
                </div>
            """, unsafe_allow_html=True)
            # Moved radio buttons first
            color_option = st.radio("Color Scheme", 
                                  ["Default (Spectrum)", "Custom Color"], 
                                  horizontal=True,
                                  help="Select between rainbow spectrum or custom color")
            
            # Moved style selectbox after radio buttons
            style = st.selectbox("Visualization Style", 
                               ["cartoon", "stick", "sphere", "surface"],
                               help="Choose how the protein structure should be displayed")
            
            if color_option == "Custom Color":
                color = st.color_picker("Pick a color", "#00FF00")
            else:
                color = "spectrum"

        # Center the visualize button and make it more prominent
        _, button_col, _ = st.columns([1, 2, 1])
        with button_col:
            st.markdown("""
                <div style='background-color: rgba(66, 214, 79, 0.1); 
                           border-left: 3px solid #42d64f; 
                           padding: 10px; 
                           border-radius: 5px;
                           margin-bottom: 15px;'>
                    <span style='color: #42d64f; font-weight: bold;'>STEP 3</span>
                    <span style='margin-left: 8px;'>Generate Visualization</span>
                </div>
            """, unsafe_allow_html=True)
            visualize_button = st.button("Visualize", use_container_width=True)

        # Inside expander
        if visualize_button and pdb_id:
            st.session_state.show_visualization = True
            st.session_state.loading = True

    st.markdown("---")  # Line break after expander

    # Loading logic moved outside expander
    if st.session_state.get('loading', False) and pdb_id != st.session_state.get('current_pdb_id'):
        try:
            col1, spinner_col, col3 = st.columns([1.1, 0.8, 1])
            with spinner_col:
                pdb_string = fetch_pdb_structure(pdb_id)
                data = get_protein_info(pdb_id) if pdb_string else None
                
                if not pdb_string:
                    st.error("Failed to fetch structure. Please check the PDB ID.")
                else:
                    st.session_state.current_pdb_id = pdb_id
                    st.session_state.pdb_string = pdb_string
                    st.session_state.protein_data = data
            st.session_state.loading = False
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.loading = False

    # Display visualization
    if st.session_state.show_visualization:
        if st.session_state.pdb_string and st.session_state.protein_data:
            viz_col, _, info_col = st.columns([1, 0.8, 1])
            
            with viz_col:
                view = render_protein_structure(st.session_state.pdb_string, style=style, color=color)
                showmol(view, height=600, width=800)
            
            with info_col:
                display_protein_info(st.session_state.current_pdb_id, st.session_state.protein_data)
            
            st.markdown("---")
            
            dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
            with dl_col2:
                st.download_button(
                    label="Download PDB",
                    data=st.session_state.pdb_string,
                    file_name=f"{st.session_state.current_pdb_id}.pdb",
                    mime="chemical/x-pdb",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
