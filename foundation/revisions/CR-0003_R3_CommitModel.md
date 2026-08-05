# 提交模型提案第三修订版

## 提案信息

```text
Proposal ID: CR-0003-R3
Title: Commit Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0003-R2
Local Decision Basis: Codex independent assessment
External Material: Historical review input only; no authority
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
Derived From: CR-0003-TYPE-AUDIT
```

> 本文件是待审查修订提案，不是冻结制度。它不能授权运行时提交、改变正式事实、覆盖现行原则或使任何上游提案自动冻结。

## 修订范围

本版保留 `CR-0003-R2` 的因果、权威、否定性证据和时点模型，只做六项冻结前收口：

1. 提交尝试身份必须先于权威写入建立；
2. 字段必须区分具体值、制度上不适用和当前未解析；
3. 候选解析与登记解析必须满足内容摘要同一性；
4. 当前解析投影被定义为版本化派生读面；
5. 候选解析记录进入不可变的未登记解析账本，不得被当作临时数据删除；
6. `ABORTED` 只描述未应用，不自动授权重试。

## 核心定义

> 提交是受制度约束的确定性投影过程。提交尝试身份先于提交点建立；目标迁移及其权威归因在同一受保护边界中成立；候选解析经过内容不变的授权登记后形成派生解析历史；当前解析只由版本化投影规则计算，不覆盖任何历史记录。

```text
Decision Fact
+ Commit Contract
+ Commit Execution Authority
-> Commit Attempt Initiation Record
     -> Commit-point Preconditions
     -> Protected Authoritative Write
          -> Target Formal State Transition
          + Authoritative Transition Record
     -> Commit Attempt Completion Record when observable

Authoritative Sources
+ Attempt Records
+ Evidence
+ Resolution Rule Version
-> Candidate Resolution Record
     -> Content Digest
     -> Registration Envelope
          -> Registered Resolution Record

Registered Resolution Records
+ Resolution Sequence
+ Projection Rule Version
-> Current Resolution Projection
```

## 统一类型边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义提交不变量 | 冻结制度 |
| `Commit Contract` | 值对象 | 定义目标迁移提交语义 | 目标类型治理制度 |
| `Committer` | 执行角色 | 履行提交尝试 | 无事实所有权 |
| `Commit Attempt Initiation Record` | 不可变运行时记录 | 在提交点前建立尝试身份和声明 | 提交尝试账本 |
| `Commit Attempt Completion Record` | 不可变观察记录 | 保存尝试结束时可观察的完成情况 | 提交尝试账本 |
| `Authoritative Transition Record` | 权威迁移归因记录 | 使目标迁移唯一归属于提交键和尝试 | 目标对象注册表 |
| `Commit Resolver` | 执行角色 | 计算候选提交结果 | 无事实所有权 |
| `Candidate Commit Resolution Record` | 不可变候选记录 | 保存尚未登记的提交解析 | 未登记提交解析账本 |
| `Commit Resolution Registrar` | 登记角色 | 为合格候选追加授权外壳 | 无目标事实所有权 |
| `Registered Commit Resolution Record` | 不可变派生记录 | 保存获准登记的提交解析 | 提交解析账本 |
| `Target Read Attempt Record` | 不可变观察记录 | 保存一次目标权威读取结果 | 读取记录账本 |
| `Target State Resolver` | 执行角色 | 计算候选目标状态解析 | 无事实所有权 |
| `Candidate Target State Resolution Record` | 不可变候选记录 | 保存尚未登记的状态解析 | 未登记状态解析账本 |
| `Target State Resolution Registrar` | 登记角色 | 为合格状态候选追加授权外壳 | 无目标事实所有权 |
| `Registered Target State Resolution Record` | 不可变派生记录 | 保存获准登记的状态解析 | 状态解析账本 |
| `Current Commit Resolution Projection` | 派生读面 | 计算指定时点可用的提交认识 | 无独立事实所有权，可重建 |
| `Current Target State Resolution Projection` | 派生读面 | 计算指定时点可用的状态认识 | 无独立事实所有权，可重建 |
| `Non-application Proof Bundle` | 值对象 | 引用支持未应用结论的合格证据 | 依附于候选提交解析 |
| `Commit Audit Record` | 追加式审计记录 | 保存检查、异常和对账过程 | 审计账本 |
| `Transaction` | 技术机制 | 提供实现级原子性和隔离性 | 架构实现层 |

