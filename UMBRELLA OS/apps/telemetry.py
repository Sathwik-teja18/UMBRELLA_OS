import math
import random
import psutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QTextEdit, QProgressBar, QGridLayout)
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter, QConicalGradient
from PyQt6.QtCore import Qt, QTimer

# ==========================================
# CENTER: GLOBAL THREAT RADAR
# ==========================================
class ThreatRadar(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(350, 350)
        self.angle = 0
        self.blips = [] # Stores active threats: [x, y, radius, opacity, color]
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.scan)
        self.timer.start(30) # Radar rotation speed

    def scan(self):
        self.angle = (self.angle - 3) % 360 # Sweep counter-clockwise
        
        # Randomly spawn new threats
        if random.randint(1, 100) > 95:
            distance = random.uniform(20, 140)
            theta = random.uniform(0, math.pi * 2)
            cx, cy = self.width() / 2, self.height() / 2
            bx = cx + distance * math.cos(theta)
            by = cy + distance * math.sin(theta)
            color = "#FF0000" if random.randint(1, 10) > 2 else "#FFD700" # Red or Yellow threat
            self.blips.append([bx, by, 0, 255, color])
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx, cy = self.width() / 2, self.height() / 2
        radius = min(cx, cy) - 20
        
        # Draw Base Grid
        painter.setPen(QPen(QColor(196, 30, 58, 80), 1))
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2))
        painter.drawEllipse(int(cx - radius/2), int(cy - radius/2), int(radius), int(radius))
        painter.drawLine(int(cx), int(cy - radius), int(cx), int(cy + radius))
        painter.drawLine(int(cx - radius), int(cy), int(cx + radius), int(cy))
        
        # Draw Radar Sweep Gradient
        gradient = QConicalGradient(cx, cy, self.angle)
        gradient.setColorAt(0, QColor(196, 30, 58, 150)) # Bright Red leading edge
        gradient.setColorAt(0.1, QColor(196, 30, 58, 0)) # Fades to transparent
        gradient.setColorAt(1, QColor(196, 30, 58, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPie(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2), self.angle * 16, 16 * 360)
        
        # Draw & Update Blips
        for blip in self.blips[:]:
            bx, by, b_rad, b_opacity, b_color = blip
            c = QColor(b_color)
            c.setAlpha(int(b_opacity))
            painter.setPen(QPen(c, 2))
            painter.drawEllipse(int(bx - b_rad), int(by - b_rad), int(b_rad * 2), int(b_rad * 2))
            
            # Expand and fade
            blip[2] += 0.5
            blip[3] -= 3
            if blip[3] <= 0:
                self.blips.remove(blip)
                
        painter.end()

# ==========================================
# MAIN COMMAND CENTER APP
# ==========================================
class ApexDiagnosticsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #050505; color: #FFFFFF; }")
        
        main_layout = QHBoxLayout(self)
        
        # ------------------------------------------
        # PANEL 1: HARDWARE REACTOR (Left)
        # ------------------------------------------
        hw_panel = QFrame()
        hw_panel.setStyleSheet("border-right: 1px solid #1A1A1A;")
        hw_layout = QVBoxLayout(hw_panel)
        
        hw_header = QLabel(">> LOCAL HARDWARE UPLINK")
        hw_header.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 14px; font-weight: bold; border: none;")
        hw_layout.addWidget(hw_header)
        
        # CPU Monitor
        self.cpu_lbl = QLabel("CPU LOAD: 0%")
        self.cpu_lbl.setStyleSheet("font-family: 'Courier New'; color: #A0B0B5; border: none;")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet("QProgressBar { border: 1px solid #1A1A1A; background-color: #0A0A0A; } QProgressBar::chunk { background-color: #C41E3A; }")
        self.cpu_bar.setTextVisible(False)
        hw_layout.addWidget(self.cpu_lbl)
        hw_layout.addWidget(self.cpu_bar)
        
        # RAM Monitor
        self.ram_lbl = QLabel("RAM USAGE: 0%")
        self.ram_lbl.setStyleSheet("font-family: 'Courier New'; color: #A0B0B5; border: none;")
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet("QProgressBar { border: 1px solid #1A1A1A; background-color: #0A0A0A; } QProgressBar::chunk { background-color: #C41E3A; }")
        self.ram_bar.setTextVisible(False)
        hw_layout.addWidget(self.ram_lbl)
        hw_layout.addWidget(self.ram_bar)
        
        hw_layout.addStretch()
        
        # ------------------------------------------
        # PANEL 2: THREAT RADAR (Center)
        # ------------------------------------------
        radar_panel = QVBoxLayout()
        radar_header = QLabel(">> GLOBAL OUTBREAK RADAR")
        radar_header.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 14px; font-weight: bold; border: none;")
        radar_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.radar = ThreatRadar()
        
        radar_panel.addWidget(radar_header)
        radar_panel.addWidget(self.radar)
        radar_panel.addStretch()
        
        # ------------------------------------------
        # PANEL 3: JARVIS UPLINK (Right)
        # ------------------------------------------
        jarvis_panel = QFrame()
        jarvis_panel.setStyleSheet("border-left: 1px solid #1A1A1A;")
        jarvis_layout = QVBoxLayout(jarvis_panel)
        
        j_header = QLabel(">> JARVIS NEURAL UPLINK")
        j_header.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 14px; font-weight: bold; border: none;")
        jarvis_layout.addWidget(j_header)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #0A0A0A; color: #A0B0B5; font-family: 'Courier New'; font-size: 11px; border: 1px solid #1A1A1A;")
        jarvis_layout.addWidget(self.terminal)
        
        # ------------------------------------------
        # ASSEMBLE PANELS
        # ------------------------------------------
        main_layout.addWidget(hw_panel, stretch=1)
        main_layout.addLayout(radar_panel, stretch=2)
        main_layout.addWidget(jarvis_panel, stretch=1)
        
        # Start Master Timers
        self.hw_timer = QTimer()
        self.hw_timer.timeout.connect(self.update_hardware)
        self.hw_timer.start(1000) # Update PC stats every 1 second
        
        self.j_timer = QTimer()
        self.j_timer.timeout.connect(self.jarvis_log)
        self.j_timer.start(800) # Type a new log every 0.8 seconds
        
        self.jarvis_phrases = [
            "Encrypting datastream... OK",
            "Bypassing external firewalls...",
            "Ping received from Raccoon City server.",
            "Analyzing viral mutation rates...",
            "WARNING: Spontaneous T-Cell regeneration detected.",
            "Compiling B.O.W. field combat data...",
            "Routing neural pathways to NEST mainframe."
        ]

    def update_hardware(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.cpu_lbl.setText(f"CPU LOAD: {cpu}%")
        self.cpu_bar.setValue(int(cpu))
        self.ram_lbl.setText(f"RAM USAGE: {ram}%")
        self.ram_bar.setValue(int(ram))
        
        if ram > 85:
            self.ram_lbl.setStyleSheet("font-family: 'Courier New'; color: #FF0000; font-weight: bold; border: none;")
        else:
            self.ram_lbl.setStyleSheet("font-family: 'Courier New'; color: #A0B0B5; border: none;")

    def jarvis_log(self):
        phrase = random.choice(self.jarvis_phrases)
        hex_code = f"0x{random.randint(1000, 9999):04X}"
        self.terminal.append(f"[{hex_code}] {phrase}")
        self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())
        
# ==========================================
# ASTROPHAGE DAEMON (STANDBY MODULE)
# ==========================================

class AstrophageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #050505;")
        layout = QVBoxLayout()
        
        # Threat Header
        header = QLabel(">> ASTROPHAGE DAEMON: ACTIVE")
        header.setStyleSheet("color: #FFD700; font-family: 'Courier New'; font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Telemetry Output
        lbl = QLabel(
            ">> WARNING: LOCAL ENERGY CONSUMPTION EXPONENTIALLY INCREASING.\n"
            ">> ALLOCATING REMAINING SYSTEM RESOURCES TO PETROVA LINE CALIBRATION.\n"
            ">> AWAITING JARVIS OVERRIDE TO INITIATE CONTAINMENT PROTOCOL."
        )
        lbl.setStyleSheet("color: #A0B0B5; font-family: 'Courier New'; font-size: 14px; line-height: 1.5;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        
        self.setLayout(layout)