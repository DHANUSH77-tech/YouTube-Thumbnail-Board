# YouTube Thumbnail Board

A Flask-based web application for organizing and managing YouTube video thumbnails in customizable boards.

## Features

- Create multiple boards to organize thumbnails
- Add YouTube video thumbnails by pasting URLs
- Download thumbnails directly from the app
- Delete thumbnails and boards
- Modern, responsive UI with dark theme
- MySQL database backend for persistent storage

## Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package installer)

## Setup Instructions

### 1. Database Setup

1. Install MySQL Server if not already installed
2. Create a new database named `thumbnail`:
   ```sql
   CREATE DATABASE thumbnail;
   ```
3. The application will automatically create the required table on first run

### 2. Application Setup

1. Clone or download this project
2. Navigate to the project directory
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Configuration

The application is configured to connect to MySQL with these default settings:
- Host: localhost
- User: root
- Password: Dhanu@124
- Database: thumbnail

If you need to change these settings, edit the `DB_CONFIG` in `app.py`.

### 4. Run the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. **Create a Board**: Click "Add New Board" in the sidebar and enter a name
2. **Add Thumbnails**: Paste a YouTube URL in the input field and click "Add to Board"
3. **Download Thumbnails**: Hover over a thumbnail and click "Download"
4. **Delete Thumbnails**: Hover over a thumbnail and click "Delete"
5. **Delete Boards**: Hover over a board name in the sidebar and click the delete button

## API Endpoints

- `GET /api/boards` - Get all boards with their thumbnails
- `POST /api/boards` - Create a new board
- `DELETE /api/boards/<board_name>` - Delete a board
- `POST /api/thumbnails` - Add a thumbnail to a board
- `DELETE /api/thumbnails/<video_id>` - Delete a thumbnail from a board

## File Structure

```
Thumbnail/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/
    └── index.html     # Main HTML template
```

## Troubleshooting

- **Database Connection Error**: Make sure MySQL is running and the credentials are correct
- **Port Already in Use**: Change the port in `app.py` or stop other services using port 5000
- **Module Not Found**: Run `pip install -r requirements.txt` to install dependencies
