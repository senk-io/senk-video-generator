# 提交模型提案第四修订版

## 提案信息

```text
Proposal ID: CR-0003-R4
Title: Commit Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0003-R3
Review Basis: CR-0003-R3-LOCAL-REVIEW
Reviewer: Codex
External Approval Required: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
Derived From: CR-0003-TYPE-AUDIT
```

> 本文件是待审查修订提案，不是冻结制度。它不能授权运行时提交、改变正式事实、覆盖现行原则或使任何上游提案自动冻结。

## 修订范围

本版保留 `CR-0003-R3` 已经通过的尝试身份、字段存在性、内容同一性、投影和重试边界，只处理本地独立审查确认的四项模型阻断：

1. 补齐解析、读取、状态解析和投影构建的执行授权；
2. 为未应用证明建立组装、资格计算和资格登记边界；
3. 分离解析账本位置与语义谱系，定义并发登记不变量；
4. 为跨解析规则版本投影建立兼容性契约。

以下冻结门槛仍明确保留：

```text
CR-0002-R1 Decision Model must be frozen first
IF-0007 Institution Freeze Evidence must be sufficient
```

## 核心定义

> 提交是受制度约束的确定性投影过程。任何执行、读取、候选计算、资格计算、登记和投影都必须拥有独立适用授权；未应用证明必须先取得资格；解析账本的追加顺序与认识谱系必须分离；跨规则版本只有在显式兼容关系下才能共同投影。

```text
Authorized Commit Attempt
  -> Protected Authoritative Write
       -> Target Formal State Transition
       + Authoritative Transition Record

Authorized Proof Assembly
  -> Candidate Non-application Proof Record
  -> Authorized Proof Qualification
  -> Registered Proof Qualification Record

Authorized Resolution Execution
  -> Candidate Resolution Record
  -> Authorized Resolution Registration
  -> Registered Resolution Record

Registered Resolution Records
+ Ledger Completeness
+ Semantic Lineage
+ Rule Compatibility
+ Authorized Projection Execution
  -> Current Resolution Projection
```

## 统一对象与角色边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义提交不变量 | 冻结制度 |
| `Commit Contract` | 值对象 | 定义目标迁移和解析契约 | 目标类型治理制度 |
| `Committer` | 执行角色 | 履行提交尝试 | 无事实所有权 |
| `Commit Attempt Initiation Record` | 不可变运行时记录 | 在提交点前建立尝试身份 | 提交尝试账本 |
| `Commit Attempt Completion Record` | 不可变观察记录 | 保存尝试完成观察 | 提交尝试账本 |
| `Authoritative Transition Record` | 权威迁移归因记录 | 使目标迁移归属于提交键和尝试 | 目标对象注册表 |
| `Non-application Proof Assembler` | 执行角色 | 组装候选未应用证明 | 无资格结论所有权 |
| `Candidate Non-application Proof Record` | 不可变候选记录 | 保存候选证明包及来源 | 未登记证明账本 |
| `Non-application Proof Qualifier` | 执行角色 | 计算候选证明资格 | 无登记权威 |
| `Candidate Proof Qualification Record` | 不可变候选记录 | 保存候选资格结论 | 未登记资格账本 |
| `Proof Qualification Registrar` | 登记角色 | 登记合格的资格候选 | 无证明内容所有权 |
| `Registered Proof Qualification Record` | 不可变派生记录 | 保存获准登记的证明资格 | 证明资格账本 |
| `Commit Resolver` | 执行角色 | 计算候选提交结果 | 无登记权威 |
| `Candidate Commit Resolution Record` | 不可变候选记录 | 保存候选提交解析 | 未登记提交解析账本 |
| `Commit Resolution Registrar` | 登记角色 | 登记内容相同的合格提交解析 | 无目标事实所有权 |
| `Registered Commit Resolution Record` | 不可变派生记录 | 保存获准登记的提交解析 | 提交解析账本 |
| `Target Reader` | 读取角色 | 读取目标权威来源 | 无状态解释权威 |
| `Target Read Attempt Record` | 不可变观察记录 | 保存一次读取结果 | 读取记录账本 |
| `Target State Resolver` | 执行角色 | 计算候选状态解析 | 无登记权威 |
| `Candidate Target State Resolution Record` | 不可变候选记录 | 保存候选状态解析 | 未登记状态解析账本 |
| `Target State Resolution Registrar` | 登记角色 | 登记内容相同的合格状态解析 | 无目标事实所有权 |
| `Registered Target State Resolution Record` | 不可变派生记录 | 保存获准登记的状态解析 | 状态解析账本 |
| `Projection Builder` | 执行角色 | 计算或重建解析投影 | 无正式事实所有权 |
| `Current Resolution Projection` | 派生读面 | 表达指定时点可用认识 | 无独立事实所有权，可重建 |
| `Resolution Ledger Position` | 账本位置值 | 表达登记追加顺序 | 解析账本原子分配 |
| `Resolution Lineage ID` | 谱系标识值 | 标识一张相连的语义演化图 | 依附于解析记录图 |
| `Transaction` | 技术机制 | 实现原子性与隔离性 | 架构实现层 |

