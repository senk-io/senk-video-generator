# 决策模型宪法单一候选

## 候选信息

```text
Proposal ID: CR-0002-CONSTITUTION-CANDIDATE
Title: Decision Model Constitution Candidate
Status: CONSISTENCY_REVIEW_REQUIRED
Authority: NONE
Executable: NO
Candidate Form: SINGLE_CONSOLIDATED_MODEL
Consolidates: CR-0002-R2 + CR-0002-R3 + CR-0002-R4 + CR-0002-R5
Consolidation Basis: CR-0002-R5-FINAL-COMPOSITE-REVIEW
Independent Consistency Review Required: YES
Post-consolidation Semantic Diff Required: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0003 Constitution Candidate R2
```

> 本文件是 `CR-0002` 决策模型的单一候选，不是冻结制度。它没有运行时权威，不能创建决策事实、登记记录、状态迁移、投影发布或冻结决定，也不覆盖 R2 至 R5 及其审查历史。

## 候选范围

本候选只定义跨领域决策模型的不变量与相邻接口：

```text
Decision Act and Decision Fact
Decision Attempt and Candidate Record
External Qualification and Authority Applicability Consumption
Derived Record Registration Authority
Deterministic Admissibility
Protected Decision Fact Commit
Non-application Proof and Commit Resolution
Resolution Projection
Composite Requirement and Exemption
Legality Review and Invalidation
Representation Correction and Read Projection
Target Transition Boundary
```

本候选不实现：

- 全局来源注册表；
- 全局资格类型全集；
- 权威授予和撤销生命周期实现；
- 通用提交、事务或依赖闭包算法；
- 具体领域决策类型；
- 提供者专属实现；
- 运行时注册表、账本或投影服务；
- 制度冻结程序或冻结权威。

## 核心定义

> 决策是一个适用主要权威在合格依据上被实际行使的明确裁决。该行为只有在外部资格与权威适用性、确定性准入和受保护权威写入全部成立后，才能形成不可变决策事实。决策事实可以满足目标迁移前置条件，但不能自行证明目标迁移已经发生。

```text
Registered Basis Qualification Resolution
+ Registered Authority Applicability Resolution
+ Observable Decision Act
+ Decision Evidence
-> Decision Attempt Record
-> Candidate Decision Record
-> Registered Admissibility Record = ADMISSIBLE
-> Protected Authoritative Decision Write
-> Authoritative Decision Record
-> Decision Fact

Decision Fact
+ Target Transition Preconditions
+ Independent Target Commit
-> Target Formal State Transition
```

## 一、统一类型边界

| 节点 | 类型 | 唯一目的 | 权威或逻辑边界 |
|---|---|---|---|
| `Decision Model` | 基础层制度模型 | 定义决策不变量与接口 | 冻结制度 |
| `Decision Request` | 候选请求 | 声明希望裁决的对象与迁移 | 请求边界 |
| `Decision Maker` | 行为角色 | 实际行使一个主要决策权威 | 无记录所有权 |
| `Decision Act` | 现实事件 | 表达一次实际裁决行为 | 现实层 |
| `Decision Attempt Record` | 不可变尝试记录 | 保存行为输入和当时观察 | 决策尝试账本 |
| `Candidate Decision Record` | 候选值对象 | 保存尚未取得事实地位的裁决内容 | 候选边界 |
| `Admissibility Resolver` | 计算角色 | 计算候选准入结果 | 无事实所有权 |
| `Candidate Admissibility Record` | 候选派生记录 | 保存准入计算输出 | 准入候选边界 |
| `Registered Admissibility Record` | 不可变派生记录 | 保存内容同一的版本化准入结论 | 准入解析账本 |
| `Derived Record Registration Authority Grant` | 独立授权实例 | 登记一种精确派生记录类型 | 权威注册表 |
| `Derived Record Registration Attempt Record` | 不可变尝试记录 | 固定登记输入、候选摘要和授权 | 登记尝试账本 |
| `Registered Derived Record Envelope` | 不可变登记外壳 | 保存内容同一载荷和登记归因 | 对应派生账本 |
| `Decision Fact Commit Contract` | 版本化值对象 | 定义决策事实写集和提交语义 | 决策类型治理制度 |
| `Decision Fact Commit Authority` | 授权对象 | 允许履行指定决策事实写入 | 权威治理制度 |
| `Decision Fact Committer` | 执行角色 | 履行受保护权威写入 | 无价值裁决权 |
| `Decision Fact Commit Attempt Record` | 不可变尝试记录 | 固定权威写入输入和提交点观察 | 决策提交账本 |
| `Authoritative Decision Record` | 权威记录 | 保存唯一决策事实及归因 | 决策注册表 |
| `Decision Fact` | 正式事实 | 表达指定裁决已经合法成立 | 决策注册表权威语义 |
| `Candidate Non-application Proof Record` | 候选证明记录 | 声明指定提交尝试未被权威应用 | 未应用证明候选边界 |
| `Candidate Proof Qualification Record` | 候选派生记录 | 保存证明资格候选计算 | 证明资格候选边界 |
| `Registered Proof Qualification Record` | 不可变派生记录 | 保存证明资格三轴坐标下的结论 | 证明资格账本 |
| `Candidate Qualification Applicability Record` | 候选派生记录 | 保存证明资格适用性候选计算 | 适用性候选边界 |
| `Registered Qualification Applicability Record` | 不可变派生记录 | 保存内容同一的证明适用性结论 | 适用性账本 |
| `Proof Qualification Projection` | 可重建读面 | 表达稳定键下的当前证明资格认识 | 无提交事实权威 |
| `Decision Commit Resolver` | 计算角色 | 解析指定提交尝试结果 | 无事实所有权 |
| `Candidate Decision Commit Resolution Record` | 候选派生记录 | 保存单条三值提交解析候选 | 提交解析候选边界 |
| `Registered Decision Commit Resolution Record` | 不可变派生记录 | 保存内容同一的单条三值解析 | 提交解析账本 |
| `Resolution Projection` | 可重建派生读面 | 汇总稳定键下的四值提交认识 | 无提交或决策事实权威 |
| `Candidate Resolution Projection Record` | 候选派生记录 | 固定投影输入、闭包和结果 | 投影候选边界 |
| `Composite Requirement Contract` | 版本化值对象 | 定义目标迁移的决策槽位 | 目标类型治理制度 |
| `Candidate Composite Requirement Resolution Record` | 候选派生记录 | 保存一个组合槽位候选解析 | 组合候选边界 |
| `Registered Composite Requirement Resolution Record` | 不可变派生记录 | 保存内容同一的组合槽位解析 | 组合解析账本 |
| `Registered Exemption Basis Qualification Resolution` | 不可变外部解析 | 保存豁免依据资格 | 豁免资格治理边界 |
| `Registered Exemption Basis Applicability Resolution Record` | 不可变派生记录 | 保存豁免依据适用性 | 豁免适用性账本 |
| `Exemption Basis Applicability Projection` | 可重建读面 | 表达稳定键下的当前豁免适用性 | 无豁免事实权威 |
| `Legality Reviewer` | 审查角色 | 计算既有决策的合法性解释 | 无失效权威 |
| `Registered Legality Review Record` | 不可变派生记录 | 保存特定坐标下的审查结论 | 合法性审查账本 |
| `Registered Legality Review Temporal Normalization Record` | 不可变派生记录 | 保存旧审查时间字段的规范映射 | 时间规范化账本 |
| `Current Legality Review Projection` | 可重建读面 | 表达稳定键下的当前合法性解释 | 无失效权威 |
| `Registered Decision Correction Record` | 不可变派生记录 | 追加非语义表示更正 | 决策更正账本 |
| `Candidate Decision Read Projection` | 候选读面 | 按更正链重建当前表示 | 可删除投影边界 |
| `Published Decision Read Projection` | 派生发布快照 | 发布内容同一的可重建表示 | 无决策事实权威 |
| `Invalidation Decision` | 新决策事实 | 改变既有决策的当前适用性 | 失效权威和决策注册表 |

