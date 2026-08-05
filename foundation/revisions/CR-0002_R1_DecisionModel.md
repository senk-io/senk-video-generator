# 决策模型修订提案第一修订版

## 提案信息

```text
Proposal ID: CR-0002-R1
Title: Decision Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0002
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Review Turn: 7a95cd34-d84e-4f39-a10e-39f470d7057f
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Derived From: CR-0001-R2 Object Graph Consistency Review
```

> 本文件是待审查修订提案，不是冻结制度。它不能创建决策权威、改变正式事实或取代现行原则。

## 修订范围

本版保留 `CR-0002` 的核心方向，只修正以下五项阻断问题：

1. 分离决策记录、决策事实与目标对象迁移；
2. 把可受理依据的定义权交还具体决策类型制度；
3. 分离提交时准入检查与事后合法性审查；
4. 定义多权威场景的组合前置条件；
5. 分离裁决倾向与请求迁移类型。

## 核心定义

> 权威授予裁决资格，决策记录该资格被如何实际行使；合法决策首先建立决策事实，目标对象是否迁移还必须满足独立的迁移前置条件和制度提交。

## DM-R1-01 决策记录权威的一次实际行使

```text
Applicable Authority Grant
  -> Observable Decision Act
  -> Decision Record
```

`Authority` 回答谁有资格决定；`Decision Act` 是该资格在现实中的一次实际行使；`Decision Record` 保存这次行为的对象、依据、结果、时间和证据。

只有权威但没有决策行为，不能建立决策事实。只有决策行为但没有适用权威，只能形成非法决策尝试。

## DM-R1-02 决策只有一个目的

决策的唯一目的是：

> 记录有权主体针对合格依据作出的明确裁决。

决策不得承担以下职责：

- 观察现实；
- 创建或修改证据；
- 比较预期与观察；
- 解释偏差原因；
- 定义成功标准；
- 授予自身权威；
- 执行目标状态迁移；
- 证明自身判断客观正确。

## DM-R1-03 每个决策实例只有一个主要权威

```text
One Decision Record
  -> One Applicable Primary Authority Grant
```

主要权威必须在决策发生时同时满足：

- 仍然有效且未过期；
- 未被撤销或取代；
- 适用于指定对象及版本；
- 允许指定决策类型；
- 允许指定请求迁移类型；
- 覆盖决策者身份或角色；
- 满足适用制度的作用域限制。

身份匹配不能替代完整作用域合法性。

## DM-R1-04 多权威要求必须拆成多个决策

多个权威不得被拼接成一个没有主要责任主体的联合决策。

目标迁移可以声明 `Composite Decision Requirement`：

```text
Target Transition requires:
  Decision A = APPROVE
  Decision B = APPROVE
  Decision C = NOT_REQUIRED
```

`Composite Decision Requirement` 是目标迁移的前置不变量，不是新的权威、决策或基础层对象。

多个子决策齐备不能自动解释为存在一个隐式联合决策。目标制度必须明确最终状态由以下哪一种方式建立：

```text
Final Decision
or
Deterministic Institutional Commit
```

## DM-R1-05 决策必须引用合格依据

每项决策必须引用至少一个被适用制度认定为合格的依据。

`Decision Model` 不维护全局依据类型枚举，也不决定其他对象何时具有资格。

```text
Decision Type Governing Institution
  -> Allowed Basis Types
  -> Qualification Conditions
  -> Version Requirements
```

每个具体决策类型的治理制度必须声明：

- 允许哪些依据类型；
- 每类依据必须处于什么状态；
- 需要哪些资格记录和证据；
- 允许引用哪些版本；
- 依据缺失、过期或冲突时如何失败关闭。

没有外部资格定义时，依据不得由决策者临时认定为可受理。

## DM-R1-06 观察记录默认不是合格依据

`Registered Observation Record` 只证明观察已经登记，不自动证明它足以支持某项决策。

```text
Observer
  -> Candidate Observation Record

Observation Registration
  -> Registered Observation Record

Evidence Qualification
  -> Qualified Basis for a Specific Decision Type
```

只有适用决策制度明确允许，并且所需证据已达到对应资格要求时，观察记录才能成为合格依据。

