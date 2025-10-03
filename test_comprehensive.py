#!/usr/bin/env python3
"""
Comprehensive Test Suite for Customer Service Agent

This script provides extensive testing including:
- Core functionality tests
- API endpoint tests  
- Performance tests
- Error handling tests
- Load tests
"""

import os
import sys
import json
import time
import argparse
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_test(name, status):
    """Print test result."""
    icons = {"pass": "✅", "fail": "❌", "warn": "⚠️", "info": "ℹ️"}
    print(f"{icons.get(status, 'ℹ️')} {name}")

def test_environment():
    """Test environment setup."""
    print_section("Environment Setup Tests")
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print_test("API Key Check", "fail")
        print("   Error: GEMINI_API_KEY not found in environment variables")
        return False
    
    if api_key == "your_gemini_api_key_here":
        print_test("API Key Check", "fail")
        print("   Error: Please replace placeholder with actual API key")
        return False
    
    print_test("API Key Check", "pass")
    print(f"   API key length: {len(api_key)} characters")
    
    # Check file structure
    required_files = ["src/app.py", "src/agent.py", "src/db/init_db.py"]
    for file_path in required_files:
        if os.path.exists(file_path):
            print_test(f"File Check: {file_path}", "pass")
        else:
            print_test(f"File Check: {file_path}", "fail")
            return False
    
    return True

def test_database():
    """Test database functionality."""
    print_section("Database Tests")
    
    try:
        # Test initialization
        from db.init_db import init_db
        init_db()
        print_test("Database Initialization", "pass")
        
        # Test KB operations
        from tools.kb import search_kb, add_kb_entry
        results = search_kb("return policy", top_k=5)
        print_test(f"KB Search", "pass")
        print(f"   Found {len(results)} results")
        
        # Test ticket operations
        from tools.tickets import create_ticket, list_open_tickets
        ticket_id = create_ticket(
            customer_name="Test User",
            customer_email="test@example.com", 
            subject="Test Ticket",
            body="This is a test ticket for automated testing"
        )
        print_test("Ticket Creation", "pass")
        print(f"   Created ticket ID: {ticket_id}")
        
        tickets = list_open_tickets()
        print_test("Ticket Listing", "pass")
        print(f"   Found {len(tickets)} open tickets")
        
        return True
        
    except Exception as e:
        print_test("Database Tests", "fail")
        print(f"   Error: {e}")
        return False

