# 30-second pilot workflow

This workflow shrinks a long-video goal into a 30-second project that can be verified shot by shot. It does not ask a local model to generate 30 continuous seconds. It freezes six 5-second shots, generates candidates separately, has a human select them, then assembles a timeline.

The first current project is [`PILOT-RED-BOAT-30S-001.json`](../projects/PILOT-RED-BOAT-30S-001.json):

| Shot | Duration | Narrative role |
| --- | ---: | --- |
| `SHOT-001` | 5 s | Establish the red paper boat and the water |
| `SHOT-002` | 5 s | Drift steadily |
| `SHOT-003` | 5 s | Meet a light breeze |
| `SHOT-004` | 5 s | Adjust direction |
| `SHOT-005` | 5 s | Pass through a warm reflection |
| `SHOT-006` | 5 s | Reach the shore |

The project contract is currently `DRAFT_NON_AUTHORITATIVE`. Subject, shots, and prompts can be revised, but a revision changes the contract digest. An already loaded but not-yet-registered old binding fail-closes at preflight so the contract cannot drift silently.

## Install and start

Reuse the provider-compatibility environment:

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

Start the operator console and the read-only observatory:

```bash
.venv-provider-compat/bin/python -m operator_console --open
.venv-provider-compat/bin/python -m observatory --open
```

The console defaults to `http://127.0.0.1:4320/`. The observatory defaults to `http://127.0.0.1:4319/`.

## Shot-by-shot operation

1. In the 30-second pilot card at the top of the page, choose "prepare this shot".
2. The console loads that shot's frozen prompt, shot binding, and a new execution id. No model is loaded at this point.
3. Check the frozen generation profile and resource guards, confirm the high-memory risk, and run preflight.
4. After preflight passes, register the immutable job, then type the full execution id to start.
5. Job completion only means a candidate output exists. Open the job, type the full shot id, and explicitly select it as the current shot.
6. If the candidate is not suitable, prepare the same shot again and form a new candidate. A new selection appends to selection history and does not overwrite old records.
7. After all six shots have a current selection, type the full project id and assemble the structural pilot.

A failed job does not invalidate other shots. Candidates, selection history, and execution evidence that already formed are kept, so work can continue from the failed shot.

## States and records

Shot states:

| State | Meaning |
| --- | --- |
| `PLANNED` | A shot contract exists; no job yet |
| `GENERATING` | A job is registered or executing |
| `CANDIDATES_READY` | At least one job formed output; no human selection yet |
| `RETRY_AVAILABLE` | Existing attempts did not form a usable candidate; retry is allowed |
| `SELECTED` | The local operator explicitly selected the current candidate |

Local run state lives at:

```text
.senknet/operator/
├── jobs/<job-id>/
└── pilots/<project-id>/
    ├── selections.jsonl
    ├── latest_assembly.json
    └── assemblies/<assembly-id>/
```

`selections.jsonl` is append-only history with predecessor digests. The assembly manifest records each shot's source job, source digest, source duration, target duration, and loop / crop / scale treatment.

## Quality boundary

The verified balance profile of the current `Wan2.1-T2V-1.3B` only generates about `1.13` second, `256×144` candidates. The assembler can loop a short candidate for a structural preview, normalize it to 5 seconds, and upsample it to the target canvas. Those treatments cannot add real detail and cannot form a quality pass.

The 30-second work therefore has two gates:

1. Structure gate: six shots, exact 30 seconds, traceable sources, and the ability to continue after failure
2. Quality gate: subject continuity, stable motion, no severe deformation, target sharpness, and human viewing confirmation

Only when both the structure gate and the quality gate hold can the pilot be called acceptable. The current implementation may build a structural pilot, but it does not automatically declare acceptance or release.

Current per-shot progress: `SHOT-001` has formed an exact five-second origami candidate and passed the technical continuity thresholds, but still waits for human selection by full shot id. `SHOT-002` has completed a forty-one-frame source probe and a forty-frame spatial-only direction derivation bound to the real digest. The final candidate is `40` frames, `8 fps`, exact `5` seconds, with a first-to-last net rightward displacement of about `116.30` pixels. All thirty-nine adjacent steps are rightward, and the maximum adjacent jump is about `4.86` pixels. Every frame keeps the origami outline, creases, water, and reflection, with no ghosting or edge seams. That result establishes a second-shot technical candidate. It does not automatically create human quality acceptance, formal selection, or timeline binding.

## Shot 002 keyframe auto-adjustment

The default workspace uses [`cogvideox_shot_002_keyframe_adjustment_v2.json`](../experiments/postprocessing/cogvideox_shot_002_keyframe_adjustment_v2.json). The operator only adjusts frames `1`, `10`, `20`, `30`, and `40`. The system expands the following parameters across all forty frames:

- `x_pixels`: positive is right
- `y_pixels`: positive is down
- `scale`
- `rotation_degrees`: positive is clockwise in picture coordinates
- `adjustment_reason`
- `review_status`, reviewer, and review time

The four transform parameters each use monotone cubic interpolation that does not cross keyframe intervals. Keyframe values are kept as written. If an auto-expanded frame is still wrong, add a complete single-frame parameter set in `manual_overrides` to replace the interpolation. The system does not auto-choose keyframes and does not write the contract backward from output.

The current five keyframes are identity transforms with `PENDING_REVIEW`, used to verify the auto-expansion path. Changing a keyframe or a single-frame override requires an adjustment reason. Recording `HUMAN_APPROVED` or `HUMAN_REJECTED` requires a reviewer and a time.

Each render must use a new execution id:

```bash
.venv-provider-compat/bin/python tools/render_keyframe_adjustments.py \
  --execution-id KEYFRAME-SHOT-002-<UNIQUE-ID>
```

The renderer only reads the existing `direction_controlled_5s.mp4`. It does not load or run a model and does not blend pixels across frames. Each derivation creates an independent, overwrite-refusing evidence directory that contains:

```text
expanded_frame_adjustments.json                # 40-frame parameters expanded from 5 keyframes
adjusted_frames/                               # all 40 adjusted frames
keyframe_adjusted_5s.mp4                       # 5-second preview candidate
before_after_keyframe_contact_sheet_40_frames.png
frame_mapping.json                             # parameter source and keyframe intervals
adjustment_summary.json
review_record.json
request.json
environment.json
summary.json
manifest.json
```

After render, interpolation can be independently recomputed and the source, output, forty-frame mapping, and "no formal fact created" boundary can be checked:

```bash
.venv-provider-compat/bin/python tools/verify_keyframe_adjustment_evidence.py \
  evidence/runtime/KEYFRAME-SHOT-002-<UNIQUE-ID>
```

The original [`cogvideox_shot_002_manual_frame_adjustment_v1.json`](../experiments/postprocessing/cogvideox_shot_002_manual_frame_adjustment_v1.json) and `render_manual_frame_adjustments.py` remain as a full per-frame fallback and do not overwrite their existing evidence.

An auto-expansion and a render result do not mean the parameters have human approval. They also do not create formal visual-quality acceptance, shot selection, or timeline binding.

## Verification

Pilot contract, binding, selection-digest-chain, and 30-second assembly tests do not load models:

```bash
.venv-provider-compat/bin/python -m unittest tests.test_pilot_project -v
```

Full tests:

```bash
.venv-provider-compat/bin/python -m unittest discover -v
```
