# 资格治理有界修订 R3：消费契约与结果层闭合

## 修订信息

```text
Proposal ID: CR-0007-R3
Title: Consumer Contract and Qualification Result Layer Closure
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0007-R2 QUALIFICATION AND APPLICABILITY RESEPARATION
Repair Basis: CR-0007-R2-CR-0002-CR-0003-CONSUMER-INTERFACE-COMPATIBILITY-REVIEW
Repair Scope: XQG-CONS-B1 + XQG-CONS-B2 + XQG-CONS-B3 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Consumer Interface Compatibility Re-review Required: YES
Independent Model Review Required: YES_AFTER_INTERFACE_PASS
Institution Freeze Created: NO
Freeze ID Created: NO
Qualification Registry Created: NO
Qualification Resolution Created: NO
Compatibility Domain Snapshot Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
Compatibility Reference: CR-0003-R7 QUALIFICATION COMPATIBILITY CLOSURE
```

> 本文件只修复资格结果层、证明资格契约作用域和前向解释身份。它不修改已经通过的来源／时间接口，不执行资格投影，不创建提交结果、适用性、闭包、制度冻结或运行时权威。

## 一、修订边界

### QG-R3-01 R3 只覆盖三项消费接口阻断

```text
XQG-CONS-B1 Atomic Qualification and Conflict Projection Layer Collapse
XQG-CONS-B2 Commit-contract Scope and Rule-domain Identity Collapse
XQG-CONS-B3 Proof and Commit Scope Identity Omission
```

### QG-R3-02 R3 覆盖基础稿的冲突条款

以下条款与本修订冲突的部分由 R3 覆盖：

```text
QG-C-05
QG-C-08
QG-C-22 through QG-C-25
QG-C-27 through QG-C-31
QG-C-36 through QG-C-47
QG-C-58
QG-C-59
QG-C-64
QG-C-65
QG-C-69
QG-C-71
QG-C-72
Current Decision
```

R1/R2 的上游消费身份和资格／适用性分离继续有效。

## 二、资格结果层分离

### QG-R3-03 单次资格计算结果必须保持三值

```text
Atomic Qualification Outcome =
  QUALIFIED
  | DISQUALIFIED
  | INDETERMINATE
```

一次 `Qualification Computation Attempt` 只能产生一个三值 `Candidate Atomic Qualification Resolution`。计算者不能产生 `CONFLICTED`。

### QG-R3-04 原候选和登记对象收紧为原子记录

基础稿中的：

```text
Candidate Qualification Resolution
Registered Qualification Resolution
```

在复合模型中分别解释为：

```text
Candidate Atomic Qualification Resolution
Registered Atomic Qualification Resolution
```

候选和登记载荷必须内容同一。登记者不能聚合多个候选、选择冲突赢家或把三值改为四值。

### QG-R3-05 原子记录必须绑定完整稳定键

`Registered Atomic Qualification Resolution` 继续绑定 R1/R2 的完整资格稳定键、输入包和消费元组，并至少增加：

```text
Atomic Qualification Outcome
Atomic Result Algebra Version
Qualification Result Layer = ATOMIC_HISTORY
Candidate Atomic Payload Digest
Registered Atomic Payload Digest
Atomic Record Digest
```

### QG-R3-06 四值只属于独立聚合或投影层

```text
Qualification Aggregate / Projection Outcome =
  QUALIFIED
  | DISQUALIFIED
  | INDETERMINATE
  | CONFLICTED
```

```text
CONFLICTED
  -/-> Atomic Qualification Outcome
```

### QG-R3-07 资格冲突聚合必须拥有独立身份

```text
Qualification Conflict Aggregate Semantic Key =
  Atomic Qualification Resolution Key without Record ID
+ Qualification Semantic Domain
+ Qualification Consumer Profile
+ Exact Atomic Record Evaluation Boundary ID and Digest
+ Required Boundary Completeness Resolution IDs and Digests
+ Aggregate Rule Version
```

候选聚合、登记尝试和已登记聚合必须与原子记录分账本、分类型和分授权。

### QG-R3-08 聚合必须消费完整原子记录集合

`Registered Qualification Conflict Aggregate Resolution` 至少绑定：

