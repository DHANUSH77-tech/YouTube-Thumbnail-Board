from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dhanu@124',
    'database': 'thumbnail'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize the database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create thumbnail table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS thumbnails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                video_id VARCHAR(20) NOT NULL,
                board_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_video_board (video_id, board_name)
            )
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Database initialized successfully")
            
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()

def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.match(regex, url)
    return match.group(1) if match else None

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/boards', methods=['GET'])
def get_boards():
    """Get all boards with their thumbnails"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get all unique board names
        cursor.execute("SELECT DISTINCT board_name FROM thumbnails ORDER BY board_name")
        boards = cursor.fetchall()
        
        result = []
        for board in boards:
            # Get thumbnails for this board
            cursor.execute("SELECT video_id FROM thumbnails WHERE board_name = %s ORDER BY created_at DESC", (board['board_name'],))
            thumbnails = [row['video_id'] for row in cursor.fetchall()]
            
            result.append({
                'name': board['board_name'],
                'thumbnails': thumbnails
            })
        
        return jsonify(result)
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/thumbnails', methods=['POST'])
def add_thumbnail():
    """Add a new thumbnail to a board"""
    data = request.get_json()
    url = data.get('url')
    board_name = data.get('board_name')
    
    if not url or not board_name:
        return jsonify({'error': 'URL and board name are required'}), 400
    
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Insert thumbnail
        insert_query = """
        INSERT INTO thumbnails (video_id, board_name) 
        VALUES (%s, %s) 
        ON DUPLICATE KEY UPDATE created_at = CURRENT_TIMESTAMP
        """
        cursor.execute(insert_query, (video_id, board_name))
        connection.commit()
        
        return jsonify({'success': True, 'video_id': video_id})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/thumbnails/<video_id>', methods=['DELETE'])
def delete_thumbnail(video_id):
    """Delete a thumbnail from a board"""
    data = request.get_json()
    board_name = data.get('board_name')
    
    if not board_name:
        return jsonify({'error': 'Board name is required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Delete thumbnail
        delete_query = "DELETE FROM thumbnails WHERE video_id = %s AND board_name = %s"
        cursor.execute(delete_query, (video_id, board_name))
        connection.commit()
        
        return jsonify({'success': True})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/boards', methods=['POST'])
def create_board():
    """Create a new board"""
    data = request.get_json()
    board_name = data.get('name')
    
    if not board_name:
        return jsonify({'error': 'Board name is required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Insert a dummy thumbnail to create the board (will be deleted immediately)
        insert_query = "INSERT INTO thumbnails (video_id, board_name) VALUES (%s, %s)"
        cursor.execute(insert_query, ('dummy', board_name))
        connection.commit()
        
        # Delete the dummy thumbnail
        delete_query = "DELETE FROM thumbnails WHERE video_id = %s AND board_name = %s"
        cursor.execute(delete_query, ('dummy', board_name))
        connection.commit()
        
        return jsonify({'success': True, 'board_name': board_name})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/boards/<board_name>', methods=['DELETE'])
def delete_board(board_name):
    """Delete a board and all its thumbnails"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Delete all thumbnails in the board
        delete_query = "DELETE FROM thumbnails WHERE board_name = %s"
        cursor.execute(delete_query, (board_name,))
        connection.commit()
        
        return jsonify({'success': True})
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
