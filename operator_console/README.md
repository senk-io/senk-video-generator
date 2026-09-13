# senk-video-generator local operator console

This directory is a standalone, machine-local video job control surface. It compiles prompts, generation parameters, resource budgets, and risk confirmation into a versioned job request, then controls the compatibility runner through a four-step flow: preflight, register, exact confirm, start.

The console and the read-only observatory have separate duties:

| Surface | Default URL | Duty |
| --- | --- | --- |
| Operator console | `http://127.0.0.1:4320/` | Define, preflight, register, start, and stop local jobs |
| Build observatory | `http://127.0.0.1:4319/` | Read-only view of stages, resources, logs, outputs, and evidence |

The console creates non-authoritative local execution requests. Job registration, a successful run, or a video file on disk is not quality acceptance, candidate selection, a release decision, a formal fact, or an institution freeze.

## 1. Current capability

- `Wan2.1-T2V-1.3B`: selectable and startable, but a high-memory-risk path
- `CogVideoX-2B`: shows cache and runnability facts, but has no independent run observation on the current Mac, so start is blocked
- `Seedance 2.0 / BytePlus ModelArk`: selectable for a no-cost preflight; the console does not register or start billed jobs and does not write `ARK_API_KEY` into requests or frontend state
- `MiniMax H3 / Open Platform V2`: selectable for a no-cost preflight; the console does not register or start billed jobs and does not write `MINIMAX_API_KEY` into requests or frontend state
- Text-to-video: attached; needs a prompt only, no image or video asset
- Image-to-video: not attached; needs an asset and is disabled in the UI
- Video transform: not attached; needs an asset and is disabled in the UI

The console defaults to the frozen "memory probe" profile, a staged-residency strategy, and a `75%` MPS recommended working-set cap. Generation parameters cannot be mixed item by item. The profile freezes them as a set so a request that looks cheap cannot drift into a high-memory combination after registration.

A complete `CogVideoX-2B` model cache means only that download closed. It does not mean the pipeline can load, enter Metal, or finish inference. The console does not promote a download result into run authorization.

## 2. Install

The console reuses the provider-compatibility environment and needs no frontend build toolchain. From the repository root:

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

Model install, fixed-revision download, and cache checks are in [`../docs/provider-compatibility-trials.md`](../docs/provider-compatibility-trials.md). Model weights are not in this repository.

## 3. Start

Start the console from the repository root:

```bash
.venv-provider-compat/bin/python -m operator_console --open
```

Omit `--open` if you do not want the default browser to launch:

```bash
.venv-provider-compat/bin/python -m operator_console
```

To watch the full build at the same time, start the observatory in another terminal:

```bash
.venv-provider-compat/bin/python -m observatory --open
```

Custom console port:

```bash
.venv-provider-compat/bin/python -m operator_console --port 5320
```

`Ctrl+C` stops only the control service. It does not automatically send a stop signal to an already started job. To stop an active job, use the page stop button first. After an unexpected control-service exit, restart it and reconcile or stop still-matching processes.

## 4. How to start a job

1. Choose a provider. The current executable local path is `Wan2.1-T2V-1.3B`. Choosing `Seedance` or `MiniMax H3` only allows a no-cost preflight; billed jobs cannot be registered or started.
2. Choose a job type. Only text-to-video is available, so no asset upload is needed.
3. Enter a prompt and check the auto-generated execution id.
4. Choose a frozen generation profile. The first run should use "memory probe". Resolution, frame count, steps, guidance, and frame rate are locked by the profile.
5. Keep the recommended "staged residency" strategy. Check the MPS cap, start memory, pre-start existing swap, in-run stop threshold, and maximum added-swap budget.
6. Confirm the high-memory risk and click "run preflight".
7. Only after every check passes can you click "register immutable job".
8. After registration, type the full execution id shown on the page again.
9. Click "confirm and start". Only then is a real model process created.
10. Watch status on the right-hand job card, or open the `4319` observatory for resources and evidence formation.

