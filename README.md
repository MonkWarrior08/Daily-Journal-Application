# Daily Journal Application

A simple journal application built with PySide6 that allows you to track daily activities, food intake, supplements, and other events with timestamps.

## Features

- Record different types of entries (supplements, food, activities, etc.)
- Automatic or manual timestamping of entries
- Save entries to text files organized by date
- Preview your journal entries within the application
- Calendar date picker for viewing or creating entries for any date

## Installation

1. Make sure you have Python 3.6+ installed
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

## Example Journal Format

```
Date: 25-05-2023
9:00am woke up
9:30am ate 1 fish
9:35am supplement - b-complex, ashwangandha
11:30am activity - went for a walk
```

## License

This project is open source and available under the MIT License. 