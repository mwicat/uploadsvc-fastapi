default:
  @just --list

# Build images
build:
  @just -f backend/justfile build
  @just -f frontend/justfile build

# Push images
push:
  @just -f backend/justfile push
  @just -f frontend/justfile push

start:
  @docker-compose up --detach
  @docker-compose watch --no-up
