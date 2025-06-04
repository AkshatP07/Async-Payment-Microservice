# Async-Payment-Microservice

## 📦 Tech Stack
- **FastAPI** – modern Python web framework  
- **Celery** – distributed task queue  
- **Redis** – in-memory message broker  
- **PostgreSQL** – reliable transaction storage  
- **SQLAlchemy** – ORM  
- **WebSockets (optional)** – real-time payment status *(coming soon)*


✅ Features
- Async payment processing via Celery
- Redis-based job queueing
- Clean architecture with app/api, app/tasks, app/db structure
- Easy to extend for other microservices

This is a production-ready microservice for handling asynchronous UPI-style payments using **FastAPI**, **Redis**, **Celery**, and **PostgreSQL**.
It supports:
- Built a scalable microservice backend for asynchronous UPI-style payments using FastAPI
- Used Celery with Redis for task queuing, handling thousands of concurrent transactions efficiently
- Ensured race-free balance updates via Redis distributed locks and PostgreSQL transactional integrity
- Delivered real-time payment status updates to clients using WebSockets and Redis Pub/Sub (Coming soon)
- Designed with scalability, consistency, and responsiveness as core system guarantees

---

## 🔧 Environment Setup

### 1. Why Use VS Code on Windows with WSL

Running Linux tools (Redis, Celery) directly on Windows is unstable.  
Instead, use **WSL (Windows Subsystem for Linux)** for a full Linux dev environment inside Windows.

#### Steps:
1. Install WSL (Ubuntu recommended)
2. Install [VS Code WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)
3. Open project folder in WSL (in VS Code: `Ctrl+Shift+P` → `Remote-WSL: Open Folder`)

---

### 2. Create Virtual Environment (Recommended)

A virtual environment isolates dependencies per project.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.Make sure Redis is installed in WSL: 

sudo apt update
sudo apt install redis-server
sudo service redis-server start

Verify:
redis-cli ping
Output: PONG

### 4.Running Celery Worker
celery -A app.core.celery_app worker --loglevel=info

### 5.Run FastAPI Server
uvicorn app.main:app --reload


