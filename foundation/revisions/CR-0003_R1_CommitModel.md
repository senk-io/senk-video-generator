# 提交模型提案第一修订版

## 提案信息

```text
Proposal ID: CR-0003-R1
Title: Commit Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0003
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Review Turn: 2025febf-73f1-470e-947e-35cee1c2634b
Source Review Result: PASS_WITH_BLOCKERS
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
Derived From: CR-0003-TYPE-AUDIT
```

> 本文件是待审查修订提案，不是冻结制度。它不能授权提交、改变正式事实、覆盖现行原则或使任何上游草案自动冻结。

## 修订范围

本版保留 `CR-0003` 的基础方向，只修正外部审查确认的四项阻断问题：

1. 目标正式状态迁移先于 `COMMITTED` 结果归类；
2. 提交结果解析与目标当前状态解析相互独立；
3. 增加与目标迁移原子耦合的 `Authoritative Transition Record`；
4. 拆分尝试记录、解析记录、权威迁移记录和审计记录。

## 核心定义

> 提交是受制度约束的确定性投影过程：受保护的权威写入原子建立目标正式状态及其权威归因记录；提交结果解析只确认该迁移是否完整、唯一地归属于指定提交键，不创建目标迁移。

```text
Decision Fact
+ Applicable Commit Execution Authority
+ Commit Contract
+ Commit-point Preconditions
-> Commit Attempt
     -> Protected Authoritative Write
          -> Target Formal State Transition
          + Authoritative Transition Record
     -> Deterministic Commit Outcome Resolution
          -> COMMITTED
          -> ABORTED
          -> INDETERMINATE
```

合法因果关系是：

```text
Target Formal State Transition
+ Authoritative Transition Record
+ Sufficient Attribution Evidence
-> Commit Outcome = COMMITTED
```

禁止反向定义：

```text
Commit Outcome = COMMITTED
-/-> create Target Formal State Transition
```

## 对象与记录边界

| 节点 | 类型 | 唯一目的 | 唯一逻辑所有者 |
|---|---|---|---|
| `Commit Model` | 基础层制度模型 | 定义正式投影不变量 | 冻结制度 |
| `Commit Contract` | 值对象 | 声明目标迁移的确定性提交语义 | 目标类型治理制度 |
| `Committer` | 执行角色 | 实施提交尝试 | 无事实所有权 |
| `Commit Attempt` | 受治理的运行时过程实例 | 尝试执行声明写集 | 无持久事实所有权 |
| `Commit Attempt Record` | 不可变运行时记录 | 保存尝试输入和当时观察 | 提交账本 |
| `Authoritative Transition Record` | 权威迁移归因记录 | 把目标迁移唯一绑定到提交键和尝试 | 目标对象注册表 |
| `Commit Resolution Record` | 不可变解析记录 | 保存一次确定性结果解析 | 提交账本 |
| `Commit Audit Record` | 追加式审计记录 | 保存检查、错误、对账和审计过程 | 审计账本 |
| `Commit Outcome` | 值 | 表达本次提交归因结论 | 依附于解析记录 |
| `Target State Resolution` | 值 | 表达目标当前权威状态可解析性 | 依附于目标状态读取记录 |
| `Transaction` | 技术机制 | 提供原子性、隔离性或持久化能力 | 实现层 |

任何一个节点都不得替代其他节点。

## CM-R1-01 提交模型位于基础层，提交行为位于运行时

基础层定义提交不变量、记录边界和合法结果；运行时履行具体提交过程；架构层选择事务、锁、日志或一致性实现。

```text
Foundation -> defines Commit Model
Execution -> performs Commit Attempt
Architecture -> implements protected write
Target Registry -> owns authoritative target state and attribution
```

模型进入基础层不代表运行时提交过程拥有制度权威。

## CM-R1-02 提交只有一个目的

提交的唯一目的是：

> 在受保护权威边界内，把已经由适用决策事实授权的声明写集确定性投影为目标正式状态，并使该迁移能够唯一归属于本次提交键。

