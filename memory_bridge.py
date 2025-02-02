from fastapi import FastAPI, Query
from supabase import create_client, Client

app = FastAPI()

# Supabase Credentials
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"  # Replace this with your actual key

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

