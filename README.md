# greedflation-scraper

To build the project you'll need:

Docker Engine  
https://docs.docker.com/engine/install/

Docker Compose  
https://docs.docker.com/compose/install/

To build the project container  
docker-compose build

To run tests  
docker-compose run --rm -e pytest=true scraper