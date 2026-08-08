# 来源注册表接口提案

## 提案信息

```text
Proposal ID: CR-0005
Title: Source Registry Interface
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: SINGLE_PURPOSE_GOVERNANCE_MODEL
Planning Basis: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Interface Baseline: CR-0004-CONSTITUTION-CANDIDATE-R1
Interface Baseline Review: CR-0004-CONSTITUTION-CANDIDATE-R1-CONSISTENCY-REVIEW
Parallel Interface Target: CR-0006 TEMPORAL MAPPING GOVERNANCE
Proposal Author: Codex
Proposal Authority: User-delegated drafting authority
Cross-interface Review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件是来源注册表接口的独立提案，不是冻结制度，也不是实际来源注册表。它不能登记来源、宣布快照完整、决定资格、改变来源适用性、构造认识边界或授权运行时消费。

## 一、单一目的与边界

### SR-C-01 本提案只有一个制度目的

本提案只定义：

> 来源提供方如何以稳定身份、明确作用域、追加位置、不可变快照、独立完整性和可追踪变化历史，为消费模型提供可复现来源边界。

### SR-C-02 来源注册表只证明来源事实边界

来源注册表可以证明：

- 哪个来源注册表和来源域被查询；
- 哪些来源身份、版本和记录位于精确边界内；
- 边界位置、记录集合和摘要是什么；
- 该边界的读取、成员、作用域和载体完整性是否被独立登记；
- 来源提供方登记了哪些生命周期或适用性变化事实。

来源注册表不得决定：

- 业务依据是否合格；
- 证明、豁免或制度是否适用；
- 决策是否准入；
- 提交结果、闭包结果或投影结果；
- 时间字段如何规范映射；
- 消费者是否拥有行动权威。

### SR-C-03 时间解释属于并行接口

基础来源快照身份不得依赖 `Valid At`、`Known At`、视图模式或时间映射结果。时间治理只能在已登记来源边界之上构造时间化查询坐标和认识边界。

```text
Source Registry Boundary and Snapshot Fact
  -> may be consumed by Temporal Mapping Governance

Temporal Mapping Result
  -/-> create or mutate Source Registry Fact
