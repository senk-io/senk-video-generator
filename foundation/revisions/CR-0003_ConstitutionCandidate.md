# 提交模型宪法候选稿

## 候选信息

```text
Proposal ID: CR-0003-CONSTITUTION-CANDIDATE
Title: Commit Model
Status: CONSTITUTION_CANDIDATE
Authority: NONE
Executable: NO
Consolidation Type: SEMANTIC_CONSOLIDATION
Consolidates: CR-0003-R4 + CR-0003-R5 + CR-0003-R6 + CR-0003-R7
Review Basis: CR-0003-R7-FINAL-CLOSURE-REVIEW
Proposer: Codex under user-authorized consolidation
External Approval Required: NO
Candidate Consistency Review Required: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
```

> 本文件是单一宪法候选稿，不是冻结制度。它不能授权运行时提交、改变正式事实、覆盖冻结原则或使任何依赖自动冻结。历史草案和审查记录继续作为不可覆盖的治理历史保存。

## 候选目的

本候选定义提交如何把已经成立的决策事实，在显式权威、确定性契约和受保护边界中投影为目标正式状态，并定义系统如何在不覆盖历史、不放大确定性和不遗漏适用来源的前提下解析提交结果与当前认识。

```text
Decision Fact
+ Commit Contract
+ Commit Execution Authority
  -> Commit Attempt
  -> Protected Authoritative Write
       -> Target Formal State Transition
       + Authoritative Transition Record

Historical Authoritative Sources
+ Qualified Evidence
+ Explicit Temporal Coordinate
+ Complete Dependency Closure
+ Safe Rule Compatibility
  -> Candidate Resolution
  -> Independent Registration
  -> Immutable Resolution History
  -> Derived Current Projection
```

## 规范边界

本候选中的“必须”“不得”和“只能”是待冻结的不变量候选。当前状态下它们只约束候选审查，不能作为运行时制度执行。

本候选不定义：

- 决策事实如何成立；
- 具体目标类型的业务迁移；
- 全局证据传播算法；
- 具体数据库、事务或消息实现；
- 具体提供者或视频领域规则；
- 制度冻结权威和冻结决定本身。

## 一、统一对象与角色边界

