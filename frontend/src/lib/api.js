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
