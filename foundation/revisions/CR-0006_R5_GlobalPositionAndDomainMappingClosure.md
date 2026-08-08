# 时间映射治理有界修订 R5

## 修订信息

```text
Proposal ID: CR-0006-R5
Title: Global Temporal Position and Required-dimension Source-domain Mapping Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R4 CORRECTION MIGRATION BOUNDARY AGGREGATE AND SOURCE COMPLETENESS CONSUMPTION CLOSURE
Repair Basis: CR-0006-R4-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R4-B1 + TM-R4-B2 only
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

> 本文件只修复 `TM-R4-B1` 与 `TM-R4-B2`：统一时间派生账本的全局位置模型，并为必要维度到来源完整性语义域建立稳定、完整且冲突优先的登记映射。它不覆盖基础稿或 R1 至 R4 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R5-01 R5 只覆盖两个有界阻断

```text
TM-R4-B1 Temporal Record Partition and Position Identity
TM-R4-B2 Required Dimension / Source Completeness Domain Mapping Identity
```

R4 已通过的更正、迁移边界和聚合稳定键，以及来源完整性聚合直接消费方向继续有效。

### TM-R5-02 R5 选择账本全局位置模型

本修订采用：

```text
ONE Temporal Ledger ID and Version + Temporal Ledger Type
  -> ONE global append-position namespace
  -> multiple Temporal Record Type payload discriminators
```

`Temporal Record Type` 不创建独立位置域、分区 ID、注册表或权威对象。

## 二、撤销独立分区对象

### TM-R5-03 R4 的已登记分区对象不再具有候选资格

以下 R4 输出不再是可登记或可消费对象：

```text
Registered Append-only Temporal Record Partition
```

R4 中“每种记录类型拥有独立位置子域”由本修订覆盖为“同一账本类型内全部记录类型共享全局位置域”。历史 R4 文本保留，但不能作为 R5 复合模型的有效消费契约。

### TM-R5-04 记录类型只允许作为规范载荷判别字段

记录类型映射封闭为：

```text
TEMPORAL_CORRECTION_COMPETING_BOUNDARY
  -> Temporal Ledger Type = CORRECTION

TEMPORAL_CORRECTION_AGGREGATE_RESOLUTION
  -> Temporal Ledger Type = CORRECTION

TEMPORAL_MIGRATION_COMPETING_BOUNDARY
  -> Temporal Ledger Type = MIGRATION

TEMPORAL_MIGRATION_AGGREGATE_RESOLUTION
  -> Temporal Ledger Type = MIGRATION

REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_CANDIDATE
  -> Temporal Ledger Type = MAPPING

REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_COMPETING_BOUNDARY
  -> Temporal Ledger Type = MAPPING

REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_AGGREGATE_RESOLUTION
  -> Temporal Ledger Type = MAPPING
```

换记录类型不能改变账本 ID、账本类型、追加纪元或位置身份。

## 三、全局位置与边界

### TM-R5-05 既有位置键继续作为唯一规范键

```text
Temporal Derived Record Position Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

同一账本 ID、类型和纪元中的位置值跨全部记录类型全局不可复用。记录类型必须保存在位置分配载荷中，但不得改变位置键。

```text
same ledger + same epoch + same position + different record type
  -> POSITION_REUSE_CONFLICT
```

### TM-R5-06 位置分配必须与记录登记原子内容同一

每个更正边界、迁移边界、聚合或维度映射聚合记录登记时，必须在对应全局账本原子取得唯一位置。位置分配记录固定记录 ID、载荷摘要、记录类型和登记尝试 ID。

失败登记留下永久空洞；记录类型变更不能回收或重用位置。

### TM-R5-07 既有账本边界必须覆盖全局位置域

```text
Temporal Derived Ledger Boundary Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ First and Last Position or Exact Record Set Digest
+ Boundary Rule Version
```

范围边界覆盖范围内全部记录类型及空洞，不能按记录类型过滤不利位置。精确记录集合边界必须保存其全局位置引用，并由独立完整性证明全部适用记录已覆盖。

### TM-R5-08 类型化读取只形成边界投影而非新边界真值

```text
Typed Temporal Record Boundary Projection =
  Registered Temporal Derived Ledger Boundary ID and Digest
+ Temporal Record Type
+ Exact Matching Record ID / Position / Payload Digest Set Digest
+ Projection Rule Version
```

该投影只用于定位边界记录或聚合记录，不能取得独立位置、边界登记或完整性权威。投影必须保留被排除的其他记录类型位置和冲突引用，不能伪装为新的完整账本边界。

### TM-R5-09 R4 边界和聚合登记键必须固定全局边界

