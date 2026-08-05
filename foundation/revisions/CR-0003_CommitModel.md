# 提交模型提案

## 提案信息

```text
Proposal ID: CR-0003
Title: Commit Model
Status: DRAFT
Authority: NONE
Executable: NO
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: 3ca24e43-5b46-473a-b6f3-6d63de3fb0a6
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0002-R1 Decision Model
Derived From: CR-0003-TYPE-AUDIT
```

> 本文件是待审查提案，不是冻结制度。它不能授权提交、改变正式事实、覆盖现行原则或使 `CR-0002-R1` 自动冻结。

## 核心定义

> 提交是一个受制度约束的原子过程：它引用已经成立且仍适用的决策事实，在提交点重新确认目标迁移前置条件，并把声明写集完整投影到目标权威注册表。

```text
Decision Fact
+ Applicable Commit Execution Authority
+ Commit Contract
+ Transition Preconditions at Commit Point
-> Commit Attempt
     -> Observed Commit Outcome
     -> Commit Evidence
     -> Deterministic Result Resolution
          -> COMMITTED
          -> ABORTED
          -> INDETERMINATE
```

只有 `COMMITTED` 才能建立本次声明的目标正式状态。

## CM-01 提交模型位于基础层，提交行为位于运行时

基础层定义提交的不变量、类型边界和合法结果；运行时执行具体提交。

```text
Foundation -> defines Commit Model
Execution -> performs Commit Attempt
Architecture -> implements isolation and persistence
Target Registry -> owns committed target state
```

模型所在层级不能被解释为提交过程拥有制度权威。

## CM-02 提交只有一个目的

提交的唯一目的是：

> 原子建立一项决策已经授权、目标制度已经定义且提交点前置条件仍然满足的目标正式状态。

提交不得观察现实、作出价值裁决、解释偏差、选择策略、授予权威或修改制度。

## CM-03 决策事实是治理事实

`Decision Fact` 是 `Formal Institutional Fact` 的治理事实子类型。目标状态是同一正式事实体系中的领域事实或治理对象事实。

```text
Formal Institutional Fact
  -> Governance Fact
  -> Domain Fact
```

两者没有高低关系，但承担不同语义：决策事实记录“已经裁决什么”，目标事实记录“权威目标状态已经改变什么”。

## CM-04 决策事实先于提交且独立存续

```text
Decision Fact -> may enable Commit
Commit Failure -/-> Decision Fact Deletion
Commit Success -/-> Decision Fact Mutation
```

提交结果无论为何，都不得修改、覆盖或删除输入决策事实。决策后来被撤销或取代时，原决策仍然是历史事实，但能否继续作为提交依据由目标制度决定。

## CM-05 提交必须引用提交契约

每个允许正式迁移的目标类型必须由其治理制度声明 `Commit Contract`，至少包括：

```text
Target Object Type
Allowed Transition Type
Required Decision Fact Types
Composite Decision Requirements
Expected Source State and Version
Transition Preconditions
Declared Write Set
Atomicity Boundary
Conflict Behavior
Evidence Requirements
Commit Result Semantics
```

提交器不得临时补充或改写契约。

## CM-06 提交不创建新的裁决

提交只执行已经冻结的确定性契约。

```text
Commit Contract Evaluation
= Deterministic Rule Evaluation
!= Decision
```

若执行需要在多个合法选项之间作价值选择、扩大写集或改变请求迁移类型，必须中止并请求新的决策。

## CM-07 每次提交尝试只有一个主要执行权威

每次 `Commit Attempt` 必须引用一个仍然有效的主要提交执行授权。授权必须覆盖：

- 提交者身份或角色；
- 目标对象和版本；
- 请求迁移类型；
- 声明写集；
- 允许访问的目标注册表；
- 适用时间和作用域。

提交执行权威不等于决策权威，也不允许提交者改变决策内容。

## CM-08 提交点必须重新检查前置条件

前置条件曾经成立不能证明提交时仍成立。提交必须在能够保护目标写集的一致性边界内重新检查：

- 适用决策事实存在且未失去未来效力；
- 所有组合决策要求齐备；
- 目标对象仍处于预期源状态和版本；
- 依赖事实没有被取代、撤销或失效；
- 声明写集与契约完全一致；
- 必要证据可定位且满足适用资格；
- 没有违反目标不变量。

检查与写入之间不得存在未受保护的竞态窗口。

## CM-09 技术事务不能替代制度提交

