# API Documentation

## Overview

The Nifty100 Financial Intelligence Platform exposes REST APIs using FastAPI.

**Base URL**

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Available Endpoints

## 1. Health Check

**Endpoint**

```
GET /api/v1/health
```

**Description**

Checks whether the API service is running.

**Response**

```json
{
    "status": "ok"
}
```

---

## 2. Companies

**Endpoint**

```
GET /api/v1/companies
```

**Description**

Returns the list of companies available in the database.

---

## 3. Company Details

**Endpoint**

```
GET /api/v1/companies/{company_id}
```

**Description**

Returns detailed information for a specific company.

---

## 4. Screener

**Endpoint**

```
GET /api/v1/screener
```

**Description**

Returns companies matching screening filters.

---

## 5. Sectors

**Endpoint**

```
GET /api/v1/sectors
```

**Description**

Returns sector-wise company information.

---

# Status Codes

| Code | Meaning |
|------|---------|
| 200 | Request successful |
| 400 | Bad request |
| 404 | Resource not found |
| 500 | Internal server error |

---

# Testing the API

Start the server:

```bash
uvicorn src.api.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Use the interactive interface to test each endpoint.