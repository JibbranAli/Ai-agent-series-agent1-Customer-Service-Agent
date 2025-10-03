import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
import logging
import os
from contextlib import asynccontextmanager

from agent import handle_user_message
from tools.tickets import create_ticket, update_ticket_status
from tools.kb import add_kb_entry

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources."""
    # Startup: initialize database
    try:
        from db.init_db import init_db
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown: cleanup if needed
    logger.info("Shutting down Customer Service Agent")

app = FastAPI(
    title="Customer Service Agent API",
    description="AI-powered customer service agent with intelligent responses",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for dashboard
try:
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.exists(frontend_path):
        app.mount("/static", StaticFiles(directory=frontend_path), name="static")
        app.mount("/dashboard.js", StaticFiles(directory=frontend_path), name="dashboard.js")
    else:
        logger.warning("Frontend directory not found. Dashboard will not be available.")
except Exception as e:
    logger.error(f"Failed to mount static files: {e}")

# Serve dashboard.js directly
@app.get("/dashboard.js")
async def dashboard_js():
    """Serve the dashboard JavaScript file."""
    try:
        js_path = os.path.join(os.path.dirname(__file__), "frontend", "dashboard.js")
        if os.path.exists(js_path):
            return FileResponse(js_path, media_type="text/javascript")
        else:
            raise HTTPException(status_code=404, detail="Dashboard JavaScript not found")
    except Exception as e:
        logger.error(f"Failed to serve dashboard.js: {e}")
        raise HTTPException(status_code=500, detail="Dashboard JavaScript unavailable")

class MessageIn(BaseModel):
    """Input model for customer messages."""
    customer_name: Optional[str] = Field(None, max_length=100, description="Customer's name")
    customer_email: Optional[EmailStr] = Field(None, description="Customer's email address")
    text: str = Field(..., min_length=1, max_length=2000, description="Customer message")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation continuity")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Message text cannot be empty')
        return v.strip()
    
    @field_validator('customer_name')
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 1:
                raise ValueError('Customer name cannot be empty if provided')
        return v

class MessageOut(BaseModel):
    """Output model for agent responses."""
    reply: str = Field(..., description="Agent's response to the customer")
    trace: List[Dict[str, Any]] = Field(..., description="Execution trace of the agent's actions")
    session_id: Optional[str] = Field(None, description="Session identifier")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score for the response")

class HealthCheck(BaseModel):
    """Health check response model."""
    status: str = "healthy"
    message: str = "Customer Service Agent is running"

@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with health check."""
    return HealthCheck()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard interface."""
    try:
        frontend_index = os.path.join(os.path.dirname(__file__), "frontend", "index.html")
        if os.path.exists(frontend_index):
            return FileResponse(frontend_index)
        else:
            return HTMLResponse("""
                <html>
                    <head><title>Dashboard Not Available</title></head>
                    <body>
                        <h1>Dashboard Not Available</h1>
                        <p>The dashboard interface is not installed. Please ensure frontend files are in place.</p>
                        <p><a href="/docs">Visit API Documentation</a></p>
                    </body>
                </html>
            """)
    except Exception as e:
        logger.error(f"Failed to serve dashboard: {e}")
        raise HTTPException(status_code=500, detail="Dashboard unavailable")

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if we can connect to the database
        from tools.kb import search_kb
        search_kb("test", top_k=1)
        
        return HealthCheck(
            status="healthy",
            message="All systems operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )

@app.post("/message", response_model=MessageOut)
async def message_endpoint(msg: MessageIn):
    """
    Process customer messages and return AI-generated responses.
    
    This endpoint accepts customer inquiries and uses the AI agent to:
    1. Search the knowledge base for relevant information
    2. Create support tickets when needed
    3. Generate intelligent, helpful responses
    """
    try:
        logger.info(f"Processing message from {msg.customer_name or 'anonymous'}")
        
        # Prepare metadata
        metadata = {
            "customer_name": msg.customer_name,
            "customer_email": str(msg.customer_email) if msg.customer_email else None,
            "session_id": msg.session_id,
            "timestamp": str(uvicorn.logging.datetime.now())
        }
        
        # Process the message
        response = handle_user_message(msg.text, metadata)
        
        return MessageOut(
            reply=response["final_text"],
            trace=response["trace"],
            session_id=msg.session_id
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )

@app.get("/kb/search")
async def search_knowledge_base(q: str = "", top_k: int = 5):
    """Search the knowledge base directly."""
    try:
        from tools.kb import search_kb
        results = search_kb(q, top_k=min(top_k, 20))  # Cap at 20 for performance
        return {"query": q, "results": results}
    except Exception as e:
        logger.error(f"KB search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tickets")
async def list_tickets():
    """List open support tickets."""
    try:
        from tools.tickets import list_open_tickets
        tickets = list_open_tickets()
        return {"tickets": tickets}
    except Exception as e:
        logger.error(f"Ticket listing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tickets")
async def create_ticket_endpoint(ticket: dict):
    """Create a new support ticket."""
    try:
        ticket_id = create_ticket(
            customer_name=ticket.get("customer_name", "Unknown"),
            customer_email=ticket.get("customer_email", ""),
            subject=ticket.get("subject", "No Subject"),
            body=ticket.get("body", "")
        )
        if ticket_id:
            return {"ticket_id": ticket_id, "status": "created"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create ticket")
    except Exception as e:
        logger.error(f"Ticket creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, update_data: dict):
    """Update ticket status."""
    try:
        new_status = update_data.get("status")
        if new_status:
            success = update_ticket_status(ticket_id, new_status)
            if success:
                return {"ticket_id": ticket_id, "status": new_status, "updated": True}
            else:
                raise HTTPException(status_code=404, detail="Ticket not found")
        else:
            raise HTTPException(status_code=400, detail="Status is required")
    except Exception as e:
        logger.error(f"Ticket update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/kb")
async def add_knowledge_base_entry(entry: dict):
    """Add a new knowledge base entry."""
    try:
        success = add_kb_entry(
            title=entry.get("title", ""),
            content=entry.get("content", ""),
            category=entry.get("category", "General"),
            tags=entry.get("tags", "")
        )
        if success:
            return {"status": "added", "title": entry.get("title")}
        else:
            raise HTTPException(status_code=400, detail="Failed to add KB entry")
    except Exception as e:
        logger.error(f"KB entry addition error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.environ.get("AGENT_HOST", "0.0.0.0")
    port = int(os.environ.get("AGENT_PORT", 8000))
    
    logger.info(f"Starting Customer Service Agent on {host}:{port}")
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=bool(os.environ.get("DEBUG", False)),
        log_level="info"
    )