## CM-R3-01 基础模型、运行时和技术实现必须分层

```text
Foundation -> defines invariants
Execution -> performs attempts, reads and resolutions
Architecture -> implements protected boundaries
Target Registry -> owns state and authoritative attribution
```

技术实现不能反向定义制度成功，基础模型也不能绑定具体数据库、消息系统或服务提供者。

## CM-R3-02 提交只有一个目的

提交只负责把已经由适用决策事实授权的声明写集，在确定性契约和受保护权威边界内投影为目标正式状态。

提交不得作出价值判断、选择策略、解释偏差、授予权威、修改制度、扩大迁移类型或扩张写集。

## CM-R3-03 决策事实独立于提交历史

```text
Decision Fact -> may authorize Commit
Commit Outcome -/-> Decision Fact Mutation
```

提交成功、中止或不确定都不能覆盖输入决策事实。决策的未来效力只能通过新的合法历史改变。

## CM-R3-04 提交必须引用完整版本化契约

`Commit Contract` 至少声明：

```text
Target Object Type
Allowed Transition Type
Required Decision Fact Types
Composite Decision Requirements
Expected Source State and Version
Transition Preconditions
Declared Write Set
Atomicity Boundary
Attribution Record Requirements
Commit Execution Authority Type
Commit Resolution Registration Authority Type
Target State Resolution Registration Authority Type
Resolution Rule
Projection Rule
Field Presence Rules
Content Canonicalization Rule
Non-application Proof Rules
Conflict Behavior
Evidence Requirements
```

未声明的写入、解析、投影或证明路径不得临时补推。

## CM-R3-05 提交尝试身份必须先于提交点建立

进入提交点前必须先追加 `Commit Attempt Initiation Record`，建立稳定的：

```text
Commit Attempt ID
Commit Key
Decision Fact References
Commit Contract Version
Commit Execution Authority Reference
Target Object ID
Expected Source Version
Declared Write Set Digest
Opened At
```

只有初始化记录成功进入提交尝试账本后，才允许检查提交点前置条件和进入受保护写入。

```text
No Initiation Record
  -> No Commit-point Entry
  -> No Protected Authoritative Write
```

预先分配但未登记的标识不能作为权威迁移归因。

## CM-R3-06 权威迁移只能引用既有尝试身份

`Authoritative Transition Record` 引用的 `Commit Attempt ID` 必须已经存在于不可变初始化记录中，且其提交键、目标对象、契约版本和写集摘要完全一致。

```text
Authoritative Transition Record
-/-> Unregistered Attempt ID
```

目标迁移与权威迁移记录仍必须在同一不可分割权威边界内成立。

## CM-R3-07 尝试完成记录不是结果真源

提交过程结束、超时或失去响应时，可以追加 `Commit Attempt Completion Record`，保存：

```text
Commit Attempt ID
Observed Completion State
Observed At
Execution Evidence References
```

该记录只描述提交器当时观察到什么，不证明迁移已经提交或中止。系统在完成记录产生前崩溃时，初始化记录和权威迁移记录仍足以支持后续对账。

## CM-R3-08 提交不创建新的价值裁决

```text
Commit Contract Evaluation = Deterministic Rule Evaluation
Commit Contract Evaluation != Decision
```

出现新的价值选择、规则冲突、范围扩张或主观裁量时，必须中止并请求新决策。

## CM-R3-09 提交执行权威只允许履行投影

每次尝试只有一个主要提交执行授权。它必须覆盖提交者、目标、版本、迁移类型、声明写集、目标注册表、时间和作用域。

提交执行权威不得隐式传播为提交解析登记权威或目标状态解析登记权威。

## CM-R3-10 前置检查、写入和权威归因共享保护边界

