concurrency=${1:-1}
celery -A config worker -l debug --concurrency=$concurrency