# Books API

A simple CRUD API created with FastAPI and SQLAlchemy for PostgreSQL

## Available APIs

It is recommended to test the available APIs from ``[GET] /docs``

- ``[GET] /`` - Root (Check API status)
- ``[POST] /patient`` - Create Patient
- ``[GET] /patient/{id}`` - Find Patient
- ``[GET] /patient`` - Get Patient
- ``[PUT] /patient`` - Update Patient
- ``[DELETE] /patient`` - Delete Patient

## Usage

1. Install [poetry](https://python-poetry.org/)
2. Copy `.env.sample` to create `.env` and fill the environment variables accordingly
3. Run `poetry install` to install dependencies
4. Run `poetry run uvicorn app.main:app` to serve the app

(note: you'll need to have python installed)
