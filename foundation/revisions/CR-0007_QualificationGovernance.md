# 资格治理提案

## 提案信息

```text
Proposal ID: CR-0007
Title: Qualification Governance
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: SINGLE_PURPOSE_GOVERNANCE_MODEL
Planning Basis: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Upstream Source Interface: CR-0005 + CR-0005-R1 through CR-0005-R11
Upstream Temporal Interface: CR-0006 + CR-0006-R1 through CR-0006-R10
Upstream Cross-interface Review: CR-0005-R11-CR-0006-R10-TERMINAL-CROSS-INTERFACE-REGRESSION-REVIEW
Proposal Author: Codex
Proposal Authority: User-delegated drafting authority
Upstream Cross-interface Compatibility Review Required: YES
Decision and Commit Interface Compatibility Review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Qualification Registry Created: NO
Qualification Rule Created: NO
Qualification Resolution Created: NO
Compatibility Record Created: NO
Compatibility Domain Snapshot Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0005-R11 Source Registry Interface Composite
Depends On: CR-0006-R10 Temporal Mapping Governance Composite
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件是资格规则、资格计算和资格兼容演进的独立提案，不是冻结制度，也不是实际资格注册表。它不能创建资格规则、执行或登记资格结果、决定权威或来源是否适用、建立提交结果、批准豁免、发布投影或授予运行时权威。

## 一、单一目的与边界

### QG-C-01 本提案只有一个制度目的

本提案只定义：

> 依据、证明和豁免候选如何在精确资格规则、来源边界、时间坐标和证据边界上被计算并登记为不可变资格结果，以及不同资格规则版本如何在不放大认识强度的前提下形成可审计兼容域和前向解释。

### QG-C-02 资格只回答输入是否满足资格规则

资格可以回答：

- 指定主体和依据类型是否被精确规则允许；
- 指定输入、证据和完整性是否满足资格条件；
- 在精确来源边界和时间坐标上，资格结果是肯定、否定、未知还是冲突；
- 两个资格规则版本的结果是否可以安全比较或解释；
- 规则变化是否要求重新资格计算。

资格不得回答：

- 权威授予在指定行为坐标上是否适用；
- 来源、历史资格、证明或豁免在当前坐标上是否仍适用；
- 决策是否准入、决策事实是否成立；
- 提交是否成功或目标状态是否迁移；
- 证明是否足以单独建立 `ABORTED`；
- 豁免是否足以单独建立 `EXEMPT`；
- 依赖闭包是否完整；
- 投影是否可以发布。

### QG-C-03 资格与适用性必须严格分离

```text
Registered Qualification = QUALIFIED
  -/-> Authority Applicability = APPLICABLE
  -/-> Source Applicability = APPLICABLE
  -/-> Proof Applicability = APPLICABLE
  -/-> Exemption Applicability = APPLICABLE
```

历史资格保持当时规则、来源和认识边界上的不可变结论。当前是否仍可消费，必须由后续适用性治理独立解析。

### QG-C-04 资格不得建立业务结果

```text
Qualification Result
  -/-> Decision Admissibility
  -/-> Decision Fact
  -/-> Commit Resolution
  -/-> Target Transition
  -/-> Projection Publication
```

资格结果只能成为这些后续模型的一个受约束输入。

## 二、规范对象与唯一目的

### QG-C-05 资格对象必须分层

| 对象 | 类型 | 唯一目的 | 逻辑真源 |
|---|---|---|---|
| `Qualification Governance Registry ID` | 稳定标识 | 标识一个资格治理注册表 | 注册表身份分配权威 |
| `Qualification Rule Lineage ID` | 稳定谱系标识 | 标识一条资格规则演进谱系 | 规则身份分配权威 |
| `Qualification Rule ID` | 稳定规则标识 | 标识一个资格规则家族 | 规则身份分配权威 |
| `Qualification Rule Version` | 不可变版本标识 | 标识规则家族中的精确语义版本 | 规则登记边界 |
| `Qualification Rule Contract` | 版本化制度契约 | 定义允许输入、算法、结果和失败关闭条件 | 资格治理制度 |
| `Qualification Subject Reference` | 精确对象引用 | 固定被资格判断的主体及版本 | 上游对象注册表 |
| `Qualification Basis Reference` | 精确依据引用 | 固定资格所评价的依据、证明或豁免候选 | 上游对象注册表或候选账本 |
| `Qualification Input Package` | 不可变输入集合 | 固定一次计算的规则、主体、依据、来源、时间和证据 | 资格输入边界 |
| `Qualification Computation Attempt` | 不可变尝试记录 | 保存一次资格计算意图、授权和输入摘要 | 资格尝试账本 |
| `Candidate Qualification Resolution` | 候选派生记录 | 保存资格计算输出 | 资格候选账本 |
| `Qualification Registration Attempt` | 不可变登记尝试 | 固定候选、授权、稳定键和候选摘要 | 资格登记尝试账本 |
| `Registered Qualification Resolution` | 不可变派生记录 | 保存内容同一的已登记资格结论 | 资格解析账本 |
| `Qualification Semantic Compatibility Record` | 不可变制度记录 | 声明两个精确规则版本的语义兼容分类 | 资格兼容注册表 |
| `Qualification Compatibility Domain Snapshot` | 不可变制度快照 | 固定一个可比较规则版本集合 | 资格兼容域注册表 |
| `Qualification Forward Interpretation Contract` | 版本化制度契约 | 定义资格结果的非放大前向解释 | 资格解释契约注册表 |
| `Candidate Qualification Interpretation Record` | 候选派生记录 | 保存一次前向解释输出 | 资格解释候选账本 |
| `Registered Qualification Interpretation Record` | 不可变派生记录 | 保存内容同一的前向解释历史 | 资格解释账本 |
| `Institutional Source Exclusion Basis` | 版本化制度契约 | 引用 `WS-02` 已建立的来源排除合法条件 | `WS-02` 来源治理制度 |
| `Source Exclusion Basis Qualification Resolution` | 不可变资格记录 | 判断来源排除依据能否被精确资格规则消费 | 资格解析账本 |
| `Qualification Recalculation Requirement Record` | 不可变制度记录 | 声明规则变化需要重新资格计算 | 资格演进注册表 |
| `Qualification Correction Record` | 非语义更正记录 | 修复资格记录的表示缺陷 | 资格更正账本 |
| `Qualification Current View` | 可重建读投影 | 展示指定坐标上的资格认识 | 派生读面 |

### QG-C-06 身份、规则、输入、结果和视图不得互换

```text
Qualification Rule ID != Qualification Rule Version
Qualification Rule Version != Qualification Rule Contract
Qualification Input Package != Qualification Result
Candidate Qualification Resolution != Registered Qualification Resolution
Registered Qualification Resolution != Qualification Current View
Compatibility Record != Compatibility Domain Snapshot
Forward Interpretation != Requalification
Qualification != Applicability
```

### QG-C-07 一个规则版本只能绑定一个精确规则内容

```text
(Qualification Rule ID, Qualification Rule Version)
  -> exactly one Canonical Rule Payload Digest
