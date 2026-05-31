import sys
import os
import psutil
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
                             QMdiArea, QMdiSubWindow, QFrame, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QObject, QEvent
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor
from apps.telemetry import ApexDiagnosticsApp

from settings import ASSETS
from apps.dos_terminal import RedQueenDOSApp
from apps.file_explorer import UmbrellaExplorerApp
from apps.telemetry import ApexDiagnosticsApp, AstrophageApp
from apps.lore_modules import DatabaseApp, RunicVaultApp, IncineratorApp
from apps.media_modules import SurveillanceApp, AudioRoutineApp, MediaRoutineApp

class OrbitalScreensaver(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #000000;")
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_orbit)

    def start_saver(self):
        self.angle = 0
        self.timer.start(30)

    def stop_saver(self):
        self.timer.stop()

    def update_orbit(self):
        self.angle += 1
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cx = self.width() / 2
        cy = self.height() / 2
        
        # Center Core
        painter.setBrush(QBrush(QColor(255, 0, 0))) 
        painter.drawEllipse(int(cx - 10), int(cy - 10), 20, 20)
        
        # Orbital Rings
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(196, 30, 58, 150), 2)) # Changed to Umbrella Red!
        painter.translate(cx, cy)
        
        for i in range(4):
            painter.rotate(self.angle * (0.5 if i % 2 == 0 else -0.5) + (i * 45))
            painter.drawEllipse(-200 + (i*20), -100, 400 - (i*40), 200)
            
        # --- THE FIX: PUT THE PAINTBRUSH DOWN ---
        painter.end()

class ActivityFilter(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.setInterval(180000) 
        self.timer.timeout.connect(self.trigger_screensaver)
        self.timer.start()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.KeyPress, QEvent.Type.MouseButtonPress):
            self.timer.start() 
            if self.main_window.stack.currentIndex() == 8: 
                self.main_window.screens[8].stop_saver()
                self.main_window.switch_screen(5) 
        return super().eventFilter(obj, event)
        
    def trigger_screensaver(self):
        if self.main_window.stack.currentIndex() == 5: 
            self.main_window.switch_screen(8)
            self.main_window.screens[8].start_saver()

from PyQt6.QtWidgets import QFileDialog # Added for the Wallpaper selector

class DesktopScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
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
            ">> RED QUEEN DOS", ">> FILE EXPLORER", ">>  DATABASE", 
            ">> APEX TELEMETRY", ">> ASTROPHAGE DAEMON", ">> RUNIC VAULT", 
            ">> INCINERATOR", ">> CHANGE WALLPAPER", ">> SYSTEM LOGOUT"
        ]
        
        for app in apps:
            item = QListWidgetItem(app)
            item.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
            self.sidebar.addItem(item)
            
        self.sidebar.itemClicked.connect(self.launch_app)
        self.top_container.addWidget(self.sidebar)
        
        self.workspace = QMdiArea()
        
        # --- REVERTED WORKSPACE FALLBACK COLOR TO BLACK ---
        bg_path = ASSETS.get("desktop_bg", "").replace("\\", "/")
        self.workspace.setStyleSheet(f"QMdiArea {{ background-image: url('{bg_path}'); background-position: center; background-repeat: no-repeat; background-color: #050505; border: none; }}")
        
        self.workspace.subWindowActivated.connect(self.refresh_taskbar)
        self.top_container.addWidget(self.workspace)
        
        self.taskbar = QFrame()
        self.taskbar.setFixedHeight(40)
        
        # --- REVERTED TASKBAR TO BLACKOUT THEME ---
        self.taskbar.setStyleSheet("""
            QFrame { background-color: #050505; border-top: 1px solid #1A1A1A; }
            QPushButton { background-color: #0A0A0A; color: #708085; border: 1px solid #1A1A1A; border-radius: 2px; font-family: 'Arial'; font-size: 11px; text-align: left; padding-left: 15px; min-width: 160px; }
            QPushButton:hover { background-color: #111111; color: #FFFFFF; border: 1px solid #C41E3A; }
            QPushButton#activeTask { background-color: #111111; border: 1px solid #C41E3A; color: #FFFFFF; font-weight: bold; border-left: 3px solid #C41E3A; }
        """)
        self.taskbar_layout = QHBoxLayout(self.taskbar)
        self.taskbar_layout.setContentsMargins(10, 4, 10, 4)
        self.taskbar_layout.addStretch() 
        
        self.main_v_layout.addLayout(self.top_container)
        self.main_v_layout.addWidget(self.taskbar)
        self.setLayout(self.main_v_layout)

        self.jarvis_timer = QTimer()
        self.jarvis_timer.timeout.connect(self.jarvis_monitor)
        self.jarvis_timer.start(10000)
    def jarvis_monitor(self):
        if psutil.virtual_memory().percent > 90:
            QMessageBox.warning(self, "JARVIS ALERT", ">> Sir, memory limits exceeded. Recommend deploying Astrophage Mode.")

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier) and event.key() == Qt.Key.Key_G:
            self.workspace.closeAllSubWindows()
            self.workspace.setStyleSheet("QMdiArea { background-color: #000000; }") 
            self.sidebar.hide()
            self.taskbar.hide()
            QMessageBox.critical(self, "GHOST PROTOCOL", "SYSTEM WIPED. NO DATA RETAINED.")

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
        if window.isMinimized(): window.showNormal()
        window.setFocus()

    def add_mdi_window(self, title, widget, width=900, height=600):
        for win in self.workspace.subWindowList():
            if win.windowTitle() == title:
                win.showNormal()
                win.setFocus()
                return
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(title)
        self.workspace.addSubWindow(sub)
        sub.resize(width, height)
        sub.show()
        self.refresh_taskbar()
        
    def change_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            css_path = file_path.replace("\\", "/")
            self.workspace.setStyleSheet(f"QMdiArea {{ background-image: url('{css_path}'); background-position: center; background-repeat: no-repeat; background-color: #FFFFFF; border: none; }}")
            
    def launch_app(self, item):
        app_name = item.text().strip()
        print(f">> SYSTEM ROUTER TRIGGERED: Attempting to launch '{app_name}'") 
        
        # --- THE FIX: Using 'in' makes the router bulletproof against typos and extra spaces ---
        if "DOS" in app_name: self.add_mdi_window(">> RED QUEEN MAINFRAME DOS", RedQueenDOSApp(), 600, 400)
        elif "EXPLORER" in app_name: self.add_mdi_window(">> NEST FILE EXPLORER", UmbrellaExplorerApp(), 1000, 700)
        
        # This will now trigger whether the button says "DATABASE", "CLASSIFIED DATABASE", or has weird spacing!
        elif "DATABASE" in app_name: self.add_mdi_window(">> UMBRELLA CLASSIFIED DATABASE", DatabaseApp(), 1100, 600)
        
        elif "TELEMETRY" in app_name: self.add_mdi_window(">> APEX DASHBOARD", ApexDiagnosticsApp(), 600, 400)
        elif "ASTROPHAGE" in app_name: self.add_mdi_window(">> ASTROPHAGE MODE", AstrophageApp(), 500, 400)
        elif "VAULT" in app_name: self.add_mdi_window(">> COLD STORAGE VAULT", RunicVaultApp(), 400, 300)
        elif "INCINERATOR" in app_name: self.add_mdi_window(">> THERMAL INCINERATOR", IncineratorApp(), 500, 400)
        elif "WALLPAPER" in app_name: self.change_wallpaper()
        elif "LOGOUT" in app_name: sys.exit()
        else:
            print(f">> ERROR: '{app_name}' not found in routing table.")
        
    def jarvis_monitor(self):
        if psutil.virtual_memory().percent > 90:
            QMessageBox.warning(self, "JARVIS ALERT", ">> Sir, memory limits exceeded. Recommend deploying Astrophage Mode.")

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier) and event.key() == Qt.Key.Key_G:
            self.workspace.closeAllSubWindows()
            self.workspace.setStyleSheet("QMdiArea { background-color: #000000; }") 
            self.sidebar.hide()
            self.taskbar.hide()
            QMessageBox.critical(self, "GHOST PROTOCOL", "SYSTEM WIPED. NO DATA RETAINED.")

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
        if window.isMinimized(): window.showNormal()
        window.setFocus()

    def add_mdi_window(self, title, widget, width=900, height=600):
        for win in self.workspace.subWindowList():
            if win.windowTitle() == title:
                win.showNormal()
                win.setFocus()
                return
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(title)
        self.workspace.addSubWindow(sub)
        sub.resize(width, height)
        sub.show()
        self.refresh_taskbar()
        
    def launch_app(self, item):
        app_name = item.text().strip()
        print(f">> SYSTEM ROUTER TRIGGERED: Attempting to launch '{app_name}'") 
        
        # --- THE FIX: Using 'in' makes the router bulletproof against typos and extra spaces ---
        if "DOS" in app_name: self.add_mdi_window(">> RED QUEEN MAINFRAME DOS", RedQueenDOSApp(), 600, 400)
        elif "EXPLORER" in app_name: self.add_mdi_window(">> NEST FILE EXPLORER", UmbrellaExplorerApp(), 1000, 700)
        
        # This will now trigger whether the button says "DATABASE", "CLASSIFIED DATABASE", or has weird spacing!
        elif "DATABASE" in app_name: self.add_mdi_window(">> UMBRELLA CLASSIFIED DATABASE", DatabaseApp(), 1100, 600)
        
        elif "TELEMETRY" in app_name: self.add_mdi_window(">> APEX DASHBOARD", ApexDiagnosticsApp(), 600, 400)
        elif "ASTROPHAGE" in app_name: self.add_mdi_window(">> ASTROPHAGE MODE", AstrophageApp(), 500, 400)
        elif "VAULT" in app_name: self.add_mdi_window(">> COLD STORAGE VAULT", RunicVaultApp(), 400, 300)
        elif "INCINERATOR" in app_name: self.add_mdi_window(">> THERMAL INCINERATOR", IncineratorApp(), 500, 400)
        elif "WALLPAPER" in app_name: self.change_wallpaper()
        elif "LOGOUT" in app_name: sys.exit()
        else:
            print(f">> ERROR: '{app_name}' not found in routing table.")