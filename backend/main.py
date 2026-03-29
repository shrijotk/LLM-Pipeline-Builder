from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict, deque

app = FastAPI(title="LLM Pipeline Backend")

# -------------------------
# CORS (VERY IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# -------------------------
# Pipeline Parse Endpoint
# -------------------------
@app.post("/pipelines/parse")
async def parse_pipeline(request: Request):
    data = await request.json()

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # Extract node IDs safely
    node_ids = [node.get("id") for node in nodes if "id" in node]

    graph = defaultdict(list)
    indegree = {nid: 0 for nid in node_ids}

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")

        if src in indegree and tgt in indegree:
            graph[src].append(tgt)
            indegree[tgt] += 1

    # Kahn’s Algorithm (DAG check)
    queue = deque([n for n in indegree if indegree[n] == 0])
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    is_dag = visited == len(node_ids)

    return {
        "num_nodes": len(node_ids),
        "num_edges": len(edges),
        "is_dag": is_dag
    }
