import sys
import os
import json
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QTimeEdit,
                               QDateEdit, QComboBox, QRadioButton,
                               QFrame, QTextEdit, QSplitter, QTableWidget,
                               QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt, QTime, QDate, QTimer
from multi import MultiDialogue, MultiDialogueWithCounts


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
        note_layout.addWidget(changes_label)

        # Changes text
        self.change_txt = QTextEdit()
        note_layout.addWidget(self.change_txt)

        splitter.addWidget(note)

        splitter.setSizes([300,200])

        # type options
        self.type_options = {
            "Daily": ["poop"],
            "Food": ["fish", "dumplings", "ginger", "plum", "olive paste", "cumin", "olive oil", "spinash", "pizza", "little fish", "cereal",
                     "peanut butter", "chips", "chips(sweet potatoes)", "tuna and beans", "chocolate", "orange", "yogurt(with cereal and berries), creatine",
                    "strawberries", "chips(corn)", "steak, noodles, salad with special sauce", "salmon(oyster sauce)"],
            "Activity": ["walk", "ice bath", "run", "uni"],
            "Supplement": [
                "vit c", "L-theanine", "DL-phenyl", "NAC", "Ashwagandha", "lithium", "Bacopa Monniery", "5-htp", "L-tryptophan",
                "slippery elm", "zinc", "lecithin", "p5p", "Alpha-GPC", "Methy-Folate", "vit d", "aniracetam", "digestive enzyme",
                 "fish oil", "john wort", "panadol", "bcaa", "bismuth potassium", "creatine", "silymarine", "magnesium", "moringa",
                 "gotu kola", "benfotiamine", "oxytocin", "CBD oil", "reishi", "rutin", "quercetin", "Holy basil"],
            "Discomfort": ["upper-abdominal pain", "anxiety", "fatigue", "testicular pain"],
            "Medication": ["Dexamphetamine", "Vyvanse (70mg)", "Lexapro", "Guanfacine", "Accutane"]
        }
        
        # Load saved type options from file
        self.load_type_options()
        
        # saved multi-select stacks for Food and Supplement
        self.type_stacks = {"Food": [], "Supplement": []}
        # Load saved stacks from file
        self.load_type_stacks()
        
        # Active discomforts tracking
        self.active_discomforts = {}  # {discomfort_name: {"rating": int, "start_time": str, "start_date": str}}
        
        # Load active discomforts from file
        self.load_active_discomforts()
        
        # Setup timer to update discomfort durations
        self.discomfort_timer = QTimer()
        self.discomfort_timer.timeout.connect(self.update_discomfort_table)
        self.discomfort_timer.start(60000)  # Update every minute
        
        # Add discomfort tracking section
        self.setup_discomfort_tracking()
        main_layout.addWidget(self.discomfort_tracking_frame)
        
        # initialize current options
        self.update_options(self.type.currentText())
        
        # Load journal after everything is initialized
        self.load_journal()
        
        # Initialize discomfort table display
        self.update_discomfort_table()
    

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
        
        # Update discomfort table when date changes
        if hasattr(self, 'discomfort_table'):
            self.update_discomfort_table()

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
        
        # Clear the entry field when switching to Food or Supplement
        if is_food_or_supp:
            self.entry_combo.setCurrentText("")
        
        self.activity_frame.setVisible(type == "Activity" or type == "Discomfort")
        self.rating_frame.setVisible(type == "Discomfort")
        
        # Always show discomfort tracking (no need to hide/show based on type)
        
        # Update discomfort table to ensure it's current
        if hasattr(self, 'discomfort_table'):
            self.update_discomfort_table()
        
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
        
        # Use MultiDialogueWithCounts for supplements, regular MultiDialogue for others
        if current_type == "Supplement":
            dialog = MultiDialogueWithCounts(
                self,
                options=self.type_options[current_type],
                title=f"Select {current_type}"
            )
        else:
            dialog = MultiDialogue(
                self,
                options=self.type_options[current_type],
                title=f"Select {current_type}"
            )
            
        if dialog.exec():
            if current_type == "Supplement":
                # Get items with counts for supplements
                select_items_with_counts = dialog.get_items_with_counts()
                if select_items_with_counts:
                    # Format with counts (only show count if > 1)
                    formatted_items = []
                    for item, count in select_items_with_counts:
                        if count == 1:
                            formatted_items.append(item)
                        else:
                            formatted_items.append(f"{count} {item}")
                    
                    combo_str = ", ".join(formatted_items)
                    self.entry_combo.setCurrentText(combo_str)
                    
                    # Save combo as stack if not already saved
                    if current_type in self.type_stacks:
                        if not self._exists_in_list(self.type_stacks[current_type], combo_str):
                            self.type_stacks[current_type].append(combo_str)
                            # Save type stacks to persist the new stack
                            self.save_type_stacks()
                            # refresh options to show newly saved stack when relevant
                            if self.type.currentText() == current_type:
                                self.update_options(current_type)
            else:
                # Regular handling for non-supplement types
                select_items = dialog.get_items()
                
                if select_items:
                    combo_str = ", ".join(select_items)
                    self.entry_combo.setCurrentText(combo_str)
                    # save combo as stack if not already saved
                    if current_type in self.type_stacks:
                        if not self._exists_in_list(self.type_stacks[current_type], combo_str):
                            self.type_stacks[current_type].append(combo_str)
                            # Save type stacks to persist the new stack
                            self.save_type_stacks()
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
                # Save type options to persist the new item
                self.save_type_options()
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
            
            # Handle discomfort tracking
            if activity_type == "started":
                # Add to active discomforts if not already there, or update if exists
                rating = 1
                if self.rating_2.isChecked():
                    rating = 2
                elif self.rating_3.isChecked():
                    rating = 3
                elif self.rating_4.isChecked():
                    rating = 4
                
                if entry_combo not in self.active_discomforts:
                    # New discomfort - add to tracking
                    self.active_discomforts[entry_combo] = {
                        "rating": rating,
                        "start_time": time_str,
                        "start_date": self.date_edit.date().toString("dd-MM-yyyy")
                    }
                else:
                    # Existing discomfort - update rating and time
                    self.active_discomforts[entry_combo]["rating"] = rating
                    self.active_discomforts[entry_combo]["start_time"] = time_str
                    self.active_discomforts[entry_combo]["start_date"] = self.date_edit.date().toString("dd-MM-yyyy")
                
                self.save_active_discomforts()
                self.update_discomfort_table()
            else:  # finished
                # Remove from active discomforts
                if entry_combo in self.active_discomforts:
                    del self.active_discomforts[entry_combo]
                    self.save_active_discomforts()
                    self.update_discomfort_table()
            
            # Create journal entry
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

        # Insert entry at the correct chronological position
        sorted_text = self.insert_entry_chronologically(current_text, entry)
        self.preview_text.setPlainText(sorted_text)

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
                # Save type stacks after removal
                self.save_type_stacks()
                self.update_options(current_type)
        else:
            # ignore if header somehow selected
            if header_idx is not None and idx == header_idx:
                return
            # remove from base options
            if self._remove_from_list(self.type_options[current_type], text):
                # Save type options after removal
                self.save_type_options()
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
        # Update active discomforts based on edited journal content
        self.update_active_discomforts_from_journal()
    
    def save_notes(self):
        notes_content = self.note_txt.toPlainText().strip()
        changes_content = self.change_txt.toPlainText().strip()
        self.save_journal(notes_content=notes_content, changes_content=changes_content)
        # Update active discomforts based on current journal content
        self.update_active_discomforts_from_journal()

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

    def save_type_options(self):
        """Save type options to a JSON file"""
        if not os.path.exists("options"):
            os.makedirs("options")
        
        filename = os.path.join("options", "type_options.json")
        with open(filename, 'w') as file:
            json.dump(self.type_options, file, indent=2)

    def load_type_options(self):
        """Load type options from a JSON file"""
        filename = os.path.join("options", "type_options.json")
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    saved_options = json.load(file)
                    # Update only the types that exist in saved data
                    for key, value in saved_options.items():
                        if key in self.type_options:
                            self.type_options[key] = value
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # Use default options if file is corrupted or doesn't exist

    def save_type_stacks(self):
        """Save type stacks to a JSON file"""
        if not os.path.exists("options"):
            os.makedirs("options")
        
        filename = os.path.join("options", "type_stacks.json")
        with open(filename, 'w') as file:
            json.dump(self.type_stacks, file, indent=2)

    def load_type_stacks(self):
        """Load type stacks from a JSON file"""
        filename = os.path.join("options", "type_stacks.json")
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    saved_stacks = json.load(file)
                    # Update only the types that exist in saved data
                    for key, value in saved_stacks.items():
                        if key in self.type_stacks:
                            self.type_stacks[key] = value
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # Use default stacks if file is corrupted or doesn't exist

    def setup_discomfort_tracking(self):
        """Setup the discomfort tracking table and controls"""
        self.discomfort_tracking_frame = QFrame()
        discomfort_layout = QVBoxLayout(self.discomfort_tracking_frame)
        
        # Header
        discomfort_header = QHBoxLayout()
        discomfort_label = QLabel("Active Discomforts:")
        discomfort_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        discomfort_header.addWidget(discomfort_label)
        discomfort_header.addStretch()
        
        discomfort_layout.addLayout(discomfort_header)

        # Table for active discomforts
        self.discomfort_table = QTableWidget()
        self.discomfort_table.setColumnCount(3)
        self.discomfort_table.setHorizontalHeaderLabels(["Discomfort", "Rating", "Start Time"])
        self.discomfort_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.discomfort_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.discomfort_table.setMaximumHeight(150)
        discomfort_layout.addWidget(self.discomfort_table)



    def update_discomfort_table(self):
        """Update the discomfort tracking table"""
        self.discomfort_table.setRowCount(0)
        
        for i, (discomfort_name, data) in enumerate(self.active_discomforts.items()):
            self.discomfort_table.insertRow(i)
            
            # Discomfort name
            name_item = QTableWidgetItem(discomfort_name)
            self.discomfort_table.setItem(i, 0, name_item)
            
            # Rating
            rating_item = QTableWidgetItem(f"Rating {data['rating']}")
            self.discomfort_table.setItem(i, 1, rating_item)
            
            # Start time (only time, no date)
            start_time_item = QTableWidgetItem(data['start_time'])
            self.discomfort_table.setItem(i, 2, start_time_item)

    def update_active_discomforts_from_journal(self):
        """Parse the edited journal content and update active discomforts accordingly"""
        journal_content = self.preview_text.toPlainText()
        lines = journal_content.strip().split('\n')
        
        # Clear current active discomforts
        self.active_discomforts.clear()
        
        # Parse each line to find discomfort entries
        for line in lines:
            line = line.strip()
            if not line or line.startswith('Date:'):
                continue
                
            # Look for discomfort patterns: "time started having discomfort rating: X"
            # or "time started having discomfort rating X"
            if 'started having' in line and 'rating' in line:
                # Extract time
                time_match = line.split()[0]  # First word should be time
                
                # Extract discomfort name (between "having" and "rating")
                if 'having' in line and 'rating' in line:
                    having_index = line.find('having')
                    rating_index = line.find('rating')
                    if having_index != -1 and rating_index != -1:
                        discomfort_name = line[having_index + 7:rating_index].strip()
                        
                        # Extract rating
                        rating_part = line[rating_index:].strip()
                        rating = 1  # default
                        if 'rating: 1' in rating_part or 'rating 1' in rating_part:
                            rating = 1
                        elif 'rating: 2' in rating_part or 'rating 2' in rating_part:
                            rating = 2
                        elif 'rating: 3' in rating_part or 'rating 3' in rating_part:
                            rating = 3
                        elif 'rating: 4' in rating_part or 'rating 4' in rating_part:
                            rating = 4
                        
                        # Update active discomforts (this will overwrite previous entries for same discomfort)
                        self.active_discomforts[discomfort_name] = {
                            "rating": rating,
                            "start_time": time_match,
                            "start_date": self.date_edit.date().toString("dd-MM-yyyy")
                        }
        
        # Save and update the table
        self.save_active_discomforts()
        self.update_discomfort_table()
        
        # Sort journal entries chronologically and update the preview
        sorted_journal = self.sort_journal_chronologically(journal_content)
        if sorted_journal != journal_content:
            self.preview_text.setPlainText(sorted_journal)

    def insert_entry_chronologically(self, journal_content, new_entry):
        """Insert a new entry at the correct chronological position in the journal"""
        lines = journal_content.strip().split('\n')
        
        # Extract time from new entry
        new_entry_time = self.extract_time_from_entry(new_entry)
        if not new_entry_time:
            # If no time found, append to end
            return journal_content + new_entry + "\n"
        
        # Find the correct position to insert
        insert_position = len(lines)  # Default to end
        
        for i, line in enumerate(lines):
            if line.startswith('Date:'):
                continue
                
            line_time = self.extract_time_from_entry(line)
            if line_time and line_time > new_entry_time:
                insert_position = i
                break
        
        # Insert the new entry at the correct position
        lines.insert(insert_position, new_entry)
        
        # Reconstruct the journal content
        return '\n'.join(lines) + '\n'

    def extract_time_from_entry(self, entry):
        """Extract time from an entry string (e.g., '11:03am take fish oil' -> '11:03am')"""
        words = entry.strip().split()
        if not words:
            return None
            
        time_str = words[0]
        
        # Check if it's a valid time format (e.g., 11:03am, 2:30pm)
        if ':' in time_str and ('am' in time_str.lower() or 'pm' in time_str.lower()):
            return time_str.lower()
        
        return None

    def sort_journal_chronologically(self, journal_content):
        """Sort all journal entries chronologically"""
        lines = journal_content.strip().split('\n')
        
        # Separate header from entries
        header_lines = []
        entry_lines = []
        
        for line in lines:
            if line.startswith('Date:'):
                header_lines.append(line)
            else:
                entry_lines.append(line)
        
        # Sort entry lines by time
        entry_lines.sort(key=lambda x: self.extract_time_from_entry(x) or '')
        
        # Reconstruct journal with header first, then sorted entries
        sorted_lines = header_lines + entry_lines
        return '\n'.join(sorted_lines) + '\n'

    def save_active_discomforts(self):
        """Save active discomforts to a JSON file"""
        if not os.path.exists("Journal"):
            os.makedirs("Journal")
        
        filename = os.path.join("Journal", "active_discomforts.json")
        with open(filename, 'w') as file:
            json.dump(self.active_discomforts, file, indent=2)

    def load_active_discomforts(self):
        """Load active discomforts from a JSON file"""
        filename = os.path.join("Journal", "active_discomforts.json")
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    self.active_discomforts = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.active_discomforts = {}

    def closeEvent(self, event):
        self.save_journal()
        # Save type options and stacks before closing
        self.save_type_options()
        self.save_type_stacks()
        self.save_active_discomforts() # Save active discomforts on close
        super().closeEvent(event)
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Journal()
    window.show()
    sys.exit(app.exec())
    