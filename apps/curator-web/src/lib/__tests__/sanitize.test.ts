import { describe, it, expect } from "vitest";
import { stripHtml, escapeHtml, sanitizeUrl, containsXssPatterns } from "../sanitize";

describe("stripHtml", () => {
  it("strips basic tags", () => {
    expect(stripHtml("<p>Hello <b>world</b></p>")).toBe("Hello world");
  });

  it("strips script tags and content", () => {
    expect(stripHtml('<p>Before</p><script>alert("xss")</script><p>After</p>')).toBe("BeforeAfter");
  });

  it("handles empty input", () => {
    expect(stripHtml("")).toBe("");
  });

  it("handles entities", () => {
    expect(stripHtml("&lt;div&gt;")).toBe("<div>");
    expect(stripHtml("&amp;")).toBe("&");
    expect(stripHtml("&quot;hello&quot;")).toBe('"hello"');
  });

  it("strips nested tags", () => {
    expect(stripHtml("<div><p><span><b>deep</b></span></p></div>")).toBe("deep");
  });
});

describe("escapeHtml", () => {
  it("escapes HTML special chars", () => {
    expect(escapeHtml('<script>alert("xss")</script>')).toBe(
      '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
    );
  });

  it("escapes ampersand", () => {
    expect(escapeHtml("A & B")).toBe("A &amp; B");
  });

  it("escapes quotes", () => {
    expect(escapeHtml('say "hello"')).toBe("say &quot;hello&quot;");
  });

  it("escapes single quotes", () => {
    expect(escapeHtml("it's")).toBe("it&#039;s");
  });
});

describe("sanitizeUrl", () => {
  it("allows https URLs", () => {
    expect(sanitizeUrl("https://example.com")).toBe("https://example.com");
  });

  it("allows http URLs", () => {
    expect(sanitizeUrl("http://example.com")).toBe("http://example.com");
  });

  it("blocks javascript: protocol", () => {
    expect(sanitizeUrl("javascript:alert(1)")).toBeNull();
  });

  it("blocks data: protocol", () => {
    expect(sanitizeUrl("data:text/html,<script>alert(1)</script>")).toBeNull();
  });

  it("blocks vbscript: protocol", () => {
    expect(sanitizeUrl("vbscript:msgbox(1)")).toBeNull();
  });

  it("blocks file: protocol", () => {
    expect(sanitizeUrl("file:///etc/passwd")).toBeNull();
  });

  it("handles case variations", () => {
    expect(sanitizeUrl("JavaScript:alert(1)")).toBeNull();
    expect(sanitizeUrl("JAVASCRIPT:alert(1)")).toBeNull();
  });
});

describe("containsXssPatterns", () => {
  it("detects script tags", () => {
    expect(containsXssPatterns('<script>alert("xss")</script>')).toBe(true);
  });

  it("detects javascript: protocol", () => {
    expect(containsXssPatterns('<a href="javascript:alert(1)">click</a>')).toBe(true);
  });

  it("detects event handlers", () => {
    expect(containsXssPatterns('<img onerror="alert(1)" src="x">')).toBe(true);
    expect(containsXssPatterns('<div onclick="alert(1)">click</div>')).toBe(true);
  });

  it("detects data:text/html", () => {
    expect(containsXssPatterns('data:text/html,<script>alert(1)</script>')).toBe(true);
  });

  it("allows safe text", () => {
    expect(containsXssPatterns("Hello world, this is safe text")).toBe(false);
    expect(containsXssPatterns('<a href="https://example.com">Safe link</a>')).toBe(false);
  });
});
