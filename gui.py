from PyQt6.QtWidgets import QApplication, QLabel, QListWidget, QMainWindow, QGridLayout, QWidget, QPushButton, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from explorer import *
from info_gather import *
from css import *

class GUI:
    # core gui
    app = QApplication([])
    clipboard = app.clipboard()
    main_window = QMainWindow()
    main_widget = QWidget()
    main_layout = QGridLayout()
    searchwin = None

    # widgets
    path_list = QListWidget()
    dynamic_info_label = QLabel()
    static_info_label = QLabel(text=f"Kernel\n{get_kernel_version()}\n\nDesktop Environment\n{get_desktop_environment().capitalize()}")
    current_dir_label = QLabel(text="/")
    copy_path_button = QPushButton(text="Copy")
    search_button = QPushButton(text="Search")
    search_textbox = QLineEdit(placeholderText="Search within current directory.")

    # fonts
    default_font = QFont("Noto Sans", 16)

    def update_cwd_label(self):
        self.current_dir_label.setText(f"{get_current_dir()}")
        self.current_dir_label.update()

    def get_list(self):
        all_list = get_all()
        all_list.sort(key=lambda v: v.upper())
        return [".."] + all_list

    def list_doubleclick(self, item):
        open_path(get_current_dir() + "/" + item.text())
        self.update_cwd_label()
        
        self.path_list.clear()
        self.path_list.addItems(self.get_list())

    def copy_current_path(self):
        try:
            self.clipboard.clear()
            self.clipboard.setText(self.current_dir_label.text())
            log("Copied current path to clipboard.", "i")
        except:
            log("Unable to copy current path to clipboard.", "e")

    def search_file(self):
        self.searchwin = SearchWindow()
        self.searchwin.generate_results(self.search_textbox.text())
        self.search_textbox.setText("")
        
    def init_list(self):
        try:
            log("Creating the path list view.", "i")
            self.path_list.setStyleSheet(list_css)
            self.path_list.verticalScrollBar().setStyleSheet(scroll_css)
            self.path_list.horizontalScrollBar().setStyleSheet(scroll_css)
            self.path_list.setFont(self.default_font)
            self.path_list.addItems(self.get_list())
            self.path_list.itemActivated.connect(self.list_doubleclick)
        except:
            log("Unable to create the path list view.", "e")

    def init_labels(self):
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
        except:
            log("Unable to create buttons.", "e")

    def __init__(self):
        # Set starting location to $HOME
        open_path(normalize_out(run("echo $HOME")))

        log("Creating the window.", "i")
        self.main_window.setWindowTitle("Tayy File Explorer")
        self.main_window.resize(1280, 720)
        self.main_window.setCentralWidget(self.main_widget)

        log("Creating widgets.", "i")
        self.init_list()
        self.init_labels()
        self.init_buttons()

        log("Applying the layout.", "i")
        self.main_layout.addWidget(self.current_dir_label, 0, 0)
        self.main_layout.addWidget(self.copy_path_button, 0, 1)
        self.main_layout.addWidget(self.path_list, 1, 0, 2, 1)
        self.main_layout.addWidget(self.static_info_label, 1, 1)
        self.main_layout.addWidget(self.dynamic_info_label, 2, 1)
        self.main_layout.addWidget(self.search_textbox, 3, 0)
        self.main_layout.addWidget(self.search_button, 3, 1)
        self.main_widget.setLayout(self.main_layout)

        log("Starting.", "i")
        self.main_window.show()
        update_dynamic_labels(self.dynamic_info_label, self.main_window)
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

GUI()