## CM-R4-01 基础模型、运行时和技术实现必须分层

```text
Foundation -> defines invariants and authority types
Execution -> performs authorized roles
Architecture -> implements protected boundaries and ledgers
Target Registry -> owns target state and attribution
```

模型不得绑定具体提供者；技术机制不得成为制度成功真源。

## CM-R4-02 提交只有一个目的

提交只负责把适用决策事实授权的声明写集，在确定性契约和受保护权威边界内投影为目标正式状态。

提交不得作价值判断、选择策略、解释偏差、授予权威、修改制度、扩大迁移类型或扩张写集。

## CM-R4-03 决策事实与提交历史相互独立

```text
Decision Fact -> may authorize Commit
Commit Outcome -/-> Decision Fact Mutation
```

提交结果不能覆盖、删除或降级决策历史。

## CM-R4-04 提交契约必须声明全部授权类型

每项 `Commit Contract` 至少声明：

```text
Commit Execution Authority Type
Non-application Proof Assembly Authority Type
Non-application Proof Qualification Execution Authority Type
Non-application Proof Qualification Registration Authority Type
Commit Resolution Execution Authority Type
Commit Resolution Registration Authority Type
Target Read Authority Type
Target State Resolution Execution Authority Type
Target State Resolution Registration Authority Type
Resolution Projection Execution Authority Type
```

还必须声明目标、迁移、决策事实、源版本、前置条件、写集、原子边界、归因记录、字段存在性、摘要规范化、证明资格、解析规则、谱系规则、投影规则、兼容性和证据要求。

## CM-R4-05 权威不得在角色之间隐式传播

```text
Commit Execution Authority
!= Proof Assembly Authority
!= Proof Qualification Authority
!= Resolution Execution Authority
!= Resolution Registration Authority
!= Target Read Authority
!= Target State Resolution Authority
!= Projection Execution Authority
```

同一主体可以持有多项独立授权，但必须使用独立任务契约、输入边界、输出记录和执行身份。

## CM-R4-06 每项执行授权必须具有完整作用域

每项授权至少限定：

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

读取授权还必须限定可读取的权威来源；投影授权还必须限定允许物化的派生读面和缓存边界。

## CM-R4-07 提交尝试身份先于提交点

`Commit Attempt Initiation Record` 必须在提交点前不可变登记，绑定提交键、尝试标识、决策事实、契约版本、执行授权、目标、预期源版本、写集摘要和开启时点。

```text
No Initiation Record
  -> No Commit-point Entry
  -> No Protected Authoritative Write
```

权威迁移记录不得引用未登记尝试标识。

## CM-R4-08 完成观察不证明提交结果

`Commit Attempt Completion Record` 只记录尝试结束时的可观察情况。它不能独自支持 `COMMITTED` 或 `ABORTED`。

完成观察缺失不删除尝试身份，也不否定可能已经成立的权威迁移。

## CM-R4-09 前置检查、写入和归因共享保护边界

```text
Check Commit-point Preconditions
+ Apply Declared Write Set
+ Create Authoritative Transition Record
= One Protected Boundary
```

目标迁移和权威迁移记录必须原子耦合。记录至少绑定提交键、尝试标识、决策事实、契约版本、前后权威版本、写集摘要、提交时点和原子边界标识。

## CM-R4-10 COMMITTED 只确认归因

```text
Target Formal State Transition
+ Authoritative Transition Record
+ Sufficient Attribution Evidence
-> Candidate Commit Outcome = COMMITTED
```

`COMMITTED` 不创建目标迁移。解析或登记迟到不能否定目标权威边界已经建立的事实。

