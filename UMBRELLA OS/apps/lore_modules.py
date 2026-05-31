import math
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QTextEdit, QScrollArea, QGridLayout, QTabWidget)
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
# ==========================================
# 1. BIO-WEAPON DATA (EXPANDED LORE)
# ==========================================
VIRUS_DB = {
    # --- UMBRELLA SYNTHETICS ---
    "PROGENITOR": { 
        "color": "#FF0000", 
        "status": "[ RESTRICTED ]", 
        "data": ">> DESIGNATION: PROGENITOR VIRUS\n>> DISCOVERY: 1966, Ndipaya Ruins, West Africa\n>> BASE: Sonnentreppe Flower\n\n>> HISTORICAL ARCHIVE:\nDiscovered by Oswell E. Spencer, James Marcus, and Edward Ashford. The virus originates from the 'Stairway of the Sun' flower, once used in ancient Ndipaya tribal rituals to select their kings. It became the foundation of Umbrella Pharmaceuticals.\n\n>> CLINICAL ANALYSIS:\nThe foundational RNA virus of all Umbrella research. It possesses the unique ability to violently rewrite the DNA of infected hosts. However, the mortality rate is exceptionally high, and it fails to yield stable Bio-Organic Weapons (B.O.W.s) due to rapid, unpredictable mutations and total host rejection." 
    },
    "T-VIRUS": { 
        "color": "#00FF00", 
        "status": "[ ACTIVE ]", 
        "data": ">> DESIGNATION: TYRANT VIRUS (T-VIRUS)\n>> ARCHITECT: Dr. James Marcus / Dr. William Birkin\n>> BASE: Progenitor + Leech DNA\n\n>> HISTORICAL ARCHIVE:\nDeveloped at the Arklay Laboratory to create the perfect bio-organic soldier. The 'Epsilon' strain successfully yielded the Tyrant (T-002) model, paving the way for mass B.O.W. production.\n\n>> CLINICAL ANALYSIS:\nInduces catastrophic cellular necrosis followed by rapid, unregulated tissue regeneration. The resulting brain damage causes severe cognitive decay, reducing the host to primal feeding instincts. Secondary infection vectors via fluid transfer (bites, scratches) are highly volatile, making it an exceptional area-denial agent. Continued cellular mutations yield 'Lickers' and 'Hunters'." 
    },
    "G-VIRUS": { 
        "color": "#800080", 
        "status": "[ CRITICAL ]", 
        "data": ">> DESIGNATION: GOLGOTHA VIRUS (G-VIRUS)\n>> ARCHITECT: Dr. William Birkin\n>> BASE: Progenitor + NE-α Parasite Anomaly\n\n>> HISTORICAL ARCHIVE:\nDiscovered after test subject Lisa Trevor successfully absorbed and neutralized a Nemesis Alpha parasite. Birkin extracted the resulting anomaly, creating a virus meant to entirely surpass the Tyrant project.\n\n>> CLINICAL ANALYSIS:\nUnlike the T-Virus, 'G' forces the host into continuous, aggressive evolutionary cycles to instantly adapt to physical trauma. Mutations are highly asymmetrical, resulting in massive increases in bone density, muscle mass, and the manifestation of large external ocular organs. The virus compels the host to reproduce by implanting embryos in genetically related targets." 
    },
    "UROBOROS": { 
        "color": "#FFD700", 
        "status": "[ ERADICATED ]", 
        "data": ">> DESIGNATION: UROBOROS VIRUS\n>> ARCHITECT: Albert Wesker\n>> BASE: Progenitor + Las Plagas + T-Virus Antibodies\n\n>> HISTORICAL ARCHIVE:\nDesigned as a forced evolutionary catalyst to cull humanity. Initial strains were too aggressive and lethal, requiring the introduction of rare T-Virus antibodies to stabilize the mutagenic process.\n\n>> CLINICAL ANALYSIS:\nRejects 99% of hosts, turning them into chaotic masses of black, leech-like pustules that violently consume organic matter to grow. Those with perfectly compatible DNA who successfully assimilate the virus gain god-like physical augmentation, enhanced durability, and superhuman speed." 
    },
    
    # --- REAL-WORLD PATHOGENS ---
    "EBOLA (ZAIRE)": { 
        "color": "#8B0000", 
        "status": "[ BSL-4 / ACTIVE ]", 
        "data": ">> DESIGNATION: ZAIRE EBOLAVIRUS\n>> DISCOVERY: 1976, Yambuku, Zaire\n>> BASE: Filoviridae Family (Natural)\n\n>> HISTORICAL ARCHIVE:\nFirst identified near the Ebola River. Outbreaks typically occur in remote villages in Central and West Africa, triggering massive international quarantine responses.\n\n>> CLINICAL ANALYSIS:\nAn extremely virulent hemorrhagic fever. The virus systematically disables the host's immune response while causing severe coagulation abnormalities. This leads to massive internal and external hemorrhaging, culminating in multi-organ failure and hypovolemic shock. Mortality rates can reach up to 90% without intensive supportive care." 
    },
    "RABIES": { 
        "color": "#FF8C00", 
        "status": "[ ENDEMIC ]", 
        "data": ">> DESIGNATION: RABIES LYSSAVIRUS\n>> DISCOVERY: Antiquity (Vaccine: 1885)\n>> BASE: Rhabdoviridae Family (Natural)\n\n>> HISTORICAL ARCHIVE:\nRecognized since antiquity as a fatal affliction transmitted by animal bites. Louis Pasteur developed the first viable vaccine in the late 19th century.\n\n>> CLINICAL ANALYSIS:\nA neurotropic virus that spreads via peripheral nerves directly to the central nervous system. Once clinical symptoms appear, it is nearly 100% fatal. It induces acute encephalitis, resulting in extreme aggression, hallucinations, paralysis, and hydrophobia. The pathogen's ability to hijack host behavior makes it a subject of extensive neurological study." 
    },
    "VARIOLA MAJOR": { 
        "color": "#A0B0B5", 
        "status": "[ VAULTED ]", 
        "data": ">> DESIGNATION: VARIOLA MAJOR (SMALLPOX)\n>> DISCOVERY: Unknown (Earliest evidence: 3rd Century BCE)\n>> BASE: Poxviridae Family (Natural)\n\n>> HISTORICAL ARCHIVE:\nOne of the most devastating diseases in human history, responsible for hundreds of millions of deaths. Following a global immunization campaign, the WHO declared it officially eradicated in 1980.\n\n>> CLINICAL ANALYSIS:\nA highly contagious airborne pathogen. It causes systemic toxemia and characteristic macroscopic skin lesions (maculopapular rash) that evolve into fluid-filled pustules. Surviving hosts are often left with extensive scarring or blindness. Maintained only in heavily restricted BSL-4 secure repositories." 
    },
    "MARBURG": { 
        "color": "#B22222", 
        "status": "[ BSL-4 / ACTIVE ]", 
        "data": ">> DESIGNATION: MARBURGVIRUS\n>> DISCOVERY: 1967, Marburg, Germany\n>> BASE: Filoviridae Family (Natural)\n\n>> HISTORICAL ARCHIVE:\nFirst documented during simultaneous outbreaks in laboratories in Germany and Yugoslavia. The initial transmission was traced back to infected African green monkeys imported for research.\n\n>> CLINICAL ANALYSIS:\nClinically similar to Ebola but antigenically distinct. It induces severe viral hemorrhagic fever. Symptoms rapidly progress to severe weight loss, jaundice, pancreatitis, and catastrophic internal bleeding. The extreme lethality and fluid transmission vectors mandate the highest levels of containment." 
    }
}
# ==========================================
# 2. DEMONIC DATA (DEVIL MAY CRY)
# ==========================================
DEMON_DB = {
    "EMPUSA": { "color": "#9ACD32", "status": "[ SCAVENGER ]", "data": ">> ENTITY: EMPUSA\n>> CLASS: Lesser Demon\n>> ORIGIN: Qliphoth Roots\n\n>> ANALYSIS:\nWorker-caste demon. Absorbs human blood to nourish the Qliphoth tree. Fragile but highly evasive. Its abdomen swells with hematological fluid." },
    "HELL CAINA": { "color": "#8A2BE2", "status": "[ SOLDIER ]", "data": ">> ENTITY: HELL CAINA\n>> CLASS: Vanguard\n>> ORIGIN: Underworld Depths\n\n>> ANALYSIS:\nManifests wielding a heavy bone scythe. Slow, rhythmic attack patterns. Represents the standard infantry of the demonic invasion." },
    "FURY": { "color": "#FF0000", "status": "[ PREDATOR ]", "data": ">> ENTITY: FURY\n>> CLASS: Apex Hunter\n>> ORIGIN: Mutated Chaos\n\n>> ANALYSIS:\nUtilizes raw demonic power to perform micro-warps through space-time, appearing as a blur of red light. Highly aggressive. Requires advanced tactical evasion." },
    "BEHEMOTH": { "color": "#B8860B", "status": "[ JUGGERNAUT ]", "data": ">> ENTITY: BEHEMOTH\n>> CLASS: Heavy Siege\n>> ORIGIN: Tartarus Block\n\n>> ANALYSIS:\nA massive, blind demon encased in heavy restraints. Attacks blindly with devastating physical force. Severing its chains triggers a hyper-aggressive berserk state." }
}

