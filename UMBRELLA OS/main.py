import sys
import os

# --- THE FAILSAFE: Forces Python to look in this exact folder for modules ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QPixmap

from settings import CORPORATE_THEME, ASSETS
from ui.boot_screens import BiosScreen, SplashScreen
from ui.auth_screens import LoginScreen, DeathScreen, LockdownScreen, OverrideScreen, RegistrationScreen
from ui.desktop import DesktopScreen, OrbitalScreensaver, ActivityFilter

# ... (The rest of your RedQueenOS class stays exactly the same below this) ...

class RedQueenOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UMBRELLA OS")
        self.showFullScreen()
        
        self.setCursor(Qt.CursorShape.BlankCursor)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Load the newly separated UI modules
        self.screens = {
            0: BiosScreen(self),
            1: LoginScreen(self),
            2: DeathScreen(self), 
            3: LockdownScreen(self),
            4: RegistrationScreen(self),
            5: DesktopScreen(self),
            6: OverrideScreen(self),
            7: SplashScreen(self),
            8: OrbitalScreensaver(self) 
        }
        
        for i in range(9): 
            self.stack.addWidget(self.screens[i])
            
        self.switch_screen(0)
        self.screens[0].start_boot()
        
        self.activity_filter = ActivityFilter(self)
        QApplication.instance().installEventFilter(self.activity_filter)

    def switch_screen(self, index):
        self.stack.setCurrentIndex(index)
        
        if index in [3, 4, 5, 6]:
            if ASSETS.get("cursor") and os.path.exists(ASSETS["cursor"]):
                custom_cursor = QCursor(QPixmap(ASSETS["cursor"]).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), 16, 16)
                self.setCursor(custom_cursor)
            else:
                self.setCursor(Qt.CursorShape.CrossCursor) 
        else:
            self.setCursor(Qt.CursorShape.BlankCursor)

        if index == 7: self.screens[7].start_splash()
        if index == 2: self.screens[2].trigger_death()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(CORPORATE_THEME)
    os_kernel = RedQueenOS()
    sys.exit(app.exec())