以下关系始终成立：

```text
Decision Act != Decision Fact
Candidate Decision Record != Authoritative Decision Record
Admissibility Resolution != Decision Fact
Registered Commit Resolution != Resolution Projection
Legality Review != Invalidation Decision
Correction Record != Decision Mutation
Projection != Formal Fact
Decision Fact != Target Formal State Transition
```

## 二、决策的单一目的与权威

### DM-C-01 决策必须来自一次实际权威行使

```text
Applicable Primary Authority Grant
-> Observable Decision Act
-> Decision Attempt Record
```

只有权威而没有实际裁决行为，不能建立决策事实。只有行为而没有适用权威，只能形成决策尝试。

### DM-C-02 决策不得吸收相邻职责

决策不得观察现实、创建证据、定义资格、授予权威、解释偏差、选择补救策略、执行目标迁移、证明价值判断客观正确或冻结自身。

### DM-C-03 一个决策实例只有一个主要权威

```text
One Decision Instance
-> One Applicable Primary Authority Grant
```

主要权威必须在决策时点同时覆盖：

```text
Decision Maker
Decision Type
Decision Object and Version
Allowed Disposition
Allowed Transition Type
Authority Effective Interval
Institution Version
```

身份、角色能力或历史成功不能替代完整作用域。

## 三、裁决倾向与请求迁移

### DM-C-04 裁决倾向独立于迁移类型

规范裁决倾向：

```text
APPROVE
REJECT
SUSPEND
NO_ACTION
```

规范请求迁移：

```text
CREATE
TRANSITION
SUPERSEDE
REVOKE
```

两者必须分别受决策类型制度约束。`REJECT` 是合法裁决倾向，不表示准入失败。

### DM-C-05 NO_ACTION 可以形成历史但不迁移目标

```text
NO_ACTION -> may form Decision Fact
NO_ACTION -/-> Target State Transition
```

没有记录不能被解释为 `NO_ACTION`。

## 四、外部资格与权威适用性消费

### DM-C-06 决策模型只消费已登记依据资格解析

`Registered Basis Qualification Resolution` 最低绑定：

```text
Resolution ID
Basis ID and Version
Decision Type
Decision Object Scope
Qualification Outcome
Effective At
As Of
Resolved At
Qualification Rule Version
Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Correction View Reference
Registration Authority Grant Reference
```

