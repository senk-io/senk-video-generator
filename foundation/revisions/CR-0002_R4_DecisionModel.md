# 决策模型提案第四修订版：接口与时间闭合增补

## 提案信息

```text
Proposal ID: CR-0002-R4
Title: Decision Model — Interface and Temporal Closure
Status: DRAFT
Authority: NONE
Executable: NO
Revision Form: BOUNDED_CORRECTION_OVERLAY
Applies To: CR-0002-R2 + CR-0002-R3
Revises: CR-0002-R3 within three reviewed blocker scopes only
Review Basis: CR-0002-R3-LOCAL-REVIEW
Independent Review Required: YES
Consolidation Required Before Freeze: YES
Institution Freeze Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0003 Constitution Candidate R2
Derived From: CR-0002-R3 Independent Review
```

> 本文件是第四修订阶段的有界纠偏草案，不是冻结制度。它不使 `CR-0003` 取得冻结权威，不创建证明资格、豁免、合法性审查、决策事实、运行时登记或冻结决定，也不覆盖 `CR-0002-R2`、`CR-0002-R3` 及其审查历史。

## 使用方式

下一轮独立一致性复审对象是：

```text
CR-0002-R2 Decision Model Core
+ CR-0002-R3 Bounded Blocker Closure
+ CR-0002-R4 Interface and Temporal Closure
```

发生冲突时，本文件只在以下范围收紧 `R3`：

1. 未应用证明资格、适用性和资格投影接口；
2. 豁免依据适用性候选、登记、谱系和投影契约；
3. 合法性审查记录的双时间规范化及其与投影键的映射。

其他语义继续由 `R2` 和 `R3` 提供。组合复审通过后，仍必须合并为单一候选并重新执行冻结依赖审计。

## 修订范围

本版只处理：

```text
Align Non-application Proof Qualification and Applicability Semantics
Complete Exemption Basis Applicability Record Contract
Normalize Legality Review Bitemporal Record and Projection Mapping
```

本版不处理：

- 决策事实成立主干；
- 派生记录登记通用契约；
- 组合单槽位记录结构；
- 更正记录和更正投影主干；
- 通用提交模型实现；
- 全局来源注册表或资格治理实现；
- 具体领域决策类型；
- 运行时授权实例；
- `IF-0001` 至 `IF-0007` 的修改；
- 制度冻结标识或冻结决定。

## 一、新增与规范化类型边界

| 节点 | 类型 | 唯一目的 | 权威或逻辑边界 |
|---|---|---|---|
| `Proof Qualification Outcome` | 规范枚举 | 表达未应用证明资格结论 | 证明资格规则 |
| `Proof Applicability Outcome` | 规范枚举 | 表达证明资格在声明坐标的适用性 | 证明适用性规则 |
| `Qualification Scope Mode` | 规范枚举 | 严格选择精确契约或兼容域快照 | 资格投影键 |
| `Projection View Mode` | 规范枚举 | 区分历史认识和当前重述 | 投影身份 |
| `Qualification Compatibility Domain Snapshot` | 不可变制度快照 | 固定可比较提交契约版本集合 | 资格治理制度 |
| `Candidate Exemption Basis Applicability Resolution Record` | 候选派生记录 | 保存豁免依据适用性的候选计算 | 豁免适用性候选边界 |
| `Registered Exemption Basis Applicability Resolution Record` | 不可变派生记录 | 保存内容同一的豁免适用性结论 | 豁免适用性账本 |
| `Exemption Basis Applicability Lineage` | 谱系值对象 | 连接同一稳定键下的追加适用性解析 | 豁免适用性账本 |
| `Exemption Basis Applicability Projection` | 可重建读面 | 表达声明认识截点下的当前豁免适用性 | 无豁免或目标迁移权威 |
| `Legality Review Temporal Mapping Contract` | 版本化制度契约 | 规定旧审查时间字段的确定性规范化 | 合法性审查治理制度 |
| `Candidate Legality Review Temporal Normalization Record` | 候选派生记录 | 保存一项旧审查记录的候选时间映射 | 时间规范化候选边界 |
| `Registered Legality Review Temporal Normalization Record` | 不可变派生记录 | 保存内容同一的审查时间映射 | 合法性审查规范化账本 |

以下关系必须始终成立：

