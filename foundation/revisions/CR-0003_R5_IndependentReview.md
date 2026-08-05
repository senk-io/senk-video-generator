# CR-0003-R5 本地独立认识闭合复核

## 复核信息

```text
Review ID: CR-0003-R5-LOCAL-REVIEW
Review Type: Epistemic Closure and Consistency Review
Status: COMPLETED
Result: PASS_WITH_BLOCKERS
Executable: NO
Reviewed Proposal Set: CR-0003-R4 + CR-0003-R5
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, R4 commit core, R4 epistemic review, R5 bounded overlay
External Approval Required: NO
Institution Freeze Created: NO
Constitution Candidate Created: NO
```

> 本文件是本地独立复核记录，不是制度冻结、正式事实或运行时授权。它不修改 `CR-0003-R4`、`CR-0003-R5` 及任何历史记录。

## 复核命题

本轮回答：

> `R4 + R5` 是否已经能够在证据、资格、规则和来源随时间演进时，确定性地重建当前认识，同时保证历史不被覆盖、未知不被提升、冲突不被隐藏、来源不被遗漏？

最低审查不变量为：

```text
Historical Record Mutation = FORBIDDEN

Projection Certainty
<= Strongest Applicable Qualified Source Certainty

Missing or Unresolved Required Dependency
-> INDETERMINATE

Derived Projection
-/-> Formal Fact or Future Action Authority
```

## 总体裁决

`CR-0003-R5` 已实质解决 `CR-0003-R4-EPISTEMIC-REVIEW` 提出的原四项阻断：

- 历史证明资格不再被视为永久适用；
- 投影拥有明确确定性上限；
- 前向解释不能放大确定性；
- 当前投影可以降级、冲突和恢复，同时不修改历史；
- 来源适用性和依赖失效已有最小消费接口。

因此，旧阻断的覆盖结果为：

```text
Original R4 Epistemic Blockers: CLOSED
```

但在把增补条款组合为完整可执行语义时，仍发现三项新的模型阻断：

1. `As Of` 同时承担现实有效时点和认识截点，双时间语义尚未分离；
2. 当前证明资格投影没有完整的作用域键、谱系兼容和冲突真值表；
3. 传递依赖闭包缺少能够证明来源全集完整的权威封闭边界。

因此：

```text
R5 Amendment Direction: PASS
Original Blocker Closure: PASS
Combined Epistemic Determinism: FAIL_WITH_BLOCKERS
Consolidation Readiness: FAIL
Constitution Candidate Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 已通过一：历史事实与当前认识保持分离

`EPI-01`、`EPI-19`、`EPI-22` 和 `EPI-28` 共同建立：

```text
Historical Resolution remains immutable
Current Projection may weaken or conflict
Projection Change -/-> Historical Mutation
Projection -/-> Formal Fact
```

新证据和更正可以改变当前可用认识，但不能把旧记录改写成从未存在。

```text
Historical Immutability: PASS
Projection / Formal Fact Separation: PASS
```

## 已通过二：认识确定性被显式封顶

`EPI-09` 至 `EPI-14` 已禁止：

- 多个不确定来源投票产生终局；
- 用默认值解析 `UNRESOLVED`；
- 在可比较终局冲突中选择一个胜者；
- 忽略必需但未决的依赖；
- 依据来源数量、模型置信度或登记新旧提升确定性。

```text
Epistemic Ceiling: PASS
Conflict Preservation Principle: PASS
Field Presence Preservation: PASS
```

## 已通过三：前向解释不再拥有隐式重新裁决能力

`EPI-16` 至 `EPI-18` 要求前向解释保留字段存在性、证据引用和认识强度。可能提高确定性的变化必须进入新的受权威约束解析历史。

```text
Forward Interpretation Non-amplification: PASS
Re-resolution History Preservation: PASS
```

## 已通过四：资格、解析、投影和策略仍然分权

`EPI-04`、`EPI-29` 和 `EPI-30` 没有让资格适用性、投影或依赖变化自动获得目标事实权威或未来行动权威。

```text
Authority Non-propagation: PASS_WITH_CLARIFICATION
Policy Separation: PASS
Self-validation Prohibition: PASS
```

合并稿仍需把 R5 新增的授权类型并入 `Commit Contract` 的统一授权清单，但这属于合并义务，不构成本轮独立阻断。

## 阻断一：现实有效时间与认识截点没有分离

### 问题

R5 使用了：

```text
Effective From
Applicability As Of
Observed At
Produced At
Projection As Of
Closure As Of
```

但没有明确区分两种不同时间：

```text
Valid Time
  -> 来源或资格在被描述现实中的适用时间

