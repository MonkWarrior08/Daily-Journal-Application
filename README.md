# Daily Journal Application

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)](https://wiki.qt.io/Qt_for_Python)

A simple, elegant journal application built with PySide6 that allows you to track daily activities, food intake, supplements, and other events with timestamps. Perfect for maintaining health logs, productivity tracking, or personal journaling.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Storage](#data-storage)
- [Example Journal Format](#example-journal-format)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- Record different types of entries (supplements, food, activities, discomforts, medications)
- Time modes: **Automatic** (uses current time) or **Custom** (set your own)
- Food: fish subtype selector (e.g., basal fillet, barramundi) and quantity (1 default or 2)
- Food/Supplement lists are editable: typing a new single item auto-adds it (case-insensitive, trims ends)
- Multi-select for Food/Supplements, with auto-saved combinations as **Saved stacks** (and a Remove button to delete items or stacks)
- Preview and inline editing of the daily journal with Save edit
- Dedicated Notes and Changes sections stored with the day’s journal
- Calendar date picker for viewing/creating entries for any date
- Lightweight, fast, cross-platform (Windows, macOS, Linux)

## Screenshots
<img width="594" height="913" alt="image" src="https://github.com/user-attachments/assets/8dd28b39-21dd-40d5-b05d-f6b7611b7d0a" />


## Requirements

- Python 3.6 or higher
- PySide6 (Qt for Python)
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MonkWarrior08/Daily-Journal-Application.git
   cd Daily-Journal-Application
   ```

2. Install the required module:
   ```bash
   pip install PySide6
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Add entries:
   - Select a date (defaults to today)
   - Choose a time mode:
     - Automatic: current time is used and the time field is disabled
     - Custom: the time field is enabled and initialized to the current time
   - Choose an entry type from the dropdown
   - Food specifics:
     - If you choose fish, select fish type and quantity (1 or 2)
   - Food/Supplement power-user features:
     - Type a new single item to auto-add it to the list (case-insensitive, trims ends)
     - Use select(multi) to pick several items. The combination is saved under a non-selectable “Saved stacks” header in the dropdown
     - Use Remove to delete either a single item or a saved stack (case-insensitive match)
   - Click Add Entry

3. Edit and save:
   - Modify the journal text in the left preview and click Save edit
   - Add Notes and Changes in their respective editors and click their Save buttons (also saved on app close)

4. To view another date:
   - Select the date from the calendar. The journal, Notes, and Changes will load if present

## Data Storage

All journal entries are stored as plain text files in the `Journal` directory. Each day's entries are stored in a separate file named:

```
Journal/<dd-MM-yyyy>.txt
```

## Example Journal Format

```
Date: 25-05-2023
9:00am woke up
9:30am ate fish(basal fillet)
9:35am took vit c, L-theanine
10:00am ate 2 fish(barramundi)
2:15pm took medication - Dexamphetamine (5mg)

Notes: felt energetic in the morning

Changes: increased L-theanine to 200mg
```

## Customization

You can customize the application by:

- Adding new entry types in code
- Changing the default time format
- Modifying the journal file naming convention
- Adjusting the UI theme

*More details about customization options will be added soon.*

## Troubleshooting

### Common Issues

- **Application won't start**: Ensure all dependencies are installed correctly
- **Entries not saving**: Check write permissions in the journals directory
- **UI elements not displaying correctly**: Update PySide6 to the latest version

If you encounter any other issues, please [open an issue](https://github.com/yourusername/daily-journal-app/issues) with details of the problem.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE). 