规范结果：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
```

只有 `QUALIFIED` 能支持正向准入。

### DM-C-07 决策模型只消费已登记权威适用性解析

`Registered Authority Applicability Resolution` 最低绑定：

```text
Resolution ID
Authority Grant ID and Version
Decision Maker Identity or Role
Decision Type
Decision Object and Version Scope
Allowed Dispositions
Allowed Transition Types
Applicability Outcome
Effective At
As Of
Resolved At
Authority Rule Version
Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Correction View Reference
Registration Authority Grant Reference
```

规范结果：

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

只有 `APPLICABLE` 能支持决策事实提交。

### DM-C-08 外部解析必须绑定同一决策坐标

```text
Decision Type
Decision Object ID and Version
Decision Time
Requested Transition Type
Decision Institution Version
```

对象、版本、时点、来源边界、更正视图或规则兼容性不一致时必须失败关闭。

### DM-C-09 解析计算、登记和决策准入必须分权

```text
Resolution Computation
-/-> Resolution Registration Authority
-/-> Decision Fact
```

决策准入不能临时认定依据合格、恢复权威、修改外部解析或为自身创建外部解析权威。

## 五、决策尝试、候选和稳定键

### DM-C-10 决策行为必须先形成不可变尝试记录

`Decision Attempt Record` 至少绑定：

```text
Decision Key
Decision Attempt ID
Decision Request ID and Version
Decision Maker
Primary Authority Grant Reference
Decision Type
Decision Object ID and Version
Basis Qualification Resolution References
Authority Applicability Resolution Reference
Decision Disposition
Requested Transition Type
Decision Act Observed At
Decision Evidence References
Decision Institution Version
Declared Record Digest
Recorded At
```

尝试记录只证明输入和观察已经保存，不证明决策事实成立。

### DM-C-11 Candidate Decision Record 没有正式事实地位

候选记录可以进入准入解析，但不得授权执行、满足目标迁移或作为正式决策被界面和策略消费。

### DM-C-12 决策键必须稳定且幂等

```text
One Decision Key
-> At Most One Authoritative Decision Fact
```

重复请求必须解析到既有权威结果或保持未知。撤销、取代和失效是新决策，不复用旧键。

## 六、派生记录登记权威

### DM-C-13 通用登记契约不传播具体权威

每个授权实例只能登记一个精确映射：

```text
One Candidate Record Type
-> One Registered Record Type
-> One Ledger Scope
```

一个准入登记授权不能登记提交解析、组合解析、合法性审查、更正、证明资格、豁免适用性或时间规范化记录。

未来兼容治理至少必须为以下记录分别提供独立授权实例：

```text
Registered Admissibility Record
Registered Proof Qualification Record
Registered Qualification Applicability Record
Registered Decision Commit Resolution Record
Registered Composite Requirement Resolution Record
Registered Exemption Basis Applicability Resolution Record
Registered Legality Review Record
Registered Legality Review Temporal Normalization Record
Registered Decision Correction Record
```

### DM-C-14 登记授权实例必须声明完整边界

最低字段：

```text
Registration Authority Grant ID and Version
Authority Holder Identity or Role
Candidate Record Type
Registered Record Type
Allowed Ledger ID and Namespace
Allowed Object Types and Version Scope
Allowed Outcome Types
Allowed Rule and Institution Versions
Effective From and Until
Can Change
Cannot Change
Registration Preconditions
Registration Decision Rule ID and Version
Failure Behavior
Grant Evidence References
Grant Institution Reference
```

`Can Change` 只允许追加内容同一登记外壳和归因元数据；`Cannot Change` 必须包括候选载荷、结果、理由、来源、时间、正式事实和其他账本。

### DM-C-15 登记必须先形成不可变尝试记录

`Derived Record Registration Attempt Record` 至少绑定候选 ID、类型和摘要、授权 ID 和版本、目标登记类型、作用域、规则版本、预期账本版本、证据、发起时间和尝试摘要。

登记结果：

```text
REGISTERED
DECLINED
INDETERMINATE
```

没有登记记录不能单独证明 `DECLINED`。

### DM-C-16 候选载荷与登记载荷必须内容同一

```text
Candidate Payload Digest
= Registered Payload Digest
```

登记外壳摘要可以另外包含授权、尝试、登记时间和账本版本，但登记者不得规范化、清洗、补默认值或改变候选内容。

## 七、确定性准入

### DM-C-17 准入解析只有规则计算权

解析器只能检查：

- 依据资格是否为 `QUALIFIED`；
- 权威适用性是否为 `APPLICABLE`；
- 对象、版本、时间和制度坐标是否一致；
- 裁决倾向和迁移类型是否允许；
- 决策证据是否齐备；
- 组合要求是否适用；
- 不变量和决策键唯一性是否满足。

候选结果：

```text
ADMISSIBLE
INADMISSIBLE
INDETERMINATE
```

### DM-C-18 准入结果必须失败关闭

`ADMISSIBLE` 要求所有正向输入已解析且没有冲突。

`INADMISSIBLE` 只允许由来源完备的确定性否定建立，例如已登记依据资格 `NOT_QUALIFIED`、权威适用性 `NOT_APPLICABLE`、枚举越界、不可变字段冲突或唯一键确定冲突。

来源不可用、闭包未证、规则未知、冲突、更正未决、键查询不完整或证据未决必须是 `INDETERMINATE`。

```text
Record Not Found -/-> INADMISSIBLE
```

### DM-C-19 准入候选与登记记录必须分离

`Registered Admissibility Record` 至少绑定：

```text
Decision Key
Decision Attempt ID
Candidate Decision Record Digest
Basis Qualification Resolution IDs
Authority Applicability Resolution ID
Admissibility Outcome
Outcome Reason Codes
Source Set Digest
Validity As Of
Knowledge Boundary Vector
Resolved At
Admissibility Rule Version
Decision Institution Version
Evidence References
Resolver Identity
Candidate Payload Digest
Registered Payload Digest
Registration Authority Grant Reference
Registered At
Registered Record Digest
```

```text
Registered Admissibility = ADMISSIBLE
-/-> Decision Fact
```

## 八、决策事实的权威成立

### DM-C-20 决策事实必须通过受保护权威写入成立

```text
Candidate Decision Record
+ Registered Admissibility Record = ADMISSIBLE
+ Decision Fact Commit Authority
+ Decision Fact Commit Contract
-> Protected Authoritative Decision Write
-> Authoritative Decision Record
-> Decision Fact
```

提交权威只能忠实写入已准入候选，不能改变裁决、迁移、依据、权威、决策时点、写集或目标状态。

### DM-C-21 写入前必须固定提交尝试

`Decision Fact Commit Attempt Record` 至少绑定：

```text
Decision Commit Attempt ID
Decision Key
Candidate Decision Record Digest
Registered Admissibility Record ID and Digest
Decision Fact Commit Contract ID and Version
Decision Fact Commit Authority Reference
Expected Decision Registry Version
Declared Write-set Digest
Initiated At
```

提交尝试不证明权威写入已经发生。

### DM-C-22 权威写入必须不可分割归因

同一保护边界必须建立：

```text
Authoritative Decision Record
+ Decision Key Attribution
+ Authoritative Registry Version Transition
```

权威记录至少绑定事实 ID、决策键、行为和提交尝试、候选和准入引用、决策者、主要权威、类型、对象版本、依据、裁决、迁移、决策时间、证据、制度版本、前后注册表版本、提交时间、提交权威和记录摘要。

## 九、未应用证明、资格与适用性

### DM-C-23 证明类型名称不等于合格证明

候选证明类型：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

任何类型都必须经过候选证明、资格计算、内容同一资格登记、适用性计算、内容同一适用性登记和资格投影，才能参与 `ABORTED` 解析。

### DM-C-24 候选未应用证明必须固定完整作用域

最低字段：

```text
Candidate Proof ID
Proof Type
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Decision Fact Commit Authority Grant Reference
Target Decision Registry ID
Expected Registry Version
Declared Write-set Digest
Validity As Of
Knowledge Boundary Vector
Produced At
Authoritative Source References
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Candidate Reference
Contrary Source References
Evidence References
Assembler Identity and Authority
Assembly Rule Version
Candidate Proof Payload Digest
```

组装者没有资格、适用性、登记或提交解析权威。

### DM-C-25 证明资格与适用性分别使用四值

证明资格：

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED
```

