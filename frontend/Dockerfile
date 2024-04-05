FROM node:20.12.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the application files to the working directory
COPY . .

# Remove the node_modules directory if it exists
RUN rm -rf node_modules

# Install the dependencies
RUN npm install

# Expose the port on which your application runs (adjust if necessary)
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev", "--", "--host"]