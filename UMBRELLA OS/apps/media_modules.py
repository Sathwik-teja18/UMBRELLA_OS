import os
import random
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QTextEdit,
                             QPushButton, QFileDialog, QMessageBox, QSlider, QProgressBar)
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QDateTime

from settings import ASSETS

class SurveillanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #2A363B; }")
        layout = QGridLayout()
        # Look how clean these dynamic paths are now!
        cam_paths = [ASSETS.get("cam1", ""), ASSETS.get("cam2", ""), ASSETS.get("cam3", ""), ASSETS.get("cam4", "")]
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
            
            if cam_paths[i] and os.path.exists(cam_paths[i]):
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
            with open(file_path, 'w') as f: f.write(classified_header + content)
            QMessageBox.information(self, "SAVED", ">> LOG ENCRYPTED AND STORED SECURELY.")

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
        for b in ["<< PREV", "[ PLAY / PAUSE ]", "NEXT >>"]: btns.addWidget(QPushButton(b))
        controls.addLayout(btns)
        main_layout.addLayout(controls)
        layout.addLayout(main_layout)
        self.setLayout(layout)