import os
import math
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QTreeView, QListView,
                             QFrame, QTextEdit, QPushButton, QStackedWidget, QGraphicsScene, QGraphicsView,
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QMessageBox, QFileIconProvider,
                             QComboBox) # <--- ADD THIS
from PyQt6.QtGui import QFileSystemModel, QDesktopServices, QColor, QBrush, QPen, QFont, QPixmap, QIcon, QPainter
from PyQt6.QtCore import Qt, QSize, QDir, QTimer, QUrl, QFileInfo
from PyQt6.QtGui import QFileSystemModel, QDesktopServices, QColor, QBrush, QPen, QFont, QPixmap, QIcon, QPainter, QImage
from settings import QUARANTINE_DIR

# ==========================================
# 3D SPATIAL PHYSICS & GRAPHICS ENGINE
# ==========================================

class TopologyEdge(QGraphicsLineItem):
    def __init__(self, source_node, target_node):
        super().__init__()
        self.source_node = source_node
        self.target_node = target_node
        # Changed from blue-grey to Dark Blood Red
        self.setPen(QPen(QColor("#500000"), 2, Qt.PenStyle.DashLine))
        self.setZValue(-1000)
        self.adjust()

    def adjust(self):
        if not self.source_node or not self.target_node: return
        p1 = self.source_node.pos()
        p2 = self.target_node.pos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())


class TopologyNode(QGraphicsEllipseItem):
    def __init__(self, x3d, y3d, z3d, radius, file_info, explorer_app):
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.file_info = file_info
        self.explorer = explorer_app
        self.edges = []
        self.x3d = x3d
        self.y3d = y3d
        self.z3d = z3d
        self.setAcceptHoverEvents(True)
        self.is_dir = file_info.isDir()
        
        # --- PURGED CYAN HERE ---
        # Root is Pure Red, Folders are Umbrella Red, Files are Grey
        self.base_color = "#FF0000" if file_info.fileName() in [".", "ROOT"] else ("#C41E3A" if self.is_dir else "#A0B0B5")
        
        self.setPen(QPen(QColor(self.base_color), 2))
        self.setBrush(QBrush(QColor("#111111")))

        label_text = file_info.fileName()[:15]
        if file_info.fileName() in [".", ""]: label_text = "CURRENT SECTOR"
        self.label = QGraphicsTextItem(label_text, self)
        self.label.setDefaultTextColor(QColor(self.base_color))
        self.label.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        self.label.setPos(-radius - 15, radius + 2)
    def add_edge(self, edge):
        self.edges.append(edge)

    def project(self, ax, ay, pan_x=0, pan_y=0):
        """Simulates 3D rotation, depth perspective mapping to 2D, and lateral panning."""
        # Y-Axis Rotation (Yaw)
        x_rot = self.x3d * math.cos(ay) - self.z3d * math.sin(ay)
        z_rot = self.x3d * math.sin(ay) + self.z3d * math.cos(ay)
        
        # X-Axis Rotation (Pitch)
        y_rot = self.y3d * math.cos(ax) - z_rot * math.sin(ax)
        z_final = self.y3d * math.sin(ax) + z_rot * math.cos(ax)

        # Perspective Divide (Depth simulation)
        focal_length = 800
        z_shifted = z_final + 400 # Push the center back from the camera
        scale = focal_length / max(10, focal_length + z_shifted)
        
        # --- PANNING ADDED HERE ---
        self.setPos((x_rot * scale) + pan_x, (y_rot * scale) + pan_y)
        self.setScale(max(0.2, scale))
        self.setZValue(-z_final) # Closer objects draw on top
        self.setOpacity(max(0.1, min(1.0, scale * 1.2))) # Distance Fog

        for edge in self.edges:
            edge.adjust()

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor("#FFFFFF"), 3))
        self.setBrush(QBrush(QColor(self.base_color)))
        self.label.setDefaultTextColor(QColor("#FFFFFF"))
        self.explorer.update_jarvis_telemetry(self.file_info)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(self.base_color), 2))
        self.setBrush(QBrush(QColor("#111111")))
        self.label.setDefaultTextColor(QColor(self.base_color))
        super().hoverLeaveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.is_dir:
            index = self.explorer.file_model.index(self.file_info.absoluteFilePath())
            self.explorer.initiate_decryption(index)
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_info.absoluteFilePath()))
        super().mouseDoubleClickEvent(event)


