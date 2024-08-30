class Config:
    CELERY_BROKER_URL="redis://localhost:12800"
    CELERY_RESULT_BACKEND="redis://localhost:12800"