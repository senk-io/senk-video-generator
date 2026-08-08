# CR-0006-R9 时间映射治理复合模型独立复审

## 审查信息

```text
Review ID: CR-0006-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0006 + CR-0006-R1 through CR-0006-R9
Repair Basis: CR-0006-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-03
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R9 self-check and candidate-level closure declaration were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0006-R9` 的目录后继槽、映射—切点联合选择和规范位置主体。它不修改被审提案，不审查 `CR-0005-R10`，不执行联合接口回归，也不创建时间制度对象、账本、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 同一前驱的全部目录映射和生效切点是否共同竞争；
2. 唯一聚合是否不可分割地选择映射与切点；
3. 后续演进是否只能使用已选择后继作为新前驱；
4. 候选位置与已分配位置是否共享规范主体并重新确认资格；
5. 账本边界、历史位置和 `T` 是否固定唯一目录后继；
6. 后继槽新增治理根是否拥有可验证登记资格；
7. `WS-03` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0006 TEMPORAL MAPPING GOVERNANCE
CR-0006-R1 through CR-0006-R8
CR-0006-R9 CATALOG SUCCESSOR-SLOT AND CUT COMPETITION CLOSURE
CR-0006-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级关闭声明均不作为通过依据。

## 总体裁决

R9 已关闭候选切点分割后继槽的问题：

```text
Predecessor-only Catalog Successor Slot: PASS
Effective Cut Excluded from Slot Key: PASS
Cut as Candidate Subobject: PASS
Mapping + Cut Combined Candidate: PASS
Complete Cross-cut Competition: PASS
Unique Joint Successor Selection: PASS
Registered Outer Successor Resolution: PASS
Selected Successor as Next Predecessor: PASS
Canonical Position Qualification Subject: PASS
Candidate-to-allocated Position Equality: PASS
Ledger Boundary Successor Pinning: PASS
T Inheritance and Historical Replay: PASS
```

但后继槽和唯一聚合键新增 `Registered Catalog Lineage Governance Root ID and Digest`，而 R9/R8 都没有定义该治理根的候选、登记、完整竞争边界或四值解析。不同裸治理根可以把同一目录谱系和前驱重新拆成多个互不可见的后继槽。

因此：

```text
TM-R8-B1 Successor Cut Competition Subject: CLOSED
Temporal Catalog Lineage Governance-root Registration: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0006-R10 Required: YES
WS-03 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：映射和切点联合竞争

R9 的后继槽只固定目录谱系和唯一前驱，明确排除生效切点、精确映射、目录版本和候选摘要。

R8 的切点向量被降为后继候选子对象。精确切点集合变化产生不同候选，但不改变后继槽归属。目录后继候选不可分割地绑定十三类映射与一个精确切点候选。

竞争边界覆盖全部映射—切点组合，唯一聚合同时选择两者：

```text
SELECTED
NOT_SELECTED
INDETERMINATE
CONFLICTED
```

相同映射异合格切点、相同切点异合格映射或多个不兼容组合必须 `CONFLICTED`。后续演进只能使用已选择后继作为新前驱。

```text
Same Predecessor / Different Cuts: COMMON_COMPETITION_DOMAIN
Caller-selected Cut after Catalog Selection: PROHIBITED
Parallel Later Successor from Old Predecessor: CONFLICTED
TM-R8-B1 Candidate-cut Partition: CLOSED
```

## 二、已通过：规范位置主体和账本谱系

R9 将候选／已分配位置统一为：

```text
Canonical Temporal Position Qualification Subject Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

候选资格不能单独授权记录登记。最终登记重新验证已分配位置与候选位置内容同一，并固定唯一目录后继、所选切点及最终 `PERMITTED`。

账本边界保存前驱目录、已选择后继、切点载荷、成员归属和位置主体。`T` 只通过映射账本边界继承，不取得目录选择权。

```text
Candidate / Allocated Position Identity: PASS
Global Position Key Preservation: PASS
Historical Position Reclassification: PROHIBITED
T Reverse Catalog Selection: PROHIBITED
```

## 三、有界阻断 TM-R9-B1：目录谱系治理根缺少登记拓扑

目录后继槽包含：

```text
Registered Catalog Lineage Governance Root ID and Digest
Catalog Successor-slot Semantic Rule ID
```

唯一后继聚合键再次固定：

```text
Registered Catalog Lineage Governance Root ID and Digest
Catalog Successor Aggregate Semantic Rule ID fixed by Governance Root
```

R9 只声明治理根不可变、规则 ID 由其固定，却没有定义：

```text
Governance Root Semantic Conflict Set Key
Root Candidate Payload and Stable Candidate Key
Root ID Allocation / Registration Attempt
Registered Root Record
Complete Root Competing Boundary and Completeness
Four-value Root Aggregate Registration Resolution
```

R8 的 `Temporal Record-type Catalog Lineage Root Key` 只是逻辑键，不会自动产生 R9 所引用的 `Registered Catalog Lineage Governance Root`。

### 反例

同一时间目录谱系和前驱 `C0` 下，两个参与者分别声称：

```text
Governance Root G1 with Rule ID S1
Governance Root G2 with Rule ID S2
```

没有根竞争边界能证明二者冲突。后继槽因此变为：

```text
Successor Slot Key(C0, G1) != Successor Slot Key(C0, G2)
```

每个槽都可形成自己的完整映射—切点边界和 `SELECTED` 聚合。后续类型资格可以沿不同裸根引用不同所选切点。

```text
Expected: one governed root per temporal catalog lineage
Current: registered root is referenced but never qualified
Result: TM-R9-B1 reproduced
```

### 关闭条件

`CR-0006-R10` 必须二选一：

1. 删除新增治理根字段，直接使用 R3 已登记时间治理合同根和 R8 既有目录谱系根确定固定规则 ID；或
2. 定义治理根语义键，排除候选根 ID、规则 ID、合同版本和载荷摘要；
3. 建立根候选、ID 分配、登记尝试、内容同一记录、完整竞争边界和四值聚合解析；
4. 同一时间目录谱系的所有根候选必须共同竞争，只有唯一外层 `REGISTERED` 且内层唯一结果可消费；
5. 后继槽和唯一聚合固定精确根聚合解析，而不是裸 `Registered ... ID and Digest`；
6. 规则 ID、边界规则和聚合规则来自该唯一根载荷，不得由目录候选提供；
7. 根解析未知或冲突时，目录后继、类型资格、位置分配和账本边界必须失败关闭；
8. 根登记位于 R3 时间治理合同注册表，不进入任何时间账本，避免自举循环。

```text
TM-R9-B1 Temporal Catalog Lineage Governance-root Registration: BLOCKED
Closure Owner: CR-0006-R10
```

## 四、回归与退出判定

未发现 R9 对以下既有方向造成其他内部回归：

```text
R5 Seven-type Baseline Catalog: PASS
R6 / R7 Six Proof Record Mappings: PASS
Exact Thirteen-type Successor Catalog: PASS
Global Temporal Position Identity: PASS
Ledger Boundary Catalog Lineage: PASS_WITH_ROOT_BLOCKER
T-scoped Aggregate Coverage: PASS
Temporal Governance Boundary Vector T: PASS
Knowledge Boundary K: PASS
Authority Non-propagation: PASS
Institution Freeze Separation: PASS
```

当前决定：

```text
CR-0006-R9 Independent Model Re-review: COMPLETED
Original Successor-cut Blocker: CLOSED
Residual Bounded Blockers: 1
CR-0006-R10 Required: YES
Cross-interface Regression Review: STILL_REQUIRED
WS-03 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
