# Ragline

## Start

Although not strictly necessary, it is recommended to create a file for the SQLite database:

```bash
touch ragline.db
```

Then start the project using docker compose (recommended):

```bash
# Build and run docker containers
docker compose build && docker compose up
```

The docker compose file doesn't expose any port by default. You can set the ports in a `docker-compose.override.yaml` file. Use `docker-compose.override.yaml.example` as a template. If you use the template, the frontend will be available at `http://localhost:7824/`.

```bash
# Open browser
http://localhost:7824/
```

## Manual steps

> Note that the manual steps are not recommended, you may encounter problems. **Use the docker compose file instead**.

```bash
# Activate virtual environment
conda activate llamaindex

# Start LLM server
python3 -m llama_cpp.server --config_file models.json

# Start weaviate
cd better_example
docker compose -f docker-compose-weaviate.yaml up

# Start local server
cd better_example
uvicorn server.main:app --host 0.0.0.0 --port 9000 --reload

# Start local frontend server
cd ui-example
npm run dev

# Open browser
http://localhost:5173/
```

## Copy conda dependencies to file

```bash
conda env export --no-builds | grep -v "prefix" > environment.yml
```

## Docker

```bash
# Build docker image for server
docker compose build server

# Build docker image for ui
docker compose build ui
```
