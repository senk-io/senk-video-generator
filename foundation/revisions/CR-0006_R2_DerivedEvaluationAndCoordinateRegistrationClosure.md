# 时间映射治理有界修订 R2

## 修订信息

```text
Proposal ID: CR-0006-R2
Title: Derived Evaluation and Coordinate Registration Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R1 KNOWLEDGE BOUNDARY AND TEMPORAL LEDGER CLOSURE
Repair Basis: CR-0005-R1-CR-0006-R1-CROSS-INTERFACE-REVIEW
Repair Scope: R1-B1 + R1-B2 + R1-B3 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Cross-interface Re-review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Coordinate Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0005-R1
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 R1 交叉接口复审的三个残余阻断。它不覆盖 `CR-0006`、`CR-0006-R1` 或复审记录的历史文本，不创建实际评价、时间账本、查询坐标、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R2-01 R2 只覆盖三个残余阻断

本修订只覆盖 `CR-0006-R1` 的 `TM-R1-05` 至 `TM-R1-09`、`TM-R1-14` 至 `TM-R1-15`、`TM-R1-18` 至 `TM-R1-22`、`TM-R1-23` 至 `TM-R1-24` 及相应当前状态中与下列事项冲突的部分：

```text
R1-B1 Requirement Lower Bound and Evaluation Identity
R1-B2 Temporal-ledger Completeness Identity
R1-B3 Coordinate Registration Conflict Closure
```

未被本修订显式覆盖的 `CR-0006` 与 `CR-0006-R1` 规则继续作为合并候选语义。`CR-0005-R1` 不需要修订。

### TM-R2-02 R2 不改变已通过的接口主干

本修订不得改变：

```text
Registered Raw Temporal Assertion handoff
Known At := Registered Knowledge Boundary Vector ID and Digest
OPEN_WORLD absence prohibition
B -> temporal records -> T -> K four-stage causality
Temporal Query Coordinate -> Source Applicability whole-coordinate consumption
```

新增的评价和登记解析只证明派生对象是否可消费，不创建来源事实、规范时间值、适用性结论或行动权威。

## 二、R1-B1：不可削减的最低完整性矩阵

### TM-R2-03 来源边界形态必须封闭

完整性要求必须绑定一种精确边界形态：

```text
POSITION_RANGE
EXACT_RECORD_SET
CLOSED_PARTITION_SET
```

- `POSITION_RANGE` 以首末追加位置固定成员；
- `EXACT_RECORD_SET` 以规范有序记录集合摘要固定成员，不声明集合外不存在其他成员；
- `CLOSED_PARTITION_SET` 以精确关闭分区集合固定穷尽作用域。

边界形态只能来自 `CR-0005` 已登记边界契约，查询者不得按结果选择更宽松的形态。

### TM-R2-04 所有确定查询必须满足共同最低维度

任何可产生确定认识边界的查询都不得删除：

```text
CARRIER_INTEGRITY
READ_COMPLETENESS
CONFLICT_SUBDOMAIN_COMPLETENESS
```

这些共同下限分别证明载体没有已知破坏、精确边界读取完成、相关冲突子域被完整读取。任一维度缺失、未登记或非 `COMPLETE` 时，要求评价不能为 `SATISFIED`。

### TM-R2-05 边界形态必须增加相应最低维度

```text
POSITION_RANGE
  -> + POSITION_CONTINUITY

EXACT_RECORD_SET
  -> no implicit POSITION_CONTINUITY requirement
  -> exact ordered record-set digest required

CLOSED_PARTITION_SET
  -> + POSITION_CONTINUITY per partition when position-ranged
  -> + SCOPE_COVERAGE
```

精确记录集合无需证明集合外位置连续，但仍必须满足共同最低维度。关闭分区集合的每个分区都必须绑定独立关闭契约、分区边界和完整性记录。

### TM-R2-06 缺失和穷尽查询必须增加成员与作用域下限

```text
QUALIFIED_ABSENCE_CHECK
  -> + MEMBERSHIP_COMPLETENESS
   + SCOPE_COVERAGE
   + applicable closure or qualified-negative evidence

EXHAUSTIVE_SCOPE_RESOLUTION
  -> + MEMBERSHIP_COMPLETENESS
   + SCOPE_COVERAGE
   + complete closed-world or closed-partition composition evidence