```

同一规则版本出现不同规范载荷、允许类型、结果代数、时间语义或证据条件时必须保持 `CONFLICTED`。不得用文件顺序、登记时间或较新载荷选择赢家。

### QG-C-08 资格稳定键必须固定完整语义坐标

```text
Qualification Resolution Key =
  Qualification Purpose
+ Qualification Subject ID and Version
+ Qualification Basis ID and Version
+ Qualification Rule ID and Version
+ Qualification Semantic Domain
+ Qualification Source Boundary Vector B
+ Temporal Query Coordinate Q
+ Correction View Reference
+ Input Package Digest
```

任何一项变化都必须产生新的稳定键。不得跨主体、依据、规则版本、来源边界、时间坐标或更正视图复用结果。

## 三、权威类型与分权

### QG-C-09 每项资格操作必须拥有独立权威

```text
Qualification Governance Registry Identity Allocation Authority Type
Qualification Rule Identity Allocation Authority Type
Qualification Rule Definition Authority Type
Qualification Rule Registration Authority Type
Qualification Computation Authority Type
Qualification Resolution Registration Authority Type
Qualification Semantic Compatibility Decision Authority Type
Qualification Semantic Compatibility Registration Authority Type
Qualification Compatibility Domain Construction Authority Type
Qualification Compatibility Domain Registration Authority Type
Qualification Forward Interpretation Contract Definition Authority Type
Qualification Forward Interpretation Contract Registration Authority Type
Qualification Forward Interpretation Execution Authority Type
Qualification Interpretation Registration Authority Type
Institutional Source Exclusion Basis Qualification Authority Type
Institutional Source Exclusion Basis Qualification Registration Authority Type
Qualification Recalculation Requirement Decision Authority Type
Qualification Recalculation Requirement Registration Authority Type
Qualification Correction Qualification Authority Type
Qualification Correction Registration Authority Type
```

### QG-C-10 权威不得隐式传播

```text
Rule Definition != Rule Registration
Rule Registration != Qualification Computation
Qualification Computation != Resolution Registration
Compatibility Decision != Compatibility Registration
Compatibility Registration != Domain Construction
Domain Construction != Domain Registration
Forward Contract Definition != Forward Interpretation Execution
Forward Interpretation != Requalification
Source Exclusion Basis Qualification != Source Exclusion Decision
Source Exclusion Basis Qualification != Source Applicability Decision
Correction Qualification != Original Record Mutation
```

同一主体可以持有多项独立授权，但必须使用不同任务契约、输入作用域、输出类型和执行归因。

### QG-C-11 每个授权实例必须完整边界化

最低字段：

```text
Authority Grant ID and Version
Authority Type
Holder ID
Allowed Governance Registry IDs
Allowed Qualification Rule IDs and Versions
Allowed Qualification Purposes and Semantic Domains
Allowed Subject Types and Scopes
Allowed Basis Types and Scopes
Allowed Source Registry IDs and Domains
Allowed Temporal Coordinate Profiles
Allowed Input and Output Record Types
Allowed Operation
Effective At and Expires At
Can Change
Cannot Change
Granting Authority Reference
Revocation and Supersession References
Evidence References
```

授权缺失、过期、冲突、作用域不匹配或无法验证时必须失败关闭。

### QG-C-12 计算者和登记者不得自证

资格计算者不能登记自己的最终结果；登记者不能修改候选结果、原因、来源、时间坐标或摘要；兼容关系决策者不能登记自身决定；兼容域构造者不能创造成员兼容性；前向解释器不能获得重新资格计算权威。

## 四、资格规则身份与契约

### QG-C-13 每个资格规则必须拥有稳定身份

```text
Qualification Rule Key =
  Qualification Governance Registry ID
