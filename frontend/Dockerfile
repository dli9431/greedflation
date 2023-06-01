# Use an official Node.js runtime as a parent image
FROM node:latest

# Set the working directory to /app
WORKDIR /app

# Copy the package and lock files into the container
COPY package.json ./

# Add ARG for build
ARG build

# Install any needed packages specified in package.json
RUN if [ "$build" = "production" ]; then npm install --production; else npm install; fi

# Copy the rest of the app code into the container
COPY . .

# Set the build environment based on the build argument
ENV NODE_ENV=${build}

# Expose port 3000
EXPOSE 3000

# Define the command to start the development server
CMD ["npm", "start"]