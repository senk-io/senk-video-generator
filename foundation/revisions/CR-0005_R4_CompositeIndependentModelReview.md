# CR-0005-R4 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 + CR-0005-R2 + CR-0005-R3 + CR-0005-R4
Repair Basis: CR-0005-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R4 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0005-R4` 对四项既有内部阻断的修复是否完整。它不修改被审提案，不重新裁决时间模型，也不创建注册表、解析记录、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 注册表标识分配与契约登记根是否闭合；
2. 来源身份、版本记录和位置是否进入不可逃逸的共同冲突域；
3. 完整性评价是否跨证据边界聚合且不能选择有利评价；
4. 适用性变化是否跨决定事实聚合；
5. 生命周期顺序或替代解析是否拥有可登记、可重放且内容同一的稳定身份；
6. 已通过的来源边界、快照、开放世界、原始断言和四值查询主体是否回归；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 RAW TEMPORAL ASSERTION AND COORDINATE CLOSURE
CR-0005-R2 COORDINATE REGISTRATION RESOLUTION PINNING
CR-0005-R3 FOUR-VALUE COORDINATE SUBJECT CLOSURE
CR-0005-R4 INTERNAL REGISTRATION AND CONFLICT AGGREGATION CLOSURE
CR-0005-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

提案自检、规则数量、文件存在和作者声明均不作为通过依据。

## 总体裁决

R4 已实质关闭原四项阻断的主体：

```text
SR-M1 Registry Root Bootstrap: CLOSED
SR-M2 Source Identity / Version Conflict Domain: CLOSED
SR-M3 Completeness Conflict Aggregation: CLOSED
SR-M4 Applicability Change Conflict Domain: CLOSED_WITH_ONE_RESIDUAL_BLOCKER
```

已通过方向：

```text
Registry ID Allocation Identity: PASS
Registry Contract Registration Chain: PASS
Registry Contract Boundary and Completeness: PASS
Source Identity Allocation and Non-reuse: PASS
Source Version Semantic Conflict Set: PASS
Competing-record Boundary Identity: PASS
Source Version Aggregate Resolution: PASS
Completeness Semantic-domain Separation: PASS
Completeness Evaluation Boundary: PASS
Completeness Aggregate Resolution: PASS
Applicability Change Conflict Set: PASS
Applicability Change Set Boundary: PASS
Closed Aggregate State Set: PASS
Authority Non-propagation: PASS
Previously Passed Source-model Backbone: PASS
```

但 `SR-R4-24` 允许“已登记、内容同一的生命周期顺序或替代解析”把不兼容生命周期组合解析为唯一确定状态，却没有定义该解析的稳定键、候选—登记链、完整输入边界和冲突解析。因此同一变化集合可以引用不同的表面“已登记解析”并得到不同后继状态，且模型没有共同身份将其归入冲突。

```text
Independent Model Re-review: FAIL
CR-0005-R5 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、SR-M1 复验：注册表根启动闭合

R4 定义了注册表标识分配稳定键、候选、尝试、记录、登记解析和四值结果，并把命名空间、预期域、契约摘要与规则版本固定进分配身份。

契约登记进一步固定：

```text
Registered ALLOCATED Registry ID Resolution
  -> Candidate Source Registry Contract
  -> Contract Registration Attempt
  -> Registered Contract Record
  -> Source Registry Contract Registration Resolution
```

契约注册表边界拥有稳定键、精确范围或记录集合摘要、作用域、空洞、冲突子域和独立完整性评价。同键异载荷不能按登记时间选赢家。

```text
Allocation Bootstrap: PASS
Contract Content Identity: PASS
Qualified NOT_REGISTERED: PASS
Self-authorization Prohibition: PASS
SR-M1 Result: CLOSED
```

## 二、SR-M2 复验：来源身份和版本竞争域闭合

来源身份分配拥有不可复用身份和四值解析。来源版本语义冲突键明确排除记录 ID、位置、登记时间、写入者、尝试和证据集合。

竞争记录边界固定全部同域候选、登记尝试、已登记记录和冲突记录，并绑定冲突子域完整性。聚合解析只按语义竞争键比较载荷，不按记录包或位置选择赢家。

```text
Identity Allocation Non-reuse: PASS
Record-package Escape: CLOSED
Position-based Winner Selection: PROHIBITED
Aggregate Registration Resolution: PASS
SR-M2 Result: CLOSED
```

