import psycopg
from app.core.config import settings

def init_db():
    """
    Connects to PostgreSQL and initializes foundational multi-tenant tables.
    """
    # Establish connection using the modern psycopg v3 driver
    with psycopg.connect(settings.DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # 1. Create Tenants Table (The SaaS clients)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tenants (
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # 2. Create Cloud Accounts Table (AWS connection coordinates)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cloud_accounts (
                    id SERIAL PRIMARY KEY,
                    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
                    account_name VARCHAR(100) NOT NULL,
                    aws_access_key VARCHAR(100) NOT NULL,
                    aws_secret_key VARCHAR(200) NOT NULL,
                    aws_region VARCHAR(30) DEFAULT 'ap-south-1',
                    is_active BOOLEAN DEFAULT TRUE
                );
            """)

            # 3. Create Cost Optimization Alerts Table (Waste Logs)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cost_alerts (
                    id SERIAL PRIMARY KEY,
                    tenant_id INT REFERENCES tenants(id) ON DELETE CASCADE,
                    resource_type VARCHAR(50) NOT NULL, -- e.g., 'EBS_ORPHAN', 'EC2_IDLE'
                    resource_id VARCHAR(100) NOT NULL,
                    estimated_monthly_waste NUMERIC(10, 2) NOT NULL,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    print("Database tables initialized successfully!")