```

## 二、统一对象与唯一目的

### SR-C-04 来源对象必须分层

| 对象 | 类型 | 唯一目的 | 逻辑真源 |
|---|---|---|---|
| `Source Registry ID` | 稳定标识 | 标识一个来源注册表 | 注册表身份分配权威 |
| `Source Registry Version` | 版本值 | 标识注册表契约版本 | 注册表制度登记边界 |
| `Source Registry Authority Reference` | 复合权威引用 | 引用该注册表适用的逐操作授权集合 | 权威注册表 |
| `Source Registry Domain` | 作用域值 | 限定允许的来源类型和现实 | 注册表契约 |
| `Source Identity` | 稳定标识 | 标识一个来源谱系 | 来源身份分配权威 |
| `Source Version ID` | 不可变版本标识 | 标识来源谱系中的精确版本 | 来源登记边界 |
| `Source Record` | 不可变事实记录 | 保存来源提供方观察或声明 | 来源注册表 |
| `Source Registry Position` | 追加位置 | 表达注册表内登记顺序 | 位置原子分配边界 |
| `Source Registry Boundary` | 不可变边界值 | 固定位置范围或精确记录集 | 边界登记账本 |
| `Source Registry Snapshot` | 不可变快照 | 固定一个边界内的来源集合和摘要 | 快照登记账本 |
| `Source Snapshot Resolution` | 派生解析记录 | 解释快照是否可用 | 快照解析账本 |
| `Source Boundary Completeness Record` | 派生完整性记录 | 表达一个边界的完整性维度 | 完整性账本 |
| `Source Applicability Change Record` | 不可变变化事实 | 保存来源提供方声明的未来适用性变化 | 来源生命周期账本 |
| `Source Correction Record` | 非语义更正 | 修复来源记录表示缺陷 | 更正登记账本 |
| `Multi-registry Source Boundary Vector` | 复合边界值 | 固定多个注册表边界 | 多注册表边界账本 |
| `Source Applicability Input` | 最小消费接口 | 向下游提供来源级适用性事实 | 来源适用性解析账本 |
| `Source Registry Current View` | 可重建读面 | 展示指定边界的当前认识 | 派生投影 |

### SR-C-05 身份、位置、边界和快照不得互换

```text
Source Identity != Source Version ID
Source Version ID != Source Record ID
Source Record ID != Source Registry Position
Source Registry Position != Source Registry Boundary
Source Registry Boundary != Source Registry Snapshot
Snapshot Digest != Snapshot Completeness
```

位置只表达追加顺序，不能证明来源版本更新、业务优先级、时间有效性或语义替代。

## 三、权威类型与分权

### SR-C-06 每项来源操作必须拥有独立权威

```text
Source Registry Identity Allocation Authority Type
Source Registry Contract Registration Authority Type
Source Identity Allocation Authority Type
Source Record Construction Authority Type
Source Record Registration Authority Type
Source Registry Position Allocation Authority Type
Source Boundary Construction Authority Type
Source Boundary Registration Authority Type
Source Snapshot Construction Authority Type
Source Snapshot Registration Authority Type
Source Snapshot Resolution Execution Authority Type
Source Snapshot Resolution Registration Authority Type
Source Boundary Completeness Qualification Authority Type
Source Boundary Completeness Registration Authority Type
Source Applicability Change Decision Authority Type
Source Applicability Change Registration Authority Type
Source Applicability Resolution Execution Authority Type
Source Applicability Resolution Registration Authority Type
Source Correction Qualification Authority Type
Source Correction Registration Authority Type
Multi-registry Boundary Construction Authority Type
Multi-registry Boundary Registration Authority Type
```

`Source Registry Authority Reference` 只是上述逐类型授权的可验证引用集合，不是可以传播到全部操作的总括权威。集合中缺少某项精确授权时，该操作仍然无权执行。

### SR-C-07 权威不得隐式传播

来源构造者不能登记自身记录；记录登记者不能分配来源身份；快照构造者不能宣布完整；完整性计算者不能登记自身结论；适用性变化决定权不能取得业务资格权；多注册表向量构造权不能改变成员注册表。

### SR-C-08 授权实例必须声明完整作用域

```text
Authority Grant ID
Authority Type
Holder ID
Allowed Registry IDs and Domains
Allowed Source Types and IDs
Allowed Input Record Types
Allowed Output Record Types
Allowed Position and Boundary Domains
Allowed Rule Versions
Effective At and Expires At
Can Change
Cannot Change
Granting Authority Reference
Revocation and Supersession References
Evidence References
```

授权缺失、冲突、过期或跨域时必须失败关闭。

## 四、注册表契约、来源身份与记录

### SR-C-09 每个注册表必须拥有稳定契约身份

```text
Source Registry Contract Key =
  Source Registry ID
+ Source Registry Version
+ Source Registry Domain
```

注册表契约至少固定：

```text
Allowed Source Types
Allowed Record Types
Registry Scope
World Boundary Mode
Position Allocation Contract
Append-only Contract
Canonical Byte Contract
Digest Algorithm Contract
Boundary Contract
Correction Contract
Lifecycle Contract
Authority References
Effective Interval
Evidence References
```

### SR-C-10 来源身份和版本必须稳定

```text
Source Identity Key =
  Source Registry ID
+ Source Registry Domain
+ Source Identity Namespace
+ Source Identity
```

```text
Source Version Key =
  Source Identity Key
+ Source Version ID
```

一个来源版本只能绑定一个精确规范载荷摘要。同版本不同内容必须 `CONFLICTED`，不得最后写入获胜。

### SR-C-11 来源记录必须先形成候选和登记尝试

```text
Candidate Source Record
  -> Source Record Registration Attempt
  -> Registered Source Record
