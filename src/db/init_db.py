import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agent_data.db")

def init_db():
    """Initialize the database with tables and sample data."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tickets table
    c.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        body TEXT,
        status TEXT DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'closed', 'pending')),
        priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # KB: FTS5 (Full Text Search)
    c.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS kb USING fts5(
        title, 
        content, 
        category,
        tags
    )''')
    
    # Clear existing KB data to avoid duplicates
    c.execute("DELETE FROM kb")
    
    # Seed knowledge base with comprehensive customer service data
    kb_samples = [
        ("Return Policy", 
         "Our return policy allows customers to return items within 30 days of purchase for a full refund. Items must be in original condition with tags attached. Returns can be processed online or in-store. Refunds are issued within 5-7 business days after we receive the returned item.",
         "Policies",
         "return refund 30-days original-condition"),

        ("Shipping Information", 
         "We offer multiple shipping options: Standard (5-8 business days, free on orders over $50), Express (2-3 business days, $9.99), and Overnight (next business day, $19.99). Tracking information is provided for all shipments.",
         "Shipping",
         "shipping standard express overnight tracking"),

        ("Payment Methods",
         "We accept all major credit cards (Visa, MasterCard, American Express, Discovery), PayPal, Apple Pay, Google Pay, and gift cards. For orders over $500, we also offer payment plans.",
         "Payment",
         "credit-card paypal apple-pay google-pay gift-cards payment-plans"),

        ("Product Warranty",
         "All products come with a 1-year manufacturer warranty covering defects in materials and workmanship. Extended warranties are available for purchase. Warranty claims can be submitted online or by calling our support team.",
         "Warranty",
         "warranty manufacturing-defects extended-warranty claims"),

        ("Account Management",
         "You can manage your account through our customer portal where you can view order history, update payment methods, change delivery addresses, and track package status. Password reset can be done through the login page.",
         "Account",
         "account portal order-history payment-methods address password-reset"),

        ("Technical Support",
         "For technical issues with products, please check our troubleshooting guides on the product pages or contact our technical support team. We provide step-between troubleshooting, warranty service, and replacement for defective items.",
         "Support",
         "technical-support troubleshooting warranty-service replacements"),

        ("Bulk Orders",
         "We offer special pricing for bulk orders with a minimum quantity of 50 units. Volume discounts start at 10% off retail pricing and can go up to 25% for larger orders. Contact our sales team for customized pricing.",
         "Sales",
         "bulk-orders volume-discounts minimum-quantity sales-team"),

        ("International Shipping",
         "We ship internationally to most countries worldwide. International shipping takes 7-14 business days. Duties and taxes are the responsibility of the customer. Some restrictions may apply based on destination country.",
         "International",
         "international-shipping duties taxes restrictions destination-country"),

        ("Live Chat Hours",
         "Our live chat support is available Monday through Friday, 8 AM to 6 PM EST. Weekend support is available Saturday 10 AM to 4 PM EST. Average response time is under 2 minutes during business hours.",
         "Support Hours",
         "live-chat business-hours monday-friday weekend-response-time"),

        ("Store Locations",
         "We have physical stores in New York, Los Angeles, Chicago, Miami, and Dallas. Store hours are Monday-Saturday 10 AM to 9 PM, Sunday 12 PM to 6 PM. All stores offer product demonstrations, repair services, and same-day pickup for online orders.",
         "Stores",
         "physical-stores nyc los-angeles chicago miami dallas store-hours demonstrations"),

        ("Price Match",
         "We offer a 30-day price match guarantee. If you find an item for less from an authorized retailer, we'll match the price plus give you 10% of the difference as store credit. Original receipt required.",
         "Policies",
         "price-match guarantee authorized-retailer difference store-credit"),

        ("Gift Cards",
         "Gift cards are available for purchase in denominations from $25 to $500. They can be used online and in stores, have no expiration date, and cannot be refunded or exchanged for cash. Gift cards make perfect gifts for any occasion.",
         "Gifts",
         "gift-cards denominations expiration-date perfect-gifts")
    ]
    
    # Insert sample KB data
    for title, content, category, tags in kb_samples:
        c.execute("""
        INSERT INTO kb(title, content, category, tags) VALUES(?, ?, ?, ?)
        """, (title, content, category, tags))
    
    # Insert sample ticket for testing
    c.execute("""
    INSERT OR IGNORE INTO tickets(customer_name, customer_email, subject, body, priority) 
    VALUES(?, ?, ?, ?, ?)
    """, ("John Doe", "john.doe@example.com", "Order Status Inquiry", 
          "I placed an order last week and haven't received any shipping updates. Order number is #12345.", "medium"))
    
    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")
    print(f"Added {len(kb_samples)} knowledge base entries")

def reset_db():
    """Reset the database by dropping and recreating all tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

if __name__ == "__main__":
    init_db()
