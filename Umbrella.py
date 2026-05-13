import sys
import os
import shutil
import json
import random
import time
import cv2
import webbrowser
import psutil  
from deepface import DeepFace
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QTreeView, QListView, QSplitter, 
                             QPushButton, QMessageBox, QDialog, QProgressBar,
                             QLineEdit, QTextEdit, QFormLayout, QHBoxLayout,
                             QStackedWidget, QListWidget, QListWidgetItem, QFrame,
                             QMdiArea, QMdiSubWindow, QSlider, QGridLayout, QTabWidget, QFileDialog,
                             QGraphicsOpacityEffect) 
from PyQt6.QtCore import Qt, QDir, QTimer, QUrl, QSize, QFileInfo, QDateTime, QPropertyAnimation, QObject, QEvent
from PyQt6.QtGui import QFileSystemModel, QDesktopServices, QFont, QPixmap, QIcon, QBrush, QColor, QMovie
from RedQueenPuzzles import PuzzleManager
# --- SAFE MULTIMEDIA IMPORT ---
try:
    from PyQt6.QtMultimedia import QSoundEffect
    AUDIO_ENABLED = True
except ImportError:
    AUDIO_ENABLED = False

# --- GLOBAL STYLESHEETS ---
CORPORATE_THEME = """
    QMainWindow, QWidget {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5C7680, stop:0.5 #384C54, stop:1 #1A2428);
    }
    QLabel { color: #FFFFFF; font-family: 'Courier New', monospace; background: transparent; }
    QLineEdit, QTextEdit {
        background-color: #55656E; color: #FFFFFF; border: 2px inset #2A363B;
        font-family: 'Courier New', monospace; font-size: 16px; padding: 6px;
    }
    QPushButton {
        background-color: #24465C; color: #FFFFFF; border: 2px outset #5C7680;
        font-family: 'Arial', sans-serif; font-size: 16px; font-weight: bold; padding: 8px;
    }
    QPushButton:pressed {
        border: 2px inset #5C7680;
        background-color: #1A2428;
    }
    QPushButton:hover { background-color: #315C7A; }
    
    /* File Explorer Specifics */
    QTreeView, QListView { 
        background-color: #384C54; color: #FFFFFF; border: 2px inset #1A2428; font-family: 'Courier New'; font-size: 14px;
    }
    QTreeView::item:selected, QListView::item:selected { background-color: #1A2428; color: #FF0000; border: 1px solid #C41E3A;}
    QTreeView::item:hover, QListView::item:hover { background-color: #2A363B; }
    QHeaderView::section { background-color: #2A363B; color: #FFFFFF; border: 1px outset #5C7680; padding: 4px; font-weight: bold; }
    
    /* Main Sidebar Specifics */
    QListWidget#DesktopSidebar {
        background-color: rgba(26, 36, 40, 0.9);
        border-right: 2px solid #1A2428;
    }
    QListWidget#DesktopSidebar::item { padding: 12px; color: #E0E0E0; border-bottom: 1px solid #2A363B; font-family: 'Courier New'; }
    QListWidget#DesktopSidebar::item:selected {
        background-color: #24465C; color: #FFFFFF; border-left: 4px solid #5BC0BE;
    }
    
    /* Draggable Window Theming - CLASSIC WINDOWS 95/XP STYLE */
    QMdiSubWindow {
        background-color: #384C54;
        border: 2px outset #A0B0B5;
    }
    QMdiSubWindow::title {
        background-color: #1A2428;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 13px;
        padding: 4px;
    }
    
    /* RESTORED WINDOW CONTROLS */
    QMdiSubWindow::minimize-button {
        background-color: #5BC0BE;
        border: 1px solid #000000;
        width: 12px; height: 12px; margin: 2px;
    }
    QMdiSubWindow::maximize-button {
        background-color: #A0B0B5;
        border: 1px solid #000000;
        width: 12px; height: 12px; margin: 2px;
    }
    QMdiSubWindow::close-button {
        background-color: #C41E3A;
        border: 1px solid #000000;
        width: 12px; height: 12px; margin: 2px;
    }
    QMdiSubWindow::minimize-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::close-button:hover {
        background-color: #FFFFFF;
    }
"""

# --- DATABASE SETUP ---
DB_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_DB.json')

