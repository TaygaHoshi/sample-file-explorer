#!./bin/python3

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QListWidget, QMainWindow, QGridLayout, QWidget, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from explorer import *
from info_gather import *
from css import *
from settings import SettingHandler

class GUI:
    # core gui
    app = QApplication([])
    clipboard = app.clipboard()
    main_window = QMainWindow()
    main_widget = QWidget()
    main_layout = QGridLayout()
    searchwin = None

    # widgets
    path_list = None
    dynamic_info_label = QLabel()
    static_info_label = QLabel(text=f"Kernel\n{get_kernel_version()}\n\nDesktop Environment\n{get_desktop_environment().capitalize()}")
    current_dir_label = QLabel(text="/")
    copy_path_button = QPushButton(text="Copy")
    search_button = QPushButton(text="Search")
    search_textbox = QLineEdit(placeholderText="Search within current directory.")
    hidden_files_checkbox = QCheckBox(text="Show hidden files")
    continue_from_last_checkbox = QCheckBox(text="Continue from last directory")

    # fonts
    default_font = QFont("Noto Sans", 16)

    # settings
    setting_handler = SettingHandler(get_current_dir())

    def init_settings(self):
        # Loads settings from the setting file and apply to widgets as necessary
        # Also initializes widgets for filters and settings
        self.hidden_files_checkbox.setStyleSheet(checkbox_css)
        self.hidden_files_checkbox.clicked.connect(self.handle_hidden_files)

        self.continue_from_last_checkbox.setStyleSheet(checkbox_css)
        self.continue_from_last_checkbox.clicked.connect(self.handle_continue_from_last_path)

        self.setting_handler.load_settings()
        log(self.setting_handler.settings["show_hidden_files"], "i")
        log(self.setting_handler.settings["continue_from_last"], "i")

        # Apply to widgets
        self.hidden_files_checkbox.setChecked("True" == self.setting_handler.settings["show_hidden_files"])
        self.continue_from_last_checkbox.setChecked("True" == self.setting_handler.settings["continue_from_last"])
        
        # Set starting path
        if not self.continue_from_last_checkbox.isChecked():
            open_path(normalize_out(run("echo $HOME")))
        else:
            last_path = self.setting_handler.settings["last_dir"]
            open_path(normalize_out(run(f"echo {last_path}")))



    def update_cwd_label(self):
        # Updates the header
        self.current_dir_label.setText(f"{get_current_dir()}")
        self.current_dir_label.update()

    def get_list(self):
        # Works similarly to basic functionalities of "ls" and "ls -a"
        # Basically, returns the content of current directory
        # ".." is used as a "go up one level" button.
        all_list = get_all()

        if not self.hidden_files_checkbox.isChecked():
            all_list = [x for x in all_list if not x.startswith(".")]

        all_list.sort(key=lambda v: v.upper())
        return [".."] + all_list

    def update_path_list(self):
        # Updates path list with the contents of current directory
        self.path_list.clear()
        self.path_list.addItems(self.get_list())

    def handle_hidden_files(self):
        # Handles toggling hidden_files_checkbox
        self.update_path_list()
        self.setting_handler.change_setting("show_hidden_files", str(self.hidden_files_checkbox.isChecked()))

    def handle_continue_from_last_path(self):
        self.setting_handler.change_setting("continue_from_last", str(self.continue_from_last_checkbox.isChecked()))

    def list_doubleclick(self, item):
        # Handles double clicking path_list
        _result = open_path(get_current_dir() + "/" + item.text())
        if _result == 0:
            self.update_cwd_label()
            self.update_path_list()
            self.path_list.setCurrentRow(0)
            self.setting_handler.change_setting("last_dir", get_current_dir())

    def manual_change_cwd(self, path):
        # Handles changing cwd and updating path_list
        _result = open_path(path)
        if _result == 0:
            self.update_cwd_label()
            self.update_path_list()
            self.path_list.setCurrentRow(0)

    def copy_current_path(self):
        # Handles clicking copy_path_button
        try:
            self.clipboard.clear()
            self.clipboard.setText(self.current_dir_label.text())
            log("Copied current path to clipboard.", "i")
        except:
            log("Unable to copy current path to clipboard.", "e")

    def search_file(self):
        # Handles clicking search_button
        self.searchwin = SearchWindow()
        self.searchwin.generate_results(self.search_textbox.text())
        self.search_textbox.setText("")

    def init_list(self):
        # Initializes path_list
        try:
            log("Creating the path list view.", "i")
            self.path_list = QListKeyboard(self)
            self.path_list.setStyleSheet(list_css)
            self.path_list.verticalScrollBar().setStyleSheet(scroll_css)
            self.path_list.horizontalScrollBar().setStyleSheet(scroll_css)
            self.path_list.setFont(self.default_font)
            self.path_list.addItems(self.get_list())
            self.path_list.itemActivated.connect(self.list_doubleclick)
            self.path_list.setCurrentRow(0)
        except:
            log("Unable to create the path list view.", "e")

    def init_labels(self):
        # Initializes all labels
        try:
            log("Creating labels.", "i")
            
            # sidebar labels
            self.dynamic_info_label.setStyleSheet(info_css)
            self.dynamic_info_label.setFont(self.default_font)
            self.dynamic_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.static_info_label.setStyleSheet(info_css)
            self.static_info_label.setFont(self.default_font)
            self.static_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # cwd header label
            self.current_dir_label.setStyleSheet(header_css)
            self.update_cwd_label()
        except:
            log("Unable to create labels.", "e")

    def init_buttons(self):
        # Initializes all buttons
        try:
            log("Creating buttons.", "i")
            self.copy_path_button.clicked.connect(self.copy_current_path)
            self.copy_path_button.setStyleSheet(copy_button_css)
            self.copy_path_button.setFont(self.default_font)

            self.search_button.clicked.connect(self.search_file)
            self.search_button.setStyleSheet(search_button_css)
            self.search_button.setFont(self.default_font)

            self.search_textbox.setStyleSheet(list_css)
            self.search_textbox.setFont(self.default_font)
            self.search_textbox.returnPressed.connect(self.search_file)
        except:
            log("Unable to create buttons.", "e")

    def __init__(self):
        # START READING HERE
        # ENTRY POINT

        # Build GUI
        log("Creating the window.", "i")
        self.main_window.setWindowTitle("Tayy File Explorer")
        self.main_window.resize(1280, 720)
        self.main_window.setCentralWidget(self.main_widget)

        log("Creating widgets.", "i")
        self.init_settings()
        self.init_list()
        self.init_labels()
        self.init_buttons()

        log("Applying the layout.", "i")
        self.main_layout.addWidget(self.current_dir_label, 0, 0)
        self.main_layout.addWidget(self.copy_path_button, 0, 1)
        self.main_layout.addWidget(self.hidden_files_checkbox, 1, 0)
        self.main_layout.addWidget(self.continue_from_last_checkbox, 1, 1)
        self.main_layout.addWidget(self.path_list, 2, 0, 2, 2)
        self.main_layout.addWidget(self.static_info_label, 2, 2)
        self.main_layout.addWidget(self.dynamic_info_label, 3, 2)
        self.main_layout.addWidget(self.search_textbox, 4, 0)
        self.main_layout.addWidget(self.search_button, 4, 1)

        self.main_widget.setLayout(self.main_layout)

        log("Starting.", "i")
        self.main_window.show()
        update_dynamic_labels(self.dynamic_info_label, self.main_window)
        self.path_list.setFocus()

        self.app.exec()

class SearchWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)

    def list_doubleclick(self, item):
        open_file(item.text())

    def generate_results(self, filename):

        results_list = QListWidget()
        results = []

        self.resize(800, 600)
        self.setWindowTitle("Search Results")
        self.setLayout(QGridLayout())

        results = search_file(filename)
        results.sort(key=lambda v: v.upper())

        results_list.addItems(results)
        results_list.setStyleSheet(list_css)
        results_list.verticalScrollBar().setStyleSheet(scroll_css)
        results_list.horizontalScrollBar().setStyleSheet(scroll_css)
        results_list.itemActivated.connect(self.list_doubleclick)

        self.layout().addWidget(results_list, 0, 0)

        self.show()

class QListKeyboard(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self)
        self.parent = parent
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return:
            self.parent.list_doubleclick(self.currentItem())
        elif e.key() == Qt.Key.Key_Down:
            self.setCurrentRow(self.currentRow() + 1)
        elif e.key() == Qt.Key.Key_Up and self.currentRow() >= 1:
            self.setCurrentRow(self.currentRow() - 1)

GUI()
