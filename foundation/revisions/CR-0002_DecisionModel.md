# 决策模型修订提案

## 提案信息

```text
Proposal ID: CR-0002
Title: Decision Model
Status: DRAFT
Authority: NONE
Executable: NO
Lifecycle: SUPERSEDED_DRAFT
Superseded By: CR-0002-R1
Source Conversation: 6a6ecde3-0aa4-83ee-a53c-7c707fbf57f2
Source Turn: fa90ab0c-308e-4bb7-b232-6cc19ff8e9f3
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Derived From: CR-0001-R2 Object Graph Consistency Review
```

> 本文件是待审查修订提案，不是冻结制度。它不能创建决策权威、改变正式事实或取代任何现行原则。

本初稿已由 [`CR-0002_R1_DecisionModel.md`](./CR-0002_R1_DecisionModel.md) 形成独立修订版。保留本文件仅用于审计提案演化历史，后续审查应以第一修订版为准。

## 提案目标

本提案只回答一个问题：

> 拥有权威的主体实际作出的裁决，如何被记录，并合法建立、拒绝或迁移正式制度事实？

核心候选原则是：

> 权威授予裁决资格，决策记录该资格被如何实际行使；只有合法决策才能建立或迁移正式制度事实。

## DM-01 决策是权威被实际行使的记录

`Authority` 回答谁有资格决定；`Decision` 回答该资格在一个具体对象和时点上被如何行使。

```text
Authority Grant
  -> Decision Act
  -> Decision Record
```

只有权威而没有决策，不能证明任何状态迁移已经发生。只有决策而没有适用权威，只能形成一次非法决策尝试。

## DM-02 决策拥有唯一目的

`Decision` 的唯一目的，是记录有权主体针对可受理依据作出的明确裁决。

决策不负责：

- 观察现实；
- 创造证据；
- 比较预期与观察；
- 解释偏差原因；
- 定义权威；
- 定义成功；
- 执行被裁决的后续动作；
- 证明自身裁决是正确的。

## DM-03 每项决策只能引用一个主要适用权威

每个决策实例必须引用一个且仅一个主要决策权威及其版本。

```text
One Decision Record -> One Applicable Primary Authority Grant
```

决策可以拥有多个前置条件和约束，但不能把多个权威拼接成一个无法追责的混合裁决。

如果一项业务动作确实需要多个独立权威，应建立多个可追踪决策，并由后续组合不变量判断它们是否齐备，而不是创建“联合但无主”的决策。

## DM-04 决策必须针对可受理依据

决策不能凭空作用于未知对象。每项决策必须引用制度允许的 `Eligible Basis`。

候选可受理依据包括：

```text
Certified Comparison Record
Conformance Record
Gap
Existing Formal Institutional Fact
Policy Candidate
Institution Proposal
Registered Observation Record
```

具体决策类型只能使用其制度明确允许的依据。可受理依据的类型不得由决策者临时扩张。

## DM-05 正式事实需要完整成立基础

候选公式为：

```text
Eligible Basis
+ Applicable Authority
+ Decision Act
+ Decision Evidence
= Valid Decision Record
-> Formal Institutional Fact | Rejection Fact | Suspension Fact
```

这取代容易被误解的简化表达：

```text
Authority + Evidence + Decision = Formal Fact
```

旧公式仍表达正确方向，但缺少“决策只能作用于可受理依据”的限制。

## DM-06 决策行为与决策记录不得混同

系统必须区分：

```text
Decision Act
Decision Record
Decision Evidence
Decision Result
```

- `Decision Act`：有权主体实际实施裁决的事件；
- `Decision Record`：对该事件及其输入、权威和结果的不可变记录；
- `Decision Evidence`：证明谁在何时针对什么依据实施了什么裁决；
- `Decision Result`：该裁决建立、拒绝、迁移、暂停或取代的对象状态。

决策记录不能反向替代决策行为；界面字段或数据库行存在不能单独证明裁决合法发生。

## DM-07 决策成立不得形成无限递归

决策记录不能要求另一项决策来证明“这项决策曾经发生”，否则会形成：

```text
Decision A requires Decision B
Decision B requires Decision C
...
```

候选非递归边界是：

```text
Applicable Authority
+ Eligible Basis
+ Observable Decision Act
+ Decision Evidence
-> Valid Decision Record
```

`Decision Act` 是在现实中发生的权威行使事件。其记录合法性由冻结制度、适用权威、可受理依据和证据共同判断，不由决策者再作一项“自我批准决策”。

独立审查可以判断该记录是否满足制度条件，但审查结果不得修改原始决策行为和证据。

## DM-08 决策不必建立目标事实

决策必须拥有明确结果，但并非每项决策都会建立请求的目标事实。

候选结果类型包括：

```text
CREATE
TRANSITION
SUPERSEDE
REVOKE
REJECT
SUSPEND
NO_ACTION
```