```text
Check Commit-point Preconditions
+ Apply Declared Write Set
+ Create Authoritative Transition Record
= One Protected Boundary
```

检查与写入之间不得存在未受保护竞态。权威迁移记录至少绑定提交键、尝试标识、决策事实、契约版本、前后权威版本、写集摘要、提交时点和原子边界标识。

## CM-R3-11 COMMITTED 只确认既有迁移归因

```text
Target Formal State Transition
+ Authoritative Transition Record
+ Sufficient Attribution Evidence
-> Candidate Commit Outcome = COMMITTED
```

禁止：

```text
COMMITTED -> create Target Transition
```

解析服务或登记服务迟到不能否定目标权威边界已经建立的迁移。

## CM-R3-12 提交结果保持三值

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：声明写集完整形成迁移，并唯一归属于指定提交键；
- `ABORTED`：合格未应用证明确认指定提交键没有形成声明迁移；
- `INDETERMINATE`：当前证据不能证明前两种结果。

单次解析结果不得增加 `CONFLICTED` 第四值。

## CM-R3-13 ABORTED 必须拥有合格未应用证明

```text
Record Not Found -/-> ABORTED
```

合法证明类型只有：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

证明必须满足提交契约中的权威来源、版本范围、查询完整性、证据时点和资格要求。证明不足时结果保持 `INDETERMINATE`。

## CM-R3-14 ABORTED 不授权重试

```text
Commit Outcome = ABORTED
-/-> Retry Authorized
```

`ABORTED` 只说明本次提交没有形成声明迁移。是否允许重试必须由独立策略依据以下内容决定：

```text
Decision Fact Validity
Commit Contract
Current Source Version
Applicable Policy
Budget
Conflict Behavior
Prior Attempt History
```

提交器、解析器和登记器都不得自行重试。

## CM-R3-15 确定性计算不自动获得登记权威

`Commit Resolver` 和 `Target State Resolver` 只能读取允许的权威来源、按指定规则计算候选结果并产生候选记录。

```text
Deterministic Computation
-/-> Registration Authority
```

解析器不得登记自身结果、创建目标事实、补写证明或修改上游记录。

## CM-R3-16 两类解析登记权威不得隐式继承

```text
Commit Resolution Registration Authority
!= Target State Resolution Registration Authority
```

每项登记授权必须限定登记者、契约类型、目标类型、来源、结果枚举、提交键或目标范围、规则版本和有效期。

同一主体可以持有两项独立授权，但必须使用不同任务契约和登记身份。

## CM-R3-17 候选解析记录必须持久且不可变

候选解析记录进入对应的未登记解析账本，不属于可随意删除的临时数据。

候选记录至少保存：

```text
Candidate Resolution Record ID
Resolution Body
Source Record IDs
Evidence References
As Of
Resolution Rule Version
Canonicalization Rule Version
Candidate Content Digest
Produced At
Producer Identity
```

候选记录即使最终 `INADMISSIBLE` 或 `INDETERMINATE`，仍必须按审计保留规则保存。

## CM-R3-18 登记只能增加授权外壳

登记不是重新构造解析内容：

```text
Registration
= Append Authorization Envelope around Immutable Candidate
!= Reconstruct Resolution Content
```

登记记录至少保存：

```text
Candidate Resolution Record ID
Candidate Content Digest
Registered Content Digest
Registration Authority Reference
Admissibility Check Record
Registration Rule Version
Registration Sequence
Registered At
```

必须满足：

```text
Candidate Content Digest
= Registered Content Digest
```

`Registered Content Digest` 只重新计算被引用候选解析本体的规范化内容，不包含登记授权、时间、序号和准入元数据。登记外壳可以增加这些元数据，但不得复制后改写解析本体。

## CM-R3-19 内容摘要必须基于版本化规范化规则

内容摘要只有在以下条件同时满足时才能比较：

```text
Same Canonicalization Rule Version
Same Covered Field Set
Same Field Presence Semantics
Same Digest Algorithm Identifier
```

摘要算法、规范化规则或覆盖字段不同不得被解释为内容不一致，必须先进行规则兼容性处理。

