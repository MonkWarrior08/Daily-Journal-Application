from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTimeEdit,
                               QDateEdit, QComboBox, QRadioButton,
                               QFrame, QListWidget, QAbstractItemView, QDialog,
                               QDialogButtonBox)

class MultiDialogue(QDialog):
    def __init__(self, parent=None, options=None, title="Select"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(300,300)
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

        if options:
            self.list_widget.addItems(options)

        layout.addWidget(self.list_widget)

        # ok and cancel button
        dialogue_butn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialogue_butn.accepted.connect(self.accept)
        dialogue_butn.rejected.connect(self.reject)
        layout.addWidget(dialogue_butn)

        self.setLayout(layout)

    def get_items(self):
        return [item.text() for item in self.list_widget.selectedItems()]
