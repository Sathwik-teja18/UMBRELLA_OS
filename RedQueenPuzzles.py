import random
import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QHBoxLayout, QGridLayout, QProgressBar, QSlider)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer

class BasePuzzle(QWidget):
    """ The master template for all puzzles. Emits a signal when beaten. """
    solved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel { color: #00FF00; font-family: 'Courier New'; font-size: 16px; font-weight: bold; background: transparent; }
            QLineEdit { background-color: #000000; color: #00FF00; border: 2px solid #00FF00; font-size: 20px; padding: 5px; }
            QPushButton { background-color: #000000; color: #00FF00; border: 2px solid #00FF00; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #003300; }
            QTextEdit { background-color: #050505; color: #00FF00; border: 1px solid #004400; font-family: 'Courier New'; }
            QProgressBar { border: 2px solid #00FF00; background: #000000; text-align: center; color: #FFF; }
            QProgressBar::chunk { background-color: #00FF00; }
        """)

# ==========================================
# 1. CRYPTOGRAPHY: The Mastermind
# ==========================================
class MastermindPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.target_code = str(random.randint(1000, 9999))
        self.attempts_left = 6
        
        self.title = QLabel(">> ENCRYPTION LATTICE: BRUTE FORCE REQUIRED\n>> GUESS THE 4-DIGIT PIN.")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFixedHeight(150)
        self.layout.addWidget(self.history)
        
        self.input_field = QLineEdit()
        self.input_field.setMaxLength(4)
        self.input_field.returnPressed.connect(self.check_guess)
        self.layout.addWidget(self.input_field)

    def check_guess(self):
        guess = self.input_field.text().strip()
        if len(guess) != 4 or not guess.isdigit():
            self.input_field.clear()
            return
            
        self.attempts_left -= 1
        self.input_field.clear()
        
        if guess == self.target_code:
            self.history.append(f">> [{guess}] - ACCESS GRANTED.")
            self.input_field.setDisabled(True)
            self.solved.emit() 
        else:
            exact = sum(1 for i in range(4) if guess[i] == self.target_code[i])
            wrong_pos = sum(1 for c in set(guess) if c in self.target_code) - exact
            self.history.append(f">> [{guess}] - EXACT: {exact} | WRONG POS: {wrong_pos} | ATTEMPTS: {self.attempts_left}")
            if self.attempts_left <= 0:
                self.history.append(">> LOCKDOWN ENFORCED. SEQUENCE FAILED.")
                self.input_field.setDisabled(True)

# ==========================================
# 2. SPATIAL: Lights Out
# ==========================================
class LightsOutPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = QLabel(">> SECTOR POWER RELAY CORRUPTED.\n>> BALANCE THE GRID (ALL GREEN).")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        grid_widget = QWidget()
        self.grid = QGridLayout(grid_widget)
        self.buttons = {}
        
        for r in range(3):
            for c in range(3):
                btn = QPushButton()
                btn.setFixedSize(60, 60)
                state = random.choice([True, False]) 
                self.buttons[(r, c)] = {'btn': btn, 'state': state}
                self.update_btn_color(r, c)
                btn.clicked.connect(lambda checked, row=r, col=c: self.toggle_cross(row, col))
                self.grid.addWidget(btn, r, c)
                
        self.layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle_cross(self, r, c):
        coords = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for row, col in coords:
            if 0 <= row < 3 and 0 <= col < 3:
                self.buttons[(row, col)]['state'] = not self.buttons[(row, col)]['state']
                self.update_btn_color(row, col)
        self.check_win()

    def update_btn_color(self, r, c):
        color = "#00FF00" if self.buttons[(r, c)]['state'] else "#FF0000"
        self.buttons[(r, c)]['btn'].setStyleSheet(f"background-color: {color}; border: 2px solid #FFF;")

    def check_win(self):
        if all(data['state'] for data in self.buttons.values()):
            self.title.setText(">> RELAY STABILIZED.")
            for data in self.buttons.values(): data['btn'].setDisabled(True)
            self.solved.emit()

# ==========================================
# 3. BIO-CHEM: The Water Jug
# ==========================================
class WaterJugPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = QLabel(">> SYNTHESIZING T-VIRUS ANTISERUM.\n>> ISOLATE EXACTLY 400ml IN ANY VAT.")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.vats = [
            {'cap': 800, 'curr': 800, 'bar': QProgressBar()},
            {'cap': 500, 'curr': 0, 'bar': QProgressBar()},
            {'cap': 300, 'curr': 0, 'bar': QProgressBar()}
        ]
        
        vat_layout = QHBoxLayout()
        for i, vat in enumerate(self.vats):
            col = QVBoxLayout()
            vat['bar'].setOrientation(Qt.Orientation.Vertical)
            vat['bar'].setRange(0, vat['cap'])
            vat['bar'].setValue(vat['curr'])
            vat['bar'].setFixedSize(40, 150)
            
            lbl = QLabel(f"VAT {i+1}\n({vat['cap']}ml)")
            col.addWidget(vat['bar'], alignment=Qt.AlignmentFlag.AlignHCenter)
            col.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
            vat_layout.addLayout(col)
            
        self.layout.addLayout(vat_layout)
        
        btn_layout = QGridLayout()
        moves = [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
        for idx, (f, t) in enumerate(moves):
            btn = QPushButton(f"{f+1} -> {t+1}")
            btn.clicked.connect(lambda checked, frm=f, to=t: self.pour(frm, to))
            btn_layout.addWidget(btn, idx//3, idx%3)
            
        self.layout.addLayout(btn_layout)

    def pour(self, frm, to):
        source = self.vats[frm]
        target = self.vats[to]
        
        transfer_amount = min(source['curr'], target['cap'] - target['curr'])
        source['curr'] -= transfer_amount
        target['curr'] += transfer_amount
        
        source['bar'].setValue(source['curr'])
        target['bar'].setValue(target['curr'])
        
        if self.vats[0]['curr'] == 400 or self.vats[1]['curr'] == 400 or self.vats[2]['curr'] == 400:
            self.title.setText(">> ANTISERUM SYNTHESIZED.")
            self.solved.emit()

# ==========================================
# 4. CSE/MATH: Binary Decoder
# ==========================================
class BinaryDecoderPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.target_decimal = random.randint(50, 255)
        self.binary_str = format(self.target_decimal, '08b')
        
        self.title = QLabel(f">> MEMORY ALLOCATION FAULT.\n>> DECODE 8-BIT STRING TO DECIMAL:\n\n[ {self.binary_str} ]")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter Integer...")
        self.input_field.returnPressed.connect(self.check_val)
        self.layout.addWidget(self.input_field)

    def check_val(self):
        guess = self.input_field.text().strip()
        if guess == str(self.target_decimal):
            self.input_field.setStyleSheet("background-color: #003300;")
            self.input_field.setDisabled(True)
            self.solved.emit()
        else:
            self.input_field.clear()
            self.input_field.setPlaceholderText(">> INCORRECT")

# ==========================================
# 5. ASTROPHYSICS: Orbital Insertion Burn
# ==========================================
class OrbitalBurnPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.title = QLabel(">> ORBITAL INSERTION CRITICAL.\n>> HIT [BURN] WHEN TELEMETRY HITS APOAPSIS (99%).")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.telemetry = QProgressBar()
        self.telemetry.setRange(0, 100)
        self.layout.addWidget(self.telemetry)
        
        self.burn_btn = QPushButton("[ INITIATE BURN ]")
        self.burn_btn.clicked.connect(self.check_burn)
        self.layout.addWidget(self.burn_btn)
        
        self.val = 0
        self.direction = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_orbit)
        self.timer.start(random.randint(15, 30))

    def update_orbit(self):
        self.val += self.direction
        if self.val >= 100 or self.val <= 0:
            self.direction *= -1
        self.telemetry.setValue(self.val)

    def check_burn(self):
        self.timer.stop()
        if 97 <= self.val <= 100:
            self.title.setText(">> ORBIT CIRCULARIZED. GOOD BURN.")
            self.burn_btn.setDisabled(True)
            self.solved.emit()
        else:
            self.title.setText(f">> MISSION FAILURE. BURNED AT {self.val}%.")
            QTimer.singleShot(1500, self.reset_burn)

    def reset_burn(self):
        self.title.setText(">> ORBITAL INSERTION CRITICAL.\n>> HIT [BURN] WHEN TELEMETRY HITS APOAPSIS (99%).")
        self.val = 0
        self.direction = 1
        self.timer.start()

# ==========================================
# 6. CRYPTOGRAPHY: Wordle (Terminal Edition)
# ==========================================
class WordlePuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.word_list = ["SPACE", "VIRUS", "STARS", "NEXUS", "ROBOT", "ORBIT"]
        self.target_word = random.choice(self.word_list)
        self.attempts_left = 6
        
        self.title = QLabel(">> 5-LETTER DECRYPTION KEY REQUIRED.")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFixedHeight(180)
        self.history.setStyleSheet("background-color: #050505; border: 1px solid #004400; font-family: 'Courier New'; font-size: 18px;")
        self.layout.addWidget(self.history)
        
        self.input_field = QLineEdit()
        self.input_field.setMaxLength(5)
        self.input_field.setPlaceholderText("Enter 5-letter key...")
        self.input_field.returnPressed.connect(self.check_word)
        self.layout.addWidget(self.input_field)

    def check_word(self):
        guess = self.input_field.text().strip().upper()
        if len(guess) != 5: return
            
        self.attempts_left -= 1
        self.input_field.clear()
        
        if guess == self.target_word:
            self.history.append(f"<span style='color:#00FF00'>[ {guess} ] - KEY ACCEPTED.</span>")
            self.input_field.setDisabled(True)
            self.solved.emit()
            return

        formatted_guess = ""
        for i, char in enumerate(guess):
            if char == self.target_word[i]:
                formatted_guess += f"<span style='color:#00FF00; font-weight:bold;'>{char}</span>"
            elif char in self.target_word:
                formatted_guess += f"<span style='color:#FFFF00; font-weight:bold;'>{char}</span>"
            else:
                formatted_guess += f"<span style='color:#FF0000;'>{char}</span>"
                
        self.history.append(f">> [ {formatted_guess} ] (Attempts: {self.attempts_left})")
        
        if self.attempts_left <= 0:
            self.history.append(">> <span style='color:#FF0000'>LOCKDOWN ENFORCED.</span>")
            self.input_field.setDisabled(True)

# ==========================================
# 7. REFLEXES: The Hash Collision
# ==========================================
class HashCollisionPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.target = random.randint(30, 85)
        
        self.title = QLabel(f">> HASH COLLISION DETECTED.\n>> LOCK THE BUFFER EXACTLY BETWEEN {self.target - 2}% AND {self.target + 2}%.")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setFixedHeight(30)
        self.layout.addWidget(self.bar)
        
        self.lock_btn = QPushButton("[ LOCK BUFFER ]")
        self.lock_btn.clicked.connect(self.check_lock)
        self.layout.addWidget(self.lock_btn)
        
        self.val = 0
        self.direction = 2
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bar)
        self.timer.start(15) 

    def update_bar(self):
        self.val += self.direction
        if self.val >= 100 or self.val <= 0:
            self.direction *= -1
        self.bar.setValue(self.val)

    def check_lock(self):
        self.timer.stop()
        if (self.target - 2) <= self.val <= (self.target + 2):
            self.title.setText(">> HASH COLLISION SECURED.")
            self.lock_btn.setDisabled(True)
            self.solved.emit()
        else:
            self.title.setText(f">> COLLISION MISSED AT {self.val}%. RESTARTING SEQUENCE.")
            QTimer.singleShot(1000, self.reset_puzzle)

    def reset_puzzle(self):
        self.title.setText(f">> HASH COLLISION DETECTED.\n>> LOCK THE BUFFER EXACTLY BETWEEN {self.target - 2}% AND {self.target + 2}%.")
        self.timer.start()

# ==========================================
# 8. ASTROPHYSICS: Doppler Calibrator
# ==========================================
class DopplerCalibratorPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.target_wl = random.randint(400, 700) 
        self.current_wl = self.target_wl + random.randint(100, 300) 
        
        self.title = QLabel(f">> TARGET STAR IS REDSHIFTED.\n>> BASELINE: {self.target_wl} nm | CURRENT OBSERVATION: {self.current_wl} nm")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.status = QLabel(">> ADJUST RELATIVE VELOCITY TO MATCH SPECTRA.")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(-300, 0) 
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_wavelength)
        self.layout.addWidget(self.slider)
        
        self.submit_btn = QPushButton("[ CONFIRM CALIBRATION ]")
        self.submit_btn.clicked.connect(self.check_calibration)
        self.layout.addWidget(self.submit_btn)

    def update_wavelength(self):
        adjusted = self.current_wl + self.slider.value()
        self.title.setText(f">> TARGET STAR IS REDSHIFTED.\n>> BASELINE: {self.target_wl} nm | CURRENT OBSERVATION: {adjusted} nm")

    def check_calibration(self):
        if (self.current_wl + self.slider.value()) == self.target_wl:
            self.status.setText(">> SPECTRA MATCHED. DOPPLER SHIFT NEUTRALIZED.")
            self.slider.setDisabled(True)
            self.submit_btn.setDisabled(True)
            self.solved.emit()
        else:
            self.status.setText(">> ERROR: SPECTROMETER MISALIGNED.")

# ==========================================
# 9. COMPUTER SCIENCE: Logic Gate Weaver
# ==========================================
class LogicGatePuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.input_a = random.choice([0, 1])
        self.input_b = random.choice([0, 1])
        
        self.gates = {"AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "XOR": lambda a, b: a ^ b}
        
        self.correct_gate = random.choice(list(self.gates.keys()))
        self.target_out = self.gates[self.correct_gate](self.input_a, self.input_b)
        
        self.title = QLabel(f">> CIRCUIT BREAKER OPEN.\n>> INPUT A: {self.input_a} | INPUT B: {self.input_b}\n>> TARGET OUTPUT: {self.target_out}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        btn_layout = QHBoxLayout()
        for gate in self.gates.keys():
            btn = QPushButton(f"[ {gate} ]")
            btn.clicked.connect(lambda checked, g=gate: self.check_logic(g))
            btn_layout.addWidget(btn)
            
        self.layout.addLayout(btn_layout)

    def check_logic(self, selected_gate):
        result = self.gates[selected_gate](self.input_a, self.input_b)
        if result == self.target_out:
            self.title.setText(f">> {selected_gate} GATE ACCEPTED. CIRCUIT CLOSED.")
            self.solved.emit()
        else:
            self.title.setText(f">> FATAL EXCEPTION: {selected_gate} RETURNS {result}. EXPECTED {self.target_out}.")

# ==========================================
# 10. REFLEXES: Typing Stress Test
# ==========================================
class TypingStressPuzzle(BasePuzzle):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        phrases = [
            "sudo rm -rf /boot/kernel",
            "import tensorflow as tf",
            "initiate_protocol_alpha",
            "eigenvalue_decomposition"
        ]
        self.target_phrase = random.choice(phrases)
        
        self.title = QLabel(f">> OVERRIDE REQUIRED. TYPE EXACTLY:\n\n{self.target_phrase}")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.timer_lbl = QLabel("TIME: 15s")
        self.timer_lbl.setStyleSheet("color: #FF0000; font-size: 20px;")
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.timer_lbl)
        
        self.input_field = QLineEdit()
        self.input_field.textChanged.connect(self.check_typing)
        self.layout.addWidget(self.input_field)
        
        self.time_left = 15
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def tick(self):
        self.time_left -= 1
        self.timer_lbl.setText(f"TIME: {self.time_left}s")
        if self.time_left <= 0:
            self.timer.stop()
            self.input_field.setDisabled(True)
            self.title.setText(">> TIMEOUT. INITIATING COUNTERMEASURES.")

    def check_typing(self):
        if self.input_field.text() == self.target_phrase and self.time_left > 0:
            self.timer.stop()
            self.input_field.setStyleSheet("background-color: #003300;")
            self.input_field.setDisabled(True)
            self.title.setText(">> OVERRIDE ACCEPTED.")
            self.solved.emit()


# ==========================================
# THE PUZZLE FACTORY
# ==========================================
class PuzzleManager:
    @staticmethod
    def get_random_puzzle():
        """ Selects a mechanical puzzle at random to inject into the OS """
        puzzles = [
            MastermindPuzzle, LightsOutPuzzle, WaterJugPuzzle,
            BinaryDecoderPuzzle, OrbitalBurnPuzzle, WordlePuzzle,
            HashCollisionPuzzle, DopplerCalibratorPuzzle, LogicGatePuzzle,
            TypingStressPuzzle
        ]
        selected_class = random.choice(puzzles)
        return selected_class()