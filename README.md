# DC Inside Scraper API

A simple API that scrapes data from DC Inside galleries using Python, FastAPI, BeautifulSoup, and Requests.

## Features

- Extract posts from DC Inside galleries
- Get gallery information (title, managers, creation date)
- Response caching to minimize requests to the target site
- Proper error handling and retry logic

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload --port 8000`
4. Access the API documentation at http://localhost:8000/docs

## API Endpoints

- `GET /gallery/posts` - Get posts from a specific gallery
- `GET /gallery/info` - Get information about a specific gallery

## Configuration

You can configure the application using environment variables:
- `CACHE_DURATION_MINUTES` - Duration of cache entries in minutes (default: 15) 