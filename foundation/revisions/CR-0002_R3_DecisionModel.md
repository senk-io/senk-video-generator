# 决策模型提案第三修订版：有界闭合增补

## 提案信息

```text
Proposal ID: CR-0002-R3
Title: Decision Model — Bounded Blocker Closure
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: BOUNDED_CORRECTION_OVERLAY
Applies To: CR-0002-R2
Revises: CR-0002-R2 within five reviewed blocker scopes only
Review Basis: CR-0002-R2-LOCAL-REVIEW
Independent Review Required: YES
Consolidation Required Before Freeze: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Derived From: CR-0002-R2 Independent Review
```

> 本文件是第三修订阶段的有界纠偏草案，不是冻结制度。它不创建登记权威、证明资格权威、投影发布权威、决策事实或运行时状态迁移，也不覆盖 `CR-0002-R2` 的历史正文。

## 使用方式

下一轮独立一致性复审对象是：

```text
CR-0002-R2 Decision Model Core
+ CR-0002-R3 Bounded Blocker Closure
```

发生冲突时，本文件只在独立审查确定的五项阻断范围内收紧 `R2`：

1. 派生记录登记权威拓扑；
2. 未应用证明资格与提交解析演进；
3. 组合要求与豁免记录；
4. 合法性审查和更正投影的谱系与双时间；
5. 失败分支术语类型。

其他决策语义继续由 `R2` 提供。组合复审通过后，仍必须合并为单一候选文档并重新执行冻结依赖审计；本文件不能单独冻结。

## 修订范围

本版只处理：

```text
Complete Derived-record Registration Authority Topology
Qualified Non-application Proof and Resolution Evolution Interface
Composite Requirement and Exemption Record Contract
Legality and Correction Projection Lineage with Bitemporal Semantics
Failure Branch Type Repair
```

本版不处理：

- 全局来源注册表实现；
- 全局资格类型全集；
- 完整通用提交模型；
- 具体领域决策类型；
- 依赖传播算法；
- `IF-0001` 至 `IF-0007` 的修改；
- 运行时授权实例；
- 制度冻结标识或冻结决定。

## 一、新增统一类型边界

| 节点 | 类型 | 唯一目的 | 权威或逻辑边界 |
|---|---|---|---|
| `Derived Record Registration Authority Contract` | 通用授权契约接口 | 约束一种候选派生记录的内容同一登记 | 权威治理制度 |
| `Derived Record Registration Authority Grant` | 独立授权实例 | 允许在精确作用域内登记一种派生记录 | 权威注册表 |
| `Derived Record Registration Attempt Record` | 不可变尝试记录 | 固定候选内容和登记输入 | 登记尝试账本 |
| `Registered Derived Record Envelope` | 不可变登记外壳 | 保存内容同一载荷及登记归因 | 对应派生记录账本 |
| `Candidate Non-application Proof Record` | 候选证明记录 | 声明一次提交未被权威应用的候选证据集合 | 未应用证明候选边界 |
| `Candidate Proof Qualification Record` | 候选派生记录 | 保存未应用证明资格的候选计算 | 证明资格候选边界 |
| `Registered Proof Qualification Record` | 不可变派生记录 | 保存证明资格的版本化结论 | 证明资格账本 |
| `Candidate Proof Applicability Resolution` | 候选派生记录 | 保存合格证明适用性的候选计算 | 证明适用性候选边界 |
| `Registered Proof Applicability Resolution` | 不可变派生记录 | 保存合格证明对指定提交坐标的当前适用性 | 证明适用性账本 |
| `Proof Qualification Projection` | 可重建读面 | 表达稳定键下的当前证明资格认识 | 无提交解析或事实权威 |
| `Commit Resolution Lineage` | 谱系值对象 | 连接历史提交解析及其后续重建 | 提交解析账本 |
| `Current Commit Resolution Projection` | 可重建读面 | 表达声明认识截点下的当前提交解释 | 无决策事实权威 |
| `Candidate Composite Requirement Resolution Record` | 候选派生记录 | 保存一个组合要求槽位的候选解析 | 组合解析候选边界 |
| `Registered Composite Requirement Resolution Record` | 不可变派生记录 | 保存内容同一的组合槽位解析 | 组合解析账本 |
| `Legality Review Lineage` | 谱系值对象 | 连接同一审查作用域内的并列或后续审查 | 合法性审查账本 |
| `Current Legality Review Projection` | 可重建读面 | 表达稳定键下的当前合法性解释 | 无失效权威 |
| `Candidate Decision Read Projection` | 候选读面 | 按更正链重建当前决策表示 | 可删除投影边界 |
| `Published Decision Read Projection` | 派生发布快照 | 发布内容同一且可重建的当前表示 | 无决策事实权威 |

以下关系必须成立：