+ Qualification Rule Lineage ID
+ Qualification Rule ID
+ Qualification Rule Version
```

规则名称、文件路径、配置键、类名或版本号大小都不能替代已登记规则身份。

### QG-C-14 规则契约必须完整

每个 `Qualification Rule Contract` 至少固定：

```text
Qualification Purpose
Qualification Semantic Domain
Allowed Subject Types and Version Shapes
Allowed Basis Types and Version Shapes
Subject-to-basis Relation Contract
Required Source Registry IDs and Domains
Required Source Boundary and Completeness Dimensions
Required Temporal Coordinate Profile
Required Evidence Types and Trust Requirements
Required Field Presence Contract
Qualification Predicate Set
Predicate Evaluation Order or Order-independence Proof
Result Algebra Version
Reason Code Registry Version
Conflict Detection Contract
Unknown and Failure-closure Contract
Institutional Source Exclusion Basis References
Source Exclusion Basis Qualification Resolution References
Correction Consumption Contract
Canonical Byte Contract and Digest Algorithm
Rule Effective Interval
Rule Knowledge Availability Boundary
Institution Freeze Reference
Authority References
Evidence References
```

缺少任何影响结果的字段时，规则不得用于确定资格计算。

### QG-C-15 允许主体和依据类型必须逐规则声明

```text
Allowed Subject Type
+ Allowed Subject Version Shape
+ Allowed Basis Type
+ Allowed Basis Version Shape
+ Allowed Relation Type
+ Qualification Purpose
```

类型名称相同、字段相似或位于同一产品不能建立允许关系。未登记类型、未知版本或关系不匹配必须为 `INDETERMINATE`，不得默认合格或不合格。

### QG-C-16 规则必须具有单一资格语义域

最低语义域：

```text
BASIS_QUALIFICATION
PROOF_QUALIFICATION
EXEMPTION_BASIS_QUALIFICATION
CORRECTION_QUALIFICATION
SOURCE_EXCLUSION_BASIS_QUALIFICATION
```

一个语义域的规则、兼容关系或结果不得在另一个语义域直接复用。跨域复用必须建立新规则和独立证据。

### QG-C-17 规则登记不等于规则冻结或运行资格

```text
Registered Qualification Rule
  -/-> Institution Freeze
  -/-> Runtime Eligibility
```

运行时消费还必须验证适用制度版本的 `Institution Freeze Reference`。本提案不创建该引用。

## 五、资格输入、来源和时间坐标

### QG-C-18 资格输入必须固定上游已登记边界

`Qualification Input Package` 至少绑定：

```text
Input Package ID
Qualification Purpose and Semantic Domain
Qualification Subject Reference and Digest
Qualification Basis Reference and Digest
Qualification Rule ID, Version and Digest
Registered Source Boundary Vector B Reference and Digest
Registered Source Snapshot References
Registered Source Completeness Aggregate References
Source Set Digest
Temporal Governance Boundary Vector T Reference and Digest
Knowledge Boundary Vector K Reference and Digest
Temporal Query Coordinate Q Reference and Digest
Temporal View Mode
Validity As Of
Correction View References
Evidence References and Digests
Contrary Source References
Institutional Source Exclusion Basis References or NOT_APPLICABLE
Source Exclusion Basis Qualification Resolution References or NOT_APPLICABLE
Input Package Canonical Digest
```

未登记候选、缓存内容、裸时间戳或仅有文件路径的材料不能成为规范资格输入。

### QG-C-19 资格必须消费 `B -> T -> K -> Q`，不得反向改写

```text
Registered Source Boundary Vector B
  -> Registered Temporal Governance Boundary Vector T
  -> Registered Knowledge Boundary Vector K
  -> Registered Temporal Query Coordinate Q
  -> Qualification Input Package
```

资格治理不能创建或修改 `B`、`T`、`K`、`Q`，不能把资格结果写回来源或时间注册表，也不能为缺失边界临时构造第二查询坐标。

### QG-C-20 有效时间、认识边界和计算时间必须分离

至少分离：

```text
Qualification Validity As Of
Knowledge Boundary Vector
Qualification Rule Effective At
Rule Known At Boundary
Computation Started At
Resolved At
Registered At
Correction Effective At
```

当前计算时间不能填充缺失有效时间；新规则当前可用不能证明它在历史认识边界已经可用。

### QG-C-21 来源完整性不能由资格计算自证

资格计算只能消费 `WS-02` 已登记的来源完整性聚合和后续闭包治理提供的完整性引用。输入数量、查询成功、摘要存在、来源无返回或计算完成均不能证明来源集合完整。

## 六、资格计算与结果代数

### QG-C-22 资格计算必须形成候选路径

```text
Registered Qualification Rule
+ Qualification Input Package
+ Qualification Computation Authority
  -> Qualification Computation Attempt
  -> Candidate Qualification Resolution
