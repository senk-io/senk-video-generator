# 时间映射治理有界修订 R7

## 修订信息

```text
Proposal ID: CR-0006-R7
Title: Mapping Claim-level Proof and T-scoped Aggregate Coverage Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R6 GOVERNED MAPPING PROOF AND TEMPORAL BOUNDARY CONSUMPTION CLOSURE
Repair Basis: CR-0006-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R6-B1 + TM-R6-B2 only
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
Compatibility Reference: CR-0005-R8
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R6-B1` 与 `TM-R6-B2`：把证明资格提升到映射声明层共同聚合，并证明所消费映射聚合覆盖 `T` 中全部同域合格成员。它不覆盖基础稿或 R1 至 R6 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订边界

### TM-R7-01 R7 只覆盖两个有界阻断

```text
TM-R6-B1 Mapping Claim-level Proof Qualification Aggregation
TM-R6-B2 T-scoped Mapping Aggregate Coverage
```

R6 已通过的受治理证据边界、独立完整性、`T` 身份固定、评价子对象和阶段无环方向继续有效。

### TM-R7-02 声明级证明与 T 范围覆盖不得自授权

```text
Mapping Claim
  -/-> qualify its own proof

Claim Proof Aggregate
  -/-> omit adverse proof candidates

T-scoped Coverage
  -/-> change T or its mapping-ledger boundary
  -/-> register new mapping candidates
  -/-> select a preferred historical aggregate
```

## 二、映射声明级语义域

### TM-R7-03 映射声明语义键必须排除证明载荷

```text
Required Dimension Source-domain Mapping Claim Semantic Conflict Set Key =
  Required Dimension / Source Completeness Domain Mapping Semantic Conflict Set Key
+ Target Source Completeness Semantic Domain Key and Digest
+ Mapping Applicability Interval
+ Mapping Claim Semantic Rule Version
```

该键禁止包含：

```text
Mapping Candidate ID or Key
Candidate Mapping Payload Digest
Any Proof ID or Digest
Evidence Boundary ID
Proof Qualification Result
Source Boundary and Scope Coverage Proof or Claim Digest
Boundary Shape Compatibility Proof or Claim
Registry Position
Registration Time
Writer or Authority Holder ID
```

相同维度、目标域、作用域、边界形态和适用区间的全部证明必须进入同一声明语义域。来源边界、查询作用域和边界形态已经由父级映射语义键固定，不能再用声明摘要分域。

### TM-R7-04 映射候选必须投影唯一声明键

每个 R5 映射候选必须内容同一投影一个声明键。候选载荷中的证明摘要不改变该声明键。

```text
Mapping Candidate.Mapping Semantic Conflict Set Key
= Claim.Mapping Semantic Conflict Set Key

Mapping Candidate.Target Domain
= Claim.Target Domain
```

同一候选投影多个声明键或同一声明键上下文字段不等必须 `CONFLICTED`。

## 三、声明级证明资格候选

### TM-R7-05 声明级证明资格候选载荷必须完整

```text
Mapping Claim Proof Qualification Candidate Payload =
  Mapping Claim Semantic Conflict Set Key
+ Registered Mapping Candidate Registration Resolution ID and Digest
+ Mapping Candidate Key and Payload Digest
+ Governed Mapping Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
+ Semantic Equivalence Proof ID and Digest
+ Scope Coverage Proof ID and Digest
+ Boundary Shape Proof ID and Digest
+ Candidate Claim Qualification Result
+ Proof Verification Rule Version
+ Candidate Canonicalization Rule Version
```

R6 的候选级证明资格可以保留为谱系，但不能直接支持确定映射成员。

### TM-R7-06 声明级证明资格候选必须拥有稳定键

```text
Mapping Claim Proof Qualification Candidate Key =
  Mapping Claim Semantic Conflict Set Key
+ Candidate Claim Qualification Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。证据或结果变化产生新候选，但仍进入同一声明语义冲突集合。

### TM-R7-07 声明级证明候选必须登记

```text
Candidate Mapping Claim Proof Qualification
  -> Claim Proof Registration Attempt
  -> Registered Mapping Claim Proof Qualification Record
     (Temporal Record Type = MAPPING_CLAIM_PROOF_QUALIFICATION)
  -> Registered Claim Proof Candidate Registration Resolution
