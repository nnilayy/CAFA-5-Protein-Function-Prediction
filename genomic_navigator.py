import streamlit as st
import obonet
import networkx as nx
from pyvis.network import Network
from io import StringIO
import os
from python_styles.obo_analysis_style import (MAIN_CSS, 
                                              METRIC_CONTAINER_DIV, 
                                              METRIC_CONTAINER_P, 
                                              METRIC_CONTAINER_H3,
                                              INFORMATION_CONTAINER_OUTER_DIV,
                                              INFORMATION_CONTAINER_KEY_DIV,
                                              INFORMATION_CONTAINER_VALUE_DIV)
from python_styles.sidebar_style import SIDEBAR_CSS
from datetime import timedelta

# Emoji mappings
EMOJI_MAP = {
    "total": "",    # Removed emoji
    "def": "",      # Removed emoji
    "ref": "",      # Removed emoji
    "name": "",     # Removed emoji
    "namespace": "", # Removed emoji
    "subset": "",    # Removed emoji
    "synonym": "",   # Removed emoji
    "is_a": "",     # Removed emoji
    "relationship": "" # Removed emoji
}

def parse_definition(definition_text):
    """
    Splits the definition into main text and references.
    Returns a tuple of (definition, references)
    """
    if not definition_text:
        return "", []
    
    # Find the last occurrence of [
    split_index = definition_text.rfind('[')
    if split_index == -1:
        return definition_text, []
        
    # Split the definition and references
    main_def = definition_text[:split_index].strip().strip('"')
    ref_part = definition_text[split_index:].strip('[]')
    
    # Parse references
    references = [ref.strip() for ref in ref_part.split(',')]
    
    return main_def, references

@st.cache_data(ttl=timedelta(hours=24))
def load_obo(file_path):
    """Load an .obo file and return a NetworkX graph."""
    graph = obonet.read_obo(file_path)
    return graph

@st.cache_data(ttl=timedelta(hours=24))
def extract_node_info(_graph, term):
    """Extract metadata for a specific term in the .obo graph."""
    if term in _graph.nodes:
        return _graph.nodes[term]
    else:
        return {}

@st.cache_data(ttl=timedelta(hours=24))
def create_dag_html(_graph, term, radius=1):
    """Create DAG visualization and return HTML content directly without file I/O"""
    # Create DAG
    subgraph = nx.ego_graph(_graph, term, radius=radius)
    for node in subgraph.nodes(data=True):
        node[1]["label"] = f"{node[0]}: {node[1].get('name', 'No Name')}"
        node[1]["color"] = {
            'background': 'rgba(66, 214, 79, 0.35)',
            'border': '#42d64f',
            'highlight': {
                'background': 'rgba(66, 214, 79, 0.5)',
                'border': '#42d64f'
            }
        }
        node[1]["font"] = {
            'color': '#ffffff',
            'size': 14,
            'face': 'arial'
        }
    
    # Create Network
    net = Network(directed=True, height="500px", width="100%", notebook=False, bgcolor='rgba(34, 34, 35, 0.3)')
    net.from_nx(subgraph)
    
    # Generate HTML content directly using the hidden method
    html_content = net.generate_html()
    
    # Add our custom styling
    html_content = html_content.replace("</head>", f"{MAIN_CSS}</head>")
    html_content = html_content.replace("</div>", """
        <script>
        var parentElement = document.querySelector('#mynetwork').parentElement;
        if (parentElement) {
            parentElement.style.backgroundColor = 'transparent';
        }
        </script>
        </div>
    """, 1)
    html_content = html_content.replace(
        '<div class="card" style="width: 100%">',
        '<div class="card" style="width: 100%; background-color: transparent !important;">'
    )
    
    return html_content

def create_metric_container(label, value, unit=""):
    st.markdown(f"""
        <div style="{METRIC_CONTAINER_DIV}">
            <p style="{METRIC_CONTAINER_P}">{label}</p>
            <h3 style="{METRIC_CONTAINER_H3}">{value} {unit}</h3>
        </div>
    """, unsafe_allow_html=True)

