const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function calculateDistance(source, destination) {
  const res = await fetch(`${API_URL}/distance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source, destination })
  });
  if (!res.ok) {
    let error;
    try {
      error = await res.json();
    } catch {
      error = { detail: 'Failed to calculate distance' };
    }
    throw new Error(error.detail || 'Failed to calculate distance');
  }
  return await res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_URL}/history`);
  if (!res.ok) {
    throw new Error('Failed to fetch history');
  }
  return await res.json();
} 