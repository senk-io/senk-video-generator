# 提交模型提案第二修订版

## 提案信息

```text
Proposal ID: CR-0003-R2
Title: Commit Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0003-R1
Review Basis: CR-0003-R1-LOCAL-REVIEW
Reviewer: Codex
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
Derived From: CR-0003-TYPE-AUDIT
```

> 本文件是待审查修订提案，不是冻结制度。它不能授权运行时提交、改变正式事实、覆盖现行原则或使任何上游提案自动冻结。

## 修订范围

本版保留 `CR-0003-R1` 已经成立的因果、原子归因和记录分离，只解决本地独立审查确认的四项阻断：

1. 为提交结果解析增加独立角色、候选记录和登记权威；
2. 分离目标读取结果与目标状态解析；
3. 强制所有解析绑定时点、版本和规则版本；
4. 为 `ABORTED` 建立完备的未应用证明契约。

## 核心定义

> 提交是受制度约束的确定性投影过程。目标迁移及其权威归因在同一受保护边界中成立；提交结果是由获授权解析者依据版本化权威记录和证据计算、再由独立登记权威追加保存的派生解析记录。

```text
Decision Fact
+ Commit Contract
+ Commit Execution Authority
+ Commit-point Preconditions
-> Commit Attempt
     -> Protected Authoritative Write
          -> Target Formal State Transition
          + Authoritative Transition Record

Authoritative Transition Record
+ Commit Attempt Record
+ Attribution Evidence
+ Resolution Rule Version
-> Commit Resolver
     -> Candidate Commit Resolution Record

Candidate Commit Resolution Record
+ Commit Resolution Registration Authority
+ Deterministic Admissibility Check
-> Registered Commit Resolution Record
```

`Registered Commit Resolution Record` 是对既有权威事实的可重建派生记录，不是新的目标正式事实，也不创建第二次裁决。

## 统一类型边界

| 节点 | 类型 | 唯一目的 | 逻辑所有者或边界 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义提交不变量 | 冻结制度 |
| `Commit Contract` | 值对象 | 定义目标迁移提交语义 | 目标类型治理制度 |
| `Committer` | 执行角色 | 履行提交尝试 | 无事实所有权 |
| `Commit Attempt Record` | 不可变运行时记录 | 保存尝试输入和当时观察 | 提交账本 |
| `Authoritative Transition Record` | 权威迁移归因记录 | 使目标迁移唯一归属于提交键 | 目标对象注册表 |
| `Commit Resolver` | 执行角色 | 计算候选提交结果 | 无事实所有权 |
| `Candidate Commit Resolution Record` | 候选记录 | 保存尚未登记的解析输出 | 临时解析边界 |
| `Commit Resolution Registrar` | 登记角色 | 在授权范围内登记合格解析记录 | 无目标事实所有权 |
| `Registered Commit Resolution Record` | 不可变派生记录 | 保存获准登记的确定性解析结果 | 提交解析账本 |
| `Commit Audit Record` | 追加式审计记录 | 保存检查、错误和对账过程 | 审计账本 |
| `Target Read Attempt Record` | 观察记录 | 保存一次目标权威读取结果 | 读取记录账本 |
| `Target State Resolver` | 执行角色 | 计算候选目标状态解析 | 无事实所有权 |
| `Candidate Target State Resolution Record` | 候选记录 | 保存尚未登记的状态解析输出 | 临时解析边界 |
| `Target State Resolution Registrar` | 登记角色 | 在授权范围内登记合格状态解析 | 无目标事实所有权 |
| `Registered Target State Resolution Record` | 不可变派生记录 | 保存指定时点的获准状态解析 | 状态解析账本 |
| `Non-application Proof Bundle` | 值对象 | 引用并限定支持未应用结论的合格证据 | 依附于候选提交解析记录 |
| `Transaction` | 技术机制 | 提供实现级原子性和隔离性 | 架构实现层 |

## CM-R2-01 模型、运行时和实现必须分层

```text
Foundation -> defines Commit invariants
Execution -> performs attempts, reads and resolutions
Architecture -> implements protected boundaries
Target Registry -> owns state and authoritative attribution
```

基础模型不能指定数据库、锁或消息产品；技术实现不能反向定义制度成功。

## CM-R2-02 提交只有一个目的

提交只负责把已经由适用决策事实授权的声明写集，在确定性契约和受保护权威边界内投影为目标正式状态。

