# One-sentence shot planning draft

This slice turns one sentence of natural-language creative intent into an observable,
non-authoritative shot draft. It does not create a formal `ShotSpec`, call a video
provider, or produce quality-pass, fail, selection, or timeline-binding facts.

## Project-survival hard gate

The planning gate, diagnosis gate, and adversarial gate are project-survival hard
gates: all three must pass to continue; any miss stops the project. The frozen
original text, current gaps, and continue/stop judgment live in
[`shot-planning-acceptance-gates.md`](./shot-planning-acceptance-gates.md).
This file keeps only the draft contract and historical observations. It must not
lower that gate, and it must not impersonate a pass with shortened text,
abbreviation overrides, or missing-evidence narrative.

```text
one-sentence request
  -> explicit semantic constraints
  -> deterministic source-fact extraction and field ownership
  -> local text model, staged residual payload
  -> deterministic system merge
  -> deterministic system context and observable-text compile
  -> structure observations
  -> semantic and observability checks
  -> multi-run stability observations
  -> a human or authorized policy decides the next action
```

## Frozen boundary

- Requests and drafts in editions 1–7 use `shot-planning-request.v1` and
  `shot-planning-proposal.v1`. Editions 8–12 use `shot-planning-request.v2` and
  `shot-planning-proposal.v2` in parallel. Historical evidence is not migrated or
  rewritten.
- Drafts must stay `DRAFT_NON_AUTHORITATIVE`.
- Narrative beats must cite exact character spans from the source sentence.
  Non-punctuation content must not be omitted.
- Scenes split when place, time, or the main narrative goal changes. Shots split
  by a single picture purpose.
- Each shot has exactly one `primary_purpose` and one primary `action`.
- Provider-specific prompts are still compiled later by `ProviderAdapter`.
- Automatic observations do not judge artistic quality. Creative results always
  keep a human-review entry.
- Structural agreement means only that repeated outputs share structure. It does
  not mean the shot is faithful or acceptable.
- Controlled-semantic agreement observes composition, performance, lighting,
  continuity, and shot-core enumerations separately. Structural agreement rate
  does not replace consistency on those fields.

## Local model prompts

The provider-neutral prompt contract can still be generated on its own:

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --print-prompt
```

The caller must write the actual `model_id`, `model_version`, `run_id`,
temperature, and random seed back onto every raw output. The validation tool
does not fabricate that execution evidence.

The current bounded reference trial freezes `Qwen/Qwen3-0.6B` revision
`c1899de289a04d12100db370d81485cdf75e47ca`. Model weights are `1,503,300,328`
bytes. Inference runs on local `MPS` and does not call a remote inference API.
Omitting `--execute` is preflight only:

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --execute \
  --execution-id LOCAL-SHOT-PLAN-QWEN3-V7-YYYYMMDDTHHMMSSZ
```

Edition 7 currently splits each planning round into seven single-duty stages:
`scene_context`, `beat_purpose`, `shot_core`, `composition`, `performance`,
`lighting`, and `continuity`. Three rounds make twenty-one calls. The automatic
retry budget is zero. Scene context emits only controlled marks. Beat action
reuses the full `shot_core.action_description` from the same run. Stable
identifiers, source spans, target duration, subject references, model revision,
draft status, and observable checks are compiled deterministically by the system
from the versioned contract. The small model has no authority to generate those
governance fields or check conclusions.

Edition 7 remains the default single-request reproduction experiment. It does
not represent general shot understanding. Cross-request observations use a
separate three-case suite: a rain crying close-up, an indoor smile medium shot,
and a locked-camera wide shot of a bicycle crossing a night street from left to
right. Each case freezes three rounds of seven stages, sixty-three calls in
total. The three cases share one model load. Automatic retry remains zero.
Reserved expectations participate only in after-the-fact observation and never
enter any model prompt.

```bash
.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_suite \
  --suite experiments/shot_planning/qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --contract experiments/shot_planning/qwen3_0_6b_guarded_source_facts_held_out_library_reader_trial_v12.json

.venv-provider-compat/bin/python -m tools.run_local_shot_planner_trial \
  --contract experiments/shot_planning/qwen3_0_6b_guarded_source_facts_held_out_snow_courtyard_cat_trial_v12.json
```