```

计算尝试至少保存规则、输入包、稳定键、执行授权、执行者、开始和结束观察、算法实现身份、候选载荷摘要及失败信息。

### QG-C-23 规范资格结果采用四值代数

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED(Conflicting Qualification References)
```

- `QUALIFIED`：完整且无冲突的正向条件证明指定输入满足精确规则；
- `DISQUALIFIED`：完整且无冲突的否定条件证明指定输入不满足精确规则；
- `INDETERMINATE`：规则、输入、来源、证据、时间、兼容性或完整性无法支持任一确定终局；
- `CONFLICTED`：同一稳定键和可比较语义域内存在相反终局或不兼容规范载荷。

缺失、超时、读取失败、空集合、未知类型和默认值都不能产生 `QUALIFIED` 或 `DISQUALIFIED`。

### QG-C-24 四值结果具有独立认识偏序

```text
INDETERMINATE <= QUALIFIED
INDETERMINATE <= DISQUALIFIED
QUALIFIED and DISQUALIFIED are incomparable terminals
CONFLICTED is outside this strength order
```

该偏序只表达认识强度，不是生命周期顺序、业务优先级或来源可信度排名。不得用数量、时间或置信度从 `CONFLICTED` 选择一个终局。

### QG-C-25 决策模型三值依据接口必须使用失败关闭适配

`CR-0002` 的依据资格消费接口保持：

```text
QUALIFIED -> QUALIFIED
DISQUALIFIED -> NOT_QUALIFIED
INDETERMINATE -> INDETERMINATE
CONFLICTED -> INDETERMINATE + Qualification Conflict References
```

`NOT_QUALIFIED` 只是该消费接口对规范 `DISQUALIFIED` 的外部表示，不是第五个资格真值。冲突适配为 `INDETERMINATE` 时必须保留全部冲突引用，不得伪装成没有冲突。

### QG-C-26 原因代码不能替代结果证明

原因代码、分数、置信度、解释文本和模型输出只能作为证据注释。它们不能提高认识强度、改变终局、选择冲突赢家或替代规则谓词和完整性证明。

### QG-C-27 资格计算必须是总函数且失败关闭

对每个合法输入包，规则必须确定地产生四值之一及完整原因和来源引用。异常、未知枚举、缺失必需字段或实现差异必须归入 `INDETERMINATE` 或 `CONFLICTED`，不得静默丢弃尝试。

## 七、资格登记、内容同一与历史

### QG-C-28 候选与登记必须分离

```text
Candidate Qualification Resolution
+ Qualification Registration Authority
+ Deterministic Admissibility Check
  -> Qualification Registration Attempt
  -> Registered Qualification Resolution
```

登记权威只验证授权、稳定键、规则资格、输入引用、字段完备和内容同一，不得重算或修改结果。

### QG-C-29 已登记资格记录必须完整

至少绑定：

```text
Qualification Resolution ID
Qualification Resolution Key and Digest
Qualification Purpose and Semantic Domain
Qualification Subject ID, Version and Digest
Qualification Basis ID, Version and Digest
Qualification Rule ID, Version and Digest
Qualification Outcome and Reason Codes
Qualification Input Package ID and Digest
Source Boundary Vector B Reference and Digest
Temporal Query Coordinate Q Reference and Digest
Validity As Of
Knowledge Boundary Vector
Temporal View Mode
Source Snapshot and Completeness References
Correction View References
Contrary and Conflict References
Evidence References
Computation Attempt ID
Qualification Resolver Identity and Authority Reference
Registration Attempt ID
Qualification Registration Authority Reference
Candidate Payload Digest
Registered Payload Digest
Registered At
Registered Record Digest
```

### QG-C-30 候选和登记载荷必须内容同一

```text
Candidate Qualification Payload Digest
= Registered Qualification Payload Digest
```

不相等时登记必须失败并保存尝试。登记者不得“规范化”结果、删除冲突、补充来源或替换时间字段。

### QG-C-31 同键并发结果必须聚合而非覆盖

同一稳定键出现多个内容相同候选时可以幂等引用同一登记结果；出现不同终局、规则摘要、输入摘要或来源集合时必须保留全部记录并形成冲突聚合，不能最后写入获胜。

### QG-C-32 历史资格不可变

规则变化、来源更正、证据失效、后续冲突或新认识只能追加新资格、适用性或解释记录。不得修改、删除或降级旧资格记录。

## 八、来源排除依据与禁止自证

### QG-C-33 来源排除依据必须由 `WS-02` 建立并通过资格消费约束

`WS-02` 提供的 `Institutional Source Exclusion Basis` 至少绑定：

```text
Source Exclusion Basis ID and Version
Exact Source Registry Scope
Exact Source Type, Identity or Partition Scope
Exclusion Decision and Reason
Valid Interval
Decision and Authority References
Institution Freeze Reference
Evidence References
Canonical Payload Digest
```

来源排除依据的身份、作用域、决定和登记权威属于 `WS-02`。`WS-04` 只能在独立资格计算和登记后，判断该已登记依据能否被精确资格规则消费；它不能创建、扩张或修改来源排除依据。

`Source Exclusion Basis Qualification Resolution` 至少绑定：

