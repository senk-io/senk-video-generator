# 资格治理有界修订 R4：内部登记与授权拓扑闭合

## 修订信息

```text
Proposal ID: CR-0007-R4
Title: Internal Registration and Authority Topology Closure
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0007-R3 CONSUMER CONTRACT AND QUALIFICATION RESULT LAYER CLOSURE
Repair Basis: CR-0007-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: QG-IM-B1 + QG-IM-B2 + QG-IM-B3 + QG-IM-B4 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Upstream Interface Regression Review Required: YES
Consumer Interface Regression Review Required: YES
Independent Composite Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
```

> 本文件只补齐资格治理内部登记、边界、完整性和累计授权拓扑。它不改变已经通过的上游字段、消费真值或证明作用域，不创建资格规则、资格结果、制度冻结或运行时权威。

## 一、修订边界

### QG-R4-01 R4 只关闭四项内部阻断

```text
QG-IM-B1 Qualification Rule Registration Topology
QG-IM-B2 Composite Authority Catalog
QG-IM-B3 Atomic Record Evaluation Boundary and Completeness
QG-IM-B4 Governance Artifact Content-identical Registration
```

### QG-R4-02 R4 是累计覆盖层

与本修订冲突的基础稿及 R1/R3 登记、授权和边界条款由 R4 覆盖；结果代数、资格／适用性分离、上游消费元组、提交契约作用域和前向解释非放大规则继续有效。

## 二、资格规则注册拓扑

### QG-R4-03 规则版本语义冲突键必须唯一

```text
Qualification Rule Semantic Conflict Set Key =
  Qualification Governance Registry ID and Version
+ Qualification Rule Lineage ID
+ Qualification Rule ID
+ Qualification Rule Version
```

规则载荷、制定者、登记时间、冻结决定或实现版本不得用于换键。

### QG-R4-04 候选规则记录必须固定精确内容

`Candidate Qualification Rule Record` 至少绑定：

```text
Rule Semantic Conflict Set Key
Qualification Rule Contract Payload
Qualification Purpose and Semantic Domain
Allowed Subject, Basis and Relation Types
Predicate, Result and Failure-closure Contracts
Source, Temporal, Evidence and Completeness Requirements
Correction and Exclusion Consumption Contracts
Canonical Byte Contract and Digest Algorithm
Candidate Rule Payload Digest
Rule Definition Authority Reference
Evidence References
```

### QG-R4-05 运行时规则登记必须晚于精确制度冻结

```text
Candidate Qualification Rule Record
  -> IF-0007 Independent Review and Freeze of exact payload
  -> Valid Institution Freeze Reference
  -> Qualification Rule Registration Attempt
  -> Registered Qualification Rule Record
```

登记不能创建或替代制度冻结。

### QG-R4-06 规则登记尝试必须不可变

至少绑定：

```text
Rule Registration Attempt ID
Rule Semantic Conflict Set Key
Candidate Rule Record ID and Digest
Institution Freeze Reference and Resolution
Target Qualification Rule Registry ID and Version
Expected Registry Boundary
Registration Authority Reference
Candidate Payload Digest
Attempted Registered Payload Digest
Attempted At
Failure Evidence or NOT_APPLICABLE
```

失败尝试和永久空洞必须保留。

### QG-R4-07 已登记规则必须保持内容同一

```text
Candidate Rule Payload Digest
= Registered Rule Payload Digest
= Frozen Content Digest under canonical contract
```

已登记记录还必须绑定尝试、登记授权、注册表位置、登记时间、制度冻结引用和记录摘要。

### QG-R4-08 规则登记解析使用四值

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

同键唯一内容同一且冻结引用有效支持 `REGISTERED`；完整边界证明没有成功登记支持 `NOT_REGISTERED`；边界或证据未知支持 `INDETERMINATE`；同键异载荷、异冻结内容或异登记结果支持 `CONFLICTED`。

### QG-R4-09 资格计算只能消费登记单例

```text
Rule Registration Resolution = REGISTERED
+ exactly one Registered Rule Record
+ content-identical Freeze Reference
  -> may support Qualification Computation
```

其他结果全部失败关闭。

## 三、累计授权目录

### QG-R4-10 R4 补齐累计操作授权

除基础稿权威外，必须登记：

