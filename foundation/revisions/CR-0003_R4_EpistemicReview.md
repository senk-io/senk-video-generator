# CR-0003-R4 认识演化一致性审查

## 审查信息

```text
Review ID: CR-0003-R4-EPISTEMIC-REVIEW
Review Type: Epistemic Evolution Consistency Review
Status: COMPLETED
Result: PASS_WITH_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0003-R4
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, R4 object graph and historical proposals
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是本地独立审查记录，不是制度冻结。它审查系统如何认识已经发生的提交事实，不创建、修改或撤销任何提交事实。

## 核心审查命题

本轮只回答：

> 当证据、证明资格、解析规则和投影规则随时间演进时，系统能否更新当前认识，同时不覆盖历史，也不借解释、兼容或投影之名获得超出合格证据的确定性？

审查采用以下候选上限：

```text
Projection Certainty
<= Strongest Applicable Qualified Source Certainty
```

以及以下历史边界：

```text
New Evidence
New Qualification
New Resolution Rule
New Projection Rule
-/-> Rewrite Historical Record
```

## 总体裁决

`CR-0003-R4` 的提交主干已经成立：

- 权威迁移与归因原子耦合；
- 提交结果不创建目标迁移；
- 未应用证明经过独立资格链；
- 解析计算、登记和投影分别授权；
- 账本追加位置与语义谱系分离；
- 跨规则版本兼容性显式分类；
- 历史记录只追加、不覆盖。

这些部分均通过。

但 `R4` 尚未完整定义“当前认识”的依赖闭包和演化规则。本轮发现四项认识层阻断：

1. 证明资格只有一次性结论，没有适用性生命周期和当前资格投影；
2. 当前解析投影没有显式确定性上限与冲突保留不变量；
3. `FORWARD_INTERPRETABLE` 缺少禁止确定性放大的解释契约；
4. 历史终局解析与当前可用认识之间缺少降级、失效和恢复语义。

另有一个跨模型依赖：证据更正和上游资格失效尚无统一依赖传播模型。

因此：

```text
Commit Core Model: PASS
Epistemic Evolution Model: FAIL_WITH_BLOCKERS
Model Freeze Review Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 已通过一：历史记录不可覆盖

`R4` 正确要求：

```text
Old Registered Resolution
  -> New Candidate Resolution
  -> New Registered Resolution
```

规则升级、重新解析、对账和补偿都不能修改旧记录。

```text
Historical Immutability: PASS
```

## 已通过二：不兼容规则不会伪造冲突

```text
INCOMPATIBLE
or UNKNOWN_COMPATIBILITY
  -> Projection = INDETERMINATE
```

规则不可比较不等于事实矛盾，因此没有被错误提升为 `CONFLICTED`。

```text
Rule Incompatibility Semantics: PASS
```

## 已通过三：证明资格不直接产生 ABORTED

```text
Proof Qualification
!= Commit Resolution
```

资格只允许证明进入提交解析；提交解析仍必须在独立授权和规则下形成候选结果。

```text
Qualification / Resolution Separation: PASS
```

## 已通过四：账本顺序与认识谱系分离

`Resolution Ledger Position` 只表达追加顺序，父引用和谱系关系表达认识演化。并发分支不会因最后写入获胜而消失。

```text
Concurrent History Preservation: PASS
```

## 阻断一：证明资格缺少适用性生命周期

### 问题

`Registered Proof Qualification Record = QUALIFIED` 只表达某项证明在某个资格规则版本和登记时点通过准入。

它没有回答：

- 资格规则后来被取代时，旧资格是否仍适用于新的解析时点；
- 证明引用的证据被更正、失效或发现版本错误时，旧资格如何影响当前认识；
- 同一证明出现 `QUALIFIED` 与 `DISQUALIFIED` 历史时，当前解析应采用哪项；
- 资格结论的适用区间和失效原因如何表达。

当前模型容易形成：

```text
Once QUALIFIED
-> Always usable
```

这会把历史资格误当成永久资格。

### 必须补充

证明资格历史需要：