```text
Qualification Resolution ID and Digest
Institutional Source Exclusion Basis ID, Version and Digest
Qualification Semantic Domain
Qualification Rule ID and Version
Allowed Subject and Basis Types
Allowed Source Registry IDs, Domains and Types
Required Completeness References
Temporal Query Coordinate
Qualification Outcome and Conflict References
Computation and Registration Authority References
Evidence References
```

通过资格消费的来源排除依据只允许资格计算在精确作用域内排除来源，不删除来源历史，也不创建来源适用性变化。

### QG-C-34 缺失和不利来源不得被临时排除

以下情况不能成为排除理由：

- 来源未返回或读取超时；
- 来源内容不利于期望结果；
- 来源登记时间较旧；
- 来源置信度或评分较低但无冻结规则；
- 多注册表之间存在冲突；
- 开放世界边界尚未关闭；
- 计算者或投影器临时声明“不相关”。

没有合格排除依据时，必需来源缺失或未知必须导致 `INDETERMINATE`，相反终局来源必须导致 `CONFLICTED`。

### QG-C-35 资格不能证明自己的输入完整

资格计算者、规则制定者、结果登记者、兼容域构造者和前向解释器都不能为自己消费的来源集合创建最终完整性证明。完整性必须来自独立授权和可追踪证据链。

## 九、语义兼容关系

### QG-C-36 跨规则兼容必须显式分类

规范分类：

```text
IDENTICAL_SEMANTICS
FORWARD_INTERPRETABLE
REQUIRES_RERESOLUTION
INCOMPATIBLE
UNKNOWN_COMPATIBILITY
```

版本号相邻、名称相同、字段超集、实现相同或历史结果相等都不能自动建立兼容关系。

### QG-C-37 兼容记录必须绑定精确语义域和方向

`Qualification Semantic Compatibility Record` 至少绑定：

```text
Compatibility Record ID
Qualification Semantic Domain
Source Qualification Rule ID, Version and Digest
Target Qualification Rule ID, Version and Digest
Direction
Compatibility Classification
Allowed Subject and Basis Type Intersection
Field Presence Comparison
Predicate Semantic Comparison
Result Algebra Comparison
Temporal Coordinate Contract Comparison
Evidence and Completeness Contract Comparison
Source Exclusion Contract Comparison
Required Re-resolution Kind or NOT_APPLICABLE
Forward Interpretation Contract Reference or NOT_APPLICABLE
Compatibility Evidence References
Compatibility Decision Authority Reference
Compatibility Registration Authority Reference
Institution Freeze Reference
Effective Interval
Record Digest
```

一个语义域的兼容记录不得被另一个语义域复用。方向相反时必须有独立记录和证据。

### QG-C-38 兼容关系不能由消费结果反向推出

```text
Same Historical Outcomes
  -/-> IDENTICAL_SEMANTICS

Successful Forward Interpretation
  -/-> Reverse Compatibility

Pairwise Compatibility A -> B and B -> C
  -/-> Compatibility A -> C
```

每个被消费的方向必须有精确登记关系或冻结制度允许且有完备证明的闭包记录。

### QG-C-39 未知和不兼容必须失败关闭

`INCOMPATIBLE` 和 `UNKNOWN_COMPATIBILITY` 都不能支持跨版本终局复用。消费方必须保持 `INDETERMINATE`，或按已登记要求执行新的重新资格计算。

## 十、兼容域快照

### QG-C-40 兼容域必须是不可变精确快照

```text
Qualification Compatibility Domain Snapshot Key =
  Compatibility Domain ID
+ Compatibility Domain Version
+ Qualification Semantic Domain
+ Exact Member Rule Version Set Digest
+ Membership Rule Version
+ Validity As Of
+ Knowledge Boundary Vector
```

### QG-C-41 快照必须完整枚举成员和关系

至少绑定：

```text
Compatibility Domain ID and Version
Qualification Semantic Domain
Exact Member Qualification Rule IDs and Versions
Exact Member Rule Digests
Exact Required Directional Compatibility Record References
Membership Digest
Membership Rule ID and Version
Allowed Qualification Scope Modes
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
Domain Construction Authority Reference
Domain Registration Authority Reference
Snapshot Digest
```

成员枚举完整不等于成员语义兼容；每个必需方向仍须有独立兼容记录。

### QG-C-42 兼容域成员变化必须产生新版本

```text
Member or Compatibility Relation Change
  -> New Domain Version
  -> New Membership Digest
  -> New Snapshot Digest
  -> New Qualification Projection Key downstream
```

不得修改旧快照、复用旧摘要、动态解释“当前成员”或用查询时最新版本替代精确成员。

### QG-C-43 精确规则模式和兼容域模式必须二选一

```text
EXACT_QUALIFICATION_RULE_VERSION
QUALIFICATION_COMPATIBILITY_DOMAIN_SNAPSHOT
```

精确模式必须填写一个规则版本并把域字段标记为 `NOT_APPLICABLE`；兼容域模式必须填写一个不可变快照并把精确规则字段标记为 `NOT_APPLICABLE`。不得两者同时填写或同时省略。

## 十一、前向解释契约

### QG-C-44 前向解释必须引用专用冻结契约

