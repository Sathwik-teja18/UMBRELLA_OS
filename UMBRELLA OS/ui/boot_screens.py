import random
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt6.QtGui import QFont, QColor, QPixmap
from settings import ASSETS

class BiosScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #000000;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        # --- REVERTED TO MATRIX GREEN AND LARGE BOLD FONT ---
        self.terminal.setStyleSheet("background-color: #000000; color: #00FF00; font-family: 'Courier New'; font-size: 18px; font-weight: bold; border: none;")
        layout.addWidget(self.terminal)
        self.setLayout(layout)
        
        # --- RESTORED ORIGINAL COMPANY INTRO ---
        self.intro_sequence = [
            "UMBRELLA CORPORATION BIOS v7.2.4",
            "COPYRIGHT (C) 1968-2026 UMBRELLA INC.",
            "ALL RIGHTS RESERVED.",
            " ",
            ">> INITIALIZING RED QUEEN KERNEL...",
            ">> VERIFYING NEST FACILITY MAINFRAME...",
            ">> CHECKING MAIN MEMORY... 128TB OK",
            ">> MOUNTING SECURE DRIVES... OK",
            ">> LOADING EXTENDED SYSTEM MODULES...",
            " "
        ]
        
        # --- KEPT THE DETAILED MODULES ---
        self.boot_modules = [
            "Loading AI_DATA_ENGINEERING.sys",
            "Mounting OXFORD_SECURE_ARCHIVE",
            "Initializing ASTROPHYSICS_NUCLEUS",
            "Calibrating ORBITAL_TELESCOPE_ARRAY",
            "Bypassing CAMBRIDGE_PROTOCOLS",
            "Booting JARVIS Core Logic",
            "Loading GPU_TENSOR_CORES",
            "Initializing QUANTUM_MECHANICS_MODULE",
            "Verifying SYSTEM_MEMORY_MANAGEMENT",
            "Establishing UMBRELLA_UPLINK",
            "Decrypting BLACK_HOLE_SPECTROSCOPY_DATA",
            "Loading CuPy Computation Libraries",
            "Mounting NEST_LOCAL_DRIVE",
            "Compiling HAWKING_AREA_LAW_VECTORS"
        ]
        
        self.line_count = 0
        # Will print the intro, plus 25 lines of random detailed hex
        self.max_lines = len(self.intro_sequence) + 25 
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_line)

    def start_boot(self):
        """Called by main.py to manually trigger the sequence."""
        self.timer.start(150) # Sped up slightly so it feels aggressive

    def add_line(self):
        # Phase 1: Print the static company intro
        if self.line_count < len(self.intro_sequence):
            self.terminal.append(self.intro_sequence[self.line_count])
            
        # Phase 2: Finish and handover
        elif self.line_count >= self.max_lines:
            self.timer.stop()
            self.terminal.append("\n>> BIOS SEQUENCE COMPLETE. HANDING OVER TO MAIN KERNEL...")
            
            # --- THE FIX: Point the router to index 7 (Splash Screen) ---
            QTimer.singleShot(800, lambda: self.main_window.switch_screen(7))
            return
            
        # Phase 3: Print the randomized, long-form hex data
        else:
            # Made the hex addresses even longer and more detailed
            hex_addr1 = f"0x{random.randint(268435456, 4294967295):08X}"
            hex_addr2 = f"0x{random.randint(65536, 1048575):05X}"
            module = random.choice(self.boot_modules)
            
            line = f"[ OK ] {hex_addr1} : {module}... [ {hex_addr2} ]"
            self.terminal.append(line)
            
        self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())
        self.line_count += 1
        
class SplashScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout()
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        try:
            pixmap = QPixmap(ASSETS["splash_image"]).scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pixmap)
        except Exception:
            self.logo.setText("[ THE FUTURE IS VIRAL. 1968. UMBRELLA CORP. ]")
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