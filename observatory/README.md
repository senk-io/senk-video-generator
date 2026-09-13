# senk-video-generator local build observatory

This directory is a complete, read-only, machine-local video-build observation surface. It projects the project's existing model cache, execution state, resource samples, logs, outputs, and evidence packages into a live page so developers can understand current reality without opening many JSON, JSONL, and log files.

The observatory does not start models, modify evidence, retry, create decisions, or promote "a file exists" into a formal fact or institution freeze.

To define prompts and resource budgets from a page and explicitly start or stop jobs, use the separate [`../operator_console/README.md`](../operator_console/README.md). The console defaults to `http://127.0.0.1:4320/`. This observatory stays read-only.

## 1. Scope

- Auto-discover running and historical provider trials
- Show the eight stages: execution registration, environment forensics, model snapshot, pipeline load, Metal transfer, inference, export, and evidence closure
- Refresh CPU, unified memory, swap, and disk every second
- Plot process-tree memory, system memory, swap, and MPS allocation trends
- Show exact revisions, cache size, snapshot files, and incomplete files for Wan2.1 and CogVideoX
- Preview thumbnails and video output that have already formed
- Inspect the frozen request, dependency environment, active processes, and filterable run logs
- Inspect the manifest, evidence files, formal-fact, cross-provider-contract, and institution-freeze boundaries
- Browse provider-trial, protected-write, correctness, and migration evidence-package history
- Support desktop and narrow-screen layouts

## 2. Install

The observatory reuses the project's compatibility-trial environment and adds no frontend toolchain or server dependency. From the repository root:

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

If the model-compatibility environment is already installed, do not repeat this.

## 3. Start

From the repository root:

```bash
.venv-provider-compat/bin/python -m observatory --open
```

Default URL:

```text
http://127.0.0.1:4319/
```

Omit `--open` if you do not want the default browser to launch:

```bash
.venv-provider-compat/bin/python -m observatory
```

Custom port:

```bash
.venv-provider-compat/bin/python -m observatory --port 5319
```

Press `Ctrl+C` to stop the observatory. The service refuses to bind `0.0.0.0` or a LAN address so local execution logs and resource state are not exposed by accident.

## 4. Watch one build

Terminal 1 starts the observatory:

```bash
.venv-provider-compat/bin/python -m observatory --open
```

Terminal 2 runs an authorized compatibility trial:

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider wan \
  --execution-id CR-0020-WAN-MAC-001
```

The page refreshes every second; no manual reload is needed. A new execution directory is discovered automatically. An active execution becomes the default observation target. Historical executions can be switched from the top selector or the evidence-package history at the bottom.

The execution command itself remains bound by proposal, policy, resource budget, and authorization. Starting the observatory is not generation authorization.

## 5. Status language

| Page state | Meaning | Does not mean |
| --- | --- | --- |
| Building | A matching parent or worker process was detected | Does not mean a final output will form |
| Output observed | The summary records that inference, export, and output have formed | Does not mean video quality passed or was formally adopted |
| Evidence closed | Summary and manifest have formed | Does not mean a formal fact exists |
| No output formed | This execution reality did not form usable output | Does not automatically decide retry or model replacement |
| Waiting or interrupted | The execution directory is unclosed and no matching process is running | Does not automatically prove why a process crashed |
| State unknown | Sources are insufficient to determine current reality | Must not be treated as a pass |

Local resource state considers both immediate available memory and existing swap:

| Resource state | Meaning |
| --- | --- |
| Resources normal | Available memory is sufficient and existing swap is below `4 GiB` |
| Swap recovering | Available memory has recovered, but leftover swap from a trial is still high; new high-memory jobs should stay blocked |
| Memory tight | Available memory is below `18%` of physical memory |
| Memory critical | Available memory is below `8%` of physical memory |

Stage state is derived only from existing files, boolean observations, worker-process stage, and active processes. The observatory writes no extra state into the evidence directory.

## 6. Sources of truth and refresh

| Area | Source of truth | Refresh |
| --- | --- | --- |
| Build stages | `request.json`, `environment.json`, `worker_state.json`, `summary.json`, `manifest.json` | 1 second |
| Process and local resources | `psutil` read-only sampling | 1 second |
| Historical resource curves | `process_metrics.jsonl`, `mps_metrics.jsonl` | 1 second |
| Run logs | last 96 KiB of `runtime.log` | 1 second |
| Output preview | `output.mp4`, `thumbnail.png` | 1-second discovery; the browser reads on demand |
| Model cache | `~/.cache/huggingface/hub/` | 15 seconds |
| All evidence packages | `evidence/runtime/*/summary.json` and `manifest.json` | 1 second |

Long resource series keep at most 420 equally spaced samples for plotting in the API. The original JSONL files are not modified or truncated.

## 7. Local API

```text
GET /api/v1/health
GET /api/v1/dashboard
GET /api/v1/dashboard?execution_id=<EXECUTION_ID>
GET /media/<EXECUTION_ID>/output.mp4
GET /media/<EXECUTION_ID>/thumbnail.png
```

The API is read-only. The video endpoint supports HTTP byte ranges so the browser can seek and play. Execution ids, media filenames, and real paths are whitelist- and directory-bounded.

## 8. Security and privacy

- Loopback is the default and the only allowed bind
- No `POST`, `PUT`, `PATCH`, or `DELETE` business endpoints
- Model-weight contents and cache absolute paths are not returned
- Repository paths, home directories, and common user paths in logs are redacted before return
- The page enables a content-security policy, forbids external scripts, and forbids framing
- All frontend assets live in the repository; there is no CDN
- The observatory does not import PyTorch, load models, or create MPS allocations

The local page may still show frozen prompts, execution logs, and publicly safe evidence summaries. Do not forward the local port to the public internet.

## 9. Verification

Observatory tests only:

```bash
.venv-provider-compat/bin/python -m unittest tests.test_observatory -v
```

All tests:

```bash
.venv-provider-compat/bin/python -m unittest discover -s tests -v
```

Observatory tests cover full state derivation, high-swap recovery state, unclosed executions, model-cache state, log-path redaction, loopback bind limits, the static page, the API, the content-security policy, path-traversal blocking, and ranged media reads.

## 10. Troubleshooting

### System Python reports missing `psutil`

Start with the project virtualenv:

```bash
.venv-provider-compat/bin/python -m observatory
```

### The port is already in use

Choose another local port:

```bash
.venv-provider-compat/bin/python -m observatory --port 5319
```

### The page has no execution record

Confirm the repository has `evidence/runtime/<execution-id>/request.json` and that `request.json` contains a provider object. Governance, correctness, and migration evidence enter the package history but are not shown as video-generation stages by mistake.

### CogVideoX shows a complete cache but no generation history

This is the current correct state: a complete cache means only that model-file download closed. It does not mean the pipeline can load, enter MPS, or finish inference. Generation stages appear on the page only after a real execution creates a new evidence directory.
