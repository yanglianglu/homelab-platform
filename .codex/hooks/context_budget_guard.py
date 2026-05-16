#!/usr/bin/env python3
"""Read-only Codex hook that suggests checkpointing long or risky sessions."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any


WARN_TOKENS = 60_000
STRONG_WARN_TOKENS = 100_000

RISK_KEYWORDS = [
    "perform",
    "apply",
    "create",
    "mutate",
    "delete",
    "reorganize",
    "notion",
    "linear",
    "harvester",
    "talos",
    "kubernetes",
    "argo",
    "live cluster",
    "next gate",
    "proceed",
    "debug",
    "repair",
    "placement",
    "control plane",
    "worker",
    "data-01",
]

DOMAIN_SWITCH_PATTERNS = [
    (r"harvester|talos", r"notion"),
    (r"talos", r"kubernetes"),
    (r"cluster operation|live cluster|repair|debug", r"documentation|docs|notion"),
    (r"implement|implementation|perform|proceed", r"architecture|decision|adr"),
]


def safe_json(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, separators=(",", ":")))


def read_input() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def transcript_tokens(path: str | None) -> int:
    if not path:
        return 0
    try:
        if not os.path.isfile(path):
            return 0
        size = os.path.getsize(path)
        return size // 4
    except Exception:
        return 0


def appears_cross_domain(prompt: str) -> bool:
    text = prompt.lower()
    for left, right in DOMAIN_SWITCH_PATTERNS:
        if re.search(left, text) and re.search(right, text):
            return True
    domain_hits = sum(
        1
        for domain in ["harvester", "talos", "kubernetes", "notion", "linear", "docs", "architecture"]
        if domain in text
    )
    return domain_hits >= 3


def risk_hits(prompt: str) -> list[str]:
    text = prompt.lower()
    return [keyword for keyword in RISK_KEYWORDS if keyword in text]


def main() -> None:
    try:
        data = read_input()
        prompt = str(data.get("prompt") or "")
        transcript_path = data.get("transcript_path")
        hook_event_name = str(data.get("hook_event_name") or "")
        cwd = str(data.get("cwd") or "")

        approx_tokens = transcript_tokens(str(transcript_path) if transcript_path else None)
        hits = risk_hits(prompt)
        cross_domain = appears_cross_domain(prompt)
        proceed_after_complex = bool(re.search(r"\b(proceed|perform|next gate|continue)\b", prompt.lower())) and bool(hits)

        reasons: list[str] = []
        if approx_tokens > STRONG_WARN_TOKENS:
            reasons.append(f"transcript is very large at about {approx_tokens:,} tokens")
        elif approx_tokens > WARN_TOKENS:
            reasons.append(f"transcript is large at about {approx_tokens:,} tokens")
        if cross_domain:
            reasons.append("prompt appears to cross platform domains")
        if proceed_after_complex:
            reasons.append("prompt asks to proceed after complex or risky context")
        if len(hits) >= 4:
            reasons.append("prompt contains multiple high-risk platform-operation keywords")

        if reasons:
            message = (
                "Context budget guard: This session appears long or cross-domain. "
                "Before implementing, consider invoking the context-checkpoint skill and recommend /compact or /new if appropriate. "
                f"Signals: {'; '.join(reasons)}."
            )
        else:
            message = ""

        safe_json(
            {
                "additionalContext": message,
                "metadata": {
                    "hook_event_name": hook_event_name,
                    "cwd": cwd,
                    "approx_transcript_tokens": approx_tokens,
                    "cross_domain": cross_domain,
                    "risk_keyword_count": len(hits),
                },
            }
        )
    except Exception:
        safe_json({"additionalContext": "", "metadata": {"hook_error_ignored": True}})


if __name__ == "__main__":
    main()
