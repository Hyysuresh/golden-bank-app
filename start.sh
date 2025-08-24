#!/bin/bash

# --- DevOps Automation Script for Golden Bank App ---
# This script automates the process of building and running all three containers
# to eliminate manual command-line errors.

echo "--- Stopping and removing old containers and images ---"
# Remove any existing containers, networks, and volumes
docker-compose down --volumes

# Remove all images built locally to ensure a fresh start
docker rmi golden-bank-frontend:latest
docker rmi golden-bank-backend:latest

echo "--- Building and running the PostgreSQL container ---"
# Run the database container in the background (-d)
docker run --name golden-bank-db -e POSTGRES_USER=devops -e POSTGRES_PASSWORD=password -e POSTGRES_DB=golden_bank_db -p 5432:5432 -d postgres:13

echo "--- Building and running the Backend container ---"
# Build the backend image
docker build -t golden-bank-backend ./backend

# Run the backend container, linking to the database
docker run --name golden-bank-backend -p 5000:5000 --link golden-bank-db:db -e DB_HOST=db -e DB_NAME=golden_bank_db -e DB_USER=devops -e DB_PASS=password -d golden-bank-backend

echo "--- Building and running the Frontend container ---"
# Build the frontend image
docker build -t golden-bank-frontend ./frontend

# Run the frontend container, which will handle all web traffic
docker run --name golden-bank-frontend -p 80:80 -d golden-bank-frontend

echo "--- All containers are now running! ---"
echo "You can check the status with 'docker ps'"
echo "Access the application at: http://localhost"

