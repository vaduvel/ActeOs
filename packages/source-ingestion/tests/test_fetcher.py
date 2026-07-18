"""Tests for the bounded fetcher with SSRF protection."""

from __future__ import annotations

import pytest

from wb_ingestion.errors import FetchError, SSRFError
from wb_ingestion.fetcher import (
    validate_content_length,
    validate_content_type,
    validate_url,
)


class TestValidateUrl:
    def test_valid_https_url(self) -> None:
        # Should not raise (DNS may or may not resolve, but validation passes)
        # We test with a real domain that should resolve
        validate_url("https://www.google.com")

    def test_http_scheme_blocked(self) -> None:
        with pytest.raises(SSRFError, match="scheme"):
            validate_url("http://example.com")

    def test_ftp_scheme_blocked(self) -> None:
        with pytest.raises(SSRFError, match="scheme"):
            validate_url("ftp://example.com/file")

    def test_file_scheme_blocked(self) -> None:
        with pytest.raises(SSRFError, match="scheme"):
            validate_url("file:///etc/passwd")

    def test_no_scheme_blocked(self) -> None:
        with pytest.raises(SSRFError, match="scheme"):
            validate_url("example.com/path")

    def test_no_hostname_blocked(self) -> None:
        with pytest.raises(SSRFError, match="hostname"):
            validate_url("https://")

    def test_localhost_blocked(self) -> None:
        with pytest.raises(SSRFError):
            validate_url("https://127.0.0.1/admin")

    def test_private_ip_10_blocked(self) -> None:
        with pytest.raises(SSRFError, match="private"):
            validate_url("https://10.0.0.1/internal")

    def test_private_ip_192_168_blocked(self) -> None:
        with pytest.raises(SSRFError, match="private"):
            validate_url("https://192.168.1.1/router")

    def test_private_ip_172_16_blocked(self) -> None:
        with pytest.raises(SSRFError, match="private"):
            validate_url("https://172.16.0.1/internal")

    def test_link_local_blocked(self) -> None:
        with pytest.raises(SSRFError):
            validate_url("https://169.254.169.254/latest/meta-data")

    def test_ipv6_loopback_blocked(self) -> None:
        with pytest.raises(SSRFError):
            validate_url("https://[::1]/admin")

    def test_domain_checker_blocks(self) -> None:
        def no_check(url: str) -> bool:
            return False

        with pytest.raises(SSRFError, match="allowlist"):
            validate_url("https://www.google.com", domain_checker=no_check)

    def test_domain_checker_allows(self) -> None:
        def allow_all(url: str) -> bool:
            return True

        validate_url("https://www.google.com", domain_checker=allow_all)


class TestValidateContentType:
    def test_html_allowed(self) -> None:
        assert validate_content_type("text/html; charset=utf-8") == "text/html"

    def test_pdf_allowed(self) -> None:
        assert validate_content_type("application/pdf") == "application/pdf"

    def test_plain_text_allowed(self) -> None:
        assert validate_content_type("text/plain") == "text/plain"

    def test_xhtml_allowed(self) -> None:
        assert validate_content_type("application/xhtml+xml") == "application/xhtml+xml"

    def test_json_blocked(self) -> None:
        with pytest.raises(FetchError, match="Unsupported content type"):
            validate_content_type("application/json")

    def test_image_blocked(self) -> None:
        with pytest.raises(FetchError, match="Unsupported content type"):
            validate_content_type("image/png")

    def test_javascript_blocked(self) -> None:
        with pytest.raises(FetchError, match="Unsupported content type"):
            validate_content_type("application/javascript")


class TestValidateContentLength:
    def test_within_limit(self) -> None:
        validate_content_length(b"x" * 1000)

    def test_at_limit(self) -> None:
        validate_content_length(b"x" * (10 * 1024 * 1024))

    def test_over_limit(self) -> None:
        with pytest.raises(FetchError, match="too large"):
            validate_content_length(b"x" * (10 * 1024 * 1024 + 1))

    def test_custom_limit(self) -> None:
        with pytest.raises(FetchError, match="too large"):
            validate_content_length(b"x" * 101, max_bytes=100)
