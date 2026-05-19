// src/api.js
export async function predictMood(input) {
  const response = await fetch("https://backend-moodpredpage.onrender.com/predict", {
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
}
// returns {predicted_mood_score:number}
 // returns the prediction to the front end