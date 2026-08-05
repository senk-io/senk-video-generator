# 决策模型提案第二修订版

## 提案信息

```text
Proposal ID: CR-0002-R2
Title: Decision Model
Status: DRAFT
Authority: NONE
Executable: NO
Revises: CR-0002-R1
Review Basis: CR-0002-R1-LOCAL-REVIEW
Independent Review Required: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Derived From: CR-0002-R1 Independent Review
```

> 本文件是待独立审查的第二修订提案，不是冻结制度。它不能创建决策权威、登记运行时决策事实、授权目标迁移、覆盖 `CR-0002-R1` 的历史，或使任何相邻模型自动冻结。

## 修订范围

本版保留 `CR-0002-R1` 已成立的单一目的、对象分离、权威分离和历史保留，只处理本地独立审查确认的五项阻断：

1. 为决策事实建立独立的候选、准入、登记和受保护写入边界；
2. 为合格依据与适用权威解析建立版本化消费契约；
3. 闭合组合决策要求、豁免和最终成立语义；
4. 分离事后合法性审查、失效决策、历史解释和依赖传播；
5. 为决策记录更正建立独立类型、资格和登记契约。

本版不定义：

- 全局依据类型全集；
- 全局权威类型全集；
- 各领域决策类型全集；
- 来源注册表内部实现；
- 资格治理完整生命周期；
- 通用提交模型全部语义；
- 依赖失效传播算法；
- 任何提供者专属事务实现。

## 核心定义

> 决策是适用主要权威在合格依据上被实际行使的明确裁决；该行为只有在版本化外部解析、确定性准入和受保护权威写入全部成立后，才能形成不可变决策事实。决策事实可以满足目标迁移的前置条件，但不能自行证明目标迁移已经发生。

```text
Qualified Basis Resolution
+ Authority Applicability Resolution
+ Observable Decision Act
+ Decision Evidence
  -> Candidate Decision Record
  -> Deterministic Admissibility Resolution
  -> Protected Authoritative Decision Write
  -> Authoritative Decision Record
  -> Decision Fact

Decision Fact
+ Target Transition Preconditions
+ Independent Target Commit
  -> Target Formal State Transition
```

## 一、统一类型边界

| 节点 | 类型 | 唯一目的 | 权威所有者或边界 |
|---|---|---|---|
| `Decision Model` | 基础层制度模型 | 定义决策不变量与接口 | 冻结制度 |
| `Decision Request` | 候选请求 | 声明希望裁决的对象与迁移 | 请求边界 |
| `Decision Maker` | 行为角色 | 实际行使主要决策权威 | 无记录所有权 |
| `Decision Act` | 现实事件 | 表达一次实际裁决行为 | 现实层 |
| `Decision Attempt Record` | 不可变尝试记录 | 保存行为输入与当时观察 | 决策尝试账本 |
| `Candidate Decision Record` | 候选记录 | 保存尚未取得事实地位的裁决记录 | 候选边界 |
| `Admissibility Resolver` | 计算角色 | 计算候选准入结果 | 无事实所有权 |
| `Candidate Admissibility Record` | 候选派生记录 | 保存准入计算输出 | 临时解析边界 |
| `Admissibility Registrar` | 登记角色 | 登记合格的准入解析记录 | 无决策事实所有权 |
| `Registered Admissibility Record` | 不可变派生记录 | 保存版本化准入结论 | 准入解析账本 |
| `Decision Fact Commit Contract` | 值对象 | 定义决策事实提交语义与写集 | 决策类型治理制度 |
| `Decision Fact Commit Authority` | 授权对象 | 允许履行指定决策事实写入 | 权威治理制度 |
| `Decision Fact Committer` | 执行角色 | 履行权威决策写入 | 无价值裁决权 |
| `Decision Fact Commit Attempt Record` | 不可变尝试记录 | 保存权威写入输入和提交点观察 | 决策提交账本 |
| `Authoritative Decision Record` | 权威记录 | 保存唯一决策事实及其归因 | 决策注册表 |
| `Decision Fact` | 正式事实 | 表达指定裁决已合法成立 | 决策注册表的权威语义 |
| `Decision Commit Resolver` | 计算角色 | 解析指定提交尝试的结果 | 无事实所有权 |
| `Registered Decision Commit Resolution Record` | 不可变派生记录 | 保存版本化提交结果解析 | 决策提交解析账本 |
| `Legality Reviewer` | 审查角色 | 计算既有决策的合法性解释 | 无失效权威 |
| `Registered Legality Review Record` | 派生审查记录 | 保存特定时间坐标下的审查结论 | 合法性审查账本 |
| `Decision Correction Record` | 派生更正记录 | 更正表示缺陷而不改变裁决语义 | 决策更正账本 |
| `Invalidation Decision` | 新决策事实 | 改变既有决策的当前适用性 | 适用失效权威与决策注册表 |

