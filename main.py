"""
Main FastAPI application for Safe Text2SQL Analytics.
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.database import initialize_database
from app.executor import execute_query
from app.llm import generate_sql
from app.models import QueryRequest, QueryResponse
from app.validator import validate_sql


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize resources during application startup.
    """

    initialize_database()

    yield


app = FastAPI(
    title="Safe Text2SQL Analytics",
    description="Secure Natural Language to SQL API for SQLite Analytics.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    """
    Root endpoint.
    """

    return {
        "message": "Safe Text2SQL Analytics API",
        "status": "running",
    }


@app.get("/health")
def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
    }


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(request: QueryRequest):
    """
    Convert natural language into SQL,
    validate it,
    execute safely,
    and return the results.
    """

    start = time.perf_counter()

    sql = generate_sql(request.question)

    if not sql:
        raise HTTPException(
            status_code=400,
            detail="Failed to generate SQL.",
        )

    is_safe, reason = validate_sql(sql)

    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail=reason,
        )

    try:
        rows = execute_query(sql)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    elapsed_ms = round(
        (time.perf_counter() - start) * 1000,
        2,
    )

    return QueryResponse(
        question=request.question,
        sql=sql,
        rows=rows,
        row_count=len(rows),
        execution_time_ms=elapsed_ms,
    )