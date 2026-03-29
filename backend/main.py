from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict, deque

app = FastAPI(title="VectorShift Backend API")

# ✅ CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Models
# -------------------------
class Node(BaseModel):
    id: str

class Edge(BaseModel):
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# -------------------------
# Pipeline Endpoint
# -------------------------
@app.post("/pipelines/parse")
def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)

    graph: Dict[str, List[str]] = defaultdict(list)
    indegree: Dict[str, int] = defaultdict(int)

    for node in pipeline.nodes:
        indegree[node.id] = 0

    for edge in pipeline.edges:
        graph[edge.source].append(edge.target)
        indegree[edge.target] += 1

    # Kahn's Algorithm
    queue = deque([n for n in indegree if indegree[n] == 0])
    visited = 0

    while queue:
        current = queue.popleft()
        visited += 1

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    is_dag = visited == num_nodes

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
