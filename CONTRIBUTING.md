# Contributing

Thanks for helping with `senk-video-generator`, which is managed by SENK. The project accepts issue reports, documentation fixes, and contributions to verifiers, provider adapters, and governance implementation.

## Before you start

- Read [`AGENTS.md`](AGENTS.md) and the `foundation/`, `execution/`, `video/`, and `verification/` documents that apply to your change.
- Generation complete, technically valid, human-accepted, formally selected, timeline-bound, and released are different states. Do not collapse them in code or documentation.
- Runtime evidence records observations only. A passing test or a file on disk is not a formal quality decision.
- Do not commit model weights, Hugging Face caches, access tokens, personal credentials, or machine-specific paths.

## Local environment

Python 3.12 is recommended:

```bash
python3.12 -m venv .venv-provider-compat
.venv-provider-compat/bin/python -m pip install --upgrade pip
.venv-provider-compat/bin/python -m pip install -r requirements-provider-compat.txt
```

For tests that do not load models, a smaller test dependency set is enough:

```bash
.venv-provider-compat/bin/python -m pip install -r requirements-test.txt
```

## Verify your change

Before you submit, run at least:

```bash
.venv-provider-compat/bin/python -m unittest discover -s tests -v
.venv-provider-compat/bin/python -m unittest discover -s migration_tests -v
```

If the change touches evidence format, also recheck existing samples with the matching `tools/verify_*.py` verifier. If the change involves a model run, first establish a unique execution id, a fixed contract, and resource stop-lines. Failure evidence must be kept. Do not auto-retry or overwrite it.

## Commits and pull requests

- Each commit should solve one explainable, verifiable problem.
- In the pull request, state the goal, non-goals, verification commands, results, and any still-open boundary.
- New capabilities must also describe the input contract, output evidence, fail-closed behavior, and how they relate to existing authority boundaries.
- Do not make checks green by deleting failure records, rewriting evidence, or relaxing thresholds.

## Reporting issues

Ordinary defects and feature requests can use GitHub issues. Do not open a public issue for an unfixed vulnerability. Follow the private disclosure process in [`SECURITY.md`](SECURITY.md).