```

记录进入现有 `Temporal Mapping Ledger` 全局位置域。候选登记解析键固定候选键、已登记映射账本边界、类型投影、必要完整性和规则版本。

```text
Mapping Claim Proof Candidate Registration Resolution Key =
  Mapping Claim Proof Qualification Candidate Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ MAPPING_CLAIM_PROOF_QUALIFICATION Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

## 四、声明级证明竞争与聚合

### TM-R7-08 声明级证明竞争边界必须覆盖全部候选

```text
Mapping Claim Proof Qualification Competing Boundary Key =
  Mapping Claim Semantic Conflict Set Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ Exact Claim Proof Candidate Registration Resolution Set Digest
+ Required Claim-proof Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖所有映射候选来源、证据边界、证明、资格候选、登记记录和冲突谱系。不得按映射候选 ID 或证明摘要过滤不利候选。

### TM-R7-09 声明级证明边界必须登记解析

```text
Candidate Mapping Claim Proof Competing Boundary
  -> Claim Proof Boundary Registration Attempt
  -> Registered Mapping Claim Proof Competing Boundary Record
     (Temporal Record Type = MAPPING_CLAIM_PROOF_BOUNDARY)
  -> Registered Claim Proof Boundary Registration Resolution
```

边界登记解析键固定边界键、映射账本边界、类型投影、必要完整性和规则版本。同键异成员、异空洞或异冲突子域必须 `CONFLICTED`。

```text
Mapping Claim Proof Boundary Registration Resolution Key =
  Mapping Claim Proof Qualification Competing Boundary Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ MAPPING_CLAIM_PROOF_BOUNDARY Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

### TM-R7-10 声明级证明聚合必须拥有稳定键

```text
Mapping Claim Proof Qualification Aggregate Resolution Key =
  Mapping Claim Semantic Conflict Set Key
+ Registered Claim Proof Boundary Registration Resolution ID and Digest
+ Required Claim-proof Boundary Completeness Resolution IDs and Digests
+ Registered Minimum Matrix Contract Registration Resolution ID and Digest
+ Registered Temporal Query Rule Contract Registration Resolution ID and Digest
+ Claim Proof Aggregate Rule Version
```

键不得包含候选结果、证据边界或所偏好的映射候选。

### TM-R7-11 声明级证明聚合必须形成外层登记解析

```text
Registered Complete Mapping Claim Proof Boundary
  -> Candidate Mapping Claim Proof Aggregate Resolution
  -> Claim Proof Aggregate Registration Attempt
  -> Registered Mapping Claim Proof Aggregate Record
     (Temporal Record Type = MAPPING_CLAIM_PROOF_AGGREGATE)
  -> Registered Claim Proof Aggregate Registration Resolution
```

外层登记解析键固定聚合键、映射账本边界、类型投影、必要完整性和规则版本，结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

```text
Mapping Claim Proof Aggregate Registration Resolution Key =
  Mapping Claim Proof Qualification Aggregate Resolution Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ MAPPING_CLAIM_PROOF_AGGREGATE Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

### TM-R7-12 声明级证明语义结果必须冲突优先

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
CONFLICTED
```

- 全部适用证明唯一支持合格或多个内容同一合格结论时可 `QUALIFIED`；
- 完整集合一致证明声明不合格且无相反结论时可 `NOT_QUALIFIED`；
- 证据、候选、读取、边界或完整性未知时必须 `INDETERMINATE`；
- `QUALIFIED` 与 `NOT_QUALIFIED` 并存、不兼容证明或同键异载荷时必须 `CONFLICTED`。

### TM-R7-13 映射竞争成员必须消费声明级聚合

R6 的合格证明成员由本规则覆盖为：

```text
Registered Mapping Candidate Registration Resolution ID and Digest
+ Registered Claim Proof Aggregate Registration Resolution ID and Digest
+ Claim Proof Semantic Result = QUALIFIED
+ Mapping Claim Semantic Conflict Set Key
+ Governed Evidence and Completeness Lineage Digest
```

候选级 `QUALIFIED` 不能替代声明级聚合。声明级 `NOT_QUALIFIED | INDETERMINATE | CONFLICTED` 时，该声明不能支持确定映射成员，且完整不利谱系必须进入后续 `T` 范围覆盖。

## 五、T 范围全域集合

### TM-R7-14 T 范围覆盖语义键必须稳定

