# Global Message In A Bottle (G-MIB)

A minimalist "Anonymous Public Wall" designed to demonstrate how a decoupled frontend (GitHub Pages) interacts with a high-performance REST API backend (Oracle Cloud / Ubuntu VM).

## Purpose
This project is an open-source educational bridge for migrating an application from "code on a laptop" to a "live app on the internet." It demonstrates:
- Building an asynchronous Python REST API using FastAPI.
- Using SQLite as a lightweight file-based database for simplicity.
- Designing a modern, zero-dependency, minimalist single-page app (HTML/CSS/Vanilla JS).
- Connecting frontend apps directly to self-hosted cloud IP addresses safely over CORS.

## Project Structure
- `app/main.py`: The single-file backend API (Python 3.10+, FastAPI).
- `docs/index.html`: The single-file frontend UI (HTML5, CSS3, ES6 JavaScript).
- `.gitignore`: Common exclusions for the project.

## Local Development (Phase 1)
Follow these setup instructions to verify the application locally before deploying to the cloud.

### 1. Backend Setup
1. **Prepare Python Environment**
   Open your terminal/command prompt at the root of the project:
   ```bash
   python -m venv venv
   ```
   **Activate the virtual environment:**
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate`

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend Server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   You should see output indicating that the backend is running on `http://127.0.0.1:8000`. The SQLite database will automatically initialize (`messages.db`) on the first run.

### 2. Frontend Setup
Because our HTML file connects to the backend over `fetch`, you must open the `docs/index.html` file in a browser.

1. **Open the App**
   Simply log into your file explorer and double-click `docs/index.html` (which opens the file in your browser via `file://` protocol), OR serve it via an HTTP server, e.g.:
   ```bash
   python -m http.server 8080 --directory docs
   ```
   and navigate to `http://127.0.0.1:8080`.

2. **Interact**
   You can monitor the backend logs while you submit messages on the frontend. The screen should immediately refresh and show your new "Message in a Bottle."

## Further Phases (Planned)
- Phase 2: Deploy Frontend on GitHub Pages.
- Phase 3/4: Provision Ubuntu VM in Cloud and set up backend running via `systemd`.
- Phase 5: Complete "The Handshake" by pointing the frontend JS variable `API_URL` to the live Cloud IP.
