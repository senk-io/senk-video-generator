# CR-0006-R5 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 + CR-0006-R2 + CR-0006-R3 + CR-0006-R4 + CR-0006-R5
Repair Basis: CR-0006-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R5 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0006-R5` 对全局位置模型和必要维度—来源完整性语义域映射的修复。它不修改被审提案，不审查 `CR-0005-R6`，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 新增时间记录是否统一进入既有全局位置域并保持位置不可复用；
2. 类型化读取是否保持非权威投影而不产生第二边界；
3. 必要维度—来源语义域映射是否拥有稳定候选、竞争边界和聚合登记身份；
4. 映射的语义等价与作用域覆盖证明是否具有受治理资格；
5. 历史和当前评价是否固定同一时间治理边界下的映射聚合；
6. 来源聚合元组与映射结果是否一一对应且失败关闭；
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
CR-0006-R1 through CR-0006-R4
CR-0006-R5 GLOBAL TEMPORAL POSITION AND REQUIRED-DIMENSION SOURCE-DOMAIN MAPPING CLOSURE
CR-0006-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、作者身份和候选级闭合声明均不作为通过依据。

## 总体裁决

R5 已关闭位置分区身份问题，并建立映射身份主干：

```text
Independent Temporal Partition Object: RETIRED
Global Position Namespace: PASS
Cross-record-type Position Non-reuse: PASS
Global Temporal Ledger Boundary: PASS
Typed Boundary Projection Non-authority: PASS
Mapping Semantic Conflict Key: PASS
Mapping Candidate Registration: PASS
Mapping Competing Boundary: PASS
Mapping Aggregate Registration: PASS
Required Dimension Mapping Tuple Coverage: PASS
Source Aggregate Domain Equality Check: PASS
Mapping Failure Propagation: PASS
```

但映射的确定资格和双时间消费仍有两个缺口：

1. 候选载荷只保存语义等价、作用域覆盖和边界形态证明摘要，没有受治理证据边界、证明资格稳定键或登记解析；
2. 映射聚合记录进入时间映射账本，但评价元组没有固定其所属 `Temporal Governance Boundary Vector T`，可以在后续冲突已经登记后继续选择旧的有利聚合。

因此：

```text
TM-R4-B1 Partition and Position Identity: CLOSED
TM-R4-B2 Mapping Identity: CLOSED_WITH_TWO_QUALIFICATION_AND_TEMPORAL_RESIDUALS
Mapping Proof Qualification: FAIL_WITH_BOUNDED_BLOCKER
Temporal Boundary Pinning: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R6 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
```

## 一、已通过：账本全局位置模型

R5 明确撤销 `Registered Append-only Temporal Record Partition` 的候选和消费资格，全部记录类型共享：

```text
Temporal Derived Record Position Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

记录类型只是载荷判别字段。相同账本、纪元和位置跨记录类型复用必须冲突；失败写保留永久空洞。

范围边界覆盖范围内全部记录类型和空洞，类型化边界投影固定全局边界与匹配记录集合，但不取得独立位置、边界登记或完整性权威。

```text
Position Namespace Ambiguity: CLOSED
Cross-type Position Collision: CONFLICTED
Typed Projection as Second Boundary: PROHIBITED
Correction / Migration Boundary References: ALIGNED_TO_GLOBAL_BOUNDARY
TM-R4-B1 Result: CLOSED
```

## 二、已通过：映射身份与来源聚合对齐主体

映射语义冲突键固定要求集合资格、必要维度、来源边界、快照、查询作用域、边界形态、最低矩阵和查询规则合同，并排除目标来源域和候选 ID。

R5 进一步建立：

```text
Required Dimension Source-domain Mapping Candidate Key
Required Dimension Source-domain Mapping Candidate Registration Resolution Key
Required Dimension Source-domain Mapping Competing Boundary Key
Required Dimension Mapping Boundary Registration Resolution Key
Required Dimension Source-domain Mapping Aggregate Resolution Key
Required Dimension Source-domain Mapping Aggregate Registration Resolution Key
```

不同目标来源域必须进入同一竞争集合。必要维度映射元组与来源完整性聚合元组必须在维度集合和语义域上逐项内容同一。

```text
Target-domain Key Escape: CLOSED
Evaluation-time Ad-hoc Mapping: PROHIBITED
Dimension Set Omission / Duplication: PROHIBITED
Mapped Domain / Source Aggregate Domain Mismatch: FAIL_CLOSED
NOT_MAPPED / INDETERMINATE / CONFLICTED Propagation: PASS
```

## 三、有界阻断 TM-R5-B1：映射证明只有摘要，没有受治理资格

映射候选载荷包含：

```text
Dimension-to-domain Semantic Equivalence Proof Digest
Source Boundary and Scope Coverage Proof Digest
Boundary Shape Compatibility Proof Digest
```

