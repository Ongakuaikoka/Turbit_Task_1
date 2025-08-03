FastAPI + MongoDB Data Pipeline

A simple containerized pipeline that pulls post and comment data from the [JSONPlaceholder API](https://jsonplaceholder.typicode.com/), stores it in MongoDB, and exposes it via a FastAPI app.

What It Does

- MongoDB runs in Docker
- Python script fetches and loads data into MongoDB
- FastAPI app exposes:
  - `/users/posts_count` — total posts per user
  - `/posts/{post_id}/comments` — comments for a specific post
---

Quick Start

1. Clone the Repo
  `git clone https://github.com/Ongakuaikoka/Turbit_Task_1.git`
  `cd Turbit_Task_1`

2. Start MongoDB and FastAPI
  `docker-compose up --build`

3. Load Data into MongoDB
  `docker exec -it fastapi_app python load_data.py`

**API Endpoints**
  GET /users/posts_count
  _Total number of posts per user_

  GET /posts/{post_id}/comments
  _Comments for a specific post_

  Docs available at:
  http://localhost:8000/docs