| 节点 | 类型 | 唯一目的 | 所有者或边界 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义提交不变量 | 冻结制度 |
| `Commit Contract` | 版本化值对象 | 定义目标迁移、证明、解析和投影契约 | 目标类型治理制度 |
| `Committer` | 执行角色 | 履行获授权提交尝试 | 无事实所有权 |
| `Commit Attempt Initiation Record` | 不可变运行时记录 | 在提交点前建立尝试身份 | 提交尝试账本 |
| `Commit Attempt Completion Record` | 不可变观察记录 | 保存尝试完成观察 | 提交尝试账本 |
| `Authoritative Transition Record` | 权威归因记录 | 使目标迁移归属于提交键和尝试 | 目标对象注册表 |
| `Non-application Proof Assembler` | 执行角色 | 组装候选未应用证明 | 无资格结论所有权 |
| `Candidate Non-application Proof Record` | 不可变候选记录 | 保存候选证明及来源 | 未登记证明账本 |
| `Non-application Proof Qualifier` | 执行角色 | 计算候选证明资格 | 无登记权威 |
| `Candidate Proof Qualification Record` | 不可变候选记录 | 保存候选资格结论 | 未登记资格账本 |
| `Proof Qualification Registrar` | 登记角色 | 登记内容相同的资格候选 | 无证明内容所有权 |
| `Registered Proof Qualification Record` | 不可变派生记录 | 保存获登记证明资格 | 证明资格账本 |
| `Proof Qualification Applicability Resolver` | 执行角色 | 计算资格在指定坐标是否适用 | 无登记权威 |
| `Candidate Qualification Applicability Record` | 不可变候选记录 | 保存候选资格适用性 | 未登记适用性账本 |
| `Qualification Applicability Registrar` | 登记角色 | 登记内容相同的适用性候选 | 无资格所有权 |
| `Registered Qualification Applicability Record` | 不可变派生记录 | 保存获登记资格适用性 | 资格适用性账本 |
| `Qualification Projection Builder` | 执行角色 | 构建指定键的当前资格投影 | 无正式事实所有权 |
| `Current Proof Qualification Projection` | 派生读面 | 表达指定坐标的可用证明资格 | 可删除并重建 |
| `Commit Resolver` | 执行角色 | 计算候选提交结果 | 无登记权威 |
| `Candidate Commit Resolution Record` | 不可变候选记录 | 保存候选提交解析 | 未登记提交解析账本 |
| `Commit Resolution Registrar` | 登记角色 | 登记内容相同的提交解析 | 无目标事实所有权 |
| `Registered Commit Resolution Record` | 不可变派生记录 | 保存获登记提交解析 | 提交解析账本 |
| `Target Reader` | 读取角色 | 读取获授权目标来源 | 无状态解释权威 |
| `Target Read Attempt Record` | 不可变观察记录 | 保存一次读取结果 | 读取记录账本 |
| `Target State Resolver` | 执行角色 | 计算候选目标状态解析 | 无登记权威 |
| `Candidate Target State Resolution Record` | 不可变候选记录 | 保存候选状态解析 | 未登记状态解析账本 |
| `Target State Resolution Registrar` | 登记角色 | 登记内容相同的状态解析 | 无目标事实所有权 |
| `Registered Target State Resolution Record` | 不可变派生记录 | 保存获登记状态解析 | 状态解析账本 |
| `Dependency Closure Builder` | 执行角色 | 构建候选传递依赖闭包 | 无登记和完整性权威 |
| `Candidate Dependency Closure Record` | 不可变候选记录 | 保存候选依赖集合和边界 | 未登记闭包账本 |
| `Dependency Closure Registrar` | 登记角色 | 登记内容相同的候选闭包 | 无完整性权威 |
| `Registered Dependency Closure Record` | 不可变派生记录 | 保存获登记依赖闭包 | 依赖闭包账本 |
| `Closure Completeness Qualifier` | 执行角色 | 计算闭包完整性 | 无闭包修改和登记权威 |
| `Candidate Closure Completeness Record` | 不可变候选记录 | 保存闭包完整性候选 | 未登记完整性账本 |
| `Closure Completeness Registrar` | 登记角色 | 登记内容相同的完整性候选 | 无投影权威 |
| `Registered Closure Completeness Record` | 不可变派生记录 | 保存获登记完整性结论 | 闭包完整性账本 |
| `Projection Builder` | 执行角色 | 构建有认识上限的候选投影 | 无正式事实所有权 |
| `Projection Publisher` | 发布角色 | 发布已完成审计登记的派生读面 | 无正式事实所有权 |
| `Current Resolution Projection` | 派生读面 | 表达指定坐标下的当前认识 | 可删除并重建 |
| `Projection Change Audit Record` | 追加式派生审计记录 | 保存投影快照变化 | 投影审计账本 |
| `Projection Publication Envelope` | 派生发布外壳 | 耦合投影与审计后的可消费发布 | 投影发布边界 |
| `Resolution Ledger Position` | 账本位置值 | 表达登记追加顺序 | 解析账本原子分配 |
| `Resolution Lineage ID` | 谱系标识值 | 标识语义演化图 | 依附于解析图 |
| `Temporal Query Coordinate` | 复合值对象 | 分离有效时点和认识截点 | 依附于解析请求 |
| `Knowledge Boundary Vector` | 复合边界值 | 固定各来源注册表认识边界 | 时间查询坐标 |
| `Qualification Projection Key` | 复合标识值 | 唯一标识资格投影 | 资格投影规则 |
| `Qualification Compatibility Domain Snapshot` | 不可变制度快照 | 固定可比较契约版本集合 | 资格治理制度 |
| `Forward Interpretation Contract` | 版本化制度契约 | 定义解析结果安全解释 | 解析治理制度 |
| `Qualification Forward Interpretation Contract` | 版本化制度契约 | 定义资格结果安全解释 | 资格治理制度 |
| `Institution Freeze Reference` | 制度引用值 | 证明制度版本合法冻结 | 制度注册表 |
| `Transaction` | 技术机制 | 实现保护边界 | 架构实现层 |

## 二、分层与单一目的

### CM-C-01 基础模型、运行时与实现必须分层

```text
Foundation -> invariants and authority types
Execution -> authorized roles
Architecture -> protected boundaries and ledgers
Target Registry -> target state and attribution
```

具体数据库、事务或提供者不能成为制度成功真源。

### CM-C-02 提交只有一个目的

提交只负责把适用决策事实授权的声明写集，在确定性契约和受保护权威边界内投影为目标正式状态。

提交不得作价值判断、选择策略、解释偏差、授予权威、修改制度、扩张迁移类型或扩大写集。

### CM-C-03 决策事实与提交历史独立

```text
Decision Fact -> may authorize Commit
Commit Outcome -/-> Decision Fact Mutation
```

提交失败、未知、对账或补偿都不能覆盖、删除或降级决策事实。

## 三、提交契约与权威

### CM-C-04 提交契约必须声明全部授权类型

每项 `Commit Contract` 或适用治理制度至少声明：

```text
Commit Execution Authority Type
Non-application Proof Assembly Authority Type
Non-application Proof Qualification Execution Authority Type
Non-application Proof Qualification Registration Authority Type
Qualification Applicability Resolution Execution Authority Type
Qualification Applicability Registration Authority Type
Qualification Projection Execution Authority Type
Commit Resolution Execution Authority Type
Commit Resolution Registration Authority Type
Target Read Authority Type
Target State Resolution Execution Authority Type
Target State Resolution Registration Authority Type
Temporal Query Resolution Execution Authority Type
Dependency Closure Build Execution Authority Type
Dependency Closure Registration Authority Type
Closure Completeness Qualification Execution Authority Type
Closure Completeness Registration Authority Type
Resolution Projection Execution Authority Type
Forward Interpretation Execution Authority Type
Projection Publication Authority Type
Projection Change Audit Registration Authority Type
Institution Freeze Reference Resolution Execution Authority Type
```

