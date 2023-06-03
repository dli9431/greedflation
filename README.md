# greedflation
App to track grocery store price inflation and shrinkflation.

To build the project you'll need:

Docker Engine  
https://docs.docker.com/engine/install/

Docker Compose  
https://docs.docker.com/compose/install/

---

Building the scraper in dev (test) mode  
build=development docker compose build scraper

Running scraper in test mode  
build=development docker compose run --rm scraper

Building the scraper in production mode  
build=production docker compose build scraper

Running the scraper in production mode  
build=production docker compose run --rm scraper

