import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

/**
 * @param {string} text
 * @returns {string | null}
 */
export function parseGithubUsername(text) {
  const match = text.match(/github\.com\/([^/?]+)/);

  if (match) {
    return match[1];
  }

  if (text.includes("/") || text.includes("?")) {
    return null;
  }

  return text;
}

export function isNotNullish(value) {
  return value != null; // note: intentional double eq
}