数据库事务、文件写入、接口成功、消息确认或事件发布都只是实现证据的一部分。

```text
Technical Transaction Success
-/-> Institutional Commit Success
```

只有目标权威注册表中的声明写集完整成立，并且提交记录与证据齐备时，结果才能是 `COMMITTED`。

## CM-10 提交结果必须三值化

合法结果只有：

```text
COMMITTED
ABORTED
INDETERMINATE
```

- `COMMITTED`：声明写集完整且可证明地进入目标权威状态；
- `ABORTED`：可以证明本次声明迁移没有进入目标权威状态；
- `INDETERMINATE`：无法证明已提交或未提交。

`INDETERMINATE` 必须失败关闭并进入对账；不得按普通失败直接重试。

## CM-11 提交成功才建立目标正式状态

```text
COMMITTED -> Target Formal State Transition
ABORTED -/-> Target Formal State Transition
INDETERMINATE -/-> New Trusted Target State Claim
```

当结果不确定时，系统只能把最后一个已确认状态保留为历史参照，同时明确标记存在未决提交。当前可信状态必须保持 `UNKNOWN` 或等价的阻断投影，不得把旧状态或可能的新状态补推为当前事实。

## CM-12 提交失败不污染目标历史

`ABORTED` 必须保证声明写集没有部分成为本次目标权威状态。失败尝试仍保留独立提交记录和证据，但不能伪装成目标生命周期迁移。

```text
Failed Attempt -> Commit History
Failed Attempt -/-> Target Lifecycle Fact
```

## CM-13 一个提交边界内禁止部分成功

一个提交声明的写集只能整体 `COMMITTED` 或整体不成立。

如果观察到部分写入：

```text
Commit Result = INDETERMINATE
System = FAIL_CLOSED
Required Action = RECONCILIATION
```

不得把部分写入标记为成功，也不得静默补写剩余部分来伪造原子历史。

## CM-14 多事实提交必须证明共享原子边界

单次提交可以建立多个正式事实，但必须证明它们共享同一原子边界。若跨越无法共同提交的注册表、存储或外部系统，则必须拆成多个提交。

拆分后的流程可以具有组合完成条件，但不得宣称不存在的全局原子性。

```text
Multiple Local Commits
!= One Global Atomic Commit
```

## CM-15 组合提交不是联合权威

多个提交记录可以满足一个 `Composite Commit Requirement`，但不能自动产生新的联合权威或隐式联合决策。

组合完成事实必须由适用制度定义确定性成立条件；若仍需主观裁决，则必须建立新的决策事实。

## CM-16 提交必须幂等

每次提交必须具有稳定的 `Commit Key`。相同键和相同声明内容的重放只能返回既有结果或继续未决对账，不能建立第二次目标迁移。

相同键但内容不同属于非法冲突，必须失败关闭。

## CM-17 并发冲突不得静默覆盖

提交必须绑定目标预期源版本。若目标状态在提交前已经迁移：

```text
Expected Version != Authoritative Version
  -> ABORTED
  or INDETERMINATE when authoritative state cannot be resolved
```

不得采用最后写入获胜来覆盖未被本次决策授权的新状态。

## CM-18 每次尝试必须建立不可变提交记录

`Commit Record` 至少保存：

```text
Commit ID
Commit Key
Attempt ID
Prior Attempt Reference
Commit Contract Version
Decision Fact References
Commit Execution Authority
Target Object and Expected Version
Declared Write Set Digest
Precondition Evaluation Record
Result
Commit Evidence References
Started At
Resolved At
Target Authoritative Version after Commit
```

不适用字段必须明确标记，不得静默省略影响审计的内容。

## CM-19 重试必须追加历史

每次重试都是新的 `Commit Attempt`，必须引用原尝试和重试依据。重试不得覆盖原记录，也不得在 `INDETERMINATE` 尚未对账时使用新键绕过幂等保护。

## CM-20 对账不是决策

`Commit Reconciliation` 只读取目标权威状态、提交日志和证据，以确定先前不确定尝试的实际结果。

```text
Reconciliation = Deterministic Fact Resolution
Reconciliation != Decision
```

对账可以追加结果确认记录，但不得修改原始提交记录。若现有证据仍不足，结果继续保持 `INDETERMINATE`。

## CM-21 补偿是新的正式迁移

已经 `COMMITTED` 的事实不能通过技术回滚从历史中消失。若业务需要恢复先前状态，必须经过适用的新决策和新提交。

