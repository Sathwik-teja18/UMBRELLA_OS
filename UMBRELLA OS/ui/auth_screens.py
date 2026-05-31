import os
import sys
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QFormLayout, 
                             QLineEdit, QPushButton, QApplication, QGraphicsOpacityEffect, 
                             QProgressBar, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QPixmap

from settings import ASSETS
from core.database import load_database, save_database
from core.biometrics import capture_face

# --- SAFE IMPORTS FOR OPTIONAL MODULES ---
try:
    from core.RedQueenPuzzles import PuzzleManager
    PUZZLES_ENABLED = True
except ImportError:
    PUZZLES_ENABLED = False

try:
    from deepface import DeepFace
    DEEPFACE_ENABLED = True
except ImportError:
    DEEPFACE_ENABLED = False

class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.auth_container = QFrame()
        self.auth_container.setStyleSheet("""
            QFrame { background-color: rgba(17, 20, 23, 0.85); border: 1px solid #2A363B; border-top: 3px solid #C41E3A; border-radius: 4px; padding: 30px; }
        """)
        container_layout = QVBoxLayout(self.auth_container)
        
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            logo_pixmap = QPixmap(ASSETS["logo"]).scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(logo_pixmap)
        except Exception:
            self.logo_label.setText("[ UMBRELLA CORPORATION ]")
            self.logo_label.setStyleSheet("color: #C41E3A; font-size: 24px; font-weight: bold; background: transparent; border: none;")
            
        container_layout.addWidget(self.logo_label)

        title = QLabel("HIGH-FIDELITY AUTHENTICATION")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; letter-spacing: 4px; font-family: 'Arial'; color: #FFFFFF; background: transparent; border: none;")
        container_layout.addWidget(title)
        
        container_layout.addSpacing(20) 

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        input_style = "background-color: #0A0D0F; color: #FFFFFF; border: 1px solid #5C7680; font-family: 'Courier New'; font-size: 14px; padding: 8px; letter-spacing: 1px;"
        
        self.emp_id_input = QLineEdit()
        self.emp_id_input.setFixedWidth(350)
        self.emp_id_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(350)
        self.password_input.setStyleSheet(input_style)
        self.security_key_input = QLineEdit()
        self.security_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.security_key_input.setFixedWidth(350)
        self.security_key_input.setStyleSheet(input_style)

        lbl_style = "font-size: 14px; font-family: 'Arial'; font-weight: bold; color: #A0B0B5; background: transparent; border: none;"
        lbl1, lbl2, lbl3 = QLabel("IDENTIFIER"), QLabel("ACCESS CODE"), QLabel("SECURITY KEY")
        for lbl in [lbl1, lbl2, lbl3]: lbl.setStyleSheet(lbl_style)

        form_layout.addRow(lbl1, self.emp_id_input)
        form_layout.addRow(lbl2, self.password_input)
        form_layout.addRow(lbl3, self.security_key_input)
        container_layout.addLayout(form_layout)

        container_layout.addSpacing(15)

        self.enter_btn = QPushButton("INITIALIZE CONNECTION")
        self.enter_btn.setFixedWidth(350)
        self.enter_btn.setStyleSheet("""
            QPushButton { background-color: #C41E3A; color: #FFFFFF; border: none; font-family: 'Arial'; font-size: 14px; font-weight: bold; padding: 12px; letter-spacing: 2px; }
            QPushButton:hover { background-color: #E82946; }
            QPushButton:pressed { background-color: #8A0303; }
        """)
        self.enter_btn.clicked.connect(self.verify_credentials) 
        container_layout.addWidget(self.enter_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #FF0000; font-family: 'Courier New'; font-weight: bold; font-size: 14px; background: transparent; border: none;")
        container_layout.addWidget(self.status_label)
        
        layout.addWidget(self.auth_container)
        self.setLayout(layout)

    def verify_credentials(self):
        emp_id = self.emp_id_input.text().strip().upper()
        pwd = self.password_input.text().strip()
        sec_key = self.security_key_input.text().strip()
        
        self.status_label.setStyleSheet("color: #FF0000; font-family: 'Courier New'; font-weight: bold; font-size: 14px; background: transparent; border: none;")
        
        # TIER 1: OWNER ACCESS
        if emp_id in ["SATHWIK", "OWNER"] and pwd == "PROJECTHAILMARY":
            self.status_label.setText(">> OWNER RECOGNIZED. WELCOME BACK.")
            self.status_label.setStyleSheet("color: #5BC0BE; font-family: 'Courier New'; font-weight: bold; font-size: 14px; background: transparent; border: none;")
            QApplication.processEvents()
            self.main_window.switch_screen(5)
            if hasattr(self.main_window.screens[5], 'file_explorer'):
                self.main_window.screens[5].file_explorer.header.setText(">> DIRECTOR OVERRIDE ACCEPTED. JARVIS ONLINE.")
                self.main_window.screens[5].file_explorer.header.setStyleSheet("color: #5BC0BE; font-family: 'Courier New', monospace; font-size: 16px; font-weight: bold;")
            self.clear_inputs()
            return

        # TIER 2: ADMIN ACCESS
        elif emp_id == "UMB-ADMIN" and pwd == "REDQUEEN":
            if sec_key == "7680":
                self.status_label.setText(">> ADMIN CREDENTIALS VERIFIED. INITIATING OVERRIDE.")
                QApplication.processEvents()
                self.main_window.switch_screen(6)
                self.main_window.screens[6].start_override()
                self.clear_inputs()
                return
            else:
                self.trigger_lockdown("INVALID ADMIN SECURITY KEY")
                return

        # TIER 3: EMPLOYEE ACCESS
        if not emp_id:
            self.main_window.switch_screen(2) 
            return
            
        db = load_database()
        
        if emp_id in db and db[emp_id]["password"] == pwd:
            if db[emp_id].get("security_key") != sec_key:
                self.trigger_lockdown("INVALID SECURITY KEY")
                return
                
            self.status_label.setText(">> CREDENTIALS ACCEPTED. INITIATING OPTICS...")
            self.status_label.setStyleSheet("color: #E0E0E0;")
            QApplication.processEvents() 
            
            live_scan_path = capture_face(f"login_attempt_{emp_id}")
            if live_scan_path and DEEPFACE_ENABLED:
                try:
                    self.status_label.setText(">> RUNNING DEEP NEURAL VERIFICATION...")
                    QApplication.processEvents()
                    
                    saved_img_path = db[emp_id]["face_img_path"]
                    result = DeepFace.verify(img1_path=saved_img_path, img2_path=live_scan_path, enforce_detection=False)
                    if os.path.exists(live_scan_path): os.remove(live_scan_path)
                    
                    if result["verified"]:
                        self.status_label.setText(f">> BIOMETRIC MATCH: {db[emp_id]['name']}\n>> STANDARD ACCESS GRANTED.")
                        self.status_label.setStyleSheet("color: #00FF00;")
                        QTimer.singleShot(1000, lambda: self.main_window.switch_screen(5))
                        self.clear_inputs()
                        return
                    else:
                        self.trigger_lockdown("BIOMETRIC MISMATCH")
                        return
                except Exception:
                    self.trigger_lockdown("NEURAL NETWORK FAILURE")
                    return
            else:
                self.trigger_lockdown("NO VISUAL DATA ACQUIRED")
                return
                
        self.trigger_lockdown("UNAUTHORIZED ENTITY DETECTED")

    def trigger_lockdown(self, reason):
        self.status_label.setText(f">> ERROR: {reason}.\n>> LOCKDOWN PROTOCOL INITIATED.")
        QApplication.processEvents()
        QTimer.singleShot(1200, self.execute_lockdown)

    def execute_lockdown(self):
        self.main_window.switch_screen(3)
        self.main_window.screens[3].start_lockdown()
        self.clear_inputs()
        
    def clear_inputs(self):
        self.emp_id_input.clear()
        self.password_input.clear()
        self.security_key_input.clear()
        self.status_label.setText("")

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
        self.puzzle_container = QWidget()
        self.puzzle_layout = QVBoxLayout(self.puzzle_container)
        self.layout.addWidget(self.puzzle_container)
        self.required_solves = 2 
        self.current_solves = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_lockdown(self):
        self.time_left = 60
        self.current_solves = 0
        self.timer.start(1000)
        self.load_next_puzzle()

    def load_next_puzzle(self):
        for i in reversed(range(self.puzzle_layout.count())): 
            widget = self.puzzle_layout.itemAt(i).widget()
            if widget is not None: widget.deleteLater()
        if PUZZLES_ENABLED:
            self.active_puzzle = PuzzleManager.get_random_puzzle()
            self.active_puzzle.solved.connect(self.puzzle_completed)
            self.puzzle_layout.addWidget(self.active_puzzle)
        else:
            lbl = QLabel(">> ERROR: PUZZLE ENGINE NOT FOUND.\n>> SECURITY LATTICE BYPASSED.")
            lbl.setStyleSheet("color: red; font-size: 20px; font-weight:bold;")
            self.puzzle_layout.addWidget(lbl)
            QTimer.singleShot(2000, self.puzzle_completed)

    def puzzle_completed(self):
        self.current_solves += 1
        if self.current_solves >= self.required_solves:
            self.timer.stop()
            self.main_window.switch_screen(4) 
        else: self.load_next_puzzle()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"TIME UNTIL NEURO-TOXIN: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.main_window.switch_screen(2)

class OverrideScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QWidget { background-color: #050A05; border: 4px solid #00FF00; }")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel(">> INITIATING ALPHA OVERRIDE...")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; color: #00FF00; font-family: 'Courier New', monospace; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFixedSize(700, 350)
        self.console.setStyleSheet("background-color: #000000; color: #00FF00; border: 1px solid #00FF00; font-family: 'Courier New'; font-size: 16px;")
        self.layout.addWidget(self.console, alignment=Qt.AlignmentFlag.AlignCenter)
        self.progress = QProgressBar()
        self.progress.setFixedSize(700, 35)
        self.progress.setStyleSheet("QProgressBar { border: 2px solid #00FF00; background: #000000; text-align: center; color: #FFF; font-weight: bold; } QProgressBar::chunk { background-color: #00FF00; }")
        self.layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_sequence)

    def start_override(self):
        self.console.clear()
        self.progress.setValue(0)
        self.step = 0
        self.logs = [
            "VERIFYING MASTER ADMINISTRATOR CREDENTIALS...", "BYPASSING NEST ENCRYPTION LATTICE...",
            "DISABLING NEURO-TOXIN DEFENSE GRID...", "REROUTING MAINFRAME POWER...",
            "DECRYPTING RED QUEEN CORE LOGIC...", "GRANTING ROOT ACCESS..."
        ]
        self.timer.start(600) 

    def run_sequence(self):
        if self.step < len(self.logs):
            self.console.append(f">> {self.logs[self.step]}")
            for _ in range(3):
                hex_str = " ".join([f"0x{random.randint(10, 99)}" for _ in range(12)])
                self.console.append(f"   {hex_str}")
            self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())
            self.progress.setValue(int(((self.step + 1) / len(self.logs)) * 100))
            self.step += 1
        else:
            self.timer.stop()
            self.console.append("\n" + "="*45)
            self.console.append(">> WELCOME, ADMINISTRATOR SATHWIK.")
            self.console.append("="*45)
            self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())
            QTimer.singleShot(1500, self.unlock_system)

    def unlock_system(self):
        self.main_window.switch_screen(5) 

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
        QTimer.singleShot(2000, self.show_blood_splash)

    def show_blood_splash(self):
        try:
            pixmap = QPixmap(ASSETS["blood_splash"]).scaled(1920, 1080, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(pixmap)
        except Exception:
            self.label.setText(">> FATAL TOXICITY <<")
            self.label.setStyleSheet("color: #8A0303; font-family: 'Impact'; font-size: 100px;")
        self.opacity_effect.setOpacity(1.0)
        QTimer.singleShot(300, self.fade_in_death)

    def fade_in_death(self):
        try:
            pixmap = QPixmap(ASSETS["death_screen"]).scaled(800, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(pixmap)
        except Exception:
            self.label.setText("YOU ARE DEAD")
            self.label.setStyleSheet("color: #8A0303; font-family: 'Times New Roman', serif; font-size: 80px; font-weight: bold;")
        self.opacity_effect.setOpacity(0.0)
        self.anim_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_in.setDuration(3000) 
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.finished.connect(self.exit_system)
        self.anim_in.start()

    def exit_system(self): QTimer.singleShot(3000, sys.exit)

class RegistrationScreen(QWidget):
    # Keeping this simple for brevity in the master layout
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header = QLabel(">> NEST REGISTRATION COMPLETE. RETURN TO LOGIN.")
        header.setStyleSheet("font-size: 25px; font-weight: bold; color: #5BC0BE;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)
        btn = QPushButton("[ BACK TO LOGIN ]")
        btn.clicked.connect(lambda: self.main_window.switch_screen(1))
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)