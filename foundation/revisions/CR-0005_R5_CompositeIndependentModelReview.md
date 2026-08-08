# CR-0005-R5 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 + CR-0005-R2 + CR-0005-R3 + CR-0005-R4 + CR-0005-R5
Repair Basis: CR-0005-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R5 self-check and candidate-level closure declaration were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0005-R5` 是否完整关闭生命周期顺序／替代解析身份阻断。它不修改被审提案，不审查 `CR-0006-R4`，也不创建注册表、生命周期解析、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 生命周期解析注册表引用是否具有稳定、内容同一且不可冒认的根身份；
2. 生命周期候选解析是否拥有稳定键、候选—登记链和四值登记解析；
3. 同一语义域的全部解析是否进入完整竞争边界；
4. 顺序、区间、后继、替代和撤销之间的跨目的矛盾是否共同聚合；
5. 聚合解析是否拥有稳定登记身份并被来源适用性固定消费；
6. 历史、当前、分权和既有来源模型主干是否回归；
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
CR-0005-R5 LIFECYCLE ORDERING AND SUPERSESSION RESOLUTION IDENTITY CLOSURE
CR-0005-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、作者身份和候选级闭合声明均不作为通过依据。

## 总体裁决

R5 已补齐生命周期解析主体链：

```text
Lifecycle Candidate Stable Identity: PASS
Candidate Content-identical Registration: PASS
Candidate Four-value Registration Resolution: PASS
Same-purpose Semantic Conflict Set: PASS
Competing-resolution Boundary Stable Key: PASS
Independent Boundary Completeness: PASS
Aggregate Resolution Stable Key: PASS
Aggregate Registration Resolution: PASS
Closed Semantic Result Set: PASS
Source Applicability Consumption Pinning: PASS
Historical Non-overwrite: PASS
Authority Non-propagation: PASS
```

但存在两个新的有界身份逃逸：

1. `Registered Lifecycle Resolution Registry Reference` 没有稳定键、内容同一登记链，也未明确把其注册表 ID 与分配解析中的候选 ID 一对一绑定；
2. `Lifecycle Resolution Purpose` 被放入语义冲突键，导致顺序、唯一后继、替代目标和撤销优先之间的跨目的矛盾不会进入同一竞争集合，而来源适用性只固定一个生命周期聚合消费引用。

因此：

```text
Registry Reference Root Identity: FAIL_WITH_BOUNDED_BLOCKER
Candidate and Registration Identity: PASS
Same-purpose Conflict Aggregation: PASS
Cross-purpose Conflict Aggregation: FAIL_WITH_BOUNDED_BLOCKER
Aggregate Registration Identity: PASS
Applicability Consumption Pinning: PASS_WITH_CROSS_PURPOSE_LIMITATION
Independent Model Re-review: FAIL
CR-0005-R6 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_TWO_BOUNDED_BLOCKERS
```

## 一、已通过：候选、登记和同目的竞争边界

R5 为生命周期解析建立：

```text
Lifecycle Ordering / Supersession Resolution Semantic Conflict Set Key
Lifecycle Ordering / Supersession Candidate Resolution Key
Lifecycle Candidate Registration Resolution Key
Lifecycle Resolution Competing Record Boundary Key
Lifecycle Resolution Competing Boundary Registration Resolution Key
Lifecycle Ordering / Supersession Aggregate Resolution Key
Lifecycle Aggregate Registration Resolution Key
```

候选载荷固定精确变化成员、前驱／后继边、有效区间、替代或撤销目标、时间坐标解析、受治理证据边界和声称结果。候选 ID 不可复用，候选与登记载荷必须内容同一。

竞争边界固定全部同域候选、登记尝试、登记记录、四值候选解析和冲突谱系，并要求独立覆盖载体、位置或精确集合、读取、冲突子域和语义域。

```text
Payload-key Escape: CLOSED
Evidence-set Escape within Same Purpose: CLOSED
Unfavorable Candidate Exclusion: PROHIBITED
Boundary Self-proof: PROHIBITED
Same-key Incompatible Aggregate Payload: CONFLICTED
```

## 二、已通过：聚合登记和来源适用性消费方向

生命周期聚合语义结果封闭为：

```text
RESOLVED
NOT_RESOLVED
INDETERMINATE
CONFLICTED
```

最终聚合记录还必须取得：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

来源适用性变化聚合键固定登记解析 ID、摘要和聚合载荷摘要；存在不兼容组合时，裸候选或 `LIFECYCLE_RESOLUTION_NOT_REQUIRED` 不能支持确定状态。

```text
Single Candidate Direct Consumption: PROHIBITED
Bare Ordering Claim: PROHIBITED
NOT_RESOLVED -> CONFLICTED Applicability: PASS
INDETERMINATE Propagation: PASS
Historical Aggregate Pinning: PASS
```

以上通过只适用于同一已建立生命周期语义冲突域；跨目的完整性另见阻断 `SR-R5-B2`。

## 三、有界阻断 SR-R5-B1：解析注册表引用缺少根身份

R5-03 定义：

```text
Registered ALLOCATED Source Registry ID Resolution
+ Registered Source Registry Contract Registration Resolution
+ Lifecycle Resolution Registry ID and Version
+ Lifecycle Resolution Registry Scope Digest
  -> Registered Lifecycle Resolution Registry Reference