```text
Qualification Conflict Aggregate Semantic Key and Digest
Exact Registered Atomic Qualification Resolution ID-and-digest Set
Exact Atomic Record Set Digest
Registered Atomic Record Evaluation Boundary ID and Digest
Required Evaluation-boundary Completeness Resolution IDs and Digests
Atomic Record Set Equality Proof Reference
Qualification Aggregate Outcome
Included QUALIFIED Record References
Included DISQUALIFIED Record References
Included INDETERMINATE Record References
Qualification Conflict References or NOT_APPLICABLE
Candidate Aggregate Payload Digest
Registered Aggregate Payload Digest
Aggregate Execution Authority Reference
Aggregate Registration Authority Reference
Aggregate Rule Version
Registered Aggregate Record Digest
```

### QG-R3-09 聚合真值表必须完备

在同一完整、可比较原子作用域内：

```text
QUALIFIED only -> QUALIFIED
DISQUALIFIED only -> DISQUALIFIED
QUALIFIED + DISQUALIFIED -> CONFLICTED
INDETERMINATE only -> INDETERMINATE
Required boundary, compatibility or set equality unresolved -> INDETERMINATE
No atomic records -> INDETERMINATE
```

原子记录的适用性聚合属于后续模型；本聚合只表达同一原子资格作用域内的登记冲突，不创建当前适用性结论。

### QG-R3-10 原子和聚合权威不得传播

```text
Atomic Qualification Computation Authority
  != Atomic Qualification Registration Authority
  != Qualification Conflict Aggregate Execution Authority
  != Qualification Conflict Aggregate Registration Authority
  != Qualification Projection Authority
```

## 三、消费结果信封

### QG-R3-11 四值证明资格消费必须声明结果来源种类

`Registered Proof Qualification Consumer Envelope` 至少绑定：

```text
Proof Qualification Consumer Envelope ID and Digest
Qualification Result Source Kind
Registered Atomic Qualification Resolution ID and Digest or NOT_APPLICABLE
Registered Qualification Conflict Aggregate Resolution ID and Digest or NOT_APPLICABLE
Qualification Outcome
Candidate Proof ID and Payload Digest
Commit Attempt ID
Commit Key
Decision Key when required
Commit Contract ID and Version
Qualification Rule ID and Version
Validity As Of
Knowledge Boundary Vector
Source and Evidence References
Consumer Mapping Rule Version
Envelope Construction Authority Reference
```

### QG-R3-12 结果来源种类必须互斥

```text
ATOMIC_REGISTERED_QUALIFICATION
REGISTERED_QUALIFICATION_CONFLICT_AGGREGATE
```

```text
ATOMIC_REGISTERED_QUALIFICATION
  -> Outcome = QUALIFIED | DISQUALIFIED | INDETERMINATE
  -> Aggregate field = NOT_APPLICABLE

REGISTERED_QUALIFICATION_CONFLICT_AGGREGATE
  -> Outcome = QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED
  -> Atomic field = NOT_APPLICABLE
```

只有第二种来源可以输出 `CONFLICTED`。

### QG-R3-13 `CR-0002` 依据资格继续使用三值原子适配

`Registered Basis Qualification Resolution` 只消费原子资格或确定的非冲突聚合：

```text
QUALIFIED -> QUALIFIED
DISQUALIFIED -> NOT_QUALIFIED
INDETERMINATE -> INDETERMINATE
CONFLICTED aggregate -> INDETERMINATE + Conflict References
```

### QG-R3-14 `CR-0003` 历史证明资格只消费原子记录

```text
CR-0003 Historical Registered Proof Qualification
  -> Registered Atomic Qualification Resolution only
  -> three-value
```

四值冲突只进入 `Registered Proof Qualification Consumer Envelope` 的聚合来源或后续 `Proof Qualification Projection`，不能改写历史原子记录。

## 四、证明资格契约作用域

### QG-R3-15 通用规则作用域与证明消费作用域必须分离

基础稿的规则级模式可以保留给非提交语义域，但 `PROOF_QUALIFICATION` 消费接口只允许：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

以下基础稿名称不得出现在证明资格消费键：