class TopologySpace(QGraphicsView):
    def __init__(self, scene, explorer):
        super().__init__(scene)
        self.explorer = explorer
        self.setStyleSheet("background-color: #020304; border: none;")
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Anchor the zoom exactly where the mouse is pointing
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.pan_x = 0.0  # Tracks lateral X movement
        self.pan_y = 0.0  # Tracks lateral Y movement
        self.last_pos = None
        self.nodes = []

    def wheelEvent(self, event):
        """Allows scrolling to zoom in and out of the 3D space."""
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            # RIGHT CLICK: Navigate Up the Hierarchy
            self.explorer.navigate_up()
            
            # Reset panning when entering a new directory
            self.pan_x = 0.0
            self.pan_y = 0.0
            
        elif event.button() in [Qt.MouseButton.LeftButton, Qt.MouseButton.XButton1, Qt.MouseButton.XButton2, Qt.MouseButton.MiddleButton]:
            # Start drag for either rotation (Left) or panning (Side/Middle)
            item = self.itemAt(event.pos())
            if not item:
                self.last_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.last_pos:
            dx = event.pos().x() - self.last_pos.x()
            dy = event.pos().y() - self.last_pos.y()
            
            # Check which button is currently being held down
            if event.buttons() & Qt.MouseButton.LeftButton:
                # ROTATION (Left Click)
                self.angle_y -= dx * 0.005
                self.angle_x -= dy * 0.005
            elif event.buttons() & (Qt.MouseButton.XButton1 | Qt.MouseButton.XButton2 | Qt.MouseButton.MiddleButton):
                # PANNING (Side Buttons or Middle Click)
                self.pan_x += dx
                self.pan_y += dy
                
            self.last_pos = event.pos()
            
            # Re-project all nodes based on new camera angle and pan offsets
            for node in self.nodes:
                node.project(self.angle_x, self.angle_y, self.pan_x, self.pan_y)
                
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.last_pos = None
        super().mouseReleaseEvent(event)

# --- CUSTOM ICON PROVIDER ---
# --- CUSTOM ICON PROVIDER (Thread-Safe V3) ---
class UmbrellaIconProvider(QFileIconProvider):
    def icon(self, file_info):
        # THE FIX: Use QImage (Thread-Safe) instead of QPixmap
        image = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if file_info.isDir():
            if file_info.isRoot() or len(file_info.absoluteFilePath()) <= 3:
                painter.setBrush(QBrush(QColor("#2A363B")))
                painter.setPen(QPen(QColor("#5C7680"), 2))
                painter.drawRect(8, 20, 48, 24)
                painter.setBrush(QBrush(QColor("#00FF00"))) 
                painter.drawEllipse(45, 28, 6, 6)
            else:
                painter.setBrush(Qt.BrushStyle.NoBrush) 
                painter.setPen(QPen(QColor("#A0B0B5"), 2))
                painter.drawRect(10, 18, 44, 28)
                painter.drawLine(10, 18, 25, 10)
                painter.drawLine(25, 10, 54, 10)
                painter.drawLine(54, 10, 54, 18)
        else:
            ext = file_info.suffix().lower()
            color = "#C41E3A" if ext in ['py', 'json', 'js', 'html', 'css'] else "#FFFFFF"
            if ext in ['exe', 'bat', 'dll']: color = "#FF0000"
            
            painter.setPen(QPen(QColor(color), 2))
            painter.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
            # Notice we are drawing text onto the 'image.rect()' now
            painter.drawText(image.rect(), Qt.AlignmentFlag.AlignCenter, f"[ .{ext[:3]} ]" if ext else "[ BIN ]")
            
        painter.end()
        
        # Convert the thread-safe QImage back into a QPixmap for the UI
        return QIcon(QPixmap.fromImage(image))

