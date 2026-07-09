"""columna_server.agent.conversation — the shared turn model."""
from __future__ import annotations

from dataclasses import dataclass

USER = "user"      # a human message
AGENT = "agent"    # the agent's proposed line (QUERY:/ASK:)
ENGINE = "engine"  # a compact wire summary the system appends after each query


@dataclass(frozen=True)
class Turn:
    role: str      # USER | AGENT | ENGINE
    text: str
