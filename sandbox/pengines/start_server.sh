#!/bin/bash

# Pengines Server Startup Script

echo "Starting Pengines Server..."
echo "========================================"

cd "$(dirname "$0")"

# Check if SWI-Prolog is installed
if ! command -v swipl &> /dev/null; then
    echo "Error: SWI-Prolog is not installed or not in PATH"
    echo "Please install SWI-Prolog first"
    exit 1
fi

# Check which server to start
if [ "$1" = "simple" ]; then
    echo "Starting simple pengines server..."
    swipl -s pengine_server.pl
elif [ "$1" = "web" ]; then
    echo "Starting web-based pengines server..."
    swipl -s web_pengine_server.pl
else
    echo "Usage: $0 [simple|web]"
    echo ""
    echo "  simple - Start a basic pengines server"
    echo "  web    - Start a web-based pengines server with HTTP interface"
    echo ""
    echo "Examples:"
    echo "  $0 simple"
    echo "  $0 web"
    exit 1
fi