但复合模型没有定义：

```text
Governed Mapping Evidence Boundary ID and Digest
Mapping Evidence Boundary Completeness Resolution ID and Digest
Dimension / Domain Mapping Proof Qualification Key
Candidate Proof Qualification
Proof Qualification Registration Attempt
Registered Proof Qualification Resolution
```

候选内容同一登记只能证明“某个摘要被登记”，不能证明该摘要来自适用、完整且无冲突的证据边界，也不能证明语义等价、作用域覆盖或边界形态结论具备资格。

### 反例

候选甲把窄查询维度映射到宽来源完整性域，并自行计算三个证明摘要。没有任何受治理证据边界或独立资格解析拒绝该证明。若竞争集合中只有甲，当前规则允许聚合 `MAPPED`，进而选择宽域的 `COMPLETE` 来源聚合。

```text
Expected: unqualified proof evidence -> INDETERMINATE
Current: unique registered candidate with opaque proof digests may map
Result: TM-R5-B1 reproduced
```

### 关闭条件

`CR-0006-R6` 必须：

1. 定义受治理映射证据边界及独立完整性解析；
2. 定义证明资格稳定键，固定映射语义键、候选载荷、证据边界、完整性和资格规则；
3. 建立候选、登记尝试和四值证明资格解析；
4. 只有适用、完整、无冲突且覆盖精确维度、来源域、作用域和边界形态的资格解析可以进入映射竞争集合；
5. 证据缺失、读取失败或完整性未知必须 `INDETERMINATE`；
6. 同键异证明资格或异结论必须 `CONFLICTED`。

```text
TM-R5-B1 Governed Mapping Proof Qualification: BLOCKED
```

## 四、有界阻断 TM-R5-B2：评价未固定映射聚合的时间治理边界

映射聚合记录被追加到 `Temporal Mapping Ledger`，其聚合登记解析固定一个映射账本边界。但 `Required Dimension Mapping Aggregate Resolution Tuple` 只固定：

```text
Required Dimension ID and Version
Registered Mapping Aggregate Registration Resolution ID and Digest
Mapping Aggregate Payload Digest
Mapping Semantic Result
Mapped Source Completeness Semantic Domain Key and Digest
```

时间完整性评价键也只固定映射元组集合，没有固定：

```text
Registered Temporal Governance Boundary Vector T ID and Digest
T.Mapping Ledger Boundary ID and Digest
Mapping Aggregate Eligibility under T
Historical or Current Temporal View Mode
```

因此“已登记聚合”没有被约束到查询所声明的时间治理边界。

### 反例

时间映射账本在边界 `T1` 时只有映射 `Dimension D -> Domain A`，聚合结果为 `MAPPED`。边界扩展到 `T2` 后出现 `D -> Domain B`，当前聚合为 `CONFLICTED`。

评价者在当前重述中仍可选择 `T1` 下旧的 `MAPPED A` 登记解析，因为映射元组和评价键没有固定当前使用的 `T2` 或查询明确声明的历史 `T1`。

```text
Expected: evaluation pins exact temporal governance boundary vector
Current: registered aggregate selectable without T eligibility
Result: TM-R5-B2 reproduced
```

### 关闭条件

`CR-0006-R6` 必须：

1. 映射元组和完整性评价键固定精确 `Registered Temporal Governance Boundary Vector T ID and Digest`；
2. 固定 `T` 中的映射账本边界及必要完整性解析；
3. 映射候选、竞争边界和聚合记录必须证明对该 `T` 有资格且内容同一；
4. 历史评价显式固定历史 `T`，当前重述使用新的已登记 `T`，不能静默沿用旧聚合；
5. 无法建立适用 `T` 或映射资格时必须 `INDETERMINATE`；
6. `T` 变化必须产生新的映射元组、时间评价和认识边界身份。

```text
TM-R5-B2 Temporal Governance Boundary Pinning for Mapping Consumption: BLOCKED
```

## 五、回归与退出判定

未发现 R5 对以下既有方向造成其他回归：

```text
Correction / Migration Boundary and Aggregate Identity: PASS
Registered Source Completeness Aggregate Consumption: PASS
Temporal Governance Contract Roots: PASS
Canonical Temporal Value Identity: PASS
Original Mapping Semantic Conflict Aggregation: PASS
Coordinate Registry Boundary Identity: PASS
Temporal-ledger Append-only Direction: PASS
Knowledge Boundary Type Closure: PASS
Historical / Current Separation Direction: PASS_WITH_MAPPING_BOUNDARY_LIMITATION
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0006-R5 Independent Model Re-review: COMPLETED
Original Two Blockers: ONE_CLOSED + ONE_CLOSED_WITH_TWO_RESIDUALS
Residual Bounded Blockers: 2
CR-0006-R6 Required: YES
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Runtime Authority: NOT_CREATED
```