R4 的下列引用：

```text
Registered Correction-boundary Record Ledger Boundary ID and Digest
Registered Correction-aggregate Record Ledger Boundary ID and Digest
Registered Migration-boundary Record Ledger Boundary ID and Digest
Registered Migration-aggregate Record Ledger Boundary ID and Digest
```

必须解释为 R5-07 的已登记全局时间派生账本边界；类型化集合只可通过 R5-08 投影固定。任何独立分区引用均不合格。

## 四、必要维度映射候选

### TM-R5-10 映射候选必须由既有登记合同治理

必要维度映射不创建新的制度合同类型。其资格和语义必须共同固定：

```text
Registered Minimum Matrix Contract Registration Resolution ID and Digest
Registered Temporal Query Rule Contract Registration Resolution ID and Digest
Registered Requirement Set Qualification Resolution ID and Digest
```

三者必须内容同一、适用且无冲突。映射候选是时间派生记录，不是制度合同，不能修改最低矩阵、查询规则或来源完整性语义域。

### TM-R5-11 映射语义冲突键必须排除目标来源域

```text
Required Dimension / Source Completeness Domain Mapping Semantic Conflict Set Key =
  Registered Requirement Set Qualification Resolution ID and Digest
+ Registered Requirement Set ID and Digest
+ Required Dimension ID and Version
+ Registered Source Boundary ID and Digest
+ Registered Source Snapshot ID and Digest
+ Exact Query Scope Digest
+ Boundary Shape
+ Registered Minimum Matrix Contract Registration Resolution ID and Digest
+ Registered Temporal Query Rule Contract Registration Resolution ID and Digest
+ Mapping Semantic Rule Version
```

下列字段不得进入语义冲突键：

```text
Target Source Completeness Semantic Domain Key
Mapping Candidate ID
Source Aggregate Resolution ID
Evidence Set ID
Registration Time
Writer or Authority Holder ID
```

同一必要维度和评价上下文的不同目标域必须竞争，不能通过目标域或合同 ID 换键。

### TM-R5-12 映射候选载荷必须完整

```text
Required Dimension Source-domain Mapping Candidate Payload =
  Mapping Semantic Conflict Set Key
+ Target Source Completeness Semantic Domain Key and Digest
+ Dimension-to-domain Semantic Equivalence Proof Digest
+ Source Boundary and Scope Coverage Proof Digest
+ Boundary Shape Compatibility Proof Digest
+ Mapping Applicability Interval
+ Mapping Result Claim
+ Candidate Canonicalization Rule Version
```

目标来源语义域必须固定 R4 来源侧定义的边界、维度、精确作用域和语义规则。时间侧不能创造、扩大或改写来源语义域。

### TM-R5-13 候选映射必须形成时间账本登记链

```text
Required Dimension Source-domain Mapping Candidate Key =
  Mapping Semantic Conflict Set Key
+ Candidate Mapping Payload Digest
+ Candidate Identity Rule Version
```

```text
Candidate Required Dimension Source-domain Mapping
  -> Mapping Candidate Registration Attempt
  -> Registered Mapping Candidate Record
     (Temporal Record Type = REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_CANDIDATE)
  -> Registered Mapping Candidate Registration Resolution
```

候选记录进入现有 `Temporal Mapping Ledger` 全局位置域。候选登记解析键固定候选键、已登记映射账本边界、候选类型投影、必要完整性和规则版本，结果为：

```text
Required Dimension Source-domain Mapping Candidate Registration Resolution Key =
  Required Dimension Source-domain Mapping Candidate Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_CANDIDATE Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

结果为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

候选与登记载荷必须内容同一。只有 `REGISTERED` 候选解析可以成为映射竞争成员；其他结果保留在冲突谱系中并失败关闭。

## 五、映射竞争边界与聚合解析

### TM-R5-14 映射竞争边界必须覆盖全部同域合同

```text
Required Dimension Source-domain Mapping Competing Boundary Key =
  Mapping Semantic Conflict Set Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ Exact Eligible Mapping Candidate Registration Resolution Set Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Mapping Boundary Rule Version
```

边界覆盖全部同语义域候选、登记尝试、登记记录、候选解析和冲突谱系。选择精确集合不能排除目标域不利的已登记候选。

### TM-R5-15 映射边界必须形成内容同一登记解析

```text
Candidate Required Dimension Mapping Competing Boundary
  -> Mapping Boundary Registration Attempt
  -> Registered Required Dimension Mapping Competing Boundary
  -> Registered Mapping Boundary Registration Resolution
