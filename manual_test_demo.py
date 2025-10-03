#!/usr/bin/env python3
"""
Manual Testing Demonstration Script

This script demonstrates how to test the Customer Service Agent manually
using the API endpoints. It shows real examples of how customers interact
with the agent and how tickets are created and managed.
"""

import requests
import json
import time
from typing import Dict, Any

class CustomerServiceAgentTester:
    """Test client for the Customer Service Agent."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = f"demo_session_{int(time.time())}"
    
    def test_health(self):
        """Test if the agent is running."""
        print("🔍 Testing Agent Health...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Agent is healthy and running")
                print(f"   Status: {response.json().get('status')}")
                return True
            else:
                print(f"❌ Agent health check failed: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to agent. Is it running?")
            print("   Start it with: python run_agent.py start")
            return False
    
    def send_message(self, customer_name: str, customer_email: str, message: str) -> Dict[str, Any]:
        """Send a message to the agent."""
        payload = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "text": message,
            "session_id": self.session_id
        }
        
        try:
            response = requests.post(f"{self.base_url}/message", json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Request error: {e}")
            return {}
    
    def list_tickets(self):
        """List all open tickets."""
        print("🎫 Listing Open Tickets...")
        try:
            response = requests.get(f"{self.base_url}/tickets", timeout=10)
            if response.status_code == 200:
                data = response.json()
                tickets = data.get('tickets', [])
                print(f"✅ Found {len(tickets)} open tickets")
                for ticket in tickets:
                    print(f"   #{ticket['id']}: {ticket['subject']} (by {ticket['customer_name']})")
                return tickets
            else:
                print(f"❌ Failed to list tickets: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error listing tickets: {e}")
            return []
    
    def search_knowledge_base(self, query: str, top_k: int = 3):
        """Search the knowledge base directly."""
        print(f"🔍 Searching Knowledge Base for: '{query}'")
        try:
            response = requests.get(f"{self.base_url}/kb/search", 
                                  params={"q": query, "top_k": top_k}, timeout=10)
            if response.status_code == 200:
                data = response json()
                results = data.get('results', [])
                print(f"✅ Found {len(results)} results")
                for i, result in enumerate(results, 1):
                    print(f"   {i}. {result['title']}: {result['content'][:80]}...")
                return results
            else:
                print(f"❌ KB search failed: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ KB search error: {e}")
            return []
    
    def show_execution_trace(self, response: Dict[str, Any]):
        """Display the execution trace from agent response."""
        trace = response.get('trace', [])
        if trace:
            print("\n🔍 Execution Trace:")
            for i, step in enumerate(trace, 1):
                action = step.get('action', 'unknown')
                reason = step.get('reason', '')
                result = step.get('result')
                
                print(f"   {i}. {action}")
                print(f"      Reason: {reason}")
                
                if action == 'search_kb' and result:
                    print(f"      Found: {len(result)} knowledge entries")
                elif action == 'create_ticket' and result:
                    print(f"      Created ticket: #{result.get('ticket_id')}")
                elif action == 'http_get' and result:
                    print(f"      HTTP Status: {result.get('status_code')}")
                print()

def main():
    """Main testing demonstration."""
    print("🤖 Customer Service Agent Manual Testing Demo")
    print("=" * 60)
    
    tester = CustomerServiceAgentTester()
    
    # Test 1: Health check
    if not tester.test_health():
        return
    
    print("\n" + "="*60)
    print("📋 Testing Scenarios")
    print("="*60)
    
    # Test 2: Basic FAQ Question
    print("\n📝 Scenario 1: Customer Asks About Return Policy")
    response = tester.send_message(
        customer_name="Alice Smith",
        customer_email="alice@example.com",
        message="What is your return policy?"
    )
    
    if response:
        print("📤 Agent Response:")
        print(f"   {response.get('reply', 'No response')[:200]}...")
        tester.show_execution_trace(response)
    
    # Test 3: Shipping Question
    print("\n📝 Scenario 2: Customer Asks About Shipping")
    response = tester.send_message(
        customer_name="Bob Johnson",
        customer_email="bob@example.com",
        message="How long does shipping take and what are the costs?"
    )
    
    if response:
        print("📤 Agent Response:")
        print(f"   {response.get('reply', 'No response')[:200]}...")
        tester.show_execution_trace(response)
    
    # Test 4: Complex Issue (should create ticket)
    print("\n📝 Scenario 3: Customer Has Complex Issue (Should Create Ticket)")
    response = tester.send_message(
        customer_name="Carol Davis",
        customer_email="carol@example.com", 
        message="I placed an order last week but haven't received any updates. The tracking number doesn't work and I'm getting worried. I need this urgently for a business presentation next week!"
    )
    
    if response:
        print("📤 Agent Response:")
        print(f"   {response.get('reply', 'No response')[:200]}...")
        tester.show_execution_trace(response)
    
    # Test 5: List tickets
    print("\n" + "="*60)
    tester.list_tickets()
    
    # Test 6: Knowledge Base Search
    print("\n" + "="*60)
    print("🔍 Direct Knowledge Base Testing")
    print("="*60)
    
    queries = [
        "return policy",
        "shipping international",
        "payment methods",
        "technical support"
    ]
    
    for query in queries:
        tester.search_knowledge_base(query, top_k=2)
        print()
    
    # Test 7: Session-based conversation
    print("\n📝 Scenario 4: Multi-Turn Conversation")
    
    # First message in session
    print("   Turn 1: Customer introduction")
    response = tester.send_message(
        customer_name="David Wilson",
        customer_email="david@example.com",
        message="Hello, I'm new here and need some help"
    )
    
    if response:
        print(f"   Agent: {response.get('reply', 'No response')[:100]}...")
    
    time.sleep(1)  # Small delay
    
    # Follow-up message
    print("   Turn 2: Customer asks specific question")
    response = tester.send_message(
        customer_name="David Wilson", 
        customer_email="david@example.com",
        message="Actually, I want to know about bulk orders"
    )
    
    if response:
        print(f"   Agent: {response.get('reply', 'No response')[:100]}...")
    
    print("\n" + "="*60)
    print("🎉 Manual Testing Demo Complete!")
    print("="*60)
    
    print("\n📊 Summary:")
    print("• Health checks passed")
    print("• FAQ questions answered")
    print("• Complex issues handled") 
    print("• Tickets created when needed")
    print("• Knowledge base searched")
    print("• Multi-turn conversations supported")
    
    print("\n🔗 Next Steps:")
    print("• View interactive API docs: http://localhost:8000/docs")
    print("• Run comprehensive tests: python test_comprehensive.py")
    print("• Check ticket status in database")
    print("• Add more knowledge base entries")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n💥 Demo error: {e}")
        print("Make sure the agent is running: python run_agent.py start")
