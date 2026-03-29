# DevTrack — Engineering Issue Tracker

A minimal backend API for tracking engineering issues. Engineers can report bugs, assign priorities, and track status.

---

## How to Run the Project

1. Clone the repository
```bash
git clone <your-repo-url>
cd devtrack_assignment
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirement.txt
```

4. Run the server
```bash
python manage.py runserver
```

---

## Endpoints

### Reporter Endpoints

| Method | URL | Description |
|---|---|---|
| POST | `/api/reporters/` | Create a new reporter |
| GET | `/api/reporters/` | Get all reporters |
| GET | `/api/reporters/?id=1` | Get a single reporter by ID |

### Issue Endpoints

| Method | URL | Description |
|---|---|---|
| POST | `/api/issues/` | Create a new issue |
| GET | `/api/issues/` | Get all issues |
| GET | `/api/issues/?id=1` | Get a single issue by ID |
| GET | `/api/issues/?status=open` | Get all issues filtered by status |

---

## Design Decision

### Router functions over separate URLs

Instead of mapping each function to a separate URL, I combined related endpoints into two router functions — `reporters()` and `issues()`. This means `/api/reporters/` handles both POST and GET requests in one place, routing to the correct function based on the HTTP method and query params.

This keeps the URL structure clean and RESTful, and makes it easy to extend later — for example adding a PATCH or DELETE without changing the URL.

---

## Data Storage

Data is stored in two JSON files:
- `reporters.json` — stores all reporters
- `issues.json` — stores all issues

---

## OOP Design

- `BaseEntity` — abstract base class with `validate()` and `to_dict()`
- `Reporter` — inherits from `BaseEntity`
- `Issue` — inherits from `BaseEntity` with a `describe()` method
- `CriticalIssue` — overrides `describe()` with urgent message
- `LowPriorityIssue` — overrides `describe()` with low priority message