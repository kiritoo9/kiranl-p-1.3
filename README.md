## (kiranl-p-1.3) NL2SQL Engine: Processing Pipeline
This document outlines the core steps of the Natural Language to SQL (NL2SQL) engine, which transforms a user's natural language request into a structured context for SQL query generation.

## Key Model
- sentence-transformers/all-MiniLM-L6-v2 (vectorization: dimension=368)
- models/gemini-2.0-flash-lite (Gemini)
- llama-3.3-70b-versatile (Groq)

## Embedding and Vector Representation
This initial phase converts all textual components—the database structure and the user's prompt—into numerical vectors (embeddings) for machine processing.

1. Schema Embedding
    - Load or generate embeddings for the database schema.
    - The schema (table names, column names, etc.) is vectorized to capture semantic meaning. Embeddings are persisted in a .npy format.
2. Vocabulary Creation
    - Create and save a word dictionary (vocabulary) from the corpus.
    - This dictionary maps unique words to specific indices for consistent embedding generation. Stored in .pkl format.
3. Prompt Tokenization & Embedding
    - Generate embeddings for the user's input prompt during the application runtime.
    - The prompt is tokenized using the established vocabulary and converted into vectors.

## Prompt Serialization and Preprocessing
The user's raw input is cleaned, normalized, and structured to ensure consistent processing and improve the accuracy of subsequent steps.

1. Normalization
    - Convert the prompt to lowercase and remove unnecessary characters (e.g., \n, \t, special symbols).
2. Typo Correction
    - Identify and correct potential typos in the prompt using a distance metric.
    - Implementation Detail: Utilizes Levenshtein Distance.
4. Context Window Segmentation
    - Segment the processed prompt into overlapping two-word phrases.
    - Example: ["word1 word2", "word2 word3", ...]

## Context Pruning and Intent Detection
This phase focuses on identifying the core meaning, required data elements, and overall intent of the user's query.

1. Key Point Detection
    - Identify and classify critical entities that define the query's scope.
        - Report Type: Desired output format (table, bar, pie, line).
    - Implementation Detail: Uses Euclidean Distance on embeddings to find semantically related items.
        - Table Name: The specific database table required.
2. Key Point Classification
    - Column Predictions: Columns needed for selection, filtering, or aggregation.
    - Sub-classification: Single Value (aggregate result) vs. Multiple Values (comparative chart data).
3.  No-Context Handling
    - Implement a fallback mechanism for low-confidence or ambiguous queries.
    - If no context is detected, return a suggestion list of relevant tables or predefined queries based on keywords.
        - Example JSON:
         ```json
        {
            "greeting_words": "Sorry, we can't find exactly what you're looking for. Perhaps there was a misspelling or typo. Here are some recommendations based on your input:",
            "list_of_suggestions": [
                {
                    "suggestion_id": 1,
                    "description": "Sales by Region Table"
                },
                {
                    "suggestion_id": 2,
                    "description": "Monthly Revenue Chart"
                }
            ]
        }
        ```

## Retrieval-Augmented Generation (RAG) and SQL Formulation
The final phase uses a Large Language Model (LLM) to validate the pruned context and transform the user's natural language into structured elements for SQL generation.

1. Reasoning Process (Context Re-Validation)
    - The LLM is prompted to re-validate the detected key points against the full database schema for logical consistency.
        ```json
        {
            "multiple_value": true|false,
            "column_prediction": [...], 
            "actual_table_schema": [{...}], 
            "user_prompt": ... 
        }
        ```
2. Generating Value and Conditions
    - The refined context is sent to the LLM to extract specific values and filtering conditions (WHERE clauses) from the user's prompt.
        - LLM Input Format (Pruned Context):
            ```json
            { 
                "table_name": ..., 
                "column_select": [...], 
                "table_schema": [{...}], 
                "user_prompt": ... 
            }
            ```
    - The LLM returns a structured JSON object containing the extracted conditions ready for SQL query construction.
        - LLM Expected Output (Structured Conditions):
            ```json
            {
                "greeting_words": "...",
                "conditions_with_value": [
                    {"column_name": "value"}
                ],
                "closing_words": "..."
            }
            ```

## Installation
```bash
virtualenv -p python3.11 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```

## Python version
3.11

## App version
kiranl-p-1.3