以下关系必须始终成立：

```text
Decision Act != Candidate Decision Record
Candidate Decision Record != Authoritative Decision Record
Admissibility Resolution != Decision Fact
Legality Review != Invalidation Decision
Correction Record != Decision Mutation
Decision Fact != Target Formal State Transition
```

## 二、决策的单一目的

### DM-R2-01 决策记录权威的一次实际行使

```text
Applicable Primary Authority Grant
  -> Observable Decision Act
  -> Candidate Decision Record
```

`Authority` 回答谁有资格决定；`Decision Act` 表达该资格在现实中的一次实际行使；记录负责保存该行为，不反向创造行为。

只有权威而没有决策行为，不能建立决策事实。只有决策行为而没有适用权威，只能形成决策尝试，不能形成决策事实。

### DM-R2-02 决策不得吸收相邻职责

决策不得：

- 观察现实；
- 创建、修改或补写证据；
- 定义依据资格；
- 授予或扩大权威；
- 比较预期与观察；
- 解释偏差原因；
- 选择运行时补救策略，除非决策类型本身是策略选择决策；
- 执行目标状态迁移；
- 证明自身价值判断客观正确；
- 创建制度或冻结自身。

### DM-R2-03 一个决策实例只有一个主要权威

```text
One Decision Instance
  -> One Applicable Primary Authority Grant
```

主要权威必须在决策时点对以下范围同时适用：

```text
Decision Maker
Decision Type
Decision Object and Version
Decision Disposition
Requested Transition Type
Authority Effective Interval
Institution Version
```

身份匹配、角色能力或历史成功都不能替代完整作用域合法性。

## 三、裁决倾向与请求迁移

### DM-R2-04 裁决倾向独立于迁移类型

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

两者必须分别绑定决策类型制度允许的枚举。

```text
APPROVE + REVOKE
```

表示批准撤销请求。

```text
REJECT + REVOKE
```

表示拒绝撤销请求。

### DM-R2-05 NO_ACTION 形成决策历史但不迁移目标

```text
NO_ACTION -> may form Decision Fact
NO_ACTION -/-> Target State Transition
```

有权主体明确决定保持当前状态时，必须保存该裁决历史。没有记录不能被解释为 `NO_ACTION`。

## 四、外部解析消费契约

### DM-R2-06 决策模型只消费依据资格解析

`Decision Model` 不定义依据为什么合格。它只消费由外部冻结制度建立的：

```text
Registered Basis Qualification Resolution
```

最低字段：

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
Source Registry Snapshot Reference
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Correction View Reference
Registration Authority Reference
```

资格结果：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
```

只有 `QUALIFIED` 能作为正向准入输入。

`NOT_QUALIFIED` 只有在来源范围和规则适用性得到完备证明时，才能形成确定性拒绝条件。否则必须使用 `INDETERMINATE`。

### DM-R2-07 决策模型只消费权威适用性解析

`Decision Model` 不授予权威，也不决定授权生命周期。它只消费：

```text
Registered Authority Applicability Resolution
```