`Qualification Forward Interpretation Contract` 至少绑定：

```text
Forward Interpretation Contract ID and Version
Qualification Semantic Domain
Source Qualification Rule ID, Version and Digest
Target Interpretation Rule ID, Version and Digest
Qualification Scope Mode
Source and Target Scope Identity
Total Deterministic Qualification Mapping
Qualification Epistemic Strength Mapping
Field Presence Preservation
Evidence Reference Preservation
Source Record Reference Preservation
Qualification Record Reference Preservation
Temporal Coordinate Preservation
Conflict Reference Preservation
Mapping Rule Version
Compatibility Evidence References
Institution Freeze Reference
Canonical Payload Digest
```

缺失任一必需字段时，兼容分类只能为 `UNKNOWN_COMPATIBILITY`。

### QG-C-45 前向解释不得放大认识强度

最低合法映射：

```text
InterpretQualification(INDETERMINATE)
  -> INDETERMINATE

InterpretQualification(QUALIFIED)
  -> QUALIFIED or INDETERMINATE

InterpretQualification(DISQUALIFIED)
  -> DISQUALIFIED or INDETERMINATE

InterpretQualification(CONFLICTED sources)
  -> CONFLICTED or INDETERMINATE
```

禁止：

```text
INDETERMINATE -> QUALIFIED
INDETERMINATE -> DISQUALIFIED
QUALIFIED -> DISQUALIFIED
DISQUALIFIED -> QUALIFIED
CONFLICTED -> one selected terminal
UNRESOLVED field -> VALUE
```

### QG-C-46 前向解释不得改变作用域身份

解释只能在以下身份全部相同的情况下执行：

```text
Same Qualification Purpose and Semantic Domain
Same Qualification Subject ID and Version
Same Qualification Basis ID and Version
Same Qualification Scope Mode
Same Exact Rule Version or Same Compatibility Domain Snapshot
Same Validity As Of
Same Knowledge Boundary Vector
Same Temporal View Mode
```

任一项变化都必须产生新键；需要提高确定性、跨终局转换或改变作用域时必须重新资格计算。

### QG-C-47 前向解释必须形成候选和内容同一登记

```text
Registered Qualification Resolution
+ Registered Compatibility Record
+ Frozen Forward Interpretation Contract
+ Forward Interpretation Execution Authority
  -> Candidate Qualification Interpretation Record
  -> Independent Content-identical Registration
  -> Registered Qualification Interpretation Record
```

解释器和登记者都不能获得资格计算权威。

## 十二、规则演进与重新资格计算

### QG-C-48 规则语义变化必须产生新版本

以下变化至少要求新规则版本：

- 允许主体、依据或关系类型变化；
- 资格谓词或计算顺序变化；
- 必需字段、来源、证据或完整性条件变化；
- 时间坐标或认识边界语义变化；
- 结果代数、原因代码语义或冲突规则变化；
- 来源排除条件变化；
- 规范字节或摘要契约变化；
- 有效窗口或制度出处变化。

不得原地修改规则并追溯解释旧资格。

### QG-C-49 提高确定性或改变作用域必须重新资格计算

```text
REQUIRES_RERESOLUTION
+ Required Re-resolution Kind = REQUALIFICATION
  -> New Qualification Input Package
  -> New Authorized Qualification Computation Attempt
  -> New Candidate Qualification Resolution
  -> Independent Content-identical Registration
```

重新资格计算必须使用新规则版本和精确当前或历史重放坐标，不能只重建投影或重新标记旧结果。

### QG-C-50 重新资格计算不得覆盖旧记录

```text
Original Registered Qualification Resolution
  -> remains immutable

New Rule and New Coordinate
  -> New Registered Qualification Resolution
```

新资格记录必须引用前序记录和演进原因，但不能继承其终局、完整性或适用性。

### QG-C-51 新资格仍须重建下游链

```text
New Registered Qualification Resolution
  -> Independent Applicability Resolution in WS-05 or WS-06
  -> Dependency Closure Rebuild in WS-08
  -> Projection Re-evaluation in WS-09
```

任何下游步骤未决时，不得从新资格直接推断 `ADMISSIBLE`、`ABORTED`、`EXEMPT`、`COMMITTED` 或已发布投影。

## 十三、双时间、更正与迁移

### QG-C-52 资格历史必须使用双时间追加语义

```text
Qualification Validity As Of
!= Qualification Resolved At
!= Qualification Registered At
!= Qualification Known At Boundary
```

历史认识视图只能消费当时认识边界内已登记规则、来源和证据。当前重述必须使用新身份，不得覆盖历史视图。

### QG-C-53 更正只能修复非语义表示缺陷

允许更正编码、转录、引用格式和不改变规则或结果含义的元数据错误。不得通过更正改变主体、依据、规则、结果、来源集合、有效时间、认识边界、证据含义或冲突集合。

语义变化必须形成新规则、新资格计算或独立失效和适用性记录。

### QG-C-54 更正必须追加且内容同一

```text
Qualification Correction Key =
  Original Qualification Record ID and Digest
+ Corrected Field Set Digest
+ Correction Request ID
+ Correction Effective Temporal Reference
```

更正必须经过独立更正资格、候选、登记尝试和内容同一登记；原记录永久保留。