```

候选和已登记记录至少共同绑定：

```text
Source Record ID
Source Identity and Version
Source Registry ID and Domain
Source Record Type
Canonical Payload Digest
Reality Binding
Origin Reference
Observed Temporal Field Reference
Recorded Temporal Field Reference
Construction and Registration Authority References
Candidate and Registered Payload Digests
Evidence References
```

```text
Candidate Source Record Payload Digest
= Registered Source Record Payload Digest
```

时间字段在本提案中只作为不透明规范字段引用保存；其语义由时间治理接口决定。

### SR-C-12 位置分配必须原子且不可复用

```text
Source Registry Position Key =
  Source Registry ID
+ Source Registry Domain
+ Append Epoch
+ Position Value
```

位置分配必须与记录登记归因耦合。位置不得复用、重排或用来覆盖旧记录。登记失败的已分配位置可以形成空洞历史，但不得回收。

### SR-C-13 来源注册表必须追加且保留冲突

同来源版本同载荷可以幂等重申；同来源版本不同载荷、同位置不同记录或同记录跨现实绑定必须追加冲突证据并使相关边界失败关闭。

删除、覆盖、原地更正或选择“最新记录”均不得消除冲突。

## 五、作用域与世界边界

### SR-C-14 注册表作用域必须显式

```text
Registry Scope =
  Allowed Source Domains
+ Allowed Source Types
+ Allowed Identity Namespaces
+ Allowed Reality Bindings
+ Inclusion Rule Version
+ Exclusion Rule Version
+ Scope Digest
```

来源是否位于作用域内必须由版本化规则决定，查询者不能临时扩大或缩小作用域。

### SR-C-15 世界边界模式必须封闭

```text
OPEN_WORLD
CLOSED_WORLD
PARTITIONED_CLOSED_WORLD
```

- `OPEN_WORLD`：边界只能证明已登记成员，缺失不能证明不存在；
- `CLOSED_WORLD`：只有存在适用关闭契约、精确作用域和独立完整性时才能证明成员穷尽；
- `PARTITIONED_CLOSED_WORLD`：每个分区分别关闭，跨分区完整性必须由独立多分区合成证明。

世界边界模式变化必须产生新注册表契约版本，不能追溯改变旧快照。

### SR-C-16 来源排除必须有制度依据

任何来源类型、身份、分区或记录排除必须绑定：

```text
Exclusion Basis ID and Version
Exact Registry Scope
Exact Source Type or Identity Scope
Valid Interval
Decision and Authority References
Institution Freeze Reference
Evidence References
```

缓存、性能限制、读取失败或查询者偏好不能成为规范排除依据。

## 六、边界和快照

### SR-C-17 来源边界必须拥有稳定身份

```text
Source Registry Boundary Key =
  Source Registry ID and Version
+ Source Registry Domain
+ Registry Scope Digest
+ World Boundary Mode
+ First and Last Position or Exact Record Set Digest
+ Boundary Rule Version
```

边界不得包含其自身完整性结果、快照摘要或下游解析结果。

### SR-C-18 边界必须形成候选—登记链

```text
Candidate Source Registry Boundary
  -> Source Boundary Registration Attempt
  -> Registered Source Registry Boundary
```

边界至少绑定位置范围或精确记录集、记录身份和摘要、空洞位置、冲突子域、作用域、世界模式、载体契约、候选与登记摘要、权威、登记时间字段引用和证据。

### SR-C-19 快照必须绑定精确边界

```text
Source Registry Snapshot Key =
  Source Registry Boundary Key
+ Source Registry Boundary Record ID and Digest
+ Snapshot Canonicalization Rule Version
+ Snapshot Digest Rule Version
```

```text
Registered Source Registry Boundary
  -> Candidate Source Registry Snapshot
  -> Source Snapshot Registration Attempt
  -> Registered Source Registry Snapshot
```

快照摘要必须覆盖有序成员身份、版本、记录摘要、位置或精确集合、作用域、世界模式、空洞和冲突引用。边界变化必须形成新快照，不能覆盖旧快照。

### SR-C-20 快照摘要不证明完整

```text
Snapshot Digest Match
  -/-> Snapshot Completeness