最低字段：

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
Source Registry Snapshot Reference
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Correction View Reference
Registration Authority Reference
```

适用性结果：

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

只有 `APPLICABLE` 能支持决策事实提交。

### DM-R2-08 解析必须绑定同一决策坐标

依据资格解析、权威适用性解析和决策请求必须能投影到同一坐标：

```text
Decision Type
Decision Object ID
Decision Object Version
Decision Time
Requested Transition Type
Decision Institution Version
```

任何以下情况都必须失败关闭：

- 对象或版本不一致；
- 解析发生在无法覆盖决策时点的时间范围；
- 规则版本缺失或不可验证；
- 来源集合不完备且无法证明适用范围；
- 更正视图不同且没有兼容性规则；
- 资格或权威结果冲突；
- 解析记录未由适用登记权威登记。

### DM-R2-09 解析执行权与登记权必须分离

```text
Resolution Computation
-/-> Resolution Registration Authority
```

决策准入可以验证解析记录的真实性、适用范围、版本和结果，不能：

- 临时把原始依据认定为合格；
- 临时恢复已撤销权威；
- 在缺少来源时推断资格；
- 修改外部解析记录；
- 为自己的准入创建外部解析权威。

## 五、候选决策与尝试记录

### DM-R2-10 决策行为必须先形成不可变尝试记录

`Decision Attempt Record` 至少绑定：

```text
Decision Key
Decision Attempt ID
Decision Request ID and Version
Decision Maker
Primary Authority Grant Reference
Decision Type
Decision Object ID and Version
Basis Resolution References
Authority Applicability Resolution Reference
Decision Disposition
Requested Transition Type
Decision Act Observed At
Decision Evidence References
Decision Institution Version
Declared Record Digest
Recorded At
```

尝试记录只证明系统登记了哪些输入和观察，不证明决策事实已经成立。

```text
Decision Attempt Record
-/-> Decision Fact
```

### DM-R2-11 候选决策记录没有正式事实地位

`Candidate Decision Record` 是根据尝试输入组织的候选值对象。它可以被检查、拒绝或因未知而阻断，但不能被目标提交、策略或界面当作正式决策消费。

```text
Candidate Decision Record
  -> eligible for Admissibility Resolution
  -/-> authorize execution
  -/-> satisfy target transition precondition
```

### DM-R2-12 决策键必须稳定且幂等

每个逻辑决策意图必须拥有稳定 `Decision Key`。同一键不得形成两个彼此竞争的权威决策事实。

```text
One Decision Key
  -> At Most One Authoritative Decision Fact
```

重复请求必须解析到既有权威结果或保持未知，不能用新记录覆盖旧记录。

不同裁决意图必须使用不同决策键；撤销、取代和失效是新的决策事实，不复用原决策键。

## 六、确定性准入解析

### DM-R2-13 准入解析只有规则计算权

`Admissibility Resolver` 只能检查：

- 外部依据资格解析是否为 `QUALIFIED`；
- 外部权威适用性解析是否为 `APPLICABLE`；
- 对象、版本、时点和制度坐标是否一致；
- 裁决倾向和迁移类型是否在允许范围；
- 决策证据是否齐备且引用有效；
- 组合要求是否适用于当前决策类型；
- 显式不变量是否满足；
- 决策键是否违反唯一性。

候选结果：

```text
ADMISSIBLE
INADMISSIBLE
INDETERMINATE
```

### DM-R2-14 准入结果的成立条件

`ADMISSIBLE` 要求所有必要正向输入均已解析，并且没有冲突或未知。

`INADMISSIBLE` 只允许由确定性否定条件建立，例如：

```text
Qualified Basis Outcome = NOT_QUALIFIED with complete coverage
Authority Outcome = NOT_APPLICABLE with complete coverage
Disposition outside frozen allowed set
Transition Type outside frozen allowed set
Required immutable field mismatch
Decision Key definitively conflicts with an existing authoritative fact
```

以下情况必须是 `INDETERMINATE`：

```text
Source unavailable
Coverage unproven
Rule version unresolved
Authority revocation view unresolved
Conflicting qualified corrections
Decision key lookup incomplete
Required evidence unresolved
```

```text
Record Not Found
-/-> INADMISSIBLE
```

### DM-R2-15 候选准入与登记准入必须分离

```text
Candidate Decision Record
+ Versioned Resolution Inputs
  -> Admissibility Resolver
  -> Candidate Admissibility Record

Candidate Admissibility Record
+ Admissibility Registration Authority
+ Deterministic Registration Check
  -> Registered Admissibility Record
