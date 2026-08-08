# CR-0006-R4 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 + CR-0006-R2 + CR-0006-R3 + CR-0006-R4
Repair Basis: CR-0006-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Basis: CR-0005-R4-CR-0006-R3-CROSS-INTERFACE-REGRESSION-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R4 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0006-R4` 是否完整关闭更正／迁移边界聚合身份及来源完整性聚合消费阻断。它不修改被审提案，不审查 `CR-0005-R5`，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 更正、迁移边界是否拥有稳定键、完整成员集合和内容同一登记解析；
2. 更正、迁移聚合是否拥有稳定键、四值登记身份和冲突优先语义；
3. 新增时间记录分区是否与既有位置键、边界键和不可复用约束一致；
4. 时间完整性评价是否只能消费来源侧已登记聚合解析；
5. 必要维度到来源完整性语义域的映射是否稳定、完整且不能选择有利域；
6. 历史、当前、权威边界和既有时间模型主干是否回归；
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
CR-0006-R1 KNOWLEDGE BOUNDARY AND TEMPORAL LEDGER CLOSURE
CR-0006-R2 DERIVED EVALUATION AND COORDINATE REGISTRATION CLOSURE
CR-0006-R3 INTERNAL GOVERNANCE AND SEMANTIC CONFLICT CLOSURE
CR-0006-R4 CORRECTION MIGRATION BOUNDARY AGGREGATE AND SOURCE COMPLETENESS CONSUMPTION CLOSURE
CR-0006-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
CR-0005-R4-CR-0006-R3-CROSS-INTERFACE-REGRESSION-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、作者身份和候选级闭合声明均不作为通过依据。

## 总体裁决

R4 已建立更正和迁移边界／聚合主体身份，并移除时间侧直接选择底层来源完整性记录的旧消费路径：

```text
Correction Competing Boundary Stable Key: PASS
Correction Boundary Registration Resolution: PASS
Correction Aggregate Stable Key: PASS
Correction Aggregate Registration Resolution: PASS
Migration Competing Boundary Stable Key: PASS
Migration Boundary Registration Resolution: PASS
Migration Aggregate Stable Key: PASS
Migration Aggregate Registration Resolution: PASS
Conflict-first Semantic Results: PASS
Historical Non-overwrite: PASS
Direct Source Completeness Record Selection: PROHIBITED
Registered Source Completeness Aggregate Pinning: PASS
Source / Time Authority Separation: PASS
```

但仍有两个有界身份缺口：

1. R4 新增四类独立时间记录分区，却没有定义分区稳定键；既有位置键也不含 `Temporal Record Type`，无法同时支持“独立位置子域”和全局位置不可复用；
2. 必要维度到来源完整性语义域的映射只存在于评价元组中，没有稳定交叉映射键、登记解析或共同冲突域。不同有利映射会形成不同评价键并逃离冲突。

因此：

```text
Correction / Migration Boundary and Aggregate Identity: PASS_WITH_PARTITION_LIMITATION
Temporal Record Partition and Position Identity: FAIL_WITH_BOUNDED_BLOCKER
Direct Aggregate Consumption: PASS
Required-dimension Coverage: PASS_WITH_MAPPING_LIMITATION
Dimension / Source-domain Mapping Identity: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R5 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
```

## 一、已通过：更正边界与聚合主体

R4 为时间更正建立：

```text
Temporal Correction Competing Record Boundary Key
Temporal Correction Boundary Registration Resolution Key
Temporal Correction Aggregate Resolution Key
Temporal Correction Aggregate Registration Resolution Key
```

竞争边界固定语义冲突键、时间更正账本边界、精确合格成员集合、完整性和已登记边界规则合同。边界候选、登记尝试、记录和四值解析必须内容同一。

聚合解析固定已登记边界解析、完整性、已登记聚合规则合同和规则版本；同键异结果、异成员或异载荷必须 `CONFLICTED`。

```text
Request-ID Escape: CLOSED
Unfavorable Correction Exclusion: PROHIBITED
Boundary Self-proof: PROHIBITED
APPLIED / NOT_APPLIED / INDETERMINATE / CONFLICTED: PASS
```

## 二、已通过：迁移边界与聚合主体

R4 为时间迁移建立：

```text
Temporal Migration Competing Record Boundary Key
Temporal Migration Boundary Registration Resolution Key
Temporal Migration Aggregate Resolution Key
Temporal Migration Aggregate Registration Resolution Key
```

不同目标合同仍在同一迁移语义域竞争。边界和聚合均固定精确成员、完整性、已登记规则合同和内容同一登记解析。

```text
Decision-ID Escape: CLOSED
Target-contract Key Escape: CLOSED
Unfavorable Migration Exclusion: PROHIBITED
MIGRATED / NOT_MIGRATED / INDETERMINATE / CONFLICTED: PASS
```

上述更正、迁移主体通过项仍受其承载分区身份阻断限制。

## 三、有界阻断 TM-R4-B1：新增记录分区与既有位置键不一致

R4 新增：

```text
Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Required Registered Temporal Governance Contract Registration Resolution IDs and Digests
+ Temporal Record Type
  -> Registered Append-only Temporal Record Partition
```

并规定四种记录类型拥有独立位置子域。但复合模型既有位置键仍是：

```text
Temporal Derived Record Position Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

该键没有 `Temporal Record Type` 或已登记分区引用。R4 也没有定义：

```text
Temporal Record Partition Key
Partition Candidate / Registration Attempt
Registered Partition Registration Resolution
Partition Position Namespace ID and Version
Partition Boundary and Completeness
```

### 反例

