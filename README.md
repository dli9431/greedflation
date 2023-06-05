# greedflation
App to track grocery store price inflation and shrinkflation.

To build the project you'll need:

Docker Engine  
https://docs.docker.com/engine/install/

Docker Compose  
https://docs.docker.com/compose/install/

---

Environments  
prod / dev / test

Building + running scraper test container  
build=test docker compose build scraper  
build=test docker compose run --rm scraper

Building + running scraper dev container  
build=dev docker compose build scraper  
build=dev docker compose run scraper

Building + running scraper prod container  
build=prod docker compose build scraper  
build=prod docker compose run scraper

Building + running backend test container  
build=test docker compose build backend  
build=test docker compose run --rm backend

Building + running backend dev container  
build=dev docker compose build backend  
build=dev docker compose up backend

Building + running backend prod container  
build=prod docker compose build backend  
build=prod docker compose up backend