```

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
Effective At
As Of
Resolved At
Admissibility Rule Version
Decision Institution Version
Evidence References
Resolver Identity
Registration Authority Reference
Registered At
```

准入登记只保存派生结论，不创造决策行为、权威、依据或决策事实。

## 七、决策事实的权威成立

### DM-R2-16 ADMISSIBLE 不是决策事实

```text
Registered Admissibility Record = ADMISSIBLE
-/-> Decision Fact
```

它只证明候选记录具备进入受保护决策写入的资格。

### DM-R2-17 决策事实必须通过受保护权威写入成立

```text
Candidate Decision Record
+ Registered Admissibility Record = ADMISSIBLE
+ Decision Fact Commit Authority
+ Decision Commit Contract
  -> Protected Authoritative Decision Write
  -> Authoritative Decision Record
  -> Decision Fact
```

`Decision Fact Commit Authority` 只允许忠实提交已登记为 `ADMISSIBLE` 的候选决策，不允许：

- 改变裁决倾向；
- 改变请求迁移类型；
- 替换依据或权威；
- 修改决策时点；
- 新增价值判断；
- 绕过决策键唯一性；
- 触发目标对象迁移。

进入受保护写入前，必须先不可变登记 `Decision Fact Commit Attempt Record`：

```text
Decision Commit Attempt ID
Decision Key
Candidate Decision Record Digest
Registered Admissibility Record ID and Digest
Decision Fact Commit Contract Version
Decision Fact Commit Authority Reference
Expected Decision Registry Version
Declared Write-set Digest
Initiated At
```

该尝试记录只证明提交输入已经固定，不证明权威写入已经发生。

```text
Decision Fact Commit Attempt Record
-/-> Decision Fact
```

### DM-R2-18 权威决策写入必须不可分割归因

受保护写入必须在同一权威边界中建立：

```text
Authoritative Decision Record
+ Decision Key Attribution
+ Authoritative Registry Version Transition
```

权威记录最低字段：

```text
Decision Fact ID
Decision Key
Decision Attempt ID
Decision Commit Attempt ID
Candidate Decision Record Digest
Registered Admissibility Record ID
Decision Maker
Primary Authority Grant Reference
Decision Type
Decision Object ID and Version
Basis Qualification Resolution References
Decision Disposition
Requested Transition Type
Decision Time
Decision Evidence References
Decision Institution Version
Prior Registry Version
New Registry Version
Committed At
Decision Fact Commit Authority Reference
Authoritative Record Digest
```

### DM-R2-19 决策事实提交采用三值结果

```text
COMMITTED
ABORTED
INDETERMINATE
```

`COMMITTED` 必须由权威决策记录和唯一决策键归因正向证明。

`ABORTED` 必须由以下任一证明建立：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

仅仅没有读到权威记录不能证明 `ABORTED`。

无法证明已提交或未应用时必须保持 `INDETERMINATE`。

提交结果必须通过独立解析与登记链保存：

```text
Decision Fact Commit Attempt Record
+ Authoritative Decision Registry Sources
+ Commit Attribution Evidence
+ Resolution Rule Version
  -> Decision Commit Resolver
  -> Candidate Decision Commit Resolution Record

Candidate Decision Commit Resolution Record
+ Decision Commit Resolution Registration Authority
+ Deterministic Registration Check
  -> Registered Decision Commit Resolution Record
```

解析器和登记者都不得创建、撤销或修改决策事实。登记记录只是对权威决策注册表和提交证据的可重建派生解释。

`Registered Decision Commit Resolution Record` 至少绑定：

```text
Decision Commit Attempt ID
Decision Key
Commit Outcome
Authoritative Decision Record Reference if applicable
Non-application Proof Reference if applicable
Source Set Digest
Coverage or Completeness Proof Reference
Effective At
As Of
Resolved At
Resolution Rule Version
Evidence References
Resolver Identity
Registration Authority Reference
Registered At
```

```text
Commit Resolution Registration
-/-> Decision Fact Mutation
```

### DM-R2-20 决策事实提交结果不授权策略

```text
COMMITTED -/-> Target Execution
ABORTED -/-> Retry
INDETERMINATE -/-> Cancel or Replace Decision
```