### QG-C-55 规则迁移不得伪装为兼容

迁移只能登记源规则、目标规则、影响范围、兼容分类、重新资格要求和历史保留方式。没有兼容证据时必须为 `UNKNOWN_COMPATIBILITY`，不得以批量迁移结果反向证明规则兼容。

## 十四、上游和下游接口

### QG-C-56 与 `WS-02` 的接口只消费来源事实

本提案只消费：

```text
Registered Source Records and Digests
Registered Source Boundary Vector B
Registered Source Snapshot References
Registered Source Completeness Aggregate References
Source Set Digest
Source Correction View References
Registered Institutional Source Exclusion Basis References
```

资格结果不能创建来源身份、记录、边界、快照、完整性或适用性变化。

### QG-C-57 与 `WS-03` 的接口只消费时间坐标

本提案只消费：

```text
Registered Temporal Governance Boundary Vector T
Registered Knowledge Boundary Vector K
Registered Temporal Query Coordinate Q
Canonical Temporal Value References
HISTORICAL_AS_KNOWN or CURRENT_RESTATED
```

资格结果不能创建时间映射、规范时间值、认识边界或查询坐标。

### QG-C-58 向 `CR-0002` 提供依据资格接口

`Registered Basis Qualification Resolution` 至少由本提案的已登记资格解析安全投影出：

```text
Resolution ID and Digest
Basis ID and Version
Decision Type and Object Scope
Qualification Outcome
Qualification Conflict References
Effective At and Validity As Of
Knowledge Boundary Vector
Resolved At and Registered At
Qualification Rule ID and Version
Institution Version and Freeze Reference
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence and Correction References
Qualification Registration Authority Reference
```

该接口不建立决策准入或决策事实。

### QG-C-59 向 `CR-0003` 提供证明资格和兼容接口

本提案提供：

```text
Registered Proof Qualification Record shape
QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED
Qualification Semantic Compatibility Record
Qualification Compatibility Domain Snapshot
Qualification Forward Interpretation Contract
Qualification Recalculation Requirement Record
```

`CR-0003` 仍负责提交解析消费和资格投影；本提案不建立 `ABORTED`、闭包或投影发布。

### QG-C-60 向 `WS-06` 提供规则基础而不决定证明或豁免适用性

`WS-06` 可以消费本提案的规则身份、资格结果代数、兼容记录、域快照和重新资格要求，但必须独立定义证明与豁免的类型注册表、适用性、完整正向链、失效和冲突治理。

### QG-C-61 接口依赖必须无环

```text
WS-02 B
  -> WS-03 T/K/Q
  -> WS-04 Qualification
  -> WS-05 or WS-06 Applicability
  -> WS-08 Closure
  -> WS-09 Projection Audit and Publication

Qualification
  -/-> rewrite B, T, K or Q
Applicability
  -/-> rewrite historical Qualification
Projection
  -/-> create Qualification
```

## 十五、规范因果路径

### QG-C-62 规则建立路径

```text
Candidate Qualification Rule Contract
  -> Independent Rule Review
  -> Applicable Institution Freeze Process
  -> Registered Qualification Rule
  -> Runtime Eligibility only after valid freeze reference
```

本提案不执行以上路径，也不创建任何规则实例。

### QG-C-63 资格计算和登记路径

```text
Registered Qualification Rule
+ Registered Source Boundary Vector B and Completeness
+ Registered Temporal Coordinate Q
+ Subject, Basis and Evidence
+ Qualification Computation Authority
  -> Qualification Input Package
  -> Qualification Computation Attempt
  -> Candidate Qualification Resolution
+ Independent Qualification Registration Authority
  -> Registered Qualification Resolution
```

### QG-C-64 兼容域和前向解释路径

```text
Exact Rule Versions
+ Compatibility Evidence
+ Compatibility Decision Authority
  -> Candidate Semantic Compatibility Record
+ Independent Compatibility Registration Authority
  -> Registered Semantic Compatibility Record
  -> Candidate Compatibility Domain Snapshot
+ Independent Domain Registration Authority
  -> Registered Immutable Domain Snapshot
+ Frozen Forward Interpretation Contract
  -> Candidate Interpretation
+ Independent Interpretation Registration
  -> Registered Interpretation History
```

### QG-C-65 规则变化和重新资格路径

```text
New Qualification Rule Version
+ Registered Compatibility Classification
  -> IDENTICAL_SEMANTICS or safe FORWARD_INTERPRETABLE
       -> bounded non-amplifying interpretation
  -> REQUIRES_RERESOLUTION
       -> new authorized qualification computation
  -> INCOMPATIBLE or UNKNOWN_COMPATIBILITY
       -> INDETERMINATE for cross-version consumption
```

## 十六、证据要求与完整性

### QG-C-66 每个确定资格终局必须拥有正向证据链

`QUALIFIED` 和 `DISQUALIFIED` 都必须绑定：

```text
Exact Registered Rule and Frozen Institution Reference
Exact Subject and Basis References
Exact Registered Source Boundary and Snapshot Set
Independent Completeness References
Exact Temporal Coordinate
All Required Predicate Evaluations
Contrary Source Search and Preservation
Qualified Source Exclusion Basis or NOT_APPLICABLE
Computation Authority and Attempt
Candidate and Registered Content Identity
Evidence Package References and Digests
```

