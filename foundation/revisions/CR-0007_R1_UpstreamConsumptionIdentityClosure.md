# 资格治理有界修订 R1：上游消费身份闭合

## 修订信息

```text
Proposal ID: CR-0007-R1
Title: Upstream Consumption Identity Closure
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0007 QUALIFICATION GOVERNANCE
Repair Basis: CR-0007-CR-0005-R11-CR-0006-R10-UPSTREAM-CROSS-INTERFACE-COMPATIBILITY-REVIEW
Repair Scope: XQG-B1 + XQG-B2 + XQG-B3 + XQG-B4 only
Repair Path for XQG-B3: CONSUMER-SIDE SR-C-16 REFERENCE PACKAGE
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Upstream Cross-interface Re-review Required: YES
Decision and Commit Interface Compatibility Review Required: YES_AFTER_UPSTREAM_PASS
Independent Model Review Required: YES_AFTER_INTERFACE_PASS
Institution Freeze Created: NO
Freeze ID Created: NO
Source Registry Created: NO
Temporal Registry Created: NO
Qualification Registry Created: NO
Qualification Rule Created: NO
Qualification Resolution Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0005-R11 Source Registry Interface Composite
Depends On: CR-0006-R10 Temporal Mapping Governance Composite
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
```

> 本文件只修复 `CR-0007` 对来源和时间终局接口的四个上游消费阻断。它不覆盖 `CR-0007` 未涉及这四项的正文，不修改 `CR-0005` 或 `CR-0006`，不创建来源排除决定、查询坐标、完整性结论、资格结果、制度冻结或运行时权威。

## 一、修订解释边界

### QG-R1-01 R1 只覆盖四个已确认阻断

```text
XQG-B1 Temporal Query Coordinate Subject Identity Omission
XQG-B2 Source Completeness Aggregate Tuple Underpinning
XQG-B3 Undefined Source Exclusion Provider Registration Topology
XQG-B4 Undefined Source Correction Consumer Object
```

本修订不提前处理 `CR-0002` 三值依据接口、`CR-0003` 四值证明资格接口、资格登记全模型或制度冻结准备度。

### QG-R1-02 R1 是有界覆盖层

以下 `CR-0007` 条款中与本修订冲突的部分由 R1 覆盖：

```text
QG-C-05
QG-C-08
QG-C-09
QG-C-10
QG-C-14
QG-C-18
QG-C-19
QG-C-21
QG-C-22
QG-C-27
QG-C-29
QG-C-32
QG-C-33
QG-C-34
QG-C-52
QG-C-56
QG-C-57
QG-C-63
QG-C-66
QG-C-69
QG-C-70
QG-C-72
Current Decision
```

其他 `CR-0007` 规则继续作为复合候选语义。本修订不删除原文件，历史审查记录永久保留。

### QG-R1-03 四类泛化字段不再具有消费资格

以下字段单独出现时不再是合格资格输入：

```text
Temporal Query Coordinate Q Reference and Digest without S + RR
Registered Source Completeness Aggregate References
Registered Institutional Source Exclusion Basis References
Source Correction View References
```

它们不得保留为兼容别名、可选简写或只进入证据包而不进入稳定身份。

## 二、R1 新增消费值对象

### QG-R1-04 新增对象只表达消费身份，不创建上游事实

| 对象 | 类型 | 唯一目的 | 逻辑真源或边界 |
|---|---|---|---|
| `Qualification Temporal Coordinate Consumption Tuple` | 复合消费值 | 固定四值坐标主体、登记解析和唯一坐标分支 | `CR-0005-R3 + CR-0006-R2` 接口 |
| `Qualification Required Source Completeness Set` | 规则派生值 | 固定资格规则要求的来源完整性维度 | 资格规则契约 |
| `Qualification Source Completeness Aggregate Tuple` | 复合消费值 | 把一个必要维度映射到精确来源聚合解析 | `CR-0005-R4` 接口 |
| `Qualification Source Completeness Consumption Bundle` | 不可变消费集合 | 固定全部必要聚合元组和集合相等证明 | 资格输入边界 |
| `SR-C-16 Source Exclusion Basis Reference Package` | 只读引用包 | 内容同一包装 `SR-C-16` 已要求的排除依据字段 | `CR-0005 SR-C-16` 和 `IF-0007` |
| `Source Exclusion Basis Qualification Resolution` | 不可变资格记录 | 判断只读排除依据包是否满足精确资格规则 | 资格解析账本 |
| `Historical Source Correction Consumption Tuple` | 历史消费值 | 固定认识边界内的已登记来源更正记录集合 | `CR-0005` 来源更正账本 |
| `Current Source View Consumption Tuple` | 当前消费值 | 固定可重建当前来源读面的载荷和全部谱系 | `CR-0005 Source Registry Current View` |
| `Qualification Source Representation Consumption Tuple` | 互斥消费值 | 按视图模式选择历史更正集合或当前读面 | 资格输入边界 |

