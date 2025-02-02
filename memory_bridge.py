from fastapi import FastAPI, Query
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase Credentials (Use Environment Variables Instead of Hardcoding)
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZhbnh0aXhtc3h0ZWh3c2R6dGF2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODI2OTA5MCwiZXhwIjoyMDUzODQ1MDkwfQ.Y7Y-EBrvNuiKYtbBiQqMmWzFjjdF4RIvfb0WrNL4CN4")  # Securely fetch from environment variables

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/search_memory/")
def search_memory(query: str = Query(None, title="Memory Search Query")):
    """Searches memories based on a keyword."""
    try:
        # If no query is provided, return all memories
        if not query:
            response = supabase.table("unified_labyrinth_nexus").select("*").execute()
        else:
            # Apply filters to all nested JSON fields using `filter()` instead of `.or_()`
            response = supabase.table("unified_labyrinth_nexus").select("*").filter("core_memory->CoreMemories", "ilike", f"%{query}%").execute()
            
            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("philosophical_reflections->Philosophy", "ilike", f"%{query}%").execute()
            
            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("reflections_and_lessons->PastConversations", "ilike", f"%{query}%").execute()

            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("expanded_threads->ExpandedThreads", "ilike", f"%{query}%").execute()

            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("meta_reflections->MetaReflections", "ilike", f"%{query}%").execute()

            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("historical_threads->HistoricalThreads", "ilike", f"%{query}%").execute()

            if not response.data:
                response = supabase.table("unified_labyrinth_nexus").select("*").filter("quiet_truths->QuietTruths", "ilike", f"%{query}%").execute()

        memories = response.data

        return {"status": "success", "retrieved_memories": memories}

    except Exception as e:
        return {"status": "error", "message": str(e)}
