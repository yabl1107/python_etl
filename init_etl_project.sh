#!/bin/bash

PROJECT_NAME="etl_project"

echo "Creando estructura del proyecto: $PROJECT_NAME"

# Directorio raíz
mkdir -p $PROJECT_NAME

# Archivos raíz
touch $PROJECT_NAME/README.md
touch $PROJECT_NAME/pyproject.toml
touch $PROJECT_NAME/.env
touch $PROJECT_NAME/.gitignore

# Config
mkdir -p $PROJECT_NAME/config
touch $PROJECT_NAME/config/__init__.py
touch $PROJECT_NAME/config/settings.py
touch $PROJECT_NAME/config/logging.py
touch $PROJECT_NAME/config/sources.yaml

# Src
mkdir -p $PROJECT_NAME/src
touch $PROJECT_NAME/src/__init__.py

# Extract
mkdir -p $PROJECT_NAME/src/extract
touch $PROJECT_NAME/src/extract/__init__.py
touch $PROJECT_NAME/src/extract/base.py
touch $PROJECT_NAME/src/extract/api.py
touch $PROJECT_NAME/src/extract/database.py
touch $PROJECT_NAME/src/extract/files.py

# Transform
mkdir -p $PROJECT_NAME/src/transform
touch $PROJECT_NAME/src/transform/__init__.py
touch $PROJECT_NAME/src/transform/clean.py
touch $PROJECT_NAME/src/transform/enrich.py
touch $PROJECT_NAME/src/transform/validate.py

# Load
mkdir -p $PROJECT_NAME/src/load
touch $PROJECT_NAME/src/load/__init__.py
touch $PROJECT_NAME/src/load/database.py
touch $PROJECT_NAME/src/load/files.py
touch $PROJECT_NAME/src/load/warehouse.py

# Pipelines
mkdir -p $PROJECT_NAME/src/pipelines
touch $PROJECT_NAME/src/pipelines/__init__.py
touch $PROJECT_NAME/src/pipelines/daily_sales.py

# Utils
mkdir -p $PROJECT_NAME/src/utils
touch $PROJECT_NAME/src/utils/__init__.py
touch $PROJECT_NAME/src/utils/db.py
touch $PROJECT_NAME/src/utils/dates.py
touch $PROJECT_NAME/src/utils/helpers.py

# Tests
mkdir -p $PROJECT_NAME/tests
touch $PROJECT_NAME/tests/test_extract.py
touch $PROJECT_NAME/tests/test_transform.py
touch $PROJECT_NAME/tests/test_load.py

# Scripts
mkdir -p $PROJECT_NAME/scripts
touch $PROJECT_NAME/scripts/run_etl.py

echo "Estructura creada correctamente"
echo "cd $PROJECT_NAME"