```text
Registration Authority Grant for Type A
-/-> Registration Authority for Type B

Registered Derived Record
-/-> Decision Fact

Qualified Non-application Proof
-/-> ABORTED without applicable complete resolution

Current Projection
-/-> Historical Record Mutation

Projection Publication
-/-> Formal Fact Creation
```

## 二、派生记录登记权威拓扑闭合

### DM-R3-01 通用登记契约不传播具体登记权威

`Derived Record Registration Authority Contract` 只统一授权字段与不变量。每一种登记记录类型都必须拥有独立 `Grant ID` 和版本：

```text
Registered Admissibility Record
Registered Decision Commit Resolution Record
Registered Composite Requirement Resolution Record
Registered Legality Review Record
Registered Decision Correction Record
```

一个授权实例只能对应一个精确映射：

```text
One Candidate Record Type
-> One Registered Record Type
-> One Ledger Scope
```

禁止：

```text
Admissibility Registration Grant
-> Composite Registration Authority

Legality Review Registration Grant
-> Correction Registration Authority
```

若实现还发布更正读投影，`Decision Read Projection Publication Authority` 必须是第六个独立授权实例，不得继承 `Correction Registration Authority`。

### DM-R3-02 每个登记授权实例必须具有完整边界

最低授权字段：

```text
Registration Authority Grant ID and Version
Authority Holder Identity or Role
Registered Record Type
Candidate Record Type
Allowed Ledger ID and Namespace
Allowed Object Types
Allowed Object and Version Scope
Allowed Outcome Types
Allowed Rule Versions
Allowed Institution Versions
Effective From
Effective Until
Can Change
Cannot Change
Registration Preconditions
Registration Decision Rule ID and Version
Failure Behavior
Grant Evidence References
Grant Institution Reference
```

`Can Change` 只能包括：

```text
Append one content-identical registered envelope
Advance the declared derived ledger version if applicable
Record registration attribution metadata
```

`Cannot Change` 至少包括：

```text
Candidate Payload
Candidate Outcome
Candidate Reason Codes
Candidate Source Set
Candidate Temporal Coordinate
Candidate Rule or Institution Version
Authoritative Source Records
Decision Fact
Target State
Another Derived Ledger
Authority Grant Scope
```

### DM-R3-03 候选载荷与登记载荷必须内容同一

为避免登记外壳元数据导致摘要混淆，登记对象必须分成：

```text
Canonical Derived Payload
Registration Attribution Envelope
```

内容同一不变量是：

```text
Candidate Payload Digest
= Registered Payload Digest
```

`Registered Record Digest` 是载荷与登记外壳共同计算的摘要，因此不要求等于候选载荷摘要，但必须能够独立验证：

```text
Registered Record Digest
= Digest(
     Registered Payload Digest,
     Registration Authority Grant Reference,
     Registration Attempt ID,
     Registered At,
     Prior Ledger Version,
     New Ledger Version
   )
```

登记者不得以规范化、清洗、补齐默认值或解释冲突为由改变候选载荷。任何内容变化必须生成新的候选记录和新的候选摘要。

### DM-R3-04 每次登记必须先形成不可变尝试记录

`Derived Record Registration Attempt Record` 至少绑定：

```text
Registration Attempt ID
Registration Authority Grant ID and Version
Candidate Record ID
Candidate Record Type
Candidate Payload Digest
Requested Registered Record Type
Object ID and Version Scope
Rule and Institution Version Scope
Expected Ledger Version if applicable
Registration Evidence References
Initiated At
Attempt Record Digest
```

登记结果只有：

```text
REGISTERED
DECLINED
INDETERMINATE
```

- `REGISTERED` 必须由内容同一的登记记录、授权归因及账本版本归因证明；
- `DECLINED` 必须由确定性前置条件失败证明；
- 来源、授权适用性、摘要或账本结果无法确定时必须是 `INDETERMINATE`。

缺少登记记录不能单独证明 `DECLINED`。

### DM-R3-05 登记失败不得改变候选或正式现实

```text
DECLINED
-/-> Candidate Mutation
-/-> Decision Fact Rejection
-/-> Decision Disposition = REJECT

INDETERMINATE
-/-> Retry Authorization
-/-> Record Deletion
-/-> Formal Fact State
```

重试、对账、升级或人工处理仍由独立策略授权。

### DM-R3-06 五类登记权威必须逐项实例化

未来兼容制度至少必须分别提供：