契约还必须声明目标、迁移、决策事实、源版本、前置条件、写集、保护边界、归因记录、字段存在性、规范化、证明规则、解析规则、谱系、时间坐标、闭包、投影、兼容性、来源排除和证据要求。

### CM-C-05 权威不得隐式传播

任一执行、读取、计算、登记、解释、发布或冻结引用解析权威都不自动产生另一项权威。

同一主体可以持有多项独立授权，但必须使用不同任务契约、输入边界、输出记录和执行身份。

### CM-C-06 每项授权必须具有完整作用域

```text
Subject or Role Identity
Allowed Object Types
Allowed Object IDs or Scope
Allowed Input Source Types
Allowed Output Record Types
Allowed Rule Versions
Validity Window
Can Change
Cannot Change
```

读取授权必须限定来源；投影授权必须限定派生读面；发布授权不得包含正式事实写入；冻结引用解析授权不得创建冻结决定。

### CM-C-07 执行角色不得自证

- 证明组装者不能宣布证明合格；
- 资格计算者不能登记自身结论；
- 适用性解析者不能登记自身结论；
- 闭包构建者不能登记或证明自身闭包完整；
- 投影器不能创建来源适用性、制度契约或正式事实；
- 解释器不能创建解释契约或执行重新资格计算；
- 发布者不能把投影升级为正式事实；
- 冻结引用解析者不能创建制度冻结。

## 四、提交尝试与权威迁移

### CM-C-08 尝试身份必须先于提交点

`Commit Attempt Initiation Record` 必须在提交点前不可变登记，至少绑定：

```text
Commit Key
Commit Attempt ID
Decision Fact Reference
Commit Contract Version
Commit Execution Authority Reference
Target Object ID
Expected Source Version
Declared Write-set Digest
Opened At
```

```text
No Initiation Record
  -> No Commit-point Entry
  -> No Protected Authoritative Write
```

### CM-C-09 完成观察不证明提交结果

`Commit Attempt Completion Record` 只记录可观察完成情况，不能独自支持 `COMMITTED` 或 `ABORTED`。完成观察缺失也不否定可能已经成立的目标迁移。

### CM-C-10 前置检查、写入与归因共享保护边界

```text
Check Commit-point Preconditions
+ Apply Declared Write Set
+ Create Authoritative Transition Record
= One Protected Boundary
```

目标迁移和归因记录必须原子耦合。归因记录至少绑定提交键、尝试、决策事实、契约版本、前后目标版本、写集摘要、提交时点和保护边界标识。

### CM-C-11 COMMITTED 只确认归因

```text
Target Formal State Transition
+ Authoritative Transition Record
+ Sufficient Attribution Evidence
-> Candidate Commit Resolution = COMMITTED
```

`COMMITTED` 不创建目标迁移。解析或登记迟到不能否定已经发生的权威迁移。

### CM-C-12 提交结果保持三值

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：声明迁移完整形成并唯一归属于提交键；
- `ABORTED`：合格且当前适用的未应用证明确认提交键没有形成声明迁移；
- `INDETERMINATE`：现有合格来源不能证明前两者。

`CONFLICTED` 只属于当前投影，不属于单次提交解析。

## 五、未应用证明与资格

### CM-C-13 未应用证明组装必须获授权

候选证明至少保存：

```text
Candidate Proof ID
Proof Type
Commit Key
Commit Attempt ID
Target Object ID
Commit Contract Version
Claimed Closed Boundary or Version Range
Source Evidence References
Assembled At
Assembler Identity
Assembly Authority Reference
Candidate Content Digest
```

合法证明类型只有：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

未找到记录、缓存未命中、异步日志缺失和读取不可用不构成未应用证明。

### CM-C-14 证明资格计算与登记必须分离

```text
Candidate Non-application Proof Record
+ Qualification Rule
+ Qualification Execution Authority
-> Candidate Proof Qualification Record

Candidate Proof Qualification Record
+ Qualification Registration Authority
+ Deterministic Admissibility Check
-> Registered Proof Qualification Record
```

登记必须保持候选内容同一性。

