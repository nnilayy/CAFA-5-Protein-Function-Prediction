import streamlit as st
import base64
from pathlib import Path

# This must be the first Streamlit command
st.set_page_config(
    page_title="BioCore Suite",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the decoration bar
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Import the pages with updated names
from bio_molecular_explorer import main as bio_molecular_explorer_page
from proteomic_dashboard import main as proteomic_dashboard_page
from genomic_navigator import main as genomic_navigator_page

# Apply CSS
from python_styles.home_style import MAIN_CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)
from python_styles.sidebar_style import SIDEBAR_CSS

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def landing():
    st.markdown('<h1 class="main-title">🧬 BioCore Suite 🧬</h1>', unsafe_allow_html=True)
    
    st.markdown("""
        Welcome to BioCore 👋 !!
        
        A comprehensive bioinformatics platform designed for molecular biology research and analysis. This suite integrates essential 
        tools for exploring protein structures, analyzing sequence data, and understanding gene relationships through three 
        specialized modules, these are mentioned as given
    """)
    
    # First card: Image+title left, text right
    image_path = "assets/protein-vis.png"
    if Path(image_path).exists():
        img_base64 = img_to_base64(image_path)
        st.markdown("""
            <style>
            .hover-image {
                filter: grayscale(100%);
                transition: filter 0.3s ease;
                cursor: pointer;
            }
            .hover-image:hover {
                filter: grayscale(0%);
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="display: flex; gap: 20px;">
                    <div style="flex: 1;">
                        <h3 style="margin-top: 0; color: #42d64f; text-align: center;">Bio-Molecular Conformational Explorer</h3>
                        <img class="hover-image" src="data:image/png;base64,{img_base64}" alt="Bio-Molecular Conformational Explorer" 
                             style="width: 90%; height: 250px; border-radius: 15px; object-fit: cover; display: block; margin: 0 auto; border: 1px solid rgba(66, 214, 79, 0.3);">
                    </div>
                    <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
                        <p style="color: #ffffff; font-style: italic; text-align: center;">A real-time bio-molecular structure viewer that fetches and renders protein data 
                        from the PDB database. Visualize structures with customizable representations 
                        and color schemes, while accessing comprehensive protein information including 
                        sequence data, citations, and structural parameters. Load structures via PDB IDs 
                        or choose from curated examples with downloadable PDB files.</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Image not found")
    
    # Second card: Text left, Image+title right
    image_path = "assets/protein-profiling.png"
    if Path(image_path).exists():
        img_base64 = img_to_base64(image_path)
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="display: flex; gap: 20px;">
                    <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
                        <p style="color: #ffffff; font-style: italic; text-align: center;">A protein sequence analysis tool that processes FASTA files for comprehensive protein characterization. 
                        Perform general sequence analysis including length distributions, amino acid compositions, and organism statistics, 
                        while enabling detailed protein examination through molecular property calculations (weight, pI, stability indices), 
                        secondary structure predictions, and flexibility profiling with interactive visualizations.</p>
                    </div>
                    <div style="flex: 1;">
                        <h3 style="margin-top: 0; color: #42d64f; text-align: center;">Proteomic Sequencing Analytics Dashboard</h3>
                        <img class="hover-image" src="data:image/png;base64,{img_base64}" alt="Proteomic Sequencing Analytics Dashboard" 
                            style="width: 90%; height: 250px; border-radius: 15px; object-fit: cover; display: block; margin: 0 auto; border: 1px solid rgba(66, 214, 79, 0.3);">
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Third card: Image+title left, text right
    image_path = "assets/geneomic-ontology.png"
    if Path(image_path).exists():
        img_base64 = img_to_base64(image_path)
        st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; margin-bottom: 40px; border: 1px solid rgba(255, 255, 255, 0.2);">
                <div style="display: flex; gap: 20px;">
                    <div style="flex: 1;">
                        <h3 style="margin-top: 0; color: #42d64f; text-align: center;">Genomic Ontology Navigator</h3>
                        <img class="hover-image" src="data:image/png;base64,{img_base64}" alt="Genomic Ontology Navigator" 
                            style="width: 90%; height: 250px; border-radius: 15px; object-fit: cover; display: block; margin: 0 auto; border: 1px solid rgba(66, 214, 79, 0.3);">
                    </div>
                    <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
                        <p style="color: #ffffff; font-style: italic; text-align: center;">A visualization system for exploring Gene Ontology terms and their interconnections. 
                        Map relationships between biological processes, molecular functions, and cellular components using interactive 
                        network displays. Examine term definitions, synonyms, and references while navigating parent-child relationships 
                        through directed acyclic graphs.</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    # Create sidebar navigation with centered title
    st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
    
    # Add CSS for full-width buttons with hover effect
    st.markdown("""
        <style>
        .stButton button {
            font-size: 20px;
            font-family: 'Consolas' !important;
            width: 100%;
            margin-bottom: 5px;
            transition: all 0.3s ease;
            background-color: #000000;
            border: 0.5px solid #42d64f !important;
            border-radius: 8px;
            padding-top: 15px;
            padding-bottom: 15px;
            margin-bottom: 15px;
        }
        .stButton button:hover {
            transform: scale(1.02);
            background-color: rgba(46, 125, 50, 0.3) !important;  /* Dark green color with 0.8 opacity */
            border: 1px solid #42d64f !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Use session state to maintain the current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Navigation buttons with session state for each component
    if st.sidebar.button("Home"):
        st.session_state.current_page = "Home"
    if st.sidebar.button("Bio-Molecular Conformational Explorer"):
        st.session_state.current_page = "Bio-Molecular Conformational Explorer"
    if st.sidebar.button("Proteomic Sequencing Analytics Dashboard"):
        st.session_state.current_page = "Proteomic Sequencing Analytics Dashboard"
    if st.sidebar.button("Genomic Ontology Navigator"):
        st.session_state.current_page = "Genomic Ontology Navigator"
    
    # Display selected page based on session state
    if st.session_state.current_page == "Home":
        landing()
    elif st.session_state.current_page == "Bio-Molecular Conformational Explorer":
        bio_molecular_explorer_page()
    elif st.session_state.current_page == "Proteomic Sequencing Analytics Dashboard":
        proteomic_dashboard_page()
    elif st.session_state.current_page == "Genomic Ontology Navigator":
        genomic_navigator_page()

if __name__ == "__main__":
    main()
