# senk-video-generator

> Managed by SENK. Provides a unified, verifiable, correctable, and auditable production process for Seedance, local open-source models, and other video capabilities.

[![License](https://img.shields.io/github/license/senk-io/senk-video-generator)](LICENSE)
[![Tests](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml/badge.svg?branch=bakboem-dev)](https://github.com/senk-io/senk-video-generator/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Managed by](https://img.shields.io/badge/Managed%20by-SENK-111111)
![Architecture](https://img.shields.io/badge/Architecture-provider--neutral-7C3AED)
![Adapters](https://img.shields.io/badge/Adapters-Seedance%20%7C%20local%20models-0284C7)
![Stage](https://img.shields.io/badge/Stage-5s%20shot%20candidates-2EA44F)

## What this project is

`senk-video-generator` is a provider-neutral video production project managed by SENK. SENK is the company that owns the project; it is not a video model, provider, or protocol. The project isolates provider-specific protocols behind `ProviderAdapter` and can attach Seedance, Veo, Kling, Runway, local open-source models, and future video capabilities. Models generate candidate frames. This project owns contracts, resource guards, evidence, deterministic post-processing, and state boundaries.

```text
Creative intent -> provider-neutral shot contract -> ProviderAdapter -> any model -> verification and correction -> human review -> timeline
```

A finished generation is not a quality pass. A candidate on disk is not a timeline binding.

## Model boundary

- High-quality models such as Seedance are formal capability-provider candidates. The adapter layer only compiles their requests and results; it does not change upstream governance semantics.
- Current reference adapters include local `CogVideoX-2B` and `Wan2.1-T2V-1.3B`, the remote `MiniMax-H3` Open Platform `V2` API, and the remote `Seedance` / BytePlus ModelArk `v3` API. Runtime backends, cost, resource, and evidence contracts stay independent per provider.
- Local small models exist to validate controlled generation, resource stop-lines, evidence closure, post-processing, and human selection at low cost. They do not define the project's model ceiling or final image-quality target.

### MiniMax H3 adapter

`MiniMax-H3` is attached as an independent `ProviderAdapter`. The current `36GB` Apple Silicon machine does not load public weights: the official `BF16` base model includes a `33B` dense video transformer and a full `Qwen3-VL-32B` encoder; the official `ComfyUI` text-to-video quantized stack is still about `39.55 GiB`, and this repo has no verified on-machine `MPS` quantized-operator path. The first effect trial therefore uses the official remote `V2` API and does not download weights.

Write real secrets only to an untracked `.env`:

```bash
cp .env.example .env
# Fill MINIMAX_API_KEY in .env
set -a
. ./.env
set +a
```

The default command is a no-cost preflight. A billed job is submitted only when `--execute` is added explicitly:

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial

.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial \
  --execute \
  --execution-id MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ

.venv-provider-compat/bin/python -m tools.verify_minimax_h3_evidence \
  evidence/runtime/MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

The fixed trial produces a `768P`, `5` second, `16:9`, `24 fps` candidate with `32 kHz` stereo audio. Automatic checks only confirm the technical contract and evidence closure. Crying semantics, visible rolling tears, identity continuity, and audio-visual emotional sync still require human review.

The operator console already lists MiniMax H3 as a remote provider. Selecting it runs a no-cost preflight. The console does not submit billed jobs and does not write `MINIMAX_API_KEY` into job requests, logs, or frontend state. Explicit billing still requires the CLI `--execute` path above.

### Seedance / BytePlus ModelArk adapter

`dreamina-seedance-2-0-260128` is attached as an independent `ProviderAdapter` for the [BytePlus ModelArk video generation API](https://docs.byteplus.com/en/docs/modelark/1520757). The adapter only compiles requests and results. It does not change upstream governance semantics and does not create quality acceptance, selection, timeline binding, or institution freeze.

Write real secrets only to an untracked `.env`:

```bash
cp .env.example .env
# Fill ARK_API_KEY in .env. Do not commit the real value to Git.
set -a
. ./.env
set +a
```

The default command is a no-cost preflight. A billed job is submitted only when `--execute` is added explicitly. Tests and preflight never call the live API. If the key is missing, preflight fail-closes and creates no empty evidence:

```bash
.venv-provider-compat/bin/python -m tools.run_seedance_trial

.venv-provider-compat/bin/python -m tools.run_seedance_trial \
  --execute \
  --execution-id SEEDANCE-CLOSEUP-YYYYMMDDTHHMMSSZ

.venv-provider-compat/bin/python -m tools.verify_seedance_evidence \
  evidence/runtime/SEEDANCE-CLOSEUP-YYYYMMDDTHHMMSSZ
```

The fixed trial produces a `720p`, `5` second, `16:9`, `24 fps` candidate and requests native audio with no watermark. Automatic checks only confirm the technical contract and evidence closure. Crying semantics, visible rolling tears, identity continuity, and audio-visual emotional sync still require human review. Secrets, signed download URLs, and authorization headers never enter evidence.

The operator console already lists Seedance as a remote provider. Selecting it runs a no-cost preflight. The console does not submit billed jobs and does not write `ARK_API_KEY` into job requests, logs, or frontend state. Explicit billing still requires the CLI `--execute` path above.

### One-sentence shot planning

A local text model can first turn one sentence of creative intent into a non-authoritative scene, narrative-beat, and shot draft. A deterministic observer then checks source-sentence coverage, stable identifiers, explicit semantics, single-shot purpose, subject references, duration, and continuity. The current reference contract splits each round into seven flat stages: `scene_context`, `beat_purpose`, `shot_core`, `composition`, `performance`, `lighting`, and `continuity`. Three rounds make twenty-one local calls with no automatic retry. Scene roles, composition, performance, lighting, and continuity marks are expanded by the system from a versioned contract. Observable checks are derived deterministically from request constraints and selected marks. Repeated runs report structural agreement and controlled-semantic agreement separately. They never auto-create a formal `ShotSpec` or a quality decision.

The default single-request command still keeps the evidenced `v7` crying-closeup baseline. Generality observations use a versioned `request.v2`, a neutral subject lexicon, and a three-case suite so stability on one request is not mistaken for cross-request understanding. Evidenced `v11` first locks facts that are explicit in the source sentence with a fail-closed deterministic extractor; the model may emit only residual fields. The rain-crying, indoor-smile, and bicycle cases lock `9`, `11`, and `9` fields respectively. All `63/63` local calls and `9/9` strict-parse rounds completed, and the model never wrote locked fields. Retained observations dropped from `120` in `v10` to `93`, but residual scene-continuity, composition, lighting, and action-continuity choices still left `0/9` structurally observable drafts. This `0.6B` path therefore remains diagnostic observation only and cannot auto-approve shots.

Later `v12` only tightens the deterministic boundary: it adds a separate extractor `v2` that keeps recomputable polarity decisions for each lexical hit. An explicit negation that hits a registered controlled lexeme or guard stem, and that has no controlled same-field positive replacement, blocks before evidence is written and before the model is called. It can no longer be handed to the model as a residual field to guess. Controlled “而是/反而/改用” corrections, affirmative idioms, subject/camera crossover, and “固定相机参数” have additional fixed boundaries. `v11` stays permanently bound to extractor `v1`; existing evidence is not reinterpreted under the new semantics. `v12` now has the three-case guarded trial contracts, the 63-call generalization suite, and two held-out trial contracts. Those files are wiring only. There is still no live-model suite run, no structurally observable 9/9 observation, and no quality-improvement claim. Held-out placeholders stay `DRAFT_NON_AUTHORITATIVE` and do not count toward the planning gate.

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite \
  --suite experiments/shot_planning/qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --contract experiments/shot_planning/qwen3_0_6b_guarded_source_facts_smile_trial_v12.json
```

The full contract and the three-run comparison method are in the [one-sentence shot planning draft](docs/one-sentence-shot-planning.md).

## Local reference observations

| Capability | Current observation |
| --- | --- |
| Memory optimization | In the CogVideoX eight-step same-parameter comparison, the MPS driver peak dropped about `63.884%`, and added swap was `0` |
| Five-second generation | Completed a `41`-frame source generation and derived a `40`-frame, `8 fps`, exact `5.000` second candidate |
| Semantic continuity | Every frame kept the red origami boat, water, reflection, and main crease |
| Direction control | The second shot netted about `116.30` pixels to the right; all `39` adjacent displacements were rightward, with no ghosting or edge seams |
| Automatic regression | `161` unit tests and `1` migration test passed. The tests themselves do not download or run models |

These results show that a controlled generation process can close. They do not mean the local small model is the only runtime path, and they are not a formal visual-quality acceptance.

## Quick start

The following steps reproduce the current local MPS reference implementation. They require an Apple Silicon Mac with MPS, macOS, and Python `3.12`. Current evidence used Python `3.12.11`.

```bash
git clone git@github.com:senk-io/senk-video-generator.git
cd senk-video-generator
python3.12 -m venv .venv-provider-compat
.venv-provider-compat/bin/python -m pip install --upgrade pip
.venv-provider-compat/bin/python -m pip install -r requirements-provider-compat.txt
```

For tests only, a smaller dependency set is enough:

```bash
.venv-provider-compat/bin/python -m pip install -r requirements-test.txt
.venv-provider-compat/bin/python -m unittest discover -s tests -v
.venv-provider-compat/bin/python -m unittest discover -s migration_tests -v
```

## Local interfaces

```bash
.venv-provider-compat/bin/python -m operator_console --open
.venv-provider-compat/bin/python -m observatory --open
```

- Operator console: `http://127.0.0.1:4320/`
- Read-only observatory: `http://127.0.0.1:4319/`

Both services may bind loopback only. The console owns controlled jobs. The observatory only reads state; it does not start models or create quality decisions.

## Run a controlled probe

The CogVideoX commands below are a local reference probe. Before a real model run, read [provider compatibility trials](docs/provider-compatibility-trials.md), confirm no leftover generation processes, and check the memory and swap stop-lines in the contract.

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-LOCAL-PROBE-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_8_steps.json

.venv-provider-compat/bin/python -m tools.verify_provider_compatibility_evidence \
  evidence/runtime/LM-COGVIDEOX-LOCAL-PROBE-YYYYMMDDTHHMMSSZ
```

Each execution id may be used only once. Success and failure evidence are both kept under `evidence/runtime/<execution-id>/`. A passing check means only that the evidence package is auditable. It does not mean picture quality has passed.

## Layout

| Path | Contents |
| --- | --- |
| `foundation/`, `execution/`, `video/` | Governance, the execution loop, and the video domain model |
| `operator_console/`, `observatory/` | Local operator console and read-only observatory |
| `provider_adapters/` | Isolation layer for local or remote provider protocols |
| `tools/`, `experiments/` | Execution tools, derivation tools, and fixed trial contracts |
| `evidence/runtime/` | Recheckable success and failure evidence samples |
| `tests/`, `migration_tests/` | Regression tests that do not load models |

## Documentation

- [Project vision](foundation/00_ProjectVision.md)
- [Governance](foundation/02_Governance.md)
- [Evidence model](foundation/05_Evidence.md)
- [Provider compatibility and Mac observations](docs/provider-compatibility-trials.md)
- [One-sentence shot planning draft](docs/one-sentence-shot-planning.md)
- [30-second pilot workflow](docs/30-second-pilot.md)
- [Operator console](operator_console/README.md)
- [Observatory](observatory/README.md)

## Open-source boundary

Model weights and the Hugging Face cache are not in this repository and must not be committed to Git. Access credentials for Seedance and other external capabilities must also stay out of the repository. Users must separately follow the licenses and use conditions of the models, services, dependencies, and generated content they use.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before contributing. Report security issues privately using [`SECURITY.md`](SECURITY.md). Project code and repository documentation are licensed under [`Apache-2.0`](LICENSE).
