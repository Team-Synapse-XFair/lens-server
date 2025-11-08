# Lens Backend

## Tech Stack

- **Backend:** Python (Flask)
- **Database:** MongoDB
- **Environment:** Virtual environment (`flask/`)
- **Dependencies:** Flask, PyMongo, Python-dotenv, Bson

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Team-Synapse-XFair/lens-server.git
cd lens-server
```

### 2. Create & activate a virtual environment and install dependencies
- Run `SetupServer.bat`

### 3. Set up environment variables
Create a `.env` file in the root directory:
```bash
MONGO_URI='mongodb+srv://<username>:<password>@lens.icyicsk.mongodb.net/?appName=Lens'
MONGO_DB_NAME='lens_dev'
```

## Run Server
- Run `RunServer.bat`
> Server will start at http://localhost:5000

---

## Notes

- All API routes are versioned under `/api/v1/`
- Auth-protected routes require valid JWT (frontend handles this)
- MongoDB stores project, user, and report data
