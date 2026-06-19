import os

class Settings:
    PROJECT_NAME: str = "Cloud Cost & Resource Sentinel SaaS"

    # Database Configuration String mapping our credentials
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://sentinel_admin:SecurePassword123!@localhost:5432/sentinel_saas_db"
    )

settings = Settings()
