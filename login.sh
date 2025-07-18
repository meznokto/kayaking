#!/bin/bash

result=$(curl -X POST -H "Content-Type: application/json" -d "{\"email\": \"$email\", \"password\": \"$password\"}" http://localhost:8000/api/token/ 2>/dev/null)

access=$(jq -r '.access' <<<"$result")
refresh=$(jq -r '.refresh' <<<"$result")

access="$access"
refresh="$refresh"
export access
export refresh
echo "Access token: $access"
echo "Refresh token: $refresh"
