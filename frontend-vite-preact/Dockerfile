# Use cypress image as base, will adjust for multi-stage build later
FROM cypress/base:latest

# Set the working directory to /app
WORKDIR /app

# Copy the package and lock files into the container
COPY package*.json ./

# Add ARG for build
ARG build

# Install any needed packages specified in package.json
# RUN if [ "$build" = "prod" ]; then npm install --production; else npm install; fi
RUN npm install

# Copy the rest of the app code into the container
COPY . .

# Set the build environment based on the build argument
ENV NODE_ENV=${build}

# Expose port 8000
EXPOSE 8000

# Define the command to start the server
CMD if [ "$NODE_ENV" = "prod" ]; then npm run prod; elif [ "$NODE_ENV" = "dev" ]; then npm run dev; elif [ "$NODE_ENV" = "test" ]; then npm run test; else echo "Invalid build argument"; fi