# Customer Service AI Agent

A sophisticated AI-powered customer service agent that provides automated, intelligent responses to customer inquiries using Google's Gemini AI model. The agent can search knowledge bases, create support tickets, and engage in natural language conversations with customers.

## Features

- **AI-Powered Responses**: Uses Google Gemini 2.0 Flash model for intelligent conversation
- **Knowledge Base Search**: Full-text search across comprehensive FAQ and support documentation
- **Support Ticket Management**: Automatic ticket creation for complex inquiries
- **HTTP API Integration**: RESTful API for easy integration with web applications
- **Database Management**: SQLite database with FTS5 full-text search capabilities
- **Real-time Processing**: Fast response times with proper error handling
- **Session Management**: Support for conversation continuity across sessions

## Quick Start

### 🚀 One-Click Setup (Recommended)

The fastest way to get started:

```bash
# Automatic setup and start
python quickstart.py
```

This script will:
- ✅ Check Python compatibility
- ✅ Install all dependencies
- ✅ Set up environment variables
- ✅ Initialize the database
- ✅ Start the agent server

### 🛠️ Manual Setup (Advanced Users)

#### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

#### Step-by-Step Installation

1. **Get your Google Gemini API key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an API key

2. **Set up the environment**
   ```bash
   # Automated setup
   python setup.py
   
   # OR manual setup:
   pip install -r requirements.txt
   cp env_template.txt .env
   # Edit .env with your API key
   python src/db/init_db.py
   ```

3. **Start the agent**
   ```bash
   # Easy start with management script
   python run_agent.py start
   
   # Or direct start
   python src/app.py
   ```

### 🎯 Available Scripts

#### Setup Scripts
- `python setup.py` - Complete automated setup
- `python quickstart.py` - One-click setup and start

#### Management Scripts  
- `python run_agent.py start` - Start the agent server
- `python run_agent.py status` - Check system status
- `python run_agent.py test` - Run quick tests

#### Testing Scripts
- `python test_agent.py` - Basic functionality tests
- `python test_comprehensive.py` - Full test suite with performance tests

#### Platform-Specific Starters
- **Windows**: Double-click `start_agent.bat` or run `start_agent.bat`
- **Unix/Linux/Mac**: Run `./start_agent.sh`

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### POST /message
Send a customer message and receive an AI-powered response.

```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "text": "I need help with my order",
  "session_id": "session_123"
}
```

Response:
```json
{
  "reply": "Hello John! I'd be happy to help you with your order...",
  "trace": [
    {
      "action": "search_kb",
      "reason": "Looking for order-related information",
      "args": {"query": "order status help", "top_k": 5},
      "result": [...]
    }
  ],
  "session_id": "session_123"
}
```

#### GET /health
Check the health status of the service.

#### GET /kb/search
Directly search the knowledge base.

#### GET /tickets
List open support tickets.

## Configuration

The agent can be configured through environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: Model to use (default: gemini-2.0-flash-exp)
- `AGENT_HOST`: Server host (default: 0.0.0.0)
- `AGENT_PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (true/false)

## Knowledge Base

The agent comes with a comprehensive knowledge base covering:

- Return policies and refunds
- Shipping information and tracking
- Payment methods and processing
- Product warranties and support
- Account management features
- Technical support procedures
- Store locations and hours
- Bulk orders and pricing
- International shipping
- Live chat availability
- Price matching policies
- Gift cards and promotions

You can add more entries by directly inserting into the database or using the admin tools.

## Architecture

The agent follows a modular architecture:

```
src/
├── app.py              # FastAPI application
├── agent.py            # Core AI agent logic
├── db/
│   ├── init_db.py     # Database initialization
│   └── agent_data.db  # SQLite database
└── tools/
    ├── kb.py          # Knowledge base operations
    ├── tickets.py     # Ticket management
    └── http_tool.py   # HTTP requests
```

### Agent Flow

1. **Message Received**: Customer message comes through API
2. **Planning**: AI analyzes the message and creates an execution plan
3. **Tool Execution**: Relevant tools are called (KB search, ticket creation, etc.)
4. **Response Generation**: AI synthesizes the final response
5. **Trace Logging**: Full execution trace is logged for debugging

## Customization

### Adding New Tools

To add new capabilities to the agent:

1. Create a new function in the appropriate tool module
2. Add the tool to the `TOOLS` dictionary in `agent.py`
3. Add the execution logic in the `execute_plan` function

### Expanding Knowledge Base

Add more entries to the knowledge base:

```python
from tools.kb import add_kb_entry

add_kb_entry(
    title="Custom Policy",
    content="Details about your custom policy...",
    category="Policies",
    tags="custom-policy specific-terms"
)
```

### Custom Responses

Modify the prompt templates in `agent.py` to customize the agent's personality and response style.

## Testing

### Manual Testing

Use curl to test the API:

```bash
curl -X POST "http://localhost:8000/message" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test Customer",
    "customer_email": "test@example.com",
    "text": "What is your return policy?",
    "session_id": "test_session"
  }'
```

### Example Interactions

**Customer**: "I want to return something I bought last week"
**Agent**: "I'd be happy to help you with your return! Our return policy allows you to return items within 30 days of purchase..."

**Customer**: "I haven't received my order yet"
**Agent**: "[Creates a support ticket] "I've created a support ticket (#12345) for your order inquiry. Our shipping team will investigate..."

## Testing

### 🧪 Quick Tests

```bash
# Basic functionality test
python test_agent.py

# Comprehensive test suite
python test_comprehensive.py

# Performance and load testing
python test_comprehensive.py --skip-api
```

### Test Scenarios Covered

- ✅ Environment setup validation
- ✅ Database operations (KB search, ticket creation)
- ✅ AI agent message processing
- ✅ Performance metrics (response times)
- ✅ Error handling (empty messages, special chars)
- ✅ API endpoint functionality
- ✅ Load simulation (concurrent requests)

## Troubleshooting

### 🛠️ Common Issues

#### Setup Issues
1. **Python Version**: Ensure Python 3.8+ is installed
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **API Key Problems**: 
   ```bash
   # Check if API key is set
   python run_agent.py status
   
   # Fix: Edit .env file with correct API key
   ```

3. **Dependencies**: Run automated setup to fix most issues
   ```bash
   python setup.py
   ```

#### Runtime Issues
1. **Database Errors**: Reset and reinitialize
   ```bash
   python -c "from src.db.init_db import reset_db; reset_db()"
   ```

2. **Import Errors**: Reinstall dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. **Server Won't Start**: Check port availability
   ```bash
   python run_agent.py start --port 8001  # Use different port
   ```

### 🔍 Debugging

#### Check System Status
```bash
python run_agent.py status
```

#### Test Core Functionality
```bash
python test_agent.py
```

#### View Detailed Logs
Start the server with debug mode:
```bash
python run_agent.py start --debug
```

#### Manual Test API
```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, can you help me?"}'
```

### 📞 Getting Help

If you're still having issues:
1. Run `python test_comprehensive.py` to see detailed error reports
2. Check that your Google Gemini API key is valid and has sufficient quota
3. Ensure firewall/antivirus isn't blocking port 8000

## Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "src/app.py"]
```

Build and run:
```bash
docker build -t customer-service-agent .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key customer-service-agent
```

## License

This project is licensed under the MIT License.

## Support

For support or questions about the Customer Service Agent, please create an issue in the repository or contact the development team.