## CM-R4-11 提交结果保持三值

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：声明迁移完整形成并唯一归属于提交键；
- `ABORTED`：合格未应用证明确认提交键没有形成声明迁移；
- `INDETERMINATE`：现有权威记录与证据不能证明前两种结果。

`CONFLICTED` 只属于投影层。

## CM-R4-12 未应用证明组装必须获得授权

`Non-application Proof Assembler` 只能在适用组装授权下读取契约允许的证据，并产生 `Candidate Non-application Proof Record`。

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

组装者不得宣布证明已经合格，也不得产生 `ABORTED`。

## CM-R4-13 未应用证明资格计算与登记必须分离

```text
Candidate Non-application Proof Record
+ Commit Contract Proof Rules
+ Proof Qualification Execution Authority
-> Non-application Proof Qualifier
     -> Candidate Proof Qualification Record

Candidate Proof Qualification Record
+ Proof Qualification Registration Authority
+ Deterministic Admissibility Check
-> Registered Proof Qualification Record
```

资格计算者不得登记自身结论；登记者不得改变候选资格内容。

## CM-R4-14 证明资格结果必须三值化

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
```

- `QUALIFIED`：候选证明满足指定契约版本的证明准入要求；
- `DISQUALIFIED`：能够确定候选证明违反至少一项要求；
- `INDETERMINATE`：当前证据不能确定前两者。

资格只回答证明是否可作为指定提交解析的输入，不证明目标迁移客观不存在，也不产生提交结果。

## CM-R4-15 ABORTED 只能引用已登记合格证明

提交解析器只有在以下条件全部成立时才能产生 `ABORTED` 候选：

```text
Candidate Non-application Proof Record exists
+ Registered Proof Qualification Record = QUALIFIED
+ Proof qualification binds same Commit Key
+ Proof qualification binds same Commit Contract Version
+ Proof qualification is applicable As Of resolution time
```

合法证明类型仍只有：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

未找到记录、缓存未命中、异步日志缺失或读取不可用不能构成合格证明。

## CM-R4-16 证明资格不得自证或递归

证明资格只执行冻结契约中的确定性准入规则，不要求另一项“证明资格决策”批准自己。

```text
Qualification Computation != Decision
Qualification Registration != Target Fact Creation
```

资格权威只允许登记规则计算结果，不能创建证据、扩大证明范围或改变目标状态。

## CM-R4-17 ABORTED 不授权重试

```text
Commit Outcome = ABORTED
-/-> Retry Authorized
```

重试只能由独立策略依据决策效力、契约、源版本、预算、冲突行为、证明和历史授权。执行器、解析器、资格器和登记器均不得自行重试。

## CM-R4-18 候选计算与登记必须分别授权

提交结果解析、目标状态解析和证明资格均采用：

```text
Authorized Candidate Computation
  -> Immutable Candidate Record
  -> Content Digest

Independent Registration Authority
  -> Deterministic Admissibility Check
  -> Content-identical Registration Envelope
```

确定性能力不能替代执行授权或登记授权。

## CM-R4-19 登记必须保证内容同一性

```text
Candidate Content Digest
= Registered Content Digest
```

摘要必须采用相同规范化规则版本、覆盖字段、字段存在性语义和算法标识。登记外壳可以增加授权、准入、账本位置和时间元数据，但不能修改候选本体。

候选记录即使未登记、被拒绝或结果不确定，也必须保存在对应未登记账本中。

## CM-R4-20 字段存在性保持三分

```text
VALUE(value)
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
```

三类值必须参与规范化摘要。静默省略规范字段非法；`N/A` 只能作为 `NOT_APPLICABLE` 的显示标签。

## CM-R4-21 读取、状态解析和投影必须分别授权

```text
Target Read Authority
  -> Target Reader
  -> Target Read Attempt Record

Target State Resolution Execution Authority
  -> Target State Resolver
  -> Candidate Target State Resolution Record

Target State Resolution Registration Authority
  -> Registered Target State Resolution Record

Resolution Projection Execution Authority
  -> Projection Builder
  -> Current Resolution Projection
```

读取能力不产生状态解释权威，状态解析执行权威不产生登记权威，登记权威不产生投影执行权威。

## CM-R4-22 读取结果与状态解析保持分离

```text
Target Read Outcome:
  AVAILABLE | UNAVAILABLE

Target State Resolution:
  RESOLVED | INDETERMINATE