```text
Qualification Input Assembly Authority Type
Completeness Tuple Mapping Proof Construction Authority Type
Completeness Tuple Mapping Proof Registration Authority Type
Completeness Consumption Bundle Construction Authority Type
Atomic Qualification Computation Authority Type
Atomic Qualification Registration Authority Type
Atomic Record Evaluation Boundary Construction Authority Type
Atomic Record Evaluation Boundary Registration Authority Type
Atomic Boundary Completeness Qualification Authority Type
Atomic Boundary Completeness Registration Authority Type
Qualification Conflict Aggregate Execution Authority Type
Qualification Conflict Aggregate Registration Authority Type
Proof Qualification Consumer Envelope Construction Authority Type
Governance Artifact Candidate Construction Authority Type
Governance Artifact Registration Authority Type
Governance Artifact Conflict Aggregate Authority Type
```

### QG-R4-11 新授权必须使用完整作用域

每项授权实例除基础字段外，至少固定：

```text
Allowed Qualification Registry IDs and Versions
Allowed Rule, Semantic Domain and Consumer Profile
Allowed Stable Keys and Boundary Types
Allowed Input Record Types
Allowed Output Record Types
Allowed Upstream Reference Types
Allowed Canonical Byte and Digest Contracts
Effective At and Expires At
Can Change
Cannot Change
Granting Authority and Evidence References
```

### QG-R4-12 所有新增权威互不传播

```text
Input Assembly != Mapping Proof Construction
Mapping Proof Construction != Mapping Proof Registration
Bundle Construction != Atomic Qualification Computation
Atomic Computation != Atomic Registration
Boundary Construction != Boundary Registration
Boundary Registration != Boundary Completeness Qualification
Boundary Completeness Qualification != Completeness Registration
Aggregate Execution != Aggregate Registration
Consumer Envelope Construction != Projection Publication
Governance Artifact Construction != Artifact Registration
Artifact Registration != Institution Freeze
```

授权缺失、过期、冲突或作用域不匹配时必须保留尝试并失败关闭。

## 四、原子资格记录评价边界

### QG-R4-13 原子记录语义域必须排除记录事实

```text
Atomic Qualification Evaluation Semantic Key =
  Atomic Qualification Resolution Key without Record ID
+ Qualification Semantic Domain
+ Qualification Consumer Profile
+ Atomic Result Algebra Version
```

记录 ID、登记位置、执行者和结果值不得用于换键。

### QG-R4-14 原子记录注册表边界必须覆盖完整竞争集合

```text
Atomic Qualification Record Evaluation Boundary Key =
  Atomic Qualification Evaluation Semantic Key
+ Atomic Qualification Registry ID and Version
+ Registry Boundary ID and Digest
+ Exact Atomic Registration Resolution Set Digest
+ Permanent Hole and Failed Attempt Set Digest
+ Required Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界必须覆盖同一语义键下全部成功、失败、空洞和冲突谱系。

### QG-R4-15 边界必须形成候选、登记和四值解析

```text
Candidate Atomic Evaluation Boundary
  -> Boundary Registration Attempt
  -> Registered Atomic Evaluation Boundary Record
  -> Atomic Evaluation Boundary Registration Resolution
```

解析值为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

候选与登记边界载荷必须内容同一。

### QG-R4-16 边界完整性必须独立登记

`Registered Atomic Evaluation Boundary Completeness Resolution` 至少绑定：

```text
Registered Atomic Evaluation Boundary ID and Digest
Completeness Semantic Domain
Governed Evidence Boundary ID and Digest
Evidence Boundary Completeness Resolution ID and Digest
Expected and Observed Atomic Registration Resolution Set Digests
Failed Attempt and Hole Coverage Proofs
Completeness Outcome
Completeness Qualification Authority Reference
Completeness Registration Authority Reference
Candidate and Registered Payload Digests
```

结果：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

边界构造者、聚合者和资格计算者不能自证完整。

### QG-R4-17 冲突聚合键必须消费登记完整边界

R3 的聚合语义键由 R4 收紧为：

```text
Qualification Conflict Aggregate Key =
  Atomic Qualification Evaluation Semantic Key
+ Registered Atomic Evaluation Boundary ID and Digest
+ Atomic Evaluation Boundary Registration Resolution ID and Digest
+ Registered Atomic Evaluation Boundary Completeness Resolution ID and Digest
+ Exact Atomic Registration Resolution Set Digest
+ Aggregate Rule Version
```

只有边界登记为 `REGISTERED` 且完整性为 `COMPLETE` 才能支持确定聚合。

### QG-R4-18 子集选择必须失败关闭

```text
Atomic A = QUALIFIED
Atomic B = DISQUALIFIED
Complete Boundary = {A, B}