提交结果解析和目标状态解析必须采用同构的摘要同一性约束。

## CM-R3-20 字段存在性必须三分

所有可能缺失的规范字段必须显式采用：

```text
VALUE(value)
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
```

- `VALUE`：已经解析出具体值；
- `NOT_APPLICABLE`：该字段在当前记录类型或结果类型中制度上不适用；
- `UNRESOLVED`：字段适用，但当前证据不足以确定。

`N/A` 只能作为 `NOT_APPLICABLE` 的显示标签，不能作为含义不明的存储值。`UNKNOWN` 不得替代 `UNRESOLVED`。

## CM-R3-21 字段存在性必须参与摘要

以下值不得产生相同规范化内容：

```text
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
VALUE(null)
field omitted
```

静默省略规范字段属于非法记录。候选摘要、登记摘要和后续审计必须保留相同的存在性语义。

## CM-R3-22 读取结果与状态解析继续分离

```text
Target Read Outcome
  -> AVAILABLE | UNAVAILABLE

Target State Resolution
  -> RESOLVED | INDETERMINATE
```

读取可用不保证状态可解析；读取不可用也不删除此前历史状态。

当状态为 `INDETERMINATE` 时必须记录直接制度原因，例如来源不可用、权威记录冲突、证据不足、时点未定义、版本不存在或归因不完整。原因不是技术根因诊断。

## CM-R3-23 所有解析必须绑定时点、版本和规则

提交结果解析至少绑定：

```text
Commit Key
Commit Attempt ID
Authoritative Transition Record Reference
Non-application Proof Bundle Reference
Prior Authoritative Version
New Authoritative Version
Resolved At
As Of
Resolution Rule Version
Source Record IDs
Evidence References
```

目标状态解析至少绑定：

```text
Target Object ID
Resolved Authoritative Version
Observed At
As Of
Target Read Attempt Record Reference
Source Record IDs
Resolution Rule Version
Evidence References
```

每个可能没有具体值的字段必须使用 `CM-R3-20` 的三分存在性结构。

## CM-R3-24 跨时点比较必须声明时间关系

历史提交结果和目标状态解析只有在明确各自 `As Of`、观察时间、权威版本和来源记录后才能比较。

```text
Commit K1 = COMMITTED at Version 12, As Of T1
Target State = RESOLVED at Version 14, As Of T2
```

表示版本 12 的提交历史成立，目标后来演化到版本 14，不构成冲突。无时点的“当前状态”不得进入正式推导。

## CM-R3-25 解析历史必须形成显式序列

每项登记解析必须保存：

```text
Prior Resolution Record Reference
Resolution Sequence
Resolution Relationship
```

合法确定性细化只有：

```text
INDETERMINATE -> COMMITTED
INDETERMINATE -> ABORTED
INDETERMINATE -> INDETERMINATE
```

`COMMITTED` 与 `ABORTED` 不得通过后到记录相互覆盖。矛盾终局解析必须保留并进入投影冲突状态和独立合法性审查。

## CM-R3-26 当前解析投影是派生读面

```text
Registered Resolution Records
+ Valid Resolution Sequence
+ Resolution Relationships
+ Projection Rule Version
+ Projection As Of
-> Current Resolution Projection
```

投影不是新的正式事实、不是某条解析记录、不是最后一条记录，也不拥有修改历史的权威。它必须能够从登记解析账本重建。

投影只能纳入 `Registered At <= Projection As Of` 且满足适用版本关系的登记记录。最低确定性规则为：

```text
No admissible source records -> INDETERMINATE
Only unresolved lineage -> INDETERMINATE
Incomplete sequence -> INDETERMINATE
One non-conflicting terminal lineage -> terminal value
Conflicting terminal lineages -> CONFLICTED
Contradictory or illegal relationship -> CONFLICTED
```

## CM-R3-27 两类当前解析投影拥有独立值域

提交当前解析投影具有四值：

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

`CONFLICTED` 只属于投影层，表示同一适用边界内存在无法由合法细化关系消解的终局解析冲突。它不会成为单次提交结果的第四值。

