const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const MODEL = {
  bias: -0.0351579522969403,
  weights: {
    sleep_hours: 0.3807960818477067,
    stress_level: -0.2557397991597848,
    nutrition_quality: 0.22070627323483816,
    social_minutes: 0.010964075940711122,
    water_effect: 0.4109646313590779,
  },
};

function predictMoodLocally(input) {
  const waterEffect = -1 * (input.water_liters - 2.0) ** 2 + 1.0;
  const predictedMoodScore =
    MODEL.bias +
    input.sleep_hours * MODEL.weights.sleep_hours +
    input.stress_level * MODEL.weights.stress_level +
    input.nutrition_quality * MODEL.weights.nutrition_quality +
    input.social_minutes * MODEL.weights.social_minutes +
    waterEffect * MODEL.weights.water_effect;

  return { predicted_mood_score: predictedMoodScore };
}

export async function predictMood(input) {
  if (!API_BASE_URL) {
    return predictMoodLocally(input);
  }

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(input)
    });

    if (!response.ok) {
      throw new Error("Prediction failed");
    }

    return await response.json();
  } catch (error) {
    console.warn("Backend unavailable. Falling back to local prediction.", error);
    return predictMoodLocally(input);
  }
}