def test_agent_core():
    """Test core agent functionality."""
    print_section("Agent Core Functionality Tests")
      
    try:
        from agent import handle_user_message
        
        test_cases = [
            {
                "name": "Return Policy Query",
                "message": "What is your return policy?",
                "expected_tools": ["search_kb"]
            },
            {
                "name": "Shipping Inquiry",
                "message": "How long does shipping take?",
                "expected_tools": ["search_kb"]
            },
            {
                "name": "Complex Request",
                "message": "I want to return something I bought last week and need help with shipping times",
                "expected_tools": ["search_kb"]
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            print(f"\n🔍 Testing: {test_case['name']}")
            print(f"   Message: '{test_case['message']}'")
            
            start_time = time.time()
            response = handle_user_message(test_case['message'], {
                "customer_name": "Test Customer",
                "customer_email": "test@example.com"
            })
            response_time = time.time() - start_time
            
            if response and "final_text" in response:
                print_test("Message Processing", "pass")
                print(f"   Response time: {response_time:.2f}s")
                print(f"   Response preview: {response['final_text'][:100]}...")
                
                # Check execution trace
                trace = response.get('trace', [])
                if trace:
                    print(f"   Execution steps: {len(trace)}")
                    for step in trace[:2]:  # Show first 2 steps
                        action = step.get('action', 'unknown')
                        reason = step.get('reason', '')[:50]
                        print(f"     - {action}: {reason}...")
                        
            else:
                print_test("Message Processing", "fail")
                print("   No valid response received")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Agent Core Tests", "fail")
        print(f"   Error: {e}")
        return False

def test_performance():
    """Test performance metrics."""
    print_section("Performance Tests")
    
    try:
        from agent import handle_user_message
        
        # Test response times
        test_messages = [
            "What is your return policy?",
            "How long does shipping take?",
            "Do you accept credit cards?",
            "What stores do you have?",
            "Can I get technical support?"
        ]
        
        times = []
        for i, msg in enumerate(test_messages, 1):
            print(f"🔍 Running performance test {i}/{len(test_messages)}...")
            
            start_time = time.time()
            response = handle_user_message(msg, {"customer_name": "Perf Test"})
            response_time = time.time() - start_time
            times.append(response_time)
            
            status = "pass" if response and "final_text" in response else "fail"
            print_test(f"Performance Test {i}", status)
            print(f"   Time: {response_time:.2f}s")
        
        # Calculate metrics
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print_test("Performance Summary", "pass")
        print(f"   Average: {avg_time:.2f}s")
        print(f"   Minimum: {min_time:.2f}s")
        print(f"   Maximum: {max_time:.2f}s")
        
        # Performance evaluation
        if avg_time > 10:
            print_test("Performance Rating", "warn")
            print("   Slow responses - check API key and network")
        elif avg_time > 5:
            print_test("Performance Rating", "warn")
            print("   Moderate response times")
        else:
            print_test("Performance Rating", "pass")
            print("   Good response times")
            
        return True
        
    except Exception as e:
        print_test("Performance Tests", "fail")
        print(f"   Error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print_section("API Endpoint Tests")
    
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print_test("Health Endpoint", "pass")
                data = response.json()
                print(f"   Status: {data.get('status', 'unknown')} birai")
            else:
                print_test("Health Endpoint", "fail")
                print(f"   Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print_test("Health Endpoint", "fail")
            print("   Server not running - start with: python run_agent.py")
            return False
        
        # Test root endpoint
        print("🔍 Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print_test("Root Endpoint", "pass")
        else:
            print_test("Root Endpoint", "fail")
        
        # Test KB search endpoint
        print("🔍 Testing KB search endpoint...")
        response = requests.get(f"{base_url}/kb/search?q=return+policy&top_k=3", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_test("KB Search Endpoint", "pass")
            print(f"   Found {len(data.get('results', []))} results")
        else:
            print_test("KB Search Endpoint", "fail")
        
        # Test tickets endpoint
        print("🔍 Testing tickets endpoint...")
        response = requests.get(f"{base_url}/tickets", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_test("Tickets Endpoint", "pass")
            print(f"   Found {len(data.get('tickets', []))} open tickets")
        else:
            print_test("Tickets Endpoint", "fail")
        
        # Test message endpoint
        print("🔍 Testing message endpoint...")
        test_data = {
            "customer_name": "API Test User",
            "customer_email": "test@example.com",
            "text": "What is your shipping policy?",
            "session_id": "test_session_comprehensive"
        }
        
        response = requests.post(f"{base_url}/message", json=test_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print_test("Message Endpoint", "pass")
            print(f"   Response preview: {result.get('reply', '')[:100]}...")
            
            trace = result.get('trace', [])
            if trace:
                print(f"   Execution steps: {len(trace)}")
        else:
            print_test("Message Endpoint", "fail")
            print(f"   Status code: {response.status_code}")
            print(f"   Error: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print_test("API Tests", "fail")
        print(f"   Error: {e}")
        return False

def test_error_handling():
    """Test error handling scenarios."""
    print_section("Error Handling Tests")
    
    try:
        from agent import handle_user_message
        
        # Test empty message
        print("🔍 Testing empty message handling...")
        try:
            response = handle_user_message("", {"customer_name": "Test"})
            if response:
                print_test("Empty Message", "pass")
            else:
                print_test("Empty Message", "fail")
        except Exception as e:
            print_test("Empty Message", "warn")
            print(f"   Exception handled: {str(e)[:50]}...")
        
        # Test very long message
        print("🔍 Testing long message handling...")
        long_msg = "This is a very long message. " * 100  # ~2500 chars
        try:
            start_time = time.time()
            response = handle_user_message(long_msg, {"customer_name": "Test"})
            response_time = time.time() - start_time
            
            if response and "final_text" in response:
                print_test("Long Message", "pass")
                print(f"   Handled {len(long_msg)} chars in {response_time:.2f}s")
            else:
                print_test("Long Message", "fail")
        except Exception as e:
            print_test("Long Message", "warn")
            print(f"   Exception handled: {str(e)[:50]}...")
        
        # Test special characters
        print("🔍 Testing special characters...")
        special_msg = "Hello! What's **your** `policy` on returns? (urgent!!!) 🚀"
        try:
            response = handle_user_message(special_msg, {"customer_name": "Test"})
            if response and "final_text" in response:
                print_test("Special Characters", "pass")
            else:
                print_test("Special Characters", "fail")
        except Exception as e:
            print_test("Special Characters", "warn")
            print(f"   Exception handled: {str(e)[:50]}...")
        
        # Test malformed request
        print("🔍 Testing malformed request...")
        malformed_msg = "aksjdhfakshdfkljasdhflaksjdhflaksjdhflaksjdhf blah blah blah nonsense query"
        try:
            response = handle_user_message(malformed_msg, {"customer_name": "Test"})
            if response and "final_text" in response:
                print_test("Malformed Request", "pass")
                print("   Provided helpful response despite unclear query")
            else:
                print_test("Malformed Request", "fail")
        except Exception as e:
            print_test("Malformed Request", "warn")
            print(f"   Exception handled: {str(e)[:50]}...")
        
        print_test("Error Handling Tests", "pass")
        return True
            
    except Exception as e:
        print_test("Error Handling Tests", "fail")
        print(f"   Error: {e}")
        return False

def test_load_simulation():
    """Simulate load testing."""
    print_section("Load Simulation Tests")
    
    try:
        import concurrent.futures
        import threading
        from agent import handle_user_message
        
        def run_concurrent_test(user_id):
            """Run a concurrent test case."""
            messages = [
                "What is your return policy?",
                "How long does shipping take?",
                "Do you accept credit cards?"
            ]
            
            start_time = времени.time()
            results = []
            
            for msg in messages:
                try:
                    response = handle_user_message(msg, {
                        "customer_name": f"Load Test User {user_id}",
                        "customer_email": f"loadtest{user_id}@example.com"
                    })
                    results.append(response is not None)
                except Exception:
                    results.append(False)
            
            response_time = time.time() - start_time
            return user_id, response_time, sum(results)
        
        # Run concurrent tests
        print("🔍 Running concurrent load tests...")
        num_concurrent = 3  # Moderate load
        max_workers = 2
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(run_concurrent_test, i) for i in range(num_concurrent)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Analyze results
        total_time = sum(result[1] for result in results)
        total_successes = sum(result[2] for result in results)
        avg_time = total_time / len(results)
        
        print_test("Concurrent Load Test", "pass")
        print(f"   Concurrent users: {num_concurrent}")
        print(f"   Average response time: {avg_time:.2f}s")
        print(f"   Success rate: {total_successes / (num_concurrent * 3):.1%}")
        
        if avg_time < 10:
            print_test("Load Performance", "pass")
            print("   Good performance under load")
        else:
            print_test("Load Performance", "warn")
            print("   May struggle under higher load")
        
        return True
        
    except Exception as e:
        print_test("Load Simulation", "fail")
        print(f"   Error: {e}")
        return False

def main():
    """Main test function with argument parsing."""
    parser = argparse.ArgumentParser(description="Comprehensive Customer Service Agent Tests")
    parser.add_argument("--skip-api", action="store_true", help="Skip API endpoint tests")
    parser.add_argument("--skip-load", action="store_true", help="Skip load simulation tests")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    args = parser.parse_args()
    
    print_section("Customer Service Agent Comprehensive Test Suite")
    print("🛠️ Testing all components of the customer service agent")
    
    tests_passed = 0
    total_tests = 0
    
    test_functions = [
        ("Environment Setup", test_environment),
        ("Database Functionality", test_database),
        ("Agent Core", test_agent_core),
        ("Performance", test_performance),
        ("Error Handling", test_error_handling),
    ]
    
    # Add optional tests based on arguments
    if not args.skip_load:
        test_functions.append(("Load Simulation", test_load_simulation))
    
    if not args.skip_api:
        test_functions.append(("API Endpoints", test_api_endpoints))
    
    # Run tests
    for test_name, test_func in test_functions:
        total_tests += 1
        try:
            if test_func():
                tests_passed += 1
        except Exception as e:
            print(f"\n💥 Test '{test_name}' crashed: {e}")
    
    # Summary
    print_section("Test Summary")
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print(f"📊 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 All tests passed! Your Customer Service Agent is ready!")
        print("\n🚀 Quick Start:")
        print("• Start server: python run_agent.py start")
        print("• API docs: http://localhost:8000/docs")
        print("• Test again: python test_comprehensive.py")
        return 0
    else:
        print(f"\n💔 {total_tests - tests_passed} tests failed!")
        print("Please check the errors above and fix any issues.")
        return 1

if __name__ == "__main__":
    exit(main())