```

读取可用不保证状态可解析；读取不可用不删除此前历史状态。无法解析时必须记录直接制度原因，不能在解析记录中写入技术根因诊断。

## CM-R4-23 所有记录必须绑定时点、版本和规则

提交解析、证明资格、状态解析和投影必须分别绑定适用的：

```text
Object or Commit Scope
Attempt or Candidate IDs
Source Record IDs
Evidence References
Observed At
As Of
Produced or Registered At
Applicable Authority References
Contract Version
Resolution or Qualification Rule Version
Canonicalization Rule Version
```

可能没有具体值的字段使用三分存在性结构。

## CM-R4-24 账本位置只表达追加顺序

每项获登记的解析记录必须取得 `Resolution Ledger Position`：

```text
Resolution Ledger Scope ID
Resolution Ledger Position
Registered Resolution Record ID
Registered At
```

账本必须在同一作用域内原子分配唯一位置。位置只表达追加顺序，不表达某记录细化、重申或冲突于另一记录。

候选作用域：

```text
Commit Resolution Scope = Commit Key
Target State Resolution Scope = Target Object ID + State Resolution Subject
```

具体作用域必须由契约版本声明。

## CM-R4-25 语义谱系独立于账本位置

每项登记解析必须保存：

```text
Resolution Lineage ID
Prior Resolution Record References
Resolution Relationship
```

`Resolution Lineage ID` 标识一张相连的语义演化图，不把整张图误写成单一线性分支。`INITIAL` 建立谱系标识；`REFINES` 和 `REAFFIRMS` 保持父记录的谱系标识。并发分支由各自从根记录到终端记录的父引用路径识别，稳定分支端点是对应终端 `Registered Resolution Record ID`。

合法关系：

```text
INITIAL
REFINES
REAFFIRMS
CONFLICTS_WITH
```

- `INITIAL`：没有语义父记录并建立新谱系；
- `REFINES`：引用一个同谱系父记录并增加确定性；
- `REAFFIRMS`：引用一个同谱系父记录并保持相同结论；
- `CONFLICTS_WITH`：显式引用一个或多个不兼容终局记录。

`CONFLICTS_WITH` 可以连接同一谱系内的分支，也可以显式连接同一解析作用域内的不同初始谱系。并发登记可以引用同一个父记录并形成分支，不得覆盖彼此。

## CM-R4-26 确定性细化仍保持三值规则

合法提交结果细化：

```text
INDETERMINATE -> COMMITTED
INDETERMINATE -> ABORTED
INDETERMINATE -> INDETERMINATE
```

`COMMITTED` 与 `ABORTED` 之间不能通过 `REFINES` 或最后记录获胜相互覆盖。终局矛盾只能通过 `CONFLICTS_WITH` 被保留，并进入冲突投影和合法性审查。

## CM-R4-27 投影输入必须证明账本完整性

投影不得仅依靠“最高序号”推断所有分支已经读取。每次投影必须使用以下一种输入证明：

```text
Complete Prefix Proof
  -> all ledger positions <= Watermark are included

Explicit Source Set
  -> exact registered record IDs
  -> stable source set digest
```

无法证明输入集合完整时，投影只能是 `INDETERMINATE`。

## CM-R4-28 投影必须从账本顺序和语义谱系共同计算

```text
Registered Resolution Records
+ Resolution Ledger Positions
+ Resolution Lineage Graph
+ Input Completeness Proof
+ Projection Rule Version
+ Projection As Of
-> Current Resolution Projection
```

账本位置解决遗漏和重复；谱系图解决细化、重申和冲突。二者不得互相替代。

## CM-R4-29 投影值域保持独立

提交解析投影：

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

目标状态解析投影：

```text
RESOLVED | INDETERMINATE | CONFLICTED
```

`CONFLICTED` 只属于投影层，不成为单次解析结果。

## CM-R4-30 投影规则必须声明源规则兼容性

每项 `Projection Rule` 必须声明：

```text
Allowed Source Resolution Rule Versions
Compatibility Relation
Canonical Interpretation Version
Migration or Re-resolution Requirement
Incompatible Source Behavior
Unknown Compatibility Behavior
```

兼容关系必须绑定明确的源规则版本对或版本集合，不能依靠版本号大小推断。

## CM-R4-31 跨规则版本兼容关系必须显式分类

```text
IDENTICAL_SEMANTICS
FORWARD_INTERPRETABLE
REQUIRES_RERESOLUTION
INCOMPATIBLE
UNKNOWN_COMPATIBILITY
```

- `IDENTICAL_SEMANTICS`：可直接共同投影；
- `FORWARD_INTERPRETABLE`：可按指定规范解释版本共同投影；
- `REQUIRES_RERESOLUTION`：必须用新规则从原权威来源产生新候选解析；
- `INCOMPATIBLE`：不得共同投影；
- `UNKNOWN_COMPATIBILITY`：缺少兼容性证据。

## CM-R4-32 重新解析必须追加新历史

`REQUIRES_RERESOLUTION` 只能触发新的受权威约束解析：

```text
Old Registered Resolution Record
+ Original Authoritative Sources
+ New Resolution Execution Authority
+ New Resolution Rule Version
-> New Candidate Resolution Record
-> New Registration
```

旧记录不被翻译、覆盖或改写。新记录必须引用旧记录和原权威来源，并声明谱系关系。

## CM-R4-33 不兼容或未知兼容性必须失败关闭

```text
INCOMPATIBLE
or UNKNOWN_COMPATIBILITY
  -> Projection = INDETERMINATE
  -> Reason = RULE_VERSION_INCOMPATIBLE or RULE_COMPATIBILITY_UNKNOWN
