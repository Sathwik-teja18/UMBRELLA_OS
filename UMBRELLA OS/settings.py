import os

# ==========================================
# PATH CONFIGURATION
# ==========================================
# This automatically finds the folder where settings.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dynamic path to the assets folder
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# The Database file will still safely save to your Windows Documents folder
DB_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_DB.json')
BIOMETRICS_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_BIOMETRICS')
QUARANTINE_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_QUARANTINE')

# ==========================================
# ASSET DICTIONARY
# ==========================================
# We store all file paths here so you can easily call them in your UI files
ASSETS = {
    "logo": os.path.join(ASSETS_DIR, "Umbrella_Corporation_logo.svg.png"),
    "desktop_bg": os.path.join(ASSETS_DIR, "umbrella_desktop_bg.jpg"),
    "splash_image": os.path.join(ASSETS_DIR, "5e8500219061405.Y3JvcCwxMzgwLDEwODAsMjcwLDA.jpg"),
    "cam1": os.path.join(ASSETS_DIR, "Camera_01.gif"),
    "cam2": os.path.join(ASSETS_DIR, "Camera_02.gif"),
    "cam3": os.path.join(ASSETS_DIR, "Camera_03.gif"),
    "cam4": os.path.join(ASSETS_DIR, "Camera_04.gif"),
    "sfx_clunk": os.path.join(ASSETS_DIR, "Dull Booming Metal Thud.wav"),
    "sfx_toxin": os.path.join(ASSETS_DIR, "Steam - Sound Effect (HD).wav")
}

