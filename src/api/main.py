from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
import time
import logging
import os

# ==========================================================
# IMPORT ROUTERS
# ==========================================================

from src.api.routers import (
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    watchlist,
    documents,
    health,
)

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

logger = logging.getLogger(__name__)

# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(title="Nifty100 Financial Intelligence API", version="1.0.0")

# ==========================================================
# DATABASE CONNECTION
# ==========================================================


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# REGISTER ROUTERS
# ==========================================================

app.include_router(companies.router, prefix="/api/v1")

app.include_router(screener.router, prefix="/api/v1")

app.include_router(sectors.router, prefix="/api/v1")

app.include_router(peers.router, prefix="/api/v1")

app.include_router(valuation.router, prefix="/api/v1")

app.include_router(portfolio.router, prefix="/api/v1")

app.include_router(watchlist.router, prefix="/api/v1")

app.include_router(documents.router, prefix="/api/v1")

app.include_router(health.router, prefix="/api/v1")

# ==========================================================
# REQUEST LOGGING MIDDLEWARE
# ==========================================================


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info("%s %s %.3f sec", request.method, request.url.path, duration)

    return response


# ==========================================================
# ROOT ENDPOINT
# ==========================================================


@app.get("/")
def root():

    return {
        "project": "Nifty100 Financial Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
    }