这些对象都不能分配来源身份、登记上游记录、改变来源作用域、创建时间坐标或证明上游完整性。

### QG-R1-05 新增消费值不取得上游登记权威

R1 不新增以下权威：

```text
Source Exclusion Basis Registration Authority Type
Source Exclusion Decision Authority Type
Source Correction Registration Authority Type
Source Registry Current View Publication Authority Type
Source Completeness Evaluation or Aggregate Authority Type
Temporal Query Coordinate Registration Authority Type
```

`Qualification Input Assembly Authority` 可以内容同一组装消费元组和引用包，但不能改变其中任何上游字段或结论。

## 三、关闭 XQG-B1：四值查询坐标主体消费

### QG-R1-06 时间坐标必须作为完整消费元组进入资格输入

`Qualification Temporal Coordinate Consumption Tuple` 至少绑定：

```text
Temporal Query Coordinate Subject Reference and Digest
Coordinate Subject State
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Coordinate Registration Resolution Result
Temporal Query Coordinate Key
Registered Normative Coordinate Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Observed Candidate Normative Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Coordinate Conflict Set Digest or NOT_APPLICABLE or NOT_ESTABLISHED
Registered Temporal Query Coordinate ID and Payload Digest or NOT_APPLICABLE
Canonical Valid At Value ID and Digest or NOT_ESTABLISHED
Registered Knowledge Boundary Vector K ID and Digest or NOT_ESTABLISHED
K.Registered Source Boundary Vector B ID and Digest or NOT_ESTABLISHED
K.Registered Temporal Governance Boundary Vector T ID and Digest or NOT_ESTABLISHED
Temporal View Mode or NOT_ESTABLISHED
Subject Reference Rule Version
Coordinate Consumption Tuple Canonical Digest
```

主体引用、登记解析、载荷集合、`Q`、`K`、`T`、`B` 和视图字段必须来自同一上游解析载荷，不得在消费侧拆分后与当前查询结果重组。

### QG-R1-07 四个主体分支必须完备且互斥

```text
REGISTERED_SINGLETON
QUALIFIED_NOT_REGISTERED
INDETERMINATE_SUBJECT
CONFLICTED_SUBJECT
```

每个消费元组必须且只能属于一个分支。未知已登记集合、候选集合或冲突集合必须使用 `NOT_ESTABLISHED`，不能伪装为 `EMPTY_SET`。

### QG-R1-08 只有登记单例分支可以支持确定资格终局

```text
Coordinate Subject State = REGISTERED_SINGLETON
+ Coordinate Registration Resolution Result = REGISTERED
+ exactly one Registered Q ID and Payload Digest
+ Q payload content-identical with subject and RR
+ K/B/T/View fields content-identical with Q
  -> Temporal Input Eligibility = ELIGIBLE_FOR_TERMINAL_QUALIFICATION
```

任何字段缺失、载荷不一致或跨边界重组必须失败关闭。

### QG-R1-09 非登记单例分支确定资格认识上限

```text
QUALIFIED_NOT_REGISTERED
  -> Qualification Outcome = INDETERMINATE

INDETERMINATE_SUBJECT
  -> Qualification Outcome = INDETERMINATE

CONFLICTED_SUBJECT
  -> Qualification Outcome = INDETERMINATE
  -> Temporal Input Conflict References required
```

`CONFLICTED_SUBJECT` 不直接等于资格结果 `CONFLICTED`。只有同一完整资格稳定键内出现可比较相反资格终局时，资格聚合才可为 `CONFLICTED`；坐标层冲突必须独立保存。

