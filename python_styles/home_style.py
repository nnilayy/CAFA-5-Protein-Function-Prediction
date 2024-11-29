MAIN_CSS ="""
    <style>
    /* Main page title styling */
    .main-title {
        text-align: center;
        padding: 1rem;
        color: #42d64f;
    }
    
    /* Card container styling */
    .card-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        padding: 20px;
    }
    
    /* Individual card styling */
    .card {
        background-color: #222223;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #42d64f;
        flex: 1;
        text-align: center;
    }
    
    /* Card image styling */
    .card img {
        max-width: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    /* Navigation link styling */
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