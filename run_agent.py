#!/usr/bin/env python3
"""
Customer Service Agent Runner Script

Easy script to start the Customer Service Agent server with proper environment setup.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🤖 {title}")
    print("="*60)

def print_info(message):
    """Print info message."""
    print(f"ℹ️ {message}")

def print_error(message):
    """Print error message."""
    print(f"❌ {message}")

def print_success(message):
    """Print success message."""
    print(f"✅ {message}")

def check_environment():
    """Check if the environment is properly set up."""
    python_executable = "venv/Scripts/python" if platform.system().lower() == "windows" else "venv/bin/python"
    
    # Check if virtual environment exists
    if not Path("venv").exists():
        print_error("Virtual environment not found!")
        print_info("Please run: python setup.py")
        return False
    
    # Check if python executable exists in venv
    if not Path(python_executable).exists():
        print_error(f"Python executable not found at {python_executable}")
        print_info("Please run: python setup.py")
        return False
    
    # Check if .env file exists
    if not Path(".env").exists():
        print_error(".env file not found!")
        print_info("Please run: python setup.py")
        return False
    
    print_success("Environment check passed")
    return True

def validate_api_key():
    """Validate that API key is set."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print_error("GEMINI_API_KEY not found in .env file!")
            print_info("Please set your Google Gemini API key in the .env file")
            return False
        
        if api_key == "your_gemini_api_key_here":
            print_error("Please replace 'your_gemini_api_key_here' with your actual API key!")
            print_info("Visit https://aistudio.google.com/ to get your API key")
            return False
        
        print_success(f"API key found (length: {len(api_key)} characters)")
        return True
        
    except ImportError:
        print_error("python-dotenv not installed!")
        print_info("Please run: python setup.py")
        return False

def start_server(host="0.0.0.0", port=8000, debug=False):
    """Start the Customer Service Agent server."""
    python_executable = "venv/Scripts/python" if platform.system().lower() == "windows" else "venv/bin/python"
    
    print_header("Starting Customer Service Agent")
    
    # Environment checks
    if not check_environment():
        return 1
    
    if not validate_api_key():
        return 1
    
    # Database check
    print_info("Checking database...")
    db_path = Path("src/db/agent_data.db")
    if not db_path.exists():
        print_info("Initializing database...")
        try:
            subprocess.run([python_executable, "src/db/init_db.py"], check=True)
            print_success("Database initialized")
        except subprocess.CalledProcessError:
            print_error("Failed to initialize database")
            return 1
    
    print_info(f"Starting server on http://{host}:{port}")
    if debug:
        print_info("Debug mode enabled")
    
    print("\n🚀 Server starting...")
    print("📍 Press Ctrl+C to stop the server")
    print(f"📍 API Documentation: http://{host}:{port}/docs")
    print(f"📍 Health Check: http://{host}:{port}/health")
    print("\n" + "="*60)
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["AGENT_HOST"] = host
        env["AGENT_PORT"] = str(port)
        env["DEBUG"] = str(debug).lower()
        
        # Start the server
        subprocess.run([
            python_executable, "-m", "uvicorn", 
            "src.app:app", 
            "--host", host, 
            "--port", str(port),
            "--reload" if debug else "--no-reload"
        ], env=env)
        
    except KeyboardInterrupt:
        print_header("Server Stopped")
        print_success("Customer Service Agent stopped gracefully")
        return 0
    except Exception as e:
        print_error(f"Failed to start server: {e}")
        return 1

def test_server():
    """Run a quick server test."""
    print_header("Testing Server Health")
    
    python_executable = "venv/Scripts/python" if platform.system().lower() == "windows" else "venv/bin/python"
    
    try:
        subprocess.run([python_executable, "test_agent.py"], check=True)
        print_success("All tests passed!")
        return 0
    except subprocess.CalledProcessError:
        print_error("Tests failed!")
        return 1

def show_status():
    """Show current status and configuration."""
    print_header("Customer Service Agent Status")
    
    # Environment status
    venv_exists = Path("venv").exists()
    env_exists = Path(".env").exists()
    db_exists = Path("src/db/agent_data.db").exists()
    
    print(f"Virtual Environment: {'✅' if venv_exists else '❌'}")
    print(f"Environment File: {'✅' if env_exists else '❌'}")
    print(f"Database: {'✅' if db_exists else '❌'}")
    
    # API key status
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY", "Not set")
        if api_key and api_key != "your_gemini_api_key_here":
            print(f"API Key: {'✅ Set (' + str(len(api_key)) + ' chars)'}")
        else:
            print("API Key: ❌ Not configured")
    except:
        print("API Key: ❌ Cannot check")
    
    print("\n📋 Available Commands:")
    print("• python run_agent.py start    - Start the server")
    print("• python run_agent.py test    - Run tests") 
    print("• python run_agent.py status  - Show this status")
    print("• python run_agent.py --help  - Show all options")

def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(description="Customer Service Agent Management")
    parser.add_argument("command", nargs="?", choices=["start", "test", "status"], default="start",
                       help="Command to run (default: start)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    if args.command == "status":
        show_status()
        return 0
    elif args.command == "test":
        return test_server()
    elif args.command == "start":
        return start_server(args.host, args.port, args.debug)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    exit(main())
