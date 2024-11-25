# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the source code
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine

# Copy built assets from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy images so that nginx can serve these
COPY --from=build /app/images /usr/share/nginx/html/images

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Expose port 443 for HTTPS
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