## DM-R1-07 决策行为、记录、证据和结果必须分离

```text
Decision Act
Decision Record
Decision Evidence
Decision Disposition
Requested Transition Type
```

- `Decision Act`：主体实际行使权威的事件；
- `Decision Record`：该事件的不可变记录；
- `Decision Evidence`：证明谁在何时针对什么作出何种裁决；
- `Decision Disposition`：主体对请求的裁决倾向；
- `Requested Transition Type`：请求作用于目标对象的迁移语义。

任何两项都不得互相替代。

## DM-R1-08 裁决倾向与迁移类型必须分离

候选裁决倾向：

```text
APPROVE
REJECT
SUSPEND
NO_ACTION
```

候选请求迁移类型：

```text
CREATE
TRANSITION
SUPERSEDE
REVOKE
```

例如：

```text
Disposition: APPROVE
Requested Transition: REVOKE
```

表示批准撤销请求。

```text
Disposition: REJECT
Requested Transition: REVOKE
```

表示拒绝撤销请求。

把 `REVOKE` 同时当作裁决结果和迁移类型，会使这两种语义无法区分。

## DM-R1-09 决策事实与目标状态迁移必须分离

决策合法成立时，首先建立的是 `Decision Fact`，不是目标对象已经完成迁移的事实。

```text
Eligible Basis
+ Applicable Authority
+ Observable Decision Act
+ Decision Evidence
-> Admissible Decision Record

Admissible Decision Record
-> Decision Fact

Decision Fact
+ Required Transition Preconditions
+ Successful Institutional Commit
-> Target Formal State Transition
```

例如：

```text
Publication Decision = APPROVE
```

只建立“发布已获批准”的决策事实，不建立：

```text
Publication State = PUBLISHED
```

后者仍需要目标对象前置条件和成功的制度提交或发布执行。

## DM-R1-10 决策事实不会自动触发执行

```text
Decision Fact != Execution Completed
Decision Fact != Target Transition Committed
```

决策可以授权后续执行或满足迁移前置条件，但执行器必须显式引用该决策事实，并在自己的权威和契约下执行。

执行失败不能抹除决策事实；决策获批也不能证明执行已经完成。

## DM-R1-11 NO_ACTION 建立决策事实但不迁移目标状态

```text
NO_ACTION -> Decision Fact
NO_ACTION -/-> Target State Transition
```

有权主体明确决定保持当前状态，是必须保留的正式历史。它不建立新的目标对象状态，也不能通过“不保存记录”表达。

## DM-R1-12 提交时准入检查是确定性规则计算

`Decision Admissibility Check` 在决策提交时检查：

- 主要权威存在且在决策时点有效；
- 对象、对象版本和依据存在；
- 依据满足适用决策类型的资格要求；
- 裁决倾向属于允许枚举；
- 请求迁移类型属于允许范围；
- 必要证据齐备；
- 显式不变量未被破坏。

```text
Decision Admissibility Check
= Deterministic Rule Evaluation
!= Decision
```

它只能产生候选准入结果：

```text
ADMISSIBLE
INADMISSIBLE
INDETERMINATE
```

`INDETERMINATE` 必须失败关闭。准入检查不得创建新的权威、依据、决策或证据。

## DM-R1-13 准入检查不得形成决策递归

决策记录不得要求另一项“自我批准决策”证明自身成立。

```text
Applicable Authority
+ Qualified Basis
+ Observable Decision Act
+ Decision Evidence
+ Deterministic Admissibility Check
-> Admissible Decision Record
```

准入检查只执行冻结规则，不表达新的主观裁决。因此它不会形成：

```text
Decision A requires Decision B requires Decision C ...
```

## DM-R1-14 事后合法性审查不修改原决策

`Decision Legality Review` 是对既有决策记录的独立事后审查，可以形成：

```text
COMPLIANT
NON_COMPLIANT
INDETERMINATE
```

它可以：

- 确认记录符合当时适用制度；
- 发现权威、依据、证据或不变量缺陷；
- 请求拥有失效权威的主体作出新的失效决策；
- 触发制度化依赖失效传播。

它不得：

- 修改原始决策行为；
- 修改原始决策记录或证据；
- 直接抹除已存在的历史；
- 用当前制度追溯判定旧制度下合法决策非法；
- 在没有失效权威时自行改变目标状态。