提交不得作出价值裁决、选择策略、解释偏差、授予权威、修改制度或扩张写集。

## CM-R1-03 决策事实与目标事实均为正式制度事实

`Decision Fact` 是治理型正式制度事实；目标状态可以是领域型或治理型正式制度事实。

```text
Formal Institutional Fact
  -> Governance Fact
       -> Decision Fact
  -> Domain Fact
       -> Domain Lifecycle Fact
```

分类表达事实作用对象，不表达合法性等级。

## CM-R1-04 决策事实先于提交并独立存续

```text
Decision Fact -> may authorize deterministic projection
Commit ABORTED -/-> Decision Fact Deletion
Commit INDETERMINATE -/-> Decision Fact Mutation
Commit COMMITTED -/-> Decision Fact Mutation
```

提交结果不得覆盖或降级输入决策事实。决策的未来效力发生变化时，必须通过新的合法历史表达。

## CM-R1-05 提交必须引用目标制度拥有的提交契约

每个允许正式迁移的目标类型必须声明 `Commit Contract`，至少包括：

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
Conflict Behavior
Evidence Requirements
Commit Outcome Semantics
```

提交器不得临时补充、删除或改写契约。

## CM-R1-06 提交不创建新的裁决

提交只执行冻结契约中的确定性规则。

```text
Commit Contract Evaluation
= Deterministic Rule Evaluation
!= Decision
```

一旦出现新的价值判断、范围选择、冲突裁决或写集扩张，必须中止并请求新的决策。

## CM-R1-07 每次提交尝试只有一个主要执行权威

每次尝试必须引用一个在提交时有效的主要提交执行授权，覆盖提交者、目标对象、预期版本、迁移类型、声明写集、目标注册表、时间和作用域。

提交执行权威只允许履行确定性投影，不等于决策权威，也不能从技术写权限反向推导。

## CM-R1-08 前置条件检查与权威写入必须共享受保护边界

提交点必须重新检查：

- 决策事实仍可用于本次未来迁移；
- 组合决策要求已经齐备；
- 目标对象处于预期源状态和版本；
- 依赖事实没有失效、撤销或被取代；
- 声明写集与提交契约一致；
- 必要依据和证据仍满足资格；
- 目标不变量没有被破坏。

检查与目标写入之间不得存在未受保护的竞态窗口。

## CM-R1-09 技术事务不能替代制度提交

```text
Database Commit
File Write
API Success
Message Acknowledgement
Event Published
-/-> Commit Outcome = COMMITTED
```

`COMMITTED` 必须由目标权威迁移、与其原子耦合的权威迁移记录以及充分归因证据共同证明。异步提交审计记录可以迟到追加，但不能成为目标状态或迁移归因的唯一真源。

## CM-R1-10 提交结果保持三值

`Commit Outcome Resolution` 回答：

> 当前提交键对应的声明写集，是否完整且唯一地形成了目标权威迁移？

合法结果只有：

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：能够证明声明写集已完整形成目标权威迁移，并唯一归属于当前提交键；
- `ABORTED`：能够证明当前提交键没有形成声明的目标权威迁移；
- `INDETERMINATE`：无法证明当前提交键属于前两种情况。

`INDETERMINATE` 不是失败结论，必须阻断依赖本次归因的后续行为并进入对账。

## CM-R1-11 目标迁移先于提交结果归类

目标正式状态迁移发生在受保护权威写入中。`COMMITTED` 只确认已经发生的迁移完整归属于本次提交尝试。

```text
Commit-point Preconditions = MET
  -> Protected Authoritative Write
       -> Target Formal State Transition
       + Authoritative Transition Record
  -> Commit Outcome Resolution
       -> COMMITTED
       -> ABORTED
       -> INDETERMINATE
```

不得用提交结果反向创建目标状态，也不得因解析记录迟到而否认已经由权威边界原子建立的迁移。

## CM-R1-12 提交结果与目标当前状态必须分离

`Commit Outcome Resolution` 与 `Target State Resolution` 回答不同问题。

```text
Commit Outcome Resolution
  -> COMMITTED | ABORTED | INDETERMINATE

