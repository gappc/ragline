# Python helper scripts

## docker container stop, git pull, build and start

```bash
docker-compose stop && git pull && docker-compose build && docker-compose up -d
```

## weaviate_client helper script

```bash
# Show collections
python -c 'from vector_store.weaviate_client import show_collections, show_collection, show_data; show_collections()'

# Show data
python -c 'from vector_store.weaviate_client import show_collections, show_collection, show_data; show_data("Ragline")'

# Use docker container
docker exec -it ragline-server-1 bash --login -c "conda activate ragline && python -c 'from vector_store.weaviate_client import show_collections, show_collection, show_data; show_data(\"Ragline\")'"
```
