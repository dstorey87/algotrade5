FROM node:20-alpine

WORKDIR /app

# Update npm and install global dependencies first
RUN npm install -g npm@latest && \
    npm install -g ts-node@latest --force

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Next.js app
RUN npm run build

# Expose the port the app will run on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]