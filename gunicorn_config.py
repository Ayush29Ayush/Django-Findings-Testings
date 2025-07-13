import multiprocessing
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "info"
errorlog = os.path.join(BASE_DIR, "media/logs/gunicorn_error.log")
accesslog = os.path.join(BASE_DIR, "media/logs/gunicorn_access.log")

# Run server : gunicorn project.wsgi:application -c gunicorn_config.py