```text
NOT_QUALIFIED
!= DISQUALIFIED without explicit compatibility evidence

NOT_APPLICABLE
!= INAPPLICABLE without explicit compatibility evidence

CONFLICTED
!= INDETERMINATE

Exact Contract Version
xor Compatibility Domain Snapshot

Review Act Observed At
!= Review Knowledge Boundary Vector

Temporal Normalization
-/-> Historical Review Mutation

Exemption Applicability Resolution
-/-> Exemption Creation
```

## 二、未应用证明资格值域闭合

### DM-R4-01 证明资格使用规范四值枚举

`R3` 中证明资格的规范值域必须在合并时替换为：

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED
```

- `QUALIFIED`：在声明规则、来源、时点和作用域内，证明满足全部正向资格条件；
- `DISQUALIFIED`：在来源完备且没有未解析冲突的条件下，存在确定性不合格原因；
- `INDETERMINATE`：来源、规则、作用域、时间或充分性无法形成确定认识；
- `CONFLICTED`：同一可比较作用域内存在相反终局资格来源。

```text
CONFLICTED
-/-> QUALIFIED
-/-> DISQUALIFIED
-/-> INDETERMINATE
```

冲突与未知都失败关闭，但必须保存为不同审计语义。

### DM-R4-02 证明适用性使用规范四值枚举

`R3` 中证明适用性的规范值域必须在合并时替换为：

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

- `APPLICABLE`：合格证明在指定有效时点、认识边界、提交键和契约作用域内可被消费；
- `INAPPLICABLE`：在来源完备且无冲突时，可确定证明不适用于该坐标；
- `INDETERMINATE`：当前无法确定适用性；
- `CONFLICTED`：同一可比较作用域内存在相反适用性终局来源。

只有 `APPLICABLE` 可以进入 `ABORTED` 的正向条件。

合并后的规范对象名称必须与兼容提交接口一致：

```text
Candidate Qualification Applicability Record
Registered Qualification Applicability Record
```

`R3` 中的：

```text
Candidate Proof Applicability Resolution
Registered Proof Applicability Resolution
```

只能作为待合并旧名称，不能形成第二套竞争记录类型。单一候选必须直接使用规范名称，或通过显式术语同一声明证明两者是同一对象而不是相邻对象。

### DM-R4-03 旧名称不得静默改名

由于 `R2` 至 `R4` 均不可执行，没有合法运行时记录需要原地迁移。单一候选合并时，规范正文必须使用 `DISQUALIFIED` 和 `INAPPLICABLE`。

若未来迁移工具导入使用以下旧候选值的非权威草案数据：

```text
NOT_QUALIFIED
NOT_APPLICABLE
```

只有存在已登记语义兼容记录时才允许映射：

```text
NOT_QUALIFIED -> DISQUALIFIED
NOT_APPLICABLE -> INAPPLICABLE
```

兼容记录至少绑定：

```text
Source Enum and Version
Target Enum and Version
Source and Target Semantic Definitions
Total Deterministic Mapping
Epistemic Strength Preservation
Conflict Preservation
Field Presence Preservation
Evidence Reference Preservation
Mapping Rule Version
Governing Institution Reference
Compatibility Evidence References
```

缺少兼容记录时只能映射为：

```text
UNRESOLVED_LEGACY_VALUE
-> INDETERMINATE projection
```

不得依靠名称相似、实现习惯或本提案文字自动宣布等价。

## 三、证明资格投影身份闭合

### DM-R4-04 资格作用域模式必须严格二选一

规范模式只有：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

每个 `Proof Qualification Projection Key` 必须且只能选择一个模式。

```text
Qualification Scope Mode = EXACT_CONTRACT_VERSION
-> Exact Commit Contract ID and Version required
-> Compatibility Domain Snapshot fields = NOT_APPLICABLE

