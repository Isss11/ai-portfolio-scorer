const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

/**
 * @param {string} ghUsername
 */
export function initiateEventSource(ghUsername, handleEvent) {
  const eventSource = new EventSource(`${API_URL}/score/${ghUsername}`);

  function close() {
    if (eventSource.readyState === EventSource.CLOSED) return;
    eventSource.close();
  }

  eventSource.addEventListener("close", close);

  eventSource.onmessage = (event) => {
    /** @type {{ event: string, [key: string]: any }} */
    const message = JSON.parse(event.data);

    handleEvent(message.type, message.data);
  };

  return close;
}

/**
 * @param {string[]} usernames
 * @param {AbortSignal} abortSignal
 */
export async function compareProfiles(usernames, abortSignal) {
  const resp = await fetch(`${API_URL}/compare/${usernames.join(",")}`, {
    signal: abortSignal,
  });

  if (!resp.ok) {
    throw new Error("Failed to compare profiles");
  }

  const comparison = await resp.json();

  return comparison;
}
