# Stage 1: Build the app
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Set environment variable for Docker build
ENV BUILD_ENV=docker
RUN npm run build

# Stage 2: Serve the built app with a lightweight web server
FROM node:20-alpine AS prod

WORKDIR /app

# Only copy the built output and necessary files
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./

# Install a simple static file server
RUN npm install -g serve

EXPOSE 4173

CMD ["serve", "-s", "build", "-l", "4173"] 