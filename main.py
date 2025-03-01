import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTimeEdit,
                               QDateEdit, QComboBox, QRadioButton,
                               QFrame, QListWidget, QAbstractItemView, QDialog,
                               QDialogButtonBox, QTextEdit, QSplitter)
from PySide6.QtCore import Qt, QTime, QDate
from mutli import MultiDialogue


class Journal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Journal")
        self.setMinimumSize(600,600)

        #main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # date section
        date_layout = QHBoxLayout()
        date_label = QLabel('Date:')
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)

        self.date_edit.dateChanged.connect(self.load_journal)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        main_layout.addLayout(date_layout)

        # time section
        time_layout = QHBoxLayout()
        time_label = QLabel('Time:')

        self.time_edit = QTimeEdit(QTime.currentTime())
        self.current_time_btn = QPushButton("Current Time")
        self.current_time_btn.clicked.connect(self.current_time)

        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)
        time_layout.addWidget(self.current_time_btn)
        main_layout.addLayout(time_layout)

        # type section
        type_layout = QHBoxLayout()
        type_label = QLabel('Type:')
        self.type = QComboBox()
        self.type.addItems(["Wake up","Food","Activity","Supplement","Discomfort","Medication"])
        self.type.currentTextChanged.connect(self.update_options)

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type)
        main_layout.addLayout(type_layout)

        # activity section (start / end)
        activity_frame = QFrame()
        activity_layout = QHBoxLayout(activity_frame)
        activity_label = QLabel("Activity Type:")

        self.activity_start = QRadioButton("Start")
        self.activity_end = QRadioButton("End")
        self.activity_start.setChecked(True) # default as "Start"

        activity_layout.addWidget(activity_label)
        activity_layout.addWidget(self.activity_start)
        activity_layout.addWidget(self.activity_end)
        activity_layout.addStretch()

        activity_frame.setVisible(False)
        self.activity_frame = activity_frame
        main_layout.addWidget(activity_frame)

        # entry section
        content_layout = QHBoxLayout()
        content_label = QLabel("Entry:")
        
        self.entry_combo = QComboBox()
        self.entry_combo.setEditable(False) # entry not editable
        self.entry_combo.setMinimumWidth(300)

        # multi-select for supplement
        self.multi_select = QPushButton("select(multi)")
        self.multi_select.clicked.connect(self.open_multi_select)
        self.multi_select.setVisible(False)

        content_layout.addWidget(content_label)
        content_layout.addWidget(self.entry_combo)
        content_layout.addWidget(self.multi_select)
        main_layout.addLayout(content_layout)

        # add entry button
        self.entry_butn = QPushButton("Add Entry")
        self.entry_butn.clicked.connect(self.add_entry)
        main_layout.addWidget(self.entry_butn)

        # splitter for preview and note section
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        main_layout.addWidget(splitter, 1) #stretch factor of 1

        #journal preview section
        preview = QWidget()
        preview_layout = QVBoxLayout(preview)
        preview_label = QLabel("Journal")
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)

        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_text)
        splitter.addWidget(preview)

        # note section
        note = QWidget()
        note_layout = QVBoxLayout(note)
        note_header_layout = QHBoxLayout()
        note_label = QLabel("Notes:")
        self.note_butn = QPushButton("Save Notes")
        self.note_butn.clicked.connect(self.save_notes)
        
        note_header_layout.addWidget(note_label)
        note_header_layout.addWidget(self.note_butn)
        note_layout.addLayout(note_header_layout)

        self.note_txt = QTextEdit()
        note_layout.addWidget(self.note_txt)
        splitter.addWidget(note)

        splitter.setSizes([300,200])

        self.load_journal()

        # type options
        self.type_options = {
            "Wake up": [],
            "Food": ["fish", "dumplings"],
            "Activity": ["run", "stretch", "ice bath", "walk"],
            "Supplement": ["usual(2 Ashwagandha, 1 Alpha-GPC, Methyl-Folate, p5p, NAC)", "L-theanine", "NAC", "Ashwagandha", "lithium", "Bacopa Monniery", "5-htp and L-tryptophan"],
            "Discomfort": ["upper-abdominal pain", "testicular pain"],
            "Medication": ["Dexamphetamine", "Lexapro", "Guanfacine", "Accutane"]
        }
        # initialize current options
        self.update_options(self.type.currentText())

    def current_time(self):
        self.time_edit.setTime(QTime.currentTime())

    def load_journal(self):

        pass
    
    def update_options(self, type):
        self.entry_combo.clear()
        self.entry_combo.addItems(self.type_options[type])

        self.multi_select.setVisible(type == "Supplement")
        self.activity_frame.setVisible(type == "Activity")

    def open_multi_select(self):
        dialog = MultiDialogue(
            self,
            options=self.type_options["Supplement"],
            title="Select Supplements"
        )
        if dialog.exec():
            select_items = dialog.get_items()
            
            if select_items:
                self.entry_combo.setCurrentText(", ".join(select_items))

    def add_entry(self):
        pass

    def save_notes():
        pass


    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Journal()
    window.show()
    sys.exit(app.exec())
    