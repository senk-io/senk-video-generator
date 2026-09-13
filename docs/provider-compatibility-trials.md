# Open-source video model compatibility trials

This guide explains how to reproduce Apple-silicon local compatibility trials for `Wan2.1-T2V-1.3B` and `CogVideoX-2B`, and a controlled remote trial of `MiniMax-H3` Open Platform `V2`. It only verifies that a named backend can complete request, execution, output, and evidence closure. It does not evaluate video quality and does not create a cross-provider institutional contract.

## MiniMax H3 remote effect trial

`MiniMax-H3` was released on `2026-07-31`. Official materials state that it supports a unified text, image, video, and audio context and can output video up to `15` seconds, up to `2K`, with native stereo audio. The current frozen trial uses text input only and the lower `768P`, `5` second, `16:9` parameters, so it can make a limited semantic observation against the existing fictional child-crying close-up candidate. It does not form a strict cost or speed benchmark.

This machine does not execute the public weights. The official full repository has a logical size of about `464.24 GiB`. The official `ComfyUI` text-to-video quantized combination consists of about `19.53 GiB` for the video model, `14.61 GiB` for the text encoder, `4.85 GiB` for the video VAE, and `0.56 GiB` for the audio VAE, about `39.55 GiB` in total. That size already exceeds this machine's `36GB` unified memory, and the `NVFP4/AWQ` text encoder has no `MPS` execution path verified by this project. Do not try your luck by downloading weights or relaxing the swap budget.

Official sources:

