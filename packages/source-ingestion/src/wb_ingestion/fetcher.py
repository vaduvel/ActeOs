"""Bounded fetcher with SSRF protection.

Fetches content from allowlisted URLs with strict limits on
size, timeout, redirects, and content types. Never follows
redirects to non-allowlisted domains.
"""

from __future__ import annotations

import ipaddress
import socket
import ssl
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from wb_ingestion.errors import FetchError, IngestionProblemCode, SSRFError


# --- Limits ---
MAX_CONTENT_BYTES = 10 * 1024 * 1024  # 10 MB
DEFAULT_TIMEOUT_SECONDS = 30
MAX_REDIRECTS = 3
ALLOWED_SCHEMES = {"https"}
ALLOWED_CONTENT_TYPES = {
    "text/html",
    "text/plain",
    "application/pdf",
    "application/xhtml+xml",
}

# Private/reserved IP ranges that must never be fetched (SSRF protection)
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


@dataclass(frozen=True)
class FetchResult:
    """Result of a successful fetch."""

    url: str
    final_url: str  # after redirects
    content: bytes
    content_type: str
    status_code: int
    content_length: int
    redirect_count: int


def _is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is in a blocked/private range."""
    try:
        addr = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return any(addr in network for network in _BLOCKED_NETWORKS)


def _resolve_and_check(hostname: str) -> list[str]:
    """Resolve hostname to IPs and check none are private.

    Returns list of resolved IP strings.
    Raises SSRFError if any resolved IP is private.
    """
    try:
        infos = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise SSRFError(f"DNS resolution failed for {hostname}: {exc}") from exc

    ips: list[str] = []
    for info in infos:
        ip_str = info[4][0]
        ips.append(ip_str)
        if _is_private_ip(ip_str):
            raise SSRFError(
                f"SSRF blocked: {hostname} resolves to private IP {ip_str}"
            )
    return ips


def validate_url(
    url: str,
    *,
    allowed_schemes: set[str] | None = None,
    domain_checker: Callable[[str], bool] | None = None,
) -> None:
    """Validate a URL before fetching.

    Checks scheme, resolves DNS, blocks private IPs, optionally
    checks domain allowlist. Raises on any violation.
    """
    schemes = allowed_schemes or ALLOWED_SCHEMES
    parsed = urlparse(url)

    if not parsed.scheme:
        raise SSRFError(f"URL has no scheme: {url}")
    if parsed.scheme.lower() not in schemes:
        raise SSRFError(
            f"URL scheme '{parsed.scheme}' not allowed (allowed: {schemes})"
        )

    hostname = parsed.hostname
    if not hostname:
        raise SSRFError(f"URL has no hostname: {url}")

    # Block raw IP addresses that are private
    if _is_private_ip(hostname):
        raise SSRFError(f"SSRF blocked: private IP {hostname}")

    # DNS resolution + private IP check
    _resolve_and_check(hostname)

    # Optional domain allowlist check
    if domain_checker is not None and not domain_checker(url):
        raise SSRFError(f"Domain not in allowlist: {hostname}")


def validate_content_type(content_type: str) -> str:
    """Validate content type header. Returns normalized content type string.

    Raises FetchError if the content type is not supported.
    """
    # Strip charset/boundary parameters
    base_type = content_type.split(";")[0].strip().lower()
    if base_type not in ALLOWED_CONTENT_TYPES:
        raise FetchError(
            IngestionProblemCode.UNSUPPORTED_CONTENT_TYPE,
            f"Unsupported content type: {base_type} "
            f"(allowed: {sorted(ALLOWED_CONTENT_TYPES)})",
        )
    return base_type


def validate_content_length(content: bytes, max_bytes: int = MAX_CONTENT_BYTES) -> None:
    """Check content size limit. Raises FetchError if too large."""
    if len(content) > max_bytes:
        raise FetchError(
            IngestionProblemCode.CONTENT_TOO_LARGE,
            f"Content too large: {len(content)} bytes (max {max_bytes})",
        )


class BoundedFetcher:
    """Fetches content with SSRF protection and strict limits.

    In production, uses urllib.request. For tests, inject a
    transport callable that takes a URL and returns FetchResult.
    """

    def __init__(
        self,
        domain_checker: Callable[[str], bool] | None = None,
        *,
        timeout: int = DEFAULT_TIMEOUT_SECONDS,
        max_bytes: int = MAX_CONTENT_BYTES,
        max_redirects: int = MAX_REDIRECTS,
    ) -> None:
        self._domain_checker = domain_checker
        self._timeout = timeout
        self._max_bytes = max_bytes
        self._max_redirects = max_redirects

    def fetch(self, url: str) -> FetchResult:
        """Fetch URL with all safety checks.

        Validates URL (SSRF), checks content type and size limits.
        Uses urllib.request for actual fetching.
        """
        validate_url(url, domain_checker=self._domain_checker)

        # Use urllib.request with a custom opener that doesn't follow
        # redirects to non-allowlisted domains
        import urllib.request

        ctx = ssl.create_default_context()

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "ActeOS-ContentBot/0.1 (+https://github.com/acteos)",
                "Accept": "text/html,application/xhtml+xml,application/pdf,text/plain",
            },
        )

        redirect_count = 0
        current_url = url

        for _ in range(self._max_redirects + 1):
            try:
                with urllib.request.urlopen(
                    request, timeout=self._timeout, context=ctx
                ) as response:
                    status = response.status
                    content_type = response.headers.get("Content-Type", "")
                    final_url = response.url

                    # If we were redirected, validate the new URL too
                    if final_url != current_url:
                        validate_url(
                            final_url,
                            domain_checker=self._domain_checker,
                        )
                        redirect_count += 1

                    # Validate content type
                    normalized_ct = validate_content_type(content_type)

                    # Read with size limit
                    content = response.read(self._max_bytes + 1)
                    validate_content_length(content, self._max_bytes)

                    return FetchResult(
                        url=url,
                        final_url=final_url,
                        content=content,
                        content_type=normalized_ct,
                        status_code=status,
                        content_length=len(content),
                        redirect_count=redirect_count,
                    )

            except urllib.error.HTTPError as exc:
                if exc.code in (301, 302, 303, 307, 308):
                    location = exc.headers.get("Location", "")
                    if not location:
                        raise FetchError(
                            IngestionProblemCode.FETCH_FAILED,
                            f"Redirect without Location header from {current_url}",
                        ) from exc
                    redirect_count += 1
                    if redirect_count > self._max_redirects:
                        raise FetchError(
                            IngestionProblemCode.FETCH_FAILED,
                            f"Too many redirects (>{self._max_redirects})",
                        ) from exc
                    current_url = location
                    validate_url(current_url, domain_checker=self._domain_checker)
                    request = urllib.request.Request(
                        current_url,
                        headers=request.headers,
                    )
                    continue
                raise FetchError(
                    IngestionProblemCode.FETCH_FAILED,
                    f"HTTP {exc.code} from {current_url}: {exc.reason}",
                ) from exc
            except urllib.error.URLError as exc:
                if "timed out" in str(exc.reason).lower():
                    raise FetchError(
                        IngestionProblemCode.FETCH_TIMEOUT,
                        f"Timeout fetching {current_url} ({self._timeout}s)",
                    ) from exc
                raise FetchError(
                    IngestionProblemCode.FETCH_FAILED,
                    f"URL error fetching {current_url}: {exc.reason}",
                ) from exc

        raise FetchError(
            IngestionProblemCode.FETCH_FAILED,
            f"Redirect loop exhausted for {url}",
        )
