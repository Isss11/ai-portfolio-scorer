/**
 * Format a number as a ranking. For example, 1 becomes "1st", 2 becomes "2nd", 3 becomes "3rd", etc.
 *
 * @param {number} ranking
 * @returns {string}
 */
export function formatRanking(ranking) {
  if (ranking === 1) return "1st";
  if (ranking === 2) return "2nd";
  if (ranking === 3) return "3rd";
  return `${ranking}th`;
}
