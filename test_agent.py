#!/usr/bin/env python3
"""
Test script for the Customer Service Agent
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_agent():
    """Test the customer service agent functionality."""
    
    print("🤖 Customer Service Agent Test Suite")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please set your Google Gemini API key in the .env file")
        return False
    
    if api_key == "your_gemini_api_key_here":
        print("❌ Error: Please replace 'your_gemini_api_key_here' with your actual API key")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Test database initialization
        print("\n📊 Testing database initialization...")
        from db.init_db import init_db
        init_db()
        print("✅ Database initialized successfully")
        
        # Test knowledge base search
        print("\n🔍 Testing knowledge base search...")
        from tools.kb import search_kb
        results = search_kb("return policy", top_k=3)
        if results:
            print(f"✅ KB search working - found {len(results)} results")
            for result in results[:2]:
                print(f"   📄 {result['title']}")
        else:
            print("⚠️ No KB results found - database may need initialization")
        
        # Test ticket creation
        print("\n🎫 Testing ticket creation...")
        from tools.tickets import create_ticket
        ticket_id = create_ticket(
            customer_name="Test User",
            customer_email="test@example.com",
            subject="Test Inquiry",
            body="This is a test ticket created by the test script"
        )
        if ticket_id:
            print(f"✅ Ticket created successfully with ID: {ticket_id}")
        else:
            print("❌ Failed to create ticket")
        
        # Test agent functionality
        print("\n🤖 Testing agent message processing...")
        from agent import handle_user_message
        
        test_message = "What is your return policy?"
        metadata = {"customer_name": "Test Customer", "customer_email": "test@example.com"}
        
        print(f"📝 Testing message: '{test_message}'")
        response = handle_user_message(test_message, metadata)
        
        if response and "final_text" in response:
            print("✅ Agent processed message successfully")
            print(f"📤 Agent response: {response['final_text'][:100]}...")
            
            # Show execution trace
            if "trace" in response:
                print(f"🔍 Execution trace:")
                for i, step in enumerate(response["trace"], 1):
                    action = step.get("action", "unknown")
                    reason = step.get("reason", "")
                    print(f"   {i}. {action}: {reason}")
            
            return True
        else:
            print("❌ Agent failed to process message")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints (requires server to be running)."""
    print("\n🌐 Testing API endpoints...")
    
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️ Health endpoint returned status {response.status_code}")
        
        # Test message endpoint
        test_data = {
            "customer_name": "API Test User",
            "customer_email": "test@example.com",
            "text": "What is your shipping policy?",
            "session_id": "test_session"
        }
        
        response = requests.post(f"{base_url}/message", json=test_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Message endpoint working")
            print(f"📤 Response: {result.get('reply', '')[:100]}...")
        else:
            print(f"⚠️ Message endpoint returned status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️ API server not running - start with: python src/app.py")
    except Exception as e:
        print(f"❌ API test error: {e}")

def main():
    """Run all tests."""
    success = test_agent()
    
    if success:
        print("\n🎉 All core tests passed!")
        print("\nTo test the API endpoints:")
        print("1. Start the server: python src/app.py")
        print("2. Run: python test_agent.py --api")
        print("3. Visit http://localhost:8000/docs for interactive API docs")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        return 1
    
    # Test API if requested
    if "--api" in sys.argv:
        test_api_endpoints()
    
    return 0

if __name__ == "__main__":
    exit(main())
