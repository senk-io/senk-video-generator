# CR-0006-R6 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 through CR-0006-R6
Repair Basis: CR-0006-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R6 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0006-R6` 对映射证明资格和时间治理边界固定的修复。它不修改被审提案，不审查 `CR-0005-R7`，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 映射证明是否固定受治理证据边界及独立完整性；
2. 相反证明是否在映射声明层共同竞争，而不是按候选载荷分域；
3. 证明资格是否拥有候选、登记、完整边界和聚合解析；
4. 映射评价是否固定精确时间治理边界向量 `T`；
5. `T` 资格是否证明聚合覆盖 `T` 内全部同域候选，而不只是证明成员位于 `T`；
6. 时间资格是否与评价内容同一登记且保持阶段无环；
7. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005-R4 INTERNAL REGISTRATION AND CONFLICT AGGREGATION CLOSURE
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 through CR-0006-R5
CR-0006-R6 GOVERNED MAPPING PROOF AND TEMPORAL BOUNDARY CONSUMPTION CLOSURE
CR-0006-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、作者身份和候选级闭合声明均不作为通过依据。

## 总体裁决

R6 已建立证明资格与时间边界主体：

```text
Governed Mapping Evidence Boundary: PASS
Independent Evidence Completeness: PASS
Proof Qualification Candidate Identity: PASS
Proof Candidate Registration Resolution: PASS
Proof Competing Boundary: PASS
Proof Aggregate Registration Resolution: PASS
Temporal Governance Boundary Vector T Pinning: PASS
Historical / Current View Mode: PASS
Temporal Eligibility Stable Key: PASS
Eligibility as Evaluation Subobject: PASS
M0 through M7 Acyclicity: PASS
Evaluation Same-key Eligibility Conflict: PASS
```

但有两个残余逃逸：

1. 证明资格语义键包含映射候选键和候选载荷摘要；而映射候选载荷已经包含证明摘要。相反证明可通过不同候选载荷进入不同资格语义域，`NOT_QUALIFIED` 候选又被排除在确定映射成员之外；
2. 时间资格只证明旧聚合及其输入“位于 `T` 内”，没有证明旧聚合的竞争边界覆盖 `T` 内全部同语义域候选。扩展 `T` 中旧有利聚合仍可保持 `ELIGIBLE`。

因此：

```text
TM-R5-B1 Governed Evidence Infrastructure: CLOSED
Claim-level Adverse Proof Aggregation: FAIL_WITH_BOUNDED_BLOCKER
TM-R5-B2 T Identity Pinning: CLOSED
T-scoped Aggregate Coverage: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R7 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
```

## 一、已通过：受治理证据与证明资格登记链

R6 固定受治理证据边界、证据记录集合或位置、规范化规则和边界完整性，并独立评价：

```text
CARRIER_INTEGRITY
POSITION_OR_EXACT_SET_COMPLETENESS
READ_COMPLETENESS
CONFLICT_SUBDOMAIN_COMPLETENESS
SEMANTIC_SCOPE_COVERAGE
```

证明资格进一步拥有候选键、时间账本登记解析、完整竞争边界、聚合键和外层登记解析。

```text
Opaque Digest as Sufficient Proof: CLOSED
Self-qualified Mapping Candidate: PROHIBITED
Missing Evidence Boundary: INDETERMINATE
Same Qualification Key / Opposite Result: CONFLICTED
```

该通过项只适用于同一个证明资格语义键；声明级跨候选证明竞争另见 `TM-R6-B1`。

## 二、有界阻断 TM-R6-B1：证明资格键被候选证明载荷分割

R6 的证明资格语义键包含：

```text
Required Dimension Source-domain Mapping Candidate Key
Candidate Mapping Payload Digest
```

R5 的候选映射载荷又包含：

```text
Dimension-to-domain Semantic Equivalence Proof Digest
Source Boundary and Scope Coverage Proof Digest
Boundary Shape Compatibility Proof Digest
```

因此相同维度、目标来源域、作用域和边界形态的两个映射声明，只要证明摘要不同，就会形成不同候选键和不同证明资格语义键。

R6-14 规定 `NOT_QUALIFIED | INDETERMINATE | CONFLICTED` 不产生确定映射成员。这样不利证明所在候选可以被保留在谱系中但不进入最终映射竞争，合格候选仍可能单独支持 `MAPPED`。

### 反例

候选甲与乙都声称：

```text
Required Dimension D -> Source Completeness Domain A
```

甲的证据资格为 `QUALIFIED`，乙的不同证明和证据边界得出 `NOT_QUALIFIED`。因为候选载荷摘要不同，两份资格不竞争。乙被排除为确定映射成员，甲可以支持 `MAPPED(A)`。

```text
Expected: adverse proof for same mapping claim participates in one qualification result
Current: candidate-payload-partitioned proof domains
Result: TM-R6-B1 reproduced
```

### 关闭条件

`CR-0006-R7` 必须：

1. 定义映射声明级证明语义键，固定维度、目标来源域、来源边界、快照、查询作用域、边界形态和适用区间；
2. 从声明级键排除候选 ID、候选载荷摘要、证明摘要和证据边界；
3. 全部同声明证明资格候选进入同一完整竞争边界；
4. `QUALIFIED` 与 `NOT_QUALIFIED` 或不兼容证明并存时必须 `CONFLICTED`；
5. 映射竞争成员只可消费已登记声明级证明聚合，而不是选择某个候选级合格证明；
6. 不利证明缺失、读取失败或完整性未知必须失败关闭。

```text
TM-R6-B1 Mapping Claim-level Proof Qualification Aggregation: BLOCKED
```

## 三、已通过：T 固定和阶段无环

R6 为映射消费固定：

```text
Registered Temporal Governance Boundary Vector T ID and Digest
T.Registered Temporal Mapping Ledger Boundary ID and Digest
T.Required Mapping-ledger Completeness Resolution IDs and Digests
Temporal View Mode
```

时间资格是完整性评价候选的内容同一子对象，不反向写入其引用的 `T`。阶段保持：

```text
M0 Mapping Candidate
M1 Proof Qualification
M2 Mapping Competing Boundary
M3 Mapping Aggregate
M4 Mapping Ledger Boundary
M5 Temporal Governance Boundary Vector T
M6 Completeness Evaluation
M7 Knowledge Boundary K
```

```text
Bare Current / Latest Position: PROHIBITED
Historical / Current T Identity Separation: PASS
Eligibility-to-T Identity Cycle: NONE_FOUND
Same Eligibility Key / Opposite Payload: CONFLICTED
```

## 四、有界阻断 TM-R6-B2：T 资格只有成员证明，没有全域覆盖证明

时间资格载荷固定聚合、证明聚合、竞争边界记录及其在 `T` 中的成员证明，并要求这些输入都位于 `T` 的映射账本边界内。

但它没有固定或证明：

```text
Exact All Applicable Mapping Candidate Set within T for Semantic Conflict Key
Exact All Claim-level Proof Qualification Set within T
Aggregate Competing Boundary Coverage of T-scoped Candidate Set
No Excluded Applicable Record under T
T-scoped Re-aggregation Result
```

“旧聚合的全部输入都在 `T` 内”不等于“旧聚合覆盖 `T` 内全部适用输入”。

### 反例

`T1` 下只有候选 `D -> A`，旧聚合为 `MAPPED(A)`。扩展到 `T2` 后新增候选 `D -> B`，当前全域应 `CONFLICTED`。

旧聚合记录、旧证明和旧竞争边界仍全部位于 `T2` 内，因此现有成员证明可以给旧聚合 `ELIGIBLE`；规则没有要求其竞争边界覆盖 `T2` 中新增的 `D -> B`。

```text
Expected: old subset aggregate is NOT_ELIGIBLE under expanded T2
Current: membership satisfied without T-scoped coverage
Result: TM-R6-B2 reproduced
```

### 关闭条件

`CR-0006-R7` 必须：

1. 时间资格固定 `T` 内同映射语义键的全部适用候选和证明资格集合摘要；
2. 独立证明该集合相对 `T.Mapping Ledger Boundary` 完整；
3. 证明被消费聚合的竞争边界成员集合与 `T` 作用域集合内容同一，或建立新的 `T` 作用域重聚合解析；
4. 旧子边界聚合在扩展 `T` 下必须 `NOT_ELIGIBLE`、`INDETERMINATE` 或 `CONFLICTED`；
5. 历史 `T1` 仍可重放旧聚合，当前 `T2` 必须使用 `T2` 作用域结果；
6. `T` 作用域集合变化必须形成新的时间资格、评价和认识边界身份。

```text
TM-R6-B2 T-scoped Mapping Aggregate Coverage: BLOCKED
```

## 五、回归与退出判定

未发现 R6 对以下既有方向造成其他回归：

```text
Global Temporal Position Model: PASS
Mapping Candidate / Boundary / Aggregate Identity: PASS
Required Dimension / Source-domain Alignment: PASS
Registered Source Completeness Aggregate Consumption: PASS
Correction / Migration Aggregate Identity: PASS
Temporal Governance Contract Roots: PASS
Knowledge Boundary Type Closure: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0006-R6 Independent Model Re-review: COMPLETED
Original Two Blockers: BOTH_CLOSED_WITH_ONE_RESIDUAL_EACH
Residual Bounded Blockers: 2
CR-0006-R7 Required: YES
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Runtime Authority: NOT_CREATED
```
