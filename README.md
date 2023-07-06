# Swagger server

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project and enchanced to support holy_grail_api.json swagger specification
This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

and open your browser here:

```
http://localhost:8080/ui/
```
## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server
```