```text
T-scoped Mapping Aggregate Coverage Semantic Key =
  Mapping Consumption Temporal Context Key
+ Required Dimension / Source Completeness Domain Mapping Semantic Conflict Set Key
+ Registered Mapping Aggregate Registration Resolution ID and Digest
+ Mapping Aggregate Payload Digest
+ T-scoped Coverage Semantic Rule Version
```

该键固定 `T`、映射语义域和被消费聚合，不包含覆盖结果或集合摘要。

### TM-R7-15 T 范围必须枚举全部映射候选

```text
Exact All Mapping Candidate Registration Resolution Set Digest within T =
  all records in T.Mapping Ledger Boundary
  matching Mapping Semantic Conflict Set Key
```

集合必须包含 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED` 候选解析及其谱系；只有满足登记与声明级证明资格的成员进入确定合格子集。

### TM-R7-16 T 范围必须枚举全部声明级证明

对每个映射声明键，必须固定：

```text
Exact Claim Proof Candidate Registration Resolution Set Digest within T
Registered Claim Proof Boundary Registration Resolution ID and Digest
Registered Claim Proof Aggregate Registration Resolution ID and Digest
Claim Proof Semantic Result
Claim Proof T-scoped Candidate-set Equality Proof Digest
```

旧声明级证明聚合若遗漏 `T` 中新增不利证明候选，不能作为该 `T` 下的确定资格。

### TM-R7-17 T 范围合格映射成员集合必须可重放

```text
Exact T-scoped Eligible Mapping Member Set Digest =
  all T-scoped mapping candidates
  whose registration result = REGISTERED
  and whose claim proof aggregate is T-scoped complete + QUALIFIED
  and whose contracts and applicability are valid under T
```

集合推导必须由已登记最低矩阵和查询规则合同固定，评价者不能排除目标域不利成员。

## 六、T 范围覆盖资格

### TM-R7-18 T 范围覆盖载荷必须比较完整集合

```text
T-scoped Mapping Aggregate Coverage Payload =
  T-scoped Mapping Aggregate Coverage Semantic Key
+ Exact All Mapping Candidate Resolution Set Digest within T
+ Exact All Claim Proof Qualification Set Digest within T
+ Exact T-scoped Eligible Mapping Member Set Digest
+ Selected Aggregate.Competing Boundary Eligible Member Set Digest
+ Eligible-member Set Equality Proof Digest
+ T.Mapping Ledger Boundary Membership and Completeness Proof Digests
+ T-scoped Coverage Result
+ Coverage Payload Rule Version
```

成员存在证明不能替代集合相等证明。

### TM-R7-19 T 范围覆盖结果必须封闭

```text
COVERAGE_MATCHED
COVERAGE_NOT_MATCHED
INDETERMINATE
CONFLICTED
```

- 被消费聚合成员集合与 `T` 范围合格集合内容同一，全部声明级证明也相对 `T` 完整时支持 `COVERAGE_MATCHED`；
- 完整 `T` 证明存在遗漏、额外或失效成员时支持 `COVERAGE_NOT_MATCHED`；
- `T`、成员、证明、读取或完整性未知支持 `INDETERMINATE`；
- 同键异集合、异证明、异覆盖结果或同域不兼容载荷支持 `CONFLICTED`。

### TM-R7-20 T 范围覆盖作为评价登记子对象

覆盖资格不写回 `Temporal Mapping Ledger`，而是作为 `Candidate Completeness Requirement Evaluation` 的不可变子对象内容同一登记。

```text
T Mapping Ledger Boundary
  -> T-scoped Coverage Subobject
  -> Completeness Requirement Evaluation
  -> Knowledge Boundary K
```

覆盖资格逻辑键进入评价稳定键；载荷摘要和结果保存在评价候选载荷。同逻辑键异载荷必须使评价登记 `CONFLICTED`。

## 七、时间资格与评价再次收紧

### TM-R7-21 时间资格必须同时满足成员和覆盖

R6 的 `Mapping Aggregate Temporal Eligibility` 新增：

```text
T-scoped Mapping Aggregate Coverage Semantic Key
T-scoped Coverage Payload Digest
T-scoped Coverage Result = COVERAGE_MATCHED
```

```text
membership proof satisfied
+ COVERAGE_MATCHED
  -> may support ELIGIBLE

COVERAGE_NOT_MATCHED
  -> NOT_ELIGIBLE

coverage INDETERMINATE
  -> INDETERMINATE

coverage CONFLICTED
  -> CONFLICTED
