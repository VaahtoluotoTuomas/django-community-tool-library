#!/bin/bash

# ==============================================================================
# Lainaamo - Deployment Script Template
# 
# INSTRUCTIONS:
# 1. Copy this file and rename it to 'deploy.sh' (which is gitignored).
# 2. Replace the "your-..." placeholders with your actual production values.
# 3. Run the script: ./deploy.sh
# ==============================================================================

# Azure Basic Settings
RG="your-resource-group-name"
NAME="lainaamo-app-prod"
LOCATION="swedencentral" 

# Azure Container Registry (ACR)
ACR_NAME="yourregistryname"
IMAGE="$ACR_NAME.azurecr.io/lainaamo-app:latest"
ACR_PASS="your-acr-password-here"

# Django Production Settings
SECRET_KEY="your-long-random-secret-key-here"
DEBUG="False"

# Database (Note: Azure MySQL requires ssl_mode=REQUIRED)
DB_URL="mysql://db_user:db_password@your-db-server.mysql.database.azure.com:3306/your_db_name?ssl_mode=REQUIRED"

# Azure Blob Storage (For media files)
STORAGE_ACCOUNT="yourstorageaccountname"
STORAGE_STRING="your-storage-connection-string-here"

# Networking and Addresses (DNS Label must be globally unique within the Azure region)
DNS_LABEL="your-unique-dns-label"
ALLOWED_HOSTS="$DNS_LABEL.$LOCATION.azurecontainer.io"

echo "--------------------------------------------------"
echo "🚀 Deploying Lainaamo container to $LOCATION..."
echo "--------------------------------------------------"

az container create \
  --resource-group $RG \
  --name $NAME \
  --image $IMAGE \
  --location $LOCATION \
  --registry-login-server "$ACR_NAME.azurecr.io" \
  --registry-username $ACR_NAME \
  --registry-password "$ACR_PASS" \
  --os-type Linux \
  --cpu 1 \
  --memory 1.5 \
  --ports 8000 \
  --dns-name-label $DNS_LABEL \
  --ip-address Public \
  --environment-variables \
    DATABASE_URL="$DB_URL" \
    ALLOWED_HOSTS="$ALLOWED_HOSTS" \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_STRING" \
    AZURE_STORAGE_ACCOUNT_NAME="$STORAGE_ACCOUNT" \
    SECRET_KEY="$SECRET_KEY" \
    DEBUG="$DEBUG"