| 登记记录 | 候选记录 | 独立授权实例 | 登记不得创建 |
|---|---|---|---|
| `Registered Admissibility Record` | `Candidate Admissibility Record` | `Admissibility Registration Authority Grant` | 决策事实、资格、权威 |
| `Registered Decision Commit Resolution Record` | `Candidate Decision Commit Resolution Record` | `Decision Commit Resolution Registration Authority Grant` | 提交结果现实、决策事实 |
| `Registered Composite Requirement Resolution Record` | `Candidate Composite Requirement Resolution Record` | `Composite Resolution Registration Authority Grant` | 子决策、豁免、目标迁移 |
| `Registered Legality Review Record` | `Candidate Legality Review Record` | `Legality Review Registration Authority Grant` | 失效事实、传播、历史修改 |
| `Registered Decision Correction Record` | `Candidate Decision Correction Record` | `Correction Registration Authority Grant` | 语义更改、事实撤销、读投影权威 |

授权实例缺失、过期、类型不匹配或范围不完整时，登记必须失败关闭。

## 三、未应用证明资格与提交解析演进闭合

### DM-R3-07 证明类型名称不等于合格证明

以下名称只表达候选证明类别：

```text
PRE_WRITE_EXCLUSION_PROOF
ATOMIC_ABORT_PROOF
AUTHORITATIVE_NON_APPLICATION_PROOF
```

任何类别必须经过：

```text
Candidate Non-application Proof Record
-> Proof Qualification Resolution
-> Registered Proof Qualification Record
-> Proof Applicability Resolution
-> Registered Proof Applicability Resolution
```

才能参与 `ABORTED` 解析。

### DM-R3-08 候选未应用证明必须固定提交作用域和来源边界

`Candidate Non-application Proof Record` 至少绑定：

```text
Candidate Proof ID
Proof Type
Decision Commit Attempt ID
Decision Key
Decision Fact Commit Contract ID and Version
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
Assembler Identity
Assembly Rule Version
Candidate Proof Payload Digest
```

证明组装者只有组装权，无资格计算、资格登记、提交解析登记或决策事实权威。

### DM-R3-09 证明资格必须由独立资格链建立

资格结果：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
```

资格计算必须先形成 `Candidate Proof Qualification Record`，再由独立证明资格登记权威按 `DM-R3-01` 至 `DM-R3-05` 登记。资格计算者不得登记自身输出，登记者不得修改候选资格载荷。

`Registered Proof Qualification Record` 至少绑定：

```text
Proof Qualification Resolution ID
Candidate Proof ID and Payload Digest
Proof Type
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Qualification Outcome
Qualification Reason Codes
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

只有内容同一且已登记的 `QUALIFIED` 可以进入证明适用性解析。来源集合不完备、完备性证明自身未合格或存在未解析相反来源时必须是 `INDETERMINATE`，不得使用 `NOT_QUALIFIED` 假装来源完整。

### DM-R3-10 证明资格与证明适用性必须分离

`QUALIFIED` 只说明候选证明在声明规则下具有证明资格，不说明它当前适用于指定提交解析。

适用性计算必须先形成 `Candidate Proof Applicability Resolution`，再由独立证明适用性登记权威进行内容同一登记。

`Registered Proof Applicability Resolution` 至少绑定：

```text
Proof Applicability Resolution ID
Registered Proof Qualification Record ID and Digest
Candidate Proof ID
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version
Applicability Outcome
Applicability Reason Codes
Validity As Of
Knowledge Boundary Vector
Resolved At
Applicability Rule ID and Version
Institution Version
Current Source Applicability References
Qualification Correction View Reference
Source Set Digest
Coverage or Completeness Proof Reference
Contrary Source References
Evidence References
Resolver Identity
Registration Authority Grant Reference
Candidate Payload Digest
Registered Payload Digest
Registered At
```

适用性结果：

```text
APPLICABLE
NOT_APPLICABLE
INDETERMINATE
```

只有 `APPLICABLE` 能支持 `ABORTED`。资格更正、来源撤销、来源恢复、契约兼容性变化或相反来源出现时，必须产生新的适用性解析，不得覆盖旧记录。

当前证明资格认识必须通过独立 `Proof Qualification Projection` 表达，其稳定键至少包含：

```text
Candidate Proof ID
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version or Compatible Contract Domain Snapshot
Validity As Of
Knowledge Boundary Vector
Qualification Rule Compatibility Domain Snapshot
Source Set Boundary
Qualification Correction View
Projection Rule Version
```

投影最低字段：

```text
Proof Qualification Projection ID
Projection Key Digest
Included Registered Qualification Record IDs
Included Registered Applicability Resolution IDs
Excluded Record IDs and Reasons
Projected Qualification Outcome
Projected Applicability Outcome
Source Set Digest
Coverage or Completeness Qualification References
Conflict References
Produced At
Projection Builder Identity
Projection Rule Version
Projection Digest
```

投影只能保持或降低认识确定性：

```text
QUALIFIED -> QUALIFIED or INDETERMINATE
NOT_QUALIFIED -> NOT_QUALIFIED or INDETERMINATE
Conflicting terminal outcomes -> INDETERMINATE
INDETERMINATE -> INDETERMINATE
```

