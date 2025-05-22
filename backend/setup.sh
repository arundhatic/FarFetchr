#!/bin/bash
set -e

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run database migration
python init_db.py

echo "Setup complete! Virtual environment is ready and database tables are created." 