```text
Proof Qualification Ledger Position
Proof Qualification Lineage
Qualification Rule Version
Effective From
Effective Until or UNRESOLVED
Supersedes Qualification Record
Source Evidence Applicability References
```

并产生可重建派生读面：

```text
Current Proof Qualification Projection
  -> QUALIFIED
   | DISQUALIFIED
   | INDETERMINATE
   | CONFLICTED
```

历史 `QUALIFIED` 记录仍保留，但提交解析只有在其 `As Of` 时点能够证明资格适用时才能引用。

### 裁决

```text
Qualification Applicability Lifecycle: FAIL
Risk Level: HIGH
Required Action: CR-0003-R5 or frozen Evidence Qualification dependency
```

## 阻断二：投影缺少确定性上限

### 问题

`R4` 定义了投影输入完整性、谱系和规则兼容性，但没有冻结以下不变量：

```text
Projection Certainty
<= Applicable Qualified Source Certainty
```

因此，一个投影规则理论上仍可能：

- 从多个 `INDETERMINATE` 来源计算出 `COMMITTED`；
- 在相互冲突的可比较终局记录中选择一个“更可信”的结果；
- 因来源数量更多而把证据不足升级成确定；
- 忽略不利的合格来源或未决分支；
- 用规则默认值补齐未解析字段。

### 必须冻结

最低投影不变量：

```text
All applicable sources INDETERMINATE
  -> Projection INDETERMINATE

Comparable COMMITTED and ABORTED terminal sources
  -> Projection CONFLICTED

Any required lineage or dependency unresolved
  -> Projection INDETERMINATE

Source omitted without institutional exclusion basis
  -> Projection INDETERMINATE

Default value
-/-> Resolve UNRESOLVED
```

投影规则只能压缩已经由来源支持的认识，不能产生来源中不存在的确定性。

### 裁决

```text
Epistemic Ceiling: FAIL
Conflict Preservation: FAIL_WITH_BLOCKER
Risk Level: CRITICAL
Required Action: CR-0003-R5
```

## 阻断三：FORWARD_INTERPRETABLE 可能放大确定性

### 问题

`FORWARD_INTERPRETABLE` 允许新投影规则按指定规范解释旧解析记录，但当前没有要求解释映射保持认识强度。

危险路径：

```text
Old Resolution = INDETERMINATE under Rule V1
  -> Forward Interpretation under Rule V2
  -> COMMITTED
```

如果没有新的候选解析、合格证据和登记过程，这相当于投影规则借“解释”之名创建新的确定性解析。

### 必须补充

`FORWARD_INTERPRETABLE` 必须具有版本化解释契约：

```text
Source Resolution Rule Version
Target Canonical Interpretation Version
Total Deterministic Mapping
Field Presence Preservation
Evidence Reference Preservation
Certainty Non-amplification Proof
Mapping Rule Version
Compatibility Evidence
```

最低不变量：

```text
Interpret(INDETERMINATE)
  -> INDETERMINATE

Interpret(UNRESOLVED field)
  -> UNRESOLVED field

Interpret(CONFLICTED comparable sources)
  -> CONFLICTED
```

任何可能提高确定性的语义变化必须采用 `REQUIRES_RERESOLUTION`，通过新的解析执行权威、候选记录、证据和登记历史完成。

### 裁决

```text
Forward Interpretation Safety: FAIL
Rule Compatibility Evidence: FAIL_WITH_BLOCKER
Risk Level: CRITICAL
Required Action: CR-0003-R5
```

## 阻断四：当前认识缺少降级和恢复语义

### 问题

单条解析谱系只允许：

```text
INDETERMINATE -> COMMITTED | ABORTED
```

这对确定性细化是正确的。但“当前解析投影”不是单条历史记录，它可能因新证据、更正、资格失效或规则不兼容而降低确定性。

合法场景：

```text
Historical Resolution R1 = ABORTED
Current Projection at T1 = ABORTED

Evidence Correction arrives at T2
Proof Qualification becomes INDETERMINATE
Current Projection at T2 = INDETERMINATE
```

