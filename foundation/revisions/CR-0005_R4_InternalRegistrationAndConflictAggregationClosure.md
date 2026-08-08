# 来源注册表接口有界修订 R4

## 修订信息

```text
Proposal ID: CR-0005-R4
Title: Internal Registration and Conflict Aggregation Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R3 FOUR-VALUE COORDINATE SUBJECT CLOSURE
Repair Basis: CR-0005-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-M1 + SR-M2 + SR-M3 + SR-M4 only
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
Compatibility Reference: CR-0006-R2
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `CR-0005` 复合模型独立审查的四项内部阻断。它不覆盖基础稿、R1 至 R3 或审查记录的历史文本，不创建来源注册表、分配记录、完整性结论、适用性决定、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R4-01 R4 只覆盖四项内部模型阻断

```text
SR-M1 Registry Root Bootstrap
SR-M2 Source Identity / Version Conflict Domain
SR-M3 Completeness Conflict Aggregation
SR-M4 Applicability Change Conflict Domain
```

未被本修订显式覆盖的 `CR-0005 + R1 + R2 + R3` 规则继续作为合并候选语义。终局来源—时间接口字段、四值查询主体、认识边界和坐标登记解析不得改变。

### SR-R4-02 内部闭包不得产生自授权

所有根分配、登记、边界、完整性和聚合权威必须来自适用的外部冻结制度引用与明确授权实例。

```text
Registry Contract
  -/-> grant its own registration authority

Source Record
  -/-> prove its registry contract

Aggregate Resolution
  -/-> prove its own input boundary completeness
```

## 二、SR-M1：注册表根身份分配

### SR-R4-03 注册表标识分配必须拥有稳定键

```text
Source Registry ID Allocation Key =
  Source Registry Namespace ID and Version
+ Candidate Source Registry ID
+ Intended Registry Domain
+ Intended Contract Content Digest
+ Allocation Rule Version
```

命名空间必须由 `IF-0007` 兼容冻结制度固定。候选 ID 在命名空间内永久不可复用；退役只追加历史。

### SR-R4-04 标识分配必须形成尝试、记录和四值解析

```text
Candidate Registry ID
  -> Registry ID Allocation Attempt
  -> Candidate Registry ID Allocation Record
  -> Allocation Registration Attempt
  -> Registered Registry ID Allocation Resolution
```

解析键至少绑定分配键、命名空间边界 ID 和摘要、必要完整性解析及分配解析规则版本。

```text
ALLOCATED
NOT_ALLOCATED
INDETERMINATE
CONFLICTED
```

唯一内容同一分配、完整命名空间边界和无冲突支持 `ALLOCATED`；合格完整未分配证明支持 `NOT_ALLOCATED`；缺失、读取或完整性未知支持 `INDETERMINATE`；同键异载荷、ID 复用或命名空间冲突支持 `CONFLICTED`。

### SR-R4-05 根分配必须逐操作分权

```text
Source Registry ID Allocation Execution Authority Type
Source Registry ID Allocation Registration Authority Type
Source Registry ID Allocation Resolution Authority Type
Source Registry ID Retirement Authority Type
```

分配执行、登记、解析、退役和契约登记权威不得互相传播。契约内容不能反向授权其自身 ID 分配。

## 三、SR-M1：注册表契约登记

### SR-R4-06 契约候选必须绑定已分配注册表 ID

```text
Registered ALLOCATED Registry ID Resolution
+ Source Registry Contract Key
+ Complete Contract Payload
  -> Candidate Source Registry Contract
```

完整契约载荷必须覆盖基础稿要求的作用域、世界模式、位置、追加、规范字节、摘要、边界、更正、生命周期、权威、有效区间和证据。

### SR-R4-07 契约登记必须形成内容同一链

```text
Candidate Source Registry Contract
  -> Contract Registration Attempt
  -> Registered Contract Record
```

```text
Candidate Contract Payload Digest
= Registered Contract Payload Digest
```

同一契约键同载荷可以幂等重申；同键异载荷必须进入冲突集合，不能按登记时间或写入者选赢家。

### SR-R4-08 契约注册表边界必须稳定且完整性独立

```text
Source Registry Contract Registry Boundary Key =
  Contract Registry ID and Version
+ First and Last Position or Exact Contract Record Set Digest
+ Contract Registry Scope Digest
+ Boundary Rule Version
```

边界必须形成候选—登记链并保存空洞和冲突子域。载体、位置、读取和冲突子域完整性由不能登记契约的独立权威评价。

### SR-R4-09 契约登记解析必须使用四值

```text
Source Registry Contract Registration Resolution Key =
  Source Registry Contract Key
+ Registered Contract Registry Boundary ID and Digest
+ Required Contract Registry Completeness Resolution IDs and Digests
+ Contract Resolution Rule Version
```

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

只有 `ALLOCATED + REGISTERED` 且内容同一的契约可以产生下游 `Source Registry Authority Reference`、来源身份和记录。空查询不能产生 `NOT_REGISTERED`。

## 四、SR-M2：来源身份分配和版本竞争域

### SR-R4-10 来源身份分配必须登记且不可复用

```text
Source Identity Allocation Key =
  Registered Source Registry ID and Version
