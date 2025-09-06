from PySide6.QtWidgets import (QVBoxLayout, QListWidget, QAbstractItemView, QDialog, 
                               QDialogButtonBox, QHBoxLayout, QLabel, QSpinBox, QWidget)
from PySide6.QtCore import Qt, QTimer

class MultiDialogue(QDialog):
    def __init__(self, parent=None, options=None, title="Select"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(400, 400)
        self.setMinimumSize(400, 400)  # Prevent shrinking
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        
        # Add selection delay to prevent accidental multiple selections
        self.selection_timer = QTimer()
        self.selection_timer.setSingleShot(True)
        self.selection_timer.setInterval(100)  # 100ms delay
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed_delayed)

        if options:
            self.list_widget.addItems(options)

        layout.addWidget(self.list_widget)

        # ok and cancel button
        dialogue_butn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialogue_butn.accepted.connect(self.accept)
        dialogue_butn.rejected.connect(self.reject)
        layout.addWidget(dialogue_butn)

        self.setLayout(layout)
        
        # Store current selection to prevent rapid changes
        self.current_selection = set()

    def on_selection_changed_delayed(self):
        """Delayed selection change handler to prevent rapid multiple selections"""
        self.selection_timer.start()

    def get_items(self):
        # Get current selection and update stored selection
        selected_items = [item.text() for item in self.list_widget.selectedItems()]
        self.current_selection = set(selected_items)
        return selected_items

    def get_items_with_counts(self):
        """Returns a list of tuples: (item_text, count)"""
        selected_items = []
        for item in self.list_widget.selectedItems():
            selected_items.append((item.text(), 1))  # Default count is 1
        self.current_selection = set([item[0] for item in selected_items])
        return selected_items


class MultiDialogueWithCounts(QDialog):
    def __init__(self, parent=None, options=None, title="Select"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 500)
        self.setMinimumSize(500, 500)  # Prevent shrinking
        self.setMaximumHeight(700)  # Prevent excessive height growth
        layout = QVBoxLayout()

        # Instructions label
        instructions = QLabel("Select items and specify quantities (1 = no count shown)")
        layout.addWidget(instructions)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        
        # Add selection delay to prevent accidental multiple selections
        self.selection_timer = QTimer()
        self.selection_timer.setSingleShot(True)
        self.selection_timer.setInterval(150)  # 150ms delay for counts dialog
        self.selection_timer.timeout.connect(self.on_selection_changed)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed_delayed)

        if options:
            self.list_widget.addItems(options)

        layout.addWidget(self.list_widget)

        # Count input section - create once and reuse
        self.count_widget = QWidget()
        self.count_layout = QVBoxLayout(self.count_widget)
        self.count_layout.addWidget(QLabel("Selected items with quantities:"))
        
        # Add scroll area for count inputs to prevent excessive height
        from PySide6.QtWidgets import QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.count_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(200)  # Limit height of count section
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        layout.addWidget(self.scroll_area)

        # ok and cancel button
        dialogue_butn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialogue_butn.accepted.connect(self.accept)
        dialogue_butn.rejected.connect(self.reject)
        layout.addWidget(dialogue_butn)

        self.setLayout(layout)
        
        # Store count inputs
        self.count_inputs = {}
        
        # Store current selection to prevent rapid changes
        self.current_selection = set()
        
        # Initialize count section
        self.on_selection_changed()

    def on_selection_changed_delayed(self):
        """Delayed selection change handler to prevent rapid multiple selections"""
        self.selection_timer.start()

    def on_selection_changed(self):
        """Update the count input section when selection changes"""
        # Get current selection
        selected_items = self.list_widget.selectedItems()
        selected_texts = [item.text() for item in selected_items]
        
        # Only update if selection actually changed significantly
        if set(selected_texts) == self.current_selection:
            return
            
        self.current_selection = set(selected_texts)
        
        # Clear existing count inputs
        for i in reversed(range(self.count_layout.count())):
            child = self.count_layout.itemAt(i)
            if child.widget():
                child.widget().setParent(None)
            elif child.layout():
                # Clear layout items
                for j in reversed(range(child.layout().count())):
                    layout_child = child.layout().itemAt(j)
                    if layout_child.widget():
                        layout_child.widget().setParent(None)
        
        # Store count inputs
        self.count_inputs = {}
        
        # Add count inputs for selected items
        for item in selected_items:
            item_text = item.text()
            
            # Create horizontal layout for item and count
            item_layout = QHBoxLayout()
            
            # Item label
            item_label = QLabel(item_text)
            item_label.setMinimumWidth(150)
            item_label.setMaximumWidth(200)  # Prevent excessive width
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
        
        # Force layout update and maintain dialog size
        self.count_widget.updateGeometry()
        self.scroll_area.updateGeometry()
        self.adjustSize()
        
        # Ensure dialog doesn't shrink below minimum
        if self.height() < 500:
            self.resize(self.width(), 500)

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