Qualification Scope Mode = COMPATIBILITY_DOMAIN_SNAPSHOT
-> Qualification Compatibility Domain Snapshot required
-> Exact Commit Contract fields = NOT_APPLICABLE
```

两组字段同时存在或同时缺失时，投影候选必须为 `INDETERMINATE`，不得生成可消费资格投影。

### DM-R4-05 兼容域必须由不可变快照固定

`Qualification Compatibility Domain Snapshot` 至少绑定：

```text
Compatibility Domain ID and Version
Exact Member Commit Contract IDs and Versions
Membership Digest
Membership Rule Version
Qualification Semantic Compatibility Record References
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
Snapshot Digest
```

成员变化必须形成新快照版本、新摘要和新投影键。决策模型只消费该快照，不创建兼容域或冻结引用。

`Institution Freeze Reference` 缺失或不可验证时，兼容域不能支持正向资格投影。

### DM-R4-06 投影视图模式必须进入资格投影键

规范视图模式：

```text
HISTORICAL_KNOWLEDGE_VIEW
CURRENT_RESTATEMENT_VIEW
```

- `HISTORICAL_KNOWLEDGE_VIEW` 只能消费不晚于声明认识边界登记的来源；
- `CURRENT_RESTATEMENT_VIEW` 可以消费后来合格更正和适用性变化，重新陈述指定有效时点的当前认识。

后来来源不得静默进入历史认识视图。当前重述不得展示为历史当时认识。

### DM-R4-07 证明资格投影键必须完整且稳定

规范键为：

```text
Proof Qualification Projection Key:
  Candidate Proof ID
  Decision Commit Attempt ID
  Decision Key
  Qualification Scope Mode
  Exact Commit Contract ID and Version or NOT_APPLICABLE
  Qualification Compatibility Domain Snapshot ID and Version or NOT_APPLICABLE
  Validity As Of
  Knowledge Boundary Vector
  Projection View Mode
  Qualification Rule Compatibility Domain Snapshot
  Source Set Boundary
  Qualification Correction View
  Qualification Projection Rule Version
```

任何字段不同都属于不同投影身份。投影不得跨证明、提交尝试、决策键、契约作用域、有效时点、认识截点、视图模式或来源边界复用。

### DM-R4-08 资格投影必须分别保留资格冲突和适用性冲突

`Proof Qualification Projection` 在 `R3` 字段基础上必须规范为：

```text
Proof Qualification Projection ID
Projection Key and Digest
Included Registered Qualification Record IDs
Included Registered Applicability Resolution IDs
Excluded Record IDs and Reasons
Projected Qualification Outcome
Aggregate Applicability Outcome
Qualification Conflict References
Applicability Conflict References
Source Set Digest
Registered Completeness References
Coverage or Completeness Qualification References
Produced At
Projection Builder Identity
Projection Rule Version
Projection Digest
```

资格冲突和适用性冲突不得合并成一个无类型冲突字段。

### DM-R4-09 资格投影使用完备真值表

在稳定键完全相同、语义可比较且来源闭包完整时：

```text
Applicable comparable QUALIFIED only
-> Projected Qualification Outcome = QUALIFIED

Applicable comparable DISQUALIFIED only
-> Projected Qualification Outcome = DISQUALIFIED

Applicable comparable QUALIFIED + DISQUALIFIED
-> Projected Qualification Outcome = CONFLICTED

Any required qualification result = CONFLICTED
-> Projected Qualification Outcome = CONFLICTED

Any required applicability result = CONFLICTED
-> Aggregate Applicability Outcome = CONFLICTED

All required applicability results = APPLICABLE
-> Aggregate Applicability Outcome = APPLICABLE

Any definitive required applicability result = INAPPLICABLE
+ no applicability conflict
+ complete applicable source set
-> Aggregate Applicability Outcome = INAPPLICABLE

Missing, incompatible or unresolved required input
-> corresponding outcome = INDETERMINATE

