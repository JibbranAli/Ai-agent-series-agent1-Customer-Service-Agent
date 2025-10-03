// Customer Service Agent Dashboard JavaScript
class AgentDashboard {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.sessionId = `dashboard_${Date.now()}`;
        this.conversationId = `conversation_${Date.now()}`;
        
        this.init();
    }

    init() {
        this.setupNavigation();
        this.loadDashboardData();
        this.setupEventListeners();
        this.checkAgentHealth();
        
        // Load initial data
        setTimeout(() => {
            this.loadTickets();
            this.searchKnowledgeBase('sample', 12);
        }, 1000);
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        const sections = document.querySelectorAll('.section');

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                
                // Add active class to clicked link
                e.target.closest('.nav-link').classList.add('active');
                
                // Hide all sections
                sections.forEach(section => section.classList.add('hidden'));
                
                // Show target section
                const targetSection = e.target.closest('.nav-link').dataset.section;
                document.getElementById(targetSection).classList.remove('hidden');
                
                // Load section-specific data
                this.loadSectionData(targetSection);
            });
        });

        // Initial active section
        document.getElementById('dashboard').classList.remove('hidden');
    }

    setupEventListeners() {
        // Submit handlers
        document.getElementById('ticketForm')?.addEventListener('submit', (e) => this.createTicket(e));
        document.getElementById('kbForm')?.addEventListener('submit', (e) => this.addKbArticle(e));
    }

    async makeRequest(endpoint, options = {}) {
        const url = `${this.apiBase}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            this.showNotification(`API Error: ${error.message}`, 'error');
            return null;
        }
    }

    async checkAgentHealth() {
        try {
            const health = await this.makeRequest('/health');
            if (health) {
                document.getElementById('agentStatus').textContent = 'Healthy ✅';
                document.getElementById('agentStatus').style.color = '#28a745';
            } else {
                document.getElementById('agentStatus').textContent = 'Unreachable ❌';
                document.getElementById('agentStatus').style.color = '#dc3545';
            }
        } catch (error) {
            document.getElementById('agentStatus').textContent = 'Error ❌';
            document.getElementById('agentStatus').style.color = '#dc3545';
        }
    }

    async loadDashboardData() {
        await this.loadTickets();
        await this.updateStats();
    }

    async updateStats() {
        try {
            // Count open tickets
            const tickets = await this.makeRequest('/tickets');
            document.getElementById('openTicketsCount').textContent = tickets?.tickets?.length || 0;

            // Count KB articles (approximate - search for common terms)
            document.getElementById('kbArticlesCount').textContent = '12'; // Pre-loaded articles
        } catch (error) {
            console.error('Failed to update stats:', error);
        }
    }

    async sendQuickMessage() {
        const input = document.getElementById('quickChatInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage('quickChatMessages', 'user', message);
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator('quickChatMessages');

        try {
            const response = await this.makeRequest('/message', {
                method: 'POST',
                body: JSON.stringify({
                    customer_name: 'Dashboard User',
                    customer_email: 'dashboard@test.com',
                    text: message,
                    session_id: this.sessionId
                })
            });

            this.hideTypingIndicator('quickChatMessages');

            if (response) {
                this.addMessage('quickChatMessages', 'agent', response.reply);
                
                // Show execution trace if available
                if (response.trace && response.trace.length > 0) {
                    this.showExecutionTrace('quickChatMessages', response.trace);
                }
            }
        } catch (error) {
            this.hideTypingIndicator('quickChatMessages');
            this.addMessage('quickChatMessages', 'agent', 'Sorry, I encountered an error processing your request.');
        }
    }

    async sendMainChatMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        const customerName = document.getElementById('customerName').value || 'Customer';
        const customerEmail = document.getElementById('customerEmail').value || 'customer@example.com';
        
        if (!message) return;

        // Add user message to chat
        this.addMessage('chatMessages', 'user', message);
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator('chatMessages');

        try {
            const response = await this.makeRequest('/message', {
                method: 'POST',
                body: JSON.stringify({
                    customer_name: customerName,
                    customer_email: customerEmail,
                    text: message,
                    session_id: this.conversationId
                })
            });

            this.hideTypingIndicator('chatMessages');

            if (response) {
                this.addMessage('chatMessages', 'agent', response.reply);
                
                // Show execution trace in chat
                if (response.trace && response.trace.length > 0) {
                    this.showExecutionTrace('chatMessages', response.trace);
                }
            }
        } catch (error) {
            this.hideTypingIndicator('chatMessages');
            this.addMessage('chatMessages', 'agent', 'Sorry, I encountered an error processing your request.');
        }
    }

    addMessage(containerId, sender, message) {
        const container = document.getElementById(containerId);
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const time = new Date().toLocaleTimeString();
        messageDiv.innerHTML = `
            <div class="message-content">
                ${message}
                <div class="message-time">${time}</div>
            </div>
        `;
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    showTypingIndicator(containerId) {
        const container = document.getElementById(containerId);
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message agent typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-spinner fa-spin"></i> AI is typing...
                <div class="message-time">Now</div>
            </div>
        `;
        container.appendChild(typingDiv);
        container.scrollTop = container.scrollHeight;
    }

    hideTypingIndicator(containerId) {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    showExecutionTrace(containerId, trace) {
        const container = document.getElementById(containerId);
        const traceDiv = document.createElement('div');
        traceDiv.className = 'message agent trace-message';
        
        let traceHtml = '<div class="message-content"><strong>🔍 Execution Trace:</strong><br><br>';
        trace.forEach((step, index) => {
            const action = step.action || 'unknown';
            const reason = step.reason || 'No reason provided';
            
            traceHtml += `
                <div style="margin-bottom: 10px; padding: 8px; background: rgba(102, 126, 234, 0.1); border-radius: 8px;">
                    <strong>${index + 1}. ${action.toUpperCase()}</strong><br>
                    <small>${reason}</small>
                </div>
            `;
            
            if (step.result && typeof step.result === 'object') {
                if (step.result.ticket_id) {
                    traceHtml += `<small>📋 Created ticket #${step.result.ticket_id}</small><br>`;
                } else if (Array.isArray(step.result)) {
                    traceHtml += `<small>📚 Found ${step.result.length} knowledge entries</small><br>`;
                }
            }
        });
        traceHtml += '<div class="message-time">Trace details</div></div>';
        
        traceDiv.innerHTML = traceHtml;
        container.appendChild(traceDiv);
        container.scrollTop = container.scrollHeight;
    }

    async loadTickets() {
        try {
            const response = await this.makeRequest('/tickets');
            if (!response) return;

            const tbody = document.getElementById('ticketsTableBody');
            tbody.innerHTML = '';

            if (response.tickets && response.tickets.length > 0) {
                response.tickets.forEach(ticket => {
                    const row = document.createElement('tr');
                    const statusClass = ticket.status === 'open' ? 'badge-open' : 
                                      ticket.status === 'closed' ? 'badge-closed' : 'badge-in-progress';
                    
                    row.innerHTML = `
                        <td>#${ticket.id}</td>
                        <td>${ticket.customer_name}</td>
                        <td>${ticket.subject}</td>
                        <td><span class="badge ${statusClass}">${ticket.status}</span></td>
                        <td>${new Date(ticket.created_at).toLocaleDateString()}</td>
                        <td>
                            <button class="btn" style="padding: 0.5rem; font-size: 0.8rem;" onclick="dashboard.updateTicketStatus(${ticket.id}, 'closed')">
                                Close
                            </button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            } else {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">No tickets found</td></tr>';
            }
        } catch (error) {
            console.error('Failed to load tickets:', error);
            document.getElementById('ticketsTableBody').innerHTML = 
                '<tr><td colspan="6" class="text-center">Error loading tickets</td></tr>';
        }
    }

    async createTicket(event) {
        event.preventDefault();
        
        const formData = {
            customer_name: document.getElementById('ticketCustomerName').value,
            customer_email: document.getElementById('ticketCustomerEmail').value,
            subject: document.getElementById('ticketSubject').value,
            body: document.getElementById('ticketBody').value,
            priority: document.getElementById('ticketPriority').value
        };

        try {
            const ticketId = await this.makeTicketRequest(formData);
            if (ticketId) {
                this.showNotification(`Ticket #${ticketId} created successfully!`, 'success');
                document.getElementById('ticketForm').reset();
                this.loadTickets();
                this.updateStats();
            }
        } catch (error) {
            this.showNotification('Failed to create ticket', 'error');
        }
    }

    async makeTicketRequest(ticketData) {
        // Since we don't have a direct ticket endpoint, we'll use a message that triggers ticket creation
        const response = await this.makeRequest('/message', {
            method: 'POST',
            body: JSON.stringify({
                customer_name: ticketData.customer_name,
                customer_email: ticketData.customer_email,
                text: `Ticket Request: ${ticketData.subject}. Details: ${ticketData.body}`,
                session_id: this.sessionId
            })
        });

        // Extract ticket ID from the response trace
        if (response && response.trace) {
            const ticketStep = response.trace.find(step => step.action === 'create_ticket');
            if (ticketStep && ticketStep.result && ticketStep.result.ticket_id) {
                return ticketStep.result.ticket_id;
            }
        }

        // If no ticket was created automatically, create one using the database directly
        // This would require adding a direct ticket endpoint to the FastAPI app
        this.showNotification('Ticket was processed as a message. Direct ticket creation not implemented yet.', 'info');
        return null;
    }

    async searchKnowledgeBase(query = null, limit = 5) {
        const searchQuery = query || document.getElementById('kbSearchInput').value;
        if (!searchQuery) return;

        try {
            const response = await this.makeRequest(`/kb/search?q=${encodeURIComponent(searchQuery)}&top_k=${limit}`);
            
 const container = document.getElementById('kbSearchResults');
            
            if (response && response.results && response.results.length > 0) {
                let html = '<h4>Search Results:</h4>';
                response.results.forEach((result, index) => {
                    html += `
                        <div style="margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                            <strong>${index + 1}. ${result.title}</strong><br>
                            <p style="margin-top: 0.5rem; color: #666;">${result.content.substring(0, 200)}...</p>
                        </div>
                    `;
                });
                container.innerHTML = html;
            } else {
                container.innerHTML = '<p>No results found for your search.</p>';
            }
        } catch (error) {
            console.error('KB search failed:', error);
            document.getElementById('kbSearchResults').innerHTML = '<p>Error searching knowledge base.</p>';
        }
    }

    async testAgentExecution() {
        const testMessage = document.getElementById('testMessage').value;
        if (!testMessage) return;

        const container = document.getElementById('executionTrace');
        container.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Testing agent execution...</p>';

        try {
            const response = await this.makeRequest('/message', {
                method: 'POST',
                body: JSON.stringify({
                    customer_name: 'Test User',
                    customer_email: 'test@example.com',
                    text: testMessage,
                    session_id: this.sessionId
                })
            });

            if (response && response.trace) {
                let html = '<h4>Execution Trace Analysis:</h4><br>';
                
                html += '<div class="message agent"><div class="message-content">';
                html += '<strong>Agent Response:</strong><br>';
                html += response.reply;
                html += '</div></div><br>';
                
                html += '<h5>📋 Execution Steps:</h5>';
                response.trace.forEach((step, index) => {
                    const icon = step.action === 'search_kb' ? '🔍' : 
                               step.action === 'create_ticket' ? '🎫' : 
                               step.action === 'respond' ? '💬' : '⚡';
                    
                    html += `
                        <div style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 8px;">
                            <strong>${icon} Step ${index + 1}: ${step.action.toUpperCase()}</strong><br>
                            <div style="margin-top: 8px;">
                                <strong>Reason:</strong> ${step.reason}<br>
                                ${step.args ? `<strong>Arguments:</strong> ${JSON.stringify(step.args)}<br>` : ''}
                                ${step.result ? `<strong>Result:</strong> ${JSON.stringify(step.result).substring(0, 200)}...` : ''}
                            </div>
                        </div>
                    `;
                });
                
                container.innerHTML = html;
            } else {
                container.innerHTML = '<p>No execution trace available.</p>';
            }
        } catch (error) {
            container.innerHTML = '<p>Error testing agent execution.</p>';
        }
    }

    clearChat() {
        document.getElementById('chatMessages').innerHTML = `
            <div class="message agent">
                , ,<div class="message-content">
                    🤖 Hello! I'm your AI Customer Service Agent. How can I assist you today?
                    <div class="message-time">Agent ready</div>
                </div>
            </div>
        `;
        document.getElementById('chatInput').value = '';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            max-width: 300px;
            animation: slideIn 0.3s ease;
        `;

        // Set background color based on type
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            info: '#17a2b8',
            warning: '#ffc107'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        notification.innerHTML = `
            ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'} ${message}
            <button onclick="this.parentElement.remove()" style="background: none; border: none; color: white; float: right; cursor: pointer;">×</button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    loadSectionData(section) {
        switch (section) {
            case 'tickets':
                this.loadTickets();
                break;
            case 'knowledge':
                this.searchKnowledgeBase('policy', 5);
                break;
            case 'analytics':
                this.checkAgentHealth();
                break;
        }
    }

    async updateTicketStatus(ticketId, newStatus) {
        try {
            // This would require implementing this endpoint in the FastAPI app
            this.showNotification(`Ticket status update not implemented yet. Use direct database access for now.`, 'info');
            
            // For now, just reload tickets
            this.loadTickets();
        } catch (error) {
            this.showNotification('Failed to update ticket status', 'error');
        }
    }

    async addKbArticle(event) {
        event.preventDefault();
        
        // This would require adding a direct KB endpoint to the FastAPI app
        this.showNotification('Add KB article feature not implemented yet. Use direct database access.', 'info');
        
        // Clear form
        document.getElementById('kbForm').reset();
    }
}

// Global functions for HTML onclick handlers
let dashboard;

window.addEventListener('DOMContentLoaded', () => {
    dashboard = new AgentDashboard();
});

// Global functions for HTML onclick handlers
function sendQuickMessage() {
    dashboard.sendQuickMessage();
}

function sendMessage() {
    dashboard.sendMainChatMessage();
}

function clearChat() {
    dashboard.clearChat();
}

function createTicket(event) {
    dashboard.createTicket(event);
}

function loadTickets() {
    dashboard.loadTickets();
}

function searchKnowledgeBase() {
    dashboard.searchKnowledgeBase();
}

function testAgentExecution() {
    dashboard.testAgentExecution();
}

function addKbArticle(event) {
    dashboard.addKbArticle(event);
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);
