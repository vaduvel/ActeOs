"""File loaders for governed authoring batches.

Requires PyYAML (install the ``authoring`` extra). Kept out of the package
__init__ so the pure evaluator imports without any third-party dependency.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "PyYAML is required for the authoring loader: pip install 'acteos-rule-engine[authoring]'"
    ) from exc


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_batch(batch_dir: Any) -> dict:
    """Load a single governed batch directory into parsed dicts.

    ``templates`` is the optional ``templates.yaml`` (step/requirement template
    content authored from the event card); ``None`` when absent. It is loaded
    here so the publish pipeline can materialize content.step_templates /
    content.requirement_templates without a second filesystem pass.
    """
    d = Path(batch_dir)
    ruleset = _load_yaml(d / "rules.yaml")
    fixtures = _load_yaml(d / "fixtures" / "golden.yaml")
    claims_path = d / "source_claims.yaml"
    claims = _load_yaml(claims_path) if claims_path.exists() else None
    templates_path = d / "templates.yaml"
    templates = _load_yaml(templates_path) if templates_path.exists() else None
    return {
        "batch_dir": str(d),
        "ruleset": ruleset,
        "fixtures": fixtures,
        "claims": claims,
        "templates": templates,
    }


def discover_batches(inbox_dir: Any) -> list[Path]:
    """Return batch directories under inbox_dir that have rules + golden fixtures."""
    base = Path(inbox_dir)
    out: list[Path] = []
    for child in sorted(base.iterdir()):
        if child.is_dir() and (child / "rules.yaml").exists() and (child / "fixtures" / "golden.yaml").exists():
            out.append(child)
    return out