# Streamlit UI
def main():
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    
    # Hide the decoration bar
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
    
    # Centered title
    st.markdown("<h1 style='text-align: center;'>🧬 OBO File Data Analysis</h1>", unsafe_allow_html=True)

    with st.expander("Instructions & File Selection"):
        st.markdown("### Instructions")
        st.markdown("""
        1. Upload an .obo file to analyze the ontology structure
        2. The file will be processed to show:
            - Total number of terms and relationships
            - Detailed information for each term
            - Interactive DAG visualization
        3. Use the dropdown to select specific terms and explore their relationships
        """)
        
        # Step 1: File Selection - Moved here, just above the radio buttons
        st.markdown("""
            <div style='background-color: rgba(66, 214, 79, 0.1); 
                       border-left: 3px solid #42d64f; 
                       padding: 10px; 
                       border-radius: 5px;
                       margin-bottom: 15px;'>
                <span style='color: #42d64f; font-weight: bold;'>STEP 1</span>
                <span style='margin-left: 8px;'>Select OBO File Source</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 1.1em;'>Choose OBO file source:</p>", unsafe_allow_html=True)
        file_option = st.radio(
            "",
            ["Use default GO-basic.obo", "Upload custom .obo file"],
            key="file_source",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        uploaded_file = None
        if file_option == "Upload custom .obo file":
            uploaded_file = st.file_uploader("Upload an .obo file", type=["obo"])
        else:
            # Use default file path
            default_path = "data/go-basic.obo"
            if os.path.exists(default_path):
                uploaded_file = default_path
            else:
                st.error("Default GO-basic.obo file not found in data directory!")
        
        # Step 2: Analysis
        st.markdown("""
            <div style='background-color: rgba(66, 214, 79, 0.1); 
                       border-left: 3px solid #42d64f; 
                       padding: 10px; 
                       border-radius: 5px;
                       margin-bottom: 15px;'>
                <span style='color: #42d64f; font-weight: bold;'>STEP 2</span>
                <span style='margin-left: 8px;'>Generate Analysis</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Center the analyze button using columns
        left_col, center_col, right_col = st.columns([1, 1.5, 1])
        with center_col:
            analyze_button = st.button("Analyze OBO File", use_container_width=True)

    # Add horizontal line after expander
    st.markdown("---")

    # Modify this section to separate initial loading from term selection
    if uploaded_file is not None:
        # Initial loading of the file (only if not already loaded)
        if analyze_button or ('graph' in st.session_state and st.session_state.graph is not None):
            if 'graph' not in st.session_state or analyze_button:
                # Center the spinner using columns
                col1, spinner_col, col3 = st.columns([1.3, 0.5, 1])
                with spinner_col:
                    # with st.spinner('Processing OBO file...'):
                    if isinstance(uploaded_file, str):  # Default file path
                        st.session_state.graph = load_obo(uploaded_file)
                    else:  # Uploaded file
                        obo_content = StringIO(uploaded_file.getvalue().decode("utf-8"))
                        st.session_state.graph = load_obo(obo_content)
                    
                    st.session_state.available_terms = list(st.session_state.graph.nodes)
                    st.session_state.formatted_terms = [
                        f"{st.session_state.graph.nodes[term].get('name', 'No Name').title()} [{term}]"
                        for term in st.session_state.available_terms
                    ]
                    st.session_state.total_terms = len(st.session_state.graph)
                    st.session_state.total_relationships = st.session_state.graph.number_of_edges()
                    
                    # Initialize DAG cache
                    st.session_state.dag_cache = {}

            # Use cached graph and terms
            graph = st.session_state.graph
            
            # Display metrics and term selection
            col1, col2 = st.columns(2)
            with col1:
                create_metric_container(f"{EMOJI_MAP['total']} Total Terms", f"{st.session_state.total_terms}")
            with col2:
                create_metric_container(f"{EMOJI_MAP['total']} Total Relationships", f"{st.session_state.total_relationships}")

            # Use cached formatted terms
            col_left, col_middle, col_right = st.columns([1, 2, 1])
            with col_middle:
                # Add vertical space before dropdown
                st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
                
                selected_term_index = st.selectbox(
                    "",
                    options=st.session_state.formatted_terms,
                    index=0,
                    key="term_select",
                    label_visibility="collapsed",
                    help="Select a GO term"
                )
                
                # Add vertical space after dropdown
                st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

            # Get selected term using cached available terms
            selected_term = st.session_state.available_terms[
                st.session_state.formatted_terms.index(selected_term_index)
            ]

            # Two-column layout with adjusted proportions
            col1, spacer, col2 = st.columns([2.5, 0.3, 3])

            # Left Column: Metadata
            with col1:
                st.markdown(
                    "<h3 style='text-align: center;'>Information for Term: {}</h3>".format(selected_term), 
                    unsafe_allow_html=True
                )
                term_info = extract_node_info(graph, selected_term)

                if term_info:
                    key_map = {
                        "def": "Definition",
                        "name": "Name",
                        "namespace": "Namespace",
                        "subset": "Subset",
                        "synonym": "Synonyms",
                        "is_a": "Parent Terms (is_a)",
                        "relationship": "Relationships",
                    }

                    namespace_map = {
                        "biological_process": "BPO (Biological Process)",
                        "molecular_function": "MFO (Molecular Function)",
                        "cellular_component": "CCO (Cellular Component)",
                    }

                    # Process metadata items
                    metadata_items = []

                    # Handle definition separately
                    if "def" in term_info:
                        definition, references = parse_definition(term_info['def'])
                        metadata_items.append(("Definition", definition))
                        if references:
                            metadata_items.append(("References", ", ".join(references)))

                    # Handle other metadata
                    for key, display_name in key_map.items():
                        if key == "namespace" and key in term_info:
                            namespace = term_info[key]
                            formatted_namespace = namespace_map.get(namespace, namespace)
                            metadata_items.append((display_name, formatted_namespace))
                        elif key == "name" and key in term_info:
                            formatted_name = term_info[key].title()
                            metadata_items.append((display_name, formatted_name))
                        elif key != "def" and key in term_info:
                            value = term_info[key]
                            formatted_value = (
                                f'<code style="color: #9370DB; background-color: rgba(147, 112, 219, 0.2);">{value}</code>'
                                if isinstance(value, (list, set)) else value
                            )
                            metadata_items.append((display_name, formatted_value))

                    # Display all items in a single column
                    for key, value in metadata_items:
                        st.markdown(
                            f"""
                            <div style="{INFORMATION_CONTAINER_OUTER_DIV}">
                                <div style="{INFORMATION_CONTAINER_KEY_DIV}">{key}</div>
                                <div style="{INFORMATION_CONTAINER_VALUE_DIV}">{value}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:
                    st.markdown("No metadata available for this term.")

            # Right Column: DAG Visualization
            with col2:
                term_name = st.session_state.graph.nodes[selected_term].get("name", "No Name").title()
                st.markdown(
                    f"<h3 style='text-align: center;'>Directed Acyclic Graph: {term_name}</h3>",
                    unsafe_allow_html=True,
                )

                # Check if DAG is in cache
                if selected_term not in st.session_state.dag_cache:
                    # Generate new DAG HTML if not in cache
                    html_content = create_dag_html(st.session_state.graph, selected_term, radius=10000)
                    # Cache the result (optional: limit cache size)
                    if len(st.session_state.dag_cache) > 10:  # Keep last 10 DAGs
                        oldest_term = next(iter(st.session_state.dag_cache))
                        del st.session_state.dag_cache[oldest_term]
                    st.session_state.dag_cache[selected_term] = html_content
                else:
                    # Use cached DAG HTML
                    html_content = st.session_state.dag_cache[selected_term]

                # Display the visualization
                st.components.v1.html(html_content, height=700, scrolling=False)

    # Clear session state only when explicitly requested
    elif analyze_button:
        for key in ['graph', 'available_terms', 'formatted_terms', 'total_terms', 
                   'total_relationships', 'dag_cache']:
            if key in st.session_state:
                del st.session_state[key]

if __name__ == "__main__":
    main()
