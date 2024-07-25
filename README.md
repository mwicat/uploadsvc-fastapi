# uploadsvc service - fastapi version

## Running

1. Install and run [Docker Engine](https://docs.docker.com/engine/install/).
2. Install [Just](https://github.com/casey/just) command runner.
3. Run:

```shell
just build start
```

4. Browse for [frontend](http://localhost:5001/) and [backend](http://localhost:5000/) 

## Adding frontend dependency

```
cd frontend
just npm_install PACKAGE_NAME
```