任何重试、对账、升级或人工处理必须由独立策略或适用治理路径授权。

## 八、决策事实与目标迁移

### DM-R2-21 决策事实先于目标迁移

```text
Decision Fact
+ Transition Preconditions
+ Target Commit Contract
+ Target Commit Authority
  -> Target Formal State Transition
```

决策模型不创建目标迁移，也不解释目标提交结果。目标制度必须自行定义目标状态、前置条件、提交语义和失败行为。

### DM-R2-22 决策失败不能被目标状态倒推

```text
Target State appears changed
-/-> Decision Fact existed
```

界面、数据库字段、导出物或目标当前状态不能反向证明决策曾合法成立。必须读取权威决策记录和完整引用链。

### DM-R2-23 决策事实不可因执行失败被抹除

目标执行或提交失败只影响目标迁移，不改变既有决策历史。

```text
Decision Fact = APPROVE
Target Commit = ABORTED
```

可以同时成立。

## 九、组合决策要求

### DM-R2-24 多权威要求必须保持多个决策事实

```text
Authority A -> Decision Fact A
Authority B -> Decision Fact B
Authority C -> Decision Fact C
```

多个权威不得拼成一个没有主要责任主体的联合决策。

### DM-R2-25 组合要求槽位与决策倾向分离

`Composite Decision Requirement` 由目标类型制度定义，至少包含：

```text
Requirement Contract ID and Version
Target Transition Type
Requirement Slot ID
Required Decision Type
Required Disposition
Required Object and Version Relation
Requirement Mode
Exemption Conditions
Evidence Requirements
Failure Behavior
```

槽位模式：

```text
REQUIRED
CONDITIONALLY_EXEMPTIBLE
```

槽位解析结果：

```text
SATISFIED
NOT_SATISFIED
EXEMPT
INDETERMINATE
```

`EXEMPT` 不是决策倾向，也不是缺少记录。

```text
Decision Record Not Found
-/-> EXEMPT
```

### DM-R2-26 豁免只能来自冻结契约

确定性豁免解析必须引用：

```text
Frozen Exemption Rule
Target Object and Version
Qualified Exemption Basis
Source Coverage Proof
Effective At
As Of
Resolved At
Rule and Institution Version
Evidence References
Registration Authority Reference
```

若豁免需要主观判断，就必须建立独立的豁免决策类型，不能由组合解析器临时决定。

### DM-R2-27 组合解析器没有联合权威

组合解析器只能检查冻结槽位是否被已成立决策事实或合格豁免满足。

```text
Composite Resolver
-/-> merge Authorities
-/-> create Decision Fact
-/-> create Exemption
-/-> choose preferred Decision
```

组合解析必须形成候选记录，再由独立组合解析登记权威保存版本化结果。

### DM-R2-28 最终决策必须是独立决策

若目标制度要求 `Final Decision`，它必须：

- 具有独立决策类型；
- 只引用一个主要权威；
- 把子决策事实作为制度允许的合格依据；
- 具有自己的裁决行为、证据、准入与受保护写入；
- 不继承子决策权威；
- 不把子决策自动合成为价值判断。

若目标制度不要求新的价值裁决，则确定性目标提交只能消费组合解析结果，不能创建隐式最终决策。

## 十、事后合法性审查

### DM-R2-29 合法性审查是派生解释，不是失效决策

```text
Historical Decision Record
+ Versioned Review Sources
+ Legality Review Contract
  -> Candidate Legality Review Record
```

候选审查结果：

```text
COMPLIANT
NON_COMPLIANT
INDETERMINATE
```

任何结果都不能直接修改决策事实或目标状态。

### DM-R2-30 历史合法性与当前认识必须分离

合法性审查必须声明视图模式：

```text
HISTORICAL_AS_COMMITTED
CURRENT_RECONSTRUCTION
```

`HISTORICAL_AS_COMMITTED` 回答：

> 按原决策坐标、当时适用制度以及当时合格可见的来源，系统为什么接受或拒绝该决策？

`CURRENT_RECONSTRUCTION` 回答：

> 使用当前已合格的更正和来源认识，系统现在如何解释该历史决策？

两种视图不得互相覆盖。