# ==========================================
# UI WIDGETS & VISUALIZERS
# ==========================================
class DNAVisualizer(QWidget):
    """Renders a pseudo-3D rotating double helix."""
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 400)
        self.angle = 0.0
        self.helix_color = QColor("#FF0000")
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(30)

    def set_color(self, hex_color):
        self.helix_color = QColor(hex_color)

    def rotate(self):
        self.angle += 0.08
        if self.angle >= math.pi * 2: self.angle = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center_x = self.width() / 2
        amplitude = 60
        spacing = 20
        num_nodes = int(self.height() / spacing)
        
        for i in range(num_nodes):
            y = i * spacing
            phase_offset = i * 0.4
            x1 = center_x + math.sin(self.angle + phase_offset) * amplitude
            x2 = center_x + math.sin(self.angle + phase_offset + math.pi) * amplitude
            z1 = math.cos(self.angle + phase_offset)
            z2 = math.cos(self.angle + phase_offset + math.pi)
            
            painter.setPen(QPen(QColor(50, 50, 50), 2))
            painter.drawLine(int(x1), int(y), int(x2), int(y))
            
            if z1 < 0:
                self.draw_node(painter, x1, y, z1)
                self.draw_node(painter, x2, y, z2)
            else:
                self.draw_node(painter, x2, y, z2)
                self.draw_node(painter, x1, y, z1)
        painter.end()

    def draw_node(self, painter, x, y, z):
        radius = 5 + (z * 2)
        opacity = 150 + int(z * 105)
        color = QColor(self.helix_color)
        color.setAlpha(opacity)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(x - radius), int(y - radius), int(radius * 2), int(radius * 2))

