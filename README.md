# 2agent Platform Builder

This repository provides a minimal "platform for creating platforms". Use the
`platform_builder` package to capture a platform idea as a blueprint, write it
to disk, and scaffold a starter folder structure with service stubs.

## Features
- Blueprint model for platform metadata, features, and services
- Scaffolder that creates README files and service directories
- Lightweight CLI to create and scaffold blueprints (no external dependencies)

## Usage
Create a blueprint JSON file:

```bash
python -m platform_builder.cli create \
  --name "Data Hub" \
  --description "Platform for data products" \
  --feature "ingestion" --feature "governance" \
  --service "api:REST interface" --service "ui:Admin console" \
  --output blueprint.json
```

Scaffold a platform directory from the saved blueprint:

```bash
python -m platform_builder.cli scaffold blueprint.json --output data-hub
```

The scaffold includes a root `README.md`, the `blueprint.json`, and per-service
folders with their own `README.md` placeholders.

## Development
Run the test suite with the built-in `unittest` runner:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
