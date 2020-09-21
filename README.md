# Flask-Redis-Postgres-Docker-app
A simple app to use and explore docker and docker-compose to build a web application

To run this application:

1. clone the repository
2. create a `.env` in the root of the repo and add
    ```
    USERNAME=admin username for postgres db
    PASSWORD=admin password for postgres db
    ```
3. run the docker-compose files:
   
   for dev: `docker-compose -f ./docker-compose.dev.yml up`
   
   for prod: `docker-compose up`
4. the application should be up and running in `http://localhost:80`

