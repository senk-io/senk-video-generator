# 来源注册表接口有界修订 R5

## 修订信息

```text
Proposal ID: CR-0005-R5
Title: Lifecycle Ordering and Supersession Resolution Identity Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R4 INTERNAL REGISTRATION AND CONFLICT AGGREGATION CLOSURE
Repair Basis: CR-0005-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R4-B1 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Independent Model Re-review Required: YES
Cross-interface Regression Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0006-R4
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R4-B1`：为生命周期顺序或替代解析建立稳定、可登记、可完整聚合且失败关闭的身份。它不覆盖 `CR-0005` 基础稿或 R1 至 R4 的历史正文，不创建任何来源注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R5-01 R5 只覆盖生命周期解析身份缺口

本修订只关闭：

```text
SR-R4-B1 Lifecycle Ordering / Supersession Resolution Identity
```

R4 已通过的注册表根、来源版本竞争、完整性聚合和适用性变化主干继续有效。R5 不改变时间模型拥有的规范时间值、查询坐标或认识边界。

### SR-R5-02 顺序解析不能自授权或自证完整

生命周期解析使用的注册表 ID、合同、边界、证据和规则必须分别来自已分配、已登记且适用的 R4 来源注册表根及 `IF-0006`、`IF-0007` 兼容边界。

```text
Lifecycle Resolution Payload
  -/-> grant its own construction or registration authority
  -/-> prove its own registry boundary completeness
  -/-> create temporal coordinate truth
  -/-> overwrite source change records
```

## 二、生命周期解析注册表根

### SR-R5-03 解析注册表必须复用已闭合根链

```text
Registered ALLOCATED Source Registry ID Resolution
+ Registered Source Registry Contract Registration Resolution
+ Lifecycle Resolution Registry ID and Version
+ Lifecycle Resolution Registry Scope Digest
  -> Registered Lifecycle Resolution Registry Reference
```

解析注册表合同必须明确覆盖顺序、替代、区间、前驱、后继、证据、登记、边界、完整性和聚合规则。未取得 `ALLOCATED + REGISTERED` 的注册表引用不能接收候选解析。

解析注册表不能通过自身载荷扩大 R4 来源注册表合同中的授权或作用域。

### SR-R5-04 解析规则必须固定已登记合同解析

每个生命周期解析必须固定：

```text
Registered Source Registry Contract Registration Resolution ID and Digest
Lifecycle Resolution Rule Contract Payload Digest
Lifecycle Resolution Rule Version
```

生命周期规则合同载荷必须是上述已登记来源注册表契约中的不可变、内容寻址子对象，不形成第二个独立合同根。裸规则版本、实现名称或“最新规则”不能替代契约解析与载荷摘要。

## 三、生命周期解析语义域与候选身份

### SR-R5-05 生命周期解析语义冲突键不得包含结论载荷

```text
Lifecycle Ordering / Supersession Resolution Semantic Conflict Set Key =
  Source Applicability Change Conflict Set Key
+ Registered Source Applicability Change Set Boundary ID and Digest
+ Registered Change-boundary Completeness Resolution IDs and Digests
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Registered Source Registry Contract Registration Resolution ID and Digest
+ Lifecycle Resolution Purpose
+ Semantic Conflict Rule Version
```

`Lifecycle Resolution Purpose` 只允许：

```text
EFFECT_INTERVAL_ORDERING
UNIQUE_SUCCESSOR
SUPERSESSION_TARGET
REVOCATION_PRECEDENCE
```

下列字段不得进入语义冲突键：

```text
Candidate Resolution ID
Resolution Record ID
Claimed Member Order
Claimed Successor ID
Claimed Effective State
Evidence Set ID
Registry Position
Registration Time
Writer or Authority Holder ID
```

不同顺序、后继或区间结论必须在同一语义冲突集合竞争，不能通过把结论放进键中逃离冲突。

### SR-R5-06 候选解析载荷必须完整且可重放

```text
Lifecycle Resolution Candidate Payload =
  Lifecycle Resolution Semantic Conflict Set Key
+ Exact Participating Change Registration Resolution Tuple Set Digest
+ Exact Directed Predecessor / Successor Edge Set Digest
+ Exact Effective Interval Interpretation Set Digest
+ Exact Supersession / Revocation Target Set Digest
+ Registered Temporal Coordinate Resolution ID and Digest Set
+ Governed Resolution Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
+ Claimed Unique Effective State or NOT_ESTABLISHED
+ Claimed Unique Successor ID and Digest or NOT_APPLICABLE or NOT_ESTABLISHED
+ Candidate Payload Canonicalization Rule Version
```

每个参与成员元组至少包含变化登记解析 ID 与摘要、变化类型、有效区间、规范时间坐标解析和来源现实绑定。候选不得补造未知端点、提升时间精度或把记录位置当作有效时间。

前驱／后继边必须无环，全部端点必须属于精确参与集合。唯一后继必须由已登记时间坐标和适用证据证明，不能由“最新”、位置或写入时间推断。

### SR-R5-07 候选解析必须拥有稳定键