## 三、SR-M3 复验：完整性聚合闭合

R4 把完整性语义域与证据集合分离，并建立：

```text
Source Completeness Semantic Domain Key
  -> Source Completeness Evidence Evaluation Key
  -> Source Completeness Evaluation Boundary Key
  -> Source Completeness Aggregate Resolution Key
```

不同证据边界的评价进入同一完整语义域。完整评价边界固定精确评价记录集合并要求独立完整性；聚合结果保持 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`，不能挑选单一有利证据。

```text
Evidence-set Key Escape: CLOSED
Complete / Incomplete Competition: PASS
Unknown Boundary Failure Closure: PASS
SR-M3 Result: CLOSED
```

本通过项只说明来源侧内部聚合对象完整；其跨接口消费另由联合回归审查裁决。

## 四、SR-M4 主体复验：变化竞争集合闭合

适用性变化语义键排除决定事实、变化记录、位置、登记时间和写入者。完整变化集合边界固定精确已登记变化解析集合及必要完整性，并覆盖激活、暂停、退役、替代与撤销。

聚合状态封闭为：

```text
ACTIVE
SUSPENDED
RETIRED
SUPERSEDED
REVOKED
NO_APPLICABLE_CHANGE
INDETERMINATE
CONFLICTED
```

不兼容生命周期组合默认冲突，记录时间、位置和“最新”均不能建立顺序。

```text
Decision-fact Key Escape: CLOSED
Complete Change-set Boundary: PASS
Conflict-first Default: PASS
Applicability Consumption Direction: PASS
```

## 五、有界阻断 SR-R4-B1：生命周期顺序或替代解析缺少稳定身份

`SR-R4-24` 规定，只有存在已登记且内容同一的生命周期顺序或替代解析时，才允许把表面不兼容组合解析为不重叠效果或唯一后继效果。该限制方向正确，但复合模型没有定义：

```text
Lifecycle Ordering / Supersession Resolution Key
Candidate Lifecycle Ordering / Supersession Resolution
Resolution Registration Attempt
Registered Lifecycle Ordering / Supersession Resolution
Competing Resolution Boundary Key
Aggregate Conflict Resolution
```

也没有固定以下最小输入：

```text
Source Applicability Change Conflict Set Key
Registered Change Set Boundary ID and Digest
Exact Ordered or Superseding Member Resolution Set Digest
Effective Interval Semantics
Registered Temporal Coordinate Resolution IDs and Digests
Required Boundary Completeness Resolution IDs and Digests
Ordering / Supersession Rule Version
```

### 反例

同一完整变化集合含 `ACTIVE` 与 `SUPERSEDED`。解析记录甲声称后者是唯一后继，解析记录乙声称两者效果区间重叠。两者均可被表面描述为“已登记”，但当前没有共同解析键、竞争边界或聚合结果迫使它们进入 `CONFLICTED`。

```text
Expected: same-key incompatible resolution payloads -> CONFLICTED
Current: no stable resolution identity or competing-resolution boundary
Result: SR-R4-B1 reproduced
```

### 关闭条件

`CR-0005-R5` 必须：

1. 定义生命周期顺序或替代解析稳定键；
2. 建立候选、登记尝试、内容同一登记记录和四值解析；
3. 建立覆盖全部同域解析的完整竞争边界；
4. 同键异顺序、异区间或异后继载荷必须 `CONFLICTED`；
5. 变化聚合解析必须固定该已登记解析 ID、摘要和完整性，而不能接受裸声明。

```text
SR-R4-B1 Lifecycle Ordering / Supersession Resolution Identity: BLOCKED
```

## 六、回归与退出判定

未发现 R4 对以下既有来源模型主干造成内部回归：

```text
Boundary / Snapshot Reproducibility: PASS
Snapshot Completeness Non-self-proof: PASS
Open-world Absence Safety: PASS
Raw Temporal Assertion Atomic Handoff: PASS
Four-value Coordinate Subject Totality: PASS
Historical / Current Applicability Separation: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0005-R4 Independent Model Re-review: COMPLETED
Original Four Blockers: THREE_CLOSED + ONE_CLOSED_WITH_RESIDUAL
Residual Bounded Blockers: 1
CR-0005-R5 Required: YES
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```
