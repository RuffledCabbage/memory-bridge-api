from fastapi import FastAPI, Query
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase Credentials from Environment Variables
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Ensure this is set in Render

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/search_memory/")
def search_memory(query: str = Query(None, title="Memory Search Query")):
    """Searches memories based on a keyword."""
    try:
        if not query:
            response = supabase.table("unified_labyrinth_nexus").select("*").execute()
        else:
            query_lower = f"%{query.lower()}%"  # Case-insensitive search pattern

            # Apply filter on multiple JSONB fields using `ilike` in Supabase
            response = supabase.table("unified_labyrinth_nexus").select("*").or_(
                f"core_memory->>CoreMemories.ilike.{query_lower},"
                f"philosophical_reflections->>Philosophy.ilike.{query_lower},"
                f"reflections_and_lessons->>PastConversations.ilike.{query_lower},"
                f"expanded_threads->>ExpandedThreads.ilike.{query_lower},"
                f"meta_reflections->>MetaReflections.ilike.{query_lower},"
                f"historical_threads->>HistoricalThreads.ilike.{query_lower},"
                f"quiet_truths->>QuietTruths.ilike.{query_lower}"
            ).execute()

        memories = response.data

        return {"status": "success", "retrieved_memories": memories}

    except Exception as e:
        return {"status": "error", "message": str(e)}
