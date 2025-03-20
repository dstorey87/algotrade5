FROM node:20-alpine as development

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

# Development command
CMD ["npm", "run", "dev"]

# Production build stage
FROM node:20-alpine as production

WORKDIR /app

# Update npm and install global dependencies first
RUN npm install -g npm@latest && \
    npm install -g ts-node@latest --force

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --only=production

# Copy the app source
COPY . .

# Clean any previous builds
RUN rm -rf .next

# Build the Next.js app
RUN npm run build

# Expose the port the app will run on
EXPOSE 3000

# Start the application in production mode
CMD ["npm", "start"]