```text
Current Knowledge Changed
-/-> Historical Record Mutation

New Institution Version
-/-> Retroactive Historical Illegality
```

### DM-R2-31 合法性审查必须绑定双时间和双规则版本

审查记录至少绑定：

```text
Reviewed Decision Fact ID
Original Decision Time
Original Effective Coordinate
Review Effective At
Review As Of
Reviewed At
Original Admissibility Rule Version
Original Institution Version
Review Rule Version
Review Institution Version
Original Source View Reference
Current Correction View Reference
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Review Outcome
Review Reason Codes
```

### DM-R2-32 候选审查与登记审查必须分离

```text
Candidate Legality Review Record
+ Legality Review Registration Authority
+ Deterministic Registration Check
  -> Registered Legality Review Record
```

登记权威只能保存审查结论，不拥有：

- 修改原决策的权威；
- 宣告原决策从未发生的权威；
- 改变目标状态的权威；
- 传播正式失效的权威；
- 修改审查来源或证据的权威。

### DM-R2-33 审查结论只能支持失效请求

```text
Registered Legality Review Record = NON_COMPLIANT
  -> may support Invalidation Decision Request
  -/-> Invalidation Decision Fact
  -/-> Dependency Invalidation Propagation
```

`INDETERMINATE` 必须保持未知，不能为了恢复流程而降级为 `NON_COMPLIANT` 或解释为原决策无效。

## 十一、失效决策与传播

### DM-R2-34 失效必须由新的合法决策建立

`Invalidation Decision` 必须拥有：

```text
Independent Decision Key
Invalidation Decision Type
Target Decision Fact ID
Qualified Legality Review or Other Allowed Basis
Applicable Invalidation Authority
Decision Act and Evidence
Decision Disposition
Requested Applicability Transition
Admissibility Resolution
Protected Decision Fact Write
```

“上级治理权威”不能作为模糊兜底。适用制度必须明确授权类型、对象范围、时点和允许迁移。

### DM-R2-35 失效改变当前适用性，不删除历史

成功失效可以建立：

```text
Decision Applicability = INVALIDATED
Effective At = declared coordinate
```

但不得：

- 删除原决策行为；
- 删除原决策证据；
- 覆盖原权威记录；
- 把历史查询改写为从未存在；
- 使用新制度无条件追溯否定旧制度合法历史。

### DM-R2-36 传播只消费已提交失效事实

```text
Committed Invalidation Decision Fact
+ Frozen Dependency Propagation Rule
+ Propagation Authority
  -> Dependency Invalidation Execution
```

以下对象都不能直接传播正式失效：

```text
Candidate Review
Registered Legality Review Record
Review Request
Model Suspicion
Missing Current Source
```

传播算法和受影响范围属于独立架构与执行制度，本模型只定义其合法输入边界。

## 十二、记录更正

### DM-R2-37 更正只修复表示缺陷

决策记录更正可以处理：

```text
Encoding Error
Transcription Error
Broken Reference Representation
Non-semantic Metadata Error
```

更正不得改变：

```text
Decision Act
Decision Maker
Primary Authority
Decision Type
Decision Object and Version
Decision Disposition
Requested Transition Type
Decision Time
Decision Evidence Meaning
Decision Fact Identity
```

需要改变上述任一语义时，必须使用新的撤销、取代或失效决策。

### DM-R2-38 更正必须经过资格与登记

```text
Correction Request
+ Correction Evidence
+ Correction Qualification Rule
  -> Candidate Decision Correction Record

Candidate Decision Correction Record
+ Correction Registration Authority
+ Deterministic Registration Check
  -> Registered Decision Correction Record
```

更正记录至少绑定：

```text
Correction Record ID
Original Decision Record ID and Digest
Affected Representational Field
Original Representational Value
Corrected Representational Value
Correction Reason
Correction Evidence References
Correction Qualification Rule Version
Effective At
As Of
Registered At
Correction Registration Authority Reference
Correction Record Digest
```

### DM-R2-39 更正采用追加投影

```text
Original Decision Record: immutable
Registered Correction Records: append-only
Current Decision Read Projection: reconstructable
```