```text
EXACT_QUALIFICATION_RULE_VERSION
QUALIFICATION_COMPATIBILITY_DOMAIN_SNAPSHOT
```

### QG-R3-16 精确契约模式必须固定契约和规则绑定

```text
Qualification Scope Mode = EXACT_CONTRACT_VERSION
  -> Exact Commit Contract ID and Version required
  -> Exact Commit Contract Payload Digest required
  -> Exact Qualification Rule ID and Version bound by contract required
  -> Contract-to-rule Binding Digest required
  -> Compatibility Domain fields = NOT_APPLICABLE
```

同一规则被多个契约引用时，各契约仍形成不同证明资格消费作用域。

### QG-R3-17 证明资格兼容域必须以提交契约成员为主身份

`Proof Qualification Compatibility Domain Snapshot` 至少绑定：

```text
Compatibility Domain ID and Version
Qualification Semantic Domain = PROOF_QUALIFICATION
Exact Member Commit Contract IDs and Versions
Exact Member Commit Contract Payload Digests
Exact Per-member Qualification Rule ID-and-version Bindings
Exact Contract-to-rule Binding Set Digest
Exact Required Directional Qualification Compatibility Record References
Exact Member Commit Contract Set Digest
Membership Digest
Membership Rule Version
Governing Institution ID and Version
Institution Freeze Reference
Established At
Validity As Of
Knowledge Boundary Vector
Snapshot Digest
```

### QG-R3-18 兼容域模式必须绑定不可变证明域快照

```text
Qualification Scope Mode = COMPATIBILITY_DOMAIN_SNAPSHOT
  -> Proof Qualification Compatibility Domain Snapshot required
  -> Exact Contract Version field = NOT_APPLICABLE
```

成员契约、契约载荷、规则绑定或方向兼容关系变化都必须产生新域版本、新摘要和新投影键。

### QG-R3-19 规则兼容不能反向证明契约兼容

```text
Same Qualification Rule Q1 used by Contracts C1 and C2
  -/-> C1 and C2 are in same proof qualification compatibility domain
```

契约成员资格必须有独立制度决定和逐方向兼容证据。

## 五、证明资格稳定键

### QG-R3-20 证明资格投影键必须与提交消费者内容同一

```text
Proof Qualification Projection Key =
  Candidate Proof ID and Payload Digest
+ Commit Key
+ Commit Attempt ID
+ Decision Key when required
+ Qualification Scope Mode
+ Exact Commit Contract ID and Version or Proof Qualification Compatibility Domain Snapshot ID and Digest
+ Qualification Rule Compatibility Domain ID and Version
+ Validity As Of
+ Knowledge Boundary Vector
+ Projection View Mode
+ Source Boundary and Correction Representation Digests
+ Qualification Projection Rule Version
```

任一项变化必须形成新键。

### QG-R3-21 一般主体和依据引用不能替代证明／提交身份

```text
Qualification Subject ID
+ Qualification Basis ID
  -/-> Candidate Proof ID + Commit Key
```

证明语义域必须同时保存一般资格身份和专用证明／提交身份。

## 六、前向解释专用契约

### QG-R3-22 证明资格前向解释必须固定完整提交作用域

`Proof Qualification Forward Interpretation Contract` 至少绑定：

```text
Forward Interpretation Contract ID and Version
Qualification Semantic Domain = PROOF_QUALIFICATION
Candidate Proof ID Scope Contract
Commit Key Scope Contract
Commit Attempt Scope Contract
Decision Key Scope Contract when required
Qualification Scope Mode
Exact Commit Contract Scope or Compatibility Domain Scope
Source Qualification Rule ID, Version and Digest
Target Qualification Interpretation Rule ID, Version and Digest
Total Deterministic Qualification Mapping
Qualification Epistemic Strength Mapping
Field Presence Preservation
Proof Payload Reference Preservation
Evidence Reference Preservation
Atomic Qualification Record Reference Preservation
Conflict Aggregate Reference Preservation
Validity and Knowledge Boundary Preservation
Mapping Rule Version
Compatibility Evidence References
Institution Freeze Reference
Canonical Payload Digest
```

### QG-R3-23 每次证明资格解释必须保持七类身份