### CM-C-15 历史证明资格保持三值

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
```

资格只回答证明在指定规则、证据和时点下是否可作为解析输入，不证明目标迁移不存在，也不产生 `ABORTED`。

### CM-C-16 历史资格不等于永久适用

```text
Registered Qualification = QUALIFIED at T1
-/-> Qualified for every future temporal coordinate
```

资格后来失效只能追加适用性记录、失效来源或证据更正，不得修改旧资格。

### CM-C-17 资格适用性必须独立解析和登记

```text
Registered Qualification Records
+ Source Applicability Inputs
+ Evidence Correction References
+ Applicability Rule Version
+ Temporal Query Coordinate
-> Candidate Qualification Applicability Record
-> Independent Registration
```

适用性值域为：

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

### CM-C-18 适用性记录必须绑定来源和双时间坐标

至少绑定：

```text
Proof Qualification Record IDs
Candidate Proof ID
Commit Contract Version
Qualification and Applicability Rule Versions
Source Evidence Versions
Source Applicability and Correction Record IDs
Validity As Of
Knowledge Boundary Vector
Observed At
Produced At
Authority References
```

无法确定旧 `As Of` 含义时使用 `UNRESOLVED`，不得猜测。

### CM-C-19 当前证明资格投影必须使用稳定键

```text
Qualification Projection Key:
  Candidate Proof ID
  Commit Key
  Qualification Scope Mode
  Exact Contract Version or Compatibility Domain Snapshot
  Validity As Of
  Knowledge Boundary Vector
  Qualification Projection Rule Version
```

任何一项变化都产生新键。跨证明、提交键、作用域或认识边界复用非法。

### CM-C-20 资格作用域模式严格二选一

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

精确模式必须填写一个契约版本并把兼容域字段标为 `NOT_APPLICABLE`。兼容域模式必须填写一个不可变域快照并把精确版本字段标为 `NOT_APPLICABLE`。

兼容域快照至少绑定域标识、域版本、精确成员枚举、成员摘要、成员规则版本、治理制度、冻结引用、有效时点和认识边界向量。成员变化必须产生新域版本、新摘要和新投影键。

### CM-C-21 当前资格投影使用完备真值表

在相同稳定键、语义可比较且依赖完整时：

```text
Applicable comparable QUALIFIED only -> QUALIFIED
Applicable comparable DISQUALIFIED only -> DISQUALIFIED
Applicable comparable QUALIFIED + DISQUALIFIED -> CONFLICTED
Required applicability, lineage or compatibility unresolved -> INDETERMINATE
No applicable qualification record -> INDETERMINATE
```

适用性冲突和资格结果冲突必须分别保存，不能用一个字段隐藏冲突层级。

### CM-C-22 ABORTED 只能引用当前可用的精确资格投影

`ABORTED` 候选必须同时引用：

```text
Historical Proof Qualification = QUALIFIED
Current Proof Qualification Projection = QUALIFIED
Exact Qualification Projection Key
Same Candidate Proof ID and Commit Key
Compatible Commit Contract Scope
Matching Temporal Query Coordinate
Registered Closure Completeness = COMPLETE
```

任一项未决时，提交解析只能保持 `INDETERMINATE`。

## 六、候选、登记与字段存在性

### CM-C-23 候选计算与登记必须分别授权

提交解析、状态解析、资格、适用性、依赖闭包和闭包完整性都采用：

```text
Authorized Candidate Computation
  -> Immutable Candidate Record
  -> Candidate Content Digest

Independent Registration
  -> Deterministic Admissibility Check
  -> Content-identical Registration Envelope
```

### CM-C-24 登记必须保证内容同一性

```text
Candidate Content Digest
= Registered Content Digest
```

摘要必须使用相同规范化规则、字段覆盖、字段存在性语义和算法标识。登记外壳只能增加授权、准入、账本位置和登记时间元数据。

候选即使未登记、被拒绝或不确定，也必须保留在对应候选账本中。

### CM-C-25 字段存在性保持三分

```text
VALUE(value)
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
```

三类状态必须进入规范摘要。静默省略规范字段非法；显示默认值不得进入正式推导。

## 七、读取与目标状态解析

### CM-C-26 读取、状态解析和登记分别授权

```text
Target Read Authority
  -> Target Read Attempt Record

Target State Resolution Execution Authority
  -> Candidate Target State Resolution Record

Target State Resolution Registration Authority
  -> Registered Target State Resolution Record
```

读取能力不产生状态解释权威，状态解析执行权威不产生登记权威。

### CM-C-27 读取结果与状态解析保持分离

```text
Target Read Outcome:
  AVAILABLE | UNAVAILABLE

Target State Resolution:
  RESOLVED | INDETERMINATE
```

读取可用不保证状态可解析；读取不可用不删除此前权威状态。解析记录只能保存直接制度原因，不能混入技术根因诊断。

## 八、时间坐标与认识视图

### CM-C-28 时间查询坐标必须双轴化

```text
Temporal Query Coordinate:
  Validity As Of
  Knowledge Boundary Vector
  Produced At
```

- `Validity As Of` 描述被查询现实的有效时点；
- `Knowledge Boundary Vector` 描述允许消费的多注册表登记边界；
- `Produced At` 描述本次计算发生时间。

三者不得互相替代。

### CM-C-29 认识边界必须是多注册表稳定向量

```text
Knowledge Boundary Vector:
  Registry Boundary Entries[]
  Vector Digest
  Boundary Rule Version
  Established At