```

快照构造者、快照登记者、摘要计算者和来源注册表本身都不能自证快照完整。

### SR-C-21 快照解析必须独立四值登记

```text
Source Snapshot Resolution Key =
  Source Registry Snapshot Key
+ Registered Snapshot Record ID and Digest
+ Source Boundary Completeness Record IDs and Digests
+ Snapshot Resolution Rule Version
```

```text
AVAILABLE
NOT_AVAILABLE
INDETERMINATE
CONFLICTED
```

精确内容同一快照、完整必要维度且无冲突支持 `AVAILABLE`；合格、适用、完整的未登记或不可用证明支持 `NOT_AVAILABLE`；同键不兼容快照、摘要、成员或解析支持 `CONFLICTED`；缺失、不完整、证明资格不可用或读取失败支持 `INDETERMINATE`。

空查询、超时和载体不可用不能产生 `NOT_AVAILABLE`。

## 七、完整性模型

### SR-C-22 完整性必须分维度

每个边界至少分别评价：

```text
CARRIER_INTEGRITY
POSITION_CONTINUITY
MEMBERSHIP_COMPLETENESS
SCOPE_COVERAGE
CONFLICT_SUBDOMAIN_COMPLETENESS
READ_COMPLETENESS
```

一个维度的 `COMPLETE` 不传播给其他维度。

### SR-C-23 完整性使用四值

```text
COMPLETE
INCOMPLETE
INDETERMINATE
CONFLICTED
```

- 精确边界、充分证据、适用规则和无冲突支持 `COMPLETE`；
- 已证明存在缺口支持 `INCOMPLETE`；
- 来源、规则、证据或读取未知支持 `INDETERMINATE`；
- 不兼容边界、证明或登记结果支持 `CONFLICTED`。

### SR-C-24 完整性必须形成候选—登记链

```text
Registered Source Boundary
+ Independent Evidence
  -> Candidate Source Boundary Completeness Record
  -> Completeness Registration Attempt
  -> Registered Source Boundary Completeness Record
```

```text
Source Boundary Completeness Key =
  Source Registry Boundary Key
+ Completeness Dimension
+ Completeness Rule Version
+ Evidence Set Digest
```

候选和登记记录必须内容同一。完整性权威不得登记被评价来源记录、修改边界或排除不利证据。

### SR-C-25 开放世界不能产生穷尽否定

`OPEN_WORLD` 边界可以对载体、位置、读取和冲突子域形成完整性结论，但不能仅凭当前快照对 `MEMBERSHIP_COMPLETENESS` 形成穷尽 `COMPLETE`。

```text
OPEN_WORLD + record missing
  -> INDETERMINATE
  -/-> qualified absence
```

### SR-C-26 关闭世界需要独立关闭证明

`CLOSED_WORLD` 或关闭分区要支持穷尽成员资格，必须绑定：

```text
Closure Contract ID and Version
Exact Scope and Partition
Closure Authority Reference
Closure Decision Reference
Closure Effective Boundary
Late-write Prohibition
Conflict Subdomain Boundary
Independent Closure Evidence
Institution Freeze Reference
```

关闭后迟到成员、越界写入或不同关闭载荷必须追加冲突并使成员完整性为 `CONFLICTED`，不得扩展旧关闭边界。

## 八、来源适用性变化

### SR-C-27 来源适用性变化必须来自独立决定

```text
Source Applicability Change Decision
  -> Candidate Source Applicability Change Record
  -> Change Registration Attempt
  -> Registered Source Applicability Change Record
```

决定和登记必须分权。来源记录存在、版本更高或写入更晚不能自动改变适用性。

### SR-C-28 变化记录必须拥有稳定身份

```text
Source Applicability Change Key =
  Source Identity and Version
+ Applicability Change Domain
+ Effective Scope Digest
+ Valid From
+ Change Decision Fact ID
```

变化类型：

```text
ACTIVATES
SUSPENDS
RETIRES
SUPERSEDES
REVOKES
```

同键同载荷幂等；同键不同载荷或不兼容变化必须进入冲突集合，不得按时间选赢家。

### SR-C-29 来源适用性解析必须失败关闭

```text
Source Applicability Resolution Key =
  Source Identity and Version