No applicable qualification record
-> Projected Qualification Outcome = INDETERMINATE
```

禁止：

```text
CONFLICTED -> INDETERMINATE for convenience
CONFLICTED -> one selected terminal
INDETERMINATE -> terminal outcome
Source Not Found -> DISQUALIFIED or INAPPLICABLE
```

### DM-R4-10 ABORTED 必须消费规范资格投影

`R3` 中安全 `ABORTED` 条件在合并时必须收紧为：

```text
Historical Registered Proof Qualification = QUALIFIED
+ Proof Qualification Projection.Projected Qualification Outcome = QUALIFIED
+ Proof Qualification Projection.Aggregate Applicability Outcome = APPLICABLE
+ Exact Proof Qualification Projection Key
+ Projection View Mode allowed by Commit Contract
+ Same Candidate Proof ID
+ Same Decision Commit Attempt ID
+ Same Decision Key
+ Same Commit Contract Scope
+ Same Declared Write-set Digest
+ Same Validity As Of
+ Same Knowledge Boundary Vector
+ Registered Completeness = COMPLETE
+ Complete Applicable Source Set
+ Underlying Qualification, Applicability, Closure and Evidence References
+ No Qualification Conflict
+ No Applicability Conflict
+ No Unresolved Contrary Source
-> Commit Resolution may be ABORTED
```

任一项未满足：

```text
Commit Resolution = INDETERMINATE
Decision Fact Existence = UNRESOLVED_AT_DECLARED_COORDINATE
```

资格投影只是可重建解析输入，不能创建、撤销或修改决策事实。

## 四、豁免依据适用性记录契约闭合

### DM-R4-11 豁免资格与豁免适用性继续分离

```text
Registered Exemption Basis Qualification Resolution = QUALIFIED
-/-> Exemption Basis currently APPLICABLE
```

资格记录回答豁免依据是否具有资格；适用性记录回答该合格依据是否能在指定槽位、对象、迁移、时间和认识边界被消费。两类记录必须拥有独立候选计算、登记授权、规则版本和谱系。

### DM-R4-12 豁免适用性采用规范四值枚举

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

`CONFLICTED` 必须保存相反适用性来源，不得折叠为普通未知或任意终局。

只有 `APPLICABLE` 可以满足 `EXEMPT` 的正向适用性条件。

### DM-R4-13 豁免适用性解析必须拥有稳定键

```text
Exemption Basis Applicability Key:
  Registered Exemption Basis Qualification Resolution ID and Digest
  Exemption Basis ID and Version
  Requirement Contract ID and Version
  Target Object ID and Version
  Target Transition Type
  Requirement Slot ID
  Frozen Exemption Rule ID and Version
  Validity As Of
  Knowledge Boundary Vector
  Projection View Mode
  Source Set Boundary
  Correction View Reference
  Applicability Rule Version
