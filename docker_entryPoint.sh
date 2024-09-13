#!/bin/bash

# Define the static files directory
STATIC_DIR="/src/config/static"

# Check if the directory exists and create it if it does not
if [ ! -d "$STATIC_DIR" ]; then
    echo "*** Creating static files directory: $STATIC_DIR ***"
    mkdir -p "$STATIC_DIR"
else
    echo "*** Static files directory already exists: $STATIC_DIR ***"
fi

# Run database migrations
echo '*** Migrating database ***'
python manage.py migrate || {
    echo 'Migration failed'
    exit 1
}

# Collect static files
echo "*** Collecting static files ***"
python manage.py collectstatic --noinput || {
    echo 'Collectstatic failed'
    exit 1
}

# Run the server
echo '*** Running server ***'
gunicorn --workers=16 --bind 0.0.0.0:8000 config.wsgi:application || {
    echo 'Gunicorn failed'
    exit 1
}
