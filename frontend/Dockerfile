# Use an official Node.js runtime as a parent image
FROM node:latest

# Set the working directory to /app
WORKDIR /app

# Copy the package and lock files into the container
COPY package.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the rest of the app code into the container
COPY . .

# Build the project based on the build argument
ARG build

# Set the build environment based on the build argument
ENV NODE_ENV=${build}

# Build the project with Webpack
# RUN if [ "$NODE_ENV" = "production" ]; then npm run build; fi

# Expose port 3000
EXPOSE 3000

# Define the command to start the development server
CMD ["npm", "start"]