```

任何字段不同都属于不同适用性解析。一个槽位、对象或豁免依据的适用性不得被另一个作用域复用。

### DM-R4-14 候选豁免适用性记录必须保存完整输入

`Candidate Exemption Basis Applicability Resolution Record` 至少绑定：

```text
Exemption Applicability Resolution ID
Exemption Basis Applicability Key and Digest
Registered Exemption Basis Qualification Resolution ID and Digest
Exemption Basis ID and Version
Requirement Contract ID and Version
Target Object ID and Version
Target Transition Type
Requirement Slot ID
Frozen Exemption Rule ID and Version
Applicability Outcome
Applicability Reason Codes
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
Resolver Identity
Applicability Resolution Authority Grant Reference
Prior Applicability Resolution References
Applicability Lineage ID
Candidate Payload Digest
```

解析器只有候选计算权，不能登记自身输出、创建豁免、建立组合结果或修改资格记录。

### DM-R4-15 豁免适用性登记必须内容同一

```text
Candidate Exemption Basis Applicability Resolution Record
+ Exemption Basis Applicability Registration Authority Grant
+ Deterministic Content-identity Registration Check
-> Registered Exemption Basis Applicability Resolution Record
```

登记授权适用 `DM-R3-01` 至 `DM-R3-05` 的通用派生记录登记契约，并且必须是独立授权实例。

登记外壳至少绑定：

```text
Registration Attempt ID
Exemption Basis Applicability Registration Authority Grant ID and Version
Candidate Record ID
Candidate Payload Digest
Registered Payload Digest
Prior Ledger Version if applicable
New Ledger Version if applicable
Registered At
Registered Record Digest
Registration Evidence References
```

必须满足：

```text
Candidate Payload Digest
= Registered Payload Digest
```

登记者不得改变适用性结果、理由、资格引用、来源、冲突、规则或时间坐标。

### DM-R4-16 豁免适用性解析必须追加演进

`Applicability Lineage ID` 标识同一稳定作用域内的解析谱系。关系类型：

```text
INITIAL
SUPPLEMENTS
REINTERPRETS_UNDER_NEW_KNOWLEDGE
SUPERSEDES_FOR_CURRENT_PROJECTION
PARALLEL_INCOMPATIBLE_VIEW
```

来源适用性变化、更正、规则兼容性变化或新增相反来源必须产生新候选与新登记记录，不得覆盖旧记录。

关系只控制当前读面选择，不改变历史资格、历史适用性或豁免事实。

### DM-R4-17 当前豁免适用性必须通过可重建投影表达

`Exemption Basis Applicability Projection` 必须使用 `DM-R4-13` 的稳定键，并至少保存：

```text
Projection ID
Projection Key and Digest
Applicability Lineage ID
Included Registered Applicability Resolution IDs
Excluded Resolution IDs and Reasons
Projected Applicability Outcome
Applicability Conflict References
Source Set Digest
Coverage or Completeness Qualification References
Produced At
Projection Builder Identity
Projection Rule Version
Projection Digest
```

投影真值：

```text
Applicable comparable APPLICABLE only -> APPLICABLE
Applicable comparable INAPPLICABLE only -> INAPPLICABLE
APPLICABLE + INAPPLICABLE -> CONFLICTED
Any required CONFLICTED -> CONFLICTED
Missing, incompatible or incomplete input -> INDETERMINATE
No applicable registered resolution -> INDETERMINATE
```

投影可删除并重建，不得创建豁免、组合结果、目标迁移或决策事实。

### DM-R4-18 EXEMPT 必须消费完整适用性链

```text
Requirement Mode = CONDITIONALLY_EXEMPTIBLE
+ Frozen Exemption Rule applicable
+ Registered Exemption Basis Qualification = QUALIFIED
+ Exact Exemption Basis Applicability Projection Key
+ Exemption Basis Applicability Projection = APPLICABLE
+ Matching Requirement Slot, Object, Version and Transition
+ Matching Validity As Of and Knowledge Boundary Vector
+ Complete Applicable Source Set
+ Qualified and Applicable Coverage Proof
+ No Qualification Conflict
+ No Applicability Conflict
+ No Unresolved Contrary Source
-> Composite Resolution may be EXEMPT
```

任何一项缺失、冲突或未知：

```text
Composite Resolution = INDETERMINATE
```

`EXEMPT` 仍然不是决策倾向、缺少决策记录、豁免决策或目标状态。

## 五、合法性审查双时间规范化闭合

### DM-R4-19 合法性审查必须使用五个不可互换时间字段

规范时间字段：

```text
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Review Act Observed At
Review Record Produced At
Review Registered At
```

- `Reviewed Historical Validity Coordinate`：本次审查所解释现实的有效历史坐标；
- `Review Knowledge Boundary Vector`：本次审查允许消费的各来源注册表认识截点；
- `Review Act Observed At`：审查行为实际发生或被观察的时间；
- `Review Record Produced At`：候选审查记录实际生成的时间；
- `Review Registered At`：内容同一审查记录进入审查账本的时间。

时间先后不自动建立语义等价。较晚产生或登记的记录可以重述较早有效坐标，但不得冒充历史当时认识。

### DM-R4-20 R2 宽泛时间字段不得直接进入当前投影

以下旧字段：

```text
Original Decision Time
Original Effective Coordinate
Review Effective At
Review As Of
Reviewed At
R3 Registered At
```

在完成规范化前只能作为旧载荷字段保存，不能直接填入 `Current Legality Review Projection Key`。

```text
Field Name Similarity
-/-> Temporal Semantic Equivalence
```

### DM-R4-21 时间规范化必须使用版本化映射契约

`Legality Review Temporal Mapping Contract` 至少绑定：

```text
Mapping Contract ID and Version
Source Review Contract ID and Version
Target Review Contract ID and Version
Source Field Definitions
Target Field Definitions
Allowed Exact Mappings
Allowed NOT_APPLICABLE Conditions
UNRESOLVED Failure Conditions
Knowledge Boundary Construction Rule
Produced and Registered Time Attribution Rule
Evidence Preservation Rule
Non-retroactive Knowledge Rule
Mapping Institution ID and Version
Institution Freeze Reference
Compatibility Evidence References
```

映射契约只能解释字段，不能修改原审查记录、补写来源或建立合法性结论。

### DM-R4-22 每个旧时间字段必须产生显式映射结果

每个源字段的映射结果只有：

```text
EXACT_MAPPED
NOT_APPLICABLE
UNRESOLVED
```

- `EXACT_MAPPED` 必须引用契约规则、目标字段和映射证据；
- `NOT_APPLICABLE` 必须引用允许省略该目标字段的规则和原因；
- `UNRESOLVED` 表示无法安全确定含义，不能补推。

最低候选映射方向：

```text
Original Decision Time
-> component of Reviewed Historical Validity Coordinate if declared by source contract

