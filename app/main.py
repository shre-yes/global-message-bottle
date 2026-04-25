from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import logging

# Configure logging to monitor behavior
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Global Message In A Bottle", version="1.0.0")

# Setup CORS to allow backend to accept requests from our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local phase; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "messages.db"

# Data models for request and response validation
class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    content: str
    timestamp: str

def init_db():
    """Initialize the SQLite database and create the messages table."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Run DB initialization at startup
init_db()

@app.get("/messages", response_model=list[MessageResponse])
def get_messages():
    """Fetch all messages from the database, ordered by latest first."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, content, timestamp FROM messages ORDER BY id DESC")
            rows = cursor.fetchall()
            
            # Map SQLite rows into dictionaries
            return [{"id": row["id"], "content": row["content"], "timestamp": row["timestamp"]} for row in rows]
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/messages", response_model=MessageResponse)
def create_message(message: MessageCreate):
    """Save a new anonymous message to the database."""
    content = message.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Message content cannot be empty")
        
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (content) VALUES (?)",
                (content,)
            )
            conn.commit()
            
            msg_id = cursor.lastrowid
            # Retrieve the full inserted row (including generated timestamp)
            cursor.execute("SELECT id, content, timestamp FROM messages WHERE id = ?", (msg_id,))
            row = dict(cursor.fetchone())
            
            logger.info(f"New message created with ID: {msg_id}")
            return row
            
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