```text
Lifecycle Ordering / Supersession Candidate Resolution Key =
  Lifecycle Resolution Semantic Conflict Set Key
+ Candidate Resolution Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与候选键一对一且永久不可复用。同键同载荷可以幂等重申；同一候选 ID 异载荷必须 `CONFLICTED`。

## 四、候选登记和四值解析

### SR-R5-08 候选解析必须形成内容同一登记链

```text
Candidate Lifecycle Ordering / Supersession Resolution
  -> Lifecycle Resolution Registration Attempt
  -> Registered Lifecycle Resolution Record
```

```text
Candidate Resolution Payload Digest
= Registered Resolution Payload Digest
```

登记记录必须固定候选键、语义冲突键、完整载荷摘要、注册表位置、执行与登记授权实例、登记时间和证据谱系。登记不能改变顺序边、区间、后继或结果。

### SR-R5-09 单一候选登记解析必须使用四值

```text
Lifecycle Candidate Registration Resolution Key =
  Lifecycle Ordering / Supersession Candidate Resolution Key
+ Registered Lifecycle Resolution Registry Boundary ID and Digest
+ Required Registry Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

唯一内容同一登记记录和完整注册表边界支持 `REGISTERED`；完整合格空集支持 `NOT_REGISTERED`；记录、读取、边界或完整性未知支持 `INDETERMINATE`；同候选键异载荷、ID 复用或登记冲突支持 `CONFLICTED`。

空查询、缺失读取或不完整边界不能产生 `NOT_REGISTERED`。

## 五、同域解析竞争边界

### SR-R5-10 竞争边界必须固定全部同域解析

```text
Lifecycle Resolution Competing Record Boundary Key =
  Lifecycle Resolution Semantic Conflict Set Key
+ Registered Lifecycle Resolution Registry Boundary ID and Digest
+ Exact Qualified Candidate Registration Resolution Set Digest
+ Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

精确集合必须覆盖同域候选、登记尝试、登记记录、四值候选解析及冲突谱系。只有 `REGISTERED` 候选解析能成为确定成员，但其他状态和不利记录必须保留在边界谱系中。

选择精确集合不得排除同域异顺序、异区间、异后继或异证据候选。

### SR-R5-11 竞争边界必须形成内容同一登记链

```text
Candidate Lifecycle Resolution Competing Boundary
  -> Competing Boundary Registration Attempt
  -> Registered Lifecycle Resolution Competing Boundary
  -> Registered Competing Boundary Registration Resolution
```

边界候选和登记载荷必须共同固定边界键、成员集合、注册表边界、空洞、冲突子域和规则版本。边界登记解析使用：

```text
Lifecycle Resolution Competing Boundary Registration Resolution Key =
  Lifecycle Resolution Competing Record Boundary Key
+ Registered Lifecycle Boundary-record Registry Boundary ID and Digest
+ Required Boundary-record Registry Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

边界记录必须进入生命周期解析注册表的独立边界记录类型子域；该子域仍受 R5-03 的已分配、已登记注册表引用约束。边界登记解析使用：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同键异成员集合、异空洞或异冲突子域必须 `CONFLICTED`。

### SR-R5-12 竞争边界完整性必须独立

解析候选构造者、候选登记者、边界构造者和聚合者均不得评价竞争边界完整性。独立完整性至少覆盖：

```text
CARRIER
POSITION_OR_EXACT_SET
READABILITY
CONFLICT_SUBDOMAIN
SEMANTIC_DOMAIN_COVERAGE
```

任何必要维度不完整或未知时，边界不能支持确定生命周期聚合结果。

## 六、生命周期聚合解析

### SR-R5-13 聚合解析必须拥有稳定键

```text
Lifecycle Ordering / Supersession Aggregate Resolution Key =
  Lifecycle Resolution Semantic Conflict Set Key
+ Registered Competing Boundary Registration Resolution ID and Digest
+ Required Competing-boundary Completeness Resolution IDs and Digests
+ Registered Source Registry Contract Registration Resolution ID and Digest
+ Lifecycle Resolution Rule Contract Payload Digest
+ Aggregate Resolution Rule Version
```

键不得包含候选聚合结果、执行者、登记时间或所偏好的候选 ID。

### SR-R5-14 聚合解析必须形成候选—登记链

```text
Registered Complete Lifecycle Resolution Competing Boundary
  -> Candidate Lifecycle Ordering / Supersession Aggregate Resolution
  -> Aggregate Resolution Registration Attempt
  -> Registered Lifecycle Ordering / Supersession Aggregate Resolution
```

候选和登记载荷必须内容同一，并固定聚合键、全部合格成员、采用或拒绝的边、区间证明、后继证明、结果和完整证据谱系。

同一聚合键的异结果或异采用成员载荷必须进入冲突集合，不能按登记时间选赢家。

最终聚合登记必须形成：

