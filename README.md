# Filmography - Track and Rate Your Films & TV Shows

A personal film and TV show tracking system that lets you log, rate, and comment on everything you watch.

## ✨ Features

- 📺 **Watch Tracking**: Record films, TV series, and shows you've watched

- ⭐ **Rating System**: Rate content on a customizable scale

- 💭 **Personal Notes**: Add comments and thoughts for each entry

- 📊 **Organized Library**: Keep your entire viewing history in one place

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (or your preferred database)
- pip or uv for package management

### Installation

#### Clone and setup

```bash
git clone https://github.com/wns444/filmography
cd filmography
pip install -r requirements.txt  # or use uv/pipenv/poetry
```

#### Configure environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

#### Database setup

```bash
# Initialize database migrations
alembic upgrade head
```

#### Launch application

```bash
# Development server
uvicorn app.main:app --reload
```

## 📁 Project Structure

## 🌐 API Usage

Once running, access:

- **API Documentation:** http://localhost:8000/docs (Swagger UI)

- **Alternative Docs:** http://localhost:8000/redoc (ReDoc)

## 🆘 Support

- Check existing issues or create a new one

- Ensure your database is running and accessible

- Verify all environment variables are set correctly

---

Enjoy tracking your film journey! 🎬