Knowledge Cutoff
  -> 本次解析允许消费到哪个登记时点的记录
```

同一个历史有效时点可能在不同认识截点产生不同投影：

```text
Valid Time = T1
Knowledge Cutoff = T2 -> ABORTED
Knowledge Cutoff = T3 -> INDETERMINATE after correction
```

如果只记录一个 `As Of`，系统无法判断投影是在重建“当时知道什么”，还是在表达“现在依据全部已知记录如何看待当时”。这会造成未来证据被静默带入历史视图，或新更正被错误排除在当前视图之外。

### 必须补充

所有资格适用性、依赖闭包和投影至少分别绑定：

```text
Validity As Of
Knowledge Cutoff
Produced At
Applicable Source Registration Boundary
```

并冻结以下不变量：

```text
Same Validity As Of
+ Different Knowledge Cutoff
-> Different legitimate projection snapshots may exist

Historical Knowledge View
  consumes only records registered by its Knowledge Cutoff

Current Restatement View
  may consume later corrections
  but must never claim to be the historical knowledge view
```

### 裁决

```text
Bitemporal Semantics: FAIL_WITH_BLOCKER
Risk Level: CRITICAL
Required Action: R5 revision before consolidation
```

## 阻断二：当前证明资格投影缺少完备解析表

### 问题

`EPI-07` 规定，只要至少一项历史资格为 `QUALIFIED` 且适用性为 `APPLICABLE`，全部必需依赖可确认，当前投影即可为 `QUALIFIED`。

但它没有定义以下组合：

```text
Applicable QUALIFIED
+ Applicable DISQUALIFIED
-> ?

Applicable QUALIFIED under Rule V1
+ Applicable DISQUALIFIED under Rule V2
+ Compatibility UNKNOWN
-> ?

Multiple proof IDs or commit scopes
-> which projection key owns the result?
```

`EPI-05` 的 `CONFLICTED` 只覆盖“适用性结论冲突”，不能自动替代“资格结果冲突”。如果不补齐，投影器可能仅因为存在一项可用 `QUALIFIED` 就忽略同一作用域内可比较的 `DISQUALIFIED`。

### 必须补充

当前证明资格投影必须绑定唯一作用域键：

```text
Candidate Proof ID
Commit Key
Commit Contract Version or Compatibility Domain
Validity As Of
Knowledge Cutoff
Qualification Projection Rule Version
```

并定义最低真值表：

```text
Applicable comparable QUALIFIED only
+ complete dependencies
-> QUALIFIED

Applicable comparable DISQUALIFIED only
+ complete dependencies
-> DISQUALIFIED

Applicable comparable QUALIFIED
+ Applicable comparable DISQUALIFIED
-> CONFLICTED

Required applicability, lineage or compatibility unresolved
-> INDETERMINATE
```

不同规则版本只有在显式资格语义兼容关系下才能比较；不可比较或兼容性未知时必须保持 `INDETERMINATE`，不能伪造冲突，也不能选择结果。

### 裁决

```text
Qualification Projection Determinism: FAIL_WITH_BLOCKER
Qualification Scope Identity: FAIL_WITH_BLOCKER
Risk Level: CRITICAL
Required Action: R5 revision before consolidation
```

## 阻断三：依赖闭包缺少来源全集的封闭证明

### 问题

`EPI-25` 要求 `Dependency Closure Reference` 和 `Completeness Proof Reference`，但没有定义完整性证明建立在什么权威来源全集上。

摘要只能证明“给出的集合没有变化”，不能证明“应该出现的来源没有被遗漏”。如果没有封闭边界，依赖闭包构建器仍可能得到：

```text
Digest of an incomplete source set
-> apparently complete closure
-> terminal projection
```

R4 的账本完整前缀证明只覆盖解析账本位置，不自动覆盖资格、证据更正、规则兼容、来源排除和传递依赖的多账本闭包。

### 必须补充

每项依赖闭包必须声明：

```text
Root Scope
Authoritative Source Registries
Per-registry Completeness Boundary or Watermark
Traversal Rule Version
Required Edge Types
Knowledge Cutoff
Closed-world or Open-world Semantics
Completeness Proof Authority Reference
```

最低规则：

```text
Any required registry has no authoritative completeness boundary
-> Closure Completeness = INDETERMINATE
-> Projection = INDETERMINATE