提交不得作出价值判断、选择策略、解释偏差、授予权威、修改制度、扩大迁移类型或扩张写集。

## CM-R2-03 决策事实与目标事实相互独立

`Decision Fact` 是治理型正式事实；目标迁移是领域型或治理型正式事实。

```text
Decision Fact -> may authorize Commit
Commit Outcome -/-> Decision Fact Mutation
```

提交失败、不确定或成功都不能覆盖输入决策历史。

## CM-R2-04 提交必须引用版本化契约

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
Non-application Proof Rules
Conflict Behavior
Evidence Requirements
```

任何未在契约中声明的写入、解析或证明路径都不得临时补推。

## CM-R2-05 提交不创建新的价值裁决

```text
Commit Contract Evaluation = Deterministic Rule Evaluation
Commit Contract Evaluation != Decision
```

出现多个合法选择、规则冲突、范围扩张或主观裁量时，提交必须中止并请求新的决策。

## CM-R2-06 提交执行权威只允许履行投影

每次 `Commit Attempt` 必须引用一个适用的主要提交执行授权，覆盖提交者、目标对象、目标版本、迁移类型、写集、目标注册表、时间和作用域。

提交执行权威不得登记提交解析结果，除非同一主体另有独立的解析登记授权和独立任务契约。

## CM-R2-07 前置检查与写入共享受保护边界

提交点必须在保护目标写集的同一边界内重新检查决策效力、组合要求、源状态、源版本、依赖、证据资格、写集和目标不变量。

```text
Check Preconditions
+ Apply Declared Write Set
+ Create Authoritative Transition Record
= One Protected Boundary
```

检查与写入之间不得存在未受保护的竞态窗口。

## CM-R2-08 目标迁移和权威归因必须原子耦合

```text
Protected Authoritative Write
  -> Target Formal State Transition
  + Authoritative Transition Record
```

`Authoritative Transition Record` 至少保存：

```text
Commit Key
Commit Attempt ID
Decision Fact References
Commit Contract Version
Prior Authoritative Version
New Authoritative Version
Applied Write Set Digest
Committed At
Atomic Boundary Identifier
```

该记录必须内嵌于目标权威状态，或与目标迁移共享可证明的不可分割提交边界。

## CM-R2-09 COMMITTED 只确认归因

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

提交解析记录迟到不能否定已经由目标权威边界建立的迁移。

## CM-R2-10 提交结果保持三值

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：能够证明声明写集完整形成目标迁移，并唯一归属于指定提交键；
- `ABORTED`：能够通过合格未应用证明确认指定提交键没有形成声明迁移；
- `INDETERMINATE`：现有权威记录和证据不能证明前两种情况。

`INDETERMINATE` 不等于失败，也不自动表示目标当前状态未知。

## CM-R2-11 确定性解析不自动获得权威

`Commit Resolver` 只能：

- 读取契约允许的权威记录和证据；
- 按指定规则版本计算候选结果；
- 产生 `Candidate Commit Resolution Record`。

它不得：

- 创建或修改目标迁移；
- 创建或补写权威迁移记录；
- 修改尝试记录和证据；
- 自行把候选结果登记为正式解析记录；
- 在证据不足时补推 `COMMITTED` 或 `ABORTED`。

```text
Deterministic Computation
-/-> Registration Authority
```

## CM-R2-12 解析登记必须拥有独立权威

每项 `Registered Commit Resolution Record` 必须引用一个主要 `Commit Resolution Registration Authority`，其授权至少限定：

```text
Resolver or Registrar Identity
Allowed Commit Contract Types
Allowed Target Object Types
Allowed Evidence Sources
Allowed Outcome Values
Commit Key Scope
Target Version Scope
Resolution Rule Versions
Validity Window
```

解析登记权威只允许登记合格的确定性候选记录，不允许改变候选内容、目标事实或上游证据。

目标状态解析采用相同但不隐式共享的权威边界：

```text
Target State Resolver
  -> Candidate Target State Resolution Record

Candidate Target State Resolution Record
+ Target State Resolution Registration Authority
+ Deterministic Admissibility Check
  -> Registered Target State Resolution Record
```

提交结果解析登记权威不得自动继承为目标状态解析登记权威，反之亦然。

## CM-R2-13 解析登记准入是确定性检查

```text
Candidate Commit Resolution Record
+ Applicable Registration Authority
+ Required Source Records
+ Required Evidence
+ Resolution Rule Version
-> Resolution Registration Admissibility Check
     -> ADMISSIBLE
     -> INADMISSIBLE
     -> INDETERMINATE