历史 `R1` 仍然真实存在，但当前可用认识必须降级。`R4` 尚未明确允许并约束这种变化。

### 必须分离

```text
Historical Resolution Refinement
  -> append-only, terminal records never rewritten

Current Projection Evolution
  -> may strengthen with new qualified evidence
  -> may weaken when applicability is lost
  -> may become CONFLICTED when comparable terminal sources conflict
  -> may recover after new qualification or legality resolution
```

每次投影变化必须记录：

```text
Previous Projection Digest
New Projection Digest
Projection Rule Version
Projection As Of
Added Applicable Sources
Removed Applicable Sources
Applicability Change References
Change Reason Code
Generated At
```

投影变化记录是派生审计记录，不修改投影来源和历史解析。

### 裁决

```text
Projection Downgrade Semantics: FAIL
Projection Recovery Semantics: FAIL
Risk Level: HIGH
Required Action: CR-0003-R5
```

## 跨模型依赖：证据更正与失效传播

`IF-0006` 允许：

```text
Evidence -> Correction
```

但当前尚未冻结一个通用模型，说明证据更正如何影响：

```text
Proof Qualification
Commit Resolution Applicability
Current Resolution Projection
Dependent Policy Authorization
```

`Commit Model` 不应自行实现全局依赖传播算法，但必须定义接口：

```text
Source Applicability Input
Applicability Change Record
Dependency Closure Reference
Fail-closed Projection Behavior
```

在依赖传播模型冻结前，任何无法确认来源仍适用的投影都必须保持 `INDETERMINATE`。

```text
Dependency Invalidation Interface: REQUIRED
Global Propagation Algorithm: OUT_OF_SCOPE
```

## 认识演化不变量候选

下一修订版必须至少明确：

```text
EPI-01 Historical records are immutable
EPI-02 Qualification is versioned and time-bounded
EPI-03 Projection certainty cannot exceed applicable qualified sources
EPI-04 Interpretation cannot amplify certainty
EPI-05 Source applicability loss may weaken current projection
EPI-06 Comparable terminal conflicts must remain visible
EPI-07 Re-resolution appends history
EPI-08 Projection is never a formal fact
EPI-09 Unknown dependency applicability fails closed
EPI-10 Recovery requires new qualified inputs or legality resolution
```

## 与冻结制度兼容性

| 冻结制度 | 结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `PASS_WITH_REVIEW` | R4 已补齐运行时授权；适用性变更仍需授权输入 |
| `IF-0006 Evidence Model` | `FAIL_WITH_BLOCKER` | 证据更正后的资格和投影降级尚未闭合 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、跨领域和历史不可变；冻结证据仍不足 |
| 五层架构边界 | `PASS` | 全局依赖传播算法保持在本模型范围外 |

## 完整审查矩阵

```text
Commit Core Causality: PASS
Attempt Identity Ordering: PASS
Authority Coverage: PASS_WITH_REVIEW
Proof Qualification Separation: PASS
Resolution Ledger / Lineage Separation: PASS
Cross-version Compatibility Classification: PASS
Historical Record Immutability: PASS
Qualification Applicability Lifecycle: FAIL
Epistemic Ceiling: FAIL
Forward Interpretation Safety: FAIL
Projection Downgrade Semantics: FAIL
Projection Recovery Semantics: FAIL
Dependency Invalidation Interface: FAIL_WITH_BLOCKER
Provider Independence: PASS
Domain Portability: PASS
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Model Freeze Review Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 独立决定

1. 不冻结 `CR-0003-R4`；
2. 不否定 `R4` 的提交主干；
3. 保留 `R4` 为历史草案，不原地修改；
4. 下一步建立 `CR-0003-R5`，只处理四项认识层阻断和依赖失效接口；
5. `R5` 不新增提交结果值，不把投影提升为正式事实；
6. `R5` 完成后由 Codex 做本地独立认识闭合复审；
7. 即使复审通过，在决策模型和 `IF-0007` 门槛闭合前，也只能成为 `CONSTITUTION_CANDIDATE`；
8. 不修改现有 `IF-0001` 至 `IF-0007`。
