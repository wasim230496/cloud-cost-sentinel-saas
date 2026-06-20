from celery import Celery

# Initialize Celery and point it to our local Redis Docker broker port (6379)
celery_engine = Celery(
    "sentinel_workers",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

# Configure execution parameters
celery_engine.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
)

# Dynamic automated worker placeholder task definition
@celery_engine.task(name="tasks.trigger_system_diagnostic")
def trigger_system_diagnostic():
    print("[CELERY WORKER] Asynchronous background system check initialized successfully!")
    return {"status": "workers_operational"}