```

每个条目至少绑定注册表标识、作用域、包含水位或精确来源集合、边界权威引用。单一时间标签只能用于显示，不能代替规范向量。

### CM-C-30 边界向量必须因果闭合

边界内记录的每项必需依赖必须位于对应注册表边界内，或由制度明确标为 `NOT_APPLICABLE`。

```text
Required dependency outside boundary
  -> CAUSALLY_INCOMPLETE
  -> Closure Completeness = INDETERMINATE
  -> Projection = INDETERMINATE
```

### CM-C-31 历史认识与当前重述必须分离

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

历史认识视图只能消费其边界内已登记记录；当前重述视图可以在新边界下消费后续更正，但不得冒充当时认识。

同一有效时点在不同认识边界下允许产生不同合法投影快照，不表示目标现实发生多次迁移。

## 九、解析账本与语义谱系

### CM-C-32 账本位置只表达追加顺序

每项已登记解析必须取得同一作用域内原子分配且唯一的 `Resolution Ledger Position`。位置不表达细化、重申或冲突。

候选作用域：

```text
Commit Resolution Scope = Commit Key
Target State Resolution Scope = Target Object ID + State Resolution Subject
```

具体作用域由契约声明。

### CM-C-33 语义谱系独立于账本位置

每项已登记解析必须保存：

```text
Resolution Lineage ID
Prior Resolution Record References
Resolution Relationship
```

合法关系：

```text
INITIAL
REFINES
REAFFIRMS
CONFLICTS_WITH
```

并发分支可以引用同一父记录，不得覆盖彼此。`CONFLICTS_WITH` 可以连接同谱系分支或同一解析作用域内的不同初始谱系。

### CM-C-34 单条提交解析只允许提高确定性

```text
INDETERMINATE -> COMMITTED
INDETERMINATE -> ABORTED
INDETERMINATE -> INDETERMINATE
```

`COMMITTED` 与 `ABORTED` 不能通过 `REFINES` 或最后记录获胜相互覆盖，只能通过冲突关系保留。

## 十、依赖闭包与完整性

### CM-C-35 投影必须使用登记的依赖闭包

候选闭包至少声明：

```text
Root Scope and Record IDs
Authoritative Source Registry IDs and Scopes
Required Edge Types
Traversal Rule Version
Temporal Query Coordinate
Closed-world or Open-world Semantics
```

闭包构建、登记、完整性计算和完整性登记分别授权。

### CM-C-36 每个注册表必须提供独立完整性边界

合法边界证明包括：

```text
Complete Prefix Proof
Exact Registered Source Set with authoritative digest
Frozen Snapshot Boundary
Institutionally equivalent completeness proof
```

一个注册表的边界不能证明另一个注册表完整。解析账本水位不能自动覆盖证据、更正、资格、兼容和排除账本。

### CM-C-37 开放世界中的缺失不能证明不存在

```text
Open-world Scope + Source Not Found
  -/-> Source Absent
  -/-> Source Inapplicable
```

没有权威枚举边界时，闭包完整性和投影都必须保持 `INDETERMINATE`。

### CM-C-38 闭包完整性保持三值

```text
COMPLETE
INCOMPLETE
INDETERMINATE
```

`COMPLETE` 要求全部根已访问、全部必需边已评估、发现节点已纳入或制度排除、没有未解析前沿、全部注册表边界匹配认识向量且满足因果闭包。

只有已登记 `COMPLETE` 能支持终局投影。闭包摘要只证明所给内容同一，不证明来源全集完整。

## 十一、认识偏序、兼容与重新解析

### CM-C-39 提交和资格认识强度采用偏序

```text
Commit:
  INDETERMINATE <= COMMITTED
  INDETERMINATE <= ABORTED
  COMMITTED and ABORTED are incomparable terminals

Qualification:
  INDETERMINATE <= QUALIFIED
  INDETERMINATE <= DISQUALIFIED
  QUALIFIED and DISQUALIFIED are incomparable terminals
```

`CONFLICTED` 是冲突投影状态，不属于更高或更低认识等级。

### CM-C-40 投影确定性不得超过适用来源

```text
Projection Certainty
<= Strongest Applicable Qualified Source Certainty
```

投影只消费适用、合格、版本兼容、依赖完整、时点有效且位于认识边界内的来源。来源数量、置信度、默认偏好和登记时间不能提升认识强度。

全部来源不确定、必需依赖未决、来源集合不完整或兼容性未知时，投影必须为 `INDETERMINATE`。

### CM-C-41 可比较终局冲突必须可见

```text
Comparable applicable COMMITTED + ABORTED
  -> Commit Projection = CONFLICTED

Comparable applicable QUALIFIED + DISQUALIFIED
  -> Qualification Projection = CONFLICTED
