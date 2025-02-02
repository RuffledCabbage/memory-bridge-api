from fastapi import FastAPI, Query
from supabase import create_client, Client

app = FastAPI()

# Supabase Credentials
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZhbnh0aXhtc3h0ZWh3c2R6dGF2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODI2OTA5MCwiZXhwIjoyMDUzODQ1MDkwfQ.Y7Y-EBrvNuiKYtbBiQqMmWzFjjdF4RIvfb0WrNL4CN4"  # Replace this with your actual key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/search_memory/")
def search_memory(query: str = Query(None, title="Memory Search Query")):
    """Searches memories based on a keyword."""
    try:
        # If no query is provided, return all memories
        if not query:
            response = supabase.table("unified_labyrinth_nexus").select("*").execute()
        else:
            # Search directly in Supabase using `ilike` for case-insensitive filtering
            response = (
                supabase.table("unified_labyrinth_nexus")
                .select("*")
                .ilike("memory_content", f"%{query}%")  # Replace "memory_content" with the actual column name
                .execute()
            )

        memories = response.data

        return {"status": "success", "retrieved_memories": memories}

    except Exception as e:
        return {"status": "error", "message": str(e)}

