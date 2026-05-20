const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://moodpredictor-lbsk.onrender.com";

export async function predictMood(input, options = {}) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(input),
    signal: options.signal,
  });

  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  return await response.json();
}
