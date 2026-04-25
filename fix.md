# Post-Implementation Fixes - 2026-04-25

During local testing of Phase 1, two primary issues were identified and resolved to ensure the application works correctly.

## 1. Port 8000 "Address Already in Use"
**Issue:**  
The terminal reported an error (or failed to start) because port `8000` was already occupied by a background process from a previous test run. This prevented the new `uvicorn` instance from binding to the port.

**Fix:**  
- Identified the process using `netstat -ano | findstr :8000`.
- Forcefully terminated the lingering process using `taskkill /F /PID <PID>`.
- Verified the port was clear before resuming instructions.

## 2. API Bug: `create_message` Internal Server Error
**Issue:**  
In `app/main.py`, the `create_message` function (handling `POST /messages`) was attempting to convert a database row into a dictionary using `dict(cursor.fetchone())`. However, the SQLite connection was not configured with `row_factory = sqlite3.Row`, meaning `fetchone()` returned a standard Python **tuple**. Passing a tuple to `dict()` without keys causes a `TypeError`.

**Fix:**  
Modified `app/main.py` to include `conn.row_factory = sqlite3.Row` within the `create_message` function:

```python
# Before
with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    # ...

# After (FIXED)
with sqlite3.connect(DB_FILE) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # ...
```

---
**Status:** Both issues are resolved. The backend should now run correctly, and the frontend should be able to post messages without encountering 500 errors.
