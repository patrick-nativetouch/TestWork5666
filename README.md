## How to run app

### Locally

Requirements
- Python 3.9.10
- Postgresql
- Redis
- Docker
- Celery

1. After cloning repo, create a virtual environment and install required packages and activate environment
```
pip3 install virtualenv 
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

2. Create a .env file and configure required variables there
```
export DATABASE_URL="postgresql://postgres:postgres@localhost/transactions_db"
export API_KEY="your_secure_api_key"
export REDIS_HOST="localhost"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"
```

3. Consume variables per terminal before running the service
```
source .env
```

4. Setup your local database by creating a postgres connection with database named 'transactions_db' which the service will use

5. Run celery worker on your terminal
```
celery -A app.service.celery_app worker --loglevel=info
```

6. Make sure docker, redis, and postgres services are running

7. On a separate terminal, run the service
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Compose

Configurations are already setup in the compose file. Edit the file if neccessary.  Run the docker compose command
```
docker-compose up --build
```
The compose file will be responsible for the database, celery, and redis services.

When restarting, clear the the volumes to keep them clean
```
docker-compose down --volumes
```

# API Documentation

Automatic Swagger documentation is available on /docs endpoint

# Run tests

```
python3 -m pytest tests/tests.py
```