证明适用性：

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

资格和适用性必须分别计算、登记和保存冲突。旧值 `NOT_QUALIFIED`、`NOT_APPLICABLE` 没有兼容证据时只能成为未解析旧值。

`Registered Proof Qualification Record` 至少绑定：

```text
Proof Qualification Resolution ID
Candidate Proof ID and Payload Digest
Proof Type
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Qualification Outcome and Reason Codes
Validity As Of
Knowledge Boundary Vector
Resolved At
Qualification Rule ID and Version
Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Qualification Reference
Contrary Source References
Evidence References
Qualification Resolver Identity
Qualification Registration Authority Grant Reference
Candidate Qualification Payload Digest
Registered Qualification Payload Digest
Registered At
Registered Qualification Record Digest
```

`Registered Qualification Applicability Record` 至少绑定：

```text
Qualification Applicability Resolution ID
Registered Proof Qualification Record ID and Digest
Candidate Proof ID
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Applicability Outcome and Reason Codes
Validity As Of
Knowledge Boundary Vector
Resolved At
Applicability Rule ID and Version
Institution Version
Source Applicability and Correction Record References
Source Set Digest
Coverage or Completeness Proof Reference
Contrary Source References
Evidence References
Applicability Resolver Identity
Applicability Registration Authority Grant Reference
Candidate Applicability Payload Digest
Registered Applicability Payload Digest
Registered At
Registered Applicability Record Digest
```

### DM-C-26 Proof Qualification Projection 必须拥有稳定身份

作用域模式严格二选一：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

稳定键至少包含候选证明、提交尝试、决策键、作用域模式、精确契约或不可变兼容域快照、有效时点、认识向量、视图模式、资格规则兼容域、来源边界、更正视图和投影规则版本。

资格兼容域快照至少绑定域 ID 和版本、精确成员契约版本、成员摘要、成员规则版本、资格语义兼容记录、治理制度和冻结引用、有效时点、认识向量及快照摘要。成员变化必须产生新快照和新投影键。

投影必须分别保存资格结果、聚合适用性、资格冲突、适用性冲突、纳入与排除记录、闭包和证据。

### DM-C-27 ABORTED 需要完整正向证明链

```text
Historical Registered Proof Qualification = QUALIFIED
+ Projected Qualification = QUALIFIED
+ Aggregate Applicability = APPLICABLE
+ Exact Projection Key
+ Allowed Projection View Mode
+ Matching Proof, Attempt, Decision Key and Contract Scope
+ Matching Write-set and Temporal Coordinate
+ Registered Closure Completeness = COMPLETE
+ Complete Applicable Source Set
+ Underlying Records and Evidence
+ No Qualification Conflict
+ No Applicability Conflict
+ No Unresolved Contrary Source
-> Candidate Commit Resolution may be ABORTED
```

任一条件缺失时只能是 `INDETERMINATE`。完备性证明也必须具有外部资格和适用性。

## 十、单条提交解析与解析投影

### DM-C-28 单条已登记提交解析保持三值

```text
COMMITTED
ABORTED
INDETERMINATE
```

`COMMITTED` 必须由权威决策记录和唯一键归因证明；`ABORTED` 必须由 `DM-C-27` 证明；无法证明前两者时为 `INDETERMINATE`。

单条解析不得使用 `CONFLICTED`，也不得创建、撤销或修改决策事实。

### DM-C-29 提交解析必须保存追加谱系

已登记解析至少绑定：

```text
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Commit Outcome
Authoritative Decision Record Reference if applicable
Qualified Non-application Proof Reference if applicable
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Resolved At
Resolution Rule ID and Version
Evidence References
Resolver Identity
Candidate Resolution Record ID and Payload Digest
Registered Payload Digest and Record Digest
Registration Authority Grant Reference
Resolution Ledger Position
Prior Resolution Record References
Resolution Lineage ID
Resolution Relationship
Validity As Of
Knowledge Boundary Vector
Source Applicability Change Inputs
Qualification Correction Inputs
Registered At
```

规范关系：

```text
INITIAL
REFINES
REAFFIRMS
CONFLICTS_WITH
```