class PortalVisualizer(QWidget):
    """Renders a breathing dimensional rift (Vergil Yamato style)."""
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 400)
        self.tick = 0.0
        self.portal_color = QColor("#00FFFF")
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def set_color(self, hex_color):
        self.portal_color = QColor(hex_color)

    def animate(self):
        self.tick += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2
        tear_width = 12 + math.sin(self.tick) * 6 # Breathe effect
        tear_height = 280
        
        painter.translate(cx, cy)
        painter.rotate(35) # Diagonal cut
        
        # Outer Aura Glow
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(6, 0, -1):
            c = QColor(self.portal_color)
            c.setAlpha(25 * i)
            painter.setBrush(QBrush(c))
            painter.drawEllipse(int(-tear_width*i), int(-tear_height/2 - 10*i), int(tear_width*2*i), int(tear_height + 20*i))
        
        # Inner Void
        painter.setBrush(QBrush(QColor("#020202")))
        painter.drawEllipse(int(-tear_width), int(-tear_height/2), int(tear_width*2), tear_height)
        
        # Spatial Tear & Cracks
        painter.setPen(QPen(QColor("#FFFFFF"), 2))
        painter.drawLine(0, int(-tear_height/2 - 15), 0, int(tear_height/2 + 15))
        
        painter.setPen(QPen(QColor(self.portal_color), 1))
        painter.drawLine(0, 0, 40, 20)
        painter.drawLine(0, -50, -30, -10)
        painter.drawLine(0, 80, -40, 100)
        painter.end()


class DataSlot(QFrame):
    """Clickable UI slot for the selection grids."""
    clicked = pyqtSignal(str)
    def __init__(self, name, status, color):
        super().__init__()
        self.entry_name = name
        self.setFixedSize(180, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"QFrame {{ background-color: #0A0A0A; border: 2px solid #1A1A1A; border-radius: 5px; }} QFrame:hover {{ border: 2px solid {color}; background-color: #111111; }}")
        
        layout = QVBoxLayout()
        lbl_icon = QLabel("☣" if "VIRUS" in status or "RESTRICTED" in status or "ACTIVE" in status else "⸎")
        lbl_icon.setStyleSheet(f"color: {color}; font-size: 36px; border: none; background: transparent;")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_name = QLabel(name)
        lbl_name.setStyleSheet("color: #FFFFFF; font-family: 'Arial'; font-weight: bold; font-size: 14px; border: none; background: transparent;")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_status = QLabel(status)
        lbl_status.setStyleSheet("color: #A0B0B5; font-family: 'Courier New'; font-size: 11px; border: none; background: transparent;")
        lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_name)
        layout.addWidget(lbl_status)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.entry_name)
            self.setStyleSheet(f"QFrame {{ background-color: #C41E3A; border: 2px solid #FF0000; border-radius: 5px; }}")
            QTimer.singleShot(100, lambda: self.setStyleSheet(f"QFrame {{ background-color: #0A0A0A; border: 2px solid #1A1A1A; border-radius: 5px; }} QFrame:hover {{ border: 2px solid #C41E3A; background-color: #111111; }}"))

