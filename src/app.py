import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
import logging
from contextlib import asynccontextmanager

from agent import handle_user_message

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
