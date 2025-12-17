# jsoned

A local application to visualize and edit entities and their relations defined in a JSON Schema. The architecture
of `jsoned` is:

- FastAPI (Python): backend
- SvelteKit (JavaScript): frontend
- MongoDB: database
- Tauri (Rust): framework for building binaries for desktop app


## Development

If you want to develop locally this package, clone the project and enter in the workspace folder:

```sh
git clone https://github.com/BAMresearch/jsoned.git
cd jsoned
```

Create a virtual environment (you can use Python>3.10) in your workspace:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

We recommend using [`uv`](https://docs.astral.sh/uv/) for installing the dependencies:

```sh
uv sync
```

### Run the app

In order to run the app, you need to follow the instructions for different services. Using `uvicorn` you can launch the FastAPI app:

```sh
cd jsoned/
uvicorn main:app --reload
```

The SwaggerUI will help you understand the implemented endpoints.

#### MongoDB Compass

Go to [MongoDB](https://www.mongodb.com/) and install [MongoDB Community Edition](https://www.mongodb.com/docs/manual/administration/install-community/?operating-system=linux&linux-distribution=ubuntu&linux-package=default&search-linux=with-search-linux) and [MongoDB Compass](https://www.mongodb.com/try/download/compass).

Once the installation is finished, launch MongoDB Compass and start a connection with URI `mongodb://localhost:27017`. Name it `json_db`. You can also create a new collection and call it `schemas`. The URI and names of the database and collection are defined in `jsoned/settings.py`.

#### NodeJS

We use `npm` to manage the frontend dependencies. Go to [NodeJS](https://nodejs.org/en) and install `npm`.

You can install and run the SvelteKit server:

```sh
cd gui/
npm run dev
```
