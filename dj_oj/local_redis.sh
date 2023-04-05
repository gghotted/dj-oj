docker rm redis-django
docker run --name redis-django -p 6379:6379 redis