The default suite path is now the edition-12 guarded-source-facts contract: three
cases, three rounds, seven stages, sixty-three planned calls, zero automatic
retries, and the same frozen model revision. Omitting `--execute` is contract
preflight only. The edition-12 live-model suite has been executed as
`LOCAL-SHOT-PLANNER-V12-20260914T032833Z` /
`LOCAL-SHOT-PLANNER-GUARDED-SOURCE-FACTS-001`. This cloud workspace could not
load that evidence directory, so the numbers below come from the read-only
prompt snapshot and stay bound to that `execution_id`. They must not be
rewritten. The suite recorded `model_call_count` `63/63`, `run_count` `9/9`,
`automatic_retry_count` `0`, `model_load_count` `1`, and
`package_integrity=COMPLETE_AND_DIGEST_MATCHED`. Strict parse is `9/9`.
Structurally observable drafts are `0/9`. The planning gate has not passed.
`formal_shot_spec_created=false`, `formal_quality_acceptance_created=false`,
and `creative_review_required=true`. This slice must not invent a later
`--execute` run or treat integrity as a quality pass. Historical edition-11
evidence still uses
`experiments/shot_planning/qwen3_0_6b_hybrid_source_facts_generalization_suite_v1.json`.
The two held-out trial contracts remain runnable placeholders. They were not
run as a live-model suite in this round. They stay
`DRAFT_NON_AUTHORITATIVE`, keep the same non-goals, and do not count toward the
planning gate.

## Single-run structure observations

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --proposal /absolute/path/to/proposal-001.json
```

## Repeated-run stability observations

For a first observation, run three times with the same model version, prompt
contract, and sampling settings:

```bash
.venv-provider-compat/bin/python -m tools.validate_shot_plan \
  --request experiments/shot_planning/foreign_child_crying_closeup_request_v1.json \
  --proposal /absolute/path/to/proposal-001.json \
  --proposal /absolute/path/to/proposal-002.json \
  --proposal /absolute/path/to/proposal-003.json