```

但没有定义：

```text
Lifecycle Resolution Registry Reference Key
Candidate Lifecycle Resolution Registry Reference
Registry Reference Registration Attempt
Registered Registry Reference Registration Resolution
Candidate Source Registry ID = Lifecycle Resolution Registry ID binding
Registry Reference Conflict Boundary and Completeness
```

“输入中存在一个已分配来源注册表 ID”不等于证明该分配解析正好分配了所声称的生命周期解析注册表 ID。输出又被称为 `Registered`，但没有候选、登记或四值解析证明其内容同一。

### 反例

同一个有效分配解析实际绑定注册表 `A`。执行者甲把它与生命周期注册表 `B` 组合，执行者乙把它与注册表 `C` 组合，两者都声称形成已登记引用。当前没有稳定引用键、显式相等绑定或共同冲突边界拒绝 `B`、`C`。

```text
Expected: allocation candidate ID must equal lifecycle registry ID
Expected: same reference key with incompatible payload -> CONFLICTED
Current: unkeyed Registered Lifecycle Resolution Registry Reference
Result: SR-R5-B1 reproduced
```

### 关闭条件

`CR-0005-R6` 必须：

1. 定义生命周期解析注册表引用稳定键；
2. 显式固定分配解析 ID、摘要及其候选注册表 ID，并要求与生命周期注册表 ID 内容同一；
3. 固定契约登记解析、作用域、记录类型、规则载荷和引用规则版本；
4. 建立候选、登记尝试、完整引用边界和四值登记解析；
5. 同键异作用域、异合同或异注册表绑定必须 `CONFLICTED`；
6. 所有候选、边界和聚合键必须固定该已登记引用解析 ID 与摘要。

```text
SR-R5-B1 Lifecycle Resolution Registry Reference Identity: BLOCKED
```

## 四、有界阻断 SR-R5-B2：解析目的隔离跨目的矛盾

R5 把以下字段放入语义冲突键：

```text
Lifecycle Resolution Purpose
```

其值分别包括：

```text
EFFECT_INTERVAL_ORDERING
UNIQUE_SUCCESSOR
SUPERSESSION_TARGET
REVOCATION_PRECEDENCE
```

这可以隔离同一变化集合和查询坐标下的跨目的矛盾。每个目的内部都可能得到独立 `RESOLVED`，但模型没有父级生命周期一致性键、跨目的完整解析向量或组合聚合解析。来源适用性消费引用又是单数，无法证明其他适用目的不存在相反结论。

### 反例

同一变化集合中：

```text
EFFECT_INTERVAL_ORDERING
  -> resolves A before B and B effective now

SUPERSESSION_TARGET
  -> resolves A as the unique superseding target of B and A effective now
```

两份解析的变化集合、查询坐标和合同相同，但因目的不同进入不同语义键。两者都可以分别 `RESOLVED + REGISTERED`，来源适用性可以固定其中一个并产生相反当前状态。

```text
Expected: incompatible cross-purpose claims -> common CONFLICTED result
Current: purpose-partitioned keys + singular consumption reference
Result: SR-R5-B2 reproduced
```

### 关闭条件

`CR-0005-R6` 必须选择以下闭合形态之一：

1. 从最终生命周期语义冲突键移除目的，使所有可比较声明直接竞争；或
2. 保留逐目的子解析，但建立父级生命周期一致性键、必要目的资格集合、完整逐目的解析向量和跨目的聚合解析。

无论采用哪种形态，都必须：

- 固定同一变化集合、查询坐标、合同和必要目的集合；
- 证明全部适用目的已覆盖；
- 顺序、区间、后继、替代与撤销之间的不兼容载荷必须 `CONFLICTED`；
- 来源适用性只能消费已登记父级组合解析，不能选择单一有利目的。

```text
SR-R5-B2 Cross-purpose Lifecycle Resolution Aggregation: BLOCKED
```

## 五、回归与退出判定

未发现 R5 对以下既有来源模型方向造成其他回归：

```text
Registry Contract Bootstrap Direction: PASS
Source Version Conflict Aggregation: PASS
Source Completeness Aggregate Resolution: PASS
Applicability Change Conflict Set: PASS
Boundary / Snapshot Reproducibility: PASS
Open-world Absence Safety: PASS
Raw Temporal Assertion Atomic Handoff: PASS
Four-value Coordinate Subject Totality: PASS
Historical / Current Separation: PASS
Authority Non-propagation: PASS
```

当前决定：

```text
CR-0005-R5 Independent Model Re-review: COMPLETED
Original Residual Blocker: PARTIALLY_CLOSED
New Bounded Blockers: 2
CR-0005-R6 Required: YES
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
