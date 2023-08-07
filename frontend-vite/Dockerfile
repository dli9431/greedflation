# # Use cypress image as base, will adjust for multi-stage build later
# FROM cypress/base:latest

# # Set the working directory to /app
# WORKDIR /app

# # Copy the package and lock files into the container
# COPY package*.json ./

# # Add ARG for build
# ARG build

# # Install any needed packages specified in package.json
# RUN npm install --target=14.18.1 --target_platform=linux --target_arch=x64

# # Copy the rest of the app code into the container
# COPY . .

# # Set the build environment based on the build argument
# ENV NODE_ENV=${build}

# # Expose port 8000
# EXPOSE 8000

# # Define the command to start the server
# CMD if [ "$NODE_ENV" = "prod" ]; then npm run build; elif [ "$NODE_ENV" = "dev" ]; then npm run dev; elif [ "$NODE_ENV" = "test" ]; then npm run test; else echo "Invalid build argument"; fi

# Stage 1: Build the dependencies
FROM node:latest as builder

# Set the working directory to /app
WORKDIR /app

# Copy the package and lock files into the container
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Stage 2: Create the final container
FROM node:latest

# Set the working directory to /app
WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /app/node_modules /app/node_modules

# Copy the rest of the app code into the container
COPY . .

# Add ARG for build
ARG build

# Set the build environment based on the build argument
ENV NODE_ENV=${build}

# Expose port 8000
EXPOSE 8000

# Define the command to start the server
CMD if [ "$NODE_ENV" = "prod" ]; then npm run build; elif [ "$NODE_ENV" = "dev" ]; then npm run dev; elif [ "$NODE_ENV" = "test" ]; then npm run test; else echo "Invalid build argument"; fi