```text
Projection = CONFLICTED
  -> FAIL_CLOSED
  -> Legality and Evidence Review Required
```

目标状态当前解析投影具有：

```text
RESOLVED
INDETERMINATE
CONFLICTED
```

两类投影不得共享或互换值域。目标状态投影的 `CONFLICTED` 只表示适用权威状态记录无法形成唯一状态认识，不表示提交结果冲突。

## CM-R3-28 投影必须绑定来源和版本

每项投影至少保存或输出：

```text
Projection Type
Projection Value
Projection As Of
Projection Rule Version
Source Resolution Record IDs
Highest Included Resolution Sequence
Generated At
Conflict References when applicable
```

投影缓存可以删除或重建，但不能成为解析历史真源，也不能反向修改来源记录。

## CM-R3-29 幂等、并发、重试和补偿必须保持历史

同一提交键和声明内容不得形成第二次迁移；同键不同内容属于非法冲突。源版本冲突不得通过最后写入获胜覆盖权威新状态。

`INDETERMINATE` 未解析前不得用新键绕过幂等保护。补偿必须通过新的适用决策和新提交形成，不能删除原迁移、归因或解析历史。

## CM-R3-30 外部副作用不属于隐式原子边界

无法与目标权威迁移共享不可分割边界的通知、发布、文件分发、模型调用或第三方写入，必须作为独立执行、观察和确认建模。

同一数据库、多个本地事务、消息发件箱、补偿流程或流程编排均不能单独证明全局原子性。

## 完整路径

```text
Decision Fact
  -> Commit Request
  -> Commit Contract Resolution
  -> Commit Execution Authority Resolution
  -> Commit Key Resolution
  -> Commit Attempt Initiation Record
       -> initiation registration failed
            -> No Commit Attempt
            -> No Protected Write

       -> initiation registered
            -> Commit-point Preconditions Evaluation

                 -> NOT_MET with qualified PRE_WRITE_EXCLUSION_PROOF
                      -> Commit Attempt Completion Record when observable
                      -> Candidate Commit Resolution: ABORTED

                 -> NOT_MET without qualified proof
                      -> Commit Attempt Completion Record when observable
                      -> Candidate Commit Resolution: INDETERMINATE

                 -> MET
                      -> Protected Authoritative Write
                           -> Target Formal State Transition
                           + Authoritative Transition Record
                      -> Commit Attempt Completion Record when observable
                      -> Candidate Commit Resolution
                           -> attributable and complete: COMMITTED
                           -> qualified non-application proof: ABORTED
                           -> otherwise: INDETERMINATE

Candidate Commit Resolution Record
  -> persistent unregistered resolution ledger
  -> deterministic registration admissibility check
       -> ADMISSIBLE
            -> verify content digest identity
            -> append registration envelope
            -> Registered Commit Resolution Record
       -> INADMISSIBLE | INDETERMINATE
            -> no registered resolution
            -> preserve candidate and audit evidence

Registered Commit Resolution Records
  -> Current Commit Resolution Projection
       -> COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

目标状态解析采用同构路径：

```text
Target Read Attempt Record
  -> Candidate Target State Resolution Record
  -> persistent unregistered state resolution ledger
  -> content-identical authorized registration
  -> Registered Target State Resolution Record
  -> Current Target State Resolution Projection