读取面可以根据适用更正投影当前表示，但必须允许审计者读取原始内容、全部更正和投影规则。

冲突更正、适用时点不明或资格状态不一致时，当前投影必须保持 `INDETERMINATE`。

### DM-R2-40 更正不改变事实成立状态

```text
Correction Record
-/-> create Decision Fact
-/-> revoke Decision Fact
-/-> change Decision Disposition
-/-> authorize Target Transition
```

## 十三、人工创意裁决

### DM-R2-41 人工裁决要求可审计，不要求客观审美证明

最低证据：

```text
Decision Maker Identity
Applicable Authority Resolution
Object and Version
Candidate Set
Qualified Basis References
Decision Disposition
Requested Transition Type
Decision Time
Recorded Rationale
Decision Evidence
```

理由可以是主观的，但必须真实记录。准入检查只能验证记录、资格和权威是否满足制度，不能证明审美选择是唯一正确答案。

## 十四、决策类型治理契约

### DM-R2-42 每种决策类型必须定义专属契约

```text
Decision Type
Allowed Object Types
Allowed Basis Types
Basis Qualification Contract
Applicable Primary Authority Type
Authority Applicability Contract
Allowed Dispositions
Allowed Transition Types
Composite Decision Requirements
Exemption Contract
Decision Fact Commit Contract
Target Transition Preconditions
Target Commit Interface
Evidence Requirements
Correction Contract
Legality Review Contract
Invalidation Contract
Failure Behavior
```

通用决策模型只规定这些契约必须存在，不定义领域取值全集。

### DM-R2-43 制度冻结决策采用更高门槛

制度冻结决策至少消费：

```text
Approved Institution Proposal
Compatibility Review
Migration or Supersession Plan
Independent Review Evidence
Applicable Freeze Authority Resolution
Freeze Decision Act and Evidence
Admissibility Resolution
Successful Institution Commit
```

本条是候选决策类型的最低契约，不使本提案取得冻结权威，也不能替代 `IF-0007` 的经验、审查、冻结标识和版本要求。

## 十五、完整因果路径

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
       -> INADMISSIBLE -> Illegal or Rejected Decision Attempt Record
       -> INDETERMINATE -> Fail Closed
       -> ADMISSIBLE -> Protected Authoritative Decision Write
            -> COMMITTED -> Authoritative Decision Record -> Decision Fact
            -> ABORTED -> No Decision Fact
            -> INDETERMINATE -> Decision Fact Status Unknown
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

### 事后合法性路径

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
  -> Reconstructable Current Read Projection

Correction -/-> Original Record Mutation
Correction -/-> Decision Semantic Change
```

## 十六、操作矩阵

| 操作 | 候选规则 |
|---|---|
| `Request` | 创建可撤回或修订的决策请求，不产生决策事实 |
| `Act` | 有权主体实际行使裁决，不自动证明准入或提交成功 |
| `Resolve Admissibility` | 确定性计算候选准入结果，无事实登记权 |
| `Register Admissibility` | 登记合格派生解析记录，不创建决策事实 |
| `Commit Decision Fact` | 在受保护权威边界写入已准入的不可变决策记录 |
| `Observe` | 授权审计者读取权威记录及完整引用链 |
| `Review Legality` | 追加版本化审查记录，不修改原决策 |
| `Correct Representation` | 追加非语义更正，不改变裁决事实 |
| `Revoke` | 通过新的合法决策改变未来适用状态 |
| `Supersede` | 通过新的合法决策取代当前适用决策并保留旧历史 |
| `Invalidate` | 通过新的合法失效决策改变当前适用性，不删除历史 |
| `Delete` | 禁止删除已提交决策事实、尝试、证据、审查和更正记录 |

## 十七、非法状态候选

以下情况应在未来冻结时明确为非法：

- 确定性准入结果直接创建决策事实；
- 候选决策记录被目标迁移当作正式决策消费；
- 决策者因拥有裁决权而自动取得任意注册表写入权；
- 依据资格或权威适用性由准入解析器临时创建；
- 解析没有对象、版本、时点、规则版本或来源完备性证明；
- 把来源未找到解释为确定不合格或确定不适用；
- 一个决策实例拼接多个主要权威；
- 把 `NOT_REQUIRED` 或 `EXEMPT` 当作决策倾向；
- 缺少子决策记录时默认组合要求已豁免；
- 最终决策自动继承多个子决策的权威；
- 合法性审查直接修改决策事实或目标状态；
- `NON_COMPLIANT` 未经新失效决策就传播正式失效；
- 当前更正规则或新制度无时点地追溯否定历史；
- 更正记录改变裁决倾向、权威、对象或决策时点；
- 冲突更正被任意选择为当前真值；
- 受保护写入结果未知时宣布已提交或已中止；
- 决策事实自动被解释为目标对象已经迁移；
- 目标当前状态反向证明决策曾合法存在；
- 制度提交失败后仍宣布决策事实或目标迁移成立；
- 删除、覆盖或静默替换历史决策、证据、审查或更正记录。

发现任一非法状态时，系统必须失败关闭并保存现有记录和证据。

## 十八、与相邻模型的职责关系

```text
Authority Model
  -> grants decision and registration authorities