Target State Resolution
  -> KNOWN | UNKNOWN | UNAVAILABLE
```

- `KNOWN`：能够从目标权威注册表确定当前状态和版本；
- `UNKNOWN`：目标注册表可访问，但不能建立唯一可信当前状态；
- `UNAVAILABLE`：目标权威注册表当前不可访问。

合法组合包括：

```text
Commit Outcome = INDETERMINATE
Target State Resolution = KNOWN
Commit Attribution = UNRESOLVED
```

因此：

```text
Commit Outcome = INDETERMINATE
-/-> Target State Resolution = UNKNOWN
```

只有目标权威状态本身无法唯一解析时，目标状态解析才是 `UNKNOWN`；访问失败时是 `UNAVAILABLE`。

## CM-R1-13 ABORTED 与 INDETERMINATE 必须分开保存

不得再用“失败尝试”统称 `ABORTED` 与 `INDETERMINATE`。

```text
ABORTED Attempt
  -> Commit Attempt History
  -/-> Target Transition

INDETERMINATE Attempt
  -> Unresolved Commit History
  -/-> Trusted Attribution Claim
```

`INDETERMINATE` 期间可能已经存在目标迁移，但系统尚不能把该迁移可信归属于当前提交键。

## CM-R1-14 一个提交边界内禁止部分成功

声明写集与 `Authoritative Transition Record` 必须在同一不可分割权威边界中整体成立。

观察到部分写入、缺失归因记录或归因记录与写集不一致时，提交结果只能保持 `INDETERMINATE`，并失败关闭进入对账。

不得静默补写来制造原子历史。

## CM-R1-15 多事实提交必须证明共享原子边界

单次提交可以建立多个正式事实，但必须证明它们与各自必要归因信息共享一个不可分割提交边界。

```text
Same Database
-/-> Same Atomic Boundary

Saga
Outbox
Compensation Workflow
Multiple Local Transactions
-/-> One Global Atomic Commit
```

不能证明共享原子性时，必须拆成多个提交并显式记录组合进度。

## CM-R1-16 组合提交不是联合权威

多个提交解析记录可以满足 `Composite Commit Requirement`，但不能产生隐式联合决策或联合权威。

组合完成条件若能由冻结制度确定性计算，可以建立候选组合完成记录；若需要价值判断，则必须请求新的决策。

## CM-R1-17 提交键必须稳定且幂等

`Commit Key` 至少绑定：

```text
Decision Fact References
Target Object ID
Expected Source Version
Requested Transition Type
Declared Write Set Digest
Commit Contract Version
```

相同提交键和相同声明内容不得产生第二次迁移。相同键但内容不同属于非法冲突，必须失败关闭。

## CM-R1-18 并发冲突不得静默覆盖

```text
Expected Source Version != Authoritative Source Version
  -> ABORTED
  or INDETERMINATE when authoritative resolution is unavailable
```

不得采用最后写入获胜覆盖没有被本次决策授权的新状态。已经存在同一提交键的权威迁移记录时，应解析既有结果，不得再次执行迁移。

## CM-R1-19 权威迁移记录必须与目标迁移原子耦合

每次目标迁移必须同时建立 `Authoritative Transition Record`，至少保存：

```text
Commit Key
Commit Attempt ID
Decision Fact References
Commit Contract Version
Prior Authoritative Version
New Authoritative Version
Applied Write Set Digest
Committed At
```

该记录属于目标权威边界，是提交归因真源。它必须内嵌于目标权威状态，或与目标迁移共享可证明的不可分割提交边界。

异步提交账本、消息、日志或审计事件不得成为目标迁移唯一归因来源。

## CM-R1-20 提交记录必须拆分且不可原地改写

### `Commit Attempt Record`

保存提交键、尝试标识、上次尝试引用、契约版本、决策事实、执行授权、目标与预期版本、声明写集、前置检查、开始时间及当时可观察结果。

### `Authoritative Transition Record`

与目标迁移原子成立，保存权威版本变化和提交归因。

### `Commit Resolution Record`

追加保存一次确定性解析结论、所依据的权威迁移记录和证据、解析者、解析时间及结果。

### `Commit Audit Record`

追加保存检查、异常、重试、对账和审计过程。它可以迟到，但必须保留真实发生时间与记录时间。

禁止在对账后把原始尝试记录中的 `INDETERMINATE` 原地改成 `COMMITTED`。

## CM-R1-21 对账追加解析记录，不修改原始尝试

```text
Original Attempt Observation = INDETERMINATE
Reconciliation
  -> Commit Resolution Record = COMMITTED | ABORTED | INDETERMINATE