# ==========================================
# UMBRELLA EXPLORER V3.0
# ==========================================
class UmbrellaExplorerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: #050505; }")
        if not os.path.exists(QUARANTINE_DIR): os.makedirs(QUARANTINE_DIR)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.terminal = QTextEdit()
        self.terminal.setFixedHeight(80)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #0A0A0A; color: #5BC0BE; font-family: 'Courier New'; font-size: 13px; border-bottom: 2px solid #1A1A1A; padding: 5px;")
        self.terminal.setText(">> NEST SYSTEM ONLINE.\n>> MOUNTING ROOT DIRECTORY...")
        layout.addWidget(self.terminal)
        
      # --- CONTROL BAR WITH FILTER ---
        control_bar = QHBoxLayout()
        self.topology_btn = QPushButton("[ TOGGLE 3D TOPOLOGY ]")
        self.topology_btn.setStyleSheet("background-color: #111; color: #FFF; border: 1px solid #5C7680; font-family: 'Courier New'; padding: 5px;")
        self.topology_btn.clicked.connect(self.toggle_view)
        
        self.current_filter = "[ ALL FILES ]"
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["[ ALL FILES ]", "[ DIRECTORIES ONLY ]", "[ EXECUTABLES ]", "[ MEDIA / AUDIO ]", "[ SOURCE CODE ]"])
        self.filter_combo.setStyleSheet("""
            QComboBox { background-color: #111; color: #5BC0BE; border: 1px solid #5C7680; font-family: 'Courier New'; padding: 5px; font-weight: bold; }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView { background-color: #0A0A0A; color: #FFF; selection-background-color: #C41E3A; border: 1px solid #5C7680;}
        """)
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        
        control_bar.addWidget(self.topology_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        control_bar.addWidget(self.filter_combo, alignment=Qt.AlignmentFlag.AlignLeft)
        control_bar.addStretch() # Pushes the buttons to the left
        layout.addLayout(control_bar)
        
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("") 
        self.file_model.setIconProvider(UmbrellaIconProvider())
        
        self.view_stack = QStackedWidget()
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(""))
        for i in range(1, self.file_model.columnCount()): self.tree_view.hideColumn(i)
        
        self.list_view = QListView()
        self.list_view.setModel(self.file_model)
        self.list_view.setRootIndex(self.file_model.index(""))
        self.list_view.setViewMode(QListView.ViewMode.IconMode)
        self.list_view.setIconSize(QSize(80, 80)) 
        self.list_view.setGridSize(QSize(140, 140))
        self.list_view.setWordWrap(True)
        self.list_view.setSpacing(10)
        
        reticle_css = """
            QListView, QTreeView { background-color: #0A0A0A; color: #FFF; font-family: 'Courier New'; outline: none; border: none; }
            QListView::item:selected { background-color: transparent; border: 2px solid #C41E3A; color: #C41E3A; }
            QListView::item:hover { border: 1px dashed #5BC0BE; }
        """
        self.list_view.setStyleSheet(reticle_css)
        self.tree_view.setStyleSheet(reticle_css)
        
        self.list_view.doubleClicked.connect(self.initiate_decryption) 
        self.tree_view.clicked.connect(self.on_tree_clicked)
        self.list_view.clicked.connect(self.on_list_clicked)
        
        # --- JARVIS PANE ---
        self.details_panel = QFrame()
        self.details_panel.setStyleSheet("background-color: #0A0A0A; border-left: 2px solid #1A1A1A;")
        details_layout = QVBoxLayout()
        details_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.det_icon = QLabel()
        self.det_icon.setFixedSize(100, 100)
        self.det_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.det_name = QLabel("AWAITING TARGET")
        self.det_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFF; border: none;")
        self.det_name.setWordWrap(True)
        
        self.jarvis_log = QTextEdit()
        self.jarvis_log.setReadOnly(True)
        self.jarvis_log.setStyleSheet("background-color: #050505; color: #A0B0B5; font-family: 'Courier New'; font-size: 11px; border: 1px solid #1A1A1A;")
        self.jarvis_log.setText(">> JARVIS TELEMETRY STANDBY.")
        
        details_layout.addWidget(self.det_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        details_layout.addWidget(self.det_name)
        details_layout.addWidget(self.jarvis_log)
        self.details_panel.setLayout(details_layout)
        
        self.splitter.addWidget(self.tree_view)
        self.splitter.addWidget(self.list_view)
        self.splitter.addWidget(self.details_panel)
        self.splitter.setSizes([200, 700, 250]) 
        self.view_stack.addWidget(self.splitter)
        
        # --- TOPOLOGY VIEW ---
        self.scene = QGraphicsScene()
        self.topology_space = TopologySpace(self.scene, self)
        self.view_stack.addWidget(self.topology_space)
        
        layout.addWidget(self.view_stack)
        self.setLayout(layout)
        self.current_path = QDir.rootPath()

    def on_tree_clicked(self, index):
        if self.file_model.isDir(index):
            self.initiate_decryption(index)

    def on_list_clicked(self, index):
        file_info = self.file_model.fileInfo(index)
        self.update_jarvis_telemetry(file_info)

    def navigate_up(self):
        """Triggered by Right-Click. Reverts to parent directory."""
        if not self.current_path: return
        parent_dir = QFileInfo(self.current_path).absolutePath()
        
        # Prevent navigating above root safely
        if parent_dir and parent_dir != self.current_path:
            index = self.file_model.index(parent_dir)
            self.initiate_decryption(index)

    def update_jarvis_telemetry(self, file_info):
        self.det_name.setText(file_info.fileName())
        self.det_icon.setPixmap(self.file_model.iconProvider().icon(file_info).pixmap(64, 64))
        
        if file_info.isDir():
            # Changed cyan text to Umbrella Red
            self.jarvis_log.setStyleSheet("background-color: #050505; color: #C41E3A; font-family: 'Courier New'; font-size: 11px; border: 1px solid #1A1A1A;")
            self.jarvis_log.setText(">> THREAT LEVEL: LOW\n>> ENCRYPTION: NONE\n>> JARVIS LOGIC: Standard directory structure detected. Safe to traverse.")
        else:
            size_mb = file_info.size() / (1024 * 1024)
            ext = file_info.suffix().lower()
            threat = "HIGH (EXECUTABLE)" if ext in ['exe', 'bat', 'dll'] else "LOW"
            # Changed cyan fallback to grey so it doesn't clash with the red
            color = "#FF0000" if threat == "HIGH (EXECUTABLE)" else "#A0B0B5"
            self.jarvis_log.setStyleSheet(f"background-color: #050505; color: {color}; font-family: 'Courier New'; font-size: 11px; border: 1px solid #1A1A1A;")
            self.jarvis_log.setText(f">> THREAT LEVEL: {threat}\n>> SIZE: {size_mb:.2f} MB\n>> MODIFIED: {file_info.lastModified().toString('yyyy-MM-dd')}\n\n>> HEX PREVIEW:\n0x4D 0x5A 0x90 0x00 0x03\n0x00 0x00 0x00 0x04 0x00")

    def initiate_decryption(self, index):
        if self.file_model.isDir(index):
            self.current_path = self.file_model.filePath(index)
            self.terminal.append(f">> INTERCEPTING ROUTE: {self.current_path}")
            self.terminal.append(">> BYPASSING SECURITY LATTICE [ ||||||      ] 40%")
            self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())
            QTimer.singleShot(250, lambda: self.complete_mount(index))
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_model.filePath(index)))

    def complete_mount(self, index):
        self.terminal.append(">> BYPASSING SECURITY LATTICE [ ||||||||||| ] 100%")
        self.terminal.append(">> SECTOR MOUNTED SUCESSFULLY.")
        self.terminal.verticalScrollBar().setValue(self.terminal.verticalScrollBar().maximum())
        self.list_view.setRootIndex(index)
        self.tree_view.setCurrentIndex(index)
        if self.current_path:
            self.render_topology(self.current_path)

    def toggle_view(self):
        current = self.view_stack.currentIndex()
        if current == 0:
            self.view_stack.setCurrentIndex(1)
            self.topology_btn.setText("[ REVERT TO DATAGRID ]")
            if self.current_path: self.render_topology(self.current_path)
        else:
            self.view_stack.setCurrentIndex(0)
            self.topology_btn.setText("[ TOGGLE 3D TOPOLOGY ]")
    def apply_filter(self, text):
        """Triggers immediately when you select a new filter from the dropdown."""
        self.current_filter = text
        if self.current_path:
            self.render_topology(self.current_path)
    def render_topology(self, path):
        """Generates the 3D Fibonacci sphere web of nodes."""
        self.scene.clear()
        self.topology_space.nodes.clear()
        if not path: return
        
        root_info = self.file_model.fileInfo(self.file_model.index(path))
        
        # Draw 3D Grid Guidelines (Background)
        for i in range(-1000, 1100, 100):
            self.scene.addLine(i, -1000, i, 1000, QPen(QColor("#080D11")))
            self.scene.addLine(-1000, i, 1000, i, QPen(QColor("#080D11")))

        # Central Core Node (0, 0, 0)
        core = TopologyNode(0, 0, 0, 25, root_info, self)
        self.scene.addItem(core)
        self.topology_space.nodes.append(core)

        # Get contents
        directory = QDir(path)
        all_files = directory.entryInfoList(QDir.Filter.Files | QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
        
        # --- THE FIX: FILTER THE DATA STREAM ---
        files = []
        for f_info in all_files:
            ext = f_info.suffix().lower()
            if self.current_filter == "[ DIRECTORIES ONLY ]" and not f_info.isDir(): continue
            if self.current_filter == "[ EXECUTABLES ]" and ext not in ['exe', 'bat', 'dll', 'msi']: continue
            if self.current_filter == "[ MEDIA / AUDIO ]" and ext not in ['mp3', 'mp4', 'wav', 'mkv', 'avi', 'png', 'jpg', 'jpeg', 'gif']: continue
            if self.current_filter == "[ SOURCE CODE ]" and ext not in ['py', 'json', 'js', 'html', 'css', 'java', 'c', 'cpp', 'h', 'txt', 'md']: continue
            files.append(f_info)

        if not files: 
            core.project(self.topology_space.angle_x, self.topology_space.angle_y)
            return

        # Fibonacci Sphere Distribution for organic, 3D nebula look
        import random
        n = len(files)
        phi = math.pi * (3. - math.sqrt(5.))  # Golden angle
        
        for i, f_info in enumerate(files):
            # Calculate 3D spherical coordinates
            y3d = 1 - (i / float(n - 1)) * 2 if n > 1 else 0
            rad_at_y = math.sqrt(1 - y3d * y3d)
            theta = phi * i
            
            # Randomizes the distance from the center (150px to 700px away)
            dynamic_radius = random.uniform(150, 700)
            
            x3d = math.cos(theta) * rad_at_y * dynamic_radius
            z3d = math.sin(theta) * rad_at_y * dynamic_radius
            y3d *= dynamic_radius
            
            # Create interactive node
            node = TopologyNode(x3d, y3d, z3d, 10, f_info, self)
            self.scene.addItem(node)
            self.topology_space.nodes.append(node)
            
            # Create dynamic tether edge
            edge = TopologyEdge(core, node)
            self.scene.addItem(edge)
            
            core.add_edge(edge)
            node.add_edge(edge)
            
        # Initial projection
        for node in self.topology_space.nodes:
            node.project(self.topology_space.angle_x, self.topology_space.angle_y)