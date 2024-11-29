MAIN_CSS = """
    <style>
    /* Styling for the visualization container */
    .stmol-container iframe {
        border-radius: 25px !important;
        border: 2px solid #42d64f !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        background-color: black !important;
        margin-left: -10px;
    }
    
    /* Center the iframe */
    .stmol-container {
        background-color: black !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Additional styling for the container div */
    div[data-testid="stBlock"] {
        background-color: black !important;
    }

    /* Style the 3Dmol viewer */
    .viewer_3Dmoljs {
        background-color: black !important;
    }

    /* Force iframe styling */
    iframe[style*="stmol"] {
        border-radius: 25px !important;
        border: 2px solid #42d64f !important;
    }
    </style>
"""

COL_5_CSS="""
    <style>
    div[data-testid="column"]:nth-child(5) {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    div[data-testid="column"]:nth-child(5) .stButton {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100%;
    }

    div[data-testid="column"]:nth-child(5) .stButton > button {
        width: 100%;
        margin-top: 1.5rem;
    }
    </style>
"""

TAB_OUTER_DIV = """
background-color: rgba(34, 34, 35, 0.3); 
padding: 10px; 
margin: 5px; 
border-radius: 5px;
"""

TAB_KEY_DIV = """
color: #42d64f; 
font-weight: bold; 
text-align: center; 
font-style: italic;
"""

TAB_VALUE_DIV = """
color: white; 
text-align: center; 
margin-top: 5px;
"""

TAB_VALUE_DIV_MONOSPACE = """
color: white; 
text-align: center; 
margin-top: 5px;
font-family: monospace;
"""

TAB_VALUE_DIV_OVERFLOW_WRAP = """
color: white; 
text-align: center; 
margin-top: 5px;
overflow-wrap: break-word;
"""