class DatabaseTab(QWidget):
    """Generic tab to hold either viruses or demons."""
    def __init__(self, header_text, db_data, VisualizerClass):
        super().__init__()
        self.db_data = db_data
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Panel (Grid)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        header = QLabel(header_text)
        header.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 16px; font-weight: bold;")
        left_layout.addWidget(header)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #050505; }")
        grid_widget = QWidget()
        self.grid_layout = QGridLayout(grid_widget)
        self.grid_layout.setSpacing(15)
        
        row, col = 0, 0
        for name, data in self.db_data.items():
            slot = DataSlot(name, data["status"], data["color"])
            slot.clicked.connect(self.load_data)
            self.grid_layout.addWidget(slot, row, col)
            col += 1
            if col > 1: col, row = 0, row + 1
                
        scroll_area.setWidget(grid_widget)
        left_layout.addWidget(scroll_area)
        
        # Right Panel (Text & Visualizer)
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #0A0A0A; border-left: 2px solid #1A1A1A;")
        right_layout = QHBoxLayout(right_panel)
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("background-color: transparent; color: #A0B0B5; font-family: 'Courier New'; font-size: 14px; border: none; padding: 20px;")
        
        self.visualizer = VisualizerClass()
        right_layout.addWidget(self.text_display, stretch=2)
        right_layout.addWidget(self.visualizer, stretch=1)
        
        layout.addWidget(left_panel, stretch=1)
        layout.addWidget(right_panel, stretch=1)
        
        # Typewriter Animation variables
        self.target_text = ""
        self.current_char_index = 0
        self.scramble_ticks = 0
        self.typewriter_timer = QTimer()
        self.typewriter_timer.timeout.connect(self.animate_text)
        
        self.load_data(list(self.db_data.keys())[0])

    def load_data(self, item_name):
        data = self.db_data[item_name]
        self.visualizer.set_color(data["color"])
        self.target_text = data["data"]
        self.current_char_index = 0
        self.scramble_ticks = 0
        self.text_display.clear()
        self.typewriter_timer.start(15) 

    def animate_text(self):
        if self.scramble_ticks < 15:
            scrambled = "".join(random.choice("0123456789ABCDEF!@#$%^&*") for _ in range(200))
            self.text_display.setText(f">> DECRYPTING MAINFRAME ARCHIVE...\n\n{scrambled}")
            self.scramble_ticks += 1
        else:
            if self.current_char_index <= len(self.target_text):
                cursor = "█" if self.current_char_index % 2 == 0 else ""
                current_reveal = self.target_text[:self.current_char_index]
                self.text_display.setText(current_reveal + cursor)
                self.current_char_index += 1
            else:
                self.text_display.setText(self.target_text)
                self.typewriter_timer.stop()

# ==========================================
# MAIN APPLICATION MODULE
# ==========================================
class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #050505; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #1A1A1A; top: -1px; }
            QTabBar::tab { background: #0A0A0A; color: #708085; padding: 10px 20px; border: 1px solid #1A1A1A; font-family: 'Courier New'; font-weight: bold; }
            QTabBar::tab:selected { background: #111111; color: #C41E3A; border-bottom-color: #111111; }
        """)
        
        self.virus_tab = DatabaseTab(">> BIO-CONTAINMENT COLD STORAGE", VIRUS_DB, DNAVisualizer)
        self.demon_tab = DatabaseTab(">> DEMONIC ENTITY ARCHIVE", DEMON_DB, PortalVisualizer)

        self.tabs.addTab(self.virus_tab, "[ BIO-WEAPONS ]")
        self.tabs.addTab(self.demon_tab, "[ EXTRADIMENSIONAL ]")
        
        layout.addWidget(self.tabs)

# ==========================================
# PENDING MODULES (STANDBY MODE)
# ==========================================
class RunicVaultApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #050505;")
        layout = QVBoxLayout()
        lbl = QLabel(">> COLD STORAGE VAULT SECURE.\n>> AWAITING JARVIS AUTHORIZATION DECRYPT.")
        lbl.setStyleSheet("color: #A0B0B5; font-family: 'Courier New'; font-size: 14px;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        self.setLayout(layout)

class IncineratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #050505;")
        layout = QVBoxLayout()
        lbl = QLabel(">> THERMAL INCINERATOR STANDBY.\n>> READY FOR PURGE SEQUENCE.")
        # Make sure this next line ends with a double quote and a parenthesis!
        lbl.setStyleSheet("color: #C41E3A; font-family: 'Courier New'; font-size: 14px;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
        self.setLayout(layout)