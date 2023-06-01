# greedflation
App to track grocery store price inflation and shrinkflation.

To build the project you'll need:

Docker Engine  
https://docs.docker.com/engine/install/

Docker Compose  
https://docs.docker.com/compose/install/

---

Building the scraper in dev (test) mode  
docker compose up --build --force-recreate scraper

Building the scraper in production mode  
export build=production  
docker compose up --build scraper

