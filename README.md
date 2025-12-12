# jsoned
A full-stack application to visualize and edit entities and their relations defined in JSON Schema.



***

# JSONED — Full Teaching Guide

> **Goal:** Learn how to build and run a full-stack app to **visualize and edit JSON Schema entities** using **FastAPI** (backend) and **React** (frontend). Includes MongoDB integration as an advanced option.

***

## ✅ Quick Start

### 1. Clone the repository

```bash
jsoned> git clone https://github.com/BAMresearch/jsoned.git
jsoned> cd jsoned
jsoned> dir    # Windows
jsoned> ls     # Linux/macOS
```

***

### 2. Backend Setup (Terminal 1)

```bash
jsoned> cd backend
backend> python -m venv venv
backend> source venv/bin/activate    # Windows: venv\Scripts\activate

backend(venv)> pip install -r requirements.txt

backend(venv)> uvicorn main:app --reload
# or specify host/port
backend(venv)> uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### If using `pyproject.toml`:

```bash
# using install -e .
pip install -e .
pip install -e .[dev]  #when dev is defined

# Check which tool is used (Poetry or Pipenv)

# If Poetry:
backend> pip install poetry
backend> poetry install
backend> poetry shell

# If Pipenv:
backend> pip install pipenv
backend> pipenv install
backend> pipenv shell

# If standard PEP 621:
backend> pip install .
```

**Check:** Open `http://127.0.0.1:8000/docs` → FastAPI docs should appear.

***

### 3. Frontend Setup (Terminal 2)

**Create React app:**

```bash
jsoned> npx create-react-app gui
jsoned> cd gui
gui> dir    # Windows
gui> ls     # Linux/macOS
```

**Install Axios for API calls:**

```bash
gui> npm install axios
gui> npm audit      #Run audit details
gui> npm audit fix  #Fix automatically

```

**Run frontend:**

```bash
gui> npm start   # Standard start command

#OR
gui> npm run dev # Alias for developer mode

INFO:To npm run dev DO THE FOLLOWING:
    in package.json add ->> "dev": "react-scripts start":

            "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject",
            "dev": "react-scripts start"
            }

```

✔ **Difference?**

*   `npm start` → Runs the default development server.
*   `npm run dev` → Custom alias (same behavior here).

📂 **Where are App.js and App.css?**

*   Located in `gui/src/`:
    *   `App.js` → Main React component
    *   `App.css` → Styling for App.js

✅ **Check:**

*   `http://localhost:3000`

***

## ✅ Architecture & Diagrams

### **High-Level Architecture**

    +-------------------+        HTTP API        +-------------------+        MongoDB
    |   React Frontend  | <--------------------> |     FastAPI       | <----> | Database |
    |  (Components/UI)  |                       |  (Routes/Models)  |        | Schemas  |
    +-------------------+                       +-------------------+        +----------+

***

### **Detailed Component Flow**

    [User Action] --> [React Component] --> [Axios API Call] --> [FastAPI Endpoint]
           |                                                      |
           |                                                      v
           |                                              [MongoDB Query]
           |                                                      |
           v                                                      v
    [Updated State] <-- [JSON Response] <-- [FastAPI Response] <-- [Database Result]

***

### **Backend Layer Diagram**

    +-------------------+
    |   main.py         |  -> Routes & Controllers
    +-------------------+
    |   models.py       |  -> Pydantic Schemas
    +-------------------+
    |   database.py     |  -> MongoDB Connection
    +-------------------+

***

### **Frontend Folder Structure**

    gui/
    ├── public/
    ├── src/
    │   ├── App.js        # Main React Component
    │   ├── api.js        # Axios API Calls
    │   ├── components/   # UI Components
    │   └── App.css       # Styling

***

### **Request Lifecycle**

    User Click -> React -> Axios -> FastAPI -> MongoDB -> Response -> React State Update

***

### **MVC Mapping**

    Model      -> Pydantic schemas (datamodel.py, model.py)
    View       -> React components (App.jsx)
    Controller -> FastAPI routes (main.py)

***

### **Sequence Flow (Add Version)**

    User -> React -> FastAPI -> In-memory DB
     |       |        |           |
     | Click Add      |           |
     |---------------> |           |
     |             POST /version   |
     |                           -> Append SchemaDefinition

***

### **UML Class Diagram**

    +-------------------------+
    |   SchemaDefinition      |
    +-------------------------+
    | id: str                |
    | name: str              |
    | version: str           |
    | content: dict          |
    | updated_at: datetime   |
    +-------------------------+

    +-------------------------+
    |     UpdateSchema        |
    +-------------------------+
    | name: str | None       |
    | version: str | None    |
    +-------------------------+

***

### **MongoDB Integration Flow**

    +-----------+        Axios HTTP        +-----------+        PyMongo        +-----------+
    |  React    |  --->  POST /version  -> |  FastAPI  |  --->  Insert Doc  -> | MongoDB   |
    | Frontend  |        GET /version      | Backend   |        Query Docs     | Database  |
    +-----------+        PATCH /version    +-----------+        Return JSON    +-----------+

***

## ✅ MongoDB Atlas Setup (Optional Advanced)

1.  Create account at <https://www.mongodb.com/atlas>
2.  Create cluster and get connection string
3.  Add `.env` in `backend`:

<!---->

    MONGO_URI="your-atlas-uri"

4.  Use `pymongo` in `database.py`:

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client.jsoned_db
```

***

## ✅ API Endpoints

    GET    /version
    POST   /version
    PUT    /version/{id}
    PATCH  /version/{id}
    DELETE /version/{id}

***

## ✅ Best Practices

*   Use `.env` for secrets
*   Enable CORS for frontend
*   Keep code modular

***

## ✅ Troubleshooting

*   **CORS errors**: Add `CORSMiddleware`
*   **npm issues**: Delete `node_modules` → `npm install`
*   **Port conflicts**: Change port in `uvicorn` or `npm run dev`

***



## ✅ Resources

*   <https://fastapi.tiangolo.com/>
*   <https://docs.pydantic.dev/>
*   <https://react.dev/>
*   <https://www.mongodb.com/docs/>

***
