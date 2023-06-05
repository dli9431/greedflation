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