+ Exact Registered Change Set Digest
+ Source Lifecycle Boundary ID and Digest
+ Registered Boundary Completeness Records
+ Valid At Reference
+ Known At Reference
+ View Mode Reference
+ Applicability Rule Version
```

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

无冲突且存在唯一适用激活状态支持 `APPLICABLE`；精确撤销、退役、替代或暂停状态支持 `INAPPLICABLE`；冲突变化或同键不兼容解析支持 `CONFLICTED`；边界、时间映射、成员资格或读取未知支持 `INDETERMINATE`。

解析执行者不得创建变化决定；解析登记者不得修改候选。

### SR-C-30 最小消费接口不得放大语义

`Source Applicability Input` 至少绑定：

```text
Source Identity and Version
Applicability Result
Applicability Valid At Reference
Knowledge Boundary Vector Reference
Source Registry Snapshot References
Source Boundary Completeness References
Source Applicability and Correction Record References
Applicability Rule Version
Registered Resolution ID and Digest
Evidence References
```

该接口只表达来源模型自己的适用性，不决定消费方资格、证明适用性、提交或投影。

## 九、更正和历史

### SR-C-31 更正只能修复非语义字段

更正不得改变来源身份、版本、规范载荷、现实绑定、注册表位置、作用域、世界模式、适用性变化语义或原始时间事实。

### SR-C-32 更正必须追加且双边界化

```text
Source Correction Key =
  Original Source Record ID and Digest
+ Corrected Field Set Digest
+ Correction Request ID
+ Correction Effective Temporal Reference
```

更正必须形成资格、候选、登记尝试和内容同一已登记记录。它只在进入认识边界后影响读面，不得伪装成历史当时已知。

### SR-C-33 当前读面必须可重建

`Source Registry Current View` 只能由已登记来源、适用性变化、更正、精确边界和时间治理提供的视图坐标重建。读面可以删除，不能反向修改来源事实。

## 十、多注册表边界

### SR-C-34 多注册表向量必须拥有稳定身份

```text
Multi-registry Source Boundary Vector Key =
  Ordered Registry Boundary Entry Digests
+ Vector Scope Digest
+ Vector Rule Version
```

每个条目至少绑定注册表身份和版本、来源域、作用域、世界模式、边界记录、快照、各维度完整性记录、冲突子域和条目摘要。

该向量不包含 `Known At`、`Valid At` 或视图模式；这些由时间治理在向量之上绑定，避免循环。

### SR-C-35 多注册表向量必须形成候选—登记链

```text
Registered Source Registry Boundaries and Snapshots
  -> Candidate Multi-registry Source Boundary Vector
  -> Vector Registration Attempt
  -> Registered Multi-registry Source Boundary Vector
```

候选与登记向量必须内容同一。成员注册表顺序必须由规则版本确定，不能按读取完成顺序排列。

### SR-C-36 跨注册表冲突必须保留

同一来源身份和版本在不同注册表出现不兼容内容、现实绑定、适用性或更正时，向量必须保存全部冲突引用并标记 `CONFLICTED`。

注册表优先级、镜像关系、等价关系或去重规则只有通过冻结制度契约才能应用；查询者不得选择方便的注册表消除冲突。

### SR-C-37 多注册表完整性不能由向量自证

向量构造者只能聚合已经登记的边界和完整性记录。向量摘要、成员数量、相同时间戳或“全部请求成功”均不能证明跨注册表完整。

## 十一、与时间治理的无环接口

### SR-C-38 WS-02 只输出非时间化来源边界

```text
Registered Multi-registry Source Boundary Vector
  -> output of WS-02
  -> input to WS-03 Knowledge Boundary construction
```

WS-02 可以保存不透明时间字段引用，但不得解释旧字段、推导规范时间或构造 `Knowledge Boundary Vector`。

### SR-C-39 时间治理只返回坐标引用

WS-03 可以返回：

```text
Canonical Temporal Value References
Registered Temporal Mapping References
Knowledge Boundary Vector Reference
Temporal View Mode Reference
```

WS-02 的适用性解析可以消费这些引用，但时间治理不能登记来源、修改来源边界或宣布来源完整。

### SR-C-40 循环依赖必须禁止

```text
Source Snapshot Key
  -/-> Temporal Mapping Result