资格投影不得把 `INDETERMINATE` 提升为确定结果，不得把相反终局任意选成一个结果，也不得登记、创建或撤销决策事实。需要提高确定性或转换终局时必须执行新的独立资格计算、登记和适用性解析。

### DM-R3-11 完备性证明也必须具有外部资格

```text
Coverage or Completeness Proof Reference
-/-> Complete Source Set
```

被引用的完备性证明必须能够解析到兼容外部治理建立的：

```text
Registered Completeness Qualification Record = QUALIFIED
+ Registered Completeness Applicability Resolution = APPLICABLE
+ Matching Source Registry Snapshots
+ Matching Validity As Of
+ Matching Knowledge Boundary Vector
```

本提案不实现全局来源注册表或完整性算法，只规定未获得上述结果时不得建立否定性提交结论。

### DM-R3-12 安全的 ABORTED 必须满足全部正向条件

```text
Historical Proof Qualification = QUALIFIED
+ Proof Qualification Projection = QUALIFIED
+ Proof Qualification Projection.Applicability Outcome = APPLICABLE
+ Matching Candidate Proof ID
+ Matching Decision Commit Attempt ID
+ Matching Decision Key
+ Matching Commit Contract ID and Version
+ Matching Declared Write-set Digest
+ Matching Validity As Of
+ Matching Knowledge Boundary Vector
+ Complete Applicable Source Set
+ Qualified and Applicable Completeness Proof
+ No Unresolved Contrary Source
-> Commit Resolution may be ABORTED
```

任何一项缺失、冲突或未知：

```text
Commit Resolution = INDETERMINATE
Decision Fact Existence = UNRESOLVED_AT_DECLARED_COORDINATE
```

不得创建名为“未知”的决策事实或改变既有决策事实。

### DM-R3-13 提交解析必须保存不可变历史和追加谱系

每个 `Registered Decision Commit Resolution Record` 在 `R2` 字段基础上必须增加：

```text
Candidate Resolution Record ID and Payload Digest
Registered Resolution Payload Digest
Registered Resolution Record Digest
Registration Authority Grant Reference
Prior Resolution Record References
Resolution Lineage ID
Resolution Relationship
Validity As Of
Knowledge Boundary Vector
Projection Rule Compatibility Domain
Source Applicability Change Inputs
Qualification Correction Inputs
Registered At
```

`Resolution Relationship` 合法值：

```text
INITIAL
SUPPLEMENTS
REINTERPRETS_UNDER_NEW_KNOWLEDGE
SUPERSEDES_FOR_CURRENT_PROJECTION
PARALLEL_INCOMPATIBLE_VIEW
```

这些关系只控制派生解释谱系，不修改任何历史解析记录。

### DM-R3-14 历史解析视图与当前提交投影必须分离

视图模式：

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

稳定投影键至少包含：

```text
Decision Commit Attempt ID
Decision Key
Commit Contract ID and Version or Compatible Contract Domain Snapshot
Validity As Of
Knowledge Boundary Vector
Projection View Mode
Projection Rule Version
Source Set Boundary
Qualification Correction View
```

当前投影必须保存：

```text
Projection ID
Projection Key Digest
Resolution Lineage ID
Included Resolution Record IDs
Excluded Resolution Record IDs and Reasons
Current Resolution Outcome
Outcome Reason Codes
Source Set Digest
Coverage Qualification References
Conflict References
Produced At
Projection Builder Identity
Projection Rule Version
Projection Digest
```

当前投影可以因新增知识从历史 `ABORTED` 重建为 `INDETERMINATE`，或在满足全部条件时产生新的当前 `ABORTED` 解释；它不得覆盖历史解析，也不得创建或撤销决策事实。

## 四、组合要求与豁免记录闭合

### DM-R3-15 一个组合解析记录只解析一个要求槽位

```text
One Composite Resolution Record
-> One Requirement Contract Version
-> One Target Object and Version
-> One Requirement Slot ID
```

多个槽位必须形成多个解析记录。汇总读面可以引用这些记录，但不得把多个权威或多个槽位压缩成一个隐式联合决策。

### DM-R3-16 候选组合解析记录必须保存完整输入和谱系

`Candidate Composite Requirement Resolution Record` 至少绑定：

