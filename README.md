# greedflation-scraper

To build the project you'll need:

Docker Engine  
https://docs.docker.com/engine/install/

Docker Compose  
https://docs.docker.com/compose/install/

To build the project
docker-compose build

To run frontend/backend
docker-compose up frontend backend

To run scraper
docker-compose up scraper

Tests
scraper
docker-compose run --rm -e pytest=true scraper
backend
docker-compose run --rm -e FLASK_ENV=test backend