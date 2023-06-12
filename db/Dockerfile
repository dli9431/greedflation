# Dockerfile
FROM mongo:latest

# set working directory
WORKDIR /usr/src/configs

# copy all the files to the container
COPY . .

EXPOSE 27017
CMD ["mongod"]