```

`OPEN_WORLD` 不能满足上述两个查询目的的关闭证据要求。`EXACT_KNOWN_SET_REPLAY + NO_ABSENCE_CLAIM` 不要求成员穷尽，但不得把未读取成员解释为不存在。

### TM-R2-07 已登记要求集合只能增加最低维度

```text
Effective Required Dimension Set =
  Common Minimum Dimension Set
+ Boundary-shape Minimum Dimension Set
+ Query-purpose Minimum Dimension Set
+ Frozen Additional Dimension Set
```

候选 `Required Completeness Dimension Set` 必须是上述有效集合的超集。任何删除、条件绕过、空集合、调用方覆盖或运行时降级必须使要求集合资格为 `NOT_QUALIFIED`、`INDETERMINATE` 或 `CONFLICTED`，不能登记为可消费要求。

以本规则收紧 R1 的要求集合键：

```text
Requirement Set Key =
  Query Purpose
+ Source Registry ID and Version
+ Registry Scope Digest
+ World Boundary Mode
+ Exact Query Scope Digest
+ Boundary Shape
+ Absence Claim Mode
+ Required Completeness Dimension Set
+ Completeness Minimum Matrix Version
+ Requirement Rule Version
```

要求集合资格值域：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
CONFLICTED
```

```text
Requirement Set Qualification Key =
  Requirement Set Key
+ Registered Minimum Matrix Contract ID and Digest
+ Requirement Qualification Rule Version
```

```text
Candidate Requirement Set
+ Registered Minimum Matrix Contract
  -> Candidate Requirement Set Qualification
  -> Requirement Qualification Registration Attempt
  -> Registered Requirement Set Qualification Resolution
```

候选与登记资格解析必须内容同一；同键不兼容最低集合、候选、资格值或登记载荷必须 `CONFLICTED`。只有已登记 `QUALIFIED` 解析及内容同一要求集合可以进入完整性评价。

## 三、R1-B1：完整性要求评价稳定身份

### TM-R2-08 完整性要求评价必须拥有稳定键

```text
Completeness Requirement Evaluation Key =
  Registered Requirement Set ID and Digest
+ Registered Source Boundary ID and Digest
+ Registered Source Snapshot ID and Digest
+ Exact Query Scope Digest
+ Boundary Shape
+ Exact Registered Source Completeness Record Set Digest
+ Completeness Evaluation Rule Version
```

评价证据只能来自键中精确记录集合。要求集合、边界、快照、作用域、形态、完整性记录集合或规则变化必须形成新评价身份。

### TM-R2-09 评价必须形成候选—登记—四值解析

```text
Registered QUALIFIED Requirement Set
+ Registered Source Boundary and Snapshot
+ Exact Registered Source Completeness Record Set
  -> Candidate Completeness Requirement Evaluation
  -> Completeness Evaluation Registration Attempt
  -> Registered Completeness Requirement Evaluation Resolution
```

候选与登记解析至少共同绑定完整键、有效最低维度集合、逐维度输入和结果、非必要不完整引用、候选与登记载荷摘要、执行和登记权威、登记时间及证据。

```text
Candidate Evaluation Payload Digest
= Registered Evaluation Payload Digest
```

### TM-R2-10 评价解析必须使用封闭四值

```text
SATISFIED
NOT_SATISFIED
INDETERMINATE
CONFLICTED
```

- 每个有效必要维度均有唯一、适用、已登记且无冲突的 `COMPLETE` 支持 `SATISFIED`；
- 至少一个必要维度有合格、适用、完整的 `INCOMPLETE` 证明支持 `NOT_SATISFIED`；
- 要求资格、边界、快照、必要记录、证据、读取或登记未知支持 `INDETERMINATE`；
- 同键不兼容候选、维度输入、最低集合、结果或登记载荷支持 `CONFLICTED`。

空集合、缺失记录或读取失败不能产生 `SATISFIED` 或 `NOT_SATISFIED`。同键内容相同可以幂等重申；同键异载荷必须进入同一冲突解析。

### TM-R2-11 认识边界只能消费已登记评价解析

认识边界条目必须引用：

```text
Registered Completeness Requirement Evaluation Resolution ID and Digest
Resolution Result = SATISFIED
Registered QUALIFIED Requirement Set ID and Digest
Effective Required Dimension Set Digest
```

