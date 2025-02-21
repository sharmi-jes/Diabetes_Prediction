import os
from pathlib import Path
import logging

# Project name
project_name = "diabetes_prediction"

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

logging.info("Starting file creation process...")

# List of files to create
list_of_files = [
    '.github/workflows/.gitkeep',
    f'Diabetes/{project_name}/components/__init__.py',
    f'Diabetes/{project_name}/constants/__init__.py',
    f'Diabetes/{project_name}/entity/__init__.py',
    f'Diabetes/{project_name}/pipeline/__init__.py',
    f'Diabetes/{project_name}/utils/__init__.py',
    f'Diabetes/logging.py',
    f'Diabetes/exception.py',
    'setup.py',
    'templates/index.html',
    'app.py',
    'main.py',
    'push.py'
]

# Creating directories and files
for filename in list_of_files:
    filepath = Path(filename)
    file_dir, file_name = os.path.split(filepath)

    # Create directory if it does not exist
    if file_dir:
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory: {file_dir}")

    # Create file if it does not exist or is empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")