```text
Composite Resolution ID
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Requirement Mode
Required Decision Type
Required Disposition
Required Object and Version Relation
Referenced Decision Fact IDs and Digests
Registered Exemption Basis Qualification Resolution IDs
Registered Exemption Basis Applicability Resolution IDs
Resolution Outcome
Outcome Reason Codes
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

候选结果仍为：

```text
SATISFIED
NOT_SATISFIED
EXEMPT
INDETERMINATE
```

### DM-R3-17 登记组合解析必须保持载荷同一

`Registered Composite Requirement Resolution Record` 在候选载荷之外至少增加登记外壳：

```text
Registration Attempt ID
Composite Resolution Registration Authority Grant Reference
Candidate Payload Digest
Registered Payload Digest
Prior Ledger Version if applicable
New Ledger Version if applicable
Registered At
Registered Record Digest
```

必须满足：

```text
Candidate Payload Digest
= Registered Payload Digest
```

组合登记者不得改变槽位、结果、理由、决策事实引用、豁免依据、时点、来源或规则版本。

### DM-R3-18 豁免依据必须来自精确的已登记资格与适用性解析

`Qualified Exemption Basis` 在合并时必须替换为显式引用：

```text
Registered Exemption Basis Qualification Resolution
Registered Exemption Basis Applicability Resolution
```

资格解析至少绑定：

```text
Exemption Basis ID and Version
Requirement Contract ID and Version
Target Object ID and Version Scope
Target Transition Type
Requirement Slot ID
Frozen Exemption Rule ID and Version
Qualification Outcome
Validity As Of
Knowledge Boundary Vector
Qualification Rule Version
Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Correction View Reference
Evidence References
Registration Authority Grant Reference
Registered Payload Digest
Registered At
```

适用性解析必须证明该合格依据当前仍适用于同一槽位、对象、迁移、规则和时间坐标。

### DM-R3-19 EXEMPT 是需要正向证明的否定性结论

```text
Requirement Mode = CONDITIONALLY_EXEMPTIBLE
+ Frozen Exemption Rule applicable
+ Registered Exemption Basis Qualification = QUALIFIED
+ Registered Exemption Basis Applicability = APPLICABLE
+ Complete Applicable Source Set
+ Qualified and Applicable Coverage Proof
+ No Unresolved Contrary Source
+ Matching Slot, Object, Version, Transition and Temporal Coordinate
-> EXEMPT
```

以下关系非法：

```text
Required Condition Not Observed
-/-> EXEMPT

Decision Fact Not Found
-/-> EXEMPT

