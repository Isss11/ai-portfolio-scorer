const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

/**
 * @param {string} ghUsername
 */
export async function initiateConnection(ghUsername) {
  const response = await fetch(`${API_URL}/`);

  for await (const chunk of response.body) {
    console.log({ chunk });
  }
}
