# A-MEM Quickstart (English)

## 1) Setup
- Python 3.9+ recommended.
- Create venv: `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`).
- Install package (from repo root): `pip install .` or for development `pip install -e .`.
- If NLTK data is missing (e.g., `punkt`), run: `python -m nltk.downloader punkt`.

## 2) Choose LLM Backend
- **Ollama (local, default in example):**
  - Install and start Ollama.
  - Pull model: `ollama pull llama3`.
  - No API key needed.
- **OpenAI (remote):**
  - Set env `OPENAI_API_KEY`.
  - Use `llm_backend="openai"` and a model you have access to (e.g., `gpt-4o-mini`).

## 3) Quick Run with Provided Example (Ollama)
From repo root (venv activated):
```bash
python examples/sovereign_memory.py
```
Expected console flow:
- Initializes the Agentic Memory system.
- Adds one memory (prints stored ID).
- Searches and prints the stored content, tags, and generated context.

## 4) Quick Run Using OpenAI Instead
Create a small script or REPL session:
```python
from agentic_memory.memory_system import AgenticMemorySystem

mem = AgenticMemorySystem(
    model_name="all-MiniLM-L6-v2",
    llm_backend="openai",
    llm_model="gpt-4o-mini",  # or another available model
)

mid = mem.add_note(
    "The user values data sovereignty and local processing above all else.",
    tags=["sovereign", "privacy"],
    category="Principles",
)
print(mem.search_agentic("sovereignty", k=1))
```
Run with your key set: `OPENAI_API_KEY=... python your_script.py`.

## 5) Notes on Storage
- Default Chroma client is in-memory; the example resets the `memories` collection on init.
- No extra database service is required for the quickstart.
- For persistence, switch to `PersistentChromaRetriever` in code (not needed for the basic run).
