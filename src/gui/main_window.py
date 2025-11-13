"""
Main application window for StarSticks
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QTextEdit, QGroupBox, QTabWidget
)
from PyQt6.QtCore import Qt, QSize
from src.core.joystick_detector import JoystickDetector
from src.core.binding_parser import BindingParser
from src.gui.joystick_widget import DualJoystickView
from src.gui.visual_joystick_widget import DualVisualJoystickView
from src.core.action_categories import ActionMode, get_mode_icon


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.joystick_detector = JoystickDetector()
        self.binding_parser = BindingParser()
        self.detected_joysticks = []  # Store detected joysticks
        self.current_bindings = []  # Store current bindings for filtering
        self.current_mode = ActionMode.ALL  # Current filter mode
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("StarSticks - Star Citizen Joystick Binding Visualizer")
        self.setMinimumSize(1400, 900)

        # Set modern stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5689;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox:drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #0e639c;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #252525;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #0e639c;
            }
            QTabBar::tab:hover {
                background-color: #3d3d3d;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title Bar
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 10)

        title_label = QLabel("StarSticks")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #0e639c;")
        title_layout.addWidget(title_label)

        title_layout.addStretch()

        subtitle_label = QLabel("Star Citizen Joystick Binding Visualizer")
        subtitle_label.setStyleSheet("font-size: 14px; color: #888888;")
        title_layout.addWidget(subtitle_label)

        main_layout.addWidget(title_widget)

        # Control Bar - horizontal layout
        control_bar = QWidget()
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(15)

        # SC Instance controls
        instance_label = QLabel("SC Instance:")
        instance_label.setStyleSheet("font-weight: bold;")
        control_layout.addWidget(instance_label)

        self.instance_combo = QComboBox()
        self.instance_combo.setMinimumWidth(100)
        control_layout.addWidget(self.instance_combo)

        self.rescan_instances_btn = QPushButton("Rescan")
        self.rescan_instances_btn.clicked.connect(self.scan_sc_instances)
        control_layout.addWidget(self.rescan_instances_btn)

        self.refresh_bindings_btn = QPushButton("Load Bindings")
        self.refresh_bindings_btn.clicked.connect(self.load_bindings)
        control_layout.addWidget(self.refresh_bindings_btn)

        # Separator
        separator1 = QLabel("|")
        separator1.setStyleSheet("color: #555555; font-size: 20px;")
        control_layout.addWidget(separator1)

        # Mode filter
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("font-weight: bold;")
        control_layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.setMinimumWidth(180)
        for mode in ActionMode:
            icon = get_mode_icon(mode)
            self.mode_combo.addItem(f"{icon} {mode.value}", mode)
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        control_layout.addWidget(self.mode_combo)

        # Separator
        separator2 = QLabel("|")
        separator2.setStyleSheet("color: #555555; font-size: 20px;")
        control_layout.addWidget(separator2)

        # Joystick controls
        self.detect_btn = QPushButton("Detect Joysticks")
        self.detect_btn.clicked.connect(self.detect_joysticks)
        control_layout.addWidget(self.detect_btn)

        self.swap_btn = QPushButton("🔄 Swap L/R Mapping")
        self.swap_btn.clicked.connect(self.swap_joysticks)
        control_layout.addWidget(self.swap_btn)

        control_layout.addStretch()

        main_layout.addWidget(control_bar)

        # Status bar for joystick info and mapping status
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 5, 0, 5)

        joystick_status_label = QLabel("Joysticks:")
        joystick_status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(joystick_status_label)

        self.joystick_status = QLabel("Not detected")
        self.joystick_status.setStyleSheet("color: #888888;")
        status_layout.addWidget(self.joystick_status)

        status_layout.addStretch()

        self.mapping_status = QLabel()
        self.mapping_status.setStyleSheet("color: #4CAF50; font-style: italic;")
        status_layout.addWidget(self.mapping_status)

        main_layout.addWidget(status_widget)

        # Tabs for different visualization modes
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Tab 1: Visual Diagram
        self.visual_widget = DualVisualJoystickView()
        self.tabs.addTab(self.visual_widget, "📊 Visual Diagram")

        # Tab 2: Button Grid
        self.viz_widget = DualJoystickView()
        self.tabs.addTab(self.viz_widget, "🔲 Button Grid")

        main_layout.addWidget(self.tabs)

        # Status Bar
        self.statusBar().showMessage("Ready")

        # Auto-detect SC instances and joysticks on startup
        self.scan_sc_instances()
        self.detect_joysticks()

    def scan_sc_instances(self):
        """Scan for installed Star Citizen instances and populate dropdown"""
        self.statusBar().showMessage("Scanning for Star Citizen installations...")

        # Get list of installed instances
        installed_instances = self.binding_parser.detect_installed_instances()

        # Clear and repopulate combo box
        self.instance_combo.clear()

        if installed_instances:
            self.instance_combo.addItems(installed_instances)
            self.statusBar().showMessage(f"Found {len(installed_instances)} SC instance(s): {', '.join(installed_instances)}")
        else:
            # No instances found, add default options
            self.instance_combo.addItems(["LIVE", "PTU", "HOTFIX"])
            self.statusBar().showMessage("No Star Citizen installation found. Please check your installation path.")

    def detect_joysticks(self):
        """Detect connected joysticks and display them"""
        self.statusBar().showMessage("Detecting joysticks...")
        joysticks = self.joystick_detector.detect()

        # Store detected joysticks
        self.detected_joysticks = joysticks

        if joysticks:
            # Update status label
            joy_names = [f"{joy['name']} (ID {joy['id']})" for joy in joysticks]
            self.joystick_status.setText(" | ".join(joy_names))
            self.joystick_status.setStyleSheet("color: #4CAF50;")

            self.statusBar().showMessage(f"Detected {len(joysticks)} joystick(s)")

            # Update visualizations
            self.viz_widget.set_joysticks(joysticks)
            self.visual_widget.set_joysticks(joysticks)
        else:
            self.joystick_status.setText("Not detected")
            self.joystick_status.setStyleSheet("color: #FF5555;")
            self.statusBar().showMessage("No joysticks detected")

            # Clear visualizations
            self.viz_widget.set_joysticks([])
            self.visual_widget.set_joysticks([])

    def load_bindings(self):
        """Load Star Citizen bindings from the selected instance"""
        instance = self.instance_combo.currentText()
        self.statusBar().showMessage(f"Loading bindings from {instance}...")

        bindings = self.binding_parser.load_bindings(instance)

        if bindings:
            joystick_bindings = bindings.get('joystick_bindings', [])
            num_bindings = len(joystick_bindings)

            if num_bindings > 0:
                # Store bindings for filtering
                self.current_bindings = joystick_bindings

                # Apply current mode filter
                self.apply_mode_filter()

                self.statusBar().showMessage(f"Loaded {num_bindings} joystick binding(s) from {instance}")
            else:
                self.current_bindings = []
                self.statusBar().showMessage(f"No joystick bindings found in {instance} profile")
        else:
            self.current_bindings = []
            self.statusBar().showMessage(f"No binding files found for {instance}")

    def on_mode_changed(self, index):
        """Handle mode selection change"""
        self.current_mode = self.mode_combo.itemData(index)
        self.apply_mode_filter()

    def swap_joysticks(self):
        """Swap the left and right joystick mapping"""
        self.viz_widget.swap_joystick_mapping()

        # Update status label
        if self.viz_widget.mapping_swapped:
            self.mapping_status.setText("⚡ Mapping SWAPPED: SC js1→RIGHT, js2→LEFT")
            self.swap_btn.setText("🔄 Swap L/R Mapping (SWAPPED)")
            self.swap_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
            """)
            self.statusBar().showMessage("Joystick mapping swapped - SC js1 and js2 reversed")
        else:
            self.mapping_status.setText("")
            self.swap_btn.setText("🔄 Swap L/R Mapping")
            self.swap_btn.setStyleSheet("")  # Reset to default
            self.statusBar().showMessage("Joystick mapping reset to normal")

        # Reload bindings with new mapping
        if self.current_bindings:
            self.apply_mode_filter()

    def apply_mode_filter(self):
        """Filter and display bindings based on selected mode"""
        from src.core.action_categories import categorize_action

        if not self.current_bindings:
            return

        # Filter bindings by mode
        if self.current_mode == ActionMode.ALL:
            filtered_bindings = self.current_bindings
        else:
            filtered_bindings = [
                binding for binding in self.current_bindings
                if categorize_action(binding.get('action', '')) == self.current_mode
            ]

        # Update button grid visualization
        self.viz_widget.update_bindings(filtered_bindings)

        # Update visual diagram with the same bindings and mapping
        if hasattr(self.viz_widget, 'sc_to_pygame_map') and self.viz_widget.sc_to_pygame_map:
            self.visual_widget.update_bindings(filtered_bindings, self.viz_widget.sc_to_pygame_map)

        # Update status bar
        total = len(self.current_bindings)
        shown = len(filtered_bindings)
        if self.current_mode == ActionMode.ALL:
            self.statusBar().showMessage(f"Showing all {total} binding(s)")
        else:
            self.statusBar().showMessage(f"Showing {shown} of {total} binding(s) for {self.current_mode.value}")