```

对账只读取目标权威状态、权威迁移记录、提交记录和证据，执行确定性事实解析。它不是新的决策，也不能创建缺失的归因历史。

证据仍不足时必须追加新的 `INDETERMINATE` 解析记录，而不是覆盖旧记录。

## CM-R1-22 重试与补偿必须追加历史

重试是新的 `Commit Attempt`，必须引用原尝试和重试依据。`INDETERMINATE` 未对账时，不得使用新提交键绕过幂等保护。

已经发生的目标迁移若需要恢复，只能通过新的合法决策和新提交建立补偿迁移：

```text
Committed Transition
  -> New Compensating Decision
  -> New Commit
  -> New Target State
```

补偿不得删除旧迁移和旧归因记录。

## CM-R1-23 外部副作用必须显式分离

无法纳入同一权威原子边界的发布、通知、模型调用、文件分发或第三方写入，不得伪装为目标状态提交的一部分。

```text
Authoritative State Transition
Authoritative Transition Record
External Effect Execution
External Effect Observation
External Effect Confirmation
```

目标制度负责定义目标迁移与外部副作用的顺序；基础模型不替领域选择顺序，也不把外部成功当作权威迁移证据。

## CM-R1-24 提交与解析都不能自证

提交器的返回值不能独自证明写入、原子性、归因或目标版本。解析器也不能通过自己的结论创建缺失的权威迁移记录。

`COMMITTED` 必须能够从以下内容重新审计：

```text
Target Authoritative State
+ Authoritative Transition Record
+ Applicable Decision Facts
+ Commit Contract Version
+ Sufficient Attribution Evidence
```

## 修订后的完整路径

```text
Decision Fact
  -> Commit Request
  -> Commit Contract Resolution
  -> Commit Execution Authority Resolution
  -> Commit Key Resolution
  -> Commit-point Preconditions Evaluation
       -> NOT_MET
            -> Commit Attempt Record
            -> Commit Resolution Record: ABORTED

       -> INDETERMINATE
            -> Commit Attempt Record
            -> Commit Resolution Record: INDETERMINATE
            -> Reconciliation Required

       -> MET
            -> Protected Authoritative Write
                 -> Target Formal State Transition
                 + Authoritative Transition Record
            -> Commit Attempt Record
            -> Deterministic Commit Outcome Resolution
                 -> proven attributable and complete
                      -> Commit Resolution Record: COMMITTED
                 -> proven not applied
                      -> Commit Resolution Record: ABORTED
                 -> otherwise
                      -> Commit Resolution Record: INDETERMINATE
                      -> Reconciliation Required