相反终局不能通过 `REFINES` 互相覆盖。

### DM-C-30 Resolution Projection 是唯一规范投影类型

```text
Normative Type = Resolution Projection
```

`Current Commit Resolution Projection` 只在 `CURRENT_RESTATEMENT_VIEW` 下作为显示别名，不进入规范类型、摘要、授权或持久化接口。

投影结果：

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

### DM-C-31 Resolution Projection Key 必须完整稳定

作用域模式严格二选一：

```text
EXACT_COMMIT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

稳定键至少包含：

```text
Decision Commit Attempt ID
Decision Key
Resolution Projection Scope Mode
Exact Commit Contract ID and Version or NOT_APPLICABLE
Resolution Compatibility Domain Snapshot or NOT_APPLICABLE
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Source Set Boundary
Correction View Reference
Resolution Projection Rule Version
```

`Resolution Compatibility Domain Snapshot` 至少绑定：

```text
Compatibility Domain ID and Version
Compatibility Semantic Domain = COMMIT_RESOLUTION
Exact Member Commit Contract IDs and Versions
Membership Digest and Rule Version
Resolution Semantic Compatibility Record References
Field Presence Compatibility References
Temporal Compatibility Rule Version
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
Snapshot Digest
```

成员变化必须产生新快照、摘要和投影键。缺少兼容证据或可验证冻结引用时兼容性保持未知。

字段存在性采用 `VALUE | NOT_APPLICABLE | UNRESOLVED`。任何必需字段未解析时不得形成终局投影。

### DM-C-32 终局投影必须消费已登记完整闭包

`Dependency Closure Reference` 至少绑定已登记闭包、已登记完整性、投影键、根解析、必需边、注册表作用域、时间坐标、视图模式、闭包摘要、规则版本和证据。

```text
Registered Closure Completeness = COMPLETE
```

是 `COMMITTED`、`ABORTED` 或 `CONFLICTED` 投影的必要条件。`INCOMPLETE`、未知、开放世界缺失或只有来源摘要时必须为 `INDETERMINATE`。

### DM-C-33 提交投影使用冲突保留真值表

```text
Applicable comparable COMMITTED only -> COMMITTED
Applicable comparable ABORTED only -> ABORTED
Applicable comparable COMMITTED + ABORTED -> CONFLICTED
Applicable INDETERMINATE only -> INDETERMINATE
No applicable registered resolution -> INDETERMINATE
```

冲突集必须保存双方全部解析、摘要、谱系、来源适用性、证据、兼容性和闭包引用。不得以新旧、数量或身份选择终局。

### DM-C-34 投影构建者只有计算权

`Candidate Resolution Projection Record` 至少绑定投影键和结果、纳入与排除解析、制度排除依据、谱系、冲突集、闭包、来源快照和摘要、更正、兼容性、证据、构建者和授权、规则版本、产生时间和候选摘要。

构建者不能创建解析、闭包、排除规则、决策事实、发布或策略授权。发布必须消费独立变化审计和发布外壳接口。

### DM-C-35 投影结果不授权行动或事实

```text
Resolution Projection = COMMITTED -/-> create Decision Fact
Resolution Projection = ABORTED -/-> Retry
Resolution Projection = INDETERMINATE -/-> Cancel or Replace
Resolution Projection = CONFLICTED -/-> Select Preferred Terminal
```

## 十一、决策事实与目标迁移

### DM-C-36 决策事实先于目标迁移

```text
Decision Fact
+ Transition Preconditions
+ Target Commit Contract
+ Target Commit Authority
-> Target Formal State Transition
```

决策模型不创建或解释目标提交结果。

### DM-C-37 目标状态不能反推决策事实

界面、数据库字段、导出物或目标当前状态不能证明决策曾合法成立。必须读取权威决策记录和完整引用链。

### DM-C-38 目标执行失败不能抹除决策事实

```text
Decision Fact = APPROVE
Target Commit = ABORTED
```

可以同时成立。执行失败只影响目标迁移。

## 十二、组合要求与豁免

### DM-C-39 多权威要求必须保持多个决策事实

多个权威不得拼成一个没有主要责任主体的联合决策。

### DM-C-40 一个组合解析只解析一个要求槽位

`Composite Requirement Contract` 至少定义：

```text
Requirement Contract ID and Version
Target Transition Type
Requirement Slot ID
Required Decision Type and Disposition
Required Object and Version Relation
Requirement Mode
Exemption Conditions
Evidence Requirements
Failure Behavior
```

模式：

```text
REQUIRED
CONDITIONALLY_EXEMPTIBLE
```

结果：

```text
SATISFIED
NOT_SATISFIED
EXEMPT
INDETERMINATE
```

### DM-C-41 组合候选与登记记录必须完整且内容同一

候选记录至少绑定：

```text
Composite Resolution ID
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Requirement Mode
Required Decision Type and Disposition
Required Object and Version Relation
Referenced Decision Fact IDs and Digests
Registered Exemption Qualification Resolution IDs
Registered Exemption Applicability Resolution IDs
Resolution Outcome and Reason Codes
Validity As Of
Knowledge Boundary Vector
Resolved At
Rule and Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Prior Resolution Record References
Resolution Lineage ID
Resolver Identity
Candidate Payload Digest
```

登记外壳必须满足候选与登记载荷摘要相等。登记者不能修改槽位、结果、依据、来源或时间。

### DM-C-42 豁免资格和适用性必须分离

```text
Registered Exemption Qualification = QUALIFIED
-/-> Current Applicability = APPLICABLE
```

豁免适用性使用 `APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED`，拥有稳定键、候选记录、独立内容同一登记、追加谱系和可重建投影。

豁免适用性稳定键至少包含资格解析和摘要、豁免依据、要求契约、目标对象版本、目标迁移、槽位、冻结豁免规则、有效时点、认识向量、视图模式、来源边界、更正视图和适用性规则版本。

候选适用性记录至少绑定：

```text
Exemption Applicability Resolution ID
Exemption Basis Applicability Key and Digest
Registered Exemption Qualification Resolution ID and Digest
Exemption Basis ID and Version
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Frozen Exemption Rule ID and Version
Applicability Outcome and Reason Codes
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Resolved At
Applicability Rule ID and Version
Institution Version
Source Applicability Input References
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Correction View Reference
Contrary Source References
Evidence References
Resolver Identity and Authority Grant Reference
Prior Applicability Resolution References
Applicability Lineage ID
Candidate Payload Digest
```

登记外壳必须绑定独立登记授权、候选和登记载荷摘要、登记时间、账本版本、证据和登记记录摘要，并满足内容同一。

### DM-C-43 EXEMPT 需要完整正向链

```text
Requirement Mode = CONDITIONALLY_EXEMPTIBLE
+ Frozen Exemption Rule applicable
+ Registered Exemption Qualification = QUALIFIED
+ Exact Exemption Applicability Projection Key
+ Exemption Applicability Projection = APPLICABLE
+ Matching Slot, Object, Version, Transition and Temporal Coordinate
+ Complete Applicable Source Set
+ Qualified and Applicable Coverage Proof
+ No Qualification Conflict
+ No Applicability Conflict
+ No Unresolved Contrary Source
-> Composite Resolution may be EXEMPT
```

缺少决策记录、未观察到条件或来源不完整都不能建立 `EXEMPT`。

### DM-C-44 最终决策必须是独立决策

若目标制度要求最终价值裁决，它必须具有独立决策类型、一个主要权威、自己的行为、证据、准入和受保护写入。子决策只作为制度允许的依据，不自动合成最终判断。

## 十三、事后合法性审查

### DM-C-45 合法性审查是派生解释

```text
Historical Decision Record
+ Versioned Review Sources
+ Legality Review Contract
-> Candidate Legality Review Record
```

结果：

```text
COMPLIANT
NON_COMPLIANT
INDETERMINATE
```

任何结果都不能直接修改决策事实或目标状态。

### DM-C-46 审查候选与登记必须内容同一且保存谱系

登记审查记录至少绑定：

```text
Reviewed Decision Fact ID
Review Outcome and Reason Codes
Original Admissibility Rule Version
Original Institution Version
Review Rule Version
Review Institution Version
Original Source View Reference
Current Correction View Reference
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Candidate Review Record ID and Payload Digest
Reviewer Identity
Review Authority Grant Reference
Registration Authority Grant Reference
Registered Review Payload Digest
Registered Review Record Digest
Registered At
Prior Review Record References
Review Lineage ID
Review Relationship
```

关系可以表达初始、补充、在新认识下重述、当前投影取代或不可比较并列，但不得覆盖历史审查。

### DM-C-47 合法性审查使用五个不可互换时间字段

```text
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Review Act Observed At
Review Record Produced At
Review Registered At
```

候选载荷绑定前四项；`Review Registered At` 只属于内容同一登记外壳，候选不得预测未来登记时间。

### DM-C-48 旧审查时间必须经过版本化规范化

旧字段只能通过 `Legality Review Temporal Mapping Contract` 逐字段得到：

```text
EXACT_MAPPED
NOT_APPLICABLE
UNRESOLVED
```

最低映射规则：

```text
Original Decision Time
-> component of Reviewed Historical Validity Coordinate if declared by source contract

