#!/bin/bash

# Check if migrations exist
if [ -z "$(ls -A migrations/versions)" ]; then
    echo "No migrations found. Initializing and creating initial migration..."
    flask db init
    flask db migrate -m "Initial migration"
else
    echo "Migrations exist. Skipping init and migrate."
fi

# Always upgrade to apply migrations
flask db upgrade
