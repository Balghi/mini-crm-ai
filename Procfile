web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8080
worker: celery -A app.worker.celery_app worker --pool=solo --loglevel=info