# Daily Journal Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://wiki.qt.io/Qt_for_Python)

A comprehensive, elegant journal application built with PySide6 that allows you to track daily activities, food intake, supplements, discomforts, and other events with intelligent timestamp management and automatic organization. Perfect for maintaining health logs, productivity tracking, or personal journaling.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Storage](#data-storage)
- [Example Journal Format](#example-journal-format)
- [File Structure](#file-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Development Notes](#development-notes)
- [License](#license)

## Features

### Core Functionality
- **Multiple Entry Types**: Daily, Food, Drink, Activity, Supplement, Discomfort, Medication
- **Smart Time Management**: 
  - **Automatic mode**: Uses current time with disabled time field
  - **Custom mode**: Set your own time with enabled time picker
- **Date Navigation**: Calendar popup for easy date selection and journal browsing

### Food & Supplement Management
- **Fish Subtype Selection**: Choose between basal fillet, barramundi with quantity options (1 or 2)
- **Dynamic Lists**: Auto-add new single items to Food/Supplement lists (case-insensitive, trimmed)
- **Multi-Select System**: 
  - Select multiple items at once
  - **Saved Stacks**: Automatically saves combinations for future use
  - **Remove Functionality**: Delete individual items or entire saved stacks
  - **Quantity Support**: Specify quantities for supplements (e.g., "2 vit c")

### Advanced Discomfort Tracking
- **Active Discomfort Monitoring**: Real-time tracking of ongoing discomforts with ratings
- **Rating System**: 1-4 scale for discomfort severity
- **Automatic Updates**: Rating and time updates when adding new entries
- **Always Visible**: Discomfort tracking table shows current active issues
- **Smart Parsing**: Automatically detects and tracks discomfort entries from journal

### Intelligent Journal Management
- **Chronological Auto-Sorting**: Entries automatically arranged by time
- **Smart Entry Insertion**: New entries placed at correct chronological position
- **Real-time Preview**: Live editing with automatic saving
- **Notes & Changes Sections**: Dedicated areas for daily notes and change tracking
- **Persistent Storage**: All data automatically saved and restored between sessions

### Enhanced Multi-Select Experience
- **Stable Dialog Sizing**: Consistent window dimensions, no more shrinking
- **Selection Protection**: Prevents accidental multiple selections
- **Scrollable Content**: Handles any number of items without size issues
- **Improved Performance**: Optimized layout management and widget handling

### Data Persistence & Organization
- **Automatic Backup**: Type options, saved stacks, and active discomforts persist between sessions
- **Human-Readable Format**: All data stored in JSON and text formats for easy backup/editing
- **Smart File Management**: Organized storage structure with automatic directory creation

## Screenshots

<img width="594" height="913" alt="image" src="https://github.com/user-attachments/assets/8dd28b39-21dd-40d5-b05d-f6b7611b7d0a" />

## Requirements

- Python 3.6 or higher
- PySide6 (Qt for Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/journ.git
   cd journ
   ```

2. Install the required module:
   ```bash
   pip install PySide6
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Basic Entry Creation
1. **Select Date**: Choose from calendar (defaults to today)
2. **Set Time Mode**:
   - **Automatic**: Current time used, field disabled
   - **Custom**: Enable time picker, initialized to current time
3. **Choose Entry Type**: Select from dropdown menu
4. **Configure Specifics**:
   - **Food**: Select fish type and quantity if choosing fish
   - **Discomfort**: Set rating (1-4) and start/end status
   - **Activity**: Choose start or end status
5. **Add Entry**: Click "Add Entry" button

### Advanced Features

#### Discomfort Tracking
- **Start Tracking**: Select "Discomfort" type, choose item, set rating, select "Start"
- **Update Rating**: Add new "Start" entry with different rating to update active discomfort
- **End Tracking**: Select "End" status to remove from active tracking
- **Monitor Active Issues**: View all current discomforts with ratings and start times

#### Multi-Select Operations
- **Select Multiple Items**: Use "select(multi)" button for Food/Supplements
- **Quantity Specification**: Set quantities for supplements (1 = no count shown)
- **Save Combinations**: Multi-selections automatically saved as reusable stacks
- **Manage Stacks**: Remove individual items or entire saved combinations

#### Journal Editing
- **Inline Editing**: Modify journal text directly in preview area
- **Automatic Sorting**: Entries automatically arranged chronologically
- **Save Changes**: Click "Save edit" to persist modifications
- **Notes & Changes**: Add daily notes and track changes in dedicated sections

### Power User Features
- **Auto-Add Items**: Type new single items to automatically add to Food/Supplement lists
- **Smart Time Insertion**: Custom time entries automatically placed in chronological order
- **Persistent Options**: All customizations automatically saved between sessions
- **Bulk Operations**: Multi-select and manage multiple items efficiently

## Data Storage

### Journal Files
Daily entries stored as plain text files:
```
Journal/<dd-MM-yyyy>.txt
```

### Configuration Files
Automatically managed in `options/` directory:
- `type_options.json`: Custom Food, Supplement, and other type lists
- `type_stacks.json`: Saved multi-select combinations
- `active_discomforts.json`: Current active discomfort tracking data

### Data Structure
- **Human-readable formats** for easy backup and editing
- **Automatic directory creation** when needed
- **JSON persistence** for complex data structures
- **Text-based journals** for maximum compatibility

## Example Journal Format

```
Date: 25-05-2023
9:00am woke up
9:30am started having fatigue rating: 2
9:35am ate fish(basal fillet)
9:40am took vit c, L-theanine
10:00am ate 2 fish(barramundi)
10:15am started having anxiety rating: 3
2:15pm took medication - Dexamphetamine (5mg)
3:00pm finished having anxiety rating: 3

Notes: felt energetic in the morning, anxiety improved after medication

Changes: increased L-theanine to 200mg
```

## File Structure

```
journ/
├── main.py                    # Main application with all features
├── multi.py                   # Enhanced multi-select dialogs
├── Journal/                   # Daily journal files
│   ├── <dd-MM-yyyy>.txt      # Daily entries
│   └── active_discomforts.json # Active discomfort tracking
├── options/                   # Persistent configuration
│   ├── type_options.json     # Custom type lists
│   └── type_stacks.json      # Saved multi-select stacks
└── README.md                  # This documentation
```

## Customization

### Adding New Features
- **New Entry Types**: Add to `type_options` dictionary in `main.py`
- **Fish Varieties**: Modify `fish_type` combo box options
- **Discomfort Types**: Extend discomfort options list
- **Activity Categories**: Add new activity types

### UI Customization
- **Time Format**: Modify time display format
- **Date Format**: Change journal file naming convention
- **Theme**: Adjust UI appearance and styling
- **Layout**: Modify widget arrangements and sizes

### Data Customization
- **Default Values**: Set initial ratings, quantities, and selections
- **Validation Rules**: Add custom input validation
- **Auto-completion**: Enhance suggestion systems
- **Export Formats**: Add data export capabilities

## Troubleshooting

### Common Issues

- **Application won't start**: Ensure PySide6 is installed correctly
- **Entries not saving**: Check write permissions in Journal directory
- **UI elements not displaying**: Update PySide6 to latest version
- **Type options not persisting**: Verify options directory permissions
- **Multi-select issues**: Check for corrupted saved stacks files
- **Discomfort tracking problems**: Verify active_discomforts.json integrity

### Performance Issues
- **Slow startup**: Check for large journal files or corrupted data
- **UI lag**: Reduce number of saved stacks or type options
- **Memory usage**: Monitor journal file sizes and clean up old entries

### Data Recovery
- **Backup files**: All data stored in human-readable formats
- **JSON validation**: Check for syntax errors in configuration files
- **Manual restoration**: Edit files directly if automatic recovery fails

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style and patterns
- Add comprehensive error handling
- Include user feedback mechanisms
- Test with various data scenarios
- Update documentation for new features

## Development Notes

### Recent Enhancements
- **Discomfort Tracking System**: Real-time monitoring with rating updates
- **Chronological Sorting**: Automatic entry organization by time
- **Enhanced Multi-Select**: Improved dialog stability and performance
- **Smart Time Management**: Intelligent entry insertion and sorting
- **Persistent State**: All user customizations automatically preserved

### Technical Features
- **Automatic data persistence** for all user customizations
- **Intelligent layout management** preventing UI corruption
- **Efficient data structures** for fast performance
- **Robust error handling** for data integrity
- **Cross-platform compatibility** (Windows, macOS, Linux)

### Architecture
- **Modular design** with separate multi-select components
- **Event-driven updates** for real-time synchronization
- **JSON-based configuration** for easy maintenance
- **Text-based storage** for maximum compatibility
- **Qt-based UI** for professional appearance

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Note**: This application is designed for personal use and health tracking. Always consult healthcare professionals for medical advice and treatment decisions. 
