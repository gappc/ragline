# ragline-server

```bash
# Start weaviate
docker compose -f docker-compose-weaviate.yaml up

# Start local server
uvicorn server.main:app --host 0.0.0.0 --port 9000 --reload
```
