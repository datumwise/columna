"""columna_server.init — the `columna init` authoring on-ramp (Track 2). The loop harness + the eval
suite. Hermetic by default (the scripted provider); the real mind (AnthropicProvider) runs only on an
explicit go."""
from .loop import InitLoop, ScriptedProvider, LoopViolation
from .eval import (Benchmark, BenchmarkResult, RunRecord, score, run_benchmark, render_report,
                   rescore_run, build_aperture, RetentionError, SCORER_VERSION, BENCHMARK_LIST_VERSION)
from .providers import (AnthropicProvider, ProviderUnavailable, parse_proposals, system_prompt,
                        revise_prompt, aperture_context)
from .runner import run_replicated_ab, InfraAbort

__all__ = ["InitLoop", "ScriptedProvider", "LoopViolation",
           "Benchmark", "BenchmarkResult", "RunRecord", "score", "run_benchmark", "render_report",
           "rescore_run", "build_aperture", "RetentionError", "SCORER_VERSION", "BENCHMARK_LIST_VERSION",
           "AnthropicProvider", "ProviderUnavailable", "parse_proposals", "system_prompt",
           "revise_prompt", "aperture_context", "run_replicated_ab", "InfraAbort"]
