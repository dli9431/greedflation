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

Containers  
scraper / backend / frontend  

Build + running tests:  
build=test docker-compose build {container}  
build=test docker-compose run --rm {container}

Building + running dev/prod  
build={env} docker-compose up --build -d {container}

Stopping containers  
build={env} docker-compose down
