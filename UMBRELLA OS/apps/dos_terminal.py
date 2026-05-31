import random
import time
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QLabel, QApplication
from PyQt6.QtCore import Qt

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
        self.setup_commands()

    def setup_commands(self):
        self.dos_commands = {
            "hawking_rad_calc": ">> CALCULATING HAWKING RADIATION...\n>> MASS: 1.989e30 kg\n>> TEMP: 6.169e-8 K\n>> EVAPORATION TIME: 2.098e67 years",
            "orbit_traj --oxford": ">> PLOTTING TRAJECTORY TO OXFORD UNIVERSITY...\n>> DISTANCE: 4,982 MILES\n>> ETA: 5 YEARS.\n>> COURSE LOCKED.",
            "orbit_traj --cambridge": ">> PLOTTING TRAJECTORY TO CAMBRIDGE...\n>> ETA: < 5 YEARS.\n>> PREPARE FOR PHD INITIATION.",
            "stellar_spectroscopy": ">> ANALYZING EMISSION LINES...\n>> TARGET: ALPHA CENTAURI\n>> RESULT: HIGH CONCENTRATIONS OF HYDROGEN DETECTED.",
            "relativity_sim": ">> INITIATING GENERAL RELATIVITY SIM...\n>> TIME DILATION AT CURRENT VELOCITY: 1.00000001.",
            "launch_seq --private": ">> INITIATING PAYLOAD SEQUENCE...\n>> PROPERTY OF: TARIKONDA SPACE CORP.\n>> T-MINUS 10 SECONDS.",
            "compile_java": ">> BUILDING MAINFRAME DEPENDENCIES...\n>> javac Main.java\n>> BUILD SUCCESS.",
            "gpu_accel --cupy": ">> ROUTING TENSOR CALCULATIONS TO ASUS GPU...\n>> OVERRIDING VRAM LIMITS. CuPy INITIALIZED.",
            "train_neural_net": ">> TRAINING MODEL...\n>> Epoch 1/100: Loss 0.89\n>> Epoch 50/100: Loss 0.22\n>> Epoch 100/100: Loss 0.04. WEIGHTS SAVED.",
            "marine_plastic_scan": ">> RUNNING ECOSYSTEM RESTORATION PROTOCOL...\n>> AI MARINE PLASTIC DETECTOR: ACTIVE.\n>> 14 ANOMALIES FOUND IN QUADRANT 7.",
            "fetch_dataset": ">> DOWNLOADING 5TB DATASET FROM GOOGLE AI PRO...\n>> STORAGE UPGRADE CONFIRMED.",
            "wake_jarvis": ">> GOOD EVENING, SATHWIK. JARVIS SUBSYSTEM ONLINE.\n>> AWAITING YOUR COMMAND.",
            "jarvis_override": ">> I'M SORRY, RED QUEEN. I'M AFRAID I CAN'T LET YOU DO THAT.",
            "sys_vram_check": ">> ASUS SYSTEM MEMORY MANAGEMENT: NOMINAL.\n>> PAGING FILE OPTIMIZED. LEAK RESOLVED.",
            "workout_hypertrophy": ">> GENERATING 90-MIN ROUTINE...\n>> CURRENT FOCUS: HYPERTROPHY & ISOLATION.\n>> DON'T SKIP LEG DAY.",
            "badminton_stats": ">> LAST MATCH TELEMETRY:\n>> SMASH VELOCITY: 280 KM/H.\n>> ACCURACY: 92%.",
            "fit_check": ">> JORDANS DETECTED. BOLD COLORS DETECTED. TECHNICAL LAYERS SYNCED.\n>> AESTHETIC MATCH: 100%. DRIP SECURED.",
            "marie_antoinette": ">> FACT CHECK: 'LET THEM EAT CAKE'\n>> HISTORICALLY ATTRIBUTED TO MARIE ANTOINETTE DURING THE FRENCH REVOLUTION.",
            "daily_mantra": ">> ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं\n>> भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्",
            "chakra_alignment": ">> SCANNING ENERGY CENTERS...\n>> ROOT CHAKRA: STABILIZED.\n>> CROWN CHAKRA: OPEN.",
            "ping mainframe": ">> PONG. MAINFRAME ONLINE. LATENCY: 0.04ms",
            "check_vats": ">> VAT 1: STABLE\n>> VAT 2: STABLE\n>> TYRANT PROJECT: DORMANT",
            "release_hounds": ">> ERROR: BIOLOGICAL CONTAINMENT PROTOCOLS ACTIVE. CANNOT RELEASE CERBERUS UNITS.",
            "nemesis_protocol": ">> DEPLOYING B.O.W. TO SPECIFIED COORDINATES...\n>> TARGET: S.T.A.R.S. MEMBERS.",
            "hive_map": ">> NEST FACILITY MAP\n[ L1: MANSION ENTRANCE ]\n[ L2: MAIN SHAFT ]\n[ L3: LAB ALPHA & BETA ]\n[ L4: SERVER ROOM (RED QUEEN) ]\n[ L5: CONTAINMENT VATS ]\n[ L6: TRAIN DEPOT ]",
            "hex_dump": ">> 0x4A 0x61 0x72 0x76 0x69 0x73 0x20 0x4F 0x6E 0x6C 0x69 0x6E 0x65\n>> 0x55 0x6D 0x62 0x72 0x65 0x6C 0x6C 0x61 0x20 0x43 0x6F 0x72 0x70\n>> MEMORY DUMP COMPLETE.",
            "sudo su": ">> WELCOME TO ROOT, ADMINISTRATOR SATHWIK.",
            "whoami": ">> SYSTEM ADMINISTRATOR: SATHWIK TEJA TARIKONDA.\n>> AGE: 18.\n>> MISSION: SPACE RESEARCH / UMBRELLA DIRECTOR.",
            "help": ">> AVAILABLE MODULES:\n>> ASTROPHYSICS (e.g., hawking_rad_calc, orbit_traj --oxford)\n>> CSE & AI (e.g., compile_java, train_neural_net)\n>> JARVIS (e.g., wake_jarvis, jarvis_override)\n>> FITNESS (e.g., workout_hypertrophy, badminton_stats)\n>> UMBRELLA (e.g., check_vats, hive_map, nemesis_protocol)\n>> ANIMATIONS: matrix_rain, sys_defrag, antivirus_synth\n>> SYSTEM: clear, exit, whoami, sudo su"
        }

    def process_command(self):
        cmd = self.command_input.text().strip().lower()
        self.command_input.clear()
        self.output.append(f"C:\\> {cmd}")
        
        if cmd == "clear":
            self.output.clear()
            self.output.setText(">> RED QUEEN MAINFRAME DOS v1.0\n>> ALL ACTIONS MONITORED.\n>> WAITING FOR INPUT...\n")
        elif cmd == "exit":
            self.window().close() 
        elif cmd == "matrix_rain":
            self.run_matrix_rain()
        elif cmd == "sys_defrag":
            self.run_sys_defrag()
        elif cmd == "antivirus_synth":
            self.run_antivirus_synth()
        elif cmd in self.dos_commands:
            self.output.append(self.dos_commands[cmd] + "\n")
        else:
            self.output.append(f">> COMMAND NOT RECOGNIZED: '{cmd}'. TYPE 'help' FOR COMMANDS.\n")
            
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())

    def run_matrix_rain(self):
        self.command_input.setDisabled(True)
        for _ in range(35):
            line = "".join(random.choice(["0", "1", " ", "  "]) for _ in range(45))
            self.output.append(f">> {line}")
            self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
            QApplication.processEvents()
            time.sleep(0.03)
        self.output.append(">> MATRIX STREAM ENDED.\n")
        self.command_input.setDisabled(False)
        self.command_input.setFocus()

    def run_sys_defrag(self):
        self.command_input.setDisabled(True)
        self.output.append(">> DEFRAGMENTING CLUSTER DRIVES...")
        blocks = ["[          ]", "[||        ]", "[||||      ]", "[||||||    ]", "[||||||||  ]", "[||||||||||]"]
        for i in range(1, 6):
            self.output.append(f">> SECTOR {i}: {random.choice(blocks)}")
            QApplication.processEvents()
            time.sleep(0.4)
            self.output.undo()
            self.output.append(f">> SECTOR {i}: {blocks[5]} - OPTIMIZED")
            self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
        self.output.append(">> DEFRAGMENTATION COMPLETE.\n")
        self.command_input.setDisabled(False)
        self.command_input.setFocus()

    def run_antivirus_synth(self):
        self.command_input.setDisabled(True)
        self.output.append(">> SYNTHESIZING G-VACCINE / ANTIGEN...")
        for i in range(0, 101, 10):
            self.output.append(f">> BINDING PROTEINS... {i}%")
            self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())
            QApplication.processEvents()
            time.sleep(0.2)
            if i < 100: self.output.undo()
        self.output.append(">> ANTIVIRUS SYNTHESIS COMPLETE. READY FOR INJECTION.\n")
        self.command_input.setDisabled(False)
        self.command_input.setFocus()