Source Set Incomplete
-/-> NOT_SATISFIED
```

来源不完整、相反依据未解析、规则不兼容或时点不一致时必须是 `INDETERMINATE`。

### DM-R3-20 组合解析谱系不得覆盖历史

组合记录必须通过 `Prior Resolution Record References` 和 `Resolution Lineage ID` 追加演进。新的决策事实、豁免更正或来源适用性变化可以产生新解析，但不得覆盖旧解析。

当前组合读面必须绑定：

```text
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Validity As Of
Knowledge Boundary Vector
Projection Rule Version
Source Set Boundary
Correction View
```

不同稳定键的解析不得被当作同一当前结果。

## 五、合法性审查谱系与稳定投影键

### DM-R3-21 合法性审查登记必须证明候选内容同一

`Registered Legality Review Record` 在 `R2` 字段基础上必须增加：

```text
Candidate Review Record ID
Candidate Review Payload Digest
Reviewer Identity
Review Authority Grant Reference
Registration Attempt ID
Legality Review Registration Authority Grant Reference
Registered Review Payload Digest
Registered Review Record Digest
Registered At
Prior Review Record References
Review Lineage ID
Review Relationship
```

必须满足：

```text
Candidate Review Payload Digest
= Registered Review Payload Digest
```

`Review Relationship` 合法值：

```text
INITIAL
SUPPLEMENTS
REINTERPRETS_UNDER_NEW_KNOWLEDGE
SUPERSEDES_FOR_CURRENT_PROJECTION
PARALLEL_INCOMPATIBLE_VIEW
```

关系只控制当前读面选取，不修改原决策事实、原审查记录或历史当时认识。

### DM-R3-22 当前合法性投影必须拥有稳定键

`Current Legality Review Projection Key` 至少包含：

```text
Reviewed Decision Fact ID
Review Mode
Validity As Of
Knowledge Boundary Vector
Original Institution Version
Review Rule Compatibility Domain Snapshot
Source Set Boundary
Correction View Reference
Projection Rule Version
```

`Review Mode` 继续使用：

```text
HISTORICAL_AS_COMMITTED
CURRENT_RECONSTRUCTION
```

任何键字段不同都属于不同投影，不得合并为一个无坐标的“当前合法性”。

### DM-R3-23 当前合法性投影必须保存构建谱系

最低投影字段：

```text
Projection ID
Projection Key Digest
Reviewed Decision Fact ID
Review Lineage ID
Included Review Record IDs
Excluded Review Record IDs and Reasons
Current Review Outcome
Outcome Reason Codes
Source Set Digest
Coverage or Completeness Qualification References
Conflict References
Produced At
Projection Builder Identity
Projection Rule Version
Projection Digest
```

冲突审查、来源不完整、兼容域未知或谱系分叉无法确定时，当前结果必须是 `INDETERMINATE`。

```text
Current Legality Review Projection = NON_COMPLIANT
-/-> Invalidation Decision Fact
-/-> Dependency Propagation
```

## 六、更正双时间与读投影谱系闭合

### DM-R3-24 更正必须区分历史坐标、认识时间、适用时间和产生时间

`R2` 更正字段中含义宽泛的 `Effective At` 和 `As Of` 在合并时必须映射为：

```text
Corrected Historical Coordinate
Correction Known At
Correction Applicable From
Knowledge Boundary Vector
Projection Produced At
```

- `Corrected Historical Coordinate`：被更正表示所属的原记录历史坐标；
- `Correction Known At`：更正证据最早进入可审计认识边界的时间；
- `Correction Applicable From`：冻结更正规则允许该更正进入当前重述的时间；
- `Knowledge Boundary Vector`：固定每个来源注册表的认识截点；
- `Projection Produced At`：本次读投影实际生成时间。

这些字段不得互相替代。`Corrected Historical Coordinate` 较早不能证明系统在该历史时点已经知道更正。

### DM-R3-25 更正记录必须保存候选同一性和追加谱系

`Registered Decision Correction Record` 至少绑定：

```text
Correction Record ID
Candidate Correction Record ID
Candidate Correction Payload Digest
Original Decision Record ID and Digest
Affected Representational Field
Original Representational Value
Corrected Representational Value
Correction Reason
Correction Evidence References
Correction Qualification Resolution ID and Digest
Correction Qualification Rule Version
Corrected Historical Coordinate
Correction Known At
Correction Applicable From
Knowledge Boundary Vector
Prior Correction Record References
Correction Lineage ID
Correction Relationship
Registration Attempt ID
Correction Registration Authority Grant Reference
Registered Correction Payload Digest
Registered At
Registered Correction Record Digest
```

必须满足：

```text
Candidate Correction Payload Digest
= Registered Correction Payload Digest
```

`Correction Relationship` 合法值：

```text
INITIAL
SUPPLEMENTS
SUPERSEDES_FOR_CURRENT_PROJECTION
CONFLICTS_WITH
```

更正关系不能改变原决策语义。需要改变裁决倾向、权威、对象、版本、时点或事实身份时，必须建立新决策。

### DM-R3-26 历史读取与当前重述必须显式分离

更正读视图只有：

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

`HISTORICAL_KNOWLEDGE_VIEW` 只能消费不晚于声明 `Knowledge Boundary Vector` 登记的更正。

`CURRENT_RESTATEMENT_VIEW` 可以使用后来合格且适用的更正重新陈述较早历史坐标，但必须显示：

```text
Restated under later knowledge
Correction Known At
Correction Applicable From
Projection Produced At
```

后来更正不得静默进入历史当时认识视图。

### DM-R3-27 当前决策读投影必须拥有稳定键

```text
Decision Read Projection Key:
  Original Decision Record ID and Digest
  Projection View Mode
  Corrected Historical Coordinate
  Knowledge Boundary Vector
  Correction Rule Compatibility Domain Snapshot
  Source Set Boundary
  Projection Rule Version
```

任何键字段不同都必须产生不同投影。稳定键不得只使用 `Decision Fact ID` 或“当前”标签。

### DM-R3-28 投影构建、发布和事实权威必须分离

```text
Original Decision Record
+ Registered Decision Correction Records
+ Declared Projection Key
+ Projection Rule Version
-> Correction Projection Builder
-> Candidate Decision Read Projection

