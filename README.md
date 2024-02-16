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

## Add user

### From command line

You can add a user to the database from outside the docker container using the command below. It adds a user with the username `test` and password `123` to the database. The user has the roles `admin` and `user`. Note that the docker container `server` (see [docker-compose.yaml](./docker-compose.yaml)) is supposed to have the name `ragline-server-1` and it must be running for this command to work:

```bash
docker exec -it ragline-server-1 bash --login -c " \
conda activate ragline \
&& python -c '\
from db.database import get_db; \
from db.crud_user import create_user; \
from db import schemas; \
db = next(get_db()); \
user = schemas.UserCreate(username=\"test\", password=\"123\", roles=\"admin,user\"); \
create_user(db, user);' \
"
```

You can run the command above from inside the container as well. Just remove the `docker exec -it ragline-server-1 bash --login -c` part and run the rest of the command.

### From frontend

You can add a user from the frontend via HTTP request (see [curl examples](./curl-example.md)), but you need to have a privileged user with role `admin` to do so. The command line example above is useful when you don't have a privileged user yet (e.g. project initialization).

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
