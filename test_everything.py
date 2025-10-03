#!/usr/bin/env python3
"""
Comprehensive test script for Customer Service Agent
Tests all components: API, Database, Agent, Dashboard
"""

import requests
import json
import sys
import time
import os
from pathlib import Path

class AgentTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {"test": test_name, "success": success, "message": message}
        self.test_results.append(result)
        print(f"{status} {test_name}: {message}")
        
    def test_server_startup(self):
        """Test 1: Server startup"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Server Startup", True, "Server running and healthy")
                    return True
                else:
                    self.log_test("Server Startup", False, f"Health check failed: {data}")
                    return False
            else:
                self.log_test("Server Startup", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Startup", False, f"Connection error: {e}")
            return False
    
    def test_dashboard_access(self):
        """Test 2: Dashboard accessibility"""
        try:
            response = self.session.get(f"{self.base_url}/dashboard", timeout=10)
            if response.status_code == 200:
                self.log_test("Dashboard Access", True, "Dashboard loads successfully")
                return True
            else:
                self.log_test("Dashboard Access", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Dashboard Access", False, f"Error: {e}")
            return False
    
    def test_api_docs(self):
        """Test 3: API documentation"""
        try:
            response = self.session.get(f"{self.base_url}/docs", timeout=10)
            if response.status_code == 200:
                self.log_test("API Documentation", True, "Swagger UI accessible")
                return True
            else:
                self.log_test("API Documentation", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Documentation", False, f"Error: {e}")
            return False
    
    def test_knowledge_base_search(self):
        """Test 4: Knowledge base search"""
        try:
            response = self.session.get(f"{self.base_url}/kb/search?q=return&top_k=3", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "results" in data and len(data["results"]) > 0:
                    self.log_test("Knowledge Base Search", True, f"Found {len(data['results'])} results")
                    return True
                else:
                    self.log_test("Knowledge Base Search", False, "No results returned")
                    return False
            else:
                self.log_test("Knowledge Base Search", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Knowledge Base Search", False, f"Error: {e}")
            return False
    
    def test_ticket_listing(self):
        """Test 5: Ticket listing"""
        try:
            response = self.session.get(f"{self.base_url}/tickets", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Ticket Listing", True, f"Found {len(data.get('tickets', []))} tickets")
                return True
            else:
                self.log_test("Ticket Listing", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Ticket Listing", False, f"Error: {e}")
            return False
    
    def test_message_processing(self):
        """Test 6: AI message processing"""
        try:
            payload = {
                "customer_name": "Test User",
                "customer_email": "test@example.com",
                "text": "What is your return policy?",
                "session_id": "test_123"
            }
            response = self.session.post(f"{self.base_url}/message", 
                                       json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "reply" in data and len(data["reply"]) > 0:
                    self.log_test("Message Processing", True, "AI generated valid response")
                    return True
                else:
                    self.log_test("Message Processing", False, "Invalid response format")
                    return False
            else:
                self.log_test("Message Processing", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Message Processing", False, f"Error: {e}")
            return False
    
    def test_ticket_creation(self):
        """Test 7: Direct ticket creation"""
        try:
            payload = {
                "customer_name": "Test Customer",
                "customer_email": "customer@test.com",
                "subject": "Test Ticket",
                "body": "This is a test ticket from automated testing"
            }
            response = self.session.post(f"{self.base_url}/tickets", 
                                       json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "ticket_id" in data:
                    self.log_test("Ticket Creation", True, f"Created ticket #{data['ticket_id']}")
                    return True
                else:
                    self.log_test("Ticket Creation", False, "No ticket ID returned")
                    return False
            else:
                self.log_test("Ticket Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("Ticket Creation", False, f"Error: {e}")
            return False
    
    def test_kb_article_creation(self):
        """Test 8: Knowledge base article creation"""
        try:
            payload = {
                "title": "Test Article",
                "content": "This is a test article for automated testing",
                "category": "Testing",
                "tags": "test automated"
            }
            response = self.session.post(f"{self.base_url}/kb", 
                                       json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "added":
                    self.log_test("KB Article Creation", True, f"Added article: {data.get('title')}")
                    return True
                else:
                    self.log_test("KB Article Creation", False, f"Wrong status: {data}")
                    return False
            else:
                self.log_test("KB Article Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
        except Exception as e:
            self.log_test("KB Article Creation", False, f"Error: {e}")
            return False
    
    def test_model_configuration(self):
        """Test 9: Gemini model configuration"""
        try:
            # Check if .env file exists and contains correct model
            env_file = Path(".env")
            if env_file.exists():
                with open(env_file, 'r') as f:
                    content = f.read()
                    if "gemini-2.0-flash" in content and "AIzaSyA5w6gUBNgab_q04cQ6mh3KQjcwSvylwtc" in content:
                        self.log_test("Model Configuration", True, "Correct Gemini model and API key configured")
                        return True
                    else:
                        self.log_test("Model Configuration", False, "Incorrect model or API key")
                        return False
            else:
                self.log_test("Model Configuration", False, ".env file not found")
                return False
        except Exception as e:
            self.log_test("Model Configuration", False, f"Error: {e}")
            return False
    
    def test_database_connection(self):
        """Test 10: Database connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "All systems operational" in data.get("message", ""):
                    self.log_test("Database Connection", True, "Database accessible and working")
                    return True
                else:
                    self.log_test("Database Connection", False, "Database not properly initialized")
                    return False
            else:
                self.log_test("Database Connection", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Database Connection", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting Comprehensive Agent Tests")
        print("=" * 50)
        
        # Check if server is running first
        if not self.test_server_startup():
            print("\n❌ Server not running! Please start the agent first:")
            print("   python src/app.py")
            return False
        
        print("\n🚀 Running all tests...")
        
        # Run all tests
        tests = [
            self.test_dashboard_access,
            self.test_api_docs,
            self.test_knowledge_base_search,
            self.test_ticket_listing,
            self.test_message_processing,
            self.test_ticket_creation,
            self.test_kb_article_creation,
            self.test_model_configuration,
            self.test_database_connection
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ FAIL {test.__name__}: Test error - {e}")
        
        # Summary
        print(f"\n📊 Test Results Summary:")
        print("=" * 30)
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print(f"\n🎉 ALL TESTS PASSED! Your Customer Service Agent is fully working! 🚀")
            print(f"\n🌐 Access Points:")
            print(f"   Dashboard: {self.base_url}/dashboard")
            print(f"   API Docs:  {self.base_url}/docs")
            print(f"   Health:    {self.base_url}/health")
            return True
        else:
            print(f"\n⚠️  Some tests failed. Please check the output above for details.")
            return False

if __name__ == "__main__":
    tester = AgentTester()
    
    # Wait a moment for any ongoing processes
    print("Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    # Run comprehensive tests
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)