```

### TM-R7-22 映射身份元组必须固定覆盖逻辑键

R6 的映射身份元组新增：

```text
T-scoped Mapping Aggregate Coverage Semantic Key
Mapping Claim Proof Qualification Aggregate Resolution Set Digest
```

覆盖载荷和结果不进入身份元组，保存在评价候选载荷；同键异结果必须冲突。

### TM-R7-23 时间评价键必须固定覆盖键集合

```text
Exact T-scoped Mapping Aggregate Coverage Semantic Key Set Digest
Exact Mapping Claim Proof Aggregate Resolution Identity Set Digest
```

以上字段进入 `Completeness Requirement Evaluation Key`。覆盖载荷集合、声明级证明谱系和结果进入候选／登记载荷。

### TM-R7-24 时间评价结果必须传播声明证明和覆盖失败

```text
all claim proof aggregates QUALIFIED
+ all T-scoped coverage results COVERAGE_MATCHED
+ all temporal eligibility results ELIGIBLE
+ all source completeness aggregates COMPLETE
  -> may support SATISFIED

any claim proof or coverage INDETERMINATE
  -> INDETERMINATE

any claim proof or coverage CONFLICTED
  -> CONFLICTED

any claim proof NOT_QUALIFIED or coverage NOT_MATCHED
  -> never SATISFIED
```

精确失败结果由已登记最低矩阵和查询规则合同固定。

### TM-R7-25 历史与当前 T 必须保持全域覆盖

历史 `T1` 可以重放当时完整的旧聚合。当前 `T2` 必须重新计算声明级证明全域和合格映射成员全域；旧聚合只有在集合相等时才可继续 `COVERAGE_MATCHED`。

新增同域候选或不利证明必须形成新的覆盖资格、时间评价和认识边界身份。

## 八、阶段、权威和非法状态

### TM-R7-26 阶段必须保持无环

```text
M0 Mapping Candidate Records
M1 Claim-level Proof Candidate / Boundary / Aggregate Records
M2 Mapping Competing Boundary Record
M3 Mapping Aggregate Record
M4 Registered Complete Mapping Ledger Boundary
M5 Registered Temporal Governance Boundary Vector T
M6 T-scoped Coverage and Temporal Eligibility Subobjects
M7 Completeness Evaluation and Knowledge Boundary K
```

`M6`、`M7` 不得反向进入 `M4`、`M5`。

### TM-R7-27 新增权威必须逐操作分离

声明投影、证明资格、证明边界、证明聚合、T 范围集合构造、T 范围覆盖评价、时间资格、完整性评价和认识边界权威不得互相传播。

### TM-R7-28 非法状态必须失败关闭

- 映射候选键或证明摘要隔离同声明相反证明；
- `NOT_QUALIFIED` 不利证明从声明级竞争谱系删除；
- 声明级证明聚合遗漏 `T` 内新增证明候选；
- T 范围覆盖只证明旧成员位于边界内；
- 被消费聚合成员集合与 T 范围合格集合不等仍 `ELIGIBLE`；
- 当前 `T2` 沿用旧 `T1` 子集聚合；
- 覆盖资格反向写入被验证映射账本或 `T`；
- `INDETERMINATE | CONFLICTED` 声明证明或覆盖结果支持 `SATISFIED`；
- 候选、自检或文件存在替代已登记证明和覆盖。

以上状态必须拒绝、`NOT_ELIGIBLE`、`INDETERMINATE` 或 `CONFLICTED`。

## 九、回归与候选级闭合声明

### TM-R7-29 已通过主干不得回归

```text
Governed Mapping Evidence Boundary: PRESERVED
Global Temporal Position Model: PRESERVED
Mapping Candidate / Boundary / Aggregate Identity: PRESERVED
Temporal Governance Boundary Vector T Pinning: PRESERVED
Evaluation-subobject Acyclicity: PRESERVED
Registered Source Completeness Aggregate Consumption: PRESERVED
Historical / Current Separation: STRENGTHENED
```

### TM-R7-30 R7 只声明两个阻断候选闭合

```text
TM-R6-B1 Mapping Claim-level Proof Qualification Aggregation: CLOSED_AS_DRAFT
TM-R6-B2 T-scoped Mapping Aggregate Coverage: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R7 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R6-B1 + TM-R6-B2 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R8` 执行交叉接口回归审查。R7 自检不能独立证明两个阻断关闭。
