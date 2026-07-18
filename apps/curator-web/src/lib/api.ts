/**
 * API client for the ActeOS backend.
 *
 * All calls go through the curator Bearer token.
 * The API base URL is configurable via environment variable.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiError {
  type: string;
  title: string;
  status: number;
  code: string;
  detail?: string;
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = token;
  }

  const resp = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!resp.ok) {
    const problem = (await resp.json()) as ApiError;
    throw new ApiRequestError(problem);
  }

  return resp.json() as Promise<T>;
}

export class ApiRequestError extends Error {
  problem: ApiError;

  constructor(problem: ApiError) {
    super(problem.title);
    this.problem = problem;
  }
}

// --- Sources ----------------------------------------------------------------

export interface SourceItem {
  id: string;
  canonical_url: string;
  publisher: string;
  authority_level: string;
  status: string;
  freshness_class: string;
  review_interval_days: number;
  last_verified_at: string | null;
}

export function listSources(token: string) {
  return request<{ items: SourceItem[] }>("/v1/curator/sources", {}, token);
}

export function createSource(
  token: string,
  data: {
    canonical_url: string;
    publisher: string;
    authority_level: string;
    freshness_class: string;
    review_interval_days: number;
  }
) {
  return request<SourceItem>("/v1/curator/sources", {
    method: "POST",
    body: JSON.stringify(data),
  }, token);
}

export function fetchSource(token: string, sourceId: string) {
  return request<{ job_id: string; status: string }>(
    `/v1/curator/sources/${sourceId}/fetch`,
    { method: "POST" },
    token
  );
}

// --- Rules / Review -----------------------------------------------------------

export interface RuleVersionStatus {
  rule_version_id: string;
  status: string;
  reviews_required: number;
  reviews_received: number;
}

export function reviewRuleVersion(
  token: string,
  ruleVersionId: string,
  decision: "approve" | "request_changes" | "reject",
  rationale: string
) {
  return request<RuleVersionStatus>(
    `/v1/curator/rule-versions/${ruleVersionId}/review`,
    {
      method: "POST",
      body: JSON.stringify({ decision, rationale }),
    },
    token
  );
}

// --- Publish / Rollback -------------------------------------------------------

export interface BundlePublication {
  publication_id: string;
  bundle_id: string;
  bundle_hash: string;
  channel: string;
  published_at: string;
}

export function publishBundle(
  token: string,
  bundleId: string,
  channel: "canary" | "production",
  reason: string
) {
  return request<BundlePublication>(
    `/v1/curator/bundles/${bundleId}/publish`,
    {
      method: "POST",
      body: JSON.stringify({ channel, reason }),
    },
    token
  );
}

export function rollbackBundle(
  token: string,
  bundleId: string,
  targetPublicationId: string,
  reason: string
) {
  return request<BundlePublication>(
    `/v1/curator/bundles/${bundleId}/rollback`,
    {
      method: "POST",
      body: JSON.stringify({ target_publication_id: targetPublicationId, reason }),
    },
    token
  );
}

// --- Evidence -----------------------------------------------------------------

export interface SourceClaimEvidence {
  id: string;
  claim_text: string;
  source: SourceItem;
  evidence_excerpt: string;
  confidence: string;
  effective_from: string | null;
  effective_to: string | null;
}

export function getClaimEvidence(claimId: string) {
  return request<SourceClaimEvidence>(`/v1/evidence/${claimId}`);
}