Source Boundary Completeness Key
  -/-> Knowledge Boundary Vector

Temporal Mapping Input
  -> may reference Source Snapshot and Boundary

Temporal Mapping Result
  -/-> rewrite Source Snapshot or Boundary
```

## 十二、规范因果路径

### SR-C-41 单注册表路径

```text
Registry Contract
  -> Source Identity and Version
  -> Candidate Source Record
  -> Registered Source Record + Stable Position
  -> Registered Source Boundary
  -> Registered Source Snapshot
  -> Independent Boundary Completeness
  -> Registered Snapshot Resolution
```

### SR-C-42 多注册表和时间消费路径

```text
Registered Registry Boundaries and Snapshots
  -> Registered Multi-registry Source Boundary Vector
  -> WS-03 Temporal Query and Knowledge Boundary
  -> Registered Source Applicability Resolution
  -> Source Applicability Input
  -> downstream qualification / authority / proof / closure models
```

下游消费不得反向改变来源注册表。

## 十三、非法状态候选

### SR-C-43 以下状态必须失败关闭

- 来源构造者登记自己的候选；
- 位置复用、重排或覆盖；
- 用位置顺序解释语义版本优先级；
- 快照摘要自证完整；
- `OPEN_WORLD` 缺失被解释为不存在；
- 边界完整性从另一个维度或注册表继承；
- 关闭世界没有独立关闭契约和迟到写冲突子域；
- 快照、边界或适用性候选未登记即被消费；
- 同来源跨注册表冲突被优先级或“最新”静默消除；
- 来源适用性接口决定业务资格、提交或投影；
- 更正覆盖原记录或修改语义字段；
- 多注册表向量包含自身完整性或时间认识结果；
- 时间映射反向创建、删除或修改来源事实；
- 文件存在、查询成功或缓存命中替代权威来源记录。

## 十四、接口与退出准备度

### SR-C-44 WS-01 冻结引用接口兼容

本提案为 `CR-0004-R1` 的 `Institution Resolution Boundary Vector` 提供注册表身份、作用域、精确边界、快照、记录摘要和独立完整性记录，但不创建制度冻结引用或引用解析结果。

```text
WS-01 Reference Compatibility: PASS_AS_DRAFT
```

### SR-C-45 CR-0002 与 CR-0003 消费接口兼容

本提案提供：

```text
Source Registry Snapshot References
Source Set Digest
Source Set Boundary
Authoritative Source Registry IDs and Scopes
Multi-registry Source Boundary Vector
Source Applicability Input
```

这些接口保持来源提供侧职责，不取得决策、提交、资格、证明、闭包或投影权威。

```text
CR-0002 Interface Compatibility: PASS_AS_DRAFT
CR-0003 Interface Compatibility: PASS_AS_DRAFT
```

## 十五、提案自检

```text
Single Purpose: PASS
Authoritative Provider-side Contract: PASS_AS_DRAFT
Source Identity and Stable Position: PASS_AS_DRAFT
Registry Scope and World Boundary: PASS_AS_DRAFT
Snapshot Reproducibility: PASS_AS_DRAFT
Completeness Non-self-proof: PASS_AS_DRAFT
Open-world Absence Safety: PASS_AS_DRAFT
Multi-registry Conflict Preservation: PASS_AS_DRAFT
Source Applicability Minimal Interface: PASS_AS_DRAFT
Temporal Interface Acyclicity: PASS_AS_DRAFT
WS-01 Reference Compatibility: PASS_AS_DRAFT
Cross-interface Review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005 Status: DRAFT
Authority: NONE
Executable: NO
Workstream: WS-02
Cross-interface Review with CR-0006: REQUIRED
Independent Model Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先与 `CR-0006` 执行交叉接口检查，再进入独立模型审查。任何通过结论都不能由本提案自检产生。