Preflight does not load a model and does not generate video. Registration only persists an immutable request and also does not load a model. Only the last exact-confirm step starts a real execution.

### 30-second pilot entry

The top of the page shows six 5-second shots. Clicking "prepare this shot" freezes the project id, shot id, project-contract digest, and prompt digest. Editing the frozen prompt fail-closes preflight. After a job completes you must still type the full shot id to select a candidate. Structural assembly opens only after all six shots have a current selection. Full notes are in [`../docs/30-second-pilot.md`](../docs/30-second-pilot.md).

## 5. Prompts and assets

The generation input for the current text-to-video job is the prompt. Useful contents include:

- Subject and its action
- Environment, time, and light
- Camera position, motion, and pace
- Picture constraints, such as no text, watermark, or extra people

Example:

```text
一艘纸船在雨后水面缓慢前行，低机位跟拍，柔和晨光，无文字。
```

Do not choose an asset for text-to-video today. When image-to-video and video transform are attached later, the console will add constrained asset-reference fields for those job types. Until then, those job types fail closed.

## 6. Job states

| State | Meaning |
| --- | --- |
| `REGISTERED` | Immutable request registered, not started |
| `STARTING` | Start checks passed; the execution process is being created |
| `RUNNING` | The matching execution process is running |
| `STOP_REQUESTED` | The local operator requested a safe stop |
| `STOPPED` | The stop request has closed |
| `COMPLETED` | The runner observed output and exited normally |
| `FAILED` | Start, resource safety, or execution reality did not form usable output |

After a control-service restart, active jobs are reconciled from process identity, creation time, command line, and evidence digest. The service does not kill arbitrary system processes from a process id alone.

## 7. Resource guards

Default budget:

| Guard | Default | Behavior |
| --- | --- | --- |
| Minimum available memory before start | `16 GiB` | Blocks register or start when short |
| Maximum existing swap before start | `4 GiB` | Blocks register or start during the high-swap recovery window after a trial |
| Minimum available memory while running | `3 GiB` | Stops the job after about `3` continuous seconds below the threshold |
| Maximum added swap | `8 GiB` | Stops the job when growth from job start exceeds the budget |
| MPS process memory cap | `75%` of recommended working set | Calls PyTorch's process-level MPS cap before model load; adjustable from `50%` to `90%` |
| Maximum execution time | `3600` seconds | The runner ends the execution on timeout |

The UI may adjust the budget inside a frozen safety range. An in-run stop is an evidenced terminal state. It does not delete existing logs, samples, or partial output.

### Frozen generation profiles

| Profile | Parameters | Use |
| --- | --- | --- |
| Memory probe | `256×144`, `9` frames, `1` step | First memory-boundary check |
| Quality probe | `256×144`, `9` frames, `4` steps | Keep the lowest canvas; raise steps only to find a recognizability/cost balance |
| Balance probe | `256×144`, `9` frames, `16` steps | If the quality probe is still unrecognizable, search the lowest recognizable profile by geometric increase |
| Recommended balance | `256×144`, `9` frames, `8` steps | Lowest recognizable profile already verified on the current Mac, and the console default |
| Low-memory generation | `416×240`, `9` frames, `4` steps | Short-video trial after the probe closes |
| Existing compatibility baseline | `416×240`, `17` frames, `4` steps | Comparison against existing high-memory evidence only |

### Execution strategies

"Staged residency" first loads the roughly `21 GiB` text encoder alone. Inside `torch.inference_mode()` it uses leaf-order offload so only the submodule needed for the current compute enters MPS. That avoids moving the whole text encoder at once and retaining autograd intermediates. After prompt embeddings are formed, it releases the encoder immediately, then loads the roughly `5.3 GiB` Transformer and roughly `484 MiB` VAE. Denoise and decode continue to use Diffusers' model-level CPU offload hooks. After inference it actively releases hooks, drops pipeline references, runs garbage collection, and clears the MPS cache. "Full residency baseline" remains as a comparison path, but it moves the complete pipeline into MPS and is not the default.