```

`Commit Audit Record` 可以在各阶段追加，但不参与创建目标权威状态，也不能替代 `Authoritative Transition Record`。

## 提交结果与状态解析矩阵

| 提交结果 | 目标状态解析 | 合法解释 | 后续边界 |
|---|---|---|---|
| `COMMITTED` | `KNOWN` | 迁移完整归属于本次提交键，当前状态可读取 | 允许依赖迁移继续 |
| `ABORTED` | `KNOWN` | 本次提交未形成迁移，目标当前状态明确 | 可依据新事实重新规划 |
| `INDETERMINATE` | `KNOWN` | 当前状态明确，但本次提交归因未决 | 阻断依赖本次归因的行动并对账 |
| `INDETERMINATE` | `UNKNOWN` | 状态与归因都无法唯一解析 | 全面失败关闭并对账 |
| `INDETERMINATE` | `UNAVAILABLE` | 权威注册表不可访问 | 保持未知，不重试迁移，先恢复读取能力 |
| `COMMITTED` | `UNKNOWN` 或 `UNAVAILABLE` | 解析结论与当前读取状态可能处于不同时间点 | 不能仅据当前读取失败撤销既有解析；需检查证据时点 |

矩阵不要求所有组合都能长期存在；它只禁止从提交结果机械推导目标当前状态。

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 用 `COMMITTED` 反向创建目标状态迁移；
- 把目标状态变化直接等同于本次提交已成功归因；
- 把 `INDETERMINATE` 自动解释成目标状态 `UNKNOWN`；
- 目标迁移没有原子耦合的权威迁移记录；
- 只在异步审计账本保存提交归因；
- 把尝试记录、解析记录、权威迁移记录和审计记录合并为可变记录；
- 对账后原地修改原始尝试结果；
- 用“失败”统称 `ABORTED` 与 `INDETERMINATE`；
- 证据不足时把不确定尝试认定为未发生；
- 没有共享不可分割边界却宣称全局原子提交；
- 提交器扩大决策语义或写集；
- 没有提交执行权威就写入目标注册表；
- 技术事务、接口、文件、消息或外部副作用替代制度归因；
- 相同提交键建立多个目标迁移；
- 并发冲突时静默覆盖权威新版本；
- 重试、对账或补偿覆盖旧历史。

## 对原提案的修订映射

| 原条款 | 第一修订版处理 |
|---|---|
| `CM-09` | 以权威迁移记录和归因证据取代“异步提交记录齐备”的模糊要求 |
| `CM-10` | 保留三值结果，改为提交键归因结论 |
| `CM-11` | 推翻 `COMMITTED -> 迁移`，改为迁移先于结果归类 |
| `CM-12` | 分离提交结果与目标当前状态解析 |
| `CM-13` | 分离 `ABORTED` 和 `INDETERMINATE` 历史语义 |
| `CM-18` | 拆分四类记录，禁止原地修改 |
| `CM-20` | 对账只能追加解析记录 |
| `CM-22` | 将目标归因真源收回目标权威边界 |
| 提交完整路径 | 改为权威迁移与归因记录先成立，结果后解析 |

## 对决策模型的澄清关系

本提案不修改 `CR-0002-R1`。若未来两者均通过冻结审查，应统一以下映射：

| 决策模型当前术语 | 第一修订版候选解释 |
|---|---|
| `Institutional Commit` | 跨领域通用的受治理 `Commit` 过程 |
| `Successful Institutional Commit` | 已存在目标权威迁移且解析结果为 `COMMITTED` |
| `Target Formal State Transition` | 在受保护权威写入中成立的正式迁移 |
| `Commit Semantics` | 目标类型治理制度拥有的 `Commit Contract` |

## 仍待后续模型定义的问题

本提案不越权解决：

1. 不同技术栈如何实现原子写入、锁、日志和一致性；
2. 目标状态读取的缓存与时点一致性模型；
3. 跨注册表组合流程的恢复算法；
4. 依赖失效传播的算法和边界；
5. 各领域具体状态机、写集和外部副作用顺序；
6. 决策模型本身的正式冻结。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Decision / Commit Separation: PASS
Commit / Target Fact Causality: PASS
Commit Outcome / Target State Separation: PASS
Atomic Attribution: PASS_WITH_REVIEW
Record Separation: PASS
Three-value Result Model: PASS
Commit / Transaction Separation: PASS
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Open Cross-model Dependencies: PRESENT
Freeze Readiness: REVIEW_REQUIRED
```

建议动作：提交独立审查。审查应重点尝试推翻权威迁移记录的最小字段、`KNOWN / UNKNOWN / UNAVAILABLE` 三值状态解析，以及跨时点出现 `COMMITTED + UNKNOWN` 时是否会产生新的概念漂移。
