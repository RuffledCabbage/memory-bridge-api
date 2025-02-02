from fastapi import FastAPI, Query
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase Credentials (Securely Fetch from Environment Variables)
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Ensure this is set in your environment

if not SUPABASE_KEY:
    raise ValueError("Supabase API key is missing. Set SUPABASE_SERVICE_KEY as an environment variable.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/search_memory/")
def search_memory(query: str = Query(None, title="Memory Search Query")):
    """Searches memories based on a keyword."""
    try:
        # If no query is provided, return all memories
        if not query:
            response = supabase.table("unified_labyrinth_nexus").select("*").execute()
        else:
            # Create an empty list to store matching results
            combined_results = []
            
            # List of fields to search
            search_fields = [
                "core_memory->>CoreMemories",
                "philosophical_reflections->>Philosophy",
                "reflections_and_lessons->>PastConversations",
                "expanded_threads->>ExpandedThreads",
                "meta_reflections->>MetaReflections",
                "historical_threads->>HistoricalThreads",
                "quiet_truths->>QuietTruths"
            ]
            
            # Iterate over fields and search each one
            for field in search_fields:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter(field, "ilike", f"%{query}%").execute()
                if response.data:
                    combined_results.extend(response.data)  # Append results instead of overwriting

        return {"status": "success", "retrieved_memories": combined_results}

    except Exception as e:
        return {"status": "error", "message": str(e)}

