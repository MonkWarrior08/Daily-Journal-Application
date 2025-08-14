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
        self.time_auto = QRadioButton("Automatic")
        self.time_custom = QRadioButton("Custom")
        self.time_auto.setChecked(True)
        self.time_auto.toggled.connect(self.on_time_mode_changed)
        self.time_custom.toggled.connect(self.on_time_mode_changed)

        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_auto)
        time_layout.addWidget(self.time_custom)
        time_layout.addWidget(self.time_edit)
        main_layout.addLayout(time_layout)

        # initialize time mode (disable editor when automatic)
        self.on_time_mode_changed()

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

        # fish details section (only for Food -> fish)
        fish_frame = QFrame()
        fish_layout = QHBoxLayout(fish_frame)
        fish_label = QLabel("Fish:")
        self.fish_type = QComboBox()
        self.fish_type.addItems(["basal fillet", "barramundi"])
        qty_label = QLabel("Qty:")
        self.fish_qty1 = QRadioButton("1")
        self.fish_qty2 = QRadioButton("2")
        self.fish_qty1.setChecked(True)

        fish_layout.addWidget(fish_label)
        fish_layout.addWidget(self.fish_type)
        fish_layout.addWidget(qty_label)
        fish_layout.addWidget(self.fish_qty1)
        fish_layout.addWidget(self.fish_qty2)
        fish_layout.addStretch()

        fish_frame.setVisible(False)
        self.fish_frame = fish_frame
        main_layout.addWidget(fish_frame)

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
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove_current_entry)
        self.remove_btn.setVisible(False)

        content_layout.addWidget(content_label)
        content_layout.addWidget(self.entry_combo)
        content_layout.addWidget(self.multi_select)
        content_layout.addWidget(self.remove_btn)
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

        # note and changes section
        note = QWidget()
        note_layout = QVBoxLayout(note)

        # Notes header
        note_header_layout = QHBoxLayout()
        note_label = QLabel("Notes:")
        self.note_butn = QPushButton("Save Notes")
        self.note_butn.clicked.connect(self.save_notes)
        note_header_layout.addWidget(note_label)
        note_header_layout.addWidget(self.note_butn)
        note_layout.addLayout(note_header_layout)

        # Notes text
        self.note_txt = QTextEdit()
        note_layout.addWidget(self.note_txt)

        # Changes header
        changes_header_layout = QHBoxLayout()
        changes_label = QLabel("Changes:")
        self.change_butn = QPushButton("Save Changes")
        self.change_butn.clicked.connect(self.save_changes)
        changes_header_layout.addWidget(changes_label)
        changes_header_layout.addWidget(self.change_butn)
        note_layout.addLayout(changes_header_layout)

        # Changes text
        self.change_txt = QTextEdit()
        note_layout.addWidget(self.change_txt)

        splitter.addWidget(note)

        splitter.setSizes([300,200])

        self.load_journal()

        # type options
        self.type_options = {
            "Daily": ["poop"],
            "Food": ["fish", "dumplings", "ginger", "plum", "pelimini", "olive paste", "cumin", "olive oil", "spinash", "pizza", "little fish", "cereal",
                     "peanut butter", "chips", "chips(sweet potatoes)", "tuna and beans", "chocolate", "orange", "yogurt(with cereal and berries), creatine",
                    "strawberries", "chips(corn)", "steak, noodles, salad with special sauce", "salmon(oyster sauce)"],
            "Activity": ["walk", "ice bath", "run"],
            "Supplement": [
                "vit c", "L-theanine", "DL-phenyl", "NAC", "Ashwagandha", "lithium", "Bacopa Monniery", "5-htp", "L-tryptophan",
                "slippery elm", "zinc", "lecithin", "p5p", "Alpha-GPC", "Methy-Folate", "vit d", "aniracetam", "digestive enzyme",
                 "fish oil", "john wort", "panadol", "bcaa", "bismuth potassium", "creatine", "silymarine", "magnesium", "moringa",
                 "gotu kola", "benfotiamine", "oxytocin", "CBD oil", "reishi", "rutin", "quercetin", "Holy basil"],
            "Discomfort": ["upper-abdominal pain", "anxiety", "fatigue", "testicular pain"],
            "Medication": ["Dexamphetamine", "Vyvanse (70mg)", "Lexapro", "Guanfacine", "Accutane"]
        }
        # saved multi-select stacks for Food and Supplement
        self.type_stacks = {"Food": [], "Supplement": []}
        # initialize current options
        self.update_options(self.type.currentText())
    

    def on_time_mode_changed(self):
        is_custom = self.time_custom.isChecked()
        self.time_edit.setEnabled(is_custom)
        # initialize editor starting from current time when switching modes
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
        if hasattr(self, 'change_txt'):
            self.change_txt.clear()

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()

            # Parse optional Notes: and Changes: sections
            journal_entry = content
            notes_text = ""
            changes_text = ""

            # find markers
            idx_notes = content.find("Notes:")
            idx_changes = content.find("Changes:")

            # determine journal portion as content before the earliest marker (if any)
            indices = [i for i in [idx_notes, idx_changes] if i != -1]
            if indices:
                first_idx = min(indices)
                journal_entry = content[:first_idx].strip()
            else:
                journal_entry = content

            # extract notes text
            if idx_notes != -1:
                start = idx_notes + len("Notes:")
                end = len(content) if idx_changes == -1 else idx_changes
                notes_text = content[start:end].strip()

            # extract changes text
            if idx_changes != -1:
                start = idx_changes + len("Changes:")
                end = len(content)
                changes_text = content[start:end].strip()

            self.preview_text.setPlainText(journal_entry)
            if notes_text:
                self.note_txt.setPlainText(notes_text)
            if changes_text and hasattr(self, 'change_txt'):
                self.change_txt.setPlainText(changes_text)

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

        is_food_or_supp = (type == "Supplement" or type == "Food")
        self.multi_select.setVisible(is_food_or_supp)
        self.remove_btn.setVisible(is_food_or_supp)
        self.entry_combo.setEditable(is_food_or_supp)
        self.activity_frame.setVisible(type == "Activity" or type == "Discomfort")
        self.rating_frame.setVisible(type == "Discomfort")
        
        # Hide dosage frame by default
        self.dosage_frame.setVisible(False)
        # Hide fish frame by default
        self.fish_frame.setVisible(False)
        
        # Show fish details when Food -> fish
        if type == "Food":
            self.entry_combo.currentTextChanged.connect(self.handle_food_change)
            self.handle_food_change(self.entry_combo.currentText())

        # Append saved stacks section for Food/Supplement
        if type in self.type_stacks and self.type_stacks[type]:
            base_count = self.entry_combo.count()
            self.entry_combo.insertSeparator(base_count)
            self.entry_combo_stack_sep_index = base_count
            self.entry_combo.addItem("Saved stacks")
            header_index = base_count + 1
            self.entry_combo_stack_header_index = header_index
            try:
                item = self.entry_combo.model().item(header_index)
                if item:
                    item.setEnabled(False)
            except Exception:
                pass
            self.entry_combo_stacks_first_index = header_index + 1
            self.entry_combo.addItems(self.type_stacks[type])

    def handle_medication_change(self, medication):
        self.dosage_frame.setVisible(medication == "Dexamphetamine")

    def handle_food_change(self, item):
        is_fish = (self._normalize_text(item) == "fish")
        self.fish_frame.setVisible(is_fish)
        if is_fish:
            self.fish_qty1.setChecked(True)

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
                combo_str = ", ".join(select_items)
                self.entry_combo.setCurrentText(combo_str)
                # save combo as stack if not already saved
                if current_type in self.type_stacks:
                    if not self._exists_in_list(self.type_stacks[current_type], combo_str):
                        self.type_stacks[current_type].append(combo_str)
                        # refresh options to show newly saved stack when relevant
                        if self.type.currentText() == current_type:
                            self.update_options(current_type)

    def add_entry(self):
        if self.time_custom.isChecked():
            time_str = self.time_edit.time().toString("h:mma").lower()
        else:
            time_str = QTime.currentTime().toString("h:mma").lower()
        entry_type = self.type.currentText()
        entry_combo = self.entry_combo.currentText().strip()

        # For Food/Supplement: auto-add new single item to options (case-insensitive, trimmed)
        if entry_type in ("Food", "Supplement") and entry_combo and "," not in entry_combo:
            if not self._exists_in_list(self.type_options[entry_type], entry_combo):
                sanitized = entry_combo.strip()
                self.type_options[entry_type].append(sanitized)
                # refresh options to include the new item
                self.update_options(entry_type)
                # ensure current text remains what user typed
                self.entry_combo.setCurrentText(sanitized)

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
                if entry_combo == "fish" and self.fish_frame.isVisible():
                    fish_kind = self.fish_type.currentText()
                    qty = 2 if self.fish_qty2.isChecked() else 1
                    if qty == 1:
                        entry = f"{time_str} ate fish({fish_kind})"
                    else:
                        entry = f"{time_str} ate {qty} fish({fish_kind})"
                else:
                    entry = f"{time_str} ate {entry_combo}"
            elif entry_type == "Medication":
                if entry_combo == "Dexamphetamine":
                    entry = f"{time_str} took medication - {entry_combo} (5mg)"
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

    def remove_current_entry(self):
        current_type = self.type.currentText()
        if current_type not in ("Food", "Supplement"):
            return
        idx = self.entry_combo.currentIndex()
        text = self.entry_combo.currentText()
        # Determine if removing a saved stack or a base item
        stacks_first = getattr(self, 'entry_combo_stacks_first_index', None)
        header_idx = getattr(self, 'entry_combo_stack_header_index', None)
        if stacks_first is not None and idx >= stacks_first:
            # remove from stacks
            if self._remove_from_list(self.type_stacks[current_type], text):
                self.update_options(current_type)
        else:
            # ignore if header somehow selected
            if header_idx is not None and idx == header_idx:
                return
            # remove from base options
            if self._remove_from_list(self.type_options[current_type], text):
                self.update_options(current_type)

    def _normalize_text(self, text: str) -> str:
        if text is None:
            return ""
        return text.casefold().strip()

    def _exists_in_list(self, items, candidate: str) -> bool:
        candidate_norm = self._normalize_text(candidate)
        for existing in items:
            if self._normalize_text(existing) == candidate_norm:
                return True
        return False

    def _remove_from_list(self, items, candidate: str) -> bool:
        candidate_norm = self._normalize_text(candidate)
        for i, existing in enumerate(items):
            if self._normalize_text(existing) == candidate_norm:
                del items[i]
                return True
        return False

    def save_preview(self):
        self.save_journal()
    
    def save_notes(self):
        notes_content = self.note_txt.toPlainText().strip()
        self.save_journal(notes_content=notes_content)

    def save_changes(self):
        changes_content = self.change_txt.toPlainText().strip()
        self.save_journal(changes_content=changes_content)

    def save_journal(self, notes_content=None, changes_content=None):
        filename = self.get_journal(self.date_edit.date())

        journal_content = self.preview_text.toPlainText()

        if notes_content is None:
            notes_content = self.note_txt.toPlainText().strip()
        if changes_content is None and hasattr(self, 'change_txt'):
            changes_content = self.change_txt.toPlainText().strip()

        # Build full content with optional sections
        full_content = journal_content.rstrip()
        if notes_content:
            full_content += f"\n\nNotes: {notes_content}"
        if changes_content:
            full_content += f"\n\nChanges: {changes_content}"

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
    