# AI Native Engineering

> AI Native Engineering 的目标，不是让 AI 一次做对，而是让每一次执行都产生可验证、可解释、可利用的偏差，使下一次执行比上一次更接近预期。

本仓库沉淀可迁移的 AI 原生工程方法。视频是第一个落地验证领域，不是仓库的最终边界。

## 五层结构

```text
.
├── AGENTS.md
├── README.md
├── foundation/
├── execution/
├── video/
├── verification/
└── knowledge/
```

根目录的 `README.md` 是仓库入口，`AGENTS.md` 是 Codex 行为协议；正文文档全部进入以下五层。

### 第一层：基础层

保存项目愿景、第一原则、治理、概念架构和统一术语。这一层定义长期不变量。

```text
foundation/
├── 00_ProjectVision.md
├── 01_FirstPrinciples.md
├── 02_Governance.md
├── 03_Architecture.md
├── 04_Glossary.md
├── 05_Evidence.md
├── 06_Institution.md
└── revisions/
```

`foundation/revisions/` 只保存待审查修订提案。草案没有制度权威，不属于现行冻结制度。

### 第二层：执行引擎

描述 AI 如何从预期进入规划、执行、验证、偏差、诊断、策略和经验沉淀。

```text
execution/
├── Expectation.md
├── Planning.md
├── Execution.md
├── Verification.md
├── Gap.md
├── Diagnosis.md
├── Policy.md
└── Learning.md
```

### 第三层：视频领域

只定义视频领域模型和创作对象，不承担跨领域治理职责。

```text
video/
├── README.md
├── DomainBoundary.md
├── Intent.md
├── Story.md
├── Script.md
├── Scene.md
├── Shot.md
├── Character.md
├── Emotion.md
├── Camera.md
├── Lighting.md
├── Color.md
├── Audio.md
├── Timeline.md
└── Publication.md
```

### 第四层：验证库

保存可复用的检查分类、指标和验收定义。

```text
verification/
├── HardChecks.md
├── SoftChecks.md
├── CreativeReview.md
├── Metrics.md
└── Acceptance.md
```

### 第五层：知识库

保存会随模型和实践持续变化的经验，不得反向成为治理制度。

```text
knowledge/
├── Seedance.md
├── Veo.md
├── Kling.md
├── PromptPatterns.md
├── FailurePatterns.md
└── RepairPatterns.md
```

## 当前状态

五层文档结构已经建立。Codex 依据本地冻结制度、证据和逻辑一致性独立起草与审查；历史 ChatGPT 对话只保留为设计来源，不再构成审查权威或推进依赖。任何正式冻结仍必须满足 `IF-0007`。

当前已经实现：

```text
IF-0001 -> foundation/01_FirstPrinciples.md -> Authority Model
IF-0002 -> execution/Expectation.md -> Expectation Model
IF-0003 -> execution/Gap.md -> Gap Model
IF-0004 -> execution/Diagnosis.md -> Diagnosis Model
IF-0005 -> execution/Policy.md -> Policy Model
IF-0006 -> foundation/05_Evidence.md -> Evidence Model
IF-0007 -> foundation/06_Institution.md -> Institution Model
```

其他文档可能处于既有草案或空白占位状态；在获得对应制度冻结前，不视为已冻结制度。

当前待审查草案：

