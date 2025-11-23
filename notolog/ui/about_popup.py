"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: About the app dialog class for displaying app's info to the user.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QEvent, QUrl
from PySide6.QtGui import QPixmap, QCursor, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QLabel, QFrame, QPushButton, QWidget
from PySide6.QtWidgets import QSizePolicy

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from functools import partial

import logging


class AboutPopup(QDialog):
    def __init__(self, parent=None):
        # Popup type may block a screen lock action.
        # Popup is not closing on macOS and no pointing hand cursor.
        # Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint
        super().__init__(parent, Qt.WindowType.Dialog)

        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('about_popup')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # Theme helper
        self.theme_helper = ThemeHelper()

        self.init_ui()

        self.setModal(True)  # Set the dialog modal to manage focus more effectively

        # self.adjustSize()  # Adjust size based on content
        """
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.25)
        dialog_height = int(main_window_size.height() * 0.25)
        # Set dialog size derived from the main window size
        self.setMinimumSize(dialog_width, dialog_height)
        """

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if self.sizeHint().isValid():
            self.setMinimumSize(self.sizeHint())

    def init_ui(self):
        # Minimal About popup: only app icon, name and usage instructions
        self.setWindowTitle(self.lexemes.get('popup_about_title') or AppConfig().get_app_name())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        self.setLayout(layout)

        # (logo removed per user request)

        # App name (fixed)
        app_name = QLabel("TagIT", self)
        app_name_font = self.font()
        app_name_font.setPointSizeF(app_name_font.pointSize() * 1.5)
        app_name.setFont(app_name_font)
        app_name.setObjectName('app_name')
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_name, alignment=Qt.AlignmentFlag.AlignCenter)

        # Usage / quick start
        usage_text = self.lexemes.get('popup_about_usage')
        if not usage_text:
            usage_text = (
                "Uporaba:\n"
                "- Za navigacijo po mapah in dokumentih uporabljaj puščico navzgor/navzdol.\n"
                "- Za odprtje mape uporabi puščico v desno\n"
                "- Za izhod iz mape uporabi puščico levo\n"
                "- Datoteko po urejanju shrani s Ctrl + S\n"
            )

        usage_label = QLabel(usage_text, self)
        usage_label.setObjectName('about_usage')
        usage_label.setWordWrap(True)
        usage_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        usage_label.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(usage_label)

        # Apply stylesheet
        self.setStyleSheet(self.theme_helper.get_css('about_popup'))

    def eventFilter(self, obj, event):
        # Close the dialog when clicking outside it
        if (event.type() == QEvent.Type.MouseButtonPress
                or event.type() == QEvent.Type.Leave
                or event.type() == QEvent.Type.FocusOut):
            self.close()
        return super().eventFilter(obj, event)