### QG-R1-10 坐标消费元组摘要必须进入稳定键

`CR-0007` 的 `Qualification Resolution Key` 由 R1 收紧为：

```text
Qualification Resolution Key =
  Qualification Purpose
+ Qualification Subject ID and Version
+ Qualification Basis ID and Version
+ Qualification Rule ID and Version
+ Qualification Semantic Domain
+ Registered Source Boundary Vector B ID and Digest
+ Qualification Temporal Coordinate Consumption Tuple Digest
+ Qualification Source Completeness Consumption Bundle Digest
+ Qualification Source Representation Consumption Tuple Digest
+ Source Exclusion Basis Reference Package Digest or NOT_APPLICABLE
+ Qualification Input Package Digest
```

主体状态、登记解析、任何载荷集合摘要、`Q`、`K`、`T`、`B` 或视图变化必须形成新的资格身份。

## 四、关闭 XQG-B2：来源完整性聚合元组固定

### QG-R1-11 资格规则必须固定精确必要完整性集合

```text
Qualification Required Source Completeness Set Key =
  Qualification Rule ID and Version
+ Qualification Purpose and Semantic Domain
+ Registered Source Boundary Vector B ID and Digest
+ Exact Query Scope Digest
+ Boundary Shape
+ Exact Required Dimension ID-and-version Set Digest
+ Exact Required Source Completeness Semantic Domain Key Set Digest
+ Requirement Mapping Rule Version
```

必要维度集合必须来自规则契约，不能由资格计算者、输入组装者或结果登记者临时缩小。

### QG-R1-12 每个必要维度必须映射到精确来源聚合元组

```text
Qualification Source Completeness Aggregate Tuple =
  Required Dimension ID and Version
+ Source Completeness Semantic Domain Key and Digest
+ Registered Source Completeness Aggregate Resolution ID and Digest
+ Source Completeness Aggregate Result
+ Registered Source Completeness Evaluation Boundary ID and Digest
+ Required Evaluation-boundary Completeness Resolution IDs and Digests
+ Exact Source Boundary and Query Scope References
+ Tuple Canonical Digest
```

上游聚合结果只允许：

```text
COMPLETE
INCOMPLETE
INDETERMINATE
CONFLICTED
```

资格治理只能验证和消费，不能重算、修正或登记这些结果。

### QG-R1-13 元组集合必须具有集合相等证明

`Qualification Source Completeness Consumption Bundle` 至少绑定：

```text
Qualification Required Source Completeness Set Key and Digest
Exact Required Dimension ID-and-version Set Digest
Exact Required Source Completeness Semantic Domain Key Set Digest
Exact Qualification Source Completeness Aggregate Tuple Set
Exact Qualification Source Completeness Aggregate Tuple Set Digest
Canonical Tuple Ordering Rule Version
Required-dimension-to-tuple One-to-one Mapping Proof Reference
Tuple Set Equality Proof Reference
Mapping Proof Authority Reference
Mapping Proof Registration Reference
Governed Mapping-proof Evidence Boundary ID and Digest
Bundle Construction Authority Reference
Bundle Canonical Digest
```

重复维度、遗漏维度、多对一歧义、额外替代元组、作用域不匹配或排序不规范都使消费包不合格。

映射证明构造、映射证明登记和消费包组装必须分别授权。任何主体都不能借集合相等证明重算来源完整性结果，也不能让消费包摘要自证元组集合完备。

### QG-R1-14 只有完整且无冲突的聚合元组集合可以支持终局资格

```text
Every required dimension
  -> exactly one applicable registered tuple
  -> Aggregate Result = COMPLETE
  -> evaluation boundary completeness resolved
  -> no tuple or payload conflict
+ Set Equality Proof = SATISFIED
  -> Source Completeness Input Eligibility = ELIGIBLE_FOR_TERMINAL_QUALIFICATION
```

失败上限：

```text
Any INCOMPLETE
  -> Qualification Outcome = INDETERMINATE

Any INDETERMINATE
  -> Qualification Outcome = INDETERMINATE

Any CONFLICTED
  -> Qualification Outcome = INDETERMINATE
  -> Source Completeness Conflict References required

Missing or extra tuple
  -> Qualification Outcome = INDETERMINATE
```

