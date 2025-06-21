import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTimeEdit,
                               QDateEdit, QComboBox, QRadioButton,
                               QFrame, QTextEdit, QSplitter)
from PySide6.QtCore import Qt, QTime, QDate
from multi import MultiDialogue


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
        self.type.addItems(["Daily", "Food", "Drink", "Activity", "Supplement", "Discomfort", "Medication"])
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

        # rating section
        rating_frame = QFrame()
        rating_layout = QHBoxLayout(rating_frame)
        rate_label = QLabel("Rating:")
        
        self.rating_1 = QRadioButton("1")
        self.rating_2 = QRadioButton("2")
        self.rating_3 = QRadioButton("3")
        self.rating_4 = QRadioButton("4")
        self.rating_1.setChecked(True)

        rating_layout.addWidget(rate_label)
        rating_layout.addWidget(self.rating_1)
        rating_layout.addWidget(self.rating_2)
        rating_layout.addWidget(self.rating_3)
        rating_layout.addWidget(self.rating_4)
        rating_layout.addStretch()

        # dosage section
        dosage_frame = QFrame()
        dosage_layout = QHBoxLayout(dosage_frame)
        dosage_label = QLabel("Dosage:")

        self.dosage1 = QRadioButton("5")
        self.dosage2 = QRadioButton("10")
        self.dosage3 = QRadioButton("15")
        self.dosage1.setChecked(True)

        dosage_layout.addWidget(dosage_label)
        dosage_layout.addWidget(self.dosage1)
        dosage_layout.addWidget(self.dosage2)
        dosage_layout.addWidget(self.dosage3)
        dosage_layout.addStretch()

        # setvisible and main layout to activity, rating and dosage
        activity_frame.setVisible(False)
        self.activity_frame = activity_frame
        main_layout.addWidget(activity_frame)

        rating_frame.setVisible(False)
        self.rating_frame = rating_frame
        main_layout.addWidget(rating_frame)

        dosage_frame.setVisible(False)
        self.dosage_frame = dosage_frame
        main_layout.addWidget(dosage_frame)

        # entry section
        content_layout = QHBoxLayout()
        content_label = QLabel("Entry:")
        
        self.entry_combo = QComboBox()
        self.entry_combo.setEditable(False) # entry not editable
        self.entry_combo.setMinimumWidth(300)

        # multi-select for supplement and food
        self.multi_select = QPushButton("select(multi)")
        self.multi_select.clicked.connect(self.open_multi_select)
        self.multi_select.setVisible(True)

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
    
        # save button for preview edits
        self.preview_save_btn = QPushButton("Save edit")
        self.preview_save_btn.clicked.connect(self.save_preview)

        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_text)
        preview_layout.addWidget(self.preview_save_btn)
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
            "Daily": ["Woke up", "poop"],
            "Food": ["fish", "dumplings", "ginger", "plum", "pelimini", "olive paste", "cumin", "olive oil", "spinash", "pizza", "little fish", "cereal",
                     "peanut butter", "chips", "chips(sweet potatoes)", "tuna and beans", "chocolate", "orange", "yogurt(with cereal and berries), creatine",
                    "strawberries", "chips(corn)", "steak, noodles, salad with special sauce", "salmon(oyster sauce)"],
            "Drink": ["green tea", "coconut water", "fruit juice", "kefir", "milk", "protein powder"],
            "Activity": ["walk", "ice bath", "run", "tACS", "tDCS", "RLT"],
            "Supplement": [
                "vit c", "L-theanine", "DL-phenyl", "NAC", "Ashwagandha", "lithium", "Bacopa Monniery", "5-htp", "L-tryptophan",
                "slippery elm", "zinc", "lecithin", "p5p", "Alpha-GPC", "Methy-Folate", "vit d", "aniracetam", "digestive enzyme",
                 "fish oil", "john wort", "panadol", "bcaa", "bismuth potassium", "creatine", "silymarine", "magnesium", "moringa",
                 "gotu kola", "benfotiamine", "oxytocin", "CBD oil", "reishi", "rutin", "quercetin", "Holy basil"],
            "Discomfort": ["upper-abdominal pain", "testicular pain", "anxiety", "fatigue", "tongue reaction"],
            "Medication": ["Dexamphetamine", "Vyvanse (70mg)", "Lexapro", "Guanfacine", "Accutane", "Candesartan", "LDN"]
        }
        # initialize current options
        self.update_options(self.type.currentText())
    

    def current_time(self):
        self.time_edit.setTime(QTime.currentTime())


    def get_journal(self, date=None):
        if not date:
            date = self.date_edit.date().toString("dd-MM-yyyy")
        else:
            date = date.toString("dd-MM-yyyy")

        if not os.path.exists("Journal"):
            os.makedirs("Journal")

        return os.path.join("Journal", f"{date}.txt")
    
    def load_journal(self):
        filename = self.get_journal(self.date_edit.date())
        self.preview_text.clear()
        self.note_txt.clear()

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()

            # check if Notes: section exist
            if "Notes:" in content:
                parts = content.split("Notes:", 1) #split between journal and notes. 
                journal_entry = parts[0].strip()
                notes = parts[1].strip()

                self.preview_text.setPlainText(journal_entry)
                self.note_txt.setPlainText(notes)
            
            else:
                self.preview_text.setPlainText(content)

        else: #if empty, add date header
            date_str = self.date_edit.date().toString("dd-MM-yyyy")
            header_date = f"Date: {date_str}\n"
            self.preview_text.setPlainText(header_date)

    def update_options(self, type):
        self.entry_combo.clear()
        self.entry_combo.addItems(self.type_options[type])

        # Disconnect any existing connections to prevent multiple signals
        try:
            self.entry_combo.currentTextChanged.disconnect()
        except:
            pass

        self.multi_select.setVisible(type == "Supplement" or type == "Food")
        self.entry_combo.setEditable(type == "Supplement" or type == "Food")
        self.activity_frame.setVisible(type == "Activity" or type == "Discomfort")
        self.rating_frame.setVisible(type == "Discomfort")
        
        # Hide dosage frame by default
        self.dosage_frame.setVisible(False)
        
        # Show dosage frame when Dexamphetamine is selected
        if type == "Medication":
            self.entry_combo.currentTextChanged.connect(self.handle_medication_change)
            # Check initial value
            self.handle_medication_change(self.entry_combo.currentText())

    def handle_medication_change(self, medication):
        self.dosage_frame.setVisible(medication == "Dexamphetamine")

    def open_multi_select(self):
        current_type = self.type.currentText()
        dialog = MultiDialogue(
            self,
            options=self.type_options[current_type],
            title="Select {current_type}"
        )
        if dialog.exec():
            select_items = dialog.get_items()
            
            if select_items:
                self.entry_combo.setCurrentText(", ".join(select_items))

    def add_entry(self):
        time_str = self.time_edit.time().toString("h:mma").lower()
        entry_type = self.type.currentText()
        entry_combo = self.entry_combo.currentText().strip()

        if entry_type == "Daily":
            entry = f"{time_str} {entry_combo}"
        
        elif entry_type == "Activity":
            if not entry_combo:
                return
            
            activity_type = "started" if self.activity_start.isChecked() else "finished"
            entry = f"{time_str} {activity_type} {entry_combo}"
        
        elif entry_type == "Discomfort":
            if not entry_combo:
                return
            activity_type = "started" if self.activity_start.isChecked() else "finished"
            if self.rating_1.isChecked():
                entry = f"{time_str} {activity_type} having {entry_combo} rating: 1"
            elif self.rating_2.isChecked():
                entry = f"{time_str} {activity_type} having {entry_combo} rating 2"
            elif self.rating_3.isChecked():
                entry = f"{time_str} {activity_type} having {entry_combo} rating 3"
            else:
                entry = f"{time_str} {activity_type} having {entry_combo} rating 4"

        else:
            if not entry_combo:
                return
            
            if entry_type == "Supplement":
                entry = f"{time_str} took {entry_combo}" 
            elif entry_type == "Drink":
                entry = f"{time_str} drink {entry_combo}"
            elif entry_type == "Food":
                entry = f"{time_str} ate {entry_combo}"
            elif entry_type == "Medication":
                if entry_combo == "Dexamphetamine":
                    if self.dosage1.isChecked():
                        entry = f"{time_str} took medication - {entry_combo} (5mg)"
                    elif self.dosage2.isChecked():
                        entry = f"{time_str} took medication - {entry_combo} (10mg)"
                    else:
                        entry = f"{time_str} took medication - {entry_combo} (15mg)"
                else:
                    entry = f"{time_str} took medication - {entry_combo}"
            else:
                return
        
        current_text = self.preview_text.toPlainText()
        if not current_text.strip():
            date_str = self.date_edit.date().toString("dd-MM-yyyy")
            current_text = f"Date: {date_str}\n"

        else:
            if not current_text.endswith("\n"):
                current_text += "\n"

        update_text = current_text + entry + "\n"
        self.preview_text.setPlainText(update_text)

        self.save_journal()
        self.current_time()            

    def save_preview(self):
        self.save_journal()
    
    def save_notes(self):
        notes_content = self.note_txt.toPlainText().strip()
        self.save_journal(notes_content)

    def save_journal(self, notes_content=None):
        filename = self.get_journal(self.date_edit.date())

        journal_content = self.preview_text.toPlainText()

        if notes_content is None:
            notes_content = self.note_txt.toPlainText().strip()
        
        if notes_content:
            full_content = f"{journal_content.rstrip()}\n\nNotes: {notes_content}"
        else:
            full_content = journal_content

        with open(filename, 'w') as file:
            file.write(full_content)

    def closeEvent(self, event):
        self.save_journal()
        super().closeEvent(event)
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Journal()
    window.show()
    sys.exit(app.exec())
    