```text
Lifecycle Aggregate Registration Resolution Key =
  Lifecycle Ordering / Supersession Aggregate Resolution Key
+ Registered Lifecycle Aggregate-record Registry Boundary ID and Digest
+ Required Aggregate-record Registry Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有唯一内容同一聚合记录、完整聚合记录边界和无冲突支持 `REGISTERED`；同聚合键异结果或异采用成员必须 `CONFLICTED`。缺失、读取或边界未知必须 `INDETERMINATE`，完整合格空集才可 `NOT_REGISTERED`。

### SR-R5-15 聚合结果必须封闭

```text
RESOLVED
NOT_RESOLVED
INDETERMINATE
CONFLICTED
```

- 完整集合中的全部合格成员内容同一，并唯一支持同一无环顺序、非重叠区间或同一唯一后继时，可以 `RESOLVED`；
- 完整集合证明不存在合格顺序或替代解析，且没有未知或冲突时，可以 `NOT_RESOLVED`；
- 集合、时间坐标、证据、合同、边界或完整性未知时必须 `INDETERMINATE`；
- 不兼容顺序、区间、后继、目标、结果载荷或同键异登记时必须 `CONFLICTED`。

`NOT_RESOLVED` 不是默认顺序，也不能把不兼容生命周期组合变为确定状态。

## 七、适用性变化聚合消费收紧

### SR-R5-16 R5 收紧来源适用性变化聚合键

本规则覆盖 R4 中 `Source Applicability Change Aggregate Resolution Key` 的消费字段：

```text
Source Applicability Change Aggregate Resolution Key =
  Source Applicability Change Conflict Set Key
+ Registered Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Lifecycle Resolution Consumption Reference
+ Aggregate Rule Version
```

```text
Lifecycle Resolution Consumption Reference =
  Registered Lifecycle Aggregate Registration Resolution ID and Digest
+ Registered Lifecycle Ordering / Supersession Aggregate Resolution Payload Digest
or
  LIFECYCLE_RESOLUTION_NOT_REQUIRED
```

只在完整变化集合含单一效果或多个内容同一效果、不存在任何顺序／替代歧义时，才允许 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`。

存在不兼容组合时：

```text
RESOLVED       -> may support the uniquely proven effective state
NOT_RESOLVED   -> CONFLICTED
INDETERMINATE  -> INDETERMINATE
CONFLICTED     -> CONFLICTED
```

裸生命周期解析、单一候选、未登记聚合或“最新记录”均不能进入来源适用性解析。

### SR-R5-17 历史解析不可被当前解析覆盖

历史来源适用性解析继续固定其变化集合、查询坐标主体和生命周期聚合解析。新增变化、证据、规则或边界必须形成新的候选、竞争边界、生命周期聚合和来源适用性身份。

```text
Historical Resolution: APPEND_ONLY
Current Restatement: NEW_IDENTITIES_REQUIRED
Retroactive Overwrite: PROHIBITED
```

## 八、权威和失败关闭

### SR-R5-18 新增角色必须逐操作分权

```text
Lifecycle Candidate Construction Authority Type
Lifecycle Candidate Registration Authority Type
Lifecycle Candidate Registration Resolution Authority Type
Lifecycle Competing Boundary Construction Authority Type
Lifecycle Competing Boundary Registration Authority Type
Lifecycle Boundary Completeness Authority Type
Lifecycle Aggregate Execution Authority Type
Lifecycle Aggregate Registration Authority Type
```

每个授权实例必须限定注册表、来源、语义域、变化边界、查询坐标、输入、输出和规则版本。任何角色都不能传播为时间值、查询坐标、来源记录或制度冻结权威。

### SR-R5-19 非法状态必须失败关闭

- 未分配或未登记的解析注册表接收候选；
- 候选载荷使用记录位置或“最新”建立有效顺序；
- 结果载荷、证据集合或候选 ID 被放入语义冲突键；
- 竞争边界排除同域不利候选；
- 聚合者自证边界完整；
- 有环顺序、区间重叠或多个后继产生 `RESOLVED`；
- `NOT_RESOLVED` 被解释为确定顺序；
- 来源适用性消费单一候选或裸顺序声明；
- 当前解析覆盖历史来源适用性；
- 候选、自检或文件存在替代已登记聚合解析。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`，不得静默降级为确定适用性。

## 九、回归和候选级闭合声明

### SR-R5-20 已通过主干不得回归

```text
Registry Root Bootstrap: PRESERVED
Source Version Conflict Aggregation: PRESERVED
Source Completeness Aggregate Resolution: PRESERVED
Applicability Change Conflict Set: PRESERVED
Boundary / Snapshot Reproducibility: PRESERVED
Open-world Absence Safety: PRESERVED
Raw Temporal Assertion Atomic Handoff: PRESERVED
Four-value Coordinate Subject Totality: PRESERVED
Cross-interface Acyclicity: PRESERVED
WS-01 Reference Direction: PRESERVED
```

### SR-R5-21 R5 只声明一个阻断候选闭合

```text
SR-R4-B1 Lifecycle Ordering / Supersession Resolution Identity: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R5 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R4-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R4` 执行交叉接口回归审查。R5 自检不能独立证明阻断关闭。