```

## 权威操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Committer` | 建立尝试初始化、检查前置条件、尝试契约写入、追加完成观察 | 作新裁决、登记解析、自行重试 |
| `Commit Resolver` | 读取合格来源、计算并保存候选提交解析 | 登记自身结果、创建目标事实、补写证明 |
| `Commit Resolution Registrar` | 校验摘要同一性并增加授权外壳 | 修改候选本体、降低证据标准 |
| `Target Reader` | 读取目标权威来源、产生读取记录 | 把访问失败解释成状态不存在 |
| `Target State Resolver` | 计算并保存候选状态解析 | 登记自身结果、修改目标状态 |
| `Target State Resolution Registrar` | 校验摘要同一性并增加授权外壳 | 修改候选本体、继承提交解析权威 |
| `Projection Builder` | 按版本化规则重建当前解析投影 | 创建正式事实、覆盖解析历史 |
| `Reconciler` | 追加候选解析和审计记录 | 修改旧记录、制造缺失归因、绕过登记权威 |
| `Policy Selector` | 依据结果和上下文决定是否授权重试 | 修改提交结果、证据或历史 |

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 权威迁移记录引用未登记的尝试标识；
- 在尝试初始化记录成立前进入提交点；
- 用尝试完成观察证明提交结果；
- 静默省略适用字段；
- 把 `NOT_APPLICABLE` 与 `UNRESOLVED` 混为同一个空值；
- 候选记录被当作临时数据删除；
- 候选摘要与登记摘要不同仍完成登记；
- 登记器重新构造或修改解析本体；
- 未声明规范化规则版本就比较内容摘要；
- 确定性解析器自动获得登记权威；
- 把读取不可用与状态不可解析写入同一枚举；
- 使用无时点、版本或规则版本的“当前状态”；
- 以最后记录获胜处理解析冲突；
- 把 `CONFLICTED` 加入单次提交结果枚举；
- 把当前投影当作正式事实或历史真源；
- 用未找到记录证明 `ABORTED`；
- 把 `ABORTED` 自动解释为允许重试；
- `COMMITTED` 反向创建目标迁移；
- 权威迁移记录与目标迁移不共享原子边界；
- 同键建立多个迁移或绑定不同声明内容；
- 对账、重试或补偿覆盖旧历史；
- 外部副作用成功替代目标权威迁移。

## 对第二修订版的映射

| 第二修订版位置 | 第三修订版处理 |
|---|---|
| 统一类型边界 | 拆分尝试初始化与完成记录；候选边界改为持久未登记账本 |
| `CM-R2-08` | 强制权威迁移引用预先登记的尝试身份 |
| `CM-R2-13` | 增加候选与登记内容摘要同一性契约 |
| `CM-R2-17` | 用 `VALUE / NOT_APPLICABLE / UNRESOLVED` 取代含义模糊的空值 |
| `CM-R2-26` | 正式定义版本化当前解析投影和 `CONFLICTED` 投影值 |
| 重试边界 | 明确 `ABORTED` 不产生重试授权 |
| 完整路径 | 把尝试初始化移动到所有提交点行为之前 |

## 与决策和策略模型的关系

```text
Decision Fact -> authorizes deterministic projection
Commit Resolution -> classifies one attempt attribution
Resolution Projection -> derives current usable knowledge
Policy -> may authorize retry or future execution
```

解析和投影都不能创建第二次价值裁决；`ABORTED`、`INDETERMINATE` 和 `CONFLICTED` 也不能自行选择未来行动。

## 仍待后续模型定义的问题

本提案不越权解决：

1. 具体存储如何实现尝试账本与目标权威边界；
2. 不同技术系统如何产生合格原子中止证明；
3. 各领域目标注册表如何提供封闭查询保证；
4. 通用状态解析和投影是否需要独立现实层模型；
5. 跨注册表组合流程与依赖失效传播算法；
6. 决策模型的正式冻结。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Attempt Identity Ordering: PASS
Decision / Commit Separation: PASS
Commit / Target Fact Causality: PASS
Candidate / Registration Identity: PASS_WITH_REVIEW
Field Presence Semantics: PASS_WITH_REVIEW
Commit Outcome / Target State Separation: PASS
Read Outcome / State Resolution Separation: PASS
Resolution Authority: PASS_WITH_REVIEW
Temporal and Version Binding: PASS_WITH_REVIEW
ABORTED Proof Boundary: PASS_WITH_REVIEW
Retry Authority Separation: PASS
Current Projection Boundary: PASS_WITH_REVIEW
Atomic Attribution: PASS_WITH_REVIEW
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Freeze Readiness: REVIEW_REQUIRED
```

建议动作：由 Codex 依据本地冻结制度执行独立对象图、摘要同一性、投影确定性、权威递归和历史一致性审查。未经该审查，不进入冻结准备度判断。
