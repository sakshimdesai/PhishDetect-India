// Thin wrapper around the existing Flask API.
// Endpoint, request shape and response shape are untouched —
// see app.py: POST /predict { input, input_type } -> { input_type, prediction, confidence, reasons[] }

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000";

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * @param {string} input - raw SMS text or URL
 * @param {"sms"|"url"} inputType
 * @returns {Promise<{input_type: string, prediction: "Phishing"|"Legitimate", confidence: number, reasons: Array<{feature:string, reason:string, contribution:number, direction:string}>}>}
 */
export async function predict(input, inputType) {
  let response;

  try {
    response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input, input_type: inputType }),
    });
  } catch {
    throw new ApiError(
      "Unable to reach the detection engine. Please make sure the Flask server is running on port 5000.",
      0
    );
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new ApiError("The detection engine returned an unreadable response.", response.status);
  }

  if (!response.ok) {
    throw new ApiError(data?.error || "The detection engine rejected the request.", response.status);
  }

  return data;
}
