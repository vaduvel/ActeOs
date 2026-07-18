/**
 * XSS-safe content sanitization.
 *
 * NEVER render untrusted source HTML directly. All source content
 * is displayed as plain text or sanitized HTML.
 */

/**
 * Strip all HTML tags and return plain text.
 * Use this for displaying source excerpts.
 * Script and style tags are removed along with their content.
 */
export function stripHtml(html: string): string {
  return html
    // Remove script and style tags with their content first
    .replace(/<script[\s>][\s\S]*?<\/script\s*>/gi, "")
    .replace(/<style[\s>][\s\S]*?<\/style\s*>/gi, "")
    .replace(/<noscript[\s>][\s\S]*?<\/noscript\s*>/gi, "")
    // Remove remaining tags
    .replace(/<[^>]*>/g, "")
    // Decode entities
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .trim();
}

/**
 * Escape a string for safe insertion into HTML.
 * Use this when you must interpolate user content into HTML.
 */
export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Sanitize a URL to prevent javascript: protocol XSS.
 * Returns null if the URL is not safe.
 */
export function sanitizeUrl(url: string): string | null {
  const lower = url.toLowerCase().trim();
  if (
    lower.startsWith("javascript:") ||
    lower.startsWith("data:") ||
    lower.startsWith("vbscript:") ||
    lower.startsWith("file:")
  ) {
    return null;
  }
  return url;
}

/**
 * Check if a string contains potential XSS patterns.
 * Used for validation, not sanitization.
 */
export function containsXssPatterns(text: string): boolean {
  const patterns = [
    /<script/i,
    /javascript:/i,
    /on\w+\s*=/i, // onclick=, onerror=, etc.
    /data:text\/html/i,
  ];
  return patterns.some((p) => p.test(text));
}