```text
CR-0001 -> foundation/revisions/CR-0001_ConstitutionRevisionV2.md -> DRAFT
CR-0001-R2 -> foundation/revisions/CR-0001_ObjectGraphReview_R2.md -> PASS_WITH_BLOCKERS
CR-0002 -> foundation/revisions/CR-0002_DecisionModel.md -> SUPERSEDED_DRAFT
CR-0002-R1 -> foundation/revisions/CR-0002_R1_DecisionModel.md -> DRAFT / PASS_WITH_BLOCKERS
CR-0002-R1-LOCAL-REVIEW -> foundation/revisions/CR-0002_R1_IndependentReview.md -> COMPLETED / PASS_WITH_BLOCKERS
CR-0002-R2 -> foundation/revisions/CR-0002_R2_DecisionModel.md -> DRAFT / INDEPENDENT_REVIEW_REQUIRED
CR-0002-R2-LOCAL-REVIEW -> foundation/revisions/CR-0002_R2_IndependentReview.md -> COMPLETED / PASS_WITH_BLOCKERS
CR-0002-R3 -> foundation/revisions/CR-0002_R3_DecisionModel.md -> DRAFT / PASS_WITH_THREE_BOUNDED_BLOCKERS / CONSOLIDATION_BLOCKED
CR-0002-R3-LOCAL-REVIEW -> foundation/revisions/CR-0002_R3_IndependentReview.md -> COMPLETED / PASS_WITH_THREE_BOUNDED_BLOCKERS
CR-0002-R4 -> foundation/revisions/CR-0002_R4_DecisionModel.md -> DRAFT / PASS_WITH_ONE_BOUNDED_BLOCKER / CONSOLIDATION_BLOCKED
CR-0002-R4-LOCAL-REVIEW -> foundation/revisions/CR-0002_R4_IndependentReview.md -> COMPLETED / PASS_WITH_ONE_BOUNDED_BLOCKER
CR-0002-R5 -> foundation/revisions/CR-0002_R5_DecisionModel.md -> DRAFT / PASS_FOR_CONSOLIDATION
CR-0002-R5-FINAL-COMPOSITE-REVIEW -> foundation/revisions/CR-0002_R5_FinalCompositeReview.md -> COMPLETED / PASS_FOR_CONSOLIDATION
CR-0002-CONSTITUTION-CANDIDATE -> foundation/revisions/CR-0002_ConstitutionCandidate.md -> PASS_AS_CONSISTENT_CANDIDATE / NOT_FROZEN
CR-0002-CONSTITUTION-CANDIDATE-SEMANTIC-DIFF -> foundation/revisions/CR-0002_ConstitutionCandidate_SemanticDiff.md -> COMPLETED / PASS_WITH_INDEPENDENT_CONSISTENCY_REVIEW_REQUIRED
CR-0002-CONSTITUTION-CANDIDATE-CONSISTENCY-REVIEW -> foundation/revisions/CR-0002_ConstitutionCandidate_ConsistencyReview.md -> COMPLETED / PASS_AS_CONSISTENT_CANDIDATE
CR-0002-FREEZE-DEPENDENCY-READINESS-AUDIT -> foundation/revisions/CR-0002_FreezeDependencyReadinessAudit.md -> COMPLETED / NOT_READY_FOR_FREEZE
CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN -> foundation/revisions/CR-0002_ExternalGovernanceDependencyClosurePlan.md -> COMPLETED / PLAN_ESTABLISHED
CR-0003-TYPE-AUDIT -> foundation/revisions/CR-0003_CommitTypeAudit.md -> PASS_WITH_CONSTRAINTS
CR-0003 -> foundation/revisions/CR-0003_CommitModel.md -> SUPERSEDED_DRAFT / PASS_WITH_BLOCKERS
CR-0003-R1 -> foundation/revisions/CR-0003_R1_CommitModel.md -> SUPERSEDED_DRAFT / PASS_WITH_BLOCKERS
CR-0003-R1-LOCAL-REVIEW -> foundation/revisions/CR-0003_R1_IndependentReview.md -> COMPLETED
CR-0003-R2 -> foundation/revisions/CR-0003_R2_CommitModel.md -> SUPERSEDED_DRAFT / PASS_WITH_BLOCKERS
CR-0003-R3 -> foundation/revisions/CR-0003_R3_CommitModel.md -> SUPERSEDED_DRAFT / PASS_WITH_BLOCKERS
CR-0003-R3-LOCAL-REVIEW -> foundation/revisions/CR-0003_R3_IndependentReview.md -> COMPLETED
CR-0003-R4 -> foundation/revisions/CR-0003_R4_CommitModel.md -> BASE_DRAFT / PASS_WITH_BLOCKERS
CR-0003-R4-EPISTEMIC-REVIEW -> foundation/revisions/CR-0003_R4_EpistemicReview.md -> COMPLETED
CR-0003-R5 -> foundation/revisions/CR-0003_R5_EpistemicCommitModel.md -> REVIEW_REQUIRED / CONSOLIDATION_REQUIRED
CR-0003-R5-LOCAL-REVIEW -> foundation/revisions/CR-0003_R5_IndependentReview.md -> COMPLETED / PASS_WITH_BLOCKERS
CR-0003-R6 -> foundation/revisions/CR-0003_R6_EpistemicClosureAmendment.md -> REVIEW_REQUIRED / CONSOLIDATION_REQUIRED
CR-0003-R6-LOCAL-REVIEW -> foundation/revisions/CR-0003_R6_IndependentReview.md -> COMPLETED / PASS_WITH_ONE_BLOCKER_CLUSTER
CR-0003-R7 -> foundation/revisions/CR-0003_R7_QualificationCompatibilityClosure.md -> REVIEW_REQUIRED / CONSOLIDATION_REQUIRED
CR-0003-R7-FINAL-CLOSURE-REVIEW -> foundation/revisions/CR-0003_R7_FinalClosureReview.md -> COMPLETED / PASS_FOR_CONSOLIDATION
CR-0003-CONSTITUTION-CANDIDATE -> foundation/revisions/CR-0003_ConstitutionCandidate.md -> CONSISTENCY_REVIEW_REQUIRED / NOT_FROZEN
CR-0003-CONSTITUTION-CANDIDATE-CONSISTENCY-REVIEW -> foundation/revisions/CR-0003_ConstitutionCandidateConsistencyReview.md -> COMPLETED / PASS_WITH_CONSOLIDATION_BLOCKERS
CR-0003-CONSTITUTION-CANDIDATE-R1 -> foundation/revisions/CR-0003_ConstitutionCandidate_R1.md -> CONSISTENCY_REVIEW_REQUIRED / NOT_FROZEN
CR-0003-CONSTITUTION-CANDIDATE-R1-CONSISTENCY-REVIEW -> foundation/revisions/CR-0003_ConstitutionCandidate_R1_ConsistencyReview.md -> COMPLETED / PASS_WITH_TWO_BOUNDED_BLOCKERS
CR-0003-CONSTITUTION-CANDIDATE-R2 -> foundation/revisions/CR-0003_ConstitutionCandidate_R2.md -> FINAL_CONSISTENCY_REVIEW_REQUIRED / NOT_FROZEN
CR-0003-CONSTITUTION-CANDIDATE-R2-FINAL-REVIEW -> foundation/revisions/CR-0003_ConstitutionCandidate_R2_FinalReview.md -> COMPLETED / PASS_AS_CONSISTENT_CANDIDATE
CR-0003-FREEZE-DEPENDENCY-READINESS-AUDIT -> foundation/revisions/CR-0003_FreezeDependencyReadinessAudit.md -> COMPLETED / NOT_READY_FOR_FREEZE
CR-0004 -> foundation/revisions/CR-0004_InstitutionRegistryAndFreezeReferenceSupport.md -> DRAFT / PASS_WITH_FOUR_BOUNDED_BLOCKERS / R1_REQUIRED
CR-0004-LOCAL-REVIEW -> foundation/revisions/CR-0004_IndependentReview.md -> COMPLETED / PASS_WITH_FOUR_BOUNDED_BLOCKERS
CR-0004-R1 -> foundation/revisions/CR-0004_R1_InstitutionRegistryAndFreezeReferenceSupport.md -> DRAFT / INDEPENDENT_REVIEW_REQUIRED / CONSOLIDATION_BLOCKED
```
