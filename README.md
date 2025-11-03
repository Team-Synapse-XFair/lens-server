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
cd infralens-backend
```

### 2. Create & activate a virtual environment
```bash
# Windows
python -m venv flask
flask\Scripts\activate

# macOS / Linux
python3 -m venv flask
source flask/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```bash
MONGO_URI='mongodb+srv://<username>:<password>@lens.icyicsk.mongodb.net/?appName=Lens'
MONGO_DB_NAME='lens_dev'
```

## Run Server
```bash
py run.py
```
Server will start at `http://localhost:5000`

---

## Notes

- All API routes are versioned under `/api/v1/`
- Auth-protected routes require valid JWT (frontend handles this)
- MongoDB stores project, user, and report data

## Development Commands
Regenerate requirements.txt after adding new packages:
```bash
pip freeze > requirements.txt
```
