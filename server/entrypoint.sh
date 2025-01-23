#!/bin/sh

# Make migrations and migrate the database.
echo "Making migrations and migrating the database."
python manage.py makemigrations --noinput
if [ $? -ne 0 ]; then 
    echo "Makemigrations failed."
    exit 1
fi

python manage.py migrate --noinput
if [ $? -ne 0 ]; then 
    echo "Migrate failed."
    exit 1
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then 
    echo "Collectstatic failed."
    exit 1
fi
echo "Static files collected."

exec "$@"