Original Effective Coordinate
-> Reviewed Historical Validity Coordinate if semantically exact

Review Effective At
-> Reviewed Historical Validity Coordinate only if source contract explicitly defines validity semantics

Review As Of
-> Review Knowledge Boundary Vector only if exact registry boundaries can be reconstructed

Reviewed At
-> Review Act Observed At only if it records the review act time

R3 Registered At
-> Review Registered At if it is attributed by the content-identical legality review registration envelope
```

禁止默认映射：

```text
Reviewed At -/-> Review Knowledge Boundary Vector
Reviewed At -/-> Review Record Produced At
Review Registered At -/-> Review Knowledge Boundary Vector
Review As Of timestamp alone -/-> complete Knowledge Boundary Vector
```

多个旧字段若被映射到同一规范目标字段，所有 `EXACT_MAPPED` 结果必须语义相同且值一致；任一冲突都必须把该目标字段标记为 `UNRESOLVED`，不得按字段优先级、非空优先或时间较新原则选择一个值。

### DM-R4-23 候选时间规范化记录必须保存逐字段证据

`Candidate Legality Review Temporal Normalization Record` 至少绑定：

```text
Temporal Normalization ID
Source Legality Review Record ID and Digest
Source Review Contract ID and Version
Target Review Contract ID and Version
Temporal Mapping Contract ID and Version
Original Decision Time Mapping Result and Evidence
Original Effective Coordinate Mapping Result and Evidence
Review Effective At Mapping Result and Evidence
Review As Of Mapping Result and Evidence
Reviewed At Mapping Result and Evidence
Normalized Reviewed Historical Validity Coordinate or UNRESOLVED
Normalized Review Knowledge Boundary Vector or UNRESOLVED
Normalized Review Act Observed At or UNRESOLVED
Normalized Review Record Produced At or UNRESOLVED
Normalized Review Registered At or UNRESOLVED
Source Set Boundary
Evidence References
Normalizer Identity
Normalization Authority Grant Reference
Produced At
Candidate Payload Digest
```

规范化执行者没有合法性裁决、审查登记、投影发布或历史修改权威。

### DM-R4-24 时间规范化登记必须内容同一

```text
Candidate Legality Review Temporal Normalization Record
+ Legality Review Temporal Normalization Registration Authority Grant
+ Deterministic Content-identity Registration Check
-> Registered Legality Review Temporal Normalization Record
```

该登记授权必须是独立实例，并适用 `DM-R3-01` 至 `DM-R3-05`。

登记外壳至少绑定：

```text
Registration Attempt ID
Temporal Normalization Registration Authority Grant ID and Version
Candidate Normalization Record ID
Candidate Payload Digest
Registered Payload Digest
Registered At
Registered Record Digest
Registration Evidence References
```

必须满足：

```text
Candidate Payload Digest
= Registered Payload Digest
```

登记者不得选择不同映射结果、补写缺失边界或改变原审查载荷。

### DM-R4-25 新合法性审查记录必须直接使用规范时间字段

单一候选合并后，新 `Candidate Legality Review Record` 的候选载荷必须直接绑定：

```text
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Review Act Observed At
Review Record Produced At
```

内容同一登记外壳必须另外绑定：

```text
Review Registered At
Legality Review Registration Authority Grant Reference
Candidate Review Payload Digest
Registered Review Payload Digest
Registered Review Record Digest
```

候选记录不得预填或预测 `Review Registered At`。登记时间属于登记归因外壳，不得进入需要与候选保持内容同一的规范审查载荷。

新记录不得继续用 `Review Effective At`、`Review As Of` 或 `Reviewed At` 作为规范字段。

旧字段只能保存在原历史记录或迁移审计载荷中。

### DM-R4-26 合法性投影键只能消费规范化时间

`Current Legality Review Projection Key` 在 `R3` 基础上规范为：

```text
Reviewed Decision Fact ID
Review Mode
Reviewed Historical Validity Coordinate
Review Knowledge Boundary Vector
Original Institution Version
Review Rule Compatibility Domain Snapshot
Source Set Boundary
Correction View Reference
Projection Rule Version
```

进入投影的每项旧审查记录必须引用：

```text
Registered Legality Review Temporal Normalization Record
```

新审查记录可以直接使用规范字段，但仍必须证明来源边界和规则兼容性。

### DM-R4-27 时间无法规范化时必须失败关闭

任何必需映射结果为：

```text
UNRESOLVED
```

则该审查记录：

```text
-/-> determinate Current Legality Review Projection
-/-> NON_COMPLIANT conclusion for invalidation request
-/-> historical knowledge claim
```

当前合法性投影必须为 `INDETERMINATE`，并保存未解析字段、来源记录、映射契约和已有证据。

### DM-R4-28 时间规范化不得伪造历史认识

```text
Later Mapping Contract
-/-> Earlier Knowledge

