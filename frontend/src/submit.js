import { useStore } from "./store";

export const SubmitButton = () => {
  const nodes = useStore((state) => state.nodes);
  const edges = useStore((state) => state.edges);

  const handleSubmit = async () => {
    try {
      const response = await fetch(
        "https://llm-pipeline-builder-production.up.railway.app/pipelines/parse",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            nodes: nodes.map((n) => ({ id: n.id })),
            edges: edges.map((e) => ({
              source: e.source,
              target: e.target,
            })),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const result = await response.json();

      alert(
        `Pipeline Analysis\n\n` +
          `Nodes: ${result.num_nodes}\n` +
          `Edges: ${result.num_edges}\n` +
          `Is DAG: ${result.is_dag ? "Yes ✅" : "No ❌"}`
      );
    } catch (error) {
      console.error(error);
      alert(
        "Failed to submit pipeline.\nPlease check backend deployment and try again."
      );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "12px",
      }}
    >
      <button
        onClick={handleSubmit}
        style={{
          padding: "8px 16px",
          backgroundColor: "#38bdf8",
          border: "none",
          borderRadius: "6px",
          color: "#020617",
          fontWeight: "600",
          cursor: "pointer",
        }}
      >
        Submit
      </button>
    </div>
  );
};
