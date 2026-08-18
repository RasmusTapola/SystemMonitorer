import { useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = "http://localhost:8000"

function App() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedAgentId, setSelectedAgentId] = useState(null);
const [latestMetrics, setLatestMetrics] = useState(null);

  useEffect(() => {
    async function fetchAgents() {
      try {
        const response = await fetch(`${API_BASE_URL}/agents`);

        if (!response.ok) {
          throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();
        console.log("Agents from API:", data);
        setAgents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchAgents();
  }, []);

  useEffect(() => {
    console.log("selected agent:", selectedAgentId);
    if (!selectedAgentId) return;

    async function fetchLatestMetrics() {
      const response = await fetch(
        `${API_BASE_URL}/agents/${selectedAgentId}/latest`
      );

      if (!response.ok) {
        throw new Error("request failed: ${response.status}")
      }

      const data = await response.json();
      setLatestMetrics(data);
    }

    fetchLatestMetrics();
  }, [selectedAgentId]);

  if (loading) {
    return <p>Loading agents...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
     <main>
      <h1>System Monitor</h1>

      <ul>
        {agents.map((agent) => (
          <li key={agent.id}>
            {agent.hostname} - {agent.ipaddress}

            <button onClick={() => setSelectedAgentId(agent.id)}>
              View metrics
            </button>
          </li>
        ))}
      </ul>
      {latestMetrics && (
        <section>
          <h2>Latest Metrics</h2>

          <p>CPU: {latestMetrics.cpu}%</p>
          <p>Memory: {latestMetrics.memory}%</p>
          <p>Disk: {latestMetrics.disk}%</p>
          <p>Network In: {latestMetrics.network_in_mbps} Mbps</p>
          <p>Network Out: {latestMetrics.network_out_mbps} Mbps</p>

          <h3>Top Processes</h3>

          <ul>
            {latestMetrics.processes.map((process) => (
              <li key={process.id}>
                {process.name} - CPU {process.cpu}% - Memory {process.memory} MB
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}

export default App