否定终局不能仅由未找到正向材料建立。

### QG-C-67 兼容和域成员关系必须逐关系有证据

兼容证据至少覆盖字段存在性、谓词语义、结果代数、时间坐标、来源与完整性、排除规则、证据保留和冲突传播。抽样结果相同不足以证明规则语义兼容。

### QG-C-68 证据链不得循环自证

资格结果不能作为其自身规则资格、来源完整性、兼容关系、域成员关系、冻结引用或登记授权的证明。任何循环引用必须失败关闭并保留诊断记录。

## 十七、非法状态候选

### QG-C-69 以下状态必须失败关闭

- 规则定义者登记自己的规则；
- 资格计算者登记自己的最终结果；
- 结果登记者修改候选载荷；
- 未登记规则、输入、来源边界或时间坐标被消费；
- 用裸时间戳、当前时间或单一 `Known At` 替代 `Q`；
- 资格结果决定权威、来源、证明或豁免适用性；
- 类型名称、版本号或字段相似性直接证明资格或兼容；
- 缺失、超时、空集合或读取失败产生确定终局；
- 开放世界边界的缺失被解释为不存在；
- 来源数量、置信度、登记时间或多数投票解决冲突；
- 不利来源被临时排除或删除；
- 快照摘要、输入摘要或计算成功自证完整；
- `CONFLICTED` 被映射为一个确定终局；
- `NOT_QUALIFIED` 被建立为规范第五真值；
- 兼容域动态引用“最新成员”；
- 兼容关系被无证据反向或传递复用；
- 前向解释提高认识强度、跨终局转换或改变作用域；
- 重新资格计算覆盖旧资格历史；
- 更正改变规则、结果、来源或证据语义；
- 资格登记、兼容登记或域快照创建被解释为制度冻结；
- 资格结果直接建立 `ADMISSIBLE`、`ABORTED`、`EXEMPT`、`COMMITTED` 或目标迁移；
- 下游适用性、闭包或投影反向修改历史资格。

## 十八、接口准备度与提案自检

### QG-C-70 `WS-02` 和 `WS-03` 接口映射

本提案使用终局通过的 `CR-0005-R11` 与 `CR-0006-R10` 复合接口形状，保持：

```text
B -> T -> K -> Q -> Qualification
Reverse Identity Dependency: PROHIBITED
Source Authority Propagation: PROHIBITED
Temporal Authority Propagation: PROHIBITED
```

该声明只是提案内接口映射，仍需独立交叉接口兼容审查。

### QG-C-71 `CR-0002` 和 `CR-0003` 接口映射

```text
CR-0002 Basis Qualification Interface: MAPPED_AS_DRAFT
CR-0003 Proof Qualification Algebra: MAPPED_AS_DRAFT
CR-0003 Qualification Compatibility Record: MAPPED_AS_DRAFT
CR-0003 Compatibility Domain Snapshot: MAPPED_AS_DRAFT
CR-0003 Forward Interpretation Contract: MAPPED_AS_DRAFT
CR-0003 Requalification Boundary: MAPPED_AS_DRAFT
```

上述映射不能替代正式兼容性审查。

### QG-C-72 提案自检

```text
Single Purpose: PASS
Qualification / Applicability Separation: PASS_AS_DRAFT
Rule Identity and Version: PASS_AS_DRAFT
Allowed Subject and Basis Types: PASS_AS_DRAFT
Computation / Registration Authority Separation: PASS_AS_DRAFT
Four-value Proof-facing Compatibility: PASS_AS_DRAFT
CR-0002 Three-value Consumer Failure Closure: PASS_AS_DRAFT
Conflict Preservation: PASS_AS_DRAFT
Completeness Non-self-proof: PASS_AS_DRAFT
Forward Interpretation Safety: PASS_AS_DRAFT
Compatibility Domain Immutability: PASS_AS_DRAFT
Rule Evolution and Requalification: PASS_AS_DRAFT
Institutional Source Exclusion Boundary: PASS_AS_DRAFT
WS-02 / WS-03 Interface Acyclicity: PASS_AS_DRAFT
Upstream Cross-interface Compatibility Review: REQUIRED
CR-0002 / CR-0003 Interface Compatibility Review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0007 Status: DRAFT
Authority: NONE
Executable: NO
Workstream: WS-04
Proposal Established: YES
Model Review Result: NOT_PERFORMED
Upstream Cross-interface Compatibility Review: REQUIRED
Decision and Commit Interface Compatibility Review: REQUIRED
Independent Model Review: REQUIRED
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Qualification Registry: NOT_CREATED
Qualification Rule: NOT_CREATED
Qualification Resolution: NOT_CREATED
Compatibility Domain Snapshot: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先对 `CR-0007` 与 `CR-0005-R11`、`CR-0006-R10` 执行上游交叉接口兼容审查，再对 `CR-0002-CONSTITUTION-CANDIDATE` 和 `CR-0003-CONSTITUTION-CANDIDATE-R2` 执行消费接口兼容审查，之后才能进入独立模型审查。任何通过结论都不能由本提案自检产生。
