import os
import sys

# Ensure we can import from source
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentic_memory.memory_system import AgenticMemorySystem

def main():
    # Load environment variables from .env if present (recommended for local development)
    # This avoids requiring users to `source .env` manually.
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    print("🧠 Initializing A-mem Sovereign System...")

    # Prefer OpenAI if OPENAI_API_KEY is set; otherwise fall back to Ollama
    backend = os.getenv("LLM_BACKEND") or ("openai" if os.getenv("OPENAI_API_KEY") else "ollama")
    llm_model = os.getenv("LLM_MODEL") or ("gpt-4o-mini" if backend == "openai" else "llama3")
    api_key = os.getenv("OPENAI_API_KEY") if backend == "openai" else None

    if backend == "openai" and not api_key:
        print("❌ OPENAI_API_KEY not set. Export it and retry, or set LLM_BACKEND=ollama.")
        return

    try:
        memory_system = AgenticMemorySystem(
            model_name='all-MiniLM-L6-v2',  # Local embeddings (via sentence-transformers)
            llm_backend=backend,
            llm_model=llm_model,
            api_key=api_key
        )
        print(f"✅ System initialized (backend={backend}, model={llm_model}).")
    except Exception as e:
        print(f"❌ Init failed: {e}")
        return

    # Add a memory
    print("\n📝 Adding Sovereign Memory...")
    content = "The user values data sovereignty and local processing above all else."
    try:
        # Note: A-mem automatically generates tags/context via LLM here
        memory_id = memory_system.add_note(
            content=content,
            tags=["sovereign", "privacy"],
            category="Principles"
        )
        print(f"   Memory stored with ID: {memory_id}")
    except Exception as e:
        print(f"❌ Failed to store memory: {e}")
        return

    # Retrieve
    print("\n🔍 Retrieving Memory...")
    try:
        results = memory_system.search_agentic("sovereignty", k=1)
        for res in results:
            print(f"   Found: {res['content']}")
            print(f"   Tags: {res['tags']}")
            print(f"   Context (LLM Generated): {res.get('context', 'N/A')}")
    except Exception as e:
        print(f"❌ Retrieval failed: {e}")

if __name__ == "__main__":
    main()