Later Registered Normalization
-/-> Historical Review Registration at Earlier Time

Current Reconstruction
-/-> Historical-as-known Mutation
```

时间规范化只解释旧字段在当前兼容契约中的可用含义，不证明当时系统已经拥有后来建立的映射规则或来源认识。

## 六、三项闭合后的规范因果路径

### DM-R4-29 ABORTED 证明消费路径

```text
Candidate Non-application Proof Record
  -> Candidate Proof Qualification Record
  -> Registered Proof Qualification Record
       -> DISQUALIFIED -> unavailable for ABORTED
       -> INDETERMINATE -> fail closed
       -> CONFLICTED -> fail closed and preserve conflict
       -> QUALIFIED -> Independent Applicability Resolution
            -> INAPPLICABLE -> unavailable for declared coordinate
            -> INDETERMINATE -> fail closed
            -> CONFLICTED -> fail closed and preserve conflict
            -> APPLICABLE -> Proof Qualification Projection
                 -> QUALIFIED + APPLICABLE + COMPLETE
                      -> may support Candidate Commit Resolution = ABORTED
                 -> otherwise
                      -> Candidate Commit Resolution = INDETERMINATE
```

### DM-R4-30 EXEMPT 消费路径

```text
Registered Exemption Basis Qualification Resolution = QUALIFIED
  -> Candidate Exemption Basis Applicability Resolution Record
  -> Registered Exemption Basis Applicability Resolution Record
  -> Exemption Basis Applicability Projection
       -> INAPPLICABLE -> no EXEMPT at declared coordinate
       -> INDETERMINATE -> Composite Resolution = INDETERMINATE
       -> CONFLICTED -> Composite Resolution = INDETERMINATE and preserve conflict
       -> APPLICABLE + COMPLETE + no conflict
            -> Composite Resolution may be EXEMPT
```

### DM-R4-31 合法性审查时间消费路径

```text
Legacy Registered Legality Review Record
  -> Candidate Legality Review Temporal Normalization Record
  -> Registered Legality Review Temporal Normalization Record
       -> Any required UNRESOLVED
            -> Current Legality Review Projection = INDETERMINATE
       -> Complete normalized temporal fields
            -> Stable Current Legality Review Projection Key
            -> Versioned Legality Review Projection

New Legality Review Record
  -> Canonical temporal fields at creation
  -> Stable Current Legality Review Projection Key
