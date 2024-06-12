# FastAPI Test Task

## Features

+ Python
+ FastAPI
+ Mysql
+ Docker
+ Alembic for Database Migrations
+ pre-commit hooks

## 1. Clone the repository
```shell
git clone git@github.com
```

## Docker Setup
Create a `.env` file and set database url's
```shell
cp .docker-env .env
```
Build and start Docker Services
```shell
docker compose up --build -d
```
Run alembic migrations
```shell
docker compose run app alembic upgrade head
```

## Non Docker environment setup
### 2. Virtual environment
Create and activate virtual environment:
```shell
cd Test-Task
python3 -m venv env
source env/bin/activate
```

### 3. Create a `.env` file
```shell
cp .env-sample .env
```
Note: set .env values according to your local configurations.

### 4. Database migration
Note: If you are running the app with Mysql, you will probably need to
create the databases as well.

### 5. Install the required modules:
```shell
bash ./setup.sh
```

### 6. Start the Application
```shell
bash run.sh
```
The API will be accessible at [http://localhost:8000](http://localhost:8000).

### 7. API Documentation
Find swagger docs at [http://127.0.1:8000/docs/swagger](http://127.0.0.1:8000/docs/swagger).

To access the Swagger documentation and test the endpoints, visit [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8000/redoc](http://localhost:8000/redoc) in your web browser.
The Swagger UI provides an interactive interface to explore the API, view the available endpoints, and test their functionalities.

Make sure the API server is running before accessing the Swagger UI.

#### example get posts curl:
```
curl -X 'GET' \
  'http://0.0.0.0:8000/api/v1/post/get-posts/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImYwNDhmMWJjLThlOGQtNGU0ZC05NGM3LTc1ZGFlZDdiNTE3YyIsImVtYWlsIjoidXNlcjJAZXhhbXBsZS5jb20iLCJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzIzMzY3MzYyLCJpYXQiOjE3MTgxODMzNjJ9.MnjZO_HYZ8zvtksNlgaDtiGm6lzLV4-8lFLBsOyiBYk'
```