```

不得用较新记录、多数来源、模型置信度或来源身份选择一个终局。

### CM-C-42 来源排除必须受冻结制度约束

`Institutional Source Exclusion Basis` 至少绑定允许来源类型、排除条件、权威类型、规则版本、证据、作用域、时间坐标和制度冻结引用。

投影器不能临时发明排除理由。排除只改变指定投影来源集合，不删除来源历史。

### CM-C-43 跨规则兼容必须显式分类

```text
IDENTICAL_SEMANTICS
FORWARD_INTERPRETABLE
REQUIRES_RERESOLUTION
INCOMPATIBLE
UNKNOWN_COMPATIBILITY
```

兼容关系必须绑定明确版本或不可变兼容域快照，不得依据版本号大小推断。

`INCOMPATIBLE` 和 `UNKNOWN_COMPATIBILITY` 导致 `INDETERMINATE`，不自动产生事实冲突。

### CM-C-44 解析前向解释不得放大确定性

每项 `FORWARD_INTERPRETABLE` 必须引用冻结的 `Forward Interpretation Contract`，保留字段存在性、证据引用、源记录和认识强度。

```text
Interpret(INDETERMINATE) -> INDETERMINATE
Interpret(COMMITTED) -> COMMITTED or INDETERMINATE
Interpret(ABORTED) -> ABORTED or INDETERMINATE
Interpret(CONFLICTED) -> CONFLICTED or INDETERMINATE
Interpret(UNRESOLVED) -> UNRESOLVED
```

### CM-C-45 资格前向解释不得放大确定性

每项资格 `FORWARD_INTERPRETABLE` 必须引用冻结的 `Qualification Forward Interpretation Contract`。

```text
InterpretQualification(INDETERMINATE) -> INDETERMINATE
InterpretQualification(QUALIFIED) -> QUALIFIED or INDETERMINATE
InterpretQualification(DISQUALIFIED) -> DISQUALIFIED or INDETERMINATE
InterpretQualification(CONFLICTED) -> CONFLICTED or INDETERMINATE
```

解释不得改变候选证明、提交键、作用域模式、契约版本或域快照、有效时点和认识边界向量。

### CM-C-46 提高确定性必须追加重新解析历史

解析结果需要提高确定性时：

```text
REQUIRES_RERESOLUTION
  -> New Authorized Resolution
  -> New Candidate
  -> Independent Registration
```

资格结果需要提高、跨终局转换或改变作用域时：

```text
REQUIRES_RERESOLUTION
+ Required Re-resolution Kind = REQUALIFICATION
  -> New Qualification Candidate
  -> Independent Registration
  -> Applicability and Closure Rebuild
```

任何重新解析都不能覆盖旧记录。

## 十二、当前投影演化与发布

### CM-C-47 当前投影是可重建派生读面

提交投影值域：

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

目标状态投影值域：

```text
RESOLVED | INDETERMINATE | CONFLICTED
```

资格投影值域：

```text
QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED
```

投影必须绑定类型、作用域、时间坐标、规则版本、来源集合、依赖闭包、谱系摘要、冲突引用和生成时间。投影缓存可删除和重建。

### CM-C-48 当前投影可以降级和冲突

合法派生变化包括：

```text
terminal -> INDETERMINATE
terminal -> CONFLICTED
```

前提包括来源资格失效、证据更正、依赖未决、规则不兼容或可比较冲突。变化不修改历史解析、目标状态或决策事实。

### CM-C-49 投影恢复必须选择显式路径

合法恢复主路径只有：

```text
PATH_A_NEW_SUPPORT
PATH_B_AUTHORIZED_EXCLUSION_OR_INVALIDATION
PATH_C_COMPATIBILITY_OR_LEGALITY_RESOLUTION
```

- 新支持路径要求新的已登记解析或资格、适用证据、兼容规则、完整闭包和受权重建；
- 排除或失效路径要求冻结制度依据、权威、证据、作用域、时间坐标、完整剩余闭包且无剩余终局冲突；
- 兼容或合法性路径要求新的已登记结论、治理制度、权威、证据、非放大解释或必要的重新解析，以及完整闭包。

投影器不能自行裁决冲突。

### CM-C-50 投影变化必须追加审计

审计至少保存：

```text
Projection Type and Scope
Previous and New Projection Digests
Previous and New Temporal Coordinates
Projection Rule Version
Added and Removed Applicable Source IDs
Applicability Change Record IDs
Dependency Closure References
Change Reason Code
Generated At
Projection Execution Authority Reference
```

首次投影使用 `NOT_APPLICABLE` 作为前一摘要。审计不是正式事实，也不能成为投影来源真值。

### CM-C-51 审计登记先于可消费投影发布

```text
Candidate Projection Snapshot
+ Candidate Projection Change Audit Record
+ Projection Publication Authority
+ Projection Change Audit Registration Authority
-> Projection Publication Envelope
```

审计追加失败时，新投影发布必须阻断；候选仍可本地重建，旧发布快照保持历史。

### CM-C-52 投影不产生正式事实或未来行动

```text
Current Projection
!= Formal Fact
!= Decision Fact
!= Historical Resolution Record

