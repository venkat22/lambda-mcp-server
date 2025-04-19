#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting MCP Client..."

# Config file for storing MCP URL
CONFIG_FILE=".mcp-config"

# Function to read MCP URL from config file
get_saved_mcp_url() {
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    fi
}

# Get saved MCP URL if it exists
SAVED_MCP_URL=$(get_saved_mcp_url)

# Prompt for MCP URL with default if available
if [ -n "$SAVED_MCP_URL" ]; then
    read -p "Enter MCP server URL (press Enter to use saved: $SAVED_MCP_URL): " MCP_URL
    MCP_URL=${MCP_URL:-$SAVED_MCP_URL}
else
    read -p "Enter MCP server URL: " MCP_URL
fi

# Save the URL for next time
echo "$MCP_URL" > "$CONFIG_FILE"

echo "📦 Getting AWS credentials from your current session..."

# Get the current role being used and verify AWS access
CURRENT_ROLE=$(aws sts get-caller-identity --query 'Arn' --output text)
if [ $? -ne 0 ]; then
    echo "❌ Failed to get AWS credentials. Please check your AWS configuration."
    exit 1
fi
echo "🔑 Using AWS Role: $CURRENT_ROLE"

# Get credentials from current session
echo "🔄 Getting AWS credentials..."
CREDS=$(aws configure export-credentials)
if [ $? -ne 0 ]; then
    echo "❌ Failed to export AWS credentials"
    exit 1
fi

# Extract credentials
AWS_ACCESS_KEY_ID=$(echo "$CREDS" | jq -r '.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | jq -r '.SecretAccessKey')
AWS_SESSION_TOKEN=$(echo "$CREDS" | jq -r '.SessionToken')
AWS_REGION=$(aws configure get region)

if [ -z "$AWS_REGION" ]; then
    AWS_REGION="us-west-2"
    echo "⚠️  No AWS region found in config, defaulting to $AWS_REGION"
else
    echo "✅ Using region: $AWS_REGION"
fi

# Build the container
echo "🏗️  Building the client container..."
docker build -t mcp-client ./client

# Run the container
echo "🚀 Running the client container..."
docker run -it \
    -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
    -e AWS_SESSION_TOKEN="$AWS_SESSION_TOKEN" \
    -e AWS_REGION="$AWS_REGION" \
    -e NODE_ENV=development \
    -e MCP_URL="$MCP_URL" \
    -v "$(pwd)/client/src:/app/src" \
    mcp-client 