```text
Committed Transition
  -> New Compensating Decision
  -> New Commit
  -> New Target State
```

补偿不证明原提交从未发生。

## CM-22 提交记录与目标事实必须分离

`Commit Record` 证明提交过程发生了什么；目标注册表拥有提交后正式状态。任何一方都不得替代另一方。

```text
Commit Ledger -> Commit History
Target Registry -> Authoritative Target State
Evidence Ledger -> Supporting Evidence
Decision Ledger -> Decision Facts
```

派生界面、缓存、事件投影或导出物不能反向创建提交成功事实。

## CM-23 外部副作用必须显式建模

无法纳入同一原子边界的发布、通知、模型调用、文件分发或第三方写入，不得被伪装成目标状态提交的一部分。

必须区分：

```text
Authoritative State Commit
External Effect Execution
External Effect Observation
External Effect Confirmation
```

目标状态是否应在外部副作用之前或之后建立，由具体目标制度定义；基础模型不替各领域选择顺序。

## CM-24 提交不能自证

提交器不能仅凭自身返回值证明：

- 前置条件检查完整；
- 写集已经原子落盘；
- 目标权威版本已经推进；
- 外部副作用已经发生；
- 提交证据充分。

提交结果必须能够由目标权威状态、不可变记录和独立证据重新审计。

## 提交完整路径

```text
Decision Fact
  -> Commit Request
  -> Commit Contract Resolution
  -> Commit Execution Authority Resolution
  -> Commit Key Resolution
  -> Commit-point Preconditions Evaluation
       -> NOT_MET -> ABORTED
       -> INDETERMINATE -> INDETERMINATE
       -> MET -> Atomic Write Attempt
            -> PROVEN_ALL_WRITTEN -> COMMITTED
            -> PROVEN_NONE_WRITTEN -> ABORTED
            -> OTHERWISE -> INDETERMINATE
  -> Immutable Commit Record
  -> if COMMITTED: Target Formal State Transition
```

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 把 `Commit` 同时定义成规则、角色、过程、记录和目标事实；
- 没有决策事实就提交需要裁决的目标迁移；
- 提交器在执行中扩大裁决范围或写集；
- 没有提交执行权威就写入目标注册表；
- 仅凭数据库、文件、接口或消息成功宣布制度提交成功；
- 前置条件检查与写入之间存在未保护竞态；
- 用单一 `FAILED` 隐藏结果未知；
- 在 `INDETERMINATE` 未对账时盲目重试；
- 把部分写入宣布为提交成功；
- 没有共享原子边界却宣称全局原子提交；
- 相同提交键产生不同迁移内容；
- 并发冲突时静默覆盖权威新版本；
- 修改、覆盖或删除提交记录；
- 用补偿删除已经发生的提交历史；
- 让提交结果反向修改决策事实；
- 把外部副作用成功等同于目标权威状态已经提交。

## 对决策模型的澄清关系

本提案不修改 `CR-0002-R1`。若未来两者均被冻结，以下术语映射应由冻结审查统一处理：

| 决策模型当前术语 | 提交模型候选解释 |
|---|---|
| `Institutional Commit` | 跨领域通用的 `Commit` |
| `Successful Institutional Commit` | `Commit Result = COMMITTED` |
| `Target Formal State Transition` | 目标注册表中由成功提交建立的正式状态迁移 |
| `Commit Semantics` | 目标类型治理制度拥有的 `Commit Contract` |

## 仍待后续模型定义的问题

本提案不越权解决：

1. 不同技术栈如何实现事务、锁、日志和一致性；
2. 观察记录与证据资格的完整生命周期；
3. 依赖失效如何沿对象图传播；
4. 各领域具体写集、状态机和外部副作用顺序；
5. 跨注册表组合流程的恢复算法；
6. 决策模型本身的正式冻结。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Decision / Commit Separation: PASS
Commit / Target Fact Separation: PASS
Commit / Transaction Separation: PASS
Authority Separation: PASS_WITH_REVIEW
Atomicity Boundary: PASS_WITH_REVIEW
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Open Cross-model Dependencies: PRESENT
Freeze Readiness: REVIEW_REQUIRED
```

建议动作：把本草案提交独立对象图、事务边界和历史一致性审查。审查必须重点尝试推翻“三值结果是否充分”“目标正式事实是否需要额外决策”以及“多注册表提交是否存在被误称为原子提交”的假设。
