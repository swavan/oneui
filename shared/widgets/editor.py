import json
import os

from PyQt6.Qsci import QsciScintilla, QsciLexerJSON, QsciLexerPython, QsciLexerHTML, QsciLexerYAML, QsciLexerXML, \
    QsciLexerJavaScript
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

from shared.widgets.builder import template_loader


class SwaVanCodeEditor(QWidget):
    editor_close = pyqtSignal()
    editor_save = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        template_loader("templates/code_board.ui", self)
        self.__editor = QsciScintilla(self)
        self.__editor.setUtf8(True)
        self.__editor.setCaretLineVisible(True)
        self.__editor.setCaretWidth(2)
        self.__editor.setMarginLineNumbers(4, True)
        self.__editor.setObjectName("SwaVanCodeEditorUI")

        # 2. End-of-line mode
        # --------------------
        self.__editor.setTabWidth(4)
        self.__editor.setIndentationGuides(True)
        self.__editor.setTabIndents(True)
        self.__editor.setAutoIndent(True)
        self.__editor.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.__editor.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByText)
        self.__editor.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentIndented)

        self.__editor.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.__editor.setMarginWidth(0, "0000")

        self.language_list_combo.addItems(['JSON', 'Text', 'XML', 'HTML', 'Javascript', 'YML', 'Python'])
        self.language_list_combo.currentTextChanged.connect(lambda x: self.update_lexer(x))
        self.language_list_combo.setStyleSheet('''
            border: None;
        ''')

        self.code_editor_close.clicked.connect(self.close_editor)
        self.code_editor_close.hide()
        self.code_editor_save_btn.clicked.connect(self.save)
        self.code_editor_save_btn.hide()

        self.code_formatter_btn.clicked.connect(self.format_data)
        self.code_editor_holder.addWidget(self.__editor)
        self.set_style()

    def set_style(self):
        self.__editor.setContentsMargins(0, 0, 0, 0)
        self.__editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def update_lexer(self, language: str):
        language_lexer = {
            "python": QsciLexerPython,
            "html": QsciLexerHTML,
            "json": QsciLexerJSON,
            "yml": QsciLexerYAML,
            "xml": QsciLexerXML,
            "javascript": QsciLexerJavaScript
        }
        __lexer = language_lexer.get(language.lower(), None)
        if __lexer:
            self.__editor.setLexer(__lexer(self.__editor))
        else:
            self.__editor.setLexer(None)

    def format_data(self):
        if self.language_list_combo.currentText().lower() == "json" and self.text:
            try:
                json_object = json.loads(self.text)
                self.text = json.dumps(json_object, indent=4)
            except (Exception):
                pass
            finally:
                pass

    @property
    def text(self) -> str:
        return self.__editor.text()

    @text.setter
    def text(self, text):
        self.__editor.setText(text)

    def disable_language(self):
        self.language_list_combo.isEnabled(False)

    def select_language(self, language: str):
        self.language_list_combo.setCurrentText(language)

    def show_close(self):
        self.code_editor_close.show()

    def form_view(self):
        self.show_save()
        self.show_close()
        self.language_list_combo.hide()
        self.code_formatter_btn.hide()

    def control_view(self):
        self.code_editor_save_btn.hide()
        self.code_editor_close.hide()
        self.language_list_combo.show()
        self.code_formatter_btn.show()

    def show_save(self):
        self.code_editor_save_btn.show()

    def close_editor(self):
        self.editor_close.emit()

    def save(self):
        self.editor_save.emit(self.text)
