MAIN_CSS = """
        <style>
        #mynetwork {
            width: 100%;
            height: 600px;
            background-color: #000000 !important;
            border: 1px solid #42d64f;
            position: relative;
            margin-top: -5px;
            margin-bottom: 20px;
            border-radius: 15px;
            padding-bottom: 2px;
        }
        .card {
            background-color: transparent !important;
            border-radius: 15px;
            border: none !important;
            margin-bottom: 10px;
        }
        .vis-network {
            background-color: #000000 !important;
            padding-bottom: 2px;
        }
        body {
            background-color: transparent !important;
        }
        .card-body {
            background-color: transparent !important;
            padding-bottom: 2px;
        }
        </style>
        """

METRIC_CONTAINER_DIV = """
display: flex; 
flex-direction: column; 
align-items: center; 
justify-content: center; 
background-color: #222223;
border-radius: 8px; 
padding: 1rem; 
margin: 0.5rem; 
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
"""

METRIC_CONTAINER_P ="""
color: white; 
font-weight: bold; 
margin-bottom: 0.5rem; 
font-size: 1rem;
"""

METRIC_CONTAINER_H3 ="""
color: #42d64f; 
margin: 0; 
font-size: 2rem;
"""

INFORMATION_CONTAINER_OUTER_DIV = """
background-color: rgba(34, 34, 35, 0.3); 
padding: 10px; 
margin: 5px; 
border-radius: 5px;
"""

INFORMATION_CONTAINER_KEY_DIV = """
color: #42d64f; 
font-weight: bold; 
text-align: center; 
font-style: italic;
"""

INFORMATION_CONTAINER_VALUE_DIV = """
color: white; 
text-align: center; 
margin-top: 5px;
"""
