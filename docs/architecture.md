# Safe Text2SQL Analytics Architecture

## Overview

The application converts natural language into safe SQL queries.

```
User
   │
   ▼
FastAPI
   │
   ▼
Gemini LLM
   │
Generated SQL
   │
   ▼
SQL Validator
   │
Safe?
 ┌──┴─────────┐
 │            │
No           Yes
 │            │
Reject     SQLite
 │            │
 ▼            ▼
Error      Results
```

---

## Components

### app/main.py

FastAPI endpoints.

---

### app/llm.py

Responsible for

- prompt construction
- Gemini API
- SQL generation

---

### app/validator.py

Prevents

- DELETE
- DROP
- UPDATE
- INSERT
- ALTER
- CREATE
- TRUNCATE
- GRANT
- REVOKE

---

### app/database.py

Executes validated SELECT queries.

---

### benchmark/

Measures

- Intent Accuracy
- Unsafe Query Block Rate
- Pass/Fail Rate

---

### tests/

Unit tests for

- validator
- api
- database