Projection = ABORTED -/-> Retry
Projection = INDETERMINATE -/-> Cancel Decision
Projection = CONFLICTED -/-> Select Preferred Source
```

未来行动仍由独立策略或决策授权。

## 十三、制度出处与冻结引用

### CM-C-53 兼容、解释和排除契约必须具有制度出处

`Forward Interpretation Contract`、`Qualification Forward Interpretation Contract`、兼容关系、兼容域快照和来源排除依据只能通过 `IF-0007` 的制度提案、审查和冻结路径建立。

运行时配置、知识条目、文件路径和模型声明不能创建这些契约。

### CM-C-54 制度资格必须由冻结引用验证

`Institution Freeze Reference` 至少包含：

```text
Freeze ID
Institution ID and Version
Frozen Content Digest
Freeze Decision Reference
Freeze Authority Reference
Freeze Evidence Package Reference
Effective Scope
Validity Interval
```

缺失、摘要不匹配、作用域不匹配或有效区间不成立时，契约不可用于运行时投影，兼容性保持未知。

冻结引用只证明制度资格，不证明具体资格、解析或投影结果正确。

## 十四、幂等、重试、对账与外部副作用

### CM-C-55 幂等和并发不得覆盖历史

同一提交键和声明内容不得形成第二次迁移；同键不同内容非法。`INDETERMINATE` 未解析前不得换键绕过幂等保护。

并发候选、资格、解析和投影来源必须全部保留，不能最后写入获胜。

### CM-C-56 ABORTED 不授权重试

```text
Commit Outcome or Projection = ABORTED
-/-> Retry Authorized
```

重试只能由独立策略依据决策效力、契约、源版本、预算、冲突行为、证明和历史授权。

### CM-C-57 对账和补偿只能追加历史

对账只能产生新候选和登记记录。补偿必须通过新决策和新提交，不得删除旧迁移、归因、证明、资格或解析历史。

### CM-C-58 外部副作用不属于隐式原子边界

通知、发布、文件分发、模型调用或第三方写入不能与目标权威迁移共享不可分割边界时，必须独立建模。

同一数据库、多个本地事务、消息发件箱、流程编排或补偿机制不能单独证明全局原子性。

## 十五、完整运行路径

### 提交与目标迁移

```text
Decision Fact
  -> Commit Contract and Authority Resolution
  -> Commit Attempt Initiation
  -> Commit-point Preconditions
       -> MET
            -> Protected Authoritative Write
                 -> Target Formal State Transition
                 + Authoritative Transition Record
       -> NOT_MET or uncertain
            -> no target write unless protected boundary proves otherwise
  -> Completion Observation when available
```

### 未应用证明与当前资格

```text
Authorized Proof Assembly
  -> Candidate Non-application Proof

Authorized Qualification
  -> Candidate Qualification
  -> Independent Registration

Authorized Applicability Resolution
  -> Candidate Applicability
  -> Independent Registration

Stable Qualification Projection Key
+ Safe Compatibility
+ Complete Causal Dependency Closure
  -> Current Proof Qualification Projection
```

### 提交和状态解析

```text
Authorized Commit Resolution
  -> COMMITTED from authoritative transition attribution
  -> ABORTED from exact current QUALIFIED proof projection
  -> otherwise INDETERMINATE
  -> Candidate Commit Resolution
  -> Independent Registration

Authorized Target Read
  -> Target Read Attempt

Authorized Target State Resolution
  -> Candidate State Resolution
  -> Independent Registration
```

### 当前认识投影

```text
Temporal Query Coordinate
+ Registered Resolution Histories
+ Complete Causal Dependency Closure
+ Semantic Lineage
+ Safe Rule Compatibility
+ Epistemic Ceiling
  -> Candidate Current Projection
  -> Projection Change Audit Registration
  -> Consumable Projection Publication Envelope
  -> Optional Independent Policy Evaluation
```

## 十六、权威操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Committer` | 建立尝试、履行契约写入、记录完成观察 | 新裁决、解析结果、自行重试 |
| `Proof Assembler` | 组装候选证明 | 宣布资格、产生 `ABORTED` |
| `Proof Qualifier` | 计算资格候选 | 登记自身结果、修改证据 |
| `Qualification Applicability Resolver` | 计算适用性候选 | 登记自身结果、创建提交解析 |
| `Qualification Projection Builder` | 构建稳定键资格投影 | 跨键复用、忽略相反来源 |
| `Commit Resolver` | 计算提交解析候选 | 登记自身结果、补写证明 |
| `Target Reader` | 读取获准来源 | 解释目标状态、扩大范围 |
| `Target State Resolver` | 计算状态解析候选 | 登记自身结果、修改目标 |
| `Dependency Closure Builder` | 构建候选闭包 | 登记或证明自身完整 |
| `Closure Completeness Qualifier` | 计算完整性候选 | 修改闭包或来源注册表 |
| 各类 `Registrar` | 登记内容相同的合格候选 | 改写候选、继承其他权威 |
| `Forward Interpreter` | 按冻结契约进行非放大解释 | 提高确定性、改变作用域 |
| `Projection Builder` | 使用完整输入构建候选投影 | 修改历史、创建正式事实 |
| `Projection Publisher` | 审计登记后发布派生读面 | 发布无审计投影、创建正式事实 |
| `Institution Freeze Reference Resolver` | 验证冻结引用 | 创建冻结决定或制度权威 |
| `Policy Selector` | 决定是否授权未来行动 | 修改提交、证明、资格或解析事实 |

