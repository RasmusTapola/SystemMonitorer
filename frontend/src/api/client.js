const API_BASE_URL = "http://localhost:8000";

export async function getAgents() {
  const response = await fetch(`${API_BASE_URL}/agents`);
  return response.json();
}

export async function getLatestMetrics(agentId) {
  const response = await fetch(`${API_BASE_URL}/agents/${agentId}/latest`);
  return response.json();
}