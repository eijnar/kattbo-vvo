#!/bin/sh
set -e

# Make sure the logs directory exists
mkdir -p /app/logs
mkdir -p /app/secrets

# Change ownership of the logs directory
chown -R appuser:appuser /app/logs

# Execute the CMD as appuser
exec gosu appuser "$@"