# CR-0006-R8 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 through CR-0006-R8
Repair Basis: CR-0006-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R8 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0006-R8` 的时间记录类型目录、目录生效切点和账本类型资格。它不修改被审提案，不审查 `CR-0005-R9`，不执行联合接口回归，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. R5、R6、R7 的时间记录类型是否形成精确、合法的目录映射；
2. 目录合同和生效切点是否位于时间账本之外并避免自举；
3. 同一前驱目录的全部候选生效切点是否共同竞争；
4. 类型资格、位置分配和记录登记是否原子内容同一；
5. 跨目录账本边界、完整性、`T` 和历史解释是否固定目录谱系；
6. 全局位置模型和 `T` 范围覆盖是否保持不变；
7. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 through CR-0006-R7
CR-0006-R8 TEMPORAL RECORD TYPE CATALOG EVOLUTION CLOSURE
CR-0006-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级关闭声明均不作为通过依据。

## 总体裁决

R8 已完成记录类型资格主体：

```text
R5 Seven-type Baseline Catalog: PASS
R6 Three Proof Record Mappings: PASS
R7 Three Claim-proof Record Mappings: PASS
Exact Thirteen-type Successor Catalog: PASS
Governance Registry / Temporal Ledger Separation: PASS
Catalog Contract Registration Chain: PASS
Record-type Eligibility: PASS
Position-key Preservation: PASS
Ledger Boundary Catalog Lineage: PASS
Catalog Completeness Dimensions: PASS
T-scoped Coverage as Non-ledger Subobject: PASS
G0 through M4 Acyclicity: PASS
```

但目录演进语义键包含已登记生效切点向量，而切点向量自己的键又包含精确切点集合。同一前驱目录可以用不同切点形成互不竞争的切点解析和目录语义键，两个平行后继分别得到 `REGISTERED`。R8-14 的“同一前驱多个不兼容后继必须冲突”因此没有统一竞争边界。

因此：

```text
TM-R7-B1 Record Type Mapping Subject: CLOSED
Temporal Catalog Successor-slot and Effective-cut Competition: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R9 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：十三类记录的目录映射

R8 以 `TEMPORAL_RECORD_TYPE_CATALOG` 时间治理合同承接 R5 的七种封闭映射，并精确追加 R6/R7 六种证明记录：

```text
R5 baseline: 7 record types
R6 proof records: 3 record types -> MAPPING
R7 claim-proof records: 3 record types -> MAPPING
Successor exact total: 13 record types
```

目录合同、切点、边界和聚合位于时间治理注册表，不进入更正、迁移或映射账本。R7 的覆盖资格继续作为评价子对象，不被默认为新时间记录。

```text
Undeclared Proof Record Type: CLOSED
New Temporal Ledger Type: NOT_CREATED
Type-specific Position Partition: NOT_CREATED
Catalog Self-registration through Mapping Ledger: NONE_FOUND
TM-R7-B1 Type Mapping Subject: PASS
```

## 二、已通过：类型资格、位置和账本边界谱系

记录类型资格固定目录聚合、账本身份、记录类型、规范判别载荷和位置引用，使用：

```text
PERMITTED
NOT_PERMITTED
INDETERMINATE
CONFLICTED
```

位置分配与记录登记原子固定目录资格；非 `PERMITTED` 不能取得位置或形成确定登记。目录字段不进入：

```text
Temporal Ledger ID and Version
Temporal Ledger Type
Append Epoch
Position Value
```

每个账本边界固定精确目录解析集合、成员到目录映射和类型资格集合。跨目录边界允许存在，但旧位置保持原目录解释；`T` 只通过已登记映射账本边界继承目录谱系。

```text
Global Position Identity: PASS
Historical Position Reclassification: PROHIBITED
Mixed-catalog Boundary Lineage: PASS
T Reverse Catalog Selection: PROHIBITED
```

以上通过项依赖唯一目录后继；切点竞争残余见下一节。

## 三、有界阻断 TM-R8-B1：生效切点分割目录后继竞争槽

R8 的生效切点向量键包含：

```text
Exact Per-ledger Effective Cut Set
```

而目录演进语义键又固定：

```text
Registered Predecessor Catalog Aggregate Registration Resolution
Registered Catalog Effective-cut Vector
```

因此不同精确切点先产生不同切点向量键，再产生不同目录演进语义键。目录竞争边界只覆盖相同目录语义键，无法同时看见同一前驱的其他切点候选。

R8-14 虽禁止同一前驱多个不兼容后继，但其冲突聚合已被候选切点预先分域。

### 反例

已有唯一目录前驱 `C0`。两个后继候选都追加相同六种证明记录，但声明不同映射账本生效切点：

```text
C1-A: first eligible mapping position = P100
C1-B: first eligible mapping position = P200
```

因为精确切点集合不同：

```text
Effective-cut Vector Key(A) != Effective-cut Vector Key(B)
Catalog Evolution Key(C1-A) != Catalog Evolution Key(C1-B)
```

两个目录竞争边界互不可见，各自均可能形成内外层 `REGISTERED`。位置 `P150` 在一条目录谱系中允许新证明类型，在另一条谱系中仍由旧目录解释；后续账本边界可以按有利目录谱系建立成员资格。

```text
Expected: all immediate successors of C0 compete over mapping and effective cut
Current: candidate cut vector partitions the successor slot
Result: TM-R8-B1 reproduced
```

### 关闭条件

`CR-0006-R9` 必须：

1. 定义目录后继槽语义键，只固定目录谱系根、唯一已登记前驱目录解析、受治理账本集合和已登记演进规则合同；
2. 从后继槽语义键排除生效切点向量、精确切点集合、目录合同 ID／版本和候选映射摘要；
3. 为切点定义候选载荷，使不同精确切点成为同一后继槽内的竞争候选；
4. 一个完整竞争边界同时覆盖全部候选映射和全部候选切点；
5. 唯一后继聚合同时选择目录映射与生效切点；同一前驱多个不兼容组合必须 `CONFLICTED`；
6. 后续合法演进必须以前一已选择后继为新前驱，不能继续从旧前驱选择较晚切点；
7. 类型资格只能固定该唯一后继聚合选中的切点，目录非唯一时不得 `PERMITTED`；
8. 位置候选到已分配位置必须形成内容同一证明，防止在切点两侧改变资格身份；
9. 历史边界继续固定旧目录，后继切点不得重解释旧位置。

```text
TM-R8-B1 Temporal Catalog Successor-slot and Effective-cut Competition: BLOCKED
Closure Owner: CR-0006-R9
```

## 四、回归与退出判定

未发现 R8 对以下既有方向造成其他内部回归：

```text
Correction / Migration Record Mapping: PASS
Mapping Candidate / Boundary / Aggregate Identity: PASS
Governed Mapping Proof: PASS
Claim-level Adverse Proof Aggregation: PASS
T-scoped Aggregate Coverage: PASS
Temporal Governance Boundary Vector T: PASS
Knowledge Boundary K: PASS
Authority Non-propagation: PASS
Institution Freeze Separation: PASS
```

当前决定：

```text
CR-0006-R8 Independent Model Re-review: COMPLETED
Original Record-type Catalog Blocker Subject: CLOSED
Residual Bounded Blockers: 1
CR-0006-R9 Required: YES
Cross-interface Regression Review: STILL_REQUIRED
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
