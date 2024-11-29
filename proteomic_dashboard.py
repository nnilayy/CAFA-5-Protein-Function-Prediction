import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import io
import numpy as np
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from python_styles.fasta_stats_style import (
    MAIN_CSS,
    METRIC_CONTAINER_OUTER_DIV,
    METRIC_CONTAINER_P,
    METRIC_CONTAINER_H3
)
from python_styles.sidebar_style import SIDEBAR_CSS
import os
from datetime import timedelta

@st.cache_data(ttl=timedelta(hours=24))
def create_plotly_template():
    """Create a dark theme template for plotly with both vertical and horizontal gridlines"""
    return dict(
        layout=dict(
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            font=dict(color='white')
        )
    )

@st.cache_data(ttl=timedelta(hours=24))
def create_metric_container(label, value, unit=""):
    st.markdown(f"""
        <div style="{METRIC_CONTAINER_OUTER_DIV}">
            <p style="{METRIC_CONTAINER_P}">{label}</p>
            <h3 style="{METRIC_CONTAINER_H3}">{value} {unit}</h3>
        </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=timedelta(hours=24))
def parse_fasta_records(file_content):
    """Parse FASTA records with caching"""
    return list(SeqIO.parse(io.StringIO(file_content), "fasta"))

@st.cache_data(ttl=timedelta(hours=24))
def analyze_fasta_file(_records):
    """Analyze general statistics of the FASTA file and preprocess data"""
    # Create initial DataFrame
    data = []
    for record in _records:
        data.append({
            "ID": record.id,
            "Description": record.description,
            "Length": len(record.seq),
            "Sequence": str(record.seq)
        })
    
    df = pd.DataFrame(data)
    
    # Extract metadata fields from Description
    df["Protein Name"] = df["Description"].str.extract(r"\|[A-Z0-9_]+\|([^OS]+)")
    df["OS"] = df["Description"].str.extract(r"OS=([^OXGNPE]+)")
    df["OX"] = df["Description"].str.extract(r"OX=(\d+)")
    df["GN"] = df["Description"].str.extract(r"GN=([^ ]+)")
    df["PE"] = df["Description"].str.extract(r"PE=(\d+)")
    df["SV"] = df["Description"].str.extract(r"SV=(\d+)")
    
    # Drop Description column
    df.drop(columns=["Description"], inplace=True)
    
    # Calculate length statistics
    lengths = df['Length'].values
    
    return {
        'total_sequences': len(_records),
        'avg_length': np.mean(lengths),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'std_length': np.std(lengths),
        'median_length': np.median(lengths),
        'percentile_25': np.percentile(lengths, 25),
        'percentile_75': np.percentile(lengths, 75),
        'lengths': lengths,
        'dataframe': df
    }

@st.cache_data(ttl=timedelta(hours=24))
def analyze_protein_sequence(sequence):
    """Analyze a specific protein sequence"""
    protein = ProteinAnalysis(str(sequence))
    return {
        'molecular_weight': protein.molecular_weight(),
        'theoretical_pi': protein.isoelectric_point(),
        'instability_index': protein.instability_index(),
        'gravy': protein.gravy(),
        'aromaticity': protein.aromaticity(),
        'secondary_structure': protein.secondary_structure_fraction(),
        'aa_composition': protein.get_amino_acids_percent(),
        'aa_count': protein.count_amino_acids(),
        'flexibility': protein.flexibility(),
        'extinction_coefficients': protein.molar_extinction_coefficient(),
        'charge_at_ph7': protein.charge_at_pH(7.0)
    }

@st.cache_data(ttl=timedelta(hours=24))
def generate_length_distribution_plot(lengths):
    """Generate sequence length distribution histogram"""
    fig = px.histogram(
        x=lengths,
        nbins=50,
        color_discrete_sequence=['#42d64f'],
        title="Sequence Length Distribution"
    )
    fig.update_traces(
        marker=dict(
            color='rgba(66, 214, 79, 0.35)',
            line=dict(color='#42d64f', width=2)
        )
    )
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title="Sequence Length",
        yaxis_title="Count",
        showlegend=False,
        height=700,
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_amino_acid_composition_plot(_records):
    """Generate overall amino acid composition plot"""
    all_sequences = "".join(str(record.seq) for record in _records)
    aa_counts = Counter(all_sequences)
    aa_df = pd.DataFrame(list(aa_counts.items()), 
                        columns=["Amino Acid", "Count"])
    aa_df = aa_df.sort_values("Amino Acid", ascending=True)
    
    fig = px.bar(
        aa_df,
        x='Amino Acid',
        y='Count',
        color_discrete_sequence=['#42d64f'],
        title="Amino Acid Composition"
    )
    fig.update_traces(
        marker=dict(
            color='rgba(66, 214, 79, 0.35)',
            line=dict(color='#42d64f', width=2)
        )
    )
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title="Amino Acid",
        yaxis_title="Count",
        height=700,
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_version_distribution_plot(df, column, title, x_label):
    """Generate distribution plot for SV or PE levels"""
    counts = df[column].value_counts().sort_index()
    plot_df = pd.DataFrame({f'{column} Level': counts.index, 'Count': counts.values})
    
    fig = px.bar(
        plot_df,
        x=f'{column} Level',
        y='Count',
        color_discrete_sequence=['#42d64f'],
        title=title
    )
    fig.update_traces(
        marker=dict(
            color='rgba(66, 214, 79, 0.35)',
            line=dict(color='#42d64f', width=2)
        ),
        texttemplate='%{y}', 
        textposition='outside', 
        textfont=dict(color='white')
    )
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title=x_label,
        yaxis_title="Count",
        height=700,
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_organism_distribution_plot(df):
    """Generate top 30 organisms distribution plot"""
    os_counts = df['OS'].value_counts().head(30)
    os_df = os_counts.reset_index()
    os_df.columns = ['Organism', 'Count']
    
    fig = px.bar(
        os_df,
        x='Organism',
        y='Count',
        color_discrete_sequence=['#42d64f'],
        title="Top 30 Organisms Distribution"
    )
    fig.update_traces(
        marker=dict(
            color='rgba(66, 214, 79, 0.35)',
            line=dict(color='#42d64f', width=2)
        )
    )
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title="Organism",
        yaxis_title="Count",
        xaxis_tickangle=45,
        height=1000,
        width=2000,
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_secondary_structure_plot(analysis):
    """Generate secondary structure prediction pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=['Helix', 'Turn', 'Sheet'],
        values=list(analysis['secondary_structure']),
        textinfo='label+percent',
        marker=dict(
            colors=['rgba(42, 139, 51, 0.35)', 'rgba(66, 214, 79, 0.35)', 'rgba(125, 232, 133, 0.35)'],
            line=dict(
                color=['#2a8b33', '#42d64f', '#7de885'],
                width=2
            )
        ),
        hole=0,
        textposition='inside',
        textfont=dict(color='white'),
    )])
    fig.update_traces(
        domain=dict(x=[0, 1], y=[0, 1])
    )
    fig.update_layout(
        template=create_plotly_template(),
        height=600,
        title="Secondary Structure Prediction",
        title_x=0.325
    )
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_flexibility_plot(analysis):
    """Generate flexibility profile plot"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=analysis['flexibility'],
        fill='tozeroy',
        fillcolor='rgba(66, 214, 79, 0.35)',
        line=dict(color='#42d64f', width=2)
    ))
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title="Position",
        yaxis_title="Flexibility Score",
        height=600,
        title="Flexibility Profile",
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def generate_specific_aa_composition_plot(analysis):
    """Generate amino acid composition plot for specific protein"""
    aa_comp = pd.DataFrame(analysis['aa_composition'].items(),
                          columns=['Amino Acid', 'Percentage'])
    aa_comp = aa_comp.sort_values('Amino Acid', ascending=True)
    
    fig = px.bar(
        aa_comp,
        x='Amino Acid',
        y='Percentage',
        color_discrete_sequence=['#42d64f'],
        title="Amino Acid Composition"
    )
    fig.update_traces(
        marker=dict(
            color='rgba(66, 214, 79, 0.35)',
            line=dict(color='#42d64f', width=2)
        )
    )
    fig.update_layout(
        template=create_plotly_template(),
        xaxis_title="Amino Acid",
        yaxis_title="Percentage (%)",
        height=1000,
        title_x=0.45
    )
    _add_grid_styling(fig)
    return fig

@st.cache_data(ttl=timedelta(hours=24))
def _add_grid_styling(fig):
    """Add common grid styling to plots"""
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        gridcolor='rgba(255, 255, 255, 0.3)',
        showgrid=True
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        gridcolor='rgba(255, 255, 255, 0.3)',
        showgrid=True
    )

@st.cache_data(ttl=timedelta(hours=24))
def generate_general_tab_plots(_stats, _df, _records):
    """Generate all plots for the general statistics tab"""
    plots = {
        'length_dist': generate_length_distribution_plot(_stats['lengths']),
        'sv_dist': generate_version_distribution_plot(_df, 'SV', "Sequence Version (SV) Distribution", "SV Level"),
        'aa_comp': generate_amino_acid_composition_plot(_records),
        'pe_dist': generate_version_distribution_plot(_df, 'PE', "Protein Evidence (PE) Level Distribution", "PE Level"),
        'organism_dist': generate_organism_distribution_plot(_df)
    }
    return plots

@st.cache_data(ttl=timedelta(hours=24))
def generate_specific_protein_plots(analysis):
    """Generate all plots for specific protein analysis"""
    plots = {
        'secondary_structure': generate_secondary_structure_plot(analysis),
        'flexibility': generate_flexibility_plot(analysis),
        'aa_composition': generate_specific_aa_composition_plot(analysis)
    }
    return plots

@st.cache_data(ttl=timedelta(hours=24))
def render_general_tab_content(stats, plots):
    """Render all content for the general statistics tab"""
    st.header("File Overview")
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_metric_container("Total Sequences", f"{stats['total_sequences']}")
        create_metric_container("Mean Length", f"{stats['avg_length']:.2f}")
    with col2:
        create_metric_container("Minimum Length", f"{stats['min_length']}")
        create_metric_container("Maximum Length", f"{stats['max_length']}")
    with col3:
        create_metric_container("Std Deviation", f"{stats['std_length']:.2f}")
        create_metric_container("Median Length", f"{stats['median_length']:.0f}")
    with col4:
        create_metric_container("25th Percentile", f"{stats['percentile_25']:.0f}")
        create_metric_container("75th Percentile", f"{stats['percentile_75']:.0f}")
    
    # Display plots in columns
    plot_col1, plot_col2 = st.columns(2)
    
    with plot_col1:
        st.plotly_chart(plots['length_dist'], use_container_width=True)
        st.plotly_chart(plots['sv_dist'], use_container_width=True)
    
    with plot_col2:
        st.plotly_chart(plots['aa_comp'], use_container_width=True)
        st.plotly_chart(plots['pe_dist'], use_container_width=True)
    
    # Display organism distribution plot (full width)
    st.plotly_chart(plots['organism_dist'], use_container_width=True)

@st.cache_data(ttl=timedelta(hours=24))
def render_specific_tab_content(df, selected_seq_id, analysis, plots):
    """Render all content for the specific protein analysis tab"""
    selected_row = df[df['ID'] == selected_seq_id].iloc[0]
    
    # Metadata section
    st.markdown("<h2 style='text-align: center;'> Metadata</h2>", unsafe_allow_html=True)
    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        create_metric_container("Protein Name", selected_row['Protein Name'])
        create_metric_container("Organism", selected_row['OS'])
        create_metric_container("Gene Name", selected_row['GN'])
    with meta_col2:
        create_metric_container("Taxonomic ID", selected_row['OX'])
        create_metric_container("Protein Evidence", selected_row['PE'])
        create_metric_container("Sequence Version", selected_row['SV'])
    
    # Basic Properties section
    st.markdown("<h2 style='text-align: center;'>📊 Basic Properties</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        create_metric_container("Molecular Weight", f"{analysis['molecular_weight']:.2f}", "Da")
        create_metric_container("Theoretical pI", f"{analysis['theoretical_pi']:.2f}")
    with col2:
        create_metric_container("Instability Index", f"{analysis['instability_index']:.2f}")
        create_metric_container("Aromaticity", f"{analysis['aromaticity']:.3f}")
    with col3:
        create_metric_container("GRAVY", f"{analysis['gravy']:.2f}")
        create_metric_container("Charge at pH 7", f"{analysis['charge_at_ph7']:.2f}")
    
    # Structure Analysis section
    st.markdown("<h2 style='text-align: center;'>🔬 Structure Analysis</h2>", unsafe_allow_html=True)
    struct_col1, struct_col2 = st.columns(2)
    
    with struct_col1:
        st.plotly_chart(plots['secondary_structure'], use_container_width=True)
    
    with struct_col2:
        st.plotly_chart(plots['flexibility'], use_container_width=True)
    
    # Composition section
    st.plotly_chart(plots['aa_composition'], use_container_width=True)

@st.cache_data(ttl=timedelta(hours=24))
def process_and_generate_plots(file_content):
    """Cache the entire process of parsing, analyzing, and generating plots"""
    records = parse_fasta_records(file_content)
    stats = analyze_fasta_file(records)
    df = stats['dataframe']
    general_plots = generate_general_tab_plots(stats, df, records)
    return records, stats, df, general_plots

@st.cache_data(ttl=timedelta(hours=24))
def get_selected_protein_data(df, selected_seq_id):
    """Cache the selected protein row lookup"""
    return df[df['ID'] == selected_seq_id].iloc[0]

@st.cache_data(ttl=timedelta(hours=24))
def get_protein_analysis(sequence, protein_id):
    """Cache analysis for individual proteins"""
    return analyze_protein_sequence(sequence)

def main():
    # st.set_page_config(page_title="Protein Sequence Analysis", layout="wide")
    
    # Add the sidebar CSS right after page config
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
    
    # Hide the decoration bar
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>🧬 Proteomic Sequencing Analytics Dashboard 🧬</h1>", unsafe_allow_html=True)
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
    
    # Initialize session state variables
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'file_content' not in st.session_state:
        st.session_state.file_content = None
    
    # Add an expander for instructions and file upload
    with st.expander("About Proteomic Sequencing Analytics Dashboard", expanded=True):
        st.markdown("""
        ### 🧬 A Protein Sequence Analysis Dashboard
        - Analyze .fasta files containing protein sequences
        - Generate comprehensive sequence statistics
        - Visualize protein properties and distributions
        - Examine individual protein characteristics
        - Support for both default and custom .fasta files
        """)
        
        # Step 1: File Selection
        st.markdown("""
            <div style='background-color: rgba(66, 214, 79, 0.1); 
                       border-left: 3px solid #42d64f; 
                       padding: 10px; 
                       border-radius: 5px;
                       margin-bottom: 15px;'>
                <span style='color: #42d64f; font-weight: bold;'>STEP 1</span>
                <span style='margin-left: 8px;'>Select .fasta File Source</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 1.1em;'>Choose .fasta file source:</p>", unsafe_allow_html=True)
        file_option = st.radio(
            "",
            ["Use the provided .fasta file", "Upload your own .fasta file"],
            key="file_source",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        uploaded_file = None
        if file_option == "Upload your own .fasta file":
            uploaded_file = st.file_uploader("Upload your .fasta file", type=['fasta'])
            if uploaded_file:
                file_content = uploaded_file.read().decode("utf-8")
                st.session_state.file_content = file_content
        else:
            # Use default file path
            default_path = "data/train_sequences.fasta"
            if os.path.exists(default_path):
                with open(default_path, 'r') as f:
                    file_content = f.read()
                    st.session_state.file_content = file_content
        
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
            analyze_button = st.button("Analyze FASTA File", use_container_width=True)
    
    # Add horizontal line
    st.markdown("---")
    
    if analyze_button:
        if st.session_state.file_content:
            try:
                # Center the spinner only during the initial processing
                col1, spinner_col, col3 = st.columns([1.1, 0.8, 1])
                with spinner_col:
                    records, stats, df, general_plots = process_and_generate_plots(st.session_state.file_content)
                
                st.session_state.fasta_records = records
                st.session_state.fasta_stats = stats
                st.session_state.fasta_df = df
                st.session_state.general_plots = general_plots
                st.session_state.analysis_done = True  # Set the analysis flag to True
    
            except Exception as e:
                st.error(f"Error processing FASTA file: {str(e)}")
                st.session_state.analysis_done = False
        else:
            st.error("No FASTA file content found.")
            st.session_state.analysis_done = False
    
    # Check if analysis is done and display the results
    if st.session_state.analysis_done:
        # Create a container to hold all content
        results_container = st.empty()
        
        # Build the entire UI content with switched tab order
        with results_container.container():
            tab_specific, tab_general = st.tabs(["🔬 Specific Protein Analysis", "📊 General File Statistics"])
            
            with tab_specific:
                df = st.session_state.fasta_df
                selected_seq_id = st.selectbox("Select sequence to analyze:", df['ID'].tolist())
                selected_row = get_selected_protein_data(df, selected_seq_id)
                # Use cached analysis for the selected protein
                analysis = get_protein_analysis(selected_row['Sequence'], selected_seq_id)
                specific_plots = generate_specific_protein_plots(analysis)
                render_specific_tab_content(df, selected_seq_id, analysis, specific_plots)

            with tab_general:
                stats = st.session_state.fasta_stats
                general_plots = st.session_state.general_plots
                render_general_tab_content(stats, general_plots)


if __name__ == "__main__":
    main()