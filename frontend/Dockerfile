# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy the rest of the source code
COPY . .

# Build the React app
RUN yarn build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine

# Copy built assets from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Expose port 443 for HTTPS
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
