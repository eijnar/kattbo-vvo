#!/bin/sh
set -e

# Make sure the logs directory exists
mkdir -p /app/logs
mkdir -p /app/socket

# Change ownership of the logs directory
chown -R appuser:appuser /app/logs
chown -R appuser:appuser /app/socket

# Execute the CMD as appuser
exec gosu appuser "$@"