# ==========================================
# GLOBAL STYLESHEET (V3 Blackout Theme)
# ==========================================
# ==========================================
# GLOBAL STYLESHEET (Blackout NEST Theme)
# ==========================================
CORPORATE_THEME = """
    /* GLOBAL BACKGROUND */
    QMainWindow, QWidget { background-color: #050505; color: #E0E0E0; }

    /* TEXT & LABELS */
    QLabel { color: #FFFFFF; font-family: 'Arial', sans-serif; background: transparent; }

    /* INPUT FIELDS */
    QLineEdit, QTextEdit { background-color: #0A0A0A; color: #FFFFFF; border: 1px solid #222222; border-radius: 2px; font-family: 'Courier New', monospace; font-size: 15px; padding: 8px; }
    QLineEdit:focus, QTextEdit:focus { border: 1px solid #C41E3A; background-color: #0D0D0D; }

    /* MODERN BUTTONS */
    QPushButton { background-color: #111111; color: #FFFFFF; border: 1px solid #333333; border-radius: 3px; font-family: 'Arial', sans-serif; font-size: 14px; font-weight: bold; padding: 10px; letter-spacing: 1px; }
    QPushButton:hover { background-color: #1A1A1A; border: 1px solid #C41E3A; color: #C41E3A; }
    QPushButton:pressed { background-color: #C41E3A; color: #000000; }

    /* FILE EXPLORER & LISTS */
    QTreeView, QListView { background-color: #0A0A0A; color: #A0B0B5; border: 1px solid #1A1A1A; font-family: 'Courier New'; font-size: 14px; }
    QTreeView::item:selected, QListView::item:selected { background-color: #111111; color: #C41E3A; border: 1px solid #222222; }
    QTreeView::item:hover, QListView::item:hover { background-color: #0D0D0D; }
    QHeaderView::section { background-color: #050505; color: #A0B0B5; border: none; border-bottom: 1px solid #222222; padding: 8px; font-weight: bold; }

    /* DESKTOP SIDEBAR */
    QListWidget#DesktopSidebar { background-color: rgba(5, 5, 5, 0.95); border-right: 1px solid #1A1A1A; }
    QListWidget#DesktopSidebar::item { padding: 15px; color: #708085; border-bottom: 1px solid #0D0D0D; font-family: 'Arial', sans-serif; font-weight: bold; letter-spacing: 1px; }
    QListWidget#DesktopSidebar::item:selected { background-color: #0A0A0A; color: #FFFFFF; border-left: 3px solid #C41E3A; }
    QListWidget#DesktopSidebar::item:hover { color: #FFFFFF; background-color: #0D0D0D; }

    /* MDI SUB-WINDOWS (Flat Glass Style) */
    QMdiSubWindow { background-color: #0A0A0A; border: 1px solid #222222; border-radius: 4px; }
    QMdiSubWindow::title { background-color: #050505; color: #A0B0B5; font-family: 'Arial', sans-serif; font-weight: bold; font-size: 12px; padding: 8px; border-bottom: 1px solid #1A1A1A; }

    /* MODERN CIRCULAR WINDOW CONTROLS */
    QMdiSubWindow::minimize-button, QMdiSubWindow::maximize-button, QMdiSubWindow::close-button { background-color: transparent; border: none; width: 12px; height: 12px; margin: 4px; border-radius: 6px; }
    QMdiSubWindow::minimize-button { background-color: #333333; }
    QMdiSubWindow::maximize-button { background-color: #555555; }
    QMdiSubWindow::close-button { background-color: #8A0303; }
    QMdiSubWindow::minimize-button:hover { background-color: #A0B0B5; }
    QMdiSubWindow::maximize-button:hover { background-color: #FFFFFF; }
    QMdiSubWindow::close-button:hover { background-color: #FF0000; }
    
    /* DIAGNOSTICS TABS */
    QTabWidget::pane { border: 1px solid #222222; background: #0A0A0A; } 
    QTabBar::tab { background: #050505; color: #708085; padding: 10px 20px; border: 1px solid #1A1A1A; border-bottom: none; font-family: 'Arial'; font-weight: bold; } 
    QTabBar::tab:selected { background: #0A0A0A; color: #FFFFFF; border-top: 2px solid #C41E3A; }
"""
# ==========================================
# LORE DATABASE
# ==========================================
VIRUS_DATA = {
    "Progenitor Virus": {"dev": "Found in Nature", "disc": "Ndipaya Kingdom, Spencer, Marcus, Ashford", "antigens": "Unknown", "color": "#FFA500"},
    "T-Veronica Virus": {"dev": "Umbrella Corporation (Alexander Ashford)", "disc": "Alexia Ashford", "antigens": "1. Anti-T-Veronica", "color": "#32CD32"},
    "G-Virus (Golgotha)": {"dev": "Umbrella Corporation (William Birkin)", "disc": "William Birkin", "antigens": "1. Anti-G\n2. G-Vaccine", "color": "#8A2BE2"},
    "T-Abyss Virus": {"dev": "synthesized by Tricell (ex-Umbrella)", "disc": "Jack Norman", "antigens": "1. T-Abyss Antivirus", "color": "#00CED1"},
    "C-Virus (Chrysalid)": {"dev": "The Family (Carla Radames)", "disc": "Carla Radames", "antigens": "1. Anti-C", "color": "#DDDDDD"},
    "T-Phobos Virus": {"dev": "Alex Wesker's Research Team", "disc": "Alex Wesker", "antigens": "None Known", "color": "#00FFFF"},
    "A-Virus (Animality)": {"dev": "synthesized by Tricell (Glenn Arias)", "disc": "Glenn Arias", "antigens": "1. Dagger\n2. D-1 Antivirus", "color": "#DC143C"},
    "Las Plagas Parasite": {"dev": "Los Iluminados (Cult)", "disc": "Osmund Saddler", "antigens": "N/A - Parasitic Removal\n1. Surgical Removal\n2. P.R.L. 412", "color": "#9ACD32"},
    "Mutamycete (E-Series)": {"dev": "The Connections", "disc": "Miranda / Mia Winters (E-001)", "antigens": "1. Eveline Antibody (Experimental)", "color": "#556B2F"}
}