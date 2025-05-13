# This file is documentation for Python-webserver

# Prerequires - Python environment

* Python v3.10.17
* pip v25.1.1

# Python depedencies (in requirements.txt)

* Django v5.2.1

# How to by docker compose?

```bash
docker compose up
```

# How to run manually?

## Build docker image

```bash
docker build -t django-image:1 .
```

## Run docker container

```bash
docker run -d --name django-server -p 8000:8000 django-image:1 
```

## Stop docker container

```bash
docker stop django-server 
```

## Remove docker container and docker image

```bash
docker rm django-server && docker rmi django-image:1
```