```

规则不兼容本身不等于事实冲突，因此不能自动产生 `CONFLICTED`。只有在同一可比较语义下存在终局矛盾时才产生冲突投影。

## CM-R4-34 当前投影仍是可重建派生读面

投影必须绑定投影类型、值、`As Of`、投影规则版本、兼容性规则版本、来源集合或完整前缀水位、谱系图摘要、生成时点和冲突引用。

投影缓存可删除和重建，不能成为解析历史真源、正式目标事实或最后写入获胜字段。

## CM-R4-35 幂等、并发、对账和补偿不得覆盖历史

同一提交键和声明内容不得形成第二次迁移；同键不同内容非法。`INDETERMINATE` 未解析前不得换键绕过幂等保护。

对账只能产生新候选记录和登记记录。补偿必须通过新决策和新提交，不得删除旧迁移、归因、证明或解析历史。

## CM-R4-36 外部副作用不属于隐式原子边界

通知、发布、文件分发、模型调用或第三方写入若不能与目标权威迁移共享不可分割边界，必须独立建模。

同一数据库、多个本地事务、消息发件箱、流程编排或补偿机制不能单独证明全局原子性。

## 完整路径

### 提交与目标迁移

```text
Decision Fact
  -> Commit Contract Resolution
  -> Commit Execution Authority Resolution
  -> Commit Attempt Initiation Record
  -> Commit-point Preconditions
       -> MET
            -> Protected Authoritative Write
                 -> Target Formal State Transition
                 + Authoritative Transition Record
       -> NOT_MET or uncertain
            -> no target write unless protected boundary proves otherwise
  -> Commit Attempt Completion Record when observable
```

### 未应用证明资格

```text
Proof Assembly Authority
  -> Candidate Non-application Proof Record

Proof Qualification Execution Authority
  -> Candidate Proof Qualification Record

Proof Qualification Registration Authority
  -> Registered Proof Qualification Record
       -> QUALIFIED | DISQUALIFIED | INDETERMINATE
```

### 提交结果解析

```text
Commit Resolution Execution Authority
  -> Commit Resolver
       -> COMMITTED basis: authoritative transition and attribution
       -> ABORTED basis: registered QUALIFIED non-application proof
       -> otherwise: INDETERMINATE
  -> Candidate Commit Resolution Record

Commit Resolution Registration Authority
  -> content identity and admissibility check
  -> Registered Commit Resolution Record
       -> atomic Resolution Ledger Position
       -> explicit Resolution Lineage relationship
```

### 读取、状态解析和投影

```text
Target Read Authority
  -> Target Read Attempt Record

Target State Resolution Execution Authority
  -> Candidate Target State Resolution Record

Target State Resolution Registration Authority
  -> Registered Target State Resolution Record

Resolution Projection Execution Authority
  -> ledger completeness
  + semantic lineage
  + cross-rule compatibility
  -> Current Resolution Projection