Original Effective Coordinate
-> Reviewed Historical Validity Coordinate if semantically exact

Review Effective At
-> Reviewed Historical Validity Coordinate only under explicit validity semantics

Review As Of
-> Review Knowledge Boundary Vector only when exact registry boundaries are reconstructable

Reviewed At
-> Review Act Observed At only when it records the review act time

Registered At
-> Review Registered At only when attributed by the content-identical review registration envelope
```

禁止把 `Reviewed At` 默认映射为认识边界或记录产生时间，也禁止用一个 `Review As Of` 时间戳代替完整认识边界向量。

映射必须形成候选记录和独立内容同一登记。多个旧字段映射到同一目标时必须一致；冲突或缺少完整注册表边界时为 `UNRESOLVED`。

### DM-C-49 当前合法性投影必须拥有稳定键

稳定键至少包含被审查决策事实、审查模式、历史有效坐标、认识向量、原制度版本、审查规则兼容域、来源边界、更正视图和投影规则版本。

投影保存纳入与排除审查、谱系、结果、理由、来源、完备性、冲突、产生时间和构建者。必需时间未解析时必须为 `INDETERMINATE`。

### DM-C-50 审查结论只能支持失效请求

```text
Registered Legality Review = NON_COMPLIANT
-> may support Invalidation Decision Request
-/-> Invalidation Decision Fact
-/-> Dependency Propagation
```

## 十四、失效与传播

### DM-C-51 失效必须由新决策事实建立

失效决策必须拥有独立决策键、类型、目标决策事实、合格依据、适用失效权威、决策行为和证据、裁决、请求迁移、准入和受保护写入。

### DM-C-52 失效改变当前适用性但不删除历史

成功失效可以建立指定坐标下的 `Decision Applicability = INVALIDATED`，但不得删除原行为、证据、权威记录或历史查询。

### DM-C-53 传播只消费已提交失效事实

```text
Committed Invalidation Decision Fact
+ Frozen Dependency Propagation Rule
+ Propagation Authority
-> Dependency Invalidation Execution
```

候选审查、已登记审查、模型怀疑或来源缺失不能直接传播正式失效。

## 十五、记录更正与读投影

### DM-C-54 更正只修复表示缺陷

允许更正编码、转录、引用表示和非语义元数据错误。

不得改变决策行为、决策者、主要权威、类型、对象版本、裁决、迁移、决策时间、证据含义或事实身份。语义变化必须使用新撤销、取代或失效决策。

### DM-C-55 更正必须经过资格和内容同一登记

更正记录至少绑定候选摘要、原记录和摘要、字段、原值、新值、原因、证据、资格解析、规则版本、历史坐标、认识时间、适用时间、认识向量、前序更正、谱系、关系、登记授权、登记时间和记录摘要。

### DM-C-56 更正必须使用双时间追加语义

```text
Corrected Historical Coordinate
Correction Known At
Correction Applicable From
Knowledge Boundary Vector
Projection Produced At
```

后来更正可以进入当前重述，但不能静默进入历史当时认识。

### DM-C-57 当前决策读投影必须稳定、可删除和可重建

投影键至少包含原决策记录和摘要、视图模式、历史坐标、认识向量、更正规则兼容域、来源边界和投影规则版本。

投影构建和发布分别授权。冲突更正、资格不明、来源不完整或规则不兼容时投影为 `INDETERMINATE`。发布载荷必须与候选投影内容同一。

### DM-C-58 更正和投影不改变事实成立状态

```text
Correction or Read Projection
-/-> create Decision Fact
-/-> revoke Decision Fact
-/-> change Decision Disposition
-/-> authorize Target Transition
```

## 十六、人工创意裁决

### DM-C-59 人工裁决要求可审计但不要求客观审美证明

最低证据包括决策者身份、适用权威解析、对象版本、候选集、合格依据、裁决、请求迁移、决策时间、真实理由和证据。

准入只验证记录、资格和权威，不证明审美选择唯一正确。

## 十七、决策类型治理契约

### DM-C-60 每种决策类型必须定义专属契约

```text
Decision Type
Allowed Object Types
Allowed Basis Types
Basis Qualification Contract
Applicable Primary Authority Type
Authority Applicability Contract
Allowed Dispositions
Allowed Transition Types
Composite Requirement Contract
Exemption Qualification and Applicability Contract
Decision Fact Commit Contract
Commit Resolution and Projection Contract
Target Transition Preconditions
Target Commit Interface
Evidence Requirements
Correction Contract
Legality Review and Temporal Mapping Contract
Invalidation Contract
Failure Behavior
```

### DM-C-61 制度冻结决策采用更高门槛

制度冻结决策至少消费已批准提案、兼容性审查、迁移计划、独立审查证据、适用冻结权威、冻结行为和证据、准入解析及成功制度提交。

本条不使本候选取得冻结权威，也不替代 `IF-0007`。

## 十八、规范因果路径

### 决策事实成立路径

```text
Decision Request
  -> Registered Basis Qualification Resolution
  -> Registered Authority Applicability Resolution
  -> Observable Decision Act
  -> Decision Attempt Record
  -> Candidate Decision Record
  -> Candidate Admissibility Record
  -> Registered Admissibility Record
       -> INADMISSIBLE
            -> NON_ADMISSIBLE_DECISION_ATTEMPT
            -> No Decision Fact
       -> INDETERMINATE
            -> Fail Closed
       -> ADMISSIBLE
            -> Decision Fact Commit Attempt Record
            -> Protected Authoritative Decision Write Attempt
                 -> Applied
                      -> Authoritative Decision Record + Decision Key Attribution
                      -> Decision Fact
                 -> Not Applied or Application Unknown
                      -> No Decision Fact Inference
            -> Independent Commit Resolution over authoritative sources
                 -> COMMITTED -> confirms existing Authoritative Decision Record and Decision Fact
                 -> ABORTED -> qualified applicable complete proof of non-application for matched attempt
                 -> INDETERMINATE -> Decision Fact Existence Unresolved at Coordinate