```

任何路径都不能创建失效决策、传播依赖失效或修改原决策事实。

## 七、非法状态候选增补

以下情况在未来合并与冻结时必须明确为非法：

- 使用 `NOT_QUALIFIED` 和 `NOT_APPLICABLE` 作为规范证明枚举；
- 没有兼容记录时把旧候选值静默改名；
- 把 `CONFLICTED` 折叠为普通 `INDETERMINATE`；
- 资格投影键同时填写精确契约和兼容域快照；
- 资格投影键既没有精确契约也没有兼容域快照；
- 资格投影键省略视图模式；
- 历史认识投影消费认识边界之后登记的来源；
- 适用性冲突和资格冲突被合并成一个无类型字段；
- 豁免资格记录直接建立当前适用性；
- 豁免适用性候选由同一授权自行登记；
- 缺少豁免适用性投影时建立 `EXEMPT`；
- 用来源缺失建立 `INAPPLICABLE`；
- 覆盖旧豁免适用性记录来表达当前变化；
- 把 `Reviewed At` 默认解释为认识截点或记录产生时间；
- 用单一 `Review As Of` 时间戳冒充完整认识边界向量；
- 时间规范化执行者补写来源或修改原审查记录；
- 未解析时间记录进入确定性合法性投影；
- 当前规范化结果被展示为历史当时已经知道。

发现任一状态时必须失败关闭，保留历史记录、候选记录、登记记录、冲突、未解析字段和证据。

## 八、对 R3 独立复审阻断的修订映射

| `R3` 复审阻断 | `R4` 修订位置 | 候选闭合方式 |
|---|---|---|
| 证明资格和适用性接口与提交候选不兼容 | `DM-R4-01` 至 `DM-R4-10` | 统一四值枚举、保留冲突、严格作用域模式、视图键和完整 `ABORTED` 条件 |
| 豁免依据适用性记录契约不完整 | `DM-R4-11` 至 `DM-R4-18` | 候选记录、内容同一登记、稳定键、追加谱系、当前投影和完整 `EXEMPT` 链 |
| 合法性审查记录与投影双时间缺少规范映射 | `DM-R4-19` 至 `DM-R4-28` | 五时间字段、版本化映射契约、逐字段结果、规范化登记和失败关闭 |

## 九、冻结与合并前依赖

本候选即使通过独立模型复审，也不能自动合并或冻结。至少仍需：

```text
Independent R2 + R3 + R4 Composite Consistency Review
Single Candidate Consolidation
Post-consolidation Semantic Diff Review
Frozen or compatible Source Registry Interface
Frozen or compatible Qualification Governance
Frozen or compatible Authority Applicability Governance
Frozen or compatible Derived Record Registration Authority Governance
Frozen or compatible Proof and Exemption Applicability Governance
Frozen or compatible Temporal Mapping Governance
Frozen or compatible Institution Registry and Freeze Reference Support
Compatible protected write implementation contract
Repeated and stable runtime evidence
Cross-provider evidence
Cross-project and cross-domain evidence
Applicable Freeze Authority
Independent Freeze Review
Freeze Decision
Successful Institution Commit
```

## 十、候选自检状态

```text
Proposal Completeness: PASS
Single Purpose: PASS
R3 Review Blocker Mapping: COMPLETE
Proof Qualification Value Compatibility: DEFINED
Proof Applicability Value Compatibility: DEFINED
Proof Conflict Preservation: DEFINED
Qualification Projection Scope Identity: DEFINED
Qualification Projection View Identity: DEFINED
Exemption Applicability Candidate Contract: DEFINED
Exemption Applicability Registration Contract: DEFINED
Exemption Applicability Lineage: DEFINED
Exemption Applicability Projection: DEFINED
Legality Review Canonical Temporal Fields: DEFINED
Legacy Review Temporal Mapping Contract: DEFINED
Legality Record / Projection Key Mapping: DEFINED
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Independent Model Review: REQUIRED
Consolidation Readiness: NOT_EVALUATED
Model-level Freeze Readiness: NOT_EVALUATED
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

这些自检只说明本草案已逐项给出候选契约，不构成独立复审结论、合并决定或冻结决定。

## 当前决定

1. 保留 `CR-0002-R2`、`CR-0002-R3` 及其独立审查记录作为不可覆盖历史；
2. 将本文件登记为 `CR-0002-R4` 有界纠偏候选；
3. 不修改已经通过的派生登记权威拓扑、组合单槽位结构、更正投影主干和失败分支类型修复；
4. 不修改 `IF-0001` 至 `IF-0007`；
5. 不使 `CR-0003` 候选获得冻结制度权威；
6. 不创建 `foundation/07_Decision.md`；
7. 不创建运行时证明、豁免、审查、登记、投影或决策事实；
8. 不创建冻结标识、冻结权威或冻结决定；
9. 下一步只对 `R2 + R3 + R4` 组合候选执行独立模型一致性复审；
10. 组合复审通过后仍需合并为单一候选并执行合并后语义差异审查；
11. 在正式冻结以前，本文件不可执行且没有制度权威。