+ Source Registry Domain
+ Source Identity Namespace
+ Candidate Source Identity
+ Intended Reality Binding
+ Allocation Rule Version
```

候选、分配尝试、分配记录和登记解析必须内容同一，结果使用：

```text
ALLOCATED | NOT_ALLOCATED | INDETERMINATE | CONFLICTED
```

来源身份退役不能复用；同一身份跨现实绑定或命名空间冲突必须 `CONFLICTED`。

### SR-R4-11 来源身份分配必须分权

```text
Source Identity Allocation Execution Authority Type
Source Identity Allocation Registration Authority Type
Source Identity Allocation Resolution Authority Type
Source Identity Retirement Authority Type
```

来源记录构造、登记和位置分配权不能隐式取得身份分配权。

### SR-R4-12 来源版本语义冲突键不得包含记录包字段

```text
Source Version Semantic Conflict Set Key =
  Registered Source Registry ID and Version
+ Source Registry Domain
+ Source Identity Key
+ Source Version ID
+ Reality Binding
+ Source Record Semantic Domain
+ Conflict Set Rule Version
```

该键禁止包含：

```text
Source Record ID
Registry Position
Registration Time
Writer or Authority Holder ID
Registration Attempt ID
Evidence Set ID
```

记录包字段保留在候选谱系中，但不能用于隔离语义竞争。

### SR-R4-13 竞争记录边界必须固定全部同域记录

```text
Source Version Competing Record Boundary Key =
  Source Version Semantic Conflict Set Key
+ Source Record Registry Boundary ID and Digest
+ Exact Competing Record Set Digest
+ Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界必须证明同域候选、登记尝试、已登记记录和冲突记录已完整读取。选择精确记录集合不能排除同域不利记录。

### SR-R4-14 来源版本登记聚合解析必须四值化

```text
Source Version Registration Aggregate Resolution Key =
  Source Version Semantic Conflict Set Key
+ Registered Competing Record Boundary ID and Digest
+ Required Completeness Resolution IDs and Digests
+ Aggregate Resolution Rule Version
```

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

唯一规范载荷或多个内容同一载荷支持 `REGISTERED`；合格完整空集支持 `NOT_REGISTERED`；边界或记录未知支持 `INDETERMINATE`；不兼容载荷、现实绑定、位置归因或登记解析支持 `CONFLICTED`。

### SR-R4-15 位置分配必须与聚合记录内容同一

每个已登记来源记录必须绑定唯一不可复用位置分配记录。位置分配和记录登记必须在同一原子归因边界完成；失败位置形成永久空洞。

聚合解析按来源版本语义竞争键比较记录，不按位置先后选赢家。边界和快照必须保存聚合解析 ID、结果和全部竞争记录引用。

## 五、SR-M3：完整性语义域与证据评价

### SR-R4-16 完整性语义域键必须与证据分离

```text
Source Completeness Semantic Domain Key =
  Source Registry Boundary ID and Digest
+ Completeness Dimension
+ Exact Completeness Scope Digest
+ Completeness Semantic Rule Version
```

证据集合、评价记录 ID、登记时间和执行者不得进入语义域键。

### SR-R4-17 单一证据边界评价必须拥有稳定键

```text
Source Completeness Evidence Evaluation Key =
  Source Completeness Semantic Domain Key
+ Governed Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
+ Evaluation Rule Version
```

候选评价、登记尝试和已登记评价必须内容同一，使用 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。

### SR-R4-18 完整性评价边界必须覆盖全部同域评价

```text
Source Completeness Evaluation Boundary Key =
  Source Completeness Semantic Domain Key
+ Evaluation Registry Boundary ID and Digest
+ Exact Evaluation Record Set Digest
+ Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

评价边界不能由完整性执行者或聚合者自证完整。不同证据边界的评价必须进入同一完整语义域集合。

### SR-R4-19 完整性聚合解析必须使用四值

```text
Source Completeness Aggregate Resolution Key =
  Source Completeness Semantic Domain Key
+ Registered Evaluation Boundary ID and Digest
+ Required Evaluation Boundary Completeness Resolution IDs and Digests
+ Aggregate Resolution Rule Version
```

所有适用评价一致 `COMPLETE` 支持聚合 `COMPLETE`；存在合格缺口且无冲突支持 `INCOMPLETE`；集合、证据或边界未知支持 `INDETERMINATE`；`COMPLETE` 与 `INCOMPLETE` 并存或同键异载荷支持 `CONFLICTED`。

下游边界、快照解析、多注册表向量和时间完整性评价只能消费已登记聚合解析，不能选择单一有利证据评价。

## 六、SR-M4：适用性变化竞争集合

### SR-R4-20 适用性变化语义键必须排除决定事实

```text
Source Applicability Change Conflict Set Key =
  Source Identity and Version