```

准入检查不是决策。只有 `ADMISSIBLE` 才能追加 `Registered Commit Resolution Record`；其余结果必须失败关闭。

已登记解析记录是对权威输入的可重建派生记录，不得取代目标权威状态或权威迁移记录。

目标状态候选解析必须通过同构的确定性准入检查后才能登记；两类准入检查共享结构，但分别引用自己的授权类型、规则版本和记录所有者。

## CM-R2-14 提交结果解析与目标状态解析分离

`Commit Outcome Resolution` 回答本次提交键是否形成并拥有声明迁移。

`Target State Resolution` 回答指定目标在指定 `As Of` 时点能否建立唯一权威状态。

```text
Commit Outcome Resolution
!= Target State Resolution
```

任何一方都不得机械推导另一方。

## CM-R2-15 目标读取与状态解析必须分离

目标读取结果只描述访问事实：

```text
Target Read Outcome
  -> AVAILABLE
  -> UNAVAILABLE
```

目标状态解析只描述认识结论：

```text
Target State Resolution
  -> RESOLVED
  -> INDETERMINATE
```

`AVAILABLE` 不保证状态可解析；`UNAVAILABLE` 也不删除此前已经形成的历史状态事实。

## CM-R2-16 状态解析必须保存原因

当目标状态解析为 `INDETERMINATE` 时，必须至少记录一个原因：

```text
SOURCE_UNAVAILABLE
CONFLICTING_AUTHORITATIVE_RECORDS
INSUFFICIENT_EVIDENCE
UNDEFINED_AS_OF
VERSION_NOT_FOUND
INCOMPLETE_ATTRIBUTION
```

原因是解析值，不是诊断；它只描述无法建立唯一状态的直接制度条件，不解释技术根因。

## CM-R2-17 所有解析必须绑定时点和版本

每项提交结果解析必须绑定：

```text
Commit Key
Commit Attempt ID
Authoritative Transition Record ID or Non-application Proof Bundle Digest
Prior Authoritative Version
New Authoritative Version or N/A
Resolved At
As Of
Resolution Rule Version
Source Record IDs
Evidence References
```

每项目标状态解析必须绑定：

```text
Target Object ID
Resolved Authoritative Version or N/A
Observed At
As Of
Target Read Attempt Record ID
Source Record IDs
Resolution Rule Version
Evidence References
```

不适用值必须显式标记，不能静默省略。

## CM-R2-18 跨时点比较必须声明时间关系

```text
Commit K1 = COMMITTED at Version 12, As Of T1
Target State = RESOLVED at Version 14, As Of T2
```

这表示版本 12 的提交历史成立，同时目标后来演化到版本 14，不构成冲突。

禁止比较：

```text
COMMITTED + Current State
```

除非“当前”被展开为明确的 `As Of`、观察时间、权威版本和来源记录。

## CM-R2-19 ABORTED 必须引用合格未应用证明

```text
Record Not Found
-/-> ABORTED
```

`ABORTED` 只能由 `Non-application Proof Bundle` 支持，其中必须包含以下证明类型之一：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

该值对象必须引用不可变证据和权威来源，但不得拥有或修改这些来源。未应用证明必须由提交契约预先允许，并满足对应资格规则。

## CM-R2-20 前置排除证明

`PRE_WRITE_EXCLUSION_PROOF` 只在以下条件成立：

- 前置条件被确定性判定为 `NOT_MET`；
- 受保护写入入口尚未进入；
- 执行边界能够证明没有产生目标写入；
- 证明绑定提交键、尝试标识、规则版本、检查结果和发生时点。

客户端提前报错或调用未返回不能单独构成该证明。

## CM-R2-21 原子中止证明

`ATOMIC_ABORT_PROOF` 只在受保护权威边界能够证明：

- 写入事务已经明确中止；
- 声明写集和权威迁移记录均未成立；
- 中止证明来自目标权威边界或其可验证事务机制；
- 证明绑定事务边界标识、提交键、目标版本和时点。

仅有提交器返回失败不能构成原子中止证明。

## CM-R2-22 权威未应用证明

`AUTHORITATIVE_NON_APPLICATION_PROOF` 必须证明目标权威来源在一个完备且封闭的范围内没有应用指定提交键，包括：

```text
Commit Key
Target Object ID
Authoritative Source
Closed Version Range or Closed Attempt Boundary
Query Completeness Guarantee
Observed At
As Of
Authority or Qualification Record
Evidence References
```

索引缺失、缓存未命中、异步日志没有记录或数据源不可访问均不构成权威未应用证明。

## CM-R2-23 未应用证明不足时保持 INDETERMINATE

```text
No Qualified Non-application Proof
  -> Commit Outcome = INDETERMINATE