## DM-R1-15 Admissible 不等于永远正确

采用 `Admissible Decision Record`，不采用容易暗示最终真实性的 `Valid Decision Record`。

`ADMISSIBLE` 只表示记录在提交时通过当时可执行的确定性制度检查。后续审计仍可能发现隐藏缺陷，但只能通过追加审查和新决策处理。

## DM-R1-16 决策不等于权威、证据、策略或执行

```text
Authority -> who may decide
Decision -> what was decided
Evidence -> what supports basis and act
Policy -> what future runtime action is authorized
Execution -> what action actually occurred
```

禁止以下替代：

```text
Evidence -/-> Decision
Policy -/-> Lifecycle Decision
Decision -/-> Evidence
Decision -/-> Execution Completed
Capability -/-> Authority
```

## DM-R1-17 决策不能验证自己

决策者不能仅凭自身声明证明：

- 权威在决策时点有效；
- 依据满足资格要求；
- 决策记录完整；
- 目标状态已经提交；
- 决策产生了预期效果；
- 主观判断具有客观唯一正确性。

准入检查和事后审查只能判断制度合法性与记录完整性，不能把价值判断转化为客观真理。

## DM-R1-18 人工创意裁决只要求可审计，不要求审美证明

人工创意裁决的最低决策证据包括：

```text
Decision Maker Identity
Applicable Authority Grant
Object and Version
Candidate Set and Referenced Evidence
Decision Disposition
Requested Transition Type
Decision Time
Recorded Rationale Requirement
```

理由可以是主观的，但必须真实记录。制度不得要求裁决者证明其审美选择“客观正确”。

## DM-R1-19 决策一经历史承诺即不可修改

正式提交以前存在的是决策请求或草案，不是决策事实，可以撤回或修订。

决策行为一旦发生并形成决策事实，就不得覆盖、删除或原地修改。变化只能追加新决策：

```text
Decision D1
  -> Revoked By Decision D2

Decision D1
  -> Superseded By Decision D3
```

新决策必须引用旧决策、新依据、新权威、新证据和变化原因。

## DM-R1-20 错误必须通过新历史纠正

### 记录错误

追加 `Correction Record`，保留原记录。

### 裁决不再适用

通过新的撤销或取代决策改变未来状态；原决策仍是当时合法历史。

### 决策提交时不合法

未通过准入检查的行为只能形成 `Illegal Decision Attempt`，不得建立决策事实或目标状态迁移。

### 事后发现隐藏合法性缺陷

由决策合法性失效权威或目标对象的上级治理权威作出新的失效决策。下游传播依据冻结依赖规则执行，不由审查者临时决定。

## DM-R1-21 决策类型制度必须定义专属契约

每一种决策类型必须在自己的治理制度中声明：

```text
Decision Type
Allowed Object Types
Allowed Basis Types
Basis Qualification Rules
Applicable Primary Authority Type
Allowed Dispositions
Allowed Transition Types
Composite Decision Requirements
Transition Preconditions
Commit Semantics
Evidence Requirements
Failure Behavior
```

通用决策模型只定义这些契约必须存在，不定义所有领域的具体类型全集。

## DM-R1-22 制度冻结决策具有更高准入门槛

制度冻结至少要求：

```text
Approved Institution Proposal
Compatibility Review
Migration or Supersession Plan
Independent Review Evidence
Applicable Freeze Authority
Freeze Decision
Successful Institution Commit
```

制度冻结不能与普通生命周期决策共享完全相同的准入门槛，也不能由运行时策略控制。

## 决策成立与目标迁移完整路径

```text
Decision Request
  -> Qualified Basis Resolution
  -> Applicable Authority Resolution
  -> Decision Act
  -> Decision Evidence
  -> Deterministic Admissibility Check
       -> INADMISSIBLE -> Illegal Decision Attempt
       -> INDETERMINATE -> Fail Closed
       -> ADMISSIBLE -> Admissible Decision Record
  -> Decision Fact
  -> Transition Preconditions Evaluation
       -> NOT_MET -> No Target Transition
       -> INDETERMINATE -> Fail Closed
       -> MET -> Institutional Commit
  -> Target Formal State Transition
```