来源不完整不能证明主体 `DISQUALIFIED`；来源完整性冲突也不能直接替代资格终局冲突。

### QG-R1-15 底层完整性记录不得成为直接满足输入

```text
Exact Registered Source Completeness Record Set
  -> lineage only
  -/-> terminal qualification support
```

资格规则和输入包只能消费已登记聚合解析元组，不能选择底层有利评价或以相同字面 `COMPLETE` 替换不同聚合身份。

## 五、关闭 XQG-B3：来源排除只读引用边界

### QG-R1-16 R1 选择消费侧引用包路径

本修订不要求 `CR-0005` 新增来源排除注册表，也不声明 `WS-02` 已提供名为 `Registered Institutional Source Exclusion Basis` 的对象。

以下 `CR-0007` 声明不再具有候选资格：

```text
Institutional Source Exclusion Basis identity and registration authority belongs to WS-02
Registered Institutional Source Exclusion Basis References
Source Exclusion Basis Registration Authority inferred from SR-C-16
```

### QG-R1-17 排除依据只能内容同一包装 `SR-C-16` 字段

`SR-C-16 Source Exclusion Basis Reference Package` 至少绑定：

```text
Exclusion Basis ID and Version
Exact Registry Scope
Exact Source Type or Identity Scope
Valid Interval
Decision References
Authority References
Institution Freeze Reference
Evidence References
SR-C-16 Field Presence Verification
Reference Package Assembly Authority Reference
Reference Package Canonical Digest
```

包摘要是资格消费外壳的内容身份，不反向成为 `WS-02` 登记摘要。组装者不能补造排除决定、扩大作用域、改变有效窗口或登记上游对象。

### QG-R1-18 排除依据资格只评价引用包本身

`Source Exclusion Basis Qualification Resolution` 的主体只能是一个精确引用包：

```text
Qualification Resolution ID and Digest
SR-C-16 Source Exclusion Basis Reference Package Digest
Qualification Semantic Domain = SOURCE_EXCLUSION_BASIS_QUALIFICATION
Qualification Rule ID and Version
Qualification Temporal Coordinate Consumption Tuple Digest
Qualification Source Completeness Consumption Bundle Digest
Qualification Outcome and Conflict References
Computation and Registration Authority References
Evidence References
```

该结果只回答引用包是否满足资格规则，不创建来源排除决定，也不证明排除决定当前适用。

### QG-R1-19 一般资格计算不得应用新的来源排除

```text
Source Exclusion Basis Qualification = QUALIFIED
  -/-> remove Source Record from B
  -/-> mutate Source Snapshot
  -/-> change Source Completeness Tuple Set
  -/-> create Source Applicability
```

一般依据、证明、豁免或更正资格计算的规范来源集合必须由已登记 `B`、快照和必要完整性元组确定。资格计算者不得根据排除依据另行删源。

### QG-R1-20 来源排除只能由上游或后续独立适用性路径生效

合法效果路径只有：

```text
PATH_SOURCE_BOUNDARY
  SR-C-16 exclusion decision and authority references
  -> WS-02 registry scope / exclusion rule
  -> new registered Source Boundary and Snapshot B
  -> new T/K/Q/S/RR
  -> new Qualification identity

PATH_LATER_APPLICABILITY
  Qualified Source Exclusion Basis Reference Package
  + independent applicability governance
  -> registered applicability result
  -> downstream projection or closure consumption
  -/-> rewrite historical Qualification input
```

`WS-04` 不执行两条路径中的来源决定或适用性解析。

## 六、关闭 XQG-B4：来源更正和当前读面精确消费

### QG-R1-21 来源表示消费必须按视图模式二选一

```text
HISTORICAL_SOURCE_CORRECTION_SET
CURRENT_SOURCE_VIEW
```

每个 `Qualification Source Representation Consumption Tuple` 必须且只能选择一种模式。不得同时填写历史更正集合与当前读面，也不得两者都省略。

### QG-R1-22 历史模式必须固定认识边界内的已登记更正集合

`Historical Source Correction Consumption Tuple` 至少绑定：

