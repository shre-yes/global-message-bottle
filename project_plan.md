# Project: The Global Message In A Bottle (G-MIB)
## Framework: 5W1H Comprehensive Deployment Blueprint

### 1. WHO (Participants & Roles)
* **Architect:** Gemini (AI) - Responsible for system design and code generation.
* **Developer/Learner:** The User - Responsible for execution, terminal commands, and cloud console navigation.
* **End User:** Public Internet Users - Can read and post anonymous messages.
* **Target Audience for Learning:** Someone seeking to bridge the gap between "code on my laptop" and "app on the internet."

### 2. WHAT (Technical Specifications)
* **The Application:** A minimalist "Anonymous Public Wall."
* **Frontend:** Single-page application (SPA) using HTML5, CSS3 (modern minimalist), and Vanilla JavaScript (Fetch API).
* **Backend:** FastAPI (Python) - High-performance, asynchronous REST API.
* **Database:** SQLite - A lightweight, file-based SQL engine (no separate server required).
* **Communication:** JSON-based RESTful communication between GitHub Pages and the Cloud VM.
* **Security:** CORS (Cross-Origin Resource Sharing) headers to allow specific cross-domain traffic.

### 3. WHERE (Infrastructure Environment)
* **Source Control:** GitHub Repository (Public/Open Source).
* **Frontend Hosting:** GitHub Pages (`https://<username>.github.io/<repo>/`).
* **Backend Hosting:** Oracle Cloud Infrastructure (OCI) - Always Free Tier (Ubuntu 22.04 LTS VM).
* **Local Dev Environment:** User's local machine (Windows/Mac/Linux) for initial testing.

### 4. WHEN (Project Timeline & Phases)
* **Phase 1: Local Synthesis:** Code the API and Frontend; test locally using `localhost`.
* **Phase 2: Frontend Launch:** Push code to GitHub; activate GitHub Pages.
* **Phase 3: Cloud Provisioning:** Create the VM instance; configure Virtual Cloud Network (VCN) Ingress Rules.
* **Phase 4: Server Hardening & Deployment:** SSH into VM; install Python environment; clone backend; setup `systemd` service.
* **Phase 5: The Handshake:** Update Frontend API URLs to point to the Cloud IP; final verification.

### 5. WHY (The Learning Objectives)
* To understand how a frontend on one domain (GitHub) talks to a backend on another (Cloud IP).
* To master SSH and Linux server management.
* To learn how to keep a web process running 24/7 using `systemd`.
* To understand networking/firewalls (Opening ports on a Cloud Console).

### 6. HOW (Step-by-Step Implementation Details)

#### Phase 1: Local Development
* **Backend File (`app/main.py`):** Use FastAPI to create `GET /messages` and `POST /messages`.
* **Database Schema:** A single table `messages` with columns: `id` (INT), `content` (TEXT), `timestamp` (DATETIME).
* **Frontend File (`docs/index.html`):** A clean UI with a text area, a "Submit" button, and a scrolling message list.

#### Phase 2: GitHub Setup
* Initialize Git repo.
* Place UI files in a `/docs` folder (standard for GitHub Pages).
* Push to main branch.
* Enable GitHub Pages via Settings > Pages > Source: `/docs`.

#### Phase 3: Oracle Cloud / GCP Setup
* **Instance:** 1 OCPU, 1GB RAM (Minimum required).
* **Network:** Open Port `8000` (FastAPI default) in the "Security List" or "Firewall Rules."
* **Access:** Download `private_key.key` for SSH access.

#### Phase 4: Backend Productionization
* Command: `sudo apt update && sudo apt install python3-pip git`.
* Install dependencies: `pip install fastapi uvicorn`.
* **Systemd Service File (`/etc/systemd/system/bottle.service`):**
    ```ini
    [Unit]
    Description=G-MIB Backend
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/project/backend
    ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

#### Phase 5: Integration
* Modify `docs/index.html` JavaScript: 
    * Change `const API_URL = "http://localhost:8000"` to `const API_URL = "http://<YOUR_VM_IP>:8000"`.
* Commit and push changes.