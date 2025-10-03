# 🎛️ Customer Service Agent Web Dashboard Guide

## 🚀 **Quick Start**

Your Customer Service Agent now has a **beautiful web dashboard**! No more curl commands needed!

### **Step 1: Start Your Agent**
```bash
# Option 1: Easy start
python run_agent.py start

# Option 2: Quick setup and start
python quickstart.py

# Option 3: Direct start
python src/app.py
```

### **Step 2: Open Dashboard**
Navigate to: **`http://localhost:8000/dashboard`**

---

## 📱 **Dashboard Features Overview**

### **🏠 Dashboard Tab**
- **Quick Chat**: Test the agent immediately
- **Statistics**: Live counts of tickets, KB articles, and agent health
- **System Status**: Real-time health monitoring

### **💬 Live Chat Tab**
- **Simulate Customers**: Enter customer details and chat
- **Multi-turn Conversations**: Maintain context across messages
- **Execution Traces**: See exactly what the agent did
- **Visual Response Display**: Beautiful chat interface

### **🎫 Tickets Tab**
- **Create Tickets**: Add support tickets manually
- **View All Tickets**: See ticket details, status, customers
- **Update Status**: Change ticket status (open → in_progress → closed)
- **Priority Levels**: Set urgent/high/medium/low priority

### **📚 Knowledge Base Tab**
- **Search Interface**: Find FAQ articles instantly
- **Add Articles**: Create new knowledge base entries
- **Browse Content**: View all 12 pre-loaded articles
- **Real-time Search**: Test search functionality

### **📈 Analytics Tab**
- **Performance Testing**: Test execution speed and traces
- **Health Monitoring**: Check database and API status
- **Execution Analysis**: View step-by-step agent decisions
- **Performance Metrics**: Monitor response times

---

## 🎯 **Practical Examples**

### **Example 1: Test Return Policy Question**
1. **Open**: `http://localhost:8000/dashboard`
2. **Go to**: Live Chat tab
3. **Enter Customer**: "John Doe", "john@example.com"
4. **Type Message**: "I want to return something I bought last week"
5. **Watch**: Agent searches KB and provides detailed response
6. **Continue**: "How long does the refund take?"
7. **See**: Agent maintains context and gives specific timing

### **Example 2: Create Support Ticket**
1. **Go to**: Tickets tab
2. **Fill Form**:
   - Customer: "Sarah Wilson"
   - Email: "sarah@example.com"
   - Subject: "Order not delivered after 2 weeks"
   - Description: "I placed order #12345 on Jan 1st..."
   - Priority: High
3. **Click**: "Create Ticket"
4. **View**: See your ticket in the "Open Tickets" table

### **Example 3: Search Knowledge Base**
1. **Go to**: Knowledge Base tab
2. **Search**: "shipping international" → See shipping info
3. **Search**: "payment methods" → See payment options
4. **Add New Article**:
   - Title: "Express Delivery Options"
   - Content: "We offer same-day delivery for orders over $100..."
   - Category: "Shipping"
   - Tags: "express delivery same-day"

### **Example 4: Analyze Agent Performance**
1. **Go to**: Analytics tab
2. **Test Simple Query**: "What is your return policy?"
3. **Test Complex Query**: "I have multiple issues with my order and need urgent help"
4. **Compare**: Execution traces and response times
5. **Monitor**: System health status

---

## 🔧 **Troubleshooting**

### **Dashboard Won't Load**
```bash
# Check if agent is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", "message": "All systems operational"}

# Check agent status
python run_agent.py status
```

### **JavaScript Not Loading**
- **Check**: Browser console (F12 → Console tab)
- **Verify**: Files exist - `ls src/frontend/`
- **Restart**: Agent server completely

### **Dashboard Features Not Working**
1. **Verify Agent URL**: Ensure it's `http://localhost:8000`
2. **Check Browser**: Try different browser or incognito mode
3. **Test API**: Visit `http://localhost:8000/docs` for API interface

---

## 🆚 **Dashboard vs Command Line**

| Action | Dashboard | Command Line |
|--------|-----------|--------------|
| **Test Agent** | ✅ Click and chat | `curl -X POST ...` |
| **Create Ticket** | ✅ Fill form | Manual database insert |
| **Search KB** | ✅ Visual interface | `curl /kb/search` |
| **View Traces** | ✅ Formatted display | Raw JSON output |
| **Update Tickets** | ✅ Click buttons | Database queries |
| **Monitor Health** | ✅ Visual status | `curl /health` |

---

## 🌐 **Access Points**

- **Main Dashboard**: `http://localhost:8000/dashboard`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Direct API**: `http://localhost:8000/message`

---

## 🚀 **Why Use the Dashboard?**

### **✅ Advantages**
- **🚀 Fast Setup**: No commands to remember
- **👀 Visual**: Beautiful, intuitive interface
- **🔍 Debugging**: See execution traces clearly
- **📊 Analytics**: Performance monitoring built-in
- **🎯 Testing**: Easy customer scenario simulation
- **📱 Responsive**: Works on mobile and desktop

### **📈 Productivity Boost**
- **5x Faster**: Than typing curl commands
- **Real-time**: Instant feedback and updates
- **Visual Debug**: See agent thinking process
- **Professional**: Demo-ready interface
- **Accessible**: Works on any device with browser

---

## 🎉 **Success!**

Your Customer Service AI Agent now has a **professional web dashboard** that makes testing and management incredibly easy!

**Access it now**: `http://localhost:8000/dashboard`

No more command-line complexity - just point, click, and interact with your AI agent visually! 🤖✨
