#!/bin/bash

result=$(curl -X POST -H "Content-Type: application/json" -d "{\"refresh\": \"$refresh\"}" http://localhost:8000/token/refresh/ 2>/dev/null)

access=$(jq -r '.access' <<<"$result")

access="$access"
export access
echo "New access token: $access"