Candidate Decision Read Projection
+ Decision Read Projection Publication Authority Grant
+ Content-identity Registration Check
-> Published Decision Read Projection
```

`Correction Projection Builder` 只有确定性重建权，没有登记、更正资格、发布或决策权威。

`Decision Read Projection Publication Authority Grant` 必须独立声明：

```text
Allowed Projection Type
Allowed Decision Record Scope
Allowed Projection Rule Versions
Allowed Source Boundaries
Effective Interval
Can Change
Cannot Change
Failure Behavior
```

其 `Can Change` 仅允许发布内容同一、可删除、可重建的投影快照；其 `Cannot Change` 必须包含权威决策记录、更正记录、决策事实、目标状态和投影候选载荷。

### DM-R3-29 投影必须保存完整来源和谱系

`Candidate Decision Read Projection` 与已发布投影载荷至少包含：

```text
Projection ID
Projection Key Digest
Original Decision Record ID and Digest
Correction Lineage IDs
Included Correction Record IDs
Excluded Correction Record IDs and Reasons
Projected Representational Fields
Unchanged Semantic Field Digest
Source Set Digest
Coverage or Completeness Qualification References
Conflict References
Projection Outcome
Projection Reason Codes
Projection Rule Version
Projection Builder Identity
Projection Produced At
Projection Payload Digest
```

投影结果：

```text
PROJECTED
INDETERMINATE
```

多项更正冲突、资格不明、来源不完整、谱系不可比较或规则版本不兼容时必须是 `INDETERMINATE`，不得按登记时间、来源数量或实现偏好选择一个值。

已发布投影必须满足：

```text
Candidate Projection Payload Digest
= Published Projection Payload Digest
```

投影可以删除并从权威原记录和追加更正重建；它不得成为决策注册表真源，也不得反向修改输入记录。

## 七、失败分支术语类型修复

### DM-R3-30 准入失败只能表达为非准入尝试

`R2` 完整因果路径中的：

```text
INADMISSIBLE -> Illegal or Rejected Decision Attempt Record
```

必须替换为：

```text
INADMISSIBLE
-> NON_ADMISSIBLE_DECISION_ATTEMPT
```

`NON_ADMISSIBLE_DECISION_ATTEMPT` 是准入分类，不是裁决倾向、法律责任结论或正式决策事实。

```text
NON_ADMISSIBLE_DECISION_ATTEMPT
!= Decision Disposition REJECT
!= ILLEGAL_ACT
!= Decision Fact
```

若制度需要判断行为是否违法、违规或应承担责任，必须进入独立分类或审查契约，不能由准入枚举推导。

### DM-R3-31 提交未知只属于解析认识

`R2` 完整因果路径中的：

```text
INDETERMINATE -> Decision Fact Status Unknown
```

必须替换为：

```text
Decision Commit Resolution = INDETERMINATE
Decision Fact Existence = UNRESOLVED_AT_DECLARED_COORDINATE
No Decision Fact Created or Mutated by Resolution
```

`INDETERMINATE` 是提交解析的认识结果，不是 `Decision Fact` 的生命周期状态。

### DM-R3-32 修订后的决策事实成立路径

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
            -> No Decision Fact Inference
       -> ADMISSIBLE
            -> Protected Authoritative Decision Write
            -> Decision Fact Commit Attempt Record
            -> Independent Commit Resolution
                 -> COMMITTED
                      -> Authoritative Decision Record
                      -> Decision Fact
                 -> ABORTED
                      -> Qualified and Applicable Non-application Proof
                      -> No Decision Fact for the matched commit attempt
                 -> INDETERMINATE
                      -> Decision Fact Existence Unresolved at Declared Coordinate
                      -> No Decision Fact Created or Mutated by Resolution
```

## 八、权威拓扑审计矩阵

| 行为 | 执行角色 | 所需独立授权 | 可以建立 | 不得建立 |
|---|---|---|---|---|
| 组装未应用证明 | `Proof Assembler` | 证明组装执行授权 | 候选证明 | 资格、适用性、`ABORTED` |
| 计算证明资格 | `Proof Qualification Resolver` | 资格计算授权 | 候选资格记录 | 已登记资格、提交结果 |
| 登记证明资格 | `Proof Qualification Registrar` | 证明资格登记权威 | 内容同一资格记录 | 决策事实、适用性 |
| 解析证明适用性 | `Proof Applicability Resolver` | 适用性解析授权 | 候选适用性记录 | 资格变更、提交结果 |
| 登记证明适用性 | `Proof Applicability Registrar` | 证明适用性登记权威 | 内容同一适用性记录 | `ABORTED`、决策事实 |
| 解析提交结果 | `Decision Commit Resolver` | 提交解析授权 | 候选提交解析 | 决策事实 |
| 登记提交解析 | `Decision Commit Resolution Registrar` | 提交解析登记权威 | 内容同一提交解析 | 提交现实、决策事实 |
| 解析组合槽位 | `Composite Resolver` | 组合解析授权 | 候选槽位解析 | 豁免、子决策、联合权威 |
| 登记组合解析 | `Composite Resolution Registrar` | 组合解析登记权威 | 内容同一槽位解析 | 目标迁移 |
| 计算合法性审查 | `Legality Reviewer` | 合法性审查授权 | 候选审查 | 失效、传播 |
| 登记合法性审查 | `Legality Review Registrar` | 合法性审查登记权威 | 内容同一审查记录 | 历史修改、失效 |
| 登记表示更正 | `Correction Registrar` | 更正登记权威 | 内容同一非语义更正 | 语义决策、读投影发布 |
| 构建更正投影 | `Correction Projection Builder` | 投影构建授权 | 候选可重建读面 | 登记、发布、正式事实 |
| 发布更正投影 | `Decision Read Projection Publisher` | 独立投影发布权威 | 内容同一可删除投影 | 决策事实、权威记录修改 |