```text
Temporal View Mode = HISTORICAL_AS_KNOWN
Qualification Temporal Coordinate Consumption Tuple Digest
Registered Source Boundary Vector B ID and Digest
Exact Registered Source Record ID-and-digest Set
Exact Registered Source Record Set Digest
Exact Registered Source Correction Record ID-and-digest Set
Exact Registered Source Correction Record Set Digest
Source Correction Key and Lineage References
Exact B-membership Proof for Correction Record Set
Qualification Source Completeness Consumption Bundle Digest covering correction semantic domain
Correction Conflict References or NOT_APPLICABLE
Historical Correction Consumption Rule Version
Tuple Canonical Digest
```

每个更正必须已经进入该 `K/Q` 认识边界。边界之后登记的更正不得进入历史元组。

### QG-R1-23 当前模式必须固定可重建读面及全部谱系

`Current Source View Consumption Tuple` 至少绑定：

```text
Temporal View Mode = CURRENT_RESTATED
Qualification Temporal Coordinate Consumption Tuple Digest
Registered Source Boundary Vector B ID and Digest
Consumer-reconstructed Source Registry Current View Payload Digest
Source Registry Current View Construction Rule Version
Current View Consumption Canonical Byte Contract ID and Version
Current View Consumption Digest Algorithm ID and Version
Exact Registered Source Record ID-and-digest Set Digest
Exact Registered Source Applicability Change Record ID-and-digest Set Digest
Exact Registered Source Correction Record ID-and-digest Set Digest
Exact Source Snapshot and Boundary References
Required Source Completeness Consumption Bundle Digest
Applicability and Correction Conflict References or NOT_APPLICABLE
Current View Reconstruction Evidence References
Current View Lineage Set Equality Proof Reference
Tuple Canonical Digest
```

`Source Registry Current View` 是可删除、可重建读面。该载荷摘要属于资格消费外壳，不声称是 `WS-02` 已登记对象摘要；它不能成为来源事实或适用性决定。资格输入必须同时固定规范字节契约、算法和全部重建谱系，不能只保存当前视图载荷。

### QG-R1-24 视图模式必须与时间坐标内容同一

```text
Source Representation Tuple.View Mode
= Qualification Temporal Coordinate Consumption Tuple.View Mode
= Registered K.View Mode
= Q.View Mode in REGISTERED_SINGLETON branch
```

不相等时输入必须 `INDETERMINATE`。当前读面不得与历史坐标组合，历史更正集合不得通过当前时间标签扩大。

### QG-R1-25 更正集合或当前读面变化必须形成新资格身份

以下任一变化都必须产生新的表示消费元组摘要和资格稳定键：

```text
Correction Record Set
Correction Conflict Set
Current View Payload
Current View Construction Rule
Current View Source Record Set
Current View Applicability Change Set
Current View Correction Set
Temporal Coordinate Consumption Tuple
Completeness Consumption Bundle
```

不得把后续更正作为原历史资格当时已知，也不得用当前读面覆盖原资格记录。

## 七、R1 收紧后的资格输入包

### QG-R1-26 输入包必须同时固定四类消费身份

`Qualification Input Package` 由 R1 收紧为：

```text
Input Package ID
Qualification Purpose and Semantic Domain
Qualification Subject Reference and Digest
Qualification Basis Reference and Digest
Qualification Rule ID, Version and Digest
Registered Source Boundary Vector B ID and Digest
Registered Source Snapshot IDs and Digests
Source Set Digest
Qualification Temporal Coordinate Consumption Tuple and Digest
Qualification Required Source Completeness Set Key and Digest
Qualification Source Completeness Consumption Bundle and Digest
Qualification Source Representation Consumption Tuple and Digest
SR-C-16 Source Exclusion Basis Reference Package and Digest or NOT_APPLICABLE
Source Exclusion Basis Qualification Resolution Reference or NOT_APPLICABLE
Evidence References and Digests
Contrary Source References
Input Package Assembly Authority Reference
Input Package Canonical Digest
```

一般资格目的必须把排除依据包和其资格解析标为 `NOT_APPLICABLE`。只有 `SOURCE_EXCLUSION_BASIS_QUALIFICATION` 可以填写两项，并且引用包同时成为精确资格主体。