```text
Same Candidate Proof ID and Payload Digest
Same Commit Key
Same Commit Attempt ID
Same Decision Key when required
Same Qualification Scope Mode
Same exact Commit Contract Version or same Proof Qualification Compatibility Domain Snapshot
Same Validity As Of and Knowledge Boundary Vector
```

还必须保持相同投影视图模式和来源／更正表示坐标。

### QG-R3-24 身份变化必须重新资格计算

上述任何身份变化都必须：

```text
REQUIRES_RERESOLUTION
+ Required Re-resolution Kind = REQUALIFICATION
  -> New Qualification Input
  -> New Atomic Candidate
  -> Independent Atomic Registration
  -> New Applicability and Closure
  -> New Projection
```

前向解释器不能迁移证明、提交键、契约作用域或认识边界。

### QG-R3-25 非放大真值表保持

原子解释只允许：

```text
INDETERMINATE -> INDETERMINATE
QUALIFIED -> QUALIFIED or INDETERMINATE
DISQUALIFIED -> DISQUALIFIED or INDETERMINATE
```

聚合／投影解释另允许：

```text
CONFLICTED -> CONFLICTED or INDETERMINATE
```

不得把聚合 `CONFLICTED` 映射为原子记录。

## 七、反例闭合

### QG-R3-26 单条资格冲突反例

```text
Atomic A = QUALIFIED
Atomic B = DISQUALIFIED

Expected:
  A and B remain immutable three-value records
  Aggregate = CONFLICTED
  no atomic CONFLICTED record
```

### QG-R3-27 同规则不同契约反例

```text
Contract C1 -> Rule Q1
Contract C2 -> Rule Q1

Expected:
  Exact-contract Key C1 != Exact-contract Key C2
  Rule identity alone cannot merge scopes
```

### QG-R3-28 同证明不同提交键反例

```text
Same proof payload P
Commit Key K1 != K2

Expected:
  Projection Key 1 != Projection Key 2
  Forward interpretation across K1/K2 = PROHIBITED
  Requalification required
```

## 八、非法状态增补

### QG-R3-29 以下状态必须失败关闭

- 单次资格计算输出 `CONFLICTED`；
- 登记者把多个原子候选压缩为一条资格记录；
- 聚合记录覆盖原子历史；
- `CONFLICTED` 信封引用原子来源种类；
- 证明资格键使用规则级作用域模式名称；
- 兼容域只枚举资格规则而不枚举提交契约；
- 相同资格规则反向证明提交契约兼容；
- 前向解释缺少候选证明、提交键或契约作用域；
- 相同证明载荷跨提交键复用资格投影；
- 聚合权威继承原子计算或投影发布权威；
- 兼容域成员变化复用旧摘要或投影键。

## 九、候选级闭合声明

### QG-R3-30 R3 只声明三项阻断具备候选修复

```text
XQG-CONS-B1 Atomic / Aggregate Result Layer Separation: CLOSED_AS_DRAFT
XQG-CONS-B2 Commit-contract Qualification Scope: CLOSED_AS_DRAFT
XQG-CONS-B3 Proof / Commit Forward-interpretation Identity: CLOSED_AS_DRAFT
CR-0002 Basis Qualification Interface: PRESERVED
CR-0003 Atomic Historical Qualification: MAPPED_AS_DRAFT
CR-0003 Four-value Qualification Projection: MAPPED_AS_DRAFT
Consumer Interface Compatibility Re-review: REQUIRED
Independent Qualification Model Review: BLOCKED_PENDING_INTERFACE_REVIEW
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0007-R3 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: XQG-CONS-B1 + XQG-CONS-B2 + XQG-CONS-B3
Proposal Revision Created: YES
Consumer Interface Compatibility Re-review: REQUIRED
Independent Qualification Model Review: NOT_READY
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Qualification Registry: NOT_CREATED
Qualification Resolution: NOT_CREATED
Compatibility Domain Snapshot: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须对 `CR-0007 + R1 + R2 + R3` 与 `CR-0002`、`CR-0003` 重新执行消费接口兼容审查。只有三项阻断全部独立关闭，才能进入资格模型独立审查。
