#!/usr/bin/env python3
"""
Customer Service Agent Quickstart Script

One-click script to get the Customer Service Agent running quickly.
Does basic setup, installation, and starts the agent.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "🚀" + "="*58)
    print(f"  {title}")
    print("🚀" + "="*58)

def print_step(step, message):
    """Print a formatted step."""
    print(f"\n📍 {step}: {message}")
    print("─" * 50)

def quick_setup():
    """Quick setup and start process."""
    print_header("Customer Service Agent Quickstart")
    print("⚡ Getting your AI customer service agent up and running...")
    
    # Step 1: Check Python
    print_step("1/6", "Checking Python installation")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required! Please upgrade Python.")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Step 2: Install dependencies
    print_step("2/6", "Installing dependencies")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Step 3: Setup environment
    print_step("3/6", "Setting up environment")
    if not Path(".env").exists():
        if Path("env_template.txt").exists():
            import shutil
            shutil.copy("env_template.txt", ".env")
            print("📄 Created .env file from template")
            print("🔑 IMPORTANT: Edit .env with your API key!")
            
            # Show API key instructions
            print("\n   To get your Google Gemini API key:")
            print("   1. Visit: https://aistudio.google.com/")
            print("   2. Create an API key")
            print("   3. Edit .env file and replace 'your_gemini_api_key_here'")
            
            response = input("\n   Continue anyway? (y/N): ").lower()
            if response not in ['y', 'yes']:
                print("⏸️ Setup paused. Run quickstart.py again after setting your API key.")
                return False
        else:
            print("⚠️ No .env template found")
    else:
        print("📄 Using existing .env file")
    
    # Step 4: Initialize database
    print_step("4/6", "Initializing database")
    try:
        subprocess.run([sys.executable, "src/db/init_db.py"], 
                      check=True, capture_output=True)
        print("✅ Database initialized")
    except subprocess.CalledProcessError:
        print("⚠️ Database initialization failed - will retry later")
    
    # Step 5: Quick test
    print_step("5/6", "Quick functionality test")
    try:
        result = subprocess.run([sys.executable, "test_agent.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Core functionality test passed")
        else:
            print("⚠️ Some tests failed - check your API key")
    except subprocess.TimeoutExpired:
        print("⚠️ Test timed out - likely API key issue")
    except Exception as e:
        print(f"⚠️ Test error: {e}")
    
    # Step 6: Start server
    print_step("6/6", "Starting Customer Service Agent")
    
    print("\n🎯 Starting the agent...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📍 API documentation: http://localhost:8000/docs")
    print("📍 Press Ctrl+C to stop the server")
    print("\n" + "─" * 60)
    
    try:
        # Start the FastAPI server
        subprocess.run([sys.executable, "-m", "uvicorn", "src.app:app", 
                       "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\n⏹️ Agent stopped by user")
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        return False
    
    return True

def show_help():
    """Show help information."""
    print_header("Customer Service Agent Help")
    
    print("🌟 What is this?")
    print("   An AI-powered customer service agent that can:")
    print("   • Answer customer questions using knowledge base")
    print("   • Create support tickets automatically")
    print("   • Provide intelligent responses via REST API")
    
    print("\n📋 Quick Commands:")
    print("   python quickstart.py        - Auto setup and start")
    print("   python setup.py             - Manual setup")
    print("   python run_agent.py start   - Start agent only")
    print("   python test_agent.py         - Run tests")
    
    print("\n🔧 Manual Setup:")
    print("   1. pip install -r requirements.txt")
    print("   2. Copy env_template.txt to .env")
    print("   3. Add your Google Gemini API key to .env")
    print("   4. python src/db/init_db.py")
    print("   5. python src/app.py")
    
    print("\n🌐 After Starting:")
    print("   • Main API: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("   • Message Endpoint: POST /message")
    
    print("\n📞 Test Your Agent:")
    print("   curl -X POST http://localhost:8000/message \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"text\": \"What is your return policy?\"}'")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h", "help"]:
            show_help()
            return 0
    
    try:
        success = quick_setup()
        if success:
            print("\n🎉 Customer Service Agent is running!")
            print("🌐 Visit http://localhost:8000/docs to try it out")
        else:
            print("\n💔 Setup failed! Try running: python setup.py")
            return 1
    except KeyboardInterrupt:
        print("\n👋 Quickstart cancelled by user")
        return 0
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Please try: python setup.py")
        return 1

if __name__ == "__main__":
    exit(main())
