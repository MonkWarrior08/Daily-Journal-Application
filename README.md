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

- Record different types of entries (supplements, food, activities, etc.)
- Automatic or manual timestamping of entries
- Save entries to text files organized by date
- Preview your journal entries within the application
- Calendar date picker for viewing or creating entries for any date
- Simple and intuitive user interface
- Lightweight and fast performance
- Cross-platform compatibility (Windows, macOS, Linux)
- Dark and light theme support

## Screenshots

*[Screenshots to be added]*

## Requirements

- Python 3.6 or higher
- PySide6 (Qt for Python)
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/daily-journal-app.git
   cd daily-journal-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Add entries using the interface:
   - Select a date (defaults to today)
   - Set the time (or use the "Use Current Time" button)
   - Choose an entry type from the dropdown
   - Enter the details in the entry field
   - Click "Add Entry"

3. The entries will automatically be saved to text files in the `journals` folder with filenames like `journal_dd-MM-yyyy.txt`

4. To view entries for a specific date:
   - Select the date from the calendar
   - The entries will be displayed in the preview panel

## Data Storage

All journal entries are stored as plain text files in the `journals` directory, making them easy to backup, read, or process with other tools. Each day's entries are stored in a separate file with the naming convention:

```
journal_dd-MM-yyyy.txt
```

## Example Journal Format

```
Date: 25-05-2023
9:00am woke up
9:30am ate 1 fish
9:35am supplement - b-complex, ashwangandha
11:30am activity - went for a walk
```

## Customization

You can customize the application by:

- Adding new entry types in the settings
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