```

边界记录以 `REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_COMPETING_BOUNDARY` 类型进入现有 `Temporal Mapping Ledger` 全局位置域。边界登记解析键为：

```text
Required Dimension Mapping Boundary Registration Resolution Key =
  Required Dimension Source-domain Mapping Competing Boundary Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_COMPETING_BOUNDARY Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

结果为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同键异成员集合、异空洞或异冲突子域必须 `CONFLICTED`。

### TM-R5-16 映射边界完整性必须独立

映射候选构造者、登记者、边界构造者、时间评价者和映射聚合者均不得评价映射边界完整性。必要维度至少覆盖：

```text
CARRIER
POSITION_OR_EXACT_SET
READABILITY
CONFLICT_SUBDOMAIN
SEMANTIC_DOMAIN_COVERAGE
```

任何必要维度未知或不完整时，映射聚合不能产生确定目标域。

### TM-R5-17 映射聚合解析必须拥有稳定键

```text
Required Dimension Source-domain Mapping Aggregate Resolution Key =
  Mapping Semantic Conflict Set Key
+ Registered Mapping Boundary Registration Resolution ID and Digest
+ Required Mapping-boundary Completeness Resolution IDs and Digests
+ Registered Minimum Matrix Contract Registration Resolution ID and Digest
+ Registered Temporal Query Rule Contract Registration Resolution ID and Digest
+ Mapping Aggregate Rule Version
```

键不得包含目标来源域、候选结果、所偏好的合同、执行者或登记时间。

### TM-R5-18 映射聚合必须形成时间账本登记链

```text
Registered Complete Required Dimension Mapping Competing Boundary
  -> Candidate Required Dimension Source-domain Mapping Aggregate Resolution
  -> Mapping Aggregate Registration Attempt
  -> Registered Mapping Aggregate Resolution Record
     (Temporal Record Type = REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_AGGREGATE_RESOLUTION)
  -> Registered Mapping Aggregate Registration Resolution
```

记录进入现有 `Temporal Mapping Ledger` 全局位置域。最终登记解析键固定映射聚合键、已登记映射账本边界、R5-08 类型投影、必要完整性和登记规则版本。

```text
Required Dimension Source-domain Mapping Aggregate Registration Resolution Key =
  Required Dimension Source-domain Mapping Aggregate Resolution Key
+ Registered Temporal Mapping Ledger Boundary ID and Digest
+ REQUIRED_DIMENSION_SOURCE_DOMAIN_MAPPING_AGGREGATE_RESOLUTION Projection Digest
+ Required Mapping-ledger Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

最终登记解析结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`；同聚合键异目标域、异成员或异载荷必须 `CONFLICTED`。

### TM-R5-19 映射聚合结果必须封闭

```text
MAPPED(Source Completeness Semantic Domain Key and Digest)
NOT_MAPPED
INDETERMINATE
CONFLICTED
```

- 唯一目标域或多个内容同一目标域、完整边界和无冲突支持 `MAPPED`；
- 完整边界证明不存在合格映射支持 `NOT_MAPPED`；
- 治理合同、候选、边界、作用域、读取或完整性未知支持 `INDETERMINATE`；
- 不同目标域、不兼容作用域、边界形态、证明或同键异载荷支持 `CONFLICTED`。

置信度、候选规则版本较新、登记位置或使用次数不能选择赢家。

## 六、完整必要维度映射集合

### TM-R5-20 每个必要维度必须固定已登记映射聚合

```text
Required Dimension Mapping Aggregate Resolution Tuple =
  Required Dimension ID and Version
+ Registered Mapping Aggregate Registration Resolution ID and Digest
+ Mapping Aggregate Payload Digest
+ Mapping Semantic Result
+ Mapped Source Completeness Semantic Domain Key and Digest or NOT_ESTABLISHED
```

有效要求集合中的每个必要维度必须恰好对应一个元组，不得重复、遗漏或添加替代元组。

### TM-R5-21 映射元组集合必须证明资格集合全覆盖

```text
Exact Required Dimension Mapping Aggregate Resolution Tuple Set Digest
```

该集合必须与 `Registered QUALIFIED Requirement Set` 的有效必要维度集合一一对应。覆盖证明固定要求集合资格解析、最低矩阵合同解析、查询规则合同解析和规范排序规则。

任一映射结果为 `NOT_MAPPED | INDETERMINATE | CONFLICTED` 时，不能构造确定的来源聚合元组集合。

## 七、来源聚合元组消费再次收紧

### TM-R5-22 来源聚合元组必须由已登记映射派生

R4 的每个 `Required Source Completeness Aggregate Resolution Tuple` 必须新增：

```text
Registered Required Dimension Mapping Aggregate Registration Resolution ID and Digest
Mapping Result = MAPPED
Mapped Source Completeness Semantic Domain Key and Digest
```