`NOT_SATISFIED`、`INDETERMINATE` 或 `CONFLICTED` 均不能支持 `AVAILABLE` 认识边界。评价执行者、评价登记者、要求制定者和认识边界构造者不得互相继承权威。

## 四、R1-B2：时间派生账本完整性稳定身份

### TM-R2-12 时间账本完整性必须绑定治理证据边界

每次时间账本完整性评价必须引用一个由 `IF-0006` 兼容证据模型提供的：

```text
Governed Completeness Evidence Boundary ID and Digest
Evidence Boundary Scope
Evidence Boundary Completeness Resolution ID and Digest
```

只有适用、完整、无冲突且覆盖精确账本边界与完整性维度的证据边界可以支持确定结论。时间账本、边界构造者、完整性执行者或查询者不能自行宣布证据边界完整。

### TM-R2-13 时间账本完整性记录必须拥有稳定键

```text
Temporal Derived Ledger Completeness Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Temporal Derived Ledger Boundary ID and Digest
+ Completeness Dimension
+ Governed Completeness Evidence Boundary ID and Digest
+ Completeness Rule Version
```

证据边界固定同一评价所允许的全部证据。若补充证据需要扩大边界，必须形成新的证据边界和完整性评价身份，不能改写旧结论。

### TM-R2-14 时间账本完整性必须形成候选—登记—四值解析

```text
Registered Temporal Derived Ledger Boundary
+ Registered Governed Completeness Evidence Boundary
  -> Candidate Temporal Derived Ledger Completeness Record
  -> Temporal Completeness Registration Attempt
  -> Registered Temporal Derived Ledger Completeness Resolution
```

解析值域：

```text
COMPLETE
INCOMPLETE
INDETERMINATE
CONFLICTED
```

候选和登记解析必须内容同一。同键同载荷可以幂等重申；同键不同维度输入、证据摘要、结论或载荷必须 `CONFLICTED`。证据或读取缺失必须 `INDETERMINATE`；已证明存在缺口才支持 `INCOMPLETE`。

### TM-R2-15 时间治理向量只能消费合格完整性解析

`Temporal Governance Boundary Vector` 每个必要账本维度必须绑定：

```text
Registered Temporal Derived Ledger Completeness Resolution ID and Digest
Resolution Result = COMPLETE
Governed Completeness Evidence Boundary ID and Digest
```

任何必要维度非 `COMPLETE` 时，该向量不能支持确定认识边界。同键冲突记录不得由向量构造者选择一个 `COMPLETE` 消除。

时间完整性执行、登记、向量构造和向量登记权威继续分离，且都不能登记被评价的映射、更正或迁移记录。

## 五、R1-B3：查询坐标登记边界与解析

### TM-R2-16 查询坐标规范载荷与登记包必须分离

```text
Normative Temporal Query Coordinate Payload =
  Temporal Query Coordinate Key
+ Canonical Valid At Value ID and Digest
+ Registered Knowledge Boundary Vector ID and Digest
+ Inherited Temporal View Mode
+ Temporal Query Rule Version
```

```text
Normative Coordinate Payload Digest
= canonical digest of Normative Temporal Query Coordinate Payload
```

构造、登记权威、登记时间和证据属于追加登记包，不改变规范坐标身份。相同键和规范摘要可以幂等重申；相同键不同规范摘要必须竞争，不能因登记包不同而分裂语义键。

### TM-R2-17 查询坐标登记边界必须可重放且非自证

新增逻辑对象：

```text
Temporal Query Coordinate Registry Boundary
Temporal Query Coordinate Registry Completeness Resolution
```

边界必须固定精确坐标候选、登记尝试、已登记坐标、规范摘要、空洞和冲突子域，并形成候选—登记链。边界完整性至少分别评价载体、读取和冲突子域；位置范围边界还必须评价位置连续性。

坐标注册表被视为受治理的 `TEMPORAL_QUERY_COORDINATE_REGISTRY` 账本类型；其边界完整性必须复用本修订前述时间账本完整性契约中的 `Temporal Derived Ledger Completeness Key`、治理证据边界、候选—登记—四值解析和非自证要求，不得创建无稳定键的第二套完整性对象。

新增逐操作权威：

```text
Temporal Query Coordinate Boundary Construction Authority Type
Temporal Query Coordinate Boundary Registration Authority Type
Temporal Query Coordinate Boundary Completeness Qualification Authority Type
Temporal Query Coordinate Boundary Completeness Registration Authority Type
```

