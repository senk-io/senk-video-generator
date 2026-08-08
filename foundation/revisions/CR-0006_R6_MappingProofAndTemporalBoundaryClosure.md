# 时间映射治理有界修订 R6

## 修订信息

```text
Proposal ID: CR-0006-R6
Title: Governed Mapping Proof and Temporal Boundary Consumption Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R5 GLOBAL TEMPORAL POSITION AND REQUIRED-DIMENSION SOURCE-DOMAIN MAPPING CLOSURE
Repair Basis: CR-0006-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R5-B1 + TM-R5-B2 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Independent Model Re-review Required: YES
Cross-interface Regression Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0005-R6
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R5-B1` 与 `TM-R5-B2`：为维度—来源语义域映射建立受治理证明资格，并把映射聚合消费固定到精确时间治理边界向量 `T`。它不覆盖基础稿或 R1 至 R5 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R6-01 R6 只覆盖两个有界阻断

```text
TM-R5-B1 Governed Mapping Proof Qualification
TM-R5-B2 Temporal Governance Boundary Pinning for Mapping Consumption
```

R5 已通过的全局位置模型、映射候选身份、竞争边界、聚合登记和来源聚合元组对齐继续有效。

### TM-R6-02 证明资格和时间边界不得自授权

```text
Mapping Candidate
  -/-> create or complete its own evidence boundary
  -/-> qualify its own semantic equivalence proof

Mapping Aggregate
  -/-> select its own Temporal Governance Boundary Vector T
  -/-> prove that no later or excluded record exists

Completeness Evaluation
  -/-> rewrite T or source completeness aggregate
```

证据边界来自 `IF-0006` 兼容权威；时间治理边界向量继续由 R1/R2 已分权角色构造和登记。

## 二、受治理映射证据边界

### TM-R6-03 映射证明必须固定受治理证据边界

每个映射证明资格候选必须固定：

```text
Governed Mapping Evidence Boundary ID and Digest
Evidence Boundary Scope
Exact Evidence Record Set Digest or First and Last Position
Evidence Canonicalization Rule Version
Evidence Boundary Completeness Resolution ID and Digest
```

证据边界作用域必须精确覆盖必要维度、目标来源完整性语义域、来源边界、快照、查询作用域、边界形态和映射适用区间。

空查询、读取成功、单一证明摘要或映射候选自身不能证明证据边界完整。

### TM-R6-04 证据边界完整性必须独立且分维度

最低必要维度为：

```text
CARRIER_INTEGRITY
POSITION_OR_EXACT_SET_COMPLETENESS
READ_COMPLETENESS
CONFLICT_SUBDOMAIN_COMPLETENESS
SEMANTIC_SCOPE_COVERAGE
```

每个维度使用 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。映射候选构造者、候选登记者、证明资格执行者和映射聚合者不得评价这些维度。

只有全部必要维度 `COMPLETE` 且内容同一，证据边界才可支持确定证明资格。

## 三、映射证明资格语义域

### TM-R6-05 证明资格语义键必须与证据载荷分离

```text
Dimension / Source-domain Mapping Proof Qualification Semantic Conflict Set Key =
  Required Dimension / Source Completeness Domain Mapping Semantic Conflict Set Key
+ Required Dimension Source-domain Mapping Candidate Key
+ Candidate Mapping Payload Digest
+ Target Source Completeness Semantic Domain Key and Digest
+ Registered Minimum Matrix Contract Registration Resolution ID and Digest
+ Registered Temporal Query Rule Contract Registration Resolution ID and Digest
+ Proof Qualification Semantic Rule Version
```

该键禁止包含证据边界 ID、证明摘要、资格候选 ID、结果、位置、登记时间和执行者。不同证据对同一映射候选的相反资格结论必须竞争。

### TM-R6-06 证明资格候选载荷必须完整

```text
Mapping Proof Qualification Candidate Payload =
  Mapping Proof Qualification Semantic Conflict Set Key
+ Governed Mapping Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
+ Dimension-to-domain Semantic Equivalence Proof ID and Digest
+ Source Boundary and Scope Coverage Proof ID and Digest
+ Boundary Shape Compatibility Proof ID and Digest
+ Proof Verification Rule Version
+ Candidate Qualification Result
+ Candidate Payload Canonicalization Rule Version
```

每个证明必须保存算法、输入、输出、失败、证据记录引用和验证谱系。摘要内容相同不替代证明身份、证据边界或验证结果。

### TM-R6-07 证明资格候选必须拥有稳定键

