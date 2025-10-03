#!/usr/bin/env python3
"""
Customer Service Agent Setup Script

This script handles the complete setup process for the Customer Service Agent:
1. Checks for Python 3.8+ compatibility
2. Creates and activates virtual environment
3. Installs dependencies
4. Sets up database
5. Validates environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_step(step, message):
    """Print a formatted step."""
    print(f"\n📍 Step {step}: {message}")
    print("-" * 40)

def check_python_version():
    """Check if Python version is compatible."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print("Please upgrade your Python installation.")
        return False
    
    print("✅ Python version is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    print_step(2, "Setting up Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        
        # Check if we need to recreate it
        response = input("Do you want to recreate the virtual environment? (y/N): ").lower()
        if response in ['y', 'yes']:
            print("🗑️ Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print("✅ Using existing virtual environment")
            return True
    
    try:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activation_script():
    """Get the appropriate activation script for the platform."""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "venv/bin/activate"

def install_dependencies():
    """Install required dependencies."""
    print_step(3, "Installing Dependencies")
    
    activation_script = get_activation_script()
    pip_path = "venv/Scripts/pip" if platform.system().lower() == "windows" else "venv/bin/pip"
    
    try:
        print("📦 Installing packages from requirements.txt...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Could not find pip at {pip_path}")
        print("Please ensure the virtual environment was created correctly")
        return False

def setup_environment_file():
    """Set up the environment configuration file."""
    print_step(4, "Setting up Environment Configuration")
    
    env_file = Path(".env")
    env_template = Path("env_template.txt")
    
    if env_file.exists():
        print("📄 .env file already exists")
        response = input("Do you want to update it? (y/N): ").lower()
        if response not in ['y', 'yes']:
            print("✅ Using existing .env file")
            return True
    
    if not env_template.exists():
        print("❌ env_template.txt not found")
        return False
    
    try:
        # Copy template to .env
        import shutil
        shutil.copy(env_template, env_file)
        print("📄 Created .env file from template")
        
        print("\n🔑 IMPORTANT: You need to set your Google Gemini API key!")
        print("1. Visit https://aistudio.google.com/")
        print("2. Create an API key")
        print("3. Edit the .env file and replace 'your_gemini_api_key_here'")
        print(f"4. Location: {env_file.absolute()}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def initialize_database():
    """Initialize the database."""
    print_step(5, "Initializing Database")
    
    python_path = "venv/Scripts/python" if platform.system().lower() == "windows" else "venv/bin/python"
    
    try:
        subprocess.run([python_path, "src/db/init_db.py"], check=True)
        print("✅ Database initialized successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def validate_setup():
    """Validate the setup."""
    print_step(6, "Validating Setup")
    
    python_path = "venv/Scripts/python" if platform.system().lower() == "windows" else "venv/bin/python"
    
    try:
        print("🧪 Running test script...")
        result = subprocess.run([python_path, "test_agent.py"], 
                             capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Setup validation successful!")
            print("\n🎉 Customer Service Agent is ready to use!")
            print("\n📍 Next steps:")
            print("1. Start the server: python run_agent.py")
            print("2. Test the API: http://localhost:8000/docs")
            print("3. Run tests: python test_agent.py")
            return True
        else:
            print("❌ Setup validation failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Validation timed out - this might indicate an API key issue")
        print("Please check your .env file and try again")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def main():
    """Main setup function."""
    print_header("Customer Service Agent Setup")
    print("This script will set up everything needed to run the Customer Service Agent.")
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Virtual Environment", create_virtual_environment),
        ("Install Dependencies", install_dependencies),
        ("Environment Configuration", setup_environment_file),
        ("Database Initialization", initialize_database),
        ("Setup Validation", validate_setup)
    ]
    
    for name, func in steps:
        if not func():
            print(f"\n💥 Setup failed at: {name}")
            print("Please fix the errors and run the setup script again.")
            return 1
    
    print_header("Setup Complete!")
    print("🎉 Your Customer Service Agent is ready!")
    print("\n📋 Quick Commands:")
    print("• Start agent: python run_agent.py")
    print("• Run tests: python test_agent.py")
    print("• API docs: http://localhost:8000/docs")
    
    return 0

if __name__ == "__main__":
    exit(main())
