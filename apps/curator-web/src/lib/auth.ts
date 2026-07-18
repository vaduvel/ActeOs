/**
 * Curator authentication and RBAC.
 *
 * In production, this validates an OIDC JWT from the identity provider.
 * For development, we accept a Bearer token with the format:
 *   `Bearer <curator_id>:<scope1,scope2,...>`
 *
 * Scopes map to the curator portal sections:
 *   - sources:read    → view source registry
 *   - sources:write   → create/edit sources, trigger fetch
 *   - rules:write     → create/edit rule drafts
 *   - rules:review    → approve/reject rule versions (2-reviewer rule)
 *   - rules:publish   → publish/rollback bundles
 */

export type CuratorScope =
  | "sources:read"
  | "sources:write"
  | "rules:write"
  | "rules:review"
  | "rules:publish";

export interface CuratorUser {
  id: string;
  name: string;
  scopes: Set<CuratorScope>;
}

export const ALL_SCOPES: CuratorScope[] = [
  "sources:read",
  "sources:write",
  "rules:write",
  "rules:review",
  "rules:publish",
];

export function parseToken(token: string): CuratorUser | null {
  if (!token.startsWith("Bearer ")) return null;
  const raw = token.slice(7).trim();
  // Split on first colon only: curator_id:scope1,scope2
  // Scopes themselves contain colons (e.g. "sources:read")
  const colonIdx = raw.indexOf(":");
  if (colonIdx < 0) return null;
  const id = raw.slice(0, colonIdx);
  const scopeStr = raw.slice(colonIdx + 1);
  if (!id) return null;
  // Scopes are comma-separated, each containing a colon (e.g. "sources:read,rules:review")
  const scopes = new Set(
    scopeStr.split(",").map(s => s.trim()).filter(Boolean) as CuratorScope[]
  );
  return { id, name: id, scopes };
}

export function hasScope(user: CuratorUser | null, scope: CuratorScope): boolean {
  return user?.scopes.has(scope) ?? false;
}

export function canReview(user: CuratorUser | null): boolean {
  return hasScope(user, "rules:review");
}

export function canPublish(user: CuratorUser | null): boolean {
  return hasScope(user, "rules:publish");
}

export function canWriteSources(user: CuratorUser | null): boolean {
  return hasScope(user, "sources:write");
}

export function canWriteRules(user: CuratorUser | null): boolean {
  return hasScope(user, "rules:write");
}

/**
 * Check if a user can approve a change.
 * The two-person rule: a critical author cannot approve their own change.
 */
export function canApproveChange(
  user: CuratorUser | null,
  authorId: string,
  isCritical: boolean
): boolean {
  if (!canReview(user)) return false;
  if (isCritical && user!.id === authorId) return false;
  return true;
}