```text
Mapping Proof Qualification Candidate Key =
  Mapping Proof Qualification Semantic Conflict Set Key
+ Candidate Qualification Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。候选结果不进入语义冲突键，只进入候选载荷。

## 四、证明资格登记与聚合

### TM-R6-08 证明资格候选必须形成时间账本登记链

```text
Candidate Mapping Proof Qualification
  -> Proof Qualification Registration Attempt
  -> Registered Mapping Proof Qualification Record
     (Temporal Record Type = REQUIRED_DIMENSION_MAPPING_PROOF_QUALIFICATION)
  -> Registered Proof Qualification Candidate Registration Resolution
```

记录进入现有 `Temporal Mapping Ledger` 全局位置域。候选和登记载荷必须内容同一。

```text
Proof Qualification Candidate Registration Resolution Key =
  Mapping Proof Qualification Candidate Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_MAPPING_PROOF_QUALIFICATION Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

登记解析使用 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### TM-R6-09 证明资格竞争边界必须覆盖全部同域候选

```text
Mapping Proof Qualification Competing Boundary Key =
  Mapping Proof Qualification Semantic Conflict Set Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ Exact Proof Qualification Candidate Registration Resolution Set Digest
+ Required Proof-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖全部证据边界、证明、候选、登记尝试、记录、候选解析和冲突谱系。选择精确集合不得排除不利资格或相反证明。

### TM-R6-10 证明资格边界必须形成登记解析

```text
Candidate Mapping Proof Qualification Competing Boundary
  -> Proof Boundary Registration Attempt
  -> Registered Mapping Proof Qualification Competing Boundary Record
     (Temporal Record Type = REQUIRED_DIMENSION_MAPPING_PROOF_BOUNDARY)
  -> Registered Proof Boundary Registration Resolution
```

```text
Mapping Proof Boundary Registration Resolution Key =
  Mapping Proof Qualification Competing Boundary Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_MAPPING_PROOF_BOUNDARY Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

同键异成员集合、异空洞或异冲突子域必须 `CONFLICTED`。

### TM-R6-11 证明资格聚合必须拥有稳定键

```text
Mapping Proof Qualification Aggregate Resolution Key =
  Mapping Proof Qualification Semantic Conflict Set Key
+ Registered Proof Boundary Registration Resolution ID and Digest
+ Required Proof-boundary Completeness Resolution IDs and Digests
+ Registered Minimum Matrix Contract Registration Resolution ID and Digest
+ Registered Temporal Query Rule Contract Registration Resolution ID and Digest
+ Proof Qualification Aggregate Rule Version
```

键不得包含证据边界、候选资格结果、所偏好证明、执行者或登记时间。

### TM-R6-12 证明资格聚合必须形成登记解析

```text
Registered Complete Mapping Proof Qualification Boundary
  -> Candidate Mapping Proof Qualification Aggregate Resolution
  -> Proof Aggregate Registration Attempt
  -> Registered Mapping Proof Qualification Aggregate Record
     (Temporal Record Type = REQUIRED_DIMENSION_MAPPING_PROOF_AGGREGATE)
  -> Registered Proof Aggregate Registration Resolution
```

最终登记解析键固定聚合键、已登记映射账本边界、类型投影、必要完整性和登记规则版本。

```text
Mapping Proof Aggregate Registration Resolution Key =
  Mapping Proof Qualification Aggregate Resolution Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_MAPPING_PROOF_AGGREGATE Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

外层登记解析结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。只有外层 `REGISTERED` 且内层证明语义结果 `QUALIFIED` 可以支持确定映射成员。

### TM-R6-13 证明资格结果必须封闭

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
CONFLICTED
```

- 唯一合格证明或多个内容同一合格证明、完整边界和无冲突支持 `QUALIFIED`；
- 完整证据边界和完整候选集合证明语义不等价、作用域不覆盖或边界形态不兼容支持 `NOT_QUALIFIED`；
- 证据、读取、证明、合同、边界或完整性未知支持 `INDETERMINATE`；
- 相反资格、不兼容证明、异作用域或同键异载荷支持 `CONFLICTED`。

证明置信度、登记位置、规则较新或使用次数不能选择赢家。

### TM-R6-14 映射竞争成员必须固定合格证明解析

R5 的合格映射成员由本规则收紧为：

```text
Registered Mapping Candidate Registration Resolution ID and Digest
+ Registered Proof Aggregate Registration Resolution ID and Digest
+ Proof Semantic Result = QUALIFIED
+ Governed Mapping Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
```

映射竞争边界和映射聚合必须固定以上完整元组。`NOT_QUALIFIED | INDETERMINATE | CONFLICTED` 不能产生确定映射成员。

## 五、时间治理边界消费身份

### TM-R6-15 映射消费必须固定精确时间治理边界向量

