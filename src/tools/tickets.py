import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/agent_data.db")

def create_ticket(customer_name: str, customer_email: str, subject: str, body: str) -> Optional[int]:
    """
    Create a new support ticket.
    
    Args:
        customer_name (str): Name of the customer
        customer_email (str): Email address of the customer
        subject (str): Subject/title of the ticket
        body (str): Description of the issue
        
    Returns:
        Optional[int]: Ticket ID if successful, None otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Validate inputs
        if not customer_name or not customer_email or not subject:
            print("Missing required fields for ticket creation")
            return None
            
        c.execute("INSERT INTO tickets(customer_name, customer_email, subject, body) VALUES(?,?,?,?)",
                  (customer_name.strip(), customer_email.strip(), subject.strip(), body.strip()))
        ticket_id = c.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Ticket created successfully with ID: {ticket_id}")
        return ticket_id
        
    except sqlite3.Error as e:
        print(f"Database error in create_ticket: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in create_ticket: {e}")
        return None

def get_ticket_by_id(ticket_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a specific ticket by its ID.
    
    Args:
        ticket_id (int): The ticket ID to retrieve
        
    Returns:
        Optional[Dict[str, Any]]: Ticket data if found, None otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "customer_name": row[1],
                "customer_email": row[2],
                "subject": row[3],
                "body": row[4],
                "status": row[5],
                "created_at": row[6]
            }
        return None
        
    except sqlite3.Error as e:
        print(f"Database error in get_ticket_by_id: {e}")
        return None

def list_open_tickets() -> List[Dict[str, Any]]:
    """
    List all open support tickets.
    
    Returns:
        List[Dict[str, Any]]: List of open tickets
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, customer_name, subject, created_at FROM tickets WHERE status='open' ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        
        return [{"id": row[0], "customer_name": row[1], "subject": row[2], "created_at": row[3]} for row in rows]
        
    except sqlite3.Error as e:
        print(f"Database error in list_open_tickets: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in list_open_tickets: {e}")
        return []

def update_ticket_status(ticket_id: int, new_status: str) -> bool:
    """
    Update the status of a ticket.
    
    Args:
        ticket_id (int): The ticket ID to update
        new_status (str): New status (e.g., 'open', 'closed', 'in_progress')
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
        conn.commit()
        affected_rows = c.rowcount
        conn.close()
        
        return affected_rows > 0
        
    except sqlite3.Error as e:
        print(f"Database error in update_ticket_status: {e}")
        return False
