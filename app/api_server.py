from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

app = FastAPI()

# Allow frontend (D3.js or React) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Use your index pattern
INDEX_PATTERN = "youtube*"

@app.get("/api/videos")
def get_latest_videos():
    try:
        # Check if any index exists matching the pattern
        indices = es.indices.get_alias(index=INDEX_PATTERN)
        if not indices:
            return {"message": "No youtube* indices found."}

        # Fetch the latest 50 documents
        res = es.search(
            index=INDEX_PATTERN,
            query={"match_all": {}},
            sort=[{"publishedAt": {"order": "desc"}}],
            size=50
        )
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception as e:
        return {"error": str(e)}
