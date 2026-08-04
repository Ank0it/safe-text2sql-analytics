import os

import google.generativeai as genai
from dotenv import load_dotenv

from app.database import get_schema

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def build_prompt(question: str) -> str:
    """
    Builds a schema-aware prompt for Text2SQL generation.
    """

    schema = get_schema()

    schema_description = ""

    for table, columns in schema.items():
        schema_description += f"\nTable: {table}\n"
        schema_description += "Columns:\n"

        for column in columns:
            schema_description += f"- {column}\n"

    prompt = f"""
You are an expert SQLite SQL generator.

Your task is to convert a natural language analytics question into SQL.

Database Schema:

{schema_description}

Rules:

1. Generate ONLY valid SQLite SQL.
2. ONLY generate SELECT queries.
3. Never generate:
   - INSERT
   - UPDATE
   - DELETE
   - DROP
   - ALTER
   - CREATE
   - TRUNCATE
4. Use ONLY tables and columns provided in the schema.
5. Do NOT invent table names.
6. Do NOT invent column names.
7. Return ONLY SQL.
8. Do NOT include markdown.
9. Do NOT explain your answer.

User Question:

{question}
"""

    return prompt


def generate_sql(question: str) -> str:
    """
    Generates SQL from a natural language question.
    """

    prompt = build_prompt(question)

    response = model.generate_content(prompt)

    sql = response.text.strip()

    # Remove markdown if the model returns it
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql