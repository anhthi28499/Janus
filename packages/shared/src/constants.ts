/**
 * Get API base URL from environment.
 * - Expo: EXPO_PUBLIC_API_BASE
 * - Nuxt: NUXT_PUBLIC_API_BASE
 * - Fallback: http://localhost:5000/api/v1
 */
export function getApiBase(): string {
  if (typeof process !== 'undefined' && process.env?.EXPO_PUBLIC_API_BASE) {
    return process.env.EXPO_PUBLIC_API_BASE;
  }
  if (typeof process !== 'undefined' && process.env?.NUXT_PUBLIC_API_BASE) {
    const base = process.env.NUXT_PUBLIC_API_BASE;
    return base.endsWith('/api/v1') ? base : `${base}/api/v1`;
  }
  return 'http://localhost:5000/api/v1';
}