- `CREATE`、`TRANSITION`、`SUPERSEDE` 和 `REVOKE` 改变正式对象的制度状态；
- `REJECT` 拒绝建立请求的目标事实，但会保存拒绝决策历史；
- `SUSPEND` 暂停裁决或后续执行；
- `NO_ACTION` 明确决定不改变当前正式状态。

拒绝和不行动不能通过“不写记录”来表达。

## DM-09 决策不等于策略

`Decision` 记录实际裁决；`Policy` 只控制未来运行时行动。

```text
Lifecycle Decision
  -> changes formal object state

Policy Selection Decision
  -> selects a Policy

Policy
  -> authorizes next runtime execution
```

选择、验收、发布、覆盖和制度审查属于决策，不应伪装成补救策略。

策略不能选择自己。策略必须由拥有策略选择权威的决策建立其适用事实。

## DM-10 决策不等于权威

权威是资格，决策是该资格的一次具体行使。

```text
Authority != Decision
Capability != Authority
Decision without Authority = Illegal Decision Attempt
```

一项历史决策不能因为执行结果良好而反向扩大决策者的权威。

## DM-11 决策不等于证据

证据支持决策的依据与发生过程，但证据本身不能作出裁决。

```text
Evidence -/-> Decide
Decision -/-> Create Evidence
```

决策必须分别引用：

1. 支持可受理依据的证据；
2. 证明决策行为发生的决策证据。

两类证据可以引用同一不可变来源，但必须具有各自明确的现实归属和观察范围。

## DM-12 决策不能验证自己

决策者不能仅凭自身声明证明：

- 自己拥有适用权威；
- 依据满足准入条件；
- 决策记录完整；
- 决策结果已经正确投影；
- 决策取得了预期效果。

独立检查只能验证决策的制度合法性和记录完整性，不能证明审美、商业或治理判断具有唯一正确答案。

## DM-13 决策一经历史承诺即不可修改

在正式提交之前，候选决策请求可以撤回或修订；正式决策行为一旦发生并形成历史承诺，就不得覆盖、删除或原地修改。

后续变化只能追加新的决策：

```text
Decision D1
  -> Revoked By Decision D2

Decision D1
  -> Superseded By Decision D3
```

新决策必须引用旧决策、变化原因、新依据、新权威和新证据。

## DM-14 错误决策必须通过新历史纠正

系统必须区分三种错误：

### 记录错误

决策行为正确发生，但记录存在抄写、编码或引用错误。只能追加 `Correction Record`，原记录不得消失。

### 裁决错误

决策当时合法，但后来被认为不合适。必须由新的撤销或取代决策改变未来状态，原决策仍是合法历史。

### 合法性错误

决策发生时缺少适用权威、可受理依据或必要证据。该行为只形成 `Illegal Decision Attempt`，不得产生目标正式事实。

若合法性错误后来才被发现，必须通过独立失效裁决追加 `Decision Invalidated`，并沿依赖关系传播下游失效；不得静默删除原记录。

制度升级不得追溯性地把旧制度下合法作出的决策变成非法。

## DM-15 决策必须显式声明作用范围

每项决策必须绑定：

```text
Decision Type
Decision Object
Object Version
Eligible Basis
Applicable Primary Authority Grant
Decision Maker
Decision Outcome
Decision Evidence
Decision Time
Decision Rule or Institution Version
Affected State Transition
```

任何字段缺失都不得依靠 Agent 推测补齐。

## DM-16 决策结果与执行必须分离

决策可以建立“允许发布”或“选择某策略”的正式事实，但执行发布、生成、重试或冻结写入仍是独立行为。

```text
Decision Result != Execution Completed
```

决策结果必须被后续执行显式引用；执行失败不能反向抹除决策曾经作出，决策成功也不能证明执行已经完成。

## DM-17 每类决策必须定义专属依据和权威

候选决策类型及最低边界：

| 决策类型 | 可受理依据 | 主要权威 | 可能结果 |
|---|---|---|---|
| `Selection Decision` | 候选资产、比较记录、符合或偏差记录 | 选择权威 | 选择、拒绝、撤销 |
| `Acceptance Decision` | 符合记录、偏差、评审证据 | 验收权威 | 接受、拒绝、等待人工 |
| `Publication Decision` | 已验证时间线及发布证据 | 发布权威 | 允许、拒绝、暂停发布 |
| `Override Decision` | 既有正式事实、覆盖理由及风险证据 | 覆盖权威 | 覆盖、拒绝、暂停 |
| `Policy Selection Decision` | 偏差、诊断、候选策略及预算 | 策略选择权威 | 选择、拒绝、终止 |
| `Institution Review Decision` | 制度提案及审查证据 | 制度审查权威 | 批准、拒绝、退回 |
| `Institution Freeze Decision` | 已批准提案、兼容性和迁移证据 | 制度冻结权威 | 冻结、拒绝、暂停 |

该表只定义候选类型边界，不预先冻结领域字段。

## 决策对象权威操作矩阵

