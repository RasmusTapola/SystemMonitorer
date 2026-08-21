import { useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = "http://localhost:8000"

function App() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedAgentId, setSelectedAgentId] = useState(null);
  const [latestMetrics, setLatestMetrics] = useState(null);
  const [processSort, setProcessSort] = useState("cpu");
  const sortedProcesses = latestMetrics
    ? [...latestMetrics.processes].sort((a, b) => b[processSort] - a[processSort])
    : [];
  const selectedAgent = agents.find(
    (agent) => String(agent.id) === String(selectedAgentId)
  );
  const [timeframeMinutes, setTimeframeMinutes] = useState(15);
  const [measurements, setMeasurements] = useState([]);
  const [showMeasurements, setShowMeasurements] = useState(false);

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

    const intervalId = setInterval(fetchAgents, 5000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    if (!selectedAgentId) return;

    async function fetchLatestMetrics() {
      const response = await fetch(
        `${API_BASE_URL}/agents/${selectedAgentId}/latest`
      );

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();
      setLatestMetrics(data);
    }

    fetchLatestMetrics();

    const interval = setInterval(fetchLatestMetrics, 5000);
  
    return () => {
      clearInterval(interval)
    }
  
  }, [selectedAgentId]);

  useEffect(() => {
  if (!selectedAgentId) return;

  async function fetchMeasurements() {
    const response = await fetch(
      `${API_BASE_URL}/agents/${selectedAgentId}/measurements?minutes=${timeframeMinutes}`
    );

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const data = await response.json();
    setMeasurements(data);
  }

  fetchMeasurements();

  const interval = setInterval(fetchMeasurements, 5000);

  return () => clearInterval(interval);
}, [selectedAgentId, timeframeMinutes]);

  if (loading) {
    return <p>Loading agents...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
     <main>
      <h1>System Monitor</h1>

      <div className="agent-selector">
        <label htmlFor="agent-select">Select agent</label>

        <select
          id="agent-select"
          value={selectedAgentId ?? ""}
          onChange={(event) => {
            setSelectedAgentId(event.target.value);
            setLatestMetrics(null);
            setMeasurements([]);
            setShowMeasurements(false);
          }}
        >
          <option value="">Choose an agent...</option>

          {agents.map((agent) => (
            <option key={agent.id} value={agent.id}>
              {agent.hostname} - {agent.ipaddress}
            </option>
          ))}
        </select>

        {selectedAgent && (
          <span className={`status ${getAgentStatus(selectedAgent)}`}>
            <span className="status-dot" />
            {getAgentStatus(selectedAgent)}
          </span>
        )}
      </div>

      <label htmlFor="timeframe-select">Timeframe</label>

      <select
        id="timeframe-select"
        value={timeframeMinutes}
        onChange={(event) => {
          setTimeframeMinutes(Number(event.target.value));
          setShowMeasurements(false);
        }}>
       
        <option value={5}>Last 5 minutes</option>
        <option value={15}>Last 15 minutes</option>
        <option value={60}>Last hour</option>
        <option value={360}>Last 6 hours</option>
        <option value={1440}>Last 24 hours</option>
        
      </select>

      <p>Measurements in selected timeframe: {measurements.length}</p>

      <button onClick={() => setShowMeasurements(!showMeasurements)}>
        {showMeasurements ? "Hide measurements" : "Display measurements"}
      </button>
      {showMeasurements && (
        <ul>
          {measurements.map((measurement) => (
            <li key={measurement.id}>
              {measurement.timestamp}: CPU {measurement.cpu}% - Memory {measurement.memory}%
            </li>
          ))}
        </ul>
      )}

      {latestMetrics && (
        <section>
          <h2>Latest Metrics</h2>

          <p>CPU: {latestMetrics.cpu}%</p>
          <p>Memory: {latestMetrics.memory}%</p>
          <p>Disk: {latestMetrics.disk}%</p>
          <p>Network In: {latestMetrics.network_in_mbps} Mbps</p>
          <p>Network Out: {latestMetrics.network_out_mbps} Mbps</p>

          <h3>Top Processes</h3>

          <p>Filter by:</p>
          <select
            value={processSort}
            onChange={(event) => setProcessSort(event.target.value)}
          >
            <option value="cpu">CPU usage</option>
            <option value="memory">Memory usage</option>
          </select>

          <ul>
            {sortedProcesses.map((process) => (
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

function getAgentStatus(agent) {
  const lastSeen = new Date(agent.last_seen);
  const now = new Date();

  const secondsSinceLastSeen = (now - lastSeen) / 1000;

  return secondsSinceLastSeen <= 15 ? "connected" : "disconnected";
}