SIDEBAR_CSS = """
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0a0a0b;
    }

    /* Target the main sidebar container */
    section[data-testid="stSidebar"] > div {
        background-color: #0a0a0b;
        border-top-right-radius: 30px;
        border-bottom-right-radius: 30px;
    }

    /* Target the sidebar content */
    section[data-testid="stSidebar"] > div > div:first-child {
        padding: 0.3rem 0.3rem;
        background-color: #0a0a0b;
        border-top-right-radius: 30px;
        border-bottom-right-radius: 30px;
    }

    /* Target the sidebar expandable container */
    section[data-testid="stSidebar"] .element-container {
        background-color: #0a0a0b;
    }

    /* Navigation link styling */
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        text-decoration: none !important;
    }

    .nav-link {
        color: #ffffff;
        text-decoration: none;
        padding: 8px 12px;
        margin: 2px 0;
        border-radius: 5px;
        display: block;
        transition: all 0.3s ease;
        border: 1px solid rgba(66, 214, 79, 0.2);
        background-color: rgba(66, 214, 79, 0.02);
        text-align: center;
    }

    .nav-link:hover {
        background-color: rgba(66, 214, 79, 0.1);
        border: 1px solid #42d64f;
        transform: translateX(5px);
        text-decoration: none !important;
        color: #42d64f !important;
    }
    </style>
"""
