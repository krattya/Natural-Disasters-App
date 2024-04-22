# Setup 
1. Install [Docker](https://www.docker.com/products/docker-desktop/)
2. Clone the project.
3. Navigate to the project folder.
4. Run the following Docker Compose command:

```
docker-compose -f .\docker-compose.yaml up -d
```
5. Find the Docs at http://localhost:8000/docs


## Testing
```
PYTHONPATH=. pytest tests/
```

## Notes:
https://github.com/tiangolo/full-stack-fastapi-template

https://github.com/tiangolo/odmantic