<div align="center">

<h1 align="center">🧬 BioCore 🧬</h1>

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Forks](https://img.shields.io/github/forks/nnilayy/BioCore?style=social)](https://github.com/nnilayy/BioCore/network/members)
[![GitHub Stars](https://img.shields.io/github/stars/nnilayy/BioCore?style=social)](https://github.com/nnilayy/BioCore/stargazers)

A comprehensive bioinformatics platform for molecular biology research and analysis, integrating tools for protein structure visualization, sequence analysis, and gene ontology exploration.

<!-- <video src="https://github.com/user-attachments/assets/2d763a69-e015-4337-bdb6-6b91a0131426" controls="controls" style="max-width: 100%;">
</video> -->

</div>

## 🌟 Try it Now

Explore BioCore directly through these live site deployments:

- **Streamlit Cloud**: [biocore-suite-nnilayy.streamlit.app](https://biocore-suite-nnilayy.streamlit.app)
- **Hugging Face Spaces**: [huggingface.co/spaces/nnilayy/BioCore](https://huggingface.co/spaces/nnilayy/BioCore)

## 🌟 Overview

BioCore is a modern, integrated platform that combines three powerful modules for bioinformatics research:

### 1. 🔬 Bio-Molecular Conformational Explorer

Core Features:

I. **PDB Integration & Structure Fetching**
   - Retrieve protein structures in real-time from the Protein Data Bank directly using their unique PDB IDs

II. **Interactive 3D Visualization & Styling**
   - Dynamic 3D visualization of bio-molecular structures with adjustable viewing styles and interactive controls for detailed exploration of the proteins

III. **Detailed Protein Structural Information**
   - Displays comprehensive structural metadata (classification, deposition date, title, R-values) including experimental methods (X-ray diffraction, NMR) and resolution metrics (resolution, R-free, R-work)
   - Provides detailed molecular information about protein chains and their source organisms
   - Includes bibliographic references with complete citation details for research attribution

IV. **Export Features**
   - Facilitates direct PDB file download for offline access and further analysis

### 2. 🧬 Proteomic Sequencing Analytics Dashboard

Core Features:

I. **Analysis of Proteins from FASTA Files**
   - Process protein sequences to generate general file-level statistics and specific protein analysis using interactive Plotly visualizations

II. **General File-Level Analysis**
   - Statistical exploration of sequence properties including length metrics and distributions, coupled with metadata insights on organism diversity and protein evidence levels, alongside global amino acid composition patterns

III. **Specific Protein Analysis**
   - Deep dive into individual proteins through biochemical characterization (molecular weight, pI, stability metrics), structural element predictions, and detailed amino acid compositional breakdown

### 3. 🔍 Genomic Ontology Navigator

Core Features:

I. **Interactive Hierarchical DAGs for Genomic Ontologies**
   - Process OBO files to create interactive networks of related Gene Ontology terms, exploring their hierarchical relationships across biological processes, molecular functions, and cellular components

II. **GO Term Metadata Analysis**
   - Extract and analyze metadata of GO terms (IDs, names, definitions, relationship types) from OBO files

## 🚀 Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/nnilayy/biocore.git
cd biocore
```

2. **Set up environment using `uv`:**
```bash
uv venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
uv pip install -r requirements.txt
```

4. **Launch the application:**
```bash
streamlit run home.py
```

## 🛠️ Core Dependencies

- `streamlit`: Web application framework
- `py3Dmol`: Molecular visualization
- `biopython`: Biological computation
- `pandas`: Data manipulation
- `plotly`: Interactive plotting
- `networkx`: Network analysis
- `obonet`: Ontology parsing
- `seaborn`: Statistical visualization

## 📚 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository ([Click here to fork BioCore](https://github.com/nnilayy/BioCore/fork))

2. Clone your fork:
```python
git clone https://github.com/nnilayy/biocore.git
cd biocore
```

3. Create your feature branch:
```python
git checkout -b feature/AmazingFeature
```

4. Make your changes and commit them:
```python
git add .
git commit -m 'Add AmazingFeature'
```

5. Push to your branch:
```python
git push origin feature/AmazingFeature
```

Then open a Pull Request from your fork to our main repository.

## 🐛 Issues
If you've found a bug or have a suggestion, feel free to open an issue.

To create a new issue:

- Go to the [Issues tab](https://github.com/nnilayy/BioCore/issues)
- Click the New Issue button
- Choose the appropriate template if available
- Fill in the required information
- Submit the issue

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- PDB Database for structural data
- Gene Ontology Consortium
- BioPython community
- Streamlit team

## 📬 Contact

Have questions or suggestions? Feel free to reach out!
- **Author**: Nilay Kumar Bhatnagar
- **Email**: nnilayy.work@gmail.com

---

<div align="center">
Made with ❤️ for the Bioinformatics Research Community
</div>