```

### 提交解析投影路径

```text
Registered Decision Commit Resolution Records
+ Source Applicability
+ Correction View
+ Compatibility Domain if applicable
+ Registered Dependency Closure
+ Registered Closure Completeness = COMPLETE
+ Resolution Projection Key
-> Candidate Resolution Projection Record
     -> COMMITTED
     -> ABORTED
     -> INDETERMINATE
     -> CONFLICTED
```

### 目标迁移路径

```text
Decision Fact
  -> Composite Requirement Resolution if applicable
  -> Target Transition Preconditions
       -> NOT_MET -> No Target Transition
       -> INDETERMINATE -> Fail Closed
       -> MET -> Independent Target Commit
            -> Target Formal State Transition
```

### 合法性和失效路径

```text
Authoritative Decision Record
  -> Versioned Legality Review
  -> Registered Legality Review Record
       -> COMPLIANT -> No automatic state change
       -> INDETERMINATE -> Fail Closed
       -> NON_COMPLIANT -> may support Invalidation Decision Request
            -> New Invalidation Decision Fact
            -> Independent Applicability Commit
            -> Dependency Propagation under frozen rule
```

### 更正路径

```text
Original Decision Record
  -> Correction Request and Evidence
  -> Correction Qualification
  -> Registered Decision Correction Record
  -> Candidate Decision Read Projection
  -> Content-identical Published Read Projection if authorized

