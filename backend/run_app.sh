#!/bin/sh

exec poetry run gunicorn \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind '0.0.0.0:5000' \
    --chdir src \
    'uploadsvc:app'