```text
Mapping Consumption Temporal Context Key =
  Registered Temporal Governance Boundary Vector T ID and Digest
+ T.Registered Temporal Mapping Ledger Boundary ID and Digest
+ T.Required Mapping-ledger Completeness Resolution IDs and Digests
+ Temporal View Mode
+ Temporal Context Rule Version
```

`Temporal View Mode` 只允许：

```text
HISTORICAL_AS_OF_T
CURRENT_RESTATEMENT_AT_T
```

裸“当前”、系统时钟或“最新账本位置”不能替代已登记 `T`。

### TM-R6-16 映射聚合时间资格必须拥有稳定键

```text
Mapping Aggregate Temporal Eligibility Key =
  Mapping Consumption Temporal Context Key
+ Required Dimension Source-domain Mapping Aggregate Registration Resolution ID and Digest
+ Mapping Aggregate Payload Digest
+ Required Dimension ID and Version
+ Registered Requirement Set Qualification Resolution ID and Digest
+ Temporal Eligibility Rule Version
```

该键固定评价所消费的映射聚合与时间边界，不能只引用聚合结果字面值。

### TM-R6-17 时间资格载荷必须证明账本包含关系

```text
Mapping Aggregate Temporal Eligibility Payload =
  Mapping Aggregate Temporal Eligibility Key
+ Mapping Aggregate Record ID, Position and Payload Digest
+ Proof Aggregate Record IDs, Positions and Payload Digests
+ Mapping Competing Boundary Record ID, Position and Payload Digest
+ T.Mapping Ledger Boundary Membership Proof Digest
+ T.Mapping Ledger Boundary Completeness Resolution IDs and Digests
+ Temporal Eligibility Result
+ Eligibility Payload Rule Version
```

所有映射候选、证明资格、竞争边界和聚合记录必须处于 `T` 的映射账本边界内。任何输入位于边界外、边界成员未知或必要完整性非 `COMPLETE` 时，不能 `ELIGIBLE`。

### TM-R6-18 时间资格结果必须封闭

```text
ELIGIBLE
NOT_ELIGIBLE
INDETERMINATE
CONFLICTED
```

- 内容同一聚合及全部输入均被完整 `T` 覆盖，并与评价上下文一致时支持 `ELIGIBLE`；
- 完整 `T` 明确证明聚合或必要输入不在边界内支持 `NOT_ELIGIBLE`；
- `T`、成员、读取、完整性或上下文未知支持 `INDETERMINATE`；
- 同键异成员证明、异聚合载荷、异边界归属或异结果支持 `CONFLICTED`。

### TM-R6-19 时间资格作为评价登记的内容同一子对象

时间资格不是新的时间账本记录，不进入其所引用的 `T`。它作为 `Candidate Completeness Requirement Evaluation` 的不可变子对象，随时间评价候选、登记尝试和最终登记解析内容同一登记。

```text
Candidate Temporal Eligibility Payload Digest
= Registered Completeness Evaluation.Temporal Eligibility Payload Digest
```

这样保持：

```text
Temporal Mapping Ledger Boundary T
  -> Mapping Aggregate Temporal Eligibility
  -> Completeness Requirement Evaluation
  -> Knowledge Boundary K
```

不存在资格记录反向进入 `T` 的身份循环。

## 六、映射元组和时间评价收紧

### TM-R6-20 必要维度映射身份元组必须新增时间上下文

R5 中进入评价稳定键的映射元组由本规则覆盖为：

```text
Required Dimension Mapping Aggregate Identity Tuple =
  Required Dimension ID and Version
+ Registered Mapping Aggregate Registration Resolution ID and Digest
+ Mapping Aggregate Payload Digest
+ Mapping Semantic Result = MAPPED
+ Mapped Source Completeness Semantic Domain Key and Digest
+ Mapping Consumption Temporal Context Key
+ Mapping Aggregate Temporal Eligibility Key
```

不同 `T` 下的相同字面映射结果不是同一身份元组。时间资格载荷摘要和结果保存在评价候选载荷中，不进入身份元组；因此同一资格键的异载荷或异结果必须在同一评价键下冲突。

### TM-R6-21 完整性要求评价键必须固定 T 和时间资格集合

R5 的评价键以本规则收紧：

```text
Registered Temporal Governance Boundary Vector T ID and Digest
T.Registered Temporal Mapping Ledger Boundary ID and Digest
Exact Required Dimension Mapping Aggregate Identity Tuple Set Digest
Exact Mapping Aggregate Temporal Eligibility Key Set Digest
Temporal View Mode
```

R5 的 `Exact Required Dimension Mapping Aggregate Resolution Tuple Set Digest` 不再作为评价键字段。映射聚合、证明资格、`T`、视图模式或时间资格逻辑键变化必须形成新的评价身份；同一时间资格逻辑键的载荷或结果变化必须形成同键登记冲突。