坐标构造、坐标登记、边界构造、边界登记、完整性资格和完整性登记权威不得互相传播。边界摘要、零记录或查询成功不能自证完整。

### TM-R2-18 查询坐标登记解析必须拥有稳定键

```text
Temporal Query Coordinate Registration Resolution Key =
  Temporal Query Coordinate Key
+ Temporal Query Coordinate Registry Boundary ID and Digest
+ Required Registry Completeness Resolution IDs and Digests
+ Coordinate Registration Resolution Rule Version
```

```text
Candidate Temporal Query Coordinate
+ Coordinate Registration Attempt
+ Registered Coordinate Registry Boundary
+ Registered Registry Completeness Resolutions
  -> Candidate Coordinate Registration Resolution
  -> Coordinate Resolution Registration Attempt
  -> Registered Temporal Query Coordinate Registration Resolution
```

候选与登记解析必须绑定规范坐标摘要集合、登记尝试集合、边界、必要完整性、解析值、候选与登记摘要、解析和登记权威、登记时间及证据，并保持内容同一。

### TM-R2-19 查询坐标登记解析必须使用四值

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

- 唯一规范载荷、内容同一登记、必要边界完整且无冲突支持 `REGISTERED`；
- 合格、适用、完整的未登记证明支持 `NOT_REGISTERED`；
- 候选、登记、边界、必要完整性、资格、证据或读取未知支持 `INDETERMINATE`；
- 同键多个不兼容规范载荷、登记记录、边界或解析载荷支持 `CONFLICTED`。

空查询、缺失坐标、超时、缓存未命中或不完整边界不能产生 `NOT_REGISTERED`。冲突优先于确定结果，不能选择最早、最新或证据最多的坐标。

### TM-R2-20 来源适用性只能消费 REGISTERED 坐标解析

`CR-0005-R1` 继续消费既有接口字段：

```text
Registered Temporal Query Coordinate ID and Digest
```

但 `WS-03` 只有在精确 `Registered Temporal Query Coordinate Registration Resolution ID and Digest` 的结果为 `REGISTERED` 时，才能把该坐标标记并输出为 `Registered Temporal Query Coordinate`。该解析引用必须进入坐标的验证包和来源适用性证据引用，不改变 `CR-0005-R1` 的规范消费字段。

坐标解析为 `NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED` 时，来源适用性不能产生确定 `APPLICABLE` 或 `INAPPLICABLE`。展开的有效时间、认识边界和视图仍必须与该 `REGISTERED` 坐标规范载荷内容同一。

## 六、非法状态与闭合声明

### TM-R2-21 新增非法状态必须失败关闭

- 以空要求集合或运行时覆盖删除共同最低完整性维度；
- 位置范围查询省略位置连续性；
- 缺失或穷尽查询省略成员完整性、作用域覆盖或关闭证据；
- 未登记或同键异载荷完整性要求评价被认识边界消费；
- 时间账本完整性记录用不同标识绕开同键冲突；
- 时间治理向量选择冲突记录中的 `COMPLETE`；
- 查询坐标登记包字段改变规范坐标身份；
- 查询坐标边界、完整性或解析自证；
- `NOT_REGISTERED` 来自空查询、缺失、超时或不完整边界；
- 未取得 `REGISTERED` 解析的坐标被来源适用性消费。

### TM-R2-22 本修订只声明候选级残余阻断关闭

```text
R1-B1 Requirement Lower Bound: CLOSED_AS_DRAFT
R1-B1 Evaluation Identity: CLOSED_AS_DRAFT
R1-B2 Temporal-ledger Completeness Identity: CLOSED_AS_DRAFT
R1-B3 Coordinate Registration Conflict Closure: CLOSED_AS_DRAFT
Raw Assertion Interface Regression: NONE_FOUND
Knowledge-time Type Regression: NONE_FOUND
Open-world Absence Safety Regression: NONE_FOUND
Four-stage Acyclicity Regression: NONE_FOUND
Cross-interface Re-review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R2 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R1-B1 + R1-B2 + R1-B3 only
Cross-interface Re-review with CR-0005-R1: REQUIRED
Independent Model Review: BLOCKED_PENDING_CROSS_REVIEW
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须使用 `CR-0005-R1 + CR-0006-R2` 执行独立交叉接口复审。自检、规则编号完整或文件存在不能独立证明残余阻断已经关闭。
