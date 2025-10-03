# 🚀 Customer Service Agent - RHEL 10 Setup Guide

## ✅ **System Requirements**
- **OS**: Red Hat Enterprise Linux 10 (RHEL 10)
- **Python**: 3.8+ (check with `python3 --version`)
- **Memory**: 2GB+ RAM recommended
- **Storage**: 1GB+ free space
- **Network**: Internet connection for package installation

---

## 🛠️ **Step-by-Step Installation**

### **Step 1: Clone Repository**
```bash
git clone https://github.com/JibbranAli/Ai-agent-series-agent1-Customer-Service-Agent.git
cd Ai-agent-series-agent1-Customer-Service-Agent
```

### **Step 2: Install Python Dependencies**
```bash
# Install pip if not available
sudo dnf install python3-pip -y

# Install required packages
pip3 install -r requirements.txt
```

### **Step 3: Create Environment File**
```bash
# Copy template and configure your API key
cp env_template.txt .env

# Edit with your Gemini API key
echo "GEMINI_API_KEY=AIzaSyA5w6gUBNgab_q04cQ6mh3KQjcwSvylwtc" > .env
echo "GEMINI_MODEL=gemini-2.0-flash-exp" >> .env
echo "AGENT_HOST=0.0.0.0" >> .env
echo "AGENT_PORT=8000" >> .env
```

### **Step 4: Initialize Database**
```bash
# Initialize database with sample data
python3 src/db/init_db.py
```

### **Step 5: Start the Agent**
```bash
# Option 1: Direct start
python3 src/app.py

# Option 2: Background start
nohup python3 src/app.py > agent.log 2>&1 &
```

---

## 🌐 **Access Your Agent**

### **Web Dashboard**
- **URL**: `http://localhost:8000/dashboard`
- **Features**: Live chat, ticket management, KB search, analytics

### **API Endpoints**
- **Health Check**: `http://localhost:8000/health`
- **API Documentation**: `http://localhost:8000/docs`
- **Message Processing**: `http://localhost:8000/message`

---

## 🎯 **Testing Your Installation**

### **Test 1: Health Check**
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "message": "All systems operational"}
```

### **Test 2: Dashboard Access**
```bash
# Open browser and navigate to:
# http://localhost:8000/dashboard
```

### **Test 3: Send Message**
```bash
curl -X POST "http://localhost:8000/message" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test User",
    "customer_email": "test@example.com",
    "text": "What is your return policy?",
    "session_id": "test123"
  }'
```

---

## 🔧 **Troubleshooting**

### **Port Already in Use (Error: Port 8000 in use)**
```bash
# Find process using port 8000
sudo netstat -tulpn | grep :8000

# Kill the process
sudo kill -9 <PID>

# Start agent again
python3 src/app.py
```

### 🔧 **Permission Denied**
```bash
# Fix Python script permissions
chmod +x src/app.py

# Or run with python3 explicitly
python3 src/app.py
```

### 🔧 **Module Not Found Errors**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --force-reinstall

# Check Python path
python3 -c "import sys; print(sys.path)"
```

### 🔧 **Database Errors**
```bash
# Reset database
rm src/db/agent_data.db
python3 src/db/init_db.py
```

### 🔧 **Firewall Issues**
```bash
# Allow port 8000 through firewall
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# Check firewall status
sudo firewall-cmd --list-ports
```

---

## 🚀 **Production Deployment**

### **Service Setup (Systemd)**
```bash
# Create service file
sudo tee /etc/systemd/system/customer-service-agent.service > /dev/null <<EOF
[Unit]
Description=Customer Service AI Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Ai-agent-series-agent1-Customer-Service-Agent
ExecStart=/usr/bin/python3 src/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable customer-service-agent
sudo systemctl start customer-service-agent

# Check status
sudo systemctl status customer-service-agent
```

### **Nginx Reverse Proxy**
```bash
# Install nginx
sudo dnf install nginx -y

# Create nginx config
sudo tee /etc/nginx/conf.d/customer-agent.conf > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## ✅ **Verification Checklist**

- [ ] Repository cloned successfully
- [ ] Python dependencies installed
- [ ] .env file created with API key
- [ ] Database initialized with 12 KB entries
- [ ] Agent starts without errors
- [ ] Health check returns "healthy"
- [ ] Dashboard loads at `/dashboard`
- [ ] Can send messages via live chat
- [ ] Can create tickets via ticket manager
- [ ] Can search knowledge base
- [ ] Can view analytics

---

## 🎉 **Success!**

Your Customer Service AI Agent is now running on RHEL 10!

**Access Points:**
- **Dashboard**: `http://localhost:8000/dashboard`
- **API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

**Key Features Working:**
- ✅ Live chat interface
- ✅ Ticket management system
- ✅ Knowledge base search
- ✅ Real-time analytics
- ✅ AI-powered responses

The agent is ready for production use! 🤖✨
