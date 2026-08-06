# API Examples

## Health

GET

```
/health
```

Response

```json
{
  "status":"healthy",
  "database":"connected",
  "llm":"configured"
}
```

---

## Generate SQL

POST

```
/query
```

Body

```json
{
  "question":"Show all customers."
}
```

Response

```json
{
  "question":"Show all customers.",
  "generated_sql":"SELECT * FROM customers;",
  "validation":{
      "safe":true,
      "reason":"Passed validation."
  },
  "result_table":[...],
  "explanation":"Retrieved all customers.",
  "confidence":{
      "level":"High",
      "score":0.96,
      "notes":[]
  }
}
```