任何角色由同一实现或同一主体承担时，仍必须使用独立授权实例、任务契约、输入边界、记录和归因；身份相同不得合并权威。

## 九、非法状态候选增补

以下情况在未来合并与冻结时必须明确为非法：

- 一个派生登记授权实例登记多个记录类型；
- 登记者在登记时修改候选载荷；
- 用登记外壳摘要掩盖候选载荷与登记载荷不一致；
- 缺少登记记录时推断登记已拒绝；
- 证明类型名称直接支持 `ABORTED`；
- 完备性证明只因被引用就被视为合格；
- 资格、适用性、提交键、契约或时间坐标不一致时建立 `ABORTED`；
- 当前提交投影覆盖历史提交解析；
- 缺少决策事实或豁免依据时默认组合槽位已满足；
- 来源不完整时建立 `EXEMPT` 或 `NOT_SATISFIED`；
- 不同组合槽位被压缩成一个隐式联合决策；
- 合法性投影没有稳定键或跨兼容域合并；
- 后来更正被展示为历史当时已经知道；
- 投影构建者继承更正登记权威或决策事实权威；
- 冲突更正由实现任意选出当前值；
- 把 `INADMISSIBLE` 解释为裁决倾向 `REJECT`；
- 把提交解析 `INDETERMINATE` 写入决策事实生命周期。

发现任一状态时必须失败关闭，保留候选、历史记录、证据、冲突和当前认识边界。

## 十、对 R2 独立审查阻断的修订映射

| `R2` 阻断 | `R3` 修订位置 | 候选闭合方式 |
|---|---|---|
| 派生记录登记权威拓扑不完整 | `DM-R3-01` 至 `DM-R3-06` | 通用接口、逐类型授权实例、内容同一、尝试记录和失败行为 |
| `ABORTED` 缺少证明资格及解析演进契约 | `DM-R3-07` 至 `DM-R3-14` | 候选证明、资格、适用性、完备性、谱系和双视图投影 |
| 组合要求与豁免缺少完整记录契约 | `DM-R3-15` 至 `DM-R3-20` | 单槽位记录、候选与登记载荷、显式豁免资格、完备性和谱系 |
| 合法性审查和更正投影缺少谱系及双时间边界 | `DM-R3-21` 至 `DM-R3-29` | 审查同一性、稳定键、更正五时间字段、投影分权与谱系 |
| 准入失败与提交未知存在术语类型歧义 | `DM-R3-30` 至 `DM-R3-32` | 非准入尝试类型与解析未知类型分离 |

## 十一、冻结前外部依赖

本候选即使通过独立模型复审，也不能自动冻结。至少仍需：

```text
Frozen or compatible Source Registry Interface
Frozen or compatible Qualification Governance
Frozen or compatible Authority Applicability Governance
Frozen or compatible Derived Record Registration Authority Governance
Frozen or compatible Proof Qualification and Applicability Governance
Frozen or compatible Institution Registry and Freeze Reference Support
Compatible protected write implementation contract
Repeated and stable runtime evidence
Cross-provider evidence
Cross-project and cross-domain evidence
Migration and consolidation evidence
Applicable Freeze Authority
Independent Freeze Review
Freeze Decision
Successful Institution Commit
```

## 十二、候选自检状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
R2 Blocker Mapping: COMPLETE
Derived-record Registration Authority Topology: DEFINED
Content Identity Invariant: DEFINED
ABORTED Proof Qualification Boundary: DEFINED
Proof Applicability Boundary: DEFINED
Resolution Evolution Boundary: DEFINED
Composite Record Contract: DEFINED
Exemption Proof Boundary: DEFINED
Legality Review Registration Contract: DEFINED
Current Review Projection Key: DEFINED
Correction Bitemporal Semantics: DEFINED
Correction Projection Lineage: DEFINED
Failure Branch Type Safety: DEFINED
Provider Independence: PASS
Domain Portability: PASS
Independent Model Review: REQUIRED
Model-level Freeze Readiness: NOT_EVALUATED
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

这些自检只说明本草案已经逐项给出候选契约，不构成独立审查结论。

## 当前决定

1. 保留 `CR-0002-R2` 及其独立审查记录作为不可覆盖历史；
2. 将本文件登记为 `CR-0002-R3` 有界纠偏候选；
3. 不修改 `IF-0001` 至 `IF-0007`；
4. 不创建 `foundation/07_Decision.md`；
5. 不创建任何运行时登记权威、证明资格权威或投影发布权威；
6. 不创建冻结标识、冻结权威或冻结决定；
7. 下一步只对 `R2 + R3` 组合候选执行独立模型一致性复审；
8. 组合复审通过后仍需合并为单一候选并重新审计外部依赖；
9. 在正式冻结以前，本文件不可执行且没有制度权威。
