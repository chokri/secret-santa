# Secret Santa 🎅

This is a Secret Santa Web Application. To run the project, make sure you have docker installed, then, just run:

```bash
docker compose up --build
```

If you don't have `Docker`, follow these commands to run the backend:

```bash

# Running the Backend

cd backend
python -m venv .venv
# On Linux / MacOS
. ./.venv/bin/activate
#On Windows
.venv\Scripts\activate

pip install --upgrade pip && pip install -r requirements.txt
fastapi dev
```

To run the frontend, follow these commands:

```bash
cd frontend
npm install -g pnpm
pnpm install
pnpm run dev
```

# Backend API

FastAPI provides an OpenAPI url to understand and test the API on the browser by following this link [http://localhost:8000/docs](http://localhost:8000/docs)



## To do

- Secure the API with api-key authentication
- Add deletion feature
- Configure the application to use PosgreSQL or other database
- Manage Context Auth in the front application

## Sources

The algorithm I used is based on the concept of a "Derangement" or "Hat-check problem" with additional constraints blacklist.

https://binary-machinery.github.io/2021/02/03/secret-santa-graph.html