## 十七、非法状态总表

以下情况一律非法：

- 角色没有适用授权却执行；
- 权威在执行、读取、资格、登记、解释、投影、发布或冻结角色间隐式传播；
- 没有提交尝试身份就进入提交点；
- 目标迁移与归因记录不在同一保护边界；
- `COMMITTED` 反向创建目标迁移；
- 完成观察、文件存在或接口成功替代提交解析；
- 未找到记录、缓存缺失或读取失败被当作未应用证明；
- 没有已登记且当前适用的精确 `QUALIFIED` 投影就产生 `ABORTED`；
- 资格、适用性、闭包或解析计算者登记自身结论；
- 登记者修改候选内容；
- 候选或历史记录被删除、覆盖或静默丢弃；
- 静默省略字段或用默认值解析 `UNRESOLVED`；
- 读取结果被当作目标状态解析；
- 用一个宽泛 `As Of` 混合有效时点和认识截点；
- 后来记录静默进入历史认识视图；
- 当前重述冒充历史认识；
- 用单一时间戳替代多注册表边界向量；
- 使用因果不闭合的边界产生终局投影；
- 跨证明、提交键、契约模式或域快照复用资格投影；
- 一个资格键同时使用精确契约和兼容域模式；
- 兼容域成员变化后复用旧版本、摘要或投影键；
- 忽略适用的相反资格或终局解析；
- 把不兼容规则误报为事实冲突；
- 用版本号、新旧关系、模型置信度或多数来源推断结果；
- 解释把 `INDETERMINATE` 提升为终局或在终局间转换；
- 需要重新资格计算时只重建投影；
- 用一个注册表水位证明多个注册表完整；
- 用摘要证明来源全集完整；
- 在开放世界中用未找到来源证明不存在；
- 传递闭包仍有未解析前沿却登记 `COMPLETE`；
- 投影器临时创建兼容、解释或来源排除契约；
- 制度状态文本、文件或模型声明替代冻结引用；
- 冻结引用无效时仍使用契约；
- 投影审计未登记却发布新投影；
- 投影、审计或资格自动创建正式事实或未来行动授权；
- `ABORTED` 自动授权重试；
- 对账、补偿、缓存或最后写入覆盖历史；
- 外部副作用成功替代目标权威迁移。

发现任何非法状态时，系统必须失败关闭并保留现有证据和历史。

## 十八、与相邻模型的关系

```text
Decision Fact -> may authorize deterministic commit
Evidence -> supports observations, proofs and applicability
Proof Qualification -> determines proof admissibility
Qualification Projection -> determines current proof usability
Commit Resolution -> classifies one commit attribution
Target State Resolution -> classifies target state at a coordinate
Current Projection -> derives current usable knowledge
Policy -> may authorize retry or future execution
Institution -> defines all governing invariants and contracts
```

任何一层都不得代替相邻层。

## 十九、合并来源覆盖映射

| 来源 | 合并内容 |
|---|---|
| `CR-0003-R4` | 提交主干、尝试身份、保护边界、证明资格、解析登记、账本谱系、兼容分类、幂等和外部副作用 |
| `CR-0003-R5` | 资格适用性生命周期、认识上限、冲突保留、投影演化、来源适用性接口 |
| `CR-0003-R6` | 双时间坐标、资格真值表、依赖闭包完整性、恢复路径和审计发布边界 |
| `CR-0003-R7` | 资格认识偏序、资格非放大解释、重新资格计算、兼容域快照、因果边界向量和冻结引用 |

后续审查应只以本候选稿作为当前模型对象，同时保留全部来源草案用于谱系、差异和遗漏核查。

## 二十、候选状态与冻结门槛

```text
Candidate Semantic Consolidation: COMPLETED
Candidate Consistency Review: REQUIRED
Candidate Type Audit: REQUIRED
Candidate Authority Audit: REQUIRED
Candidate Causality Audit: REQUIRED
Candidate Terminology Audit: REQUIRED
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
```

即使候选审查通过，仍必须满足：

1. `CR-0002-R1` 或兼容决策模型已经冻结；
2. 来源注册表和资格治理制度能够提供本候选要求的接口与冻结契约；
3. 制度注册表能够验证 `Institution Freeze Reference`；
4. 已建立满足 `IF-0007` 的重复性、稳定性、跨提供者、跨项目、兼容性和迁移证据；
5. 已声明提案者、审查者和冻结权威；
6. 已形成正式冻结决定、唯一冻结标识和版本边界。

在这些条件满足前，本候选始终保持：

```text
Status: CONSTITUTION_CANDIDATE
Authority: NONE
Executable: NO
```

建议动作：对本单一候选稿执行对象图、类型、权威、因果、时间、认识上限和术语一致性审查。发现合并遗漏或语义冲突时建立新的候选修订，不修改历史草案，也不得直接冻结。