```

The report records structural agreement on scene count, beat count, shot count,
purpose sequence, action class, shot size, camera move, scene mapping, and
duration distribution. Separately, it records agreement on shot-core,
composition, performance, lighting, and continuity controlled fields and on
their whole-group marks. Repeated `proposal_id` or `run_id` values are not
counted twice. If model version, prompt contract, or sampling settings disagree,
the whole comparison fail-closes. The report only establishes observations. It
does not interpret any agreement-rate threshold as formal stability or
acceptance.

## Seven local single-request observations

| Edition | Strict JSON | Comparable drafts | Main observation |
| --- | --- | --- | --- |
| `v1` | `0/3` | `0/3` | All three rounds used code fences, wrong governance-field nesting, and omitted the shot array |
| `v2` | `3/3` | `0/3` | Bare JSON stabilized, but the model returned only the first scene item of the nested template |
| `v3` | `3/3` | `3/3` | Three-stage structural agreement `1.0`, but human review found “close-up, crying, in the rain” was not faithfully executed |
| `v4` | `3/3` | `0/3` | Core semantics were stably corrected; five composition, emotion, continuity, and check-text differences remained unobservable |
| `v5` | `3/3` | `3/3` | Seven-stage controlled text removed the five short-text differences; human review then found place/time role errors and an incompatible `ZOOM + LEFT + FAST` combination |
| `v6` | `3/3` | `0/3` | Place, time, and camera policy converged; the model still stably abbreviated allowed text “持续降雨” and “孩子在雨中哭泣” to “雨” and “哭”, and the system refused to compile |
| `v7` | `3/3` | `3/3` | Scenes became tokenized context and reused the full core action; three-round seven-stage raw outputs matched stage-for-stage, proposal-block observations were zero, and both structural and controlled-semantic maximum exact-group ratios were `1.0` |

Editions 5–7 did not lower `minimum_free_text_characters` or accept abbreviations
in order to manufacture a zero-difference result. The edition-7 result shows that
the current request can form three comparable drafts that agree on structure and
controlled semantics under a fixed model, revision, prompt contract, and
controlled lexicon. It does not prove artistic quality, general request
coverage, or video-generation effect. Drafts therefore stay
`DRAFT_NON_AUTHORITATIVE` and still require human creative review.

## Multi-request generality observations

| Edition | Strict-parse runs | Comparable drafts | Retained observations | Main observation |
| --- | --- | --- | --- | --- |
| `v8` | `9/9` | `0/9` | `228` | Multi-candidates were emitted as single-element arrays; the system rejected the type error by contract and did not auto-unbox or patch |
| `v9` | `9/9` | `3/9` | `153` | Scalar candidates removed the array-shape problem; the crying case compiled but chose `WIDE` in all three rounds; the smile and bicycle cases were still blocked by stage constraints |
| `v10` | `9/9` | `0/9` | `120` | Candidate Chinese glosses reduced wrong choices, but environment-continuity errors, illegal enumerations, and mistaking subject lateral motion for camera `PAN` remained |
| `v11` | `9/9` | `0/9` | `93` | Deterministic extraction locked `9/11/9` explicit or deterministically derived fields; the model never wrote locked fields, but residual continuity, composition, and lighting choices still blocked every run |
| `v12` | `9/9` | `0/9` | not counted in this prompt snapshot | Live suite `LOCAL-SHOT-PLANNER-V12-20260914T032833Z` completed `63/63` calls and `9/9` parsed runs with zero automatic retries and one model load; integrity is `COMPLETE_AND_DIGEST_MATCHED`. Each case has `structurally_observable_run_count=0`. This is not a planning-gate pass, formal `ShotSpec`, or quality acceptance |

Identical in-round controlled fingerprints only mean the model repeated the same
choice. When the choice itself is wrong, that agreement must not be read as
semantic stability or a quality pass. Edition 11 shows that explicit fact
ownership can reduce observations: per-round controlled-value mismatches for the
rain-crying, indoor-smile, and bicycle cases dropped from `6/9/7` to `5/7/6`,
and the smile case also kept exact source-sentence echo across three proposal
rounds. `Qwen3-0.6B` is still insufficient on the remaining `17–19` fields of
cross-stage semantic choice. Two cases were blocked after merge by continuity
observations, and the smile case also failed the observable-text requirement.
The next live-model knife after edition 11 compared the same residual field
contract under `extractor.v2` / `guarded prompt.v12`. It did not lower
observation thresholds. The edition-12 result still leaves structurally
observable drafts at `0/9`, so the planning gate remains closed.

Edition 12 is not an overlay fix of edition-11 evidence. `trial.v11`,
`extractor.v1`, `extraction.v1`, and `hybrid prompt.v11` stay closed-bound.
Only `trial.v12` binds `extractor.v2`, `extraction.v2`, and `guarded prompt.v12`.
`extractor.v2` records `ASSERTED`, `NEGATED`, `CONTEXT_ONLY`, `UNRESOLVED`, or
`IGNORED_QUOTED` for each lexical hit. An explicit negation that hits a
registered controlled lexeme or guard stem and has no controlled same-field
positive replacement, and an unresolvable nested polarity that already hit, block
before evidence is written and before the model is called. Adversarial
regressions cover “并非/从未/别/勿”, controlled “而是/反而/改用” corrections,
affirmative idioms, non-negative compounds, camera lateral motion near the
subject, and “固定相机参数” boundaries. The existing three positive cases still
lock the same `9/11/9` fields under both extractors, so wiring non-regression
alone never proved model-quality improvement. Edition 12 now has crying, smile,
and bicycle `trial.v12` files plus
`qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json`, and those
contracts have a live-model suite execution:
`LOCAL-SHOT-PLANNER-V12-20260914T032833Z` /
`LOCAL-SHOT-PLANNER-GUARDED-SOURCE-FACTS-001`. The live suite is not a
planning-gate pass. Structural observability is `0/9`, not `9/9`.
`formal_shot_spec_created` remains `false`. `formal_quality_acceptance_created`
remains `false`. `creative_review_required` remains `true`. The held-out
library-reader and snow-courtyard-cat trials are also `trial.v12`, but they
were not run as a live-model suite in this round. They remain
`DRAFT_NON_AUTHORITATIVE` placeholders and must not be counted as 3/3
structurally observable results.

Per-case observations from the prompt snapshot, bound to
`LOCAL-SHOT-PLANNER-V12-20260914T032833Z`:

| Case | Missing compiled terms | Codes / extra marks | Must not be read as |
| --- | --- | --- | --- |
| `CRY_RAIN_CLOSEUP` | 小孩 / 哭 / 泪 / 雨 / 面部 / 相机保持静止 | `GENERALIZED_*_MISMATCH` + `PROPOSAL_NOT_OBJECT`; same fingerprint across three rounds | Same-fingerprint agreement as acceptable or structurally observable |
| `SMILE_INDOOR_MEDIUM` | 上半身 only | `exact_source_echo` `3`; `largest_exact_controlled_semantic_group_ratio=1.0` | Agreement `1.0` on a wrong choice as acceptable |
| `BICYCLE_LEFT_TO_RIGHT_WIDE` | 自行车 / 左 / 右 / 街道 / 全景 / 相机保持静止 | `GENERALIZED_TEAR_HIGHLIGHT_WITHOUT_VISIBLE_TEARS`; `PROPOSAL_NOT_OBJECT` | Cross-case tear contamination as ignorable, or a missing-term draft as comparable |

The next knife should iterate the policy contract against missing compiled
terms and `PROPOSAL_NOT_OBJECT` / cross-case contamination. It must not lower
thresholds, shrink required text, accept abbreviation overrides, or rewrite
wrong-choice agreement as a pass.

All seven evidence packages can have their file set and digests rechecked.
The edition-7 live execution id is
`LOCAL-SHOT-PLAN-QWEN3-V7-20260812T165514Z`. The evidence manifest covers `98`
files:

```bash
.venv-provider-compat/bin/python -m tools.verify_local_shot_planner_evidence \
  evidence/runtime/LOCAL-SHOT-PLAN-QWEN3-V7-20260812T165514Z