def load_database():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f: json.dump({}, f) 
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_database(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- BIOMETRIC SCANNER ---
def capture_face(emp_id="temp"):
    cap = cv2.VideoCapture(0)
    saved_path = None
    img_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_BIOMETRICS')
    if not os.path.exists(img_dir): os.makedirs(img_dir)
        
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        height, width, _ = frame.shape
        cv2.rectangle(frame, (width//4, height//4), (width*3//4, height*3//4), (0, 0, 255), 2)
        cv2.putText(frame, "ALIGN FACE IN GRID", (width//4, height//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(frame, "PRESS 'SPACE' TO INITIATE SCAN", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("UMBRELLA CORP // BIOMETRIC SCANNER", frame)
        
        key = cv2.waitKey(1)
        if key == 32: 
            file_name = f"{emp_id}_scan.jpg"
            saved_path = os.path.join(img_dir, file_name)
            cv2.imwrite(saved_path, frame)
            break
        elif key == 27: break
            
    cap.release()
    cv2.destroyAllWindows()
    return saved_path

# ==========================================
# INTERNAL SUB-ROUTINES (DRAGGABLE APPS)
# ==========================================

class RedQueenDOSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #050505; border: 2px solid #00FF00;")
        layout = QVBoxLayout()
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-size: 14px; background: transparent; border: none;")
        self.output.setText(">> RED QUEEN MAINFRAME DOS v1.0\n>> ALL ACTIONS MONITORED.\n>> WAITING FOR INPUT...\n")
        
        input_layout = QHBoxLayout()
        prompt = QLabel("C:\\>")
        prompt.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-size: 14px; font-weight: bold; border: none;")
        self.command_input = QLineEdit()
        self.command_input.setStyleSheet("color: #00FF00; font-family: 'Courier New'; font-size: 14px; background: transparent; border: none;")
        self.command_input.returnPressed.connect(self.process_command)
        
        input_layout.addWidget(prompt)
        input_layout.addWidget(self.command_input)
        
        layout.addWidget(self.output)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
    def process_command(self):
        cmd = self.command_input.text().strip().lower()
        self.command_input.clear()
        self.output.append(f"C:\\> {cmd}")
        
        if cmd == "ping mainframe":
            self.output.append(">> PONG. MAINFRAME ONLINE. LATENCY: 0.04ms\n")
        elif cmd == "check_vats":
            self.output.append(">> VAT 1: STABLE\n>> VAT 2: STABLE\n>> TYRANT PROJECT: DORMANT\n")
        elif cmd == "release_hounds":
            self.output.append(">> ERROR: BIOLOGICAL CONTAINMENT PROTOCOLS ACTIVE. CANNOT RELEASE CERBERUS UNITS.\n")
        elif cmd == "clear":
            self.output.clear()
            self.output.setText(">> RED QUEEN MAINFRAME DOS v1.0\n>> ALL ACTIONS MONITORED.\n>> WAITING FOR INPUT...\n")
        elif cmd == "help":
            self.output.append(">> AVAILABLE COMMANDS: ping mainframe, check_vats, release_hounds, clear, exit\n")
        elif cmd == "whoami":
            self.output.append(">> UMBRELLA CORP PERSONNEL.\n")
        elif cmd == "exit":
            self.window().close() 
        else:
            self.output.append(f">> COMMAND NOT RECOGNIZED: '{cmd}'. TYPE 'help' FOR COMMANDS.\n")
        
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())


class SurveillanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #2A363B; }")
        layout = QGridLayout()
        
        cam_paths = [r"D:\cam1.gif", r"D:\cam2.gif", r"D:\cam3.gif", r"D:\cam4.gif"]
        labels = ["CAM 01 - LAB ALPHA", "CAM 02 - SERVER ROOM", "CAM 03 - CONTAINMENT", "CAM 04 - CORRIDOR B"]
        
        for i in range(4):
            container = QWidget()
            cont_layout = QVBoxLayout(container)
            
            title = QLabel(labels[i])
            title.setStyleSheet("color: #FFFFFF; background: #1A2428; font-family: 'Courier New'; font-weight: bold; padding: 4px; border: 1px solid #5C7680;")
            cont_layout.addWidget(title)
            
            feed = QLabel()
            feed.setAlignment(Qt.AlignmentFlag.AlignCenter)
            feed.setStyleSheet("background-color: #1A2428; border: 2px inset #5C7680;")
            
            if os.path.exists(cam_paths[i]):
                movie = QMovie(cam_paths[i])
                feed.setMovie(movie)
                movie.start()
            else:
                feed.setText(">> CAMERA OFFLINE\n>> NO SIGNAL")
                feed.setStyleSheet("color: #FF0000; font-family: 'Courier New'; background-color: #1A2428; border: 2px inset #5C7680;")
                
            cont_layout.addWidget(feed)
            row, col = divmod(i, 2)
            layout.addWidget(container, row, col)
            
        self.setLayout(layout)

class DiagnosticsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; color: #FFFFFF; font-family: 'Courier New'; }")
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::pane { border: 2px inset #5C7680; background: #2A363B; } QTabBar::tab { background: #1A2428; color: #A0B0B5; padding: 8px 15px; border: 1px solid #5C7680; } QTabBar::tab:selected { background: #384C54; color: #FFF; border-bottom: none; }")
        
        perf_tab = QWidget()
        perf_layout = QFormLayout(perf_tab)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet("QProgressBar { border: 2px inset #1A2428; background: #55656E; text-align: center; color: #FFF; } QProgressBar::chunk { background-color: #C41E3A; width: 10px; margin: 1px; }")
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet("QProgressBar { border: 2px inset #1A2428; background: #55656E; text-align: center; color: #FFF; } QProgressBar::chunk { background-color: #5BC0BE; width: 10px; margin: 1px; }")
        
        perf_layout.addRow("CPU UTILIZATION:", self.cpu_bar)
        perf_layout.addRow("RAM ALLOCATION:", self.ram_bar)
        
        cont_tab = QWidget()
        cont_layout = QVBoxLayout(cont_tab)
        cont_layout.addWidget(QLabel(">> T-VIRUS VAT 1: NOMINAL (99%)\n>> T-VIRUS VAT 2: NOMINAL (98%)\n>> TYRANT PROJECT: DORMANT"))
        
        tabs.addTab(perf_tab, "PERFORMANCE")
        tabs.addTab(cont_tab, "CONTAINMENT")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

    def update_stats(self):
        self.cpu_bar.setValue(int(psutil.cpu_percent()))
        self.ram_bar.setValue(int(psutil.virtual_memory().percent))

class CommLinkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; }")
        layout = QVBoxLayout()
        
        header = QLabel(">> SECURE NEST COMM-LINK")
        header.setStyleSheet("color: #FFFFFF; font-family: 'Courier New'; font-weight: bold; font-size: 16px; border: none;")
        layout.addWidget(header)
        
        self.text_editor = QTextEdit()
        self.text_editor.setStyleSheet("background-color: #F0F0F0; color: #000000; font-family: 'Courier New'; border: 2px inset #1A2428;")
        layout.addWidget(self.text_editor)
        
        save_btn = QPushButton("[ ENCRYPT & SAVE LOG ]")
        save_btn.clicked.connect(self.save_log)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)

    def save_log(self):
        content = self.text_editor.toPlainText()
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        classified_header = f"========================================\n// UMBRELLA CORPORATION - TOP SECRET\n// NEST FACILITY COMM-LOG\n// TIMESTAMP: {timestamp}\n========================================\n\n"
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Classified Log", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(classified_header + content)
            QMessageBox.information(self, "SAVED", ">> LOG ENCRYPTED AND STORED SECURELY.")

class IncineratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #2A363B; }")
        self.layout = QVBoxLayout()
        
        self.title = QLabel(">> UMBRELLA INCINERATOR")
        self.title.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 24px; font-weight: bold; border: none;")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.info = QLabel("Select a file for permanent thermal deletion.\nWARNING: THIS ACTION CANNOT BE UNDONE.")
        self.info.setStyleSheet("color: #E0E0E0; font-family: 'Arial'; border: none;")
        self.layout.addWidget(self.info, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.select_btn = QPushButton("[ SELECT TARGET FILE ]")
        self.select_btn.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_btn)
        
        self.target_lbl = QLabel("TARGET: NONE")
        self.target_lbl.setStyleSheet("color: #FFF; font-family: 'Courier New'; border: 2px inset #1A2428; background: #111417; padding: 5px;")
        self.layout.addWidget(self.target_lbl)
        
        self.purge_btn = QPushButton("[ PURGE PROTOCOL ]")
        self.purge_btn.setStyleSheet("background-color: #8A0303; color: #FFF; font-size: 18px; font-weight: bold; padding: 15px; border: 2px outset #C41E3A;")
        self.purge_btn.clicked.connect(self.purge_file)
        self.layout.addWidget(self.purge_btn)
        
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setStyleSheet("QProgressBar { border: 2px inset #1A2428; background: #55656E; text-align: center; color: #FFF; } QProgressBar::chunk { background-color: #FF4500; }")
        self.layout.addWidget(self.progress)
        
        self.setLayout(self.layout)
        self.target_file = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Target to Purge", "", "All Files (*)")
        if file_path:
            self.target_file = file_path
            self.target_lbl.setText(f"TARGET: {os.path.basename(file_path)}")

    def purge_file(self):
        if not self.target_file or not os.path.exists(self.target_file):
            return
        self.title.setText(">> INCINERATING...")
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.burn_animation)
        self.timer.start(50)

    def burn_animation(self):
        self.counter += 2
        self.progress.setValue(self.counter)
        if self.counter >= 100:
            self.timer.stop()
            try:
                os.remove(self.target_file)
                self.title.setText(">> TARGET DESTROYED.")
                self.target_lbl.setText("TARGET: NONE")
                self.target_file = None
            except Exception as e:
                self.title.setText(">> INCINERATOR FAILURE.")
            self.progress.setValue(0)

class AudioRoutineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; }")
        layout = QVBoxLayout()
        header = QLabel(">> UMBRELLA CORP // SPATIAL AUDIO MATRIX")
        header.setStyleSheet("color: #FFFFFF; font-family: 'Courier New'; font-weight: bold; font-size: 16px;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)
        
        eq_layout = QHBoxLayout()
        freqs = ["32Hz", "64Hz", "125Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz", "16kHz"]
        for freq in freqs:
            col = QVBoxLayout()
            slider = QSlider(Qt.Orientation.Vertical)
            slider.setRange(-12, 12)
            slider.setValue(random.randint(-5, 8))
            slider.setStyleSheet("QSlider::groove:vertical { background: #1A2428; width: 6px; border: 1px inset #5C7680; } QSlider::handle:vertical { background: #A0B0B5; height: 15px; margin: 0 -4px; border: 1px outset #FFFFFF;}")
            lbl = QLabel(freq)
            lbl.setStyleSheet("font-size: 10px; color: #FFFFFF;")
            col.addWidget(slider, alignment=Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
            eq_layout.addLayout(col)
            
        layout.addLayout(eq_layout)
        self.setLayout(layout)

class MediaRoutineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; }")
        layout = QVBoxLayout()
        header = QLabel(">> UMBRELLA CORP // AUDIO VISUALIZER")
        header.setStyleSheet("color: #FFFFFF; font-family: 'Courier New'; font-weight: bold; font-size: 16px;")
        layout.addWidget(header)
        
        main_layout = QHBoxLayout()
        album_art = QLabel("NO SIGNAL")
        album_art.setFixedSize(150, 150)
        album_art.setStyleSheet("background-color: #1A2428; border: 2px inset #5C7680;")
        album_art.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(album_art)
        
        controls = QVBoxLayout()
        self.track_name = QLabel("TRACK: Unknown_Signal.wav\nARTIST: Classified")
        self.track_name.setStyleSheet("font-size: 14px; color: #FFFFFF; background-color: #2A363B; padding: 5px; border: 1px inset #1A2428;")
        controls.addWidget(self.track_name)
        
        progress = QProgressBar()
        progress.setValue(35)
        progress.setStyleSheet("QProgressBar { background-color: #1A2428; border: 2px inset #5C7680; height: 10px; } QProgressBar::chunk { background-color: #5BC0BE; }")
        progress.setTextVisible(False)
        controls.addWidget(progress)
        
        btns = QHBoxLayout()
        for b in ["<< PREV", "[ PLAY / PAUSE ]", "NEXT >>"]:
            btn = QPushButton(b)
            btns.addWidget(btn)
        controls.addLayout(btns)
        main_layout.addLayout(controls)
        layout.addLayout(main_layout)
        self.setLayout(layout)

# ==========================================
# VIRUS DATABASE MODULE
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

class VirusDatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; }")
        layout = QHBoxLayout()
        
        self.virus_list = QListWidget()
        self.virus_list.setFixedWidth(300)
        self.virus_list.setStyleSheet("background-color: #2A363B; font-size: 16px; border: 2px inset #1A2428;")
        for v in VIRUS_DATA.keys(): self.virus_list.addItem(v)
        self.virus_list.itemClicked.connect(self.display_virus)
        layout.addWidget(self.virus_list)
        
        self.card_panel = QFrame()
        self.card_panel.setStyleSheet("background-color: #2A363B; border: 2px inset #1A2428;")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        self.v_title = QLabel(">> SELECT VIRUS STRAIN")
        self.v_title.setStyleSheet("font-size: 28px; font-family: 'Arial'; font-weight: bold; color: #FFFFFF; border: none;")
        self.v_dev = QLabel("")
        self.v_disc = QLabel("")
        self.v_anti = QLabel("")
        for lbl in [self.v_dev, self.v_disc, self.v_anti]:
            lbl.setStyleSheet("font-size: 16px; font-family: 'Arial'; color: #E0E0E0; border: none;")
            lbl.setWordWrap(True)
            
        self.vial_graphic = QLabel()
        self.vial_graphic.setFixedSize(150, 250)
        self.vial_graphic.setStyleSheet("background-color: #111417; border: 2px inset #000000; border-radius: 10px;")
        
        data_layout = QHBoxLayout()
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.v_title)
        text_layout.addWidget(self.v_dev)
        text_layout.addWidget(self.v_disc)
        text_layout.addWidget(self.v_anti)
        text_layout.addStretch()
        data_layout.addLayout(text_layout)
        data_layout.addWidget(self.vial_graphic, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        card_layout.addLayout(data_layout)
        self.card_panel.setLayout(card_layout)
        layout.addWidget(self.card_panel)
        self.setLayout(layout)
        
    def display_virus(self, item):
        name = item.text()
        data = VIRUS_DATA[name]
        self.v_title.setText(f"Full Name: {name}")
        self.v_dev.setText(f"Developer: {data['dev']}")
        self.v_disc.setText(f"Discovered By: {data['disc']}")
        self.v_anti.setText(f"Known Antigens:\n{data['antigens']}")
        self.vial_graphic.setStyleSheet(f"background: qradialgradient(cx:0.5, cy:0.5, radius: 0.8, fx:0.5, fy:0.5, stop:0 {data['color']}, stop:1 #000000); border: 2px inset #000000; border-radius: 10px;")

# ==========================================
# THE FILE EXPLORER
# ==========================================
class UmbrellaExplorerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #384C54; }")
        self.quarantine_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'UMBRELLA_QUARANTINE')
        if not os.path.exists(self.quarantine_dir): os.makedirs(self.quarantine_dir)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        header_layout = QHBoxLayout()
        self.header = QLabel(f">> SYSTEM ONLINE.\n>> QUARANTINE ZONE: {self.quarantine_dir}")
        self.header.setStyleSheet("color: #FFFFFF; font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; border: none;")
        header_layout.addWidget(self.header)
        layout.addLayout(header_layout)
        
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("") 
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(""))
        for i in range(1, self.file_model.columnCount()): self.tree_view.hideColumn(i)
        
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        self.list_view.setRootIndex(self.file_model.index(""))
        self.list_view.setViewMode(QListView.ViewMode.IconMode)
        self.list_view.setIconSize(QSize(64, 64))
        self.list_view.setGridSize(QSize(120, 120))
        self.list_view.setWordWrap(True)
        self.list_view.doubleClicked.connect(self.open_file) 
        
        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.list_view.clicked.connect(self.update_details_pane)
        self.tree_view.clicked.connect(self.update_details_pane)
        
        self.details_panel = QFrame()
        self.details_panel.setStyleSheet("background-color: #2A363B; border-left: 2px solid #1A2428;")
        details_layout = QVBoxLayout()
        details_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.det_icon = QLabel()
        self.det_icon.setFixedSize(100, 100)
        self.det_icon.setStyleSheet("background-color: #1A2428; border: 2px inset #000000; border-radius: 5px;")
        
        self.det_name = QLabel("Select a file")
        self.det_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFF; margin-top: 20px; border: none;")
        self.det_name.setWordWrap(True)
        
        self.det_info = QLabel("Select a single file to get more\ninformation and share your\ncloud content.")
        self.det_info.setStyleSheet("font-size: 12px; color: #A0B0B5; margin-top: 10px; border: none;")
        self.det_info.setWordWrap(True)
        
        details_layout.addWidget(self.det_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        details_layout.addWidget(self.det_name)
        details_layout.addWidget(self.det_info)
        
        self.quarantine_btn = QPushButton("[ CONTAIN BIOHAZARD ]")
        self.quarantine_btn.setStyleSheet("margin-top: 50px;")
        self.quarantine_btn.clicked.connect(self.quarantine_selected_file)
        details_layout.addWidget(self.quarantine_btn)
        
        self.details_panel.setLayout(details_layout)
        
        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.list_view)
        splitter.addWidget(self.details_panel)
        splitter.setSizes([250, 600, 250]) 
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def on_tree_clicked(self, index):
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            self.list_view.setRootIndex(index)

    def update_details_pane(self, index):
        file_info = self.file_model.fileInfo(index)
        self.det_name.setText(file_info.fileName())
        if file_info.isDir():
            self.det_info.setText("Type: File Folder\n\nContains secure Umbrella assets.")
            self.det_icon.setStyleSheet("background-color: #D4AF37; border-radius: 5px;") 
        else:
            size_kb = file_info.size() / 1024
            mod_time = file_info.lastModified().toString("dd-MM-yyyy HH:mm")
            self.det_info.setText(f"Date Modified:\n{mod_time}\n\nSize: {size_kb:.2f} KB\n\nClassification: RESTRICTED")
            self.det_icon.setStyleSheet("background-color: #5BC0BE; border-radius: 5px;") 

    def open_file(self, index):
        if self.file_model.isDir(index):
            self.list_view.setRootIndex(index)
            self.tree_view.setCurrentIndex(index)
            path = self.file_model.filePath(index)
            if hasattr(self, 'header') and "ALPHA OVERRIDE ACCEPTED" not in self.header.text():
                self.header.setText(f">> ACCESSING SECTOR: {path}")
        else:
            file_path = self.file_model.filePath(index)
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def quarantine_selected_file(self):
        indexes = self.list_view.selectedIndexes()
        if not indexes: return
        file_path = self.file_model.filePath(indexes[0])
        file_name = self.file_model.fileName(indexes[0])
        if self.file_model.isDir(indexes[0]): return
            
        warning = QMessageBox(self)
        warning.setWindowTitle("BIOHAZARD DETECTED")
        warning.setText(f"WARNING: Data anomalies detected in:\n\n{file_name}\n\nProceed with containment?")
        warning.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Abort)
        
        if warning.exec() == QMessageBox.StandardButton.Yes:
            try:
                destination = os.path.join(self.quarantine_dir, file_name)
                shutil.move(file_path, destination)
                self.det_info.setText(">> FILE SECURED IN QUARANTINE.")
            except Exception as e:
                pass