- [MiniMax H3 release notes](https://minimaxi.com/blog/minimax-h3)
- [MiniMax H3 public weights repository](https://github.com/MiniMax-AI/MiniMax-H3)
- [MiniMax H3 Open Platform V2 API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [ComfyUI MiniMax H3 workflow](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)

The frozen contract is at:

```text
experiments/provider_compatibility/minimax_h3_fictional_child_crying_closeup_v1.json
```

First put the key in an untracked `.env` and load it in the current terminal. The adapter only checks whether `MINIMAX_API_KEY` exists. It does not record the value in any output, log, or evidence:

```bash
cp .env.example .env
# 编辑 .env，填写 MINIMAX_API_KEY
set -a
. ./.env
set +a
```

By default this only runs a no-cost preflight and does not submit a task:

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial
```

After preflight passes, you must explicitly add `--execute` and a new execution id before a billed task is submitted:

```bash
.venv-provider-compat/bin/python -m tools.run_minimax_h3_trial \
  --execute \
  --execution-id MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

The adapter always connects to `https://api.minimax.io`, calls `/v2/video_generation`, polls `/v2/query/video_generation/{task_id}`, and immediately downloads the temporary output URL after success. Signed download URLs and authorization headers do not enter evidence. The automatic technical gate requires the output short side to be `768` pixels, about `5` seconds, `24 fps`, and to include `32 kHz` stereo audio.

If local polling fails or times out before the remote task reaches a terminal state, the adapter calls `/v2/video_generation/{task_id}` to attempt cancellation and writes the result to `cancellation_attempt.json`. The official API only allows queued tasks to be cancelled; a running task may refuse cancellation. Closing the local terminal therefore does not mean cloud execution has stopped. Actual cost bounds must be judged from cancellation evidence or a later queried terminal state.

Independent verification:

```bash
.venv-provider-compat/bin/python -m tools.verify_minimax_h3_evidence \
  evidence/runtime/MINIMAX-H3-CLOSEUP-YYYYMMDDTHHMMSSZ
```

A successful verification only means the model identifier, request parameters, task terminal state, media technical attributes, file digest, evidence closure, and credential scan are consistent. The fictional child close-up, crying semantics, a clearly rolling tear, lower-lip tremor, identity continuity, a safe performance context, breathing or sobbing sound, and audio-visual sync all remain frame-by-frame and human creative review. The generation adapter must not judge them as passing.

## 1. Run boundary

The frozen trial contract is at:

```text
experiments/provider_compatibility/trial_contract.json
```

Both models share the same English prompt and random seed. English is used because the official `CogVideoX-2B` model card states that prompt input supports English only. The first trial reduces frame count and denoise steps to control time and memory. These parameters cannot be used as a formal quality baseline.

The frozen contract requires model-level staged residency, a `65%` MPS recommended working-set cap, at least `5 GiB` available memory while running, and at most `4 GiB` added swap. When available memory stays below budget or swap growth exceeds budget, the parent process asks the child to save stop evidence and release resources.

Model weights come from the model publisher and are not in this repository. The default cache location is managed by `huggingface_hub`, usually `~/.cache/huggingface/hub/`. The evidence package records only the model identifier, snapshot revision, parameters, stages, resource observations, and output digest. It does not record the local username, serial number, or a unique hardware identifier.

## 2. Prerequisites

- Apple-silicon Mac;
- macOS with Metal support;
- At least tens of GiB of free disk for the two model caches;
- `uv` installed;
- Access to Hugging Face public model repositories;
- Other high-memory tasks closed during the run.

This round of dependencies is frozen on `Python 3.12.11`. Do not use system Python, and do not commit the virtual environment or model weights to Git.

## 3. Install path

From the repository root:

```bash
uv venv --python 3.12.11 .venv-provider-compat
uv pip sync \
  --python .venv-provider-compat/bin/python \
  requirements-provider-compat.txt
```

Verify the Metal backend and both model pipelines:

```bash
.venv-provider-compat/bin/python - <<'PY'
import torch
from diffusers import CogVideoXPipeline, WanPipeline

print(torch.__version__)
print(torch.backends.mps.is_built())
print(torch.backends.mps.is_available())
print(WanPipeline.__name__)
print(CogVideoXPipeline.__name__)
PY
```

Expect both the `mps` built and available states to be `True`. If either is `False`, do not continue downloading models. First check that you are using native `arm64` Python, macOS, and PyTorch versions.

## 4. Download models only, do not generate

Download and generation are two different stages. To prefetch weights only, use the commands below. They import `huggingface_hub` only. They do not import PyTorch, do not build a model pipeline, and do not use Metal.

Wan2.1:

```bash
HF_HUB_DISABLE_TELEMETRY=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download(
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    revision="0fad780a534b6463e45facd96134c9f345acfa5b",
))
PY
```

CogVideoX:

```bash
HF_HUB_DISABLE_TELEMETRY=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download(
    "zai-org/CogVideoX-2b",
    revision="1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
))
PY
```

After download, you can confirm the exact snapshots offline. This check does not load the models:

```bash
HF_HUB_OFFLINE=1 \
  .venv-provider-compat/bin/python - <<'PY'
from huggingface_hub import snapshot_download

models = {
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers": "0fad780a534b6463e45facd96134c9f345acfa5b",
    "zai-org/CogVideoX-2b": "1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
}
for model_id, revision in models.items():
    print(snapshot_download(model_id, revision=revision, local_files_only=True))
PY
```

The paths printed by those commands should sit under `snapshots/<revision>/` in the Hugging Face cache. Do not copy model weights from that path into the project repository.

## 5. Run a full compatibility trial

The commands below actually load the models and generate video. Memory demand is far higher than download-only. On the current 36GB unified-memory Mac, a Wan2.1 measurement once pushed Metal driver allocation to about 30.98GB and increased system swap by about 23.39GB. Read the measured record in section 8 before running, and close other high-memory tasks.

For everyday local operation, prefer the standalone operator console. It runs a resource preflight, registers an immutable request, and requires you to type the full execution id again before a real start:

```bash
.venv-provider-compat/bin/python -m operator_console --open
```

The console defaults to `http://127.0.0.1:4320/`. Full notes are in [`../operator_console/README.md`](../operator_console/README.md). Only the Wan2.1 text-to-video path is currently allowed to start. CogVideoX has formed minimum denoise and independent small-tile decode evidence, but has not yet formed an integrated low-memory job and quality acceptance, so the console continues to fail closed.

The first low-memory verification should keep these defaults:

```text
Generation profile: wan_probe
Execution strategy: mps_model_offload_bounded
MPS recommended working-set ratio: 0.75
Parameters: 256×144, 9 frames, 1 step, 8 fps
```

When the memory probe succeeds but the picture is unrecognizable, the next profile is `wan_quality_probe`: keep `256×144`, `9` frames, and the same prompt, and raise inference steps only to `4`. This step isolates the effect of step count on quality and elapsed time. Do not raise resolution at the same time before this step has formed a real observation.

The console writes these values into an `operator-job.v4` job request. Before start, at least `16 GiB` available memory and no more than `4 GiB` existing swap must both be satisfied. The runner first sets the process-level MPS cap, then loads the text encoder alone. In no-gradient inference mode it uses leaf-order offload to form prompt embeddings and then releases them, and only after that loads the Transformer and VAE. After inference it releases hooks, pipeline references, and the MPS cache. Run evidence records the limit configuration, component residency strategy, text-encoder release, MPS peak, and final release separately. You cannot assert that the strategy took effect from the page selection alone.

To watch stages, memory, swap, MPS, logs, and evidence formation live in a browser, first start the read-only observatory in another terminal:

```bash
.venv-provider-compat/bin/python -m observatory --open
```

Full observatory notes are in `observatory/README.md`. It does not start or control a trial. The lower-level command-line path still requires independent explicit authorization and does not replace the console's risk-confirmation experience. The commands below without a job spec read the frozen compatibility contract. They have the MPS ratio, in-run available-memory and added-swap limits, and Wan-specific early text-encoder release, but they do not run the console's pre-start swap-recovery gate. They are only for independent compatibility evidence and should not be the everyday generation entry.

Wan2.1:

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider wan \
  --execution-id CR-0019-WAN-MAC-001
```

CogVideoX:

```bash
.venv-provider-compat/bin/python \
  tools/run_provider_compatibility_trial.py \
  --provider cogvideox \
  --execution-id CR-0019-COGVIDEOX-MAC-001
```

CogVideoX frozen eight-step quality probe:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-8STEP-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_8_steps.json
```

The sixteen-step comparison uses `cogvideox_quality_16_steps.json` and a new execution id. The thirty-two-step material and rain-scene probe uses `cogvideox_quality_32_steps.json`, still keeping nine frames and all frozen inputs, and raising inference steps only:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps.json
```

The three nine-frame controlled contracts allow only inference steps to change relative to the four-step baseline. Model snapshot, prompt, seed, canvas, frame count, guidance scale, frame rate, and resource budget stay unchanged. They only establish quality observations. They do not automatically create quality acceptance or console start permission. The thirty-two-step contract also explicitly forbids generating five seconds directly or entering a thirty-second timeline.

After the thirty-two-step frozen prompt still did not form clear creases, the origami-prompt comparison uses an independent contract. It only changes the subject description in the prompt to folded paper craft and clear triangular creases. Steps, seed, nine-frame canvas, and all resource bounds stay unchanged:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-ORIGAMI-QUALITY-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps_origami_prompt.json
```

This contract still allows nine-frame output only and does not automatically generate five seconds. Only after origami structure, subject semantics, and scene semantics close frame by frame can a new forty-one-frame resource contract be created separately.

After the nine-frame origami gate passes, the five-second origami candidate uses the independent contract `cogvideox_five_second_32_steps_origami.json`. The contract keeps the `65%` MPS cap, the at-least-`5 GiB` available-memory stop-line, and the at-most-`4 GiB` added-swap stop-line, and forbids automatic retry:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-32STEP-ORIGAMI-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_32_steps_origami.json
```

That contract generates a `41`-frame source output, then trims it to `40` frames, `8 fps`, exactly `5` seconds. If the subject centroid still exceeds the existing stability threshold, new evidence may only be derived with `cogvideox_origami_temporal_stability_v1.json` bound to the source digest. The source must not be modified and the model must not be rerun.

After the nine-frame staged strict comparison closes, the five-second candidate observation uses the independent contract `cogvideox_five_second_16_steps.json`. That contract freezes the sixteen-step quality baseline, `41`-frame source output, the `65%` MPS cap, the at-least-`5 GiB` available-memory stop-line, and the at-most-`4 GiB` added-swap stop-line. Only after the source output has fully formed does the runner derive `derived_5s.mp4` at `40` frames, `8 fps`, exactly `5` seconds, using `DROP_LAST_FRAME`:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-16STEP-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_16_steps.json
```

The five-second contract allows only a single controlled execution. On failure it keeps evidence and does not retry automatically. Success also produces only a candidate observation. It does not create formal quality acceptance, console permission, a cross-provider contract, an institution freeze, or a thirty-second timeline. Before running you must still independently confirm that no generation process is present, that memory pressure is normal, and that a swap baseline is recorded.

When an existing five-second candidate shows subject-position jitter, you can form an independent technical-stability candidate with the frozen derivation contract `cogvideox_temporal_stability_v1.json` without rerunning the model and without modifying the source evidence. The contract locks the source video digest, translates along the straight path between the first- and last-frame red-subject centroids in integer pixels, uses replicate fill at the edges, then applies a symmetric three-frame blend with weights `1:4:1`:

```bash
.venv-provider-compat/bin/python -m tools.stabilize_cogvideox_candidate \
  --execution-id LM-COGVIDEOX-STABILITY-DERIVATION-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_temporal_stability_v1.json
```

This derivation does not use the model or MPS, does not overwrite the source asset, and does not restore raindrops, paper creases, or water-surface detail the model did not generate. The observation thresholds only constrain whether the subject is retained, adjacent centroid jumps, and area change. Meeting all of them is still not visual quality acceptance, shot selection, or timeline binding.

The second-shot nine-frame source already retains origami structure, water surface, and reflection, but the prompt required rightward motion while the actual net motion was leftward. That gap must not be hidden by automatic model retry or horizontal mirroring, because a horizontal mirror would also reverse the already-correct bow orientation. The frozen derivation contract `cogvideox_shot_002_rightward_direction_v1.json` locks the source execution id and video digest, builds a net-rightward `32`-pixel straight path from the first-frame subject centroid, and applies nearest-integer-pixel translation, edge replication, and a `1:4:1` symmetric three-frame blend on each frame:

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_direction_v1.json
```

The execution budget is one derivation and zero model runs. After derivation, all nine frames must retain the red subject; first-to-last net rightward motion must be at least `24` pixels; all eight adjacent lateral displacements must be at least `0.5` pixels; the maximum adjacent centroid jump must not exceed `5.5` pixels; the mean jump must not exceed `4.5` pixels; and the maximum adjacent subject-area change must not exceed `13%`. The tool also exports nine independent review images and one nine-frame contact sheet. Meeting the thresholds only closes the nine-frame direction-control observation. It must not be extrapolated directly to forty-one frames, and it must not create visual acceptance, shot selection, or timeline binding.

The first and only execution `LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-20260810T023111Z` changed first-to-last net lateral displacement from leftward `18.775` pixels to rightward `31.804` pixels, showing that a frozen translation path can change the overall direction observation. But the last adjacent step retreated `1.726` pixels, the maximum adjacent centroid jump was `9.954` pixels, the mean jump was `4.981` pixels, and the maximum adjacent subject-area change was `15.767%`. Those four gates did not close. All nine frames retain the origami boat, water surface, and reflection, but frames `4`, `5`, `7`, `8`, and `9` show a visible translucent double contour. The evidence package passed independent integrity verification with result `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`. That result is registered only as direction-correction success and technical-stability and visual-integrity failure. A second derivation is not appended.

For the already-established ghosting gap, the next policy must use the new contract `cogvideox_shot_002_rightward_spatial_only_v2.json`, rebinding the original nine-frame source rather than the failed derivation. That contract keeps the same net-rightward `32`-pixel target trajectory, but performs integer-pixel spatial translation only and no cross-frame blending:

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_v2.json
```

This contract only verifies the direction trajectory, subject retention, and whether new ghosting is introduced. Source-inherent subject-area fluctuation must continue to be reported, but it is not something a spatial-only direction derivation can repair, and this contract cannot use it as grounds to expand to forty-one frames. The execution budget remains one derivation and zero model runs.

The only execution `LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-20260810T023643Z` output a nine-frame, `768×496`, `8 fps`, `1.13` second video. All nine adjacent lateral displacements were positive, the minimum was `2.453` pixels, first-to-last net rightward motion was `33.541` pixels, and the mean adjacent centroid jump was `4.264` pixels. Those direction observations all meet the contract. But the maximum adjacent centroid jump was `6.103` pixels, `0.603` pixels over the preset `5.5` pixel cap, so the automatic gates still did not all close. Source-inherent area fluctuation continued; after derivation the maximum adjacent subject-area change was `20.729%`.

Frame-by-frame review of all nine frames confirmed that the origami main contour, triangular paper faces, major creases, water surface, and reflection persist, the bow stays rightward, the previous translucent double contour is absent, and no edge-replication seam is seen. The evidence package passed the dedicated verifier with result `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`. That result shows that removing cross-frame blending resolved the newly introduced ghosting, but it is registered only as visual-repair success and a direction trajectory near the gate. The single maximum-jump gap and the existing area fluctuation must not be treated as closed.

For the independent gap that the maximum single-step jump exceeded by `0.603` pixels, the next contract `cogvideox_shot_002_rightward_spatial_only_24px_v3.json` only narrows the nine-frame target net displacement from `32` pixels to `24` pixels, continues to bind the original source, and keeps spatial-only translation. All observation thresholds are kept as-is. The maximum-jump cap must not be raised from `5.5` pixels:

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-24PX-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_24px_v3.json
```

This contract likewise has a budget of one derivation and zero model runs. Even if every direction threshold and human visual check closes, source-inherent area fluctuation remains an unresolved observation. Later work may only use that to design a forty-one-frame contract. Forty-one frames must not be executed directly.

The only execution `LM-COGVIDEOX-SHOT-002-RIGHTWARD-SPATIAL-ONLY-24PX-20260810T025213Z` output a nine-frame, `768×496`, `8 fps`, `1.13` second video with digest `9e6abf1f535d0eb1d065c45663c30e5f0cddd28c717c233772116ceac45452c9`. First-to-last net rightward motion was `24.961` pixels. All eight adjacent lateral displacements were positive and the minimum was `0.777` pixels. The maximum adjacent centroid jump was `5.028` pixels and the mean was `3.225` pixels. All preset direction thresholds closed.

Frame-by-frame review of all nine frames confirmed that the origami main contour, triangular paper faces, major creases, water surface, and reflection persist, the bow stays rightward, and no ghosting, double contour, or edge-replication seam is seen. The evidence package passed independent verification with result `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE` and `all_observation_thresholds_met` true. That result is registered as the second-shot nine-frame low-speed direction-control baseline. It does not create visual quality acceptance, shot selection, or timeline binding. Maximum adjacent subject-area change remains `20.737%`. Before a forty-one-frame execution, a resource contract and a forty-frame direction-derivation design bound to a future source digest must be created separately. The nine-frame recipe must not be assumed to extrapolate directly.

The second-shot forty-one-frame resource contract is `cogvideox_five_second_32_steps_shot_002.json`. It keeps thirty-two steps, `41` frames, the `65%` MPS cap, the at-least-`5 GiB` available-memory stop-line, and the at-most-`4 GiB` added-swap stop-line. The resource budget cites the second-shot nine-frame measured peaks and the existing origami forty-one-frame measured peaks, and concludes that no hard limit is relaxed:

```bash
.venv-provider-compat/bin/python -m tools.run_provider_compatibility_trial \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-5S-32STEP-SHOT-002-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_five_second_32_steps_shot_002.json
```

That model contract allows only one execution. On failure it keeps evidence and does not retry automatically. Source output is `41` frames; after success it is trimmed to `derived_5s.mp4` at `40` frames, `8 fps`, exactly `5` seconds. Whether the model obeyed the direction prompt is recorded as an observation only. It is not automatically accepted or used to trigger derivation at generation time.

The forty-frame direction derivation currently exists only as the design `cogvideox_shot_002_five_second_direction_design_v1.json`, with state frozen as `UNBOUND_SOURCE_NOT_EXECUTABLE`. The design converts the nine-frame baseline of about `3` pixels per frame into a forty-frame net-rightward `117` pixels, keeps spatial-only translation, and forbids cross-frame blending. It must not pre-create a source execution id or digest. Only after the forty-one-frame source evidence is independently verified, all forty frames retain a measurable subject, and a real digest is obtained can a new bound contract be created and executed after submission. Whether background translation breaks the static-camera intent must be a forty-frame human check. It cannot be inferred as passing from the nine-frame result.

The only execution `LM-COGVIDEOX-5S-32STEP-SHOT-002-20260810T030029Z` completed the `41`-frame source output and the `40`-frame exact five-second derivation. Total elapsed time was `1678.695` seconds, of which inference was `1666.570` seconds and CPU small-tile decode was `334.633` seconds. MPS driver-allocation peak was `6,562,824,192` bytes, process-tree resident-memory peak was `15,602,139,136` bytes, system used-memory peak was `30,058,528,768` bytes, and start and peak swap were both `2,232,090,624` bytes, with no added swap. Evidence verification result was `VERIFIED_OBSERVATION_PACKAGE`.

All `41` frames retain the red origami contour, dark triangular creases, water surface, and reflection, with no subject collapse or severe deformation. Source-output maximum adjacent subject-area change was `6.228%`, clearly lower than the second-shot nine-frame source's `21.895%`. The model still did not obey the direction prompt: the exact five-second derivation had first-to-last net leftward motion of `53.262` pixels, minimum adjacent lateral displacement of `-7.597` pixels, and maximum adjacent centroid jump of `7.602` pixels. The derived video digest is `06efd281e3fca0037f4c0aafb94f8683e255563681c55d5377e05a0391643825`. That result forms a qualified five-second direction-derivation source observation. It does not create direction acceptance. A later bound contract must cite this real execution id and digest.

Only after the source evidence was submitted did the bound contract `cogvideox_shot_002_five_second_rightward_bound_v1.json` become executable. The contract freezes the real execution id and digest above, builds a forty-frame net-rightward `117`-pixel trajectory at `3` pixels per frame, caps spatial translation at `192` pixels, keeps edge replication, and forbids cross-frame blending. The tool must export all forty frame-by-frame review images and a five-column contact sheet:

```bash
.venv-provider-compat/bin/python -m tools.derive_cogvideox_shot_direction \
  --execution-id LM-COGVIDEOX-SHOT-002-5S-RIGHTWARD-BOUND-YYYYMMDDTHHMMSSZ \
  --contract experiments/postprocessing/cogvideox_shot_002_five_second_rightward_bound_v1.json
```

The bound-derivation budget is one execution and zero model runs. Automatic observations require first-to-last net rightward motion of at least `100` pixels, every adjacent lateral displacement of at least `0.5` pixels, a maximum adjacent centroid jump of no more than `5.5` pixels, a mean of no more than `4.5` pixels, and subject retention on all forty frames. Human review must also confirm that creases, water surface, reflection, bow orientation, edge seams, and background translation did not break the static-camera intent. Meeting the automatic thresholds cannot replace those visual observations.

The only execution `LM-COGVIDEOX-SHOT-002-5S-RIGHTWARD-BOUND-20260810T033318Z` formed a `40`-frame, `768×496`, `8 fps`, exact `5.000` second direction-control video with digest `73278576b53bff3126582cd630f3a3c3a907f6f78b6e25ebde99159eb6a49616`. First-to-last net rightward motion was `116.300` pixels. All thirty-nine adjacent lateral displacements were positive and the minimum was `1.500` pixels. The maximum adjacent centroid jump was `4.861` pixels and the mean was `3.043` pixels. All automatic direction thresholds closed. Maximum adjacent subject-area change was `6.354%`, close to the source's `6.228%`.

Review of all forty frames confirmed that the origami contour, dark triangular creases, water surface, and reflection persist, with no ghosting, double contour, subject collapse, or edge-replication seam, and no obvious rigid camera translation. Dedicated evidence verification result was `VERIFIED_COGVIDEOX_DIRECTION_OBSERVATION_PACKAGE`, with `all_observation_thresholds_met` true. That result is registered as the second-shot exact five-second low-speed rightward technical candidate. It does not create visual quality acceptance, formal selection, or timeline binding, and it does not authorize assembling a thirty-second video directly.

The fictional child-crying close-up uses the independent contract `cogvideox_quality_32_steps_fictional_child_crying_closeup.json`, frozen as `CogVideoX-2B`, 9 frames, 32 steps, 8 fps, and explicitly forbids five-second extension, automatic retry, harm narrative, formal acceptance, and timeline binding:

```bash
.venv-provider-compat/bin/python tools/run_provider_compatibility_trial.py \
  --provider cogvideox \
  --execution-id LM-COGVIDEOX-32STEP-FICTIONAL-CHILD-CRYING-CLOSEUP-YYYYMMDDTHHMMSSZ \
  --trial-contract experiments/provider_compatibility/cogvideox_quality_32_steps_fictional_child_crying_closeup.json
```

The only execution `LM-COGVIDEOX-32STEP-FICTIONAL-CHILD-CRYING-CLOSEUP-20260810T081709Z` successfully output a 9-frame, `768×496`, 8 fps, `1.13` second candidate with digest `aec19a34c213b270a8d563ed07b017fa00855d7df087d4d9e3ecc9035a59f351`. Total elapsed time was `276.868` seconds, of which inference was `260.281` seconds and CPU decode was `91.094` seconds. MPS driver-allocation peak was `4,367,155,200` bytes, process-tree resident-memory peak was `14,135,918,592` bytes, and peak swap rose `3,798,728,704` bytes from start. No stop-line was triggered. The evidence package passed independent verification.

All nine frames keep the facial identity and close-up composition of a light-haired fictional young child. No severe facial collapse, harm, bruise, blood, abuse, threat, text, or logo is seen. A tear at the eye corner, closed eyes, and a sad expression remain visible, but a clearly rolling tear and lower-lip tremor were not observed, so crying-action semantics form only a partial observation. This candidate does not create visual quality acceptance, a selection decision, or later five-second execution permission.

If a complete CogVideoX execution has already saved `denoised_latents.safetensors`, you can run `180×120` CPU small-tile decode alone without repeating denoise:

```bash
.venv-provider-compat/bin/python -m tools.decode_cogvideox_latent \
  --source-execution-id LM-COGVIDEOX-CPU-DECODE-R2-20260809T175503Z \
  --execution-id LM-COGVIDEOX-SMALL-TILE-DECODE-YYYYMMDDTHHMMSSZ
```

At least `16 GiB` available memory is required before start. When existing swap exceeds `4 GiB`, it may be judged historical residue only if the authoritative macOS memory-pressure class is still the normal value `1`. While running, at least `5 GiB` available memory and at most `4 GiB` added swap remain hard stop conditions. Each execution id may be used only once.

The script writes evidence by default to:

```text
evidence/runtime/<execution-id>/
```

Each execution id may be used only once. If the directory already exists, the script fail-closes so existing evidence is not overwritten.

## 6. Evidence contents

A complete execution forms:

```text
environment.json
request.json
process_metrics.jsonl
mps_metrics.jsonl
runtime.log
worker_state.json
summary.json
output.mp4
thumbnail.png
manifest.json
```

If model download, load, transfer, inference, or export fails, the output video may be absent. The parent process still saves the exit code, completed stages, error observations, and memory trace. Failure evidence does not mean the model permanently does not support Mac. It only proves this reality for the named versions, parameters, and machine context.

## 7. Independent verification

```bash
.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-WAN-MAC-001

.venv-provider-compat/bin/python \
  tools/verify_provider_compatibility_evidence.py \
  evidence/runtime/CR-0019-COGVIDEOX-MAC-001

.venv-provider-compat/bin/python -m tools.verify_cogvideox_decode_evidence \
  evidence/runtime/LM-COGVIDEOX-SMALL-TILE-DECODE-20260809T181252Z

.venv-provider-compat/bin/python -m tools.verify_cogvideox_stability_evidence \
  evidence/runtime/LM-COGVIDEOX-STABILITY-DERIVATION-20260809T192825Z

.venv-provider-compat/bin/python -m tools.verify_cogvideox_direction_evidence \
  evidence/runtime/LM-COGVIDEOX-SHOT-002-RIGHTWARD-DERIVATION-20260810T023111Z
```

The verifier checks the manifest digest, file closure, request and execution ids, output digest, and absolute user paths that must not appear in the public repository. For controlled jobs created by the console, it also checks the frozen generation profile, execution strategy, MPS ratio, strategy activation, and post-inference active-release observations. A passing verification only means the evidence package can be re-audited. It does not mean video quality is acceptable or that provider suitability has passed.

## 8. Low-memory acceptance order

Low-memory implementation and real-run observations must be judged separately. After code and model-free regression tests pass, form real observations in this order:

1. Use the "memory probe" profile, keep the `75%` MPS cap and staged residency, and run only one Wan2.1 job;
2. Confirm no other generation process is present, available memory before start is at least `16 GiB`, and existing swap is no more than `4 GiB`;
3. Watch unified memory, swap growth, MPS peak, and stage changes continuously in the observatory;
4. After the run, verify the evidence package and check the post-inference active-release record;
5. Only after the probe closes stably may the "low-memory generation" profile be used;
6. CogVideoX has completed staged denoise, small-tile CPU decode, 41-frame source output, exact five-second derived output, one non-model temporal-stability derivation, and a thirty-two-step nine-frame quality probe. Water-surface and rain-scene semantics improved, but paper creases and formal quality acceptance still have not closed, so the console remains blocked.

The independent text-encoder stage formed two real failure observations: `LM-WAN-STAGED-PROBE-20260809T161019Z` showed that model-level offload lets the full UMT5 enter MPS; `LM-WAN-LEAF-PROBE-20260809T161726Z` showed that calling `encode_prompt` directly without disabling autograd still accumulates intermediates under leaf-order offload and hits the cap. After enabling leaf-order offload and `torch.inference_mode()`, `LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` completed prompt encoding, text-encoder release, denoise-pipeline load, inference, video export, and evidence closure. That result only allows the frozen memory probe to be treated as runnable. It must not be extrapolated to a higher profile or picture quality.

## 9. Current Mac measured record

The numbers below are observations on one specific machine, dependency set, and parameter set. They are not a product specification or a performance promise.

| Model | Current conclusion | Exact snapshot | Key observation |
| --- | --- | --- | --- |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` | One real generation and evidence closure completed | `0fad780a534b6463e45facd96134c9f345acfa5b` | Cache about 27G; total elapsed 2730.198 seconds, of which first snapshot resolution 2661.848 seconds; 17 frames, 416×240, 8 fps; Metal driver-allocation peak 30,979,096,576 bytes; swap increased about 23.39GB from start |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` low-memory probe | Pipeline and staged strategy activated successfully; inference terminated by the swap guard | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`, 9 frames, 1 step; pipeline load 28.482 seconds; MPS driver sampled peak 4,210,524,160 bytes; added swap 9,075,425,280 bytes, over the 8 GiB budget; no video output; execution id `LM-WAN-PROBE-20260809T152435Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` no-gradient leaf probe | Controlled generation and independent evidence closure completed | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`, 9 frames, 1 step, 8 fps; total elapsed 23.444 seconds; MPS driver peak 8,413,462,528 bytes; system swap peak did not exceed the start value; output 11,712 bytes; execution id `LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` quality probe | Run closed but semantics unrecognizable | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`, 9 frames, 4 steps, 8 fps; total elapsed 28.624 seconds; MPS driver peak 8,413,462,528 bytes; swap did not grow; output 32,028 bytes; picture remains blue-purple blocks, red paper boat not recognizable; execution id `LM-WAN-QUALITY-PROBE-20260809T170134Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 16-step balance probe | Run closed and semantic form appeared for the first time | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`, 9 frames, 16 steps, 8 fps; total elapsed 33.684 seconds, of which inference 9.331 seconds; MPS driver peak 8,413,462,528 bytes; swap did not grow; a red subject and water-surface structure appeared in the center, but the paper-boat contour remains coarse; execution id `LM-WAN-BALANCE-PROBE-20260809T170402Z` |
| `Wan-AI/Wan2.1-T2V-1.3B-Diffusers` 8-step balance backtest | Run closed; current lowest recognizable profile identified | `0fad780a534b6463e45facd96134c9f345acfa5b` | `256×144`, 9 frames, 8 steps, 8 fps; total elapsed 30.685 seconds, of which inference 5.945 seconds; MPS driver peak 8,413,462,528 bytes; swap did not grow; all 9 frames retain the red hull, pointed ends, and water-surface layers, with a contour better than this 16-step output; execution id `LM-WAN-BALANCE-BACKTEST-20260809T170657Z` |
| `zai-org/CogVideoX-2b` | Eight steps is the lowest recognizable point; thirty-two steps is the current nine-frame quality baseline | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Eight-step same-parameter staged comparison total elapsed 104.597 seconds, MPS driver peak 4,367,155,200 bytes, swap growth 0; versus the old full-pipeline eight-step, MPS driver peak fell 63.884%, nine-frame hull semantics retained; thirty-two steps further formed clearer reflection, ripple, and rain-scene semantics, but paper creases remain insufficient; execution id `LM-COGVIDEOX-8STEP-STAGED-20260809T184407Z` |
| `zai-org/CogVideoX-2b` thirty-two-step quality probe | Nine-frame rain scene and water surface improved; origami material still not closed | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Total elapsed 247.653 seconds; MPS driver peak 4,367,155,200 bytes, added swap 0; all nine frames retain the hull; maximum adjacent centroid jump fell from the sixteen-step 15.54 px to 10.58 px, mean from 7.90 px to 4.29 px; water-surface reflection and concentric ripples clearly stronger, but maximum subject-area change rose to 15.42%, and there are no clear paper creases; execution id `LM-COGVIDEOX-32STEP-QUALITY-20260809T193147Z` |
| `zai-org/CogVideoX-2b` thirty-two-step origami-prompt probe | Stable recognizable origami structure formed for the first time | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Only the prompt subject description changed; total elapsed 220.365 seconds, MPS driver peak 4,356,620,288 bytes, added swap 0; all nine frames formed overlapping triangular paper faces and a persistent diagonal fold line, and retained water-surface reflection and ripples; but maximum adjacent centroid jump was 20.45 px and maximum subject-area change was 17.08%; nine-frame quality gate passed only, five-second continuity not yet proven; execution id `LM-COGVIDEOX-32STEP-ORIGAMI-QUALITY-20260809T193843Z` |
| `zai-org/CogVideoX-2b` thirty-two-step origami five-second candidate | 41-frame quality and resources closed | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Total elapsed 1331.091 seconds; MPS driver peak 6,562,824,192 bytes, added swap 0; all 41 frames retain origami faces, creases, water surface, and reflection, and an exact 5-second derivation was formed; original maximum adjacent centroid jump 7.40 px; execution id `LM-COGVIDEOX-5S-32STEP-ORIGAMI-20260809T194654Z` |
| Origami five-second temporal-stability derivation | All technical-continuity thresholds passed | Same as above | Model not rerun; maximum adjacent centroid jump fell from 7.40 px to 1.27 px, mean from 3.46 px to 0.70 px, maximum area change fell to 2.15%; 40-frame origami structure and scene semantics retained; execution id `LM-COGVIDEOX-ORIGAMI-STABILITY-DERIVATION-20260809T201042Z` |
| `zai-org/CogVideoX-2b` five-second candidate observation | Technical closure; motion continuity still needs handling | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Sixteen-step generation of 41 frames and derivation of 40 frames, 8 fps, exact 5 seconds; total elapsed 828.230 seconds, MPS driver peak 6,562,824,192 bytes, added swap 0; all 41 frames retain the red hull, but maximum adjacent centroid jump about 45.1 px, formal quality acceptance must not be registered; execution id `LM-COGVIDEOX-5S-16STEP-20260809T190026Z` |
| `zai-org/CogVideoX-2b` five-second temporal-stability derivation | Technical-continuity thresholds closed; still awaiting human quality acceptance | `1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01` | Locks the existing five-second source digest, does not rerun the model; output 40 frames, 8 fps, exact 5 seconds, all frames retain the hull; maximum adjacent centroid jump fell from about 45.1 px to 2.78 px, mean from about 12.29 px to 1.37 px, maximum area change 12.08%; 40-frame review showed no edge seam or obvious double image, but raindrops, creases, and water-surface detail remain insufficient; execution id `LM-COGVIDEOX-STABILITY-DERIVATION-20260809T192825Z` |

Existing successful Wan2.1 evidence is at `evidence/runtime/CR-0019-WAN-MAC-001/`. First-round low-memory failure evidence is at `evidence/runtime/LM-WAN-PROBE-20260809T152435Z/`. Current no-gradient leaf-probe success evidence is at `evidence/runtime/LM-WAN-INFERENCE-LEAF-PROBE-20260809T162212Z/`. Four-step quality evidence is at `evidence/runtime/LM-WAN-QUALITY-PROBE-20260809T170134Z/`. Sixteen-step balance evidence is at `evidence/runtime/LM-WAN-BALANCE-PROBE-20260809T170402Z/`. Eight-step balance-backtest evidence is at `evidence/runtime/LM-WAN-BALANCE-BACKTEST-20260809T170657Z/`. Under the same prompt, seed, canvas, frame count, guidance scale, and frame rate, 4 steps is unrecognizable and 8 steps is recognizable, so 8 steps is the lowest usable point in the current trial scope. That conclusion does not extrapolate to other prompts, seeds, resolutions, or models. Each CogVideoX round of evidence is in the matching `evidence/runtime/<execution-id>/` directory and has passed the applicable verifier. The thirty-two-step frozen prompt established the current original-prompt quality baseline. The origami-prompt comparison further closed the nine-frame origami-structure gate, so the next step may separately design a forty-one-frame contract. It does not automatically prove five-second continuity, and it does not lift the human quality-acceptance, console-job, or thirty-second-timeline blocks.

A fuller observation write-up is in `knowledge/Wan2.1_and_CogVideoX_Mac_Compatibility.md`.

## 10. Common questions

### Memory pressure or system swap

On less than 64GB of unified memory, video diffusion models readily trigger swap. Process-tree resident memory, system used memory, swap, and Metal driver allocation in the evidence should be read together. No single number should be called the model's exact VRAM.

### Metal does not support an operator

The trial explicitly enables `PYTORCH_ENABLE_MPS_FALLBACK=1`. Unsupported operators can fall back to the CPU. Logs and elapsed time will reflect that reality. If it still fails, keep the error observation. Do not switch backends without a record.

### First run takes a long time

The first run includes model download. `summary.json` records snapshot resolution, model load, inference, and export as separate stages. Later cache hits should not be mixed with first-download elapsed time as one metric.

### Why frame count and step count are low

This round's goal is to establish actual runnability and evidence capability, not a quality evaluation. A formal cross-provider contract must separately freeze standard resolution, frame count, step count, prompt compilation, and comparable observations. These trial parameters must not be reused directly.