Aggregate over {A} -> INVALID_SUBSET
Aggregate over {A, B} -> CONFLICTED
```

## 五、治理工件统一登记

### QG-R4-19 治理工件类型必须封闭

```text
QUALIFICATION_SEMANTIC_COMPATIBILITY_RECORD
QUALIFICATION_COMPATIBILITY_DOMAIN_SNAPSHOT
QUALIFICATION_FORWARD_INTERPRETATION_CONTRACT
QUALIFICATION_RECALCULATION_REQUIREMENT
```

每种类型拥有独立稳定键、允许字段和注册表作用域。

### QG-R4-20 每类工件必须拥有逐类型稳定键

```text
Compatibility Record Key =
  Semantic Domain + Source Rule Version + Target Rule Version + Direction

Compatibility Domain Snapshot Key =
  Domain ID + Domain Version + Semantic Domain

Forward Interpretation Contract Key =
  Contract ID + Contract Version + Semantic Domain

Recalculation Requirement Key =
  Source Rule Version + Target Rule Version + Re-resolution Scope Digest
```

分类、成员、映射、结果或登记时间不得进入稳定键换根。

### QG-R4-21 候选治理工件必须使用统一信封

```text
Candidate Governance Artifact Envelope:
  Artifact Type
  Artifact Stable Key and Digest
  Exact Type-specific Payload
  Canonical Byte Contract and Digest Algorithm
  Candidate Payload Digest
  Candidate Construction Authority Reference
  Evidence References
```

### QG-R4-22 治理工件必须先冻结精确候选内容

```text
Candidate Governance Artifact
  -> independent institutional review
  -> applicable freeze authority and decision
  -> valid Institution Freeze Reference for exact payload
  -> Governance Artifact Registration Attempt
```

构造者、登记者和冻结权威必须分离。登记不能创建冻结。

### QG-R4-23 登记尝试和记录必须内容同一

```text
Candidate Artifact Payload Digest
= Frozen Content Digest
= Registered Artifact Payload Digest
```

登记尝试至少固定稳定键、候选、冻结引用、目标注册表、登记授权、尝试摘要、时间和失败证据。已登记记录保存完整归因和位置。

### QG-R4-24 工件登记解析必须四值失败关闭

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同键异分类、异成员、异映射、异重新资格要求或异冻结内容必须 `CONFLICTED`。不得以较新、较高版本号或登记时间选赢家。

### QG-R4-25 工件纠正和取代必须追加

非语义表示缺陷使用独立更正记录；语义变化必须产生新工件版本或新方向记录，并绑定取代关系。原工件、冲突和失败尝试永久保留。

### QG-R4-26 运行消费只允许登记冻结单例

```text
Artifact Registration Resolution = REGISTERED
+ exactly one content-identical Registered Artifact
+ valid Institution Freeze Reference
  -> Runtime Consumer Eligibility
```

其他结果使兼容性保持未知、域不可用、解释不可执行或重新资格要求未决。

## 六、回归与非法状态

### QG-R4-27 已通过接口不得回归

```text
B/T/K/Q/S/RR Consumption: PRESERVED
Qualification / Applicability Separation: PRESERVED
Atomic Three-value History: PRESERVED
Four-value Aggregate: STRENGTHENED
CR-0002 Basis Adapter: PRESERVED
CR-0003 Contract Scope and Proof Identity: PRESERVED
```

### QG-R4-28 以下状态必须失败关闭

- 未登记或冲突规则支持资格计算；
- 规则登记摘要与冻结内容不一致；
- 新操作从旧授权隐式继承；
- 原子评价边界遗漏失败尝试、空洞或相反记录；
- 聚合者构造或自证边界完整；
- 聚合选择完整边界的有利子集；
- 治理工件登记者修改候选载荷；
- 工件登记创建或推断制度冻结；
- 同键异工件按版本号或时间选赢家；
- 兼容域消费未登记兼容关系；
- 解释器消费冲突或未冻结契约；
- 更正覆盖原工件或原子资格历史。

## 七、候选级闭合声明

### QG-R4-29 R4 只声明四项内部阻断具备候选修复

```text
QG-IM-B1 Rule Registration Topology: CLOSED_AS_DRAFT
QG-IM-B2 Composite Authority Catalog: CLOSED_AS_DRAFT
QG-IM-B3 Atomic Evaluation Boundary and Completeness: CLOSED_AS_DRAFT
QG-IM-B4 Governance Artifact Registration: CLOSED_AS_DRAFT
Upstream Interface Regression Review: REQUIRED
Consumer Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0007-R4 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: QG-IM-B1 + QG-IM-B2 + QG-IM-B3 + QG-IM-B4
Proposal Revision Created: YES
Upstream Interface Regression Review: REQUIRED
Consumer Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先执行上游和消费接口回归检查，再执行复合独立模型复审。只有三项审查均无阻断，`WS-04` 模型工作流才可退出。
