import streamlit as st

# This must be the first Streamlit command
st.set_page_config(
    page_title="BioAnalysis Suite",
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
from molecular_viewer import main as molecular_viewer_page
from proteomic_dashboard import main as proteomic_dashboard_page
from genomic_navigator import main as genomic_navigator_page

# Apply CSS
from python_styles.home_style import MAIN_CSS
st.markdown(MAIN_CSS, unsafe_allow_html=True)
from python_styles.sidebar_style import SIDEBAR_CSS

def landing():
    st.markdown('<h1 class="main-title">🧬 BioAnalysis Suite</h1>', unsafe_allow_html=True)
    
    st.markdown("""
        ## Welcome to the BioAnalysis Suite
        
        A comprehensive toolkit for molecular conformation visualization, proteomic data analysis, 
        and genomic ontology navigation. This suite combines three powerful tools to help you 
        analyze and understand biological data more effectively.
    """)
    
    # Feature cards with updated descriptions and names
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="card">
                <img src="path_to_structure_viewer_image.png" alt="Molecular Conformational Viewer">
                <h3>Molecular Conformational Viewer</h3>
                <p>Interactive 3D visualization of molecular structures with customizable 
                display options and detailed structural information.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <img src="path_to_stats_image.png" alt="Proteomic Sequencing Analytics Dashboard">
                <h3>Proteomic Sequencing Analytics Dashboard</h3>
                <p>Comprehensive analysis of proteomic sequences, including 
                composition, physical properties, and sequence patterns.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card">
                <img src="path_to_obo_image.png" alt="Genomic Ontology Navigator">
                <h3>Genomic Ontology Navigator</h3>
                <p>Explore and analyze genomic ontologies with interactive visualizations, 
                understanding term relationships, and detailed ontology information.</p>
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
    if st.sidebar.button("Molecular Conformational Viewer"):
        st.session_state.current_page = "Molecular Conformational Viewer"
    if st.sidebar.button("Proteomic Sequencing Analytics Dashboard"):
        st.session_state.current_page = "Proteomic Sequencing Analytics Dashboard"
    if st.sidebar.button("Genomic Ontology Navigator"):
        st.session_state.current_page = "Genomic Ontology Navigator"
    
    # Display selected page based on session state
    if st.session_state.current_page == "Home":
        landing()
    elif st.session_state.current_page == "Molecular Conformational Viewer":
        molecular_viewer_page()
    elif st.session_state.current_page == "Proteomic Sequencing Analytics Dashboard":
        proteomic_dashboard_page()
    elif st.session_state.current_page == "Genomic Ontology Navigator":
        genomic_navigator_page()

if __name__ == "__main__":
    main()