Open-world dependency scope
+ absence of source record
-/-> source is absent or inapplicable
```

依赖闭包构建器可以重建集合，但不能仅用自己产生的摘要证明来源全集完整。完整性必须来自适用注册表边界、封闭前缀证明或独立授权的完整性证明。

### 裁决

```text
Dependency Closure Completeness: FAIL_WITH_BLOCKER
Omission Resistance: FAIL_WITH_BLOCKER
Risk Level: CRITICAL
Required Action: R5 revision before consolidation
```

## 合并前非阻断修订

以下问题不会单独推翻 R5 方向，但应随下一修订一并精确化：

### 一、恢复依据需要声明组合逻辑

`EPI-20` 的依据列表必须明确是替代路径还是必须同时满足的条件，并为每条恢复路径声明最低充分输入。不能让投影器自行解释列表中的“或”与“且”。

### 二、兼容性和来源排除契约必须声明制度出处

`Forward Interpretation Contract`、规则兼容关系和 `Institutional Source Exclusion Basis` 必须引用其治理制度、版本、适用权威和证据，不得由投影运行时临时创建。

### 三、投影审计写入失败必须失败关闭

物化投影发生变化时，若 `Projection Change Audit Record` 无法追加，新的物化投影不得发布为可消费读面。审计记录仍不是正式事实，也不能自证投影正确。

## 与冻结制度兼容性

| 冻结制度 | 结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `PASS_WITH_CLARIFICATION` | 角色分权成立；新增完整性证明边界仍需明确 |
| `IF-0006 Evidence Model` | `PASS_WITH_BLOCKER` | 历史不可变成立；双时间与更正消费截点未闭合 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、提供者独立和跨领域；不具备冻结证据 |
| 五层架构边界 | `PASS` | 全局传播算法仍保持在提交模型范围外 |

## 完整复核矩阵

```text
Commit Core Causality: PASS
Attempt Identity Ordering: PASS
Authority Coverage: PASS_WITH_CLARIFICATION
Proof Qualification Separation: PASS
Historical Record Immutability: PASS
Original R4 Epistemic Blocker Closure: PASS
Epistemic Ceiling: PASS
Conflict Preservation Principle: PASS
Forward Interpretation Safety: PASS
Projection Downgrade Semantics: PASS
Projection Recovery Direction: PASS_WITH_CLARIFICATION
Projection / Formal Fact Separation: PASS
Policy Separation: PASS
Bitemporal Semantics: FAIL_WITH_BLOCKER
Qualification Projection Determinism: FAIL_WITH_BLOCKER
Qualification Scope Identity: FAIL_WITH_BLOCKER
Dependency Closure Completeness: FAIL_WITH_BLOCKER
Omission Resistance: FAIL_WITH_BLOCKER
Provider Independence: PASS
Domain Portability: PASS
Consolidation Readiness: FAIL
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Constitution Candidate Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 独立决定

1. 接受 `CR-0003-R5` 的修订方向；
2. 确认 `R4` 认识审查提出的原四项阻断已经关闭；
3. 不把 `R4 + R5` 合并为宪法候选；
4. 不冻结任何提交模型制度；
5. 保留 `R4`、`R5` 为不可覆盖的历史草案；
6. 下一步只修订三项新阻断和三项非阻断精确化，不重写已经通过的提交主干；
7. 修订完成后再次执行本地独立闭合复核；
8. 即使模型复核通过，仍不得越过决策模型和 `IF-0007` 的冻结门槛。