```

## 权威操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Committer` | 建立尝试、检查前置条件、履行契约写入、记录完成观察 | 作新裁决、解析结果、自行重试 |
| `Proof Assembler` | 组装并保存候选证明 | 宣布证明合格、产生 `ABORTED` |
| `Proof Qualifier` | 按规则计算候选资格 | 登记自身结论、修改证据 |
| `Proof Qualification Registrar` | 登记内容相同的资格候选 | 改写资格、创建提交结果 |
| `Commit Resolver` | 按规则计算候选提交解析 | 登记自身结果、补写证明 |
| `Commit Resolution Registrar` | 登记内容相同的提交候选 | 修改候选、改变目标事实 |
| `Target Reader` | 读取获准来源、产生读取记录 | 解释状态、扩大读取范围 |
| `Target State Resolver` | 计算候选状态解析 | 登记自身结果、修改目标状态 |
| `Target State Resolution Registrar` | 登记内容相同的状态候选 | 修改候选、继承其他权威 |
| `Projection Builder` | 按兼容规则和完整输入构建投影 | 修改解析历史、创建正式事实 |
| `Policy Selector` | 决定是否授权未来执行 | 修改提交、证明或解析事实 |

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 角色仅凭能力执行而没有适用授权；
- 提交执行权威隐式传播给解析、读取、资格或投影角色；
- 证明组装者自行宣布证明合格；
- 证明资格器登记自身结论；
- 没有已登记 `QUALIFIED` 资格记录就产生 `ABORTED`；
- 资格结果直接创建提交结果或目标事实；
- 登记器修改候选内容；
- 候选记录被删除或静默丢弃；
- 账本位置与语义谱系共用一个字段；
- 并发分支互相覆盖；
- 账本位置在同一作用域重复或非原子分配；
- 投影只用最高序号却没有完整前缀或来源集合证明；
- 用版本号大小猜测语义兼容性；
- 把不兼容规则下的记录直接共同投影；
- 重新解析覆盖旧解析记录；
- 未知规则兼容性被当作通过；
- `ABORTED` 自动授权重试；
- `COMMITTED` 反向创建目标迁移；
- 对账、补偿或投影覆盖历史；
- 外部副作用成功替代目标权威迁移。

## 对第三修订版的映射

| 第三修订版位置 | 第四修订版处理 |
|---|---|
| `CM-R3-04` | 增加全部运行时执行、读取、资格和投影授权类型 |
| `CM-R3-13` | 为未应用证明增加组装、资格计算和资格登记链 |
| `CM-R3-15`、`CM-R3-16` | 分离候选计算执行权威与登记权威 |
| `CM-R3-25` | 拆分解析账本位置和语义谱系 |
| `CM-R3-26` 至 `CM-R3-28` | 增加输入完整性证明和跨规则版本兼容性 |
| 权威操作矩阵 | 为全部运行时角色补齐授权边界 |

## 与决策、证据和策略模型的关系

```text
Decision Fact -> authorizes deterministic target projection
Evidence -> supports observations and proof candidates
Proof Qualification -> determines proof admissibility
Commit Resolution -> classifies one commit attribution
Resolution Projection -> derives current usable knowledge
Policy -> may authorize retry or future execution
```

任何一层都不得代替相邻层。

## 保留的冻结门槛

即使本提案通过模型审查，以下条件闭合前也只能成为宪法候选：

1. `CR-0002-R1 Decision Model` 已正式冻结或被兼容的冻结版本取代；
2. 已建立满足 `IF-0007` 的重复性、稳定性、跨提供者、跨项目、兼容性和迁移证据；
3. 已声明提案者、审查者和冻结权威；
4. 已形成正式冻结决策、唯一冻结标识和版本边界。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Attempt Identity Ordering: PASS
Authority Coverage: PASS_WITH_REVIEW
Proof Qualification Boundary: PASS_WITH_REVIEW
Commit / Target Fact Causality: PASS
Candidate / Registration Identity: PASS
Field Presence Semantics: PASS
Commit Outcome / Target State Separation: PASS
Read Outcome / State Resolution Separation: PASS
Concurrent Resolution Lineage: PASS_WITH_REVIEW
Ledger Completeness Boundary: PASS_WITH_REVIEW
Cross-version Projection Compatibility: PASS_WITH_REVIEW
Retry Authority Separation: PASS
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Model Freeze Review Readiness: REVIEW_REQUIRED
Institution Freeze Eligibility: FAIL
```

建议动作：由 Codex 对本版执行本地独立权威闭合、证明资格非递归、并发谱系确定性和跨版本投影审查。模型审查通过后，可将其提升为 `CONSTITUTION_CANDIDATE`；不得越过仍未满足的冻结门槛。
