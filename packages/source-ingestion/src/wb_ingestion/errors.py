"""Error types for source ingestion.

Uses the shared error vocabulary from wb_contracts, extended
with ingestion-specific problem codes.
"""

from __future__ import annotations

from enum import Enum

from wb_contracts.errors import WbError


class IngestionProblemCode(str, Enum):
    """Problem codes specific to source ingestion."""

    FETCH_FAILED = "fetch_failed"
    SSRF_BLOCKED = "ssrf_blocked"
    SNAPSHOT_IMMUTABLE = "snapshot_immutable"
    SNAPSHOT_NOT_FOUND = "snapshot_not_found"
    NORMALIZE_FAILED = "normalize_failed"
    DIFF_FAILED = "diff_failed"
    SOURCE_NOT_FOUND = "source_not_found"
    SOURCE_ALREADY_EXISTS = "source_already_exists"
    PUBLISH_CONFLICT = "publish_conflict"
    REVIEW_REQUIRED = "review_required"
    REVIEW_SELF_APPROVAL = "review_self_approval"
    ROLLBACK_FAILED = "rollback_failed"
    AI_EXTRACTION_DISABLED = "ai_extraction_disabled"
    CONTENT_TOO_LARGE = "content_too_large"
    UNSUPPORTED_CONTENT_TYPE = "unsupported_content_type"
    FETCH_TIMEOUT = "fetch_timeout"
    MALFORMED_DOCUMENT = "malformed_document"


class IngestionError(WbError):
    """Base error for all ingestion failures."""

    def __init__(self, code: IngestionProblemCode, detail: str) -> None:
        super().__init__(detail)
        self.ingestion_code = code

    def to_problem(self) -> dict:
        return {"type": self.ingestion_code.value, "title": self.message}


class RegistryError(IngestionError):
    """Source registry operation failed."""


class FetchError(IngestionError):
    """Fetch operation failed."""


class SSRFError(FetchError):
    """SSRF protection triggered."""

    def __init__(self, detail: str) -> None:
        super().__init__(IngestionProblemCode.SSRF_BLOCKED, detail)


class SnapshotError(IngestionError):
    """Snapshot operation failed."""


class NormalizeError(IngestionError):
    """Normalization failed."""


class DiffError(IngestionError):
    """Diff computation failed."""


class ReviewError(IngestionError):
    """Review workflow error."""


class PublishError(IngestionError):
    """Publish/rollback error."""


class StalenessError(IngestionError):
    """Staleness scheduler error."""
