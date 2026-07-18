import { describe, it, expect } from "vitest";
import {
  parseToken,
  hasScope,
  canReview,
  canPublish,
  canWriteSources,
  canWriteRules,
  canApproveChange,
  ALL_SCOPES,
} from "../auth";

describe("parseToken", () => {
  it("parses valid token", () => {
    const user = parseToken("Bearer curator1:sources:read,rules:review");
    expect(user).not.toBeNull();
    expect(user!.id).toBe("curator1");
    expect(user!.scopes.has("sources:read")).toBe(true);
    expect(user!.scopes.has("rules:review")).toBe(true);
  });

  it("returns null for invalid format", () => {
    expect(parseToken("Basic abc")).toBeNull();
    expect(parseToken("")).toBeNull();
  });

  it("handles token with no scopes", () => {
    const user = parseToken("Bearer curator1:");
    expect(user).not.toBeNull();
    expect(user!.scopes.size).toBe(0);
  });
});

describe("hasScope", () => {
  it("returns true for existing scope", () => {
    const user = parseToken("Bearer c1:sources:read")!;
    expect(hasScope(user, "sources:read")).toBe(true);
  });

  it("returns false for missing scope", () => {
    const user = parseToken("Bearer c1:sources:read")!;
    expect(hasScope(user, "rules:publish")).toBe(false);
  });

  it("returns false for null user", () => {
    expect(hasScope(null, "sources:read")).toBe(false);
  });
});

describe("role helpers", () => {
  it("canReview requires rules:review", () => {
    expect(canReview(parseToken("Bearer c1:rules:review"))).toBe(true);
    expect(canReview(parseToken("Bearer c1:sources:read"))).toBe(false);
  });

  it("canPublish requires rules:publish", () => {
    expect(canPublish(parseToken("Bearer c1:rules:publish"))).toBe(true);
    expect(canPublish(parseToken("Bearer c1:rules:review"))).toBe(false);
  });

  it("canWriteSources requires sources:write", () => {
    expect(canWriteSources(parseToken("Bearer c1:sources:write"))).toBe(true);
    expect(canWriteSources(parseToken("Bearer c1:sources:read"))).toBe(false);
  });

  it("canWriteRules requires rules:write", () => {
    expect(canWriteRules(parseToken("Bearer c1:rules:write"))).toBe(true);
    expect(canWriteRules(parseToken("Bearer c1:rules:review"))).toBe(false);
  });
});

describe("canApproveChange — two-person rule", () => {
  it("allows review by non-author for non-critical", () => {
    const user = parseToken("Bearer reviewer1:rules:review")!;
    expect(canApproveChange(user, "author1", false)).toBe(true);
  });

  it("allows review by non-author for critical", () => {
    const user = parseToken("Bearer reviewer1:rules:review")!;
    expect(canApproveChange(user, "author1", true)).toBe(true);
  });

  it("blocks self-approval for critical", () => {
    const user = parseToken("Bearer author1:rules:review")!;
    expect(canApproveChange(user, "author1", true)).toBe(false);
  });

  it("allows self-approval for non-critical", () => {
    const user = parseToken("Bearer author1:rules:review")!;
    expect(canApproveChange(user, "author1", false)).toBe(true);
  });

  it("blocks non-reviewer", () => {
    const user = parseToken("Bearer viewer1:sources:read")!;
    expect(canApproveChange(user, "author1", false)).toBe(false);
  });

  it("blocks null user", () => {
    expect(canApproveChange(null, "author1", false)).toBe(false);
  });
});

describe("ALL_SCOPES", () => {
  it("contains all expected scopes", () => {
    expect(ALL_SCOPES).toContain("sources:read");
    expect(ALL_SCOPES).toContain("sources:write");
    expect(ALL_SCOPES).toContain("rules:write");
    expect(ALL_SCOPES).toContain("rules:review");
    expect(ALL_SCOPES).toContain("rules:publish");
    expect(ALL_SCOPES.length).toBe(5);
  });
});