该映射结果中的来源语义域必须与来源聚合解析的语义域内容同一。时间评价者不得替换目标域或临时构造映射。

### TM-R5-23 完整性要求评价键必须固定映射集合

R4 的评价键由本规则收紧为：

```text
Completeness Requirement Evaluation Key =
  Registered Requirement Set ID and Digest
+ Registered Source Boundary ID and Digest
+ Registered Source Snapshot ID and Digest
+ Exact Query Scope Digest
+ Boundary Shape
+ Exact Required Dimension Mapping Aggregate Resolution Tuple Set Digest
+ Exact Required Source Completeness Semantic Domain Key Set Digest
+ Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
+ Completeness Evaluation Rule Version
```

任何必要维度映射、映射聚合解析、目标来源域、来源聚合解析或评价边界变化必须形成新的评价身份。

### TM-R5-24 评价登记必须验证映射与来源聚合内容同一

```text
Registered QUALIFIED Requirement Set
+ Exact Required Dimension Mapping Aggregate Resolution Tuple Set
+ Exact Required Source Completeness Aggregate Resolution Tuple Set
  -> Candidate Completeness Requirement Evaluation
  -> Completeness Evaluation Registration Attempt
  -> Registered Completeness Requirement Evaluation Resolution
```

评价候选和登记解析必须验证：

```text
Required Dimension Set
= Mapping Tuple Dimension Set
= Source Aggregate Tuple Dimension Set

each Mapping Tuple.Mapped Domain
= corresponding Source Aggregate Tuple.Semantic Domain
```

任何不等、重复、遗漏、未知或冲突必须失败关闭。

### TM-R5-25 时间评价结果必须传播映射失败

```text
all mapping results MAPPED
+ all required source aggregate results COMPLETE
  -> may support SATISFIED

any mapping result NOT_MAPPED or INDETERMINATE
  -> INDETERMINATE

any mapping result CONFLICTED
  -> CONFLICTED

all mappings established
+ at least one required source aggregate INCOMPLETE
+ no conflict
  -> NOT_SATISFIED
```

查询者选择宽域、旧映射或有利目标域不能产生 `SATISFIED`。

### TM-R5-26 认识边界必须固定映射谱系

认识边界只可消费 `SATISFIED` 的已登记时间评价，并新增固定：

```text
Exact Required Dimension Mapping Aggregate Resolution Tuple Set Digest
Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
```

映射候选、聚合、目标域或来源聚合变化必须形成新的评价和认识边界身份；旧 `SATISFIED` 不能覆盖新冲突。

## 八、权威和失败关闭

### TM-R5-27 新增角色必须逐操作分权

映射候选构造、候选登记、映射边界构造、边界登记、边界完整性、映射聚合、聚合记录登记、聚合登记解析、时间评价和认识边界构造权威不得互相传播。

时间侧只能验证来源聚合身份和结果，不能取得来源完整性评价、边界或聚合权威。

### TM-R5-28 非法状态必须失败关闭

- 同一账本位置因记录类型不同而复用；
- 类型化投影自称独立完整账本边界；
- 更正或迁移记录引用已撤销的独立分区对象；
- 目标来源语义域进入映射语义冲突键；
- 映射竞争边界排除不利目标域候选；
- 查询者临时选择必要维度到来源域的映射；
- 映射结果非 `MAPPED` 仍产生确定来源聚合元组；
- 映射目标域与来源聚合语义域不等；
- 旧 `SATISFIED` 覆盖新映射冲突；
- 候选、自检或文件存在替代已登记解析。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`。

## 九、回归与候选级闭合声明

### TM-R5-29 已通过主干不得回归

```text
Correction / Migration Boundary and Aggregate Identity: PRESERVED
Registered Source Completeness Aggregate Consumption: PRESERVED
Temporal Governance Contract Roots: PRESERVED
Canonical Temporal Value Identity: PRESERVED
Mapping Semantic Conflict Aggregation: PRESERVED
Coordinate Registry Boundary Identity: PRESERVED
Temporal-ledger Append-only Direction: PRESERVED
Knowledge Boundary Type Closure: PRESERVED
Historical / Current Separation: PRESERVED
Cross-interface Acyclicity: PRESERVED
```

### TM-R5-30 R5 只声明两个阻断候选闭合

```text
TM-R4-B1 Temporal Record Partition and Position Identity: CLOSED_AS_DRAFT
TM-R4-B2 Required Dimension / Source Completeness Domain Mapping Identity: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R5 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R4-B1 + TM-R4-B2 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R6` 执行交叉接口回归审查。R5 自检不能独立证明两个阻断关闭。
