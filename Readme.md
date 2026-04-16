# Athena — AI-Powered Knowledge Blog Engine

Athena is a full-stack AI-driven technical blogging platform designed to automatically generate, store, search, and explain technical knowledge.

It combines LLMs, vector search, full-text search, and structured databases into a single production-style system.

At the core of Athena is **Pythia**, a context-aware AI assistant that answers questions about each blog using semantic understanding.

---

# Features

## AI Blog Generation

* Automatically generates technical blogs using Groq LLM
* Structured Markdown formatting
* Includes sections, explanations, and examples
* Supports automated daily blog publishing

---

## Smart Search (Elasticsearch)

* Full-text search across blog titles and content
* Fast and scalable retrieval
* Ranked search results

---

## Semantic Understanding (ChromaDB)

* Vector embeddings for each blog
* Context-aware retrieval
* Enables intelligent AI responses

---

## Pythia — Context-Aware Chatbot

Users can ask questions directly about a blog.

Pythia:

* Reads blog context
* Finds relevant chunks
* Generates precise answers
* Understands technical content

---

## Blog Images

Each blog includes:

* Topic-relevant dynamic images
* Visual preview cards
* Improved reading experience

---

## Automated Blog Scheduler

Blogs are generated automatically:

* Runs every 24 hours
* Picks technical topic
* Generates full article
* Stores and indexes automatically

---

## Admin Utilities

Includes developer tools such as:

DELETE /admin/delete-all

Used to:

* Reset database
* Clear search index
* Remove vector embeddings

---

# System Architecture

Frontend (React + TypeScript)
↓
FastAPI Backend
↓
-

PostgreSQL    -> Blog Storage
Elasticsearch -> Search Engine
ChromaDB      -> Vector Database
--------------------------------

```
    ↓  
```

Groq LLM API
↓
AI Blog Generation + Chat

---

# Application Flow

## Blog Generation Flow

Scheduler runs
↓
Select topic
↓
Generate blog via Groq
↓
Store in PostgreSQL
↓
Index into Elasticsearch
↓
Embed into ChromaDB
↓
Available in UI

---

## Blog Reading Flow

User opens Library
↓
Blog cards displayed
↓
User opens Blog
↓
Blog content loads
↓
Pythia chat available
↓
User asks question
↓
Context retrieved
↓
Answer generated

---

## Search Flow

User types in search bar
↓
Backend receives query
↓
Elasticsearch searches blogs
↓
Matching results returned

---

# Tech Stack

## Backend

* FastAPI
* PostgreSQL
* Elasticsearch
* ChromaDB
* Groq API
* SQLAlchemy
* APScheduler

---

## Frontend

* React
* TypeScript
* Tailwind CSS
* Framer Motion
* TanStack Query

---

## Infrastructure

* Docker
* Docker Compose

---

# Project Structure

Athena/

backend/
app/
routes/
services/
models/
schemas/
elastic/

vector/
workers/
Dockerfile
docker-compose.yml

frontend/
src/
pages/
components/
lib/
services/

README.md
.gitignore

---

# Getting Started

## Prerequisites

Install:

* Docker
* Docker Compose
* Node.js
* Git

---

## Clone Repository

git clone https://github.com/YOUR_USERNAME/Athena-AI-Blog-System.git
cd Athena-AI-Blog-System

---

## Start Backend Services

docker compose up -d

This starts:

* PostgreSQL
* Elasticsearch
* ChromaDB
* FastAPI

---

## Run Frontend

cd frontend
npm install
npm run dev

---

## Access Application

Frontend:

http://localhost:5173

Backend API Documentation:

http://localhost:8000/docs

---

# API Endpoints

## Blog

GET /blogs
GET /blogs/{id}
POST /generate-blog

---

## Search

GET /search?q=keyword

---

## Chat (Pythia)

POST /chat

Example request:

{
"question": "Explain this article",
"blog_id": "123"
}

---

## Admin

DELETE /admin/delete-all

---

# AI Capabilities

Athena integrates multiple AI-powered workflows:

* Blog generation using LLM
* Semantic vector retrieval
* Context-aware Q&A
* Technical content structuring
* Automated knowledge publishing

---

# Future Enhancements

* User authentication
* Bookmark system
* AI summarization
* Multi-language support
* Blog rating system

---

# Author

Built by:

Naman Sharma

Full-stack developer focused on scalable AI-powered systems, backend architecture, and distributed services.
