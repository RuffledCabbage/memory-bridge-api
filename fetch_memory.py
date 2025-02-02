import requests

# Your API URL
API_URL = "https://memory-bridge-api.onrender.com/retrieve_memory"

def fetch_memory(keyword=None):
    """Fetches stored memories from the Nexus API and filters them by keyword."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            memories = data.get("memories", [])
            
            if keyword:
                # Filter memories by keyword
                filtered_memories = [
                    memory for memory in memories
                    if keyword.lower() in str(memory).lower()
                ]
                return filtered_memories
            return memories
        else:
            print("Error retrieving memories:", response.text)
            return []
    except Exception as e:
        print("Error:", e)
        return []

if __name__ == "__main__":
    search_keyword = input("Enter a keyword to search for: ")
    results = fetch_memory(search_keyword)
    print("\n🔍 Retrieved Memories:")
    for memory in results:
        print(memory)