### QG-R1-27 四类输入必须相互内容同一

```text
Input.B = Temporal Tuple.K.B
Input.B = Completeness Bundle.B
Input.B = Representation Tuple.B

Temporal Tuple = REGISTERED_SINGLETON branch
  -> Input.Q = Temporal Tuple.Registered Q

Input.View Mode = Temporal Tuple.View Mode
Input.View Mode = Representation Tuple.View Mode

Completeness Bundle.Required Dimensions
= Qualification Rule.Required Dimensions
```

任何不一致都不得通过输入包总摘要隐藏。

### QG-R1-28 候选和登记资格记录必须复制消费摘要

`Candidate Qualification Resolution` 和 `Registered Qualification Resolution` 必须共同绑定：

```text
Qualification Temporal Coordinate Consumption Tuple Digest
Coordinate Subject State
Coordinate Registration Resolution ID, Digest and Result
Qualification Source Completeness Consumption Bundle Digest
Exact Required Aggregate Tuple Set Digest
Qualification Source Representation Consumption Tuple Digest
Source Representation Mode
SR-C-16 Source Exclusion Basis Reference Package Digest or NOT_APPLICABLE
Input Package Digest
Temporal Input Conflict References
Source Completeness Conflict References
Source Correction or Current View Conflict References
```

候选和登记载荷摘要必须相等。登记者不能换用当前 `S`、`RR`、完整性聚合、更正集合或当前读面。

### QG-R1-29 确定资格终局必须通过全部输入门槛

```text
Temporal Input Eligibility = ELIGIBLE_FOR_TERMINAL_QUALIFICATION
+ Source Completeness Input Eligibility = ELIGIBLE_FOR_TERMINAL_QUALIFICATION
+ Source Representation Consumption = CONTENT_IDENTICAL_AND_COMPLETE
+ Qualification Rule = frozen, registered and applicable to exact input types
+ Subject and Basis = exact and allowed
+ Required Evidence = complete and conflict-free
+ No unresolved contrary source
  -> may compute QUALIFIED or DISQUALIFIED
```

任一门槛未成立时只能为 `INDETERMINATE`；同一完整稳定键内已有相反终局时由资格聚合保留 `CONFLICTED`。

## 八、权威、历史与无环边界

### QG-R1-30 输入组装权不能取得计算、登记或上游权威

```text
Input Assembly
  != Source Registration
  != Completeness Evaluation
  != Temporal Coordinate Registration
  != Qualification Computation
  != Qualification Registration
```

组装者只能复制精确上游载荷、按冻结规范排序并计算消费外壳摘要。

### QG-R1-31 R1 保持单向因果

```text
WS-02 Registered B and Source Governance Facts
  -> WS-03 Registered T/K/Q/RR/S
  -> WS-04 Consumption Tuples and Qualification
  -> later Applicability, Closure and Projection
```

```text
Qualification
  -/-> B, T, K, Q, RR or S mutation
Consumption Tuple
  -/-> upstream registration
Source Exclusion Qualification
  -/-> source removal
Current View Consumption
  -/-> source fact mutation
```

### QG-R1-32 历史成功和当前冲突必须形成不同资格身份

```text
RR0 = REGISTERED
S0 = REGISTERED_SINGLETON
Representation0 = HISTORICAL_SOURCE_CORRECTION_SET
  -> Qualification Key 0

RR1 = CONFLICTED
S1 = CONFLICTED_SUBJECT
Representation1 = CURRENT_SOURCE_VIEW or new historical boundary
  -> Qualification Key 1

Qualification Key 0 != Qualification Key 1
```

旧资格保留在历史坐标，当前冲突不能覆盖或复用旧终局。

## 九、必要反例闭合

### QG-R1-33 坐标登记演进反例

```text
Given:
  RR0 = REGISTERED, S0 = REGISTERED_SINGLETON
  RR1 = CONFLICTED, S1 = CONFLICTED_SUBJECT

Then:
  Temporal Tuple 0 Digest != Temporal Tuple 1 Digest
  Qualification Key 0 != Qualification Key 1
  Current terminal reuse = PROHIBITED
  Historical terminal preservation = REQUIRED
```

### QG-R1-34 不利完整性元组反例

