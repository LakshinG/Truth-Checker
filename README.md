# Research Paper Truth-Checker

A RAG-based system to check for contradictions in research papers using LLMs.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Set up environment variables:
    Copy `.env.example` to `.env` and add your API Keys.
    ```bash
    cp .env.example .env
    ```
    
    You can use either **OpenAI** or **Google Gemini**.
    *   For OpenAI: Set `OPENAI_API_KEY`.
    *   For Google Gemini: Set `GOOGLE_API_KEY`.
    (I had added two called Google and Gemini key, paste your key for both of these)

    The system will automatically detect which key is present. Delete the other

### 1. Generate Dummy Data (Optional)
To create sample research papers for testing:
```bash
python tests/create_dummy_pdf.py
```
This will create `Doe_2023_10.1234.pdf` and `Smith_2024_10.5678.pdf`.

### 2. Run the System
Ingest the PDFs and query the system:

```bash
python main.py --ingest . --query "Does coffee improve performance?"
```

This will:
- Ingest PDFs from the current directory.
- Store them in a local Vector Store (`chroma_db`).
- Perform Hybrid Search (Vector + BM25).
- Use an LLM "Critic Agent" to analyze the retrieved contexts for contradictions.

## Project Structure

- `src/ingestion.py`: Handles PDF loading, semantic chunking, and metadata.
- `src/vector_store.py`: Manages ChromaDB and Hybrid Retrieval.
- `src/critic.py`: Defines the Critic Agent logic.
- `src/evaluation.py`: Setup for RAGAs evaluation metrics.
- `main.py`: Entry point for the application.
- `tests/`: Verification scripts and dummy data generator.

## Evaluation
To run RAGAs evaluation metrics (requires ground truth data setup):
See `src/evaluation.py` and `tests/verify_evaluation.py`.