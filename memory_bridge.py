from fastapi import FastAPI, Query
from supabase import create_client, Client

app = FastAPI()

# Supabase Credentials
SUPABASE_URL = "https://fanxtixmsxtehwsdztav.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZhbnh0aXhtc3h0ZWh3c2R6dGF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgyNjkwOTAsImV4cCI6MjA1Mzg0NTA5MH0.4RW8iLQ_tHCoCQ9zq6HZK0x9U4a_NniAdhInwGzB94Q"  # Replace this with your actual key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/search_memory/")
def search_memory(query: str = Query(None, title="Memory Search Query")):
    """API Endpoint to search memories based on a query."""
    try:
        response = supabase.table("unified_labyrinth_nexus").select("*").execute()
        memories = response.data

        if query:
            query_lower = query.lower()
            filtered_memories = [
                memory for memory in memories
                if query_lower in str(memory).lower()
            ]
            return {"status": "success", "retrieved_memories": filtered_memories}

        return {"status": "success", "retrieved_memories": memories}
    except Exception as e:
        return {"status": "error", "message": str(e)}

