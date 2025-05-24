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
  if (!address || address.trim().length < 8) return false;
  // Require at least one number (street number)
  if (!/\d+/.test(address)) return false;
  // Require at least one word (street name)
  if (!/[a-zA-Z]{2,}/.test(address)) return false;
  // Require a comma (to separate street from city/state)
  if (!address.includes(',')) return false;
  // Require at least two comma-separated parts
  const parts = address.split(',').map(p => p.trim()).filter(Boolean);
  if (parts.length < 2) return false;
  // Optionally: Require state code or zip in the last part
  const lastPart = parts[parts.length - 1].trim();
  if (
    !/^[A-Za-z]{2}$/.test(lastPart) && // state code only
    !/^[A-Za-z]{2}\s*\d{5}$/.test(lastPart) // state code + zip
  ) return false;
  return true;
}

export function cleanAddress(address: string): string {
  let cleaned = address.replace(/suite.*$/i, '');
  cleaned = cleaned.replace(/(,\s*)+/g, ', '); // collapse any sequence of commas and spaces
  cleaned = cleaned.replace(/\s+/g, ' '); // collapse multiple spaces
  cleaned = cleaned.replace(/,\s*$/, '').trim();
  return cleaned;
} 