# ==========================================
# SYSTEM SCREENS
# ==========================================

class BiosScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QWidget { background-color: #000000; } QTextEdit { background-color: #000000; color: #00FF00; border: none; font-family: 'Courier New'; font-size: 16px; font-weight: bold; }")
        layout = QVBoxLayout()
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        layout.addWidget(self.terminal)
        self.setLayout(layout)
        
    def start_boot(self):
        if AUDIO_ENABLED and hasattr(self.main_window, 'sfx_boot'):
            self.main_window.sfx_boot.play()
            
        self.terminal.clear()
        self.boot_lines = [
            "UMBRELLA CORP BIOS v4.0.2",
            "Copyright (C) 1998, Umbrella Corporation",
            "Initializing Memory Controllers...", "OK",
            "Loading Red Queen Logic Matrix...", "OK",
            "Mounting NEST Facility Network...", "OK",
            "Bypassing Thermal Regulators...", "WARNING: REGULATORS OFFLINE",
            "Checking T-Virus Containment Vats...", "VAT 1: STABLE", "VAT 2: STABLE", "VAT 3: STABLE",
            "Initializing Defense Grid...", "ARMED",
            "Fetching Corporate UI Assets...", "OK",
            "SYSTEM READY. HANDING OVER TO MAINFRAME..."
        ]
        for _ in range(30): self.boot_lines.insert(3, f"0x{random.randint(100000, 999999):06X} : MEMORY ALLOCATED")
        self.current_line = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.print_next_line)
        self.timer.start(200) 
        
    def print_next_line(self):
        if self.current_line < len(self.boot_lines):
            self.terminal.append(self.boot_lines[self.current_line])
            self.current_line += 1
        else:
            self.timer.stop()
            QTimer.singleShot(800, lambda: self.main_window.switch_screen(7))

class SplashScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout()
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        splash_path = r"D:\5e8500219061405.Y3JvcCwxMzgwLDEwODAsMjcwLDA.jpg" 
        if os.path.exists(splash_path):
            pixmap = QPixmap(splash_path).scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pixmap)
        else:
            self.logo.setText("[ THE FUTURE IS VIRAL. 1968. UMBRELLA CORP. ]\n(Save image to D:\\5e8500219061405.Y3JvcCwxMzgwLDEwODAsMjcwLDA.jpg)")
            self.logo.setStyleSheet("color: #FFFFFF; font-family: 'Arial'; font-size: 24px; font-weight: bold;")
            
        layout.addWidget(self.logo)
        self.setLayout(layout)

        self.opacity_effect = QGraphicsOpacityEffect()
        self.logo.setGraphicsEffect(self.opacity_effect)

    def start_splash(self):
        self.anim_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_in.setDuration(2000) 
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.finished.connect(self.pause_splash)
        self.anim_in.start()

    def pause_splash(self):
        QTimer.singleShot(1500, self.fade_out)

    def fade_out(self):
        self.anim_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_out.setDuration(2000) 
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.finished.connect(lambda: self.main_window.switch_screen(1)) 
        self.anim_out.start()

class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_path = r"D:\Umbrella_Corporation_logo.svg.png"
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path).scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(logo_pixmap)
        else:
            self.logo_label.setText("[ UMBRELLA LOGO ]")
            self.logo_label.setStyleSheet("color: red; font-size: 20px; background: transparent;")
            
        layout.addWidget(self.logo_label)

        title = QLabel("UMBRELLA\nLABORATORIES")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 55px; letter-spacing: 2px; font-family: 'Impact'; color: #FFFFFF; background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel("Our business is life itself")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; font-family: 'Courier New', monospace; color: #A0B0B5; background: transparent;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(30) 

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        self.emp_id_input = QLineEdit()
        self.emp_id_input.setFixedWidth(300)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(300)
        self.security_key_input = QLineEdit()
        self.security_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.security_key_input.setFixedWidth(300)

        lbl1, lbl2, lbl3 = QLabel("User"), QLabel("Access Code"), QLabel("Security Key")
        for lbl in [lbl1, lbl2, lbl3]: lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF; background: transparent;")

        form_layout.addRow(lbl1, self.emp_id_input)
        form_layout.addRow(lbl2, self.password_input)
        form_layout.addRow(lbl3, self.security_key_input)
        layout.addLayout(form_layout)

        self.enter_btn = QPushButton("ENTER")
        self.enter_btn.setFixedWidth(150)
        self.enter_btn.clicked.connect(self.verify_credentials) 
        layout.addWidget(self.enter_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #FF0000; font-family: 'Courier New'; font-weight: bold; font-size: 16px; background: transparent;")
        layout.addWidget(self.status_label)
        
        layout.addSpacing(20)

        fine_print = QLabel("SECURITY WARNING: Anything viewed beyond this screen is covered under the Umbrella Corporation Security Agreement\nand any second party viewing by unauthorized personnel will be punished under said company's Treason and Terrorism\nDirective (Article 12, paragraph 19, section C.)")
        fine_print.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fine_print.setStyleSheet("font-family: 'Arial', sans-serif; font-size: 11px; color: #A0B0B5; background: transparent;")
        layout.addWidget(fine_print)

        self.setLayout(layout)

    def verify_credentials(self):
        emp_id = self.emp_id_input.text().strip().upper()
        pwd = self.password_input.text().strip()
        sec_key = self.security_key_input.text().strip()
        
        if emp_id == "UMB-ADMIN" and pwd == "REDQUEEN":
            if sec_key == "7680":
                delay = random.randint(355, 900)
                QTimer.singleShot(delay, self.play_login_sfx)
                
                self.main_window.switch_screen(6)
                self.main_window.screens[6].start_override()
                self.emp_id_input.clear()
                self.password_input.clear()
                self.security_key_input.clear()
                return
            else:
                self.main_window.switch_screen(3)
                self.main_window.screens[3].start_lockdown()
                return

        if not emp_id:
            self.main_window.switch_screen(2) 
            return
            
        db = load_database()
        
        if emp_id in db and db[emp_id]["password"] == pwd:
            if db[emp_id].get("security_key") != sec_key:
                self.status_label.setText(">> ERROR: INVALID SECURITY KEY.")
                return
                
            self.status_label.setText(">> CREDENTIALS ACCEPTED. INITIATING OPTICS...")
            QApplication.processEvents() 
            
            live_scan_path = capture_face(f"login_attempt_{emp_id}")
            if live_scan_path:
                try:
                    self.status_label.setText(">> RUNNING DEEP NEURAL VERIFICATION...")
                    QApplication.processEvents()
                    
                    saved_img_path = db[emp_id]["face_img_path"]
                    result = DeepFace.verify(img1_path=saved_img_path, img2_path=live_scan_path, enforce_detection=False)
                    if os.path.exists(live_scan_path): os.remove(live_scan_path)
                    
                    if result["verified"]:
                        delay = random.randint(355, 900)
                        QTimer.singleShot(delay, self.play_login_sfx)
                        
                        self.status_label.setText(f">> BIOMETRIC MATCH: {db[emp_id]['name']}\n>> ACCESS GRANTED.")
                        QTimer.singleShot(1000, lambda: self.main_window.switch_screen(5))
                        return
                    else:
                        self.status_label.setText(">> ERROR: BIOMETRIC MISMATCH.")
                except Exception:
                    self.status_label.setText(">> ERROR: NEURAL NETWORK FAILURE.")
            else:
                self.status_label.setText(">> ERROR: NO FACE DETECTED.")
                
        self.main_window.switch_screen(3)
        self.main_window.screens[3].start_lockdown()

    def play_login_sfx(self):
        if hasattr(self.main_window, 'sfx_login'):
            self.main_window.sfx_login.play()

# --- UPDATED: DEATH SCREEN ---
class DeathScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window 
        self.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0) 
        self.label.setGraphicsEffect(self.opacity_effect)

    def trigger_death(self):
        self.opacity_effect.setOpacity(0.0) 
        
        if AUDIO_ENABLED and hasattr(self.main_window, 'sfx_toxin'):
            self.main_window.sfx_toxin.play()
            
        QTimer.singleShot(2000, self.show_blood_splash)

    def show_blood_splash(self):
        blood_path = r"D:\blood_splash.png"
        if os.path.exists(blood_path):
            pixmap = QPixmap(blood_path).scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(pixmap)
        else:
            self.label.setText(">> FATAL TOXICITY <<")
            self.label.setStyleSheet("color: #8A0303; font-family: 'Impact'; font-size: 100px;")
            
        self.opacity_effect.setOpacity(1.0)
        QTimer.singleShot(300, self.fade_in_death)

    def fade_in_death(self):
        death_img_path = r"D:\you_are_dead.jpg"
        if os.path.exists(death_img_path):
            pixmap = QPixmap(death_img_path).scaled(800, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(pixmap)
        else:
            self.label.setText("YOU ARE DEAD\n(Save image to D:\\you_are_dead.jpg)")
            self.label.setStyleSheet("color: #8A0303; font-family: 'Times New Roman', serif; font-size: 80px; font-weight: bold;")
            
        self.opacity_effect.setOpacity(0.0)
        self.anim_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_in.setDuration(3000) 
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.finished.connect(self.exit_system)
        self.anim_in.start()

    def exit_system(self):
        QTimer.singleShot(3000, sys.exit)

class LockdownScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QWidget { background-color: #4A0000; }")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 25px; color: #FF0000; font-family: 'Courier New', monospace; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

        # Container to hold the dynamic mechanical puzzles
        self.puzzle_container = QWidget()
        self.puzzle_layout = QVBoxLayout(self.puzzle_container)
        self.layout.addWidget(self.puzzle_container)
        
        self.required_solves = 2 # Normal Employee Requirement
        self.current_solves = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_lockdown(self):
        self.time_left = 60
        self.current_solves = 0
        self.timer.start(1000)
        self.load_next_puzzle()

    def load_next_puzzle(self):
        # Clear the old puzzle
        for i in reversed(range(self.puzzle_layout.count())): 
            widget = self.puzzle_layout.itemAt(i).widget()
            if widget is not None: widget.deleteLater()
            
        # Get a new interactive puzzle from the external engine
        self.active_puzzle = PuzzleManager.get_random_puzzle()
        self.active_puzzle.solved.connect(self.puzzle_completed)
        self.puzzle_layout.addWidget(self.active_puzzle)

    def puzzle_completed(self):
        self.current_solves += 1
        if self.current_solves >= self.required_solves:
            self.timer.stop()
            self.main_window.switch_screen(4) # Unlock successful
        else:
            self.load_next_puzzle()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"TIME UNTIL NEURO-TOXIN: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.main_window.switch_screen(2) # Death
class OverrideScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QWidget { background-color: #050A05; border: 4px solid #00FF00; }")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel()
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 25px; color: #00FF00; font-family: 'Courier New', monospace; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

        self.puzzle_container = QWidget()
        self.puzzle_layout = QVBoxLayout(self.puzzle_container)
        self.layout.addWidget(self.puzzle_container)
        
        self.required_solves = 5 # Admin Override Requirement
        self.current_solves = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_override(self):
        self.time_left = 360 # More time for 5 mechanical puzzles
        self.current_solves = 0
        self.timer.start(1000)
        self.load_next_puzzle()

    def load_next_puzzle(self):
        for i in reversed(range(self.puzzle_layout.count())): 
            widget = self.puzzle_layout.itemAt(i).widget()
            if widget is not None: widget.deleteLater()
            
        self.active_puzzle = PuzzleManager.get_random_puzzle()
        self.active_puzzle.solved.connect(self.puzzle_completed)
        self.puzzle_layout.addWidget(self.active_puzzle)

    def puzzle_completed(self):
        self.current_solves += 1
        if self.current_solves >= self.required_solves:
            self.timer.stop()
            self.main_window.switch_screen(5) # Direct to Desktop
            if hasattr(self.main_window.screens[5], 'file_explorer'):
                self.main_window.screens[5].file_explorer.header.setText(">> ALPHA OVERRIDE ACCEPTED.")
        else:
            self.load_next_puzzle()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"SYSTEM LOCK IN: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.main_window.switch_screen(2) # Death

class RegistrationScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.face_encoding_data = None
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header = QLabel(">> NEST FACILITY REGISTRATION")
        header.setStyleSheet("font-size: 25px; font-weight: bold; color: #C41E3A;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        self.inputs = {
            "name": QLineEdit(), "password": QLineEdit(), "blood_group": QLineEdit(),
            "allergies": QLineEdit(), "hobbies": QLineEdit(), "loyalty": QLineEdit(),
            "strengths": QLineEdit(), "weaknesses": QLineEdit(), "opinion": QTextEdit(), "ambition": QTextEdit()
        }
        self.inputs["password"].setEchoMode(QLineEdit.EchoMode.Password)
        labels = ["FULL NAME:", "SET PASSWORD:", "BLOOD GROUP:", "KNOWN ALLERGIES:", "CIVILIAN HOBBIES:", 
                  "CORP LOYALTY INDEX:", "COMBAT/INTEL STRENGTHS:", "PSYCHOLOGICAL WEAKNESSES:", "OPINION ON UMBRELLA:", "RESEARCH AMBITIONS:"]
        for idx, (key, widget) in enumerate(self.inputs.items()):
            widget.setFixedWidth(500)
            if isinstance(widget, QTextEdit): widget.setFixedHeight(40)
            lbl = QLabel(labels[idx])
            lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
            form_layout.addRow(lbl, widget)

        layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.scan_btn = QPushButton("[ CAPTURE BIOMETRIC SIGNATURE ]")
        self.scan_btn.clicked.connect(self.run_biometric_scan)
        layout.addWidget(self.scan_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.submit_btn = QPushButton("[ COMMIT TO DATABASE ]")
        self.submit_btn.clicked.connect(self.save_employee)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def run_biometric_scan(self):
        self.face_encoding_data = capture_face("temp_registration")
        if self.face_encoding_data:
            self.scan_btn.setText("[ BIOMETRIC SIGNATURE ACQUIRED ]")
            self.scan_btn.setStyleSheet("color: #00FF00; border: 2px solid #00FF00;")

    def save_employee(self):
        if not self.face_encoding_data: return
        db = load_database()
        while True:
            new_id = f"UMB-{random.randint(1, 999):03d}"
            if new_id not in db: break
            
        new_sec_key = f"{random.randint(1000, 9999):04d}" 
        
        final_img_path = self.face_encoding_data.replace("temp_registration", new_id)
        if os.path.exists(self.face_encoding_data): os.rename(self.face_encoding_data, final_img_path)
                
        db[new_id] = { k: v.text() if isinstance(v, QLineEdit) else v.toPlainText() for k, v in self.inputs.items() }
        db[new_id]["face_img_path"] = final_img_path
        db[new_id]["security_key"] = new_sec_key
        
        save_database(db)
        QMessageBox.information(self, "ASSIMILATION COMPLETE", f">> YOUR SECURE IDENTIFIER IS: {new_id}\n>> YOUR SECURITY KEY IS: {new_sec_key}\n\nMEMORIZE THESE IMMEDIATELY.")
        self.main_window.switch_screen(1)


# --- NEW: IDLE SCREENSAVER (Bouncing Logo) ---
class Screensaver(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #000000;")
        
        self.logo = QLabel(self)
        logo_path = r"D:\Umbrella_Corporation_logo.svg.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pixmap)
        else:
            self.logo.setText("[ UMBRELLA ]")
            self.logo.setStyleSheet("color: red; font-size: 24px; font-weight: bold;")
            
        self.logo.resize(150, 150)
        self.x_pos = 100
        self.y_pos = 100
        self.x_vel = 3
        self.y_vel = 3
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)

    def start_saver(self):
        self.timer.start(30)

    def stop_saver(self):
        self.timer.stop()

    def update_position(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        
        if self.x_pos <= 0 or self.x_pos + self.logo.width() >= self.width():
            self.x_vel *= -1
        if self.y_pos <= 0 or self.y_pos + self.logo.height() >= self.height():
            self.y_vel *= -1
            
        self.logo.move(self.x_pos, self.y_pos)

# --- GLOBAL ACTIVITY FILTER (For Screensaver) ---
class ActivityFilter(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.setInterval(180000) # 3 minutes = 180000 ms
        self.timer.timeout.connect(self.trigger_screensaver)
        self.timer.start()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.KeyPress, QEvent.Type.MouseButtonPress):
            self.timer.start() # Reset timer on activity
            if self.main_window.stack.currentIndex() == 8: # If in screensaver
                self.main_window.screens[8].stop_saver()
                self.main_window.switch_screen(5) # Wake up to desktop
        return super().eventFilter(obj, event)
        
    def trigger_screensaver(self):
        if self.main_window.stack.currentIndex() == 5: # Only trigger if on desktop
            self.main_window.switch_screen(8)
            self.main_window.screens[8].start_saver()

# ==========================================
# DESKTOP ENVIRONMENT WITH MDI
# ==========================================
class DesktopScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.main_v_layout = QVBoxLayout()
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)
        
        self.top_container = QHBoxLayout()
        self.top_container.setSpacing(0)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("DesktopSidebar")
        self.sidebar.setFixedWidth(275) 
        self.sidebar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        apps = [
            " [ Terminal: Web ]", " [ Sub-Routine: Audio Control ]", " [ Sub-Routine: Games ]", 
            " [ Sub-Routine: Media ]", " [ Sub-Routine: Driver Control ]", " [ Sub-Routine: Refresh Rate ]",
            "-----------------------",
            ">> RED QUEEN DOS",
            ">> FILE EXPLORER", ">> VIRUS DATABASE", ">> FACILITY DIAGNOSTICS", ">> NEST COMM-LINK", ">> INCINERATOR",
            "-----------------------",
            ">> ARMOURY CRATE", ">> G-HELPER", ">> STEAM", ">> EPIC GAMES", ">> SYSTEM LOGOUT"
        ]
        
        for app in apps:
            item = QListWidgetItem(app)
            if ">>" in app:
                item.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
                item.setForeground(Qt.GlobalColor.white)
            self.sidebar.addItem(item)
            
        self.sidebar.itemClicked.connect(self.launch_app)
        self.top_container.addWidget(self.sidebar)
        
        self.workspace = QMdiArea()
        self.workspace.setStyleSheet("QMdiArea { background-image: url(D:/Umbrella_Corporation_logo.svg.png); background-position: center; background-repeat: no-repeat; background-color: #1A2428; }")
        self.workspace.subWindowActivated.connect(self.refresh_taskbar)
        self.top_container.addWidget(self.workspace)
        
        self.taskbar = QFrame()
        self.taskbar.setFixedHeight(35)
        self.taskbar.setStyleSheet("""
            QFrame { 
                background-color: #1A2428; 
                border-top: 2px solid #5C7680; 
            }
            QPushButton { 
                background-color: #384C54; 
                color: #FFFFFF; 
                border: 1px outset #5C7680; 
                font-family: 'Arial'; 
                font-size: 11px;
                text-align: left;
                padding-left: 10px;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #24465C; }
            QPushButton#activeTask { 
                background-color: #24465C; 
                border: 1px inset #000000; 
                color: #5BC0BE;
                font-weight: bold;
            }
        """)
        self.taskbar_layout = QHBoxLayout(self.taskbar)
        self.taskbar_layout.setContentsMargins(5, 2, 5, 2)
        self.taskbar_layout.addStretch() 
        
        self.main_v_layout.addLayout(self.top_container)
        self.main_v_layout.addWidget(self.taskbar)
        self.setLayout(self.main_v_layout)

    def refresh_taskbar(self):
        for i in reversed(range(self.taskbar_layout.count())): 
            widget = self.taskbar_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        for window in self.workspace.subWindowList():
            btn = QPushButton(window.windowTitle())
            if self.workspace.activeSubWindow() == window:
                btn.setObjectName("activeTask")
            
            btn.clicked.connect(lambda checked, w=window: self.toggle_window(w))
            self.taskbar_layout.insertWidget(self.taskbar_layout.count() - 1, btn)

    def toggle_window(self, window):
        if window.isMinimized():
            window.showNormal()
        window.setFocus()

    def add_mdi_window(self, title, widget, width=900, height=600):
        for win in self.workspace.subWindowList():
            if win.windowTitle() == title:
                win.showNormal()
                win.setFocus()
                return
        
        if AUDIO_ENABLED and hasattr(self.main_window, 'sfx_clunk'):
            self.main_window.sfx_clunk.play()
            
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(title)
        self.workspace.addSubWindow(sub)
        sub.resize(width, height)
        sub.show()
        self.refresh_taskbar()
        
    def launch_app(self, item):
        app_name = item.text().strip()
        
        if app_name == ">> RED QUEEN DOS":
            self.add_mdi_window(">> RED QUEEN MAINFRAME DOS", RedQueenDOSApp(), 600, 400)
        elif app_name == ">> FILE EXPLORER":
            self.add_mdi_window(">> NEST FILE EXPLORER", UmbrellaExplorerApp(), 1000, 700)
        elif app_name == ">> VIRUS DATABASE":
            self.add_mdi_window(">> VIRUS DATABASE", VirusDatabaseApp(), 1100, 600)
        elif app_name == ">> FACILITY DIAGNOSTICS":
            self.add_mdi_window(">> DIAGNOSTICS", DiagnosticsApp(), 600, 400)
        elif app_name == ">> NEST COMM-LINK":
            self.add_mdi_window(">> COMM-LINK SECURE CHANNEL", CommLinkApp(), 600, 500)
        elif app_name == ">> INCINERATOR":
            self.add_mdi_window(">> THERMAL INCINERATOR", IncineratorApp(), 500, 400)
        elif app_name == "[ Sub-Routine: Surveillance ]":
            self.add_mdi_window(">> INTERNAL SURVEILLANCE", SurveillanceApp(), 800, 600)
        elif app_name == "[ Sub-Routine: Audio Control ]":
            self.add_mdi_window(">> AUDIO MATRIX CONTROL", AudioRoutineApp(), 600, 400)
        elif app_name == "[ Sub-Routine: Media ]":
            self.add_mdi_window(">> AUDIO VISUALIZER", MediaRoutineApp(), 500, 300)
        elif app_name == ">> SYSTEM LOGOUT":
            sys.exit()

        # EXTERNAL WINDOWS
        elif app_name == "[ Terminal: Web ]":
            webbrowser.open('https://google.com') 
        elif app_name == "[ Sub-Routine: Games ]":
            try: os.startfile(r"E:\Games")
            except: pass
        elif app_name == "[ Sub-Routine: Driver Control ]" or app_name == ">> G-HELPER":
            try: os.startfile(r"C:\Users\Sathwik\OneDrive\Desktop\ASUS\GHelper.exe")
            except: pass
        elif app_name == ">> STEAM":
            try: os.startfile(r"C:\Users\Sathwik\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Steam.lnk")
            except: pass
        elif app_name == ">> EPIC GAMES":
            try: os.startfile(r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe")
            except: pass


# ==========================================
# THE MASTER WINDOW
# ==========================================
class RedQueenOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UMBRELLA OS")
        self.showFullScreen()
        
        # --- LOAD SOUND EFFECTS ---
        if AUDIO_ENABLED:
                       
            self.sfx_clunk = QSoundEffect()
            self.sfx_clunk.setSource(QUrl.fromLocalFile(r"D:\Dull Booming Metal Thud.wav"))
            
            self.sfx_toxin = QSoundEffect()
            self.sfx_toxin.setSource(QUrl.fromLocalFile(r"D:\Steam - Sound Effect (HD).wav"))
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.screens = {
            0: BiosScreen(self),
            1: LoginScreen(self),
            2: DeathScreen(self), 
            3: LockdownScreen(self),
            4: RegistrationScreen(self),
            5: DesktopScreen(self),
            6: OverrideScreen(self),
            7: SplashScreen(self),
            8: Screensaver(self) 
        }
        
        for i in range(9): self.stack.addWidget(self.screens[i])
            
        self.switch_screen(0)
        self.screens[0].start_boot()
        
        self.activity_filter = ActivityFilter(self)
        QApplication.instance().installEventFilter(self.activity_filter)

    def switch_screen(self, index):
        self.stack.setCurrentIndex(index)
        if index == 7: self.screens[7].start_splash()
        if index == 2: self.screens[2].trigger_death()

# --- APPLICATION LAUNCH ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(CORPORATE_THEME)
    os_kernel = RedQueenOS()
    sys.exit(app.exec())
