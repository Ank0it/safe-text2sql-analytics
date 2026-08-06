import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

from app.database import get_relationships, get_schema

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash") # or "gemini-2.5" for the standard model


def build_prompt(question: str) -> str:
    """
    Build a schema-aware prompt for Text2SQL generation.
    """

    schema = get_schema()
    relationships = get_relationships()

    schema_text = ""

    for table, columns in schema.items():
        schema_text += f"\nTable: {table}\n"

        for column in columns:
            schema_text += f"  - {column}\n"

    relationship_text = ""

    if relationships:
        for relation in relationships:
            relationship_text += f"  - {relation}\n"
    else:
        relationship_text = "  No foreign-key relationships found.\n"

    prompt = f"""
You are an expert SQLite SQL generator.

Your task is to convert a natural-language analytics question into ONE valid SQLite SELECT query.

========================
DATABASE SCHEMA
========================

{schema_text}

========================
DATABASE RELATIONSHIPS
========================

{relationship_text}

========================
STRICT RULES
========================

1. Return ONLY SQL.

2. Return exactly ONE SQL statement.

3. The query MUST be a SELECT statement.

4. You may use:
   - JOIN
   - LEFT JOIN
   - GROUP BY
   - ORDER BY
   - HAVING
   - LIMIT
   - Aggregate functions
   - DISTINCT
   - WITH (CTEs)

5. NEVER generate:
   INSERT
   UPDATE
   DELETE
   DROP
   ALTER
   CREATE
   TRUNCATE
   PRAGMA
   REPLACE

6. NEVER invent tables.

7. NEVER invent columns.

8. Use the provided relationships whenever joins are required.

9. Do NOT use Markdown.

10. Do NOT explain your answer.

11. Do NOT include comments.

========================
USER QUESTION
========================

{question}
"""

    return prompt.strip()


def clean_sql(response_text: str) -> str:
    """
    Cleans Gemini output and extracts only SQL.
    """

    if not response_text:
        return ""

    sql = response_text.strip()

    # Remove Markdown fences
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    prefixes = [
        "SQL:",
        "Query:",
        "Generated SQL:",
        "Here is the SQL:",
        "Here is your SQL:",
    ]

    for prefix in prefixes:
        if sql.lower().startswith(prefix.lower()):
            sql = sql[len(prefix):].strip()

    # Keep only the first SQL statement ending with ;
    match = re.search(
        r"(SELECT|WITH).*?;",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(0).strip()

    # Fallback if semicolon is missing
    match = re.search(
        r"(SELECT|WITH).*",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(0).strip()

    return ""


def generate_sql(question: str) -> str:
    """
    Generate SQL from a natural-language analytics question.
    """

    prompt = build_prompt(question)

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0,
                "top_p": 1,
                "top_k": 1,
            },
        )

    except Exception as e:
        print("\n" + "=" * 80)
        print("GEMINI ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(e)
        print("=" * 80 + "\n")
        return ""

    if response is None:
        return ""

    text = getattr(response, "text", "")

    return clean_sql(text)