同一 `Temporal Correction Ledger`、同一追加纪元中：

```text
TEMPORAL_CORRECTION_COMPETING_BOUNDARY at position 7
TEMPORAL_CORRECTION_AGGREGATE_RESOLUTION at position 7
```

若“独立位置子域”允许各类型从位置 7 开始，两条记录的既有位置键完全相同，违反位置不可复用。若实际要求账本全局位置唯一，则 R4 所称独立分区和分区边界没有稳定身份证明记录属于哪个子域。

```text
Expected: registered partition identity participates in position and boundary keys
Current: unkeyed partition + position key without Temporal Record Type
Result: TM-R4-B1 reproduced
```

### 关闭条件

`CR-0006-R5` 必须选择并固定一种模型：

1. 若记录类型拥有独立位置域，定义 `Temporal Record Partition Key`、分区候选—登记四值解析和不可复用位置命名空间，并收紧位置键与边界键固定已登记分区解析；或
2. 若所有记录类型共享账本全局位置域，删除“独立位置子域”和独立已登记分区对象，明确记录类型只是载荷判别字段，并证明边界完整覆盖同账本位置域。

任一模型都必须防止记录类型、分区或位置换键逃离冲突和完整性边界。

```text
TM-R4-B1 Temporal Record Partition and Position Identity: BLOCKED
```

## 四、已通过：来源完整性聚合直接消费

R4 明确撤销时间评价对下列旧字段的直接消费资格：

```text
Exact Registered Source Completeness Record Set Digest
```

时间评价现在固定每个来源完整性聚合解析的 ID、摘要、结果、评价边界和边界完整性。`INDETERMINATE | CONFLICTED` 失败关闭，`INCOMPLETE` 只能支持 `NOT_SATISFIED`，底层记录集合只能保留为只读谱系。

```text
Selected COMPLETE Record Bypass: CLOSED
Aggregate ID and Digest Pinning: PASS
Aggregate Result Propagation: PASS
Source Aggregate Recalculation by Time Side: PROHIBITED
```

该通过项证明时间侧不能绕过已经选定的来源聚合解析，但尚不能证明必要维度到来源语义域的选择唯一。

## 五、有界阻断 TM-R4-B2：必要维度到来源语义域映射没有稳定身份

R4 定义评价元组：

```text
Required Dimension ID and Version
+ Source Completeness Semantic Domain Key and Digest
+ Registered Source Completeness Aggregate Resolution ID and Digest
+ Source Completeness Aggregate Result
+ Registered Source Completeness Evaluation Boundary ID and Digest
+ Required Evaluation-boundary Completeness Resolution IDs and Digests
```

并要求每个必要维度恰好对应一个元组。但模型没有定义：

```text
Required Dimension / Source Completeness Domain Mapping Key
Mapping Candidate / Registration Attempt
Registered Mapping Resolution
Complete Competing Mapping Boundary
Cross-mapping Aggregate Resolution
```

`Exact Required Source Completeness Aggregate Resolution Tuple Set Digest` 被放入 `Completeness Requirement Evaluation Key`。因此两个不同映射集合会产生两个不同评价键，而不是进入同一评价冲突集合。逐评价内部的一一对应不能阻止查询者选择一个有利的跨域映射。

### 反例

同一要求集合中的必要维度 `READ_COMPLETENESS` 可以被两个执行者分别映射到：

```text
Domain A: broad source scope -> Aggregate Result COMPLETE
Domain B: exact query scope -> Aggregate Result CONFLICTED
```

每份元组集合内部都只有一个 `READ_COMPLETENESS` 元组，因此表面满足一一对应。因为语义域集合摘要和元组集合摘要不同，两份评价形成不同稳定键；模型没有共同映射解析迫使它们冲突，消费者可以选择 `Domain A` 得到 `SATISFIED`。

```text
Expected: same requirement dimension and query scope have one registered domain mapping
Current: mapping exists only inside evaluation-specific tuple set
Result: TM-R4-B2 reproduced
```

### 关闭条件

`CR-0006-R5` 必须：

1. 定义必要维度到来源完整性语义域的稳定映射键，至少固定已登记要求集合、维度、查询作用域、边界形态、来源边界和最低矩阵合同解析；
2. 建立候选、登记尝试、完整竞争边界和四值映射解析；
3. 同键异语义域、异作用域或异来源边界必须 `CONFLICTED`；
4. 证明全部必要维度映射已完整且一一对应；
5. 完整性评价键固定已登记映射解析 ID、摘要和由其导出的精确来源聚合元组集合；
6. 查询者不能临时构造或选择映射以绕过不利来源聚合。

```text
TM-R4-B2 Required Dimension / Source Completeness Domain Mapping Identity: BLOCKED
```

## 六、回归与退出判定

未发现 R4 对以下既有时间模型方向造成其他回归：

```text
Temporal Governance Contract Roots: PASS
Canonical Temporal Value Identity: PASS
Mapping Semantic Conflict Aggregation: PASS
Coordinate Registry Boundary Identity: PASS
Raw Assertion Provider Identity: PASS
Temporal-ledger Append-only Direction: PASS_WITH_PARTITION_LIMITATION
Knowledge Boundary Type Closure: PASS
Historical / Current View Separation: PASS
Four-stage Acyclicity: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0006-R4 Independent Model Re-review: COMPLETED
TM-R3-B1: CLOSED_WITH_ONE_PARTITION_RESIDUAL
XREG-B1: CLOSED_WITH_ONE_MAPPING_RESIDUAL
New Bounded Blockers: 2
CR-0006-R5 Required: YES
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Runtime Authority: NOT_CREATED
```
