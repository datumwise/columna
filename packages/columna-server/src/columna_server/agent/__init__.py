"""columna_server.agent — the natural-language query agent (a true MCP client; ADR-032 D8)."""
from .conversation import AGENT, ENGINE, USER, Turn
from .loop import Agent, MAX_TOOL_CYCLES, load_system_prompt, prompt_example_queries, render_manifold_context
from .providers import (AnthropicProvider, Provider, ProviderUnavailable, ScriptedProvider,
                        TextStep, ToolCall, ToolStep, make_provider)

__all__ = ["Turn", "USER", "AGENT", "ENGINE", "Agent", "MAX_TOOL_CYCLES", "load_system_prompt",
           "prompt_example_queries", "render_manifold_context",
           "Provider", "ProviderUnavailable", "ScriptedProvider", "AnthropicProvider",
           "ToolCall", "ToolStep", "TextStep", "make_provider"]