### TM-R6-22 评价结果必须传播证明和时间资格失败

```text
all required proof qualifications QUALIFIED
+ all mapping aggregates MAPPED
+ all temporal eligibility results ELIGIBLE
+ all source completeness aggregates COMPLETE
  -> may support SATISFIED

any proof or temporal eligibility INDETERMINATE
  -> INDETERMINATE

any proof or temporal eligibility CONFLICTED
  -> CONFLICTED

any proof NOT_QUALIFIED or temporal result NOT_ELIGIBLE
  -> NOT_SATISFIED or INDETERMINATE according to registered requirement rule,
     never SATISFIED
```

失败结果的精确映射必须由已登记最低矩阵和查询规则合同固定，查询者不能选择较有利结果。同一评价键出现相反时间资格载荷或结果时，最终登记评价必须 `CONFLICTED`。

### TM-R6-23 历史和当前视图必须显式分离

历史评价固定 `HISTORICAL_AS_OF_T` 及其精确 `T`。当前重述固定新的 `CURRENT_RESTATEMENT_AT_T` 及适用的已登记 `T`；不得沿用旧 `T` 下的 `MAPPED` 或 `ELIGIBLE` 覆盖新边界中的冲突。

没有适用已登记 `T` 时，当前重述必须 `INDETERMINATE`。

### TM-R6-24 认识边界必须固定完整映射时间谱系

认识边界只可消费 `SATISFIED` 的已登记时间评价，并固定：

```text
Registered Temporal Governance Boundary Vector T ID and Digest
Exact Required Dimension Mapping Aggregate Identity Tuple Set Digest
Exact Mapping Proof Qualification Aggregate Resolution Set Digest
Exact Mapping Aggregate Temporal Eligibility Payload Set Digest
Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
```

任一谱系变化必须形成新的评价和认识边界身份。

## 七、阶段无环与权威

### TM-R6-25 映射账本内部阶段必须严格递增

```text
M0 Mapping Candidate Record
M1 Proof Qualification Candidate / Boundary / Aggregate Records
M2 Mapping Competing Boundary Record
M3 Mapping Aggregate Resolution Record
M4 Registered Complete Temporal Mapping Ledger Boundary
M5 Registered Temporal Governance Boundary Vector T
M6 Completeness Evaluation with Temporal Eligibility Subobject
M7 Knowledge Boundary K
```

每一阶段只能引用较早阶段的已登记对象或同阶段之前的固定边界。`M6`、`M7` 不得反向进入 `M4` 或 `M5` 身份。

### TM-R6-26 新增角色必须逐操作分权

证据边界构造、证据完整性、证明资格执行、证明登记、证明边界、证明聚合、时间治理向量、时间资格评价、完整性评价和认识边界构造权威不得互相传播。

时间侧不能登记、修正或重新聚合来源完整性结果。

## 八、非法状态与回归

### TM-R6-27 新增非法状态必须失败关闭

- 映射候选或聚合者自证映射证据完整；
- 只有证明摘要而没有受治理证据边界；
- 非 `QUALIFIED` 证明候选进入映射竞争；
- 映射评价只固定聚合结果而不固定 `T`；
- 聚合或其必要输入位于 `T` 的映射边界之外；
- 当前重述沿用旧 `T` 下的有利映射；
- 时间资格记录反向进入其引用的 `T`；
- `INDETERMINATE | CONFLICTED` 证明或时间资格支持 `SATISFIED`；
- 查询者选择失败结果映射；
- 候选、自检或文件存在替代已登记解析。

以上状态必须拒绝、`INDETERMINATE`、`NOT_SATISFIED` 或 `CONFLICTED`，不得静默升级。

### TM-R6-28 已通过主干不得回归

```text
Global Temporal Position Model: PRESERVED
Mapping Candidate / Boundary / Aggregate Identity: PRESERVED
Required Dimension / Source-domain Alignment: PRESERVED
Registered Source Completeness Aggregate Consumption: PRESERVED
Correction / Migration Aggregate Identity: PRESERVED
Temporal Governance Contract Roots: PRESERVED
Knowledge Boundary Type Closure: PRESERVED
Historical / Current Separation: STRENGTHENED
Cross-interface Acyclicity: PRESERVED
```

## 九、候选级闭合声明

### TM-R6-29 R6 只声明两个阻断候选闭合

```text
TM-R5-B1 Governed Mapping Proof Qualification: CLOSED_AS_DRAFT
TM-R5-B2 Temporal Governance Boundary Pinning for Mapping Consumption: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R6 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R5-B1 + TM-R5-B2 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0006` 复合模型，并在来源侧当前基线确定后执行交叉接口回归审查。R6 自检不能独立证明两个阻断关闭。