| 操作 | 候选规则 |
|---|---|
| `Create` | 有权主体针对可受理依据实施决策行为并建立不可变记录 |
| `Modify` | 禁止修改已提交决策；提交前对象只是请求或草案，不是决策 |
| `Observe` | 允许授权审计者读取决策及其引用链 |
| `Verify` | 独立检查合法性与记录完整性，不验证价值判断唯一正确 |
| `Approve` | 只有决策类型和主要权威允许时，才能产生批准结果 |
| `Reject` | 只有决策类型和主要权威允许时，才能产生拒绝结果 |
| `Delete` | 禁止删除历史承诺后的决策记录 |
| `Supersede` | 只能由新的合法决策显式取代，并保留旧决策 |

## 决策成立条件

一项决策只有同时满足以下条件才具有制度效力：

- 引用一个明确决策类型；
- 引用一个明确对象及版本；
- 引用制度允许的可受理依据；
- 引用一个主要适用权威及版本；
- 决策者身份处于该权威授权范围内；
- 决策行为可被观察并拥有决策证据；
- 明确声明结果和状态迁移；
- 引用适用制度或决策规则版本；
- 不修改观察现实、历史证据或既有决策；
- 不把后续执行伪装成已经完成；
- 能够由后来者重新审计。

## 非法状态候选

以下情况应被正式冻结为非法：

- 只有权威但没有实际决策就迁移状态；
- 没有适用权威却建立正式事实；
- 决策没有可受理依据；
- 一个决策实例拼接多个主要权威；
- 用数据库字段或界面状态代替决策行为；
- 让证据、比较、诊断或策略直接代替决策；
- 决策者自行证明决策合法；
- 决策直接执行其授权的行动；
- 拒绝时不保存拒绝决策；
- 修改、覆盖或删除已提交决策；
- 用当前制度重新判定旧制度下合法历史；
- 决策记录依赖另一项无限上溯的自我确认决策；
- 缺少对象、依据、权威、结果、时间或证据时依靠推测补齐。

## 与现有原则的关系

本提案若未来冻结，至少需要建立以下正式关系：

| 现有原则 | 候选关系 |
|---|---|
| `A-01` | 保留并扩展：正式事实需要可受理依据与决策证据 |
| `A-03` | 修订：区分角色能力、决策权威和执行权威 |
| `A-06` | 保留：决策不得验证自己 |
| `A-07` | 澄清：历史由合法决策产生的权威迁移建立 |
| `A-08` | 保留：历史承诺后的决策不可修改 |
| `P-01` | 收窄：策略只控制未来运行时执行，不垄断所有裁决 |
| `P-04` | 澄清：策略必须通过策略选择决策建立 |
| `EV-07` | 扩展：决策行为和决策结果都必须具有适用证据 |
| `EV-14` | 澄清：加入可受理依据，并避免决策成立递归 |
| `I-09` | 保留：修订必须通过新版本而不是覆盖旧制度 |
| `I-10` | 保留：新制度不得追溯否定旧制度合法历史 |

## 未决问题

本提案在以下问题解决前不得进入冻结审查：

1. `Eligible Basis` 的资格由哪个模型统一定义？
2. `Registered Observation Record` 是否足以成为依据，还是必须先经过证据资格审查？
3. 决策合法性检查是派生计算、资格记录还是另一类正式裁决？
4. 多权威业务要求应采用多个决策还是组合权威对象？
5. `Decision Invalidated` 由谁裁决，如何传播下游失效？
6. `NO_ACTION` 是否应建立独立正式事实，还是只保存决策历史？
7. 人工创意裁决的决策证据最低要求是什么？
8. 制度冻结决策是否需要比普通决策更高的审查与兼容性门槛？

## 审查准入问题

正式审查必须逐项回答：

```text
Decision 是什么？
Decision 改变什么？
Decision 不能改变什么？
Decision 与 Authority、Policy、Evidence 的边界是什么？
Decision 是否必然创建状态迁移？
Decision 可以拒绝创建事实吗？
Decision 能否被撤回，还是只能被后续 Decision 取代？
一个 Decision 是否只能拥有一个主要 Authority？
Decision 的合法依据有哪些类型？
Decision 错误时如何纠正而不改写历史？
```

本草案已经给出候选答案，但只有制度审查能够确认或推翻。

## 建议后续顺序

```text
CR-0002 Decision Model Review
  -> Reality Layer Clarification
  -> Comparison and Conformance Model
  -> Evidence Qualification Boundary
  -> Authority Operation Matrix Amendment
  -> Policy Scope Amendment
  -> Existing Principle Replacement Map
  -> Constitution Consistency Review R3
```

## 当前裁决

```text
Proposal Completeness: PASS
Single Purpose: PASS
Authority Separation: PASS_WITH_BLOCKERS
Evidence Separation: PASS_WITH_BLOCKERS
History Preservation: PASS
Non-recursive Foundation: PASS_WITH_BLOCKERS
Freeze Readiness: FAIL
```

建议动作：提交 `CR-0002` 进行独立审查。在获得正式冻结以前，不创建 `foundation/07_Decision.md`，也不修改 `IF-0001` 至 `IF-0007`。
