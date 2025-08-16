from PySide6.QtWidgets import (QVBoxLayout, QListWidget, QAbstractItemView, QDialog, 
                               QDialogButtonBox, QHBoxLayout, QLabel, QSpinBox, QWidget)
from PySide6.QtCore import Qt

class MultiDialogue(QDialog):
    def __init__(self, parent=None, options=None, title="Select"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 400)
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

    def get_items_with_counts(self):
        """Returns a list of tuples: (item_text, count)"""
        selected_items = []
        for item in self.list_widget.selectedItems():
            selected_items.append((item.text(), 1))  # Default count is 1
        return selected_items


class MultiDialogueWithCounts(QDialog):
    def __init__(self, parent=None, options=None, title="Select"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 500)
        layout = QVBoxLayout()

        # Instructions label
        instructions = QLabel("Select items and specify quantities (1 = no count shown)")
        layout.addWidget(instructions)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

        if options:
            self.list_widget.addItems(options)

        layout.addWidget(self.list_widget)

        # Count input section
        self.count_widget = QWidget()
        self.count_layout = QVBoxLayout(self.count_widget)
        self.count_layout.addWidget(QLabel("Selected items with quantities:"))
        layout.addWidget(self.count_widget)

        # ok and cancel button
        dialogue_butn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialogue_butn.accepted.connect(self.accept)
        dialogue_butn.rejected.connect(self.reject)
        layout.addWidget(dialogue_butn)

        self.setLayout(layout)
        
        # Store count inputs
        self.count_inputs = {}
        
        # Initialize count section
        self.on_selection_changed()

    def on_selection_changed(self):
        """Update the count input section when selection changes"""
        # Remove the old count widget entirely
        if hasattr(self, 'count_widget') and self.count_widget:
            self.count_widget.setParent(None)
        
        # Create a new count widget
        self.count_widget = QWidget()
        self.count_layout = QVBoxLayout(self.count_widget)
        self.count_layout.addWidget(QLabel("Selected items with quantities:"))
        
        # Insert the new count widget back into the main layout
        # Find the position before the button box
        main_layout = self.layout()
        main_layout.insertWidget(main_layout.count() - 1, self.count_widget)
        
        # Store count inputs
        self.count_inputs = {}
        
        # Add count inputs for selected items
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            item_text = item.text()
            
            # Create horizontal layout for item and count
            item_layout = QHBoxLayout()
            
            # Item label
            item_label = QLabel(item_text)
            item_label.setMinimumWidth(150)
            item_layout.addWidget(item_label)
            
            # Count label
            count_label = QLabel("Count:")
            item_layout.addWidget(count_label)
            
            # Count spinbox
            count_spinbox = QSpinBox()
            count_spinbox.setMinimum(1)
            count_spinbox.setMaximum(99)
            count_spinbox.setValue(1)
            count_spinbox.setMaximumWidth(60)
            item_layout.addWidget(count_spinbox)
            
            # Add stretch to push everything to the left
            item_layout.addStretch()
            
            # Add to main count layout
            self.count_layout.addLayout(item_layout)
            
            # Store reference to spinbox
            self.count_inputs[item_text] = count_spinbox

    def get_items_with_counts(self):
        """Returns a list of tuples: (item_text, count)"""
        selected_items = []
        for item in self.list_widget.selectedItems():
            item_text = item.text()
            count = self.count_inputs.get(item_text, 1)
            if hasattr(count, 'value'):
                count = count.value()
            selected_items.append((item_text, count))
        return selected_items

    def get_items(self):
        """Backward compatibility - returns items without counts"""
        return [item.text() for item in self.list_widget.selectedItems()]