```text
Required Dimensions = {A, B}
Tuple A = COMPLETE
Tuple B = CONFLICTED

Omit B
  -> Set Equality Proof = NOT_SATISFIED

Include B
  -> Source Completeness Input Eligibility = NOT_ELIGIBLE

Both paths
  -> Qualification Outcome = INDETERMINATE
```

### QG-R1-35 排除依据无来源效果反例

```text
SR-C-16 Reference Package exists
+ Source Exclusion Basis Qualification = QUALIFIED
+ no new WS-02 B
+ no later registered applicability result

Then:
  Source Set remains unchanged
  Exclusion Effect = NONE
```

### QG-R1-36 历史更正边界反例

```text
Q0/K0 excludes later Correction C1
Q1/K1 CURRENT_RESTATED includes C1

Historical Tuple 0 excludes C1
Current View Tuple 1 pins C1 lineage
Representation Tuple 0 Digest != Representation Tuple 1 Digest
Qualification Key 0 != Qualification Key 1
```

## 十、非法状态增补

### QG-R1-37 以下状态必须失败关闭

- 只凭 `Q` 标识或摘要支持确定资格；
- `S`、`RR` 与 `Q` 来自不同认识边界；
- 非 `REGISTERED_SINGLETON` 分支伪造已登记 `Q`；
- `REGISTERED_SINGLETON` 缺少唯一已登记 `Q`；
- 未知集合被表示为 `EMPTY_SET`；
- 主体状态或登记解析变化却复用旧资格键；
- 泛化完整性引用替代逐维度精确聚合元组；
- 省略不利必要维度后仍通过输入包摘要；
- 直接消费底层来源完整性评价支持终局；
- `INCOMPLETE` 被解释为主体 `DISQUALIFIED`；
- 资格消费方声明 `WS-02` 已有未定义的排除依据登记对象；
- 排除依据资格直接从 `B` 删除来源；
- 引用包摘要被反向解释为上游登记摘要；
- 使用未定义的 `Source Correction View References`；
- 历史视图消费认识边界之后的更正；
- 当前读面只保存载荷摘要而不保存重建谱系；
- 当前读面与历史坐标组合；
- 输入组装者重算来源完整性、登记坐标或执行资格计算；
- 新消费元组创建第二来源、时间或资格事实。

## 十一、候选级阻断闭合声明

### QG-R1-38 R1 只声明四项阻断已具备候选修复

```text
XQG-B1 Four-value Coordinate Subject Consumption: CLOSED_AS_DRAFT
XQG-B2 Source Completeness Aggregate Tuple Pinning: CLOSED_AS_DRAFT
XQG-B3 Source Exclusion Provider Topology: CLOSED_AS_DRAFT_BY_CONSUMER_PATH
XQG-B4 Source Correction Object Identity: CLOSED_AS_DRAFT
B -> T -> K -> Q -> Qualification Direction: PRESERVED
Second Query Coordinate: NOT_CREATED
Source Authority Propagation: NOT_CREATED
Temporal Authority Propagation: NOT_CREATED
Upstream Cross-interface Re-review: REQUIRED
CR-0002 / CR-0003 Consumer Compatibility Review: BLOCKED_PENDING_UPSTREAM_REVIEW
Independent Qualification Model Review: BLOCKED_PENDING_INTERFACE_REVIEWS
Institution Freeze Eligibility: FAIL
```

以上结论只是修订提案自检，不能关闭独立审查中的发现。

## 当前决定

```text
CR-0007-R1 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: XQG-B1 + XQG-B2 + XQG-B3 + XQG-B4
Proposal Revision Created: YES
Upstream Cross-interface Re-review: REQUIRED
CR-0002 / CR-0003 Consumer Compatibility Review: NOT_READY
Independent Qualification Model Review: NOT_READY
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Temporal Registry: NOT_CREATED
Qualification Registry: NOT_CREATED
Qualification Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须使用 `CR-0007 + CR-0007-R1` 对 `CR-0005-R11 + CR-0006-R10` 重新执行独立上游交叉接口兼容审查。只有 `XQG-B1` 至 `XQG-B4` 全部经独立复审关闭，才能进入 `CR-0002`／`CR-0003` 消费接口兼容审查。
