// Utility functions for distance calculation and address validation

export function haversine(lat1: number, lon1: number, lat2: number, lon2: number) {
  const toRad = (x: number) => (x * Math.PI) / 180;
  const R = 6371; // km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const km = R * c;
  const miles = km * 0.621371;
  return { kilometers: km, miles };
}

export function isValidAddress(address: string): boolean {
  if (!address || address.trim().length < 5) return false;
  // All numbers
  if (/^\d+$/.test(address.trim())) return false;
  // No letters
  if (!/[a-zA-Z]/.test(address)) return false;
  // Only special characters
  if (/^[^a-zA-Z0-9]+$/.test(address.trim())) return false;
  return true;
}

export function cleanAddress(address: string): string {
  let cleaned = address.replace(/suite.*$/i, '');
  cleaned = cleaned.replace(/(,\s*)+/g, ', '); // collapse any sequence of commas and spaces
  cleaned = cleaned.replace(/\s+/g, ' '); // collapse multiple spaces
  cleaned = cleaned.replace(/,\s*$/, '').trim();
  return cleaned;
} 