```

The integrity recheck result is `COMPLETE_AND_DIGEST_MATCHED`. That result only
means the evidence file set and digests match the frozen contract. It is not a
formal shot spec or quality acceptance.

Edition 8–11 suite evidence can also be rechecked. The edition-11 execution id
is `LOCAL-SHOT-PLAN-QWEN3-HYBRID-SOURCE-FACTS-20260813T022128Z`. It records
implementation digests for the extractor, field ownership, model residual
payload, deterministic merge, and suite aggregator. Three cases, sixty-three
calls, one model load, zero automatic retries:

```bash
.venv-provider-compat/bin/python -m tools.verify_local_shot_planner_suite \
  evidence/runtime/LOCAL-SHOT-PLAN-QWEN3-HYBRID-SOURCE-FACTS-20260813T022128Z
```

The recheck result is also `COMPLETE_AND_DIGEST_MATCHED`, but the suite
explicitly keeps `formal_shot_spec_created=false`,
`formal_quality_acceptance_created=false`, and a human-review requirement.
The edition-10 execution remains
`LOCAL-SHOT-PLAN-QWEN3-SEMANTIC-GLOSS-20260812T174803Z`. Earlier `v8` and `v9`
suite executions are
`LOCAL-SHOT-PLAN-QWEN3-GENERALIZATION-20260812T173104Z` and
`LOCAL-SHOT-PLAN-QWEN3-SCALAR-GENERALIZATION-20260812T173628Z`. The first run
that stopped on an implementation gap,
`LOCAL-SHOT-PLAN-QWEN3-GENERALIZATION-20260812T173012Z`, is kept as-is and is
not cited as a complete suite.

The edition-12 live suite execution id is
`LOCAL-SHOT-PLANNER-V12-20260914T032833Z`. This cloud workspace could not load
`evidence/runtime/LOCAL-SHOT-PLANNER-V12-20260914T032833Z`, so the counts above
are the read-only prompt snapshot, not a fresh digest recheck performed here.
When that directory is present on the machine that ran the suite, the same
verifier applies:

```bash
.venv-provider-compat/bin/python -m tools.verify_local_shot_planner_suite \
  evidence/runtime/LOCAL-SHOT-PLANNER-V12-20260914T032833Z
```

The prompt snapshot already records `package_integrity=COMPLETE_AND_DIGEST_MATCHED`,
`formal_shot_spec_created=false`, `formal_quality_acceptance_created=false`, and
a human-review requirement. Integrity is not a formal shot spec, quality
acceptance, or planning-gate pass.