Correction -/-> Original Record Mutation
Correction -/-> Decision Semantic Change
```

## 十九、操作矩阵

| 操作 | 规范边界 |
|---|---|
| `Request` | 创建候选请求，不产生决策事实 |
| `Act` | 实际行使裁决，不自动证明准入或提交 |
| `Resolve Admissibility` | 计算候选准入，无事实登记权 |
| `Register Derived Record` | 按逐类型授权登记内容同一载荷 |
| `Commit Decision Fact` | 在受保护权威边界写入已准入决策 |
| `Resolve Commit` | 对单次提交尝试建立三值派生解析 |
| `Project Resolutions` | 在完整闭包下建立四值可重建认识 |
| `Observe` | 读取权威记录和完整引用链 |
| `Resolve Composite Requirement` | 解析一个槽位，不合并权威 |
| `Review Legality` | 追加审查，不修改原决策 |
| `Correct Representation` | 追加非语义更正 |
| `Revoke` | 通过新决策改变未来适用状态 |
| `Supersede` | 通过新决策取代当前适用决策并保留历史 |
| `Invalidate` | 通过新失效决策改变当前适用性 |
| `Delete` | 禁止删除已提交事实、尝试、证据、解析、审查和更正 |

## 二十、非法状态候选

未来冻结时必须明确禁止：

- 准入结果直接创建决策事实；
- 候选记录被当作正式决策；
- 一个授权实例登记多种派生记录；
- 登记者修改候选载荷；
- 来源缺失被解释为不合格、不适用、`ABORTED` 或 `EXEMPT`；
- 证明类型名称直接支持 `ABORTED`；
- 完备性证明自证完整；
- 把 `CONFLICTED` 折叠为未知或任意终局；
- 一个决策实例拼接多个主要权威；
- 缺少子决策时默认组合槽位豁免；
- 最终决策继承多个子决策权威；
- 合法性审查直接修改决策事实或传播失效；
- 当前知识无坐标地追溯否定历史；
- 把 `Reviewed At` 当作认识边界；
- 后来更正伪装成历史当时认识；
- `Current Commit Resolution Projection` 被用作规范类型；
- 投影省略视图模式或契约作用域；
- 来源摘要代替已登记闭包完整性；
- 闭包非 `COMPLETE` 时建立终局投影；
- 投影结果创建决策事实或授权行动；
- `INADMISSIBLE` 被解释为裁决倾向 `REJECT`；
- 提交解析未知被写入决策事实生命周期；
- 覆盖、删除或静默替换历史记录与证据。

发现任一状态必须失败关闭并保存已有历史、冲突和证据。

## 二十一、与相邻模型的职责关系

```text
Authority Model
  -> grants decision, registration and projection authorities

Evidence Model
  -> establishes evidence trust requirements

Qualification Governance
  -> establishes basis, proof and exemption qualifications

Authority Applicability Governance
  -> establishes authority and source applicability

Decision Model
  -> establishes decision fact, review and projection semantic contracts

Commit Model
  -> implements compatible protected writes, closure and projection interfaces

Dependency Governance
  -> builds closure and propagates committed applicability changes

Institution Model
  -> governs proposal, review, freeze and evolution
```

相邻模型可以实现接口，不能反向扩大决策职责。候选依赖缺失时，决策模型不能自行吞并来源、资格、提交或传播治理。

## 二十二、合并来源映射

| 规范部分 | 主要来源 |
|---|---|
| 决策目的、权威、尝试、准入、事实写入、目标边界 | `R2` |
| 派生登记权威、内容同一、证明链、组合记录、审查和更正谱系、失败术语 | `R3` |
| 四值证明接口、豁免适用性、合法性时间规范化 | `R4` |
| 规范提交投影、冲突、作用域、闭包和谱系兼容 | `R5` |

本表只保存来源谱系，不使旧覆盖层继续充当规范定义。

## 二十三、冻结前外部依赖

```text
Post-consolidation Semantic Diff Review
Independent Single Candidate Consistency Review
Frozen or compatible Source Registry Interface
Frozen or compatible Qualification Governance
Frozen or compatible Authority Applicability Governance
Frozen or compatible Derived Record Registration Governance
Frozen or compatible Proof and Exemption Applicability Governance
Frozen or compatible Temporal Mapping Governance
Frozen or compatible Dependency Closure Governance
Frozen or compatible Projection Audit and Publication Interface
Frozen or compatible Institution Registry and Freeze Reference Support
Compatible Protected Write Implementation Evidence
Repeated and Stable Runtime Evidence
Cross-provider Evidence
Cross-project and Cross-domain Evidence
Applicable Freeze Authority
Independent Freeze Review
Freeze Decision
Successful Institution Commit
```

## 二十四、候选自检状态

```text
Single Consolidated Model: YES
Proposal Completeness: PASS
Single Purpose: PASS
Known Review Finding Mapping: COMPLETE
Duplicate Normative Type Definitions: NOT_OBSERVED
Legacy Enum Removal: COMPLETE
Legacy Temporal Field Normalization: COMPLETE
Resolution Projection Normalization: COMPLETE
Authority Separation: DEFINED
Evidence and History Preservation: DEFINED
Provider Independence: PASS
Domain Portability: PASS
Post-consolidation Semantic Diff Review: REQUIRED
Independent Consistency Review: REQUIRED
Model-level Blockers: NOT_EVALUATED
Freeze Dependency Readiness: NOT_EVALUATED
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: CONSISTENCY_REVIEW_REQUIRED
```

这些自检不是独立审查结论。

## 当前决定

1. 保留 R2 至 R5 及其审查记录作为不可覆盖历史；
2. 将本文件登记为 `CR-0002-CONSTITUTION-CANDIDATE` 单一候选；
3. 不修改 `IF-0001` 至 `IF-0007`；
4. 不创建 `foundation/07_Decision.md`；
5. 不创建运行时权威、注册表、记录、投影或决策事实；
6. 不创建冻结标识、冻结权威或冻结决定；
7. 下一步执行合并后语义差异审查；
8. 语义差异闭合后执行独立单一候选一致性审查；
9. 独立一致性通过后重新执行冻结依赖准备度审计；
10. 在全部 `IF-0007` 条件满足以前，本候选不可执行且没有制度权威。