`Decision Fact` 永远先于目标状态迁移。没有成功制度提交，目标迁移不得成立。

## 决策操作矩阵

| 操作 | 候选规则 |
|---|---|
| `Create` | 有权主体针对合格依据实施决策行为，通过准入后建立决策事实 |
| `Modify` | 禁止修改决策事实；提交前对象只是请求或草案 |
| `Observe` | 授权审计者可以读取决策及其完整引用链 |
| `Verify` | 独立审查合法性与记录完整性，不验证价值判断唯一正确 |
| `Approve` | 决策类型和主要权威允许时，产生 `APPROVE` 决策事实 |
| `Reject` | 决策类型和主要权威允许时，产生 `REJECT` 决策事实 |
| `Delete` | 禁止删除已经建立的决策事实和原始记录 |
| `Supersede` | 只能由新的合法决策显式取代，并保留旧决策 |

## 非法状态候选

以下情况应在未来冻结时明确为非法：

- 决策事实自动被当作目标对象已经迁移；
- 发布获批自动被当作已经发布；
- 决策模型维护所有领域依据类型的全局枚举；
- 登记观察未经适用资格要求就成为决策依据；
- 用另一项自我批准决策建立决策记录合法性；
- 事后审查修改原始决策或证据；
- 多个子决策自动合成为隐式联合决策；
- 把裁决倾向和迁移类型写入同一个枚举；
- 一个决策实例引用多个主要权威；
- 权威在决策时点已经过期、撤销或超出对象范围；
- `NO_ACTION` 不保存决策历史；
- 人工创意裁决被要求证明审美客观正确；
- 缺少合格依据、适用权威、证据或准入结果时继续迁移；
- 制度提交失败后仍宣布目标状态迁移成立；
- 用当前制度追溯否定旧制度下合法决策。

## 对原提案的修订映射

| 原条款 | 第一修订版处理 |
|---|---|
| `DM-03` | 增加组合决策要求及最终提交边界 |
| `DM-04` | 删除通用依据全集，改由具体决策类型制度定义 |
| `DM-05` | 拆成决策事实与目标状态迁移两阶段 |
| `DM-07` | 引入确定性准入检查，消除合法性递归 |
| `DM-08` | 拆分裁决倾向与请求迁移类型 |
| `DM-14` | 明确事后审查与失效决策的分离 |
| `DM-15` | 收紧权威在时间、对象、版本、类型和迁移范围上的有效性 |
| `DM-16` | 增加制度提交，彻底分离决策与目标状态迁移 |
| 未决问题 1 | 由具体决策类型治理制度定义依据资格 |
| 未决问题 2 | 登记观察默认不足，必须满足适用证据资格 |
| 未决问题 3 | 提交时准入是规则计算，事后审查另行保存 |
| 未决问题 4 | 多个决策加组合前置条件，不产生联合权威 |
| 未决问题 5 | 由失效权威作出新决策，依赖规则传播失效 |
| 未决问题 6 | `NO_ACTION` 建立决策事实，不迁移目标状态 |
| 未决问题 7 | 人工裁决要求可审计，不要求客观审美证明 |
| 未决问题 8 | 制度冻结采用更高准入门槛 |

## 仍待后续模型定义的问题

以下问题不应由决策模型越权解决：

1. `Institutional Commit` 的事务边界与原子性，属于现实层澄清或架构模型；
2. 观察登记和证据资格的完整生命周期，属于现实层与证据资格模型；
3. 比较记录、符合记录和偏差记录如何取得依据资格，属于比较与符合模型；
4. 各领域的决策类型、依据类型和迁移类型全集，属于对应领域治理制度；
5. 依赖失效传播的算法与边界，属于架构和执行制度。

## 当前审查状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
Authority Separation: PASS
Decision / Execution Separation: PASS
Decision / State Transition Separation: PASS
Non-recursive Foundation: PASS
History Preservation: PASS
Open Cross-model Dependencies: PRESENT
Freeze Readiness: REVIEW_REQUIRED
```

建议动作：将 `CR-0002-R1` 提交独立审查。只有审查确认上述跨模型依赖不会反向扩大决策职责后，才能进入正式冻结审查。