The MPS cap is for fail-fast and process-allocation limiting. It is not hard isolation of whole-system memory or swap. Use it together with pre-start available memory, pre-start existing swap, the in-run stop threshold, and the maximum added-swap guard. Even after available memory recovers, the console still shows a recovery state and blocks new jobs while existing swap is above budget.

## 8. Local records and evidence

Control state defaults to:

```text
.senknet/operator/jobs/<job-id>/
├── request.json
├── status.json
├── events.jsonl
└── launcher.log
```

- `request.json` is the immutable job request; `status.json` stores a recoverable state projection
- `events.jsonl` is an append-only event chain with predecessor digests
- `launcher.log` stores control-layer start logs
- `.senknet/operator/` is Git-ignored so local job history is not committed by mistake

Real run evidence still writes to:

```text
evidence/runtime/<execution-id>/
```

The job-spec digest enters runtime-environment evidence so the console request and the runner reality can be checked against each other.

Controlled-job evidence also records the frozen generation profile, the requested execution strategy, the recommended and actual MPS-cap ratios, strategy-activation results, inference peaks, and MPS allocation after active release. The independent verifier checks these fields. A missing or inconsistent field keeps the package from passing.

## 9. Local API

```text
GET  /api/v1/health
GET  /api/v1/operator
GET  /api/v1/jobs/<job-id>
POST /api/v1/preflight
POST /api/v1/jobs
POST /api/v1/jobs/<job-id>/start
POST /api/v1/jobs/<job-id>/stop
POST /api/v1/pilots/<project-id>/shots/<shot-id>/select
POST /api/v1/pilots/<project-id>/assemble
```

Every write endpoint requires the `X-Senknet-CSRF` token obtained by the page session. The API is not a remote job service and has no public-internet identity system.

## 10. Security boundary

- Bind only `127.0.0.1`, `::1`, or `localhost`
- Do not bind `0.0.0.0` or a LAN address
- Static files and job paths are directory-bounded
- Write endpoints require a local session token
- Request bodies have size limits; job fields have range and type constraints
- Dynamic preflight runs again before start so machine reality after registration cannot silently drift
- Start requires a second confirmation of the full execution id
- Stop reconciles process id, creation time, run script, and execution id
- The page uses local assets and a content-security policy; it loads no external scripts

Do not forward the local port to the public internet. Do not upload records under `.senknet/operator/` that may contain prompts.

## 11. Verification

Console tests only:

```bash
.venv-provider-compat/bin/python -m unittest tests.test_operator_console -v
```

All tests:

```bash
.venv-provider-compat/bin/python -m unittest discover -s tests -v
```

Console tests use a temporary fake executor and do not load models. Pilot tests use local media tools to generate tiny solid-color clips. They only verify contracts, digest chains, and exact 30-second assembly; they do not call a generation model. Coverage includes frozen profiles, text-encoder leaf-order offload and early release, exception-traceback escape, the MPS cap, both residency strategies, active-release evidence, the high-swap recovery gate, request ranges, immutable registration, the event digest chain, second confirmation, stop races, pilot binding, human selection, structural assembly, dynamic preflight, session tokens, path traversal, loopback bind limits, and Seedance / MiniMax H3 remote-preflight wiring (no key, no network, console billed execution forbidden).

## 12. Troubleshooting

### The page says the model cache is not ready

Download the fixed revision from the provider guide and confirm the cache has no incomplete files. Do not bypass the exact-revision requirement by weakening the check.

### Available memory is insufficient

Close other high-memory tasks, wait for swap pressure to recover, then run preflight again. Do not lower thresholds to values that do not match machine reality just to pass preflight.

### The execution id is already used

Click "generate new id". Both the console and the runner refuse to overwrite an existing evidence directory.

### After a control-service restart the job still shows running

The page reconciles the matching process. If the process still exists, keep watching or use the stop button. If the process is gone, status reconverges to a terminal state from existing evidence.

### CogVideoX cannot start

This is the current expected behavior. First establish load, Metal-transfer, and inference evidence through an independently authorized, low-memory real run, then revise the provider capability state.