```

系统不得为了允许重试而降低 `ABORTED` 证明标准。只有证明本次提交没有形成迁移，才能安全进入允许重新执行的策略判断。

## CM-R2-24 提交键必须稳定且幂等

`Commit Key` 至少绑定决策事实、目标对象、预期源版本、请求迁移类型、声明写集摘要和契约版本。

同键同内容不得建立第二次迁移；同键不同内容属于非法冲突。已存在权威迁移记录时必须解析既有结果，不得再次执行。

## CM-R2-25 并发冲突不得静默覆盖

源版本冲突只有在形成合格前置排除证明或原子中止证明时才能解析为 `ABORTED`。否则必须保持 `INDETERMINATE`。

不得采用最后写入获胜覆盖未被本次决策授权的新状态。

## CM-R2-26 记录只能追加，不能原地修正

```text
Commit Attempt Record
Authoritative Transition Record
Candidate Commit Resolution Record
Registered Commit Resolution Record
Target Read Attempt Record
Candidate Target State Resolution Record
Registered Target State Resolution Record
Commit Audit Record
```

全部必须不可变或通过追加更正处理。后续对账产生新的解析记录，不得把旧 `INDETERMINATE` 改写成 `COMMITTED` 或 `ABORTED`。

解析记录必须形成显式序列：

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

`COMMITTED` 与 `ABORTED` 之间不得依靠“最后记录获胜”相互覆盖。出现矛盾解析时，必须保留全部记录、将当前解析投影失败关闭，并进入独立合法性与证据审查。

## CM-R2-27 重试和补偿必须保留历史

`INDETERMINATE` 未解析前不得用新提交键绕过幂等保护。

已提交迁移需要恢复时，必须通过新的适用决策和新提交形成补偿迁移。补偿不能删除原迁移、权威归因或解析历史。

## CM-R2-28 外部副作用不属于隐式原子边界

无法与目标权威迁移共享同一不可分割边界的通知、发布、文件分发、模型调用或第三方写入，必须作为独立执行、观察和确认建模。

同一数据库、多个本地事务、消息发件箱、补偿流程或流程编排均不能单独证明全局原子性。

## CM-R2-29 提交器、解析器和登记器都不能自证

- 提交器不能凭返回值证明迁移成功或中止；
- 解析器不能凭算法确定性获得登记权威；
- 登记器不能修改候选解析内容；
- 对账器不能创建缺失的权威迁移记录或未应用证明；
- 技术管理员不能因存储权限获得制度裁决权。

所有记录必须能够从适用权威、版本化规则、不可变来源和证据重新审计。

## 修订后的完整路径

```text
Decision Fact
  -> Commit Request
  -> Commit Contract Resolution
  -> Commit Execution Authority Resolution
  -> Commit Key Resolution
  -> Commit-point Preconditions Evaluation

       -> NOT_MET with qualified PRE_WRITE_EXCLUSION_PROOF
            -> Commit Attempt Record
            -> Commit Resolver
            -> Candidate Resolution: ABORTED
            -> Resolution Registration

       -> NOT_MET without qualified proof
            -> Commit Attempt Record
            -> Candidate Resolution: INDETERMINATE
            -> Resolution Registration
            -> Reconciliation Required

       -> MET
            -> Protected Authoritative Write
                 -> Target Formal State Transition
                 + Authoritative Transition Record
            -> Commit Attempt Record
            -> Commit Resolver
                 -> attributable and complete
                      -> Candidate Resolution: COMMITTED
                 -> qualified non-application proof
                      -> Candidate Resolution: ABORTED
                 -> otherwise
                      -> Candidate Resolution: INDETERMINATE
            -> Resolution Registration
            -> if INDETERMINATE: Reconciliation Required