Evidence Model
  -> establishes evidence trust requirements

Qualification Governance
  -> establishes basis qualification resolutions

Authority Applicability Governance
  -> establishes authority applicability resolutions

Decision Model
  -> establishes decision semantic and fact contracts

Commit Model
  -> may implement compatible protected write and target projection contracts

Dependency Governance
  -> propagates committed applicability changes

Institution Model
  -> governs proposal, review, freeze and evolution
```

相邻模型可以实现本提案声明的接口，但不得反向扩大决策职责。决策模型也不得因相邻制度尚未建立，就自行承担来源、资格、提交或传播的全部治理。

## 十九、对 R1 独立审查阻断的修订映射

| `R1` 阻断 | `R2` 修订位置 | 候选处理 |
|---|---|---|
| 决策事实缺少受保护权威登记 | `DM-R2-10` 至 `DM-R2-20` | 拆分尝试、候选、准入登记、受保护写入和三值提交结果 |
| 资格与权威解析输入未闭合 | `DM-R2-06` 至 `DM-R2-09` | 建立版本、时点、来源覆盖和更正视图消费契约 |
| 组合决策豁免与最终语义不完整 | `DM-R2-24` 至 `DM-R2-28` | 分离槽位、豁免解析、最终决策和确定性提交 |
| 事后合法性、失效和传播边界未闭合 | `DM-R2-29` 至 `DM-R2-36` | 引入双视图、双时间、独立登记、新失效决策和传播门槛 |
| 更正记录契约不完整 | `DM-R2-37` 至 `DM-R2-40` | 限定表示更正、独立资格登记和追加投影 |

## 二十、冻结前外部依赖

本候选即使通过独立模型复审，也不能自动冻结。至少仍需：

```text
Frozen or compatible Source Registry Interface
Frozen or compatible Qualification Governance
Frozen or compatible Authority Applicability Governance
Frozen or compatible Institution Registry and Freeze Reference Support
Compatible protected write implementation contract
Repeated and stable runtime evidence
Cross-provider evidence
Cross-project and cross-domain evidence
Migration and compatibility evidence
Applicable Freeze Authority
Independent Freeze Review
Freeze Decision
Successful Institution Commit
```

## 二十一、候选自检状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
R1 Blocker Mapping: COMPLETE
Decision Fact Establishment Boundary: DEFINED
External Resolution Consumption Boundary: DEFINED
Composite Requirement Boundary: DEFINED
Legality and Invalidation Boundary: DEFINED
Correction Boundary: DEFINED
Provider Independence: PASS
Domain Portability: PASS
Independent Model Review: REQUIRED
Model-level Freeze Readiness: NOT_EVALUATED
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

## 当前决定

1. 保留 `CR-0002-R1` 及其独立审查记录作为不可覆盖历史；
2. 将本文件登记为 `CR-0002-R2` 待审查候选；
3. 不修改 `IF-0001` 至 `IF-0007`；
4. 不创建 `foundation/07_Decision.md`；
5. 不创建冻结标识、冻结权威或冻结决定；
6. 下一步只对本候选执行独立模型一致性审查；
7. 独立复审以前，本文件没有运行时权威。