+ Applicability Semantic Domain
+ Effective Scope Digest
+ Canonical Valid Coordinate ID and Digest
+ Reality Binding
+ Conflict Set Rule Version
```

禁止字段：

```text
Change Decision Fact ID
Change Record ID
Registry Position
Registration Time
Writer or Authority Holder ID
```

决定事实和登记谱系保留在成员载荷中，不能用于换键。

### SR-R4-21 变化成员必须先取得登记解析

每个变化决定仍形成候选、登记尝试和变化记录，但只有已登记：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

变化登记解析中的 `REGISTERED` 成员可以进入竞争集合。未登记、未知或冲突成员不能被当作确定变化。

### SR-R4-22 完整变化集合边界必须可重放

```text
Source Applicability Change Set Boundary Key =
  Source Applicability Change Conflict Set Key
+ Change Registry Boundary ID and Digest
+ Exact Registered Change Resolution Set Digest
+ Required Change-boundary Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界必须覆盖激活、暂停、退役、替代、撤销成员及其冲突谱系。空集合只有在完整边界下才是合格空集。

### SR-R4-23 变化聚合状态必须封闭

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

单一确定效果或多个内容同一效果支持相应状态；完整空集支持 `NO_APPLICABLE_CHANGE`；集合、时间映射、决定资格或边界未知支持 `INDETERMINATE`。

### SR-R4-24 不兼容生命周期组合必须冲突优先

```text
ACTIVE + SUSPENDED -> CONFLICTED
ACTIVE + RETIRED -> CONFLICTED
ACTIVE + SUPERSEDED -> CONFLICTED
ACTIVE + REVOKED -> CONFLICTED
multiple incompatible negative states -> CONFLICTED
same conflict-set incompatible aggregate payloads -> CONFLICTED
```

只有同一完整集合内存在已登记、内容同一的生命周期顺序或替代解析，证明效果区间不重叠或唯一后继效果时，才允许得到唯一确定状态。记录时间、位置或“最新”不能建立该顺序。

### SR-R4-25 来源适用性解析只能消费变化聚合解析

```text
Source Applicability Change Aggregate Resolution Key =
  Source Applicability Change Conflict Set Key
+ Registered Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Aggregate Rule Version
```

`ACTIVE` 可以支持 `APPLICABLE`；`SUSPENDED | RETIRED | SUPERSEDED | REVOKED` 可以支持 `INAPPLICABLE`；`NO_APPLICABLE_CHANGE | INDETERMINATE` 只能支持 `INDETERMINATE`；`CONFLICTED` 必须支持 `CONFLICTED`。

现有来源适用性稳定键继续固定查询主体和坐标登记解析；不得回退为裸 `Known At` 或分散坐标字段。

## 七、权威、回归和非法状态

### SR-R4-26 新增聚合角色必须逐操作分权

```text
Registry Contract Boundary Construction / Registration / Completeness Authority Types
Source Version Competition Boundary Construction / Registration Authority Types
Source Version Aggregate Resolution Execution / Registration Authority Types
Source Completeness Evaluation / Boundary / Aggregate Authority Types
Applicability Change Boundary / Aggregate Resolution Authority Types
```

每个授权实例必须限定输入、输出、注册表、语义域、边界和规则版本。构造、评价、聚合、登记和完整性权威不得互相传播。

### SR-R4-27 新增非法状态必须失败关闭

- 未分配注册表 ID 登记契约；
- 契约登记或身份分配自授权；
- 来源记录 ID、位置或写入者隔离同版本冲突；
- 完整性证据集合摘要隔离同语义域矛盾评价；
- 聚合者选择单一 `COMPLETE` 评价；
- 决定事实 ID 隔离适用性变化冲突；
- 用记录时间或“最新”解决生命周期冲突；
- `NO_APPLICABLE_CHANGE` 被解释为来源适用；
- 内部聚合规则改变四值查询主体或来源—时间接口；
- 任何候选、自检或文件存在替代已登记解析。

### SR-R4-28 已通过主干不得回归

```text
Boundary / Snapshot Reproducibility: PRESERVED
Snapshot Completeness Non-self-proof: PRESERVED
Open-world Absence Safety: PRESERVED
Raw Temporal Assertion Atomic Handoff: PRESERVED
Multi-registry Conflict Preservation: PRESERVED
Four-value Coordinate Subject Totality: PRESERVED
Cross-interface Acyclicity: PRESERVED
WS-01 Reference Direction: PRESERVED
```

## 八、候选级闭合声明

### SR-R4-29 R4 只声明四项内部阻断候选闭合

```text
SR-M1 Registry Root Bootstrap: CLOSED_AS_DRAFT
SR-M2 Source Identity / Version Conflict Domain: CLOSED_AS_DRAFT
SR-M3 Completeness Conflict Aggregation: CLOSED_AS_DRAFT
SR-M4 Applicability Change Conflict Domain: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R4 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-M1 + SR-M2 + SR-M3 + SR-M4 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 `CR-0005` 复合模型独立复审，并与 `CR-0006-R3` 共同执行终局接口回归检查。自检不能独立证明四项阻断关闭。