```

目标状态读取和解析是独立支线：

```text
Target Read Attempt
  -> Target Read Attempt Record: AVAILABLE | UNAVAILABLE
  -> Target State Resolver
       -> Candidate State Resolution: RESOLVED | INDETERMINATE
       -> Target State Resolution Registration
       -> Versioned Registered Target State Resolution Record
```

## 权威操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Committer` | 检查前置条件、尝试契约写入、产生尝试记录 | 作新裁决、登记解析、修改目标契约 |
| `Commit Resolver` | 读取合格来源、按规则计算候选结果 | 登记自身结果、创建目标事实、补写证明 |
| `Commit Resolution Registrar` | 在授权范围内登记合格候选解析 | 改写候选结果、改变目标事实、降低证据标准 |
| `Target Reader` | 读取目标权威来源、产生读取记录 | 把访问失败解释为状态不存在 |
| `Target State Resolver` | 计算指定 `As Of` 的候选状态解析 | 登记自身结果、修改目标状态、忽略版本和时点 |
| `Target State Resolution Registrar` | 登记合格的候选状态解析 | 修改候选内容、继承提交结果解析权威 |
| `Reconciler` | 追加新解析和审计记录 | 修改旧记录、制造缺失归因 |

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 确定性解析器自动获得解析登记权威；
- 提交执行权威被隐式解释为解析登记权威；
- 登记器修改候选解析内容；
- 把读取 `UNAVAILABLE` 与状态 `INDETERMINATE` 写入同一枚举；
- 使用无 `As Of`、版本或规则版本的“当前状态”；
- 跨时点比较提交结果和目标状态却不声明时间关系；
- 用未找到记录、缓存未命中或异步日志缺失证明 `ABORTED`；
- 在没有合格未应用证明时认定 `ABORTED`；
- 技术失败返回值替代原子中止证明；
- `COMMITTED` 反向创建目标迁移；
- 权威迁移记录与目标迁移不在同一不可分割边界；
- 对账修改旧尝试或旧解析记录；
- 同键建立多个迁移或同键绑定不同内容；
- 并发冲突时静默覆盖目标新版本；
- 外部副作用成功替代目标权威迁移；
- 补偿删除历史。

## 对第一修订版的映射

| 第一修订版条款 | 第二修订版处理 |
|---|---|
| `CM-R1-07` | 分离提交执行权威和解析登记权威 |
| `CM-R1-10` | 保留三值结果，要求 `ABORTED` 引用合格未应用证明 |
| `CM-R1-12` | 拆成目标读取结果与目标状态解析两个维度 |
| `CM-R1-17` | 增加所有解析的 `As Of`、权威版本和规则版本 |
| `CM-R1-20` | 增加候选解析记录与获授权登记边界 |
| `CM-R1-21` | 对账沿用相同解析登记路径，不获得特殊越权 |
| 提交结果矩阵 | 取消无时点矩阵，改为版本化记录和显式时间关系 |

## 对决策模型的关系

本提案不修改 `CR-0002-R1`。提交解析不创建第二次价值裁决；若提交过程中出现新的价值选择，则停止并请求新决策。

```text
Decision Fact -> authorizes deterministic projection
Commit Resolution -> classifies attribution
Target State Resolution -> resolves state as of a versioned time
```

三者不得互相替代。

## 仍待后续模型定义的问题

本提案不越权解决：

1. 具体数据库或分布式系统如何产生合格原子中止证明；
2. 各领域目标注册表如何提供封闭版本范围和查询完整性保证；
3. 目标状态解析记录是否需要独立于提交模型的通用现实层模型；
4. 跨注册表组合流程及其恢复算法；
5. 依赖失效传播算法；
6. 决策模型的正式冻结。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Decision / Commit Separation: PASS
Commit / Target Fact Causality: PASS
Commit Outcome / Target State Separation: PASS
Read Outcome / State Resolution Separation: PASS
Resolution Authority: PASS_WITH_REVIEW
Temporal and Version Binding: PASS_WITH_REVIEW
ABORTED Proof Boundary: PASS_WITH_REVIEW
Atomic Attribution: PASS_WITH_REVIEW
Record Immutability: PASS
Provider Independence: PASS
Domain Portability: PASS
Open Cross-model Dependencies: PRESENT
Freeze Readiness: REVIEW_REQUIRED
```

建议动作：由 Codex 依据本地冻结制度执行独立对象图、权威递归、否定性证据和跨时点一致性审查。未经该审查，不进入冻结准备度判断。
