import sqlite3
import sqlite3 as sqlite
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/agent_data.db")

def search_kb(query: str, top_k: int = 5) -> List[Dict[str, str]]:
    """
    Search the knowledge base using Full Text Search (FTS5).
    
    Args:
        query (str): The search query
        top_k (int): Maximum number of results to return
        
    Returns:
        List[Dict[str, str]]: List of dictionary objects with 'title' and 'content' keys
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if advanced schema exists (with category column)
        c.execute("PRAGMA table_info(kb)")
        columns = [col[1] for col in c.fetchall()]
        
        if 'category' in columns:
            # New schema with category support
            c.execute("SELECT title, content FROM kb WHERE kb MATCH ? ORDER BY rank LIMIT ?", (query, top_k))
        else:
            # Old schema - just title and content
            c.execute("SELECT title, content FROM kb WHERE kb MATCH ? LIMIT ?", (query, top_k))
            
        rows = c.fetchall()
        conn.close()
        
        return [{"title": row[0], "content": row[1]} for row in rows]
        
    except sqlite3.Error as e:
        print(f"Database error in search_kb: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in search_kb: {e}")
        return []

def add_kb_entry(title: str, content: str) -> bool:
    """
    Add a new entry to the knowledge base.
    
    Args:
        title (str): The title/topic of the KB entry
        content (str): The content/answer for the entry
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO kb(title, content) VALUES(?, ?)", (title, content))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error in add_kb_entry: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in add_kb_entry: {e}")
        return False

def get_all_kb_entries() -> List[Dict[str, str]]:
    """
    Retrieve all knowledge base entries.
    
    Returns:
        List[Dict[str, str]]: List of all KB entries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT title, content FROM kb")
        rows = c.fetchall()
        conn.close()
        
        return [{"title": row[0], "content": row[1]} for row in rows]
    except sqlite3.Error as e:
        print(f"Database error in get_all_kb_entries: {e}")
        return []
