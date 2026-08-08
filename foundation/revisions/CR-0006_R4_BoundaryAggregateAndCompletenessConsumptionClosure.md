# 时间映射治理有界修订 R4

## 修订信息

```text
Proposal ID: CR-0006-R4
Title: Correction Migration Boundary Aggregate and Source Completeness Consumption Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R3 INTERNAL GOVERNANCE AND SEMANTIC CONFLICT CLOSURE
Repair Basis: CR-0006-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Basis: CR-0005-R4-CR-0006-R3-CROSS-INTERFACE-REGRESSION-REVIEW
Repair Scope: TM-R3-B1 + XREG-B1 only
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
Compatibility Reference: CR-0005-R5
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R3-B1` 与 `XREG-B1`：补齐时间更正、迁移的竞争边界和聚合登记身份，并使时间完整性评价强制消费来源侧已登记聚合解析。它不覆盖基础稿或 R1 至 R3 的历史正文，不创建时间记录、账本、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R4-01 R4 只覆盖两个有界阻断

```text
TM-R3-B1 Correction / Migration Boundary and Aggregate Identity
XREG-B1 Source Completeness Aggregate Resolution Consumption
```

R3 已通过的制度注册根、规范时间值、映射聚合和坐标边界身份继续有效。R4 不修改来源侧完整性聚合语义，也不取得来源完整性评价权威。

### TM-R4-02 新边界和聚合不得自授权

更正、迁移边界与聚合记录只能进入 R1/R2 已定义的已登记追加时间派生账本边界。其规则合同必须由 R3 时间治理制度注册根登记。

```text
Correction / Migration Record
  -/-> prove its competing boundary completeness

Aggregate Resolution
  -/-> grant its own registration authority
  -/-> modify its input ledger boundary

Temporal Completeness Evaluation
  -/-> recompute or replace source aggregate authority
```

## 二、共用登记与账本边界

### TM-R4-03 新规则合同与账本分区必须已登记

本修订对 R3 的时间治理合同类型集合做最小封闭扩展：

```text
TEMPORAL_CORRECTION_BOUNDARY_RULE
TEMPORAL_CORRECTION_AGGREGATE_RULE
TEMPORAL_MIGRATION_BOUNDARY_RULE
TEMPORAL_MIGRATION_AGGREGATE_RULE
```

四类合同必须完整复用 R3 的治理注册表 ID 分配、合同稳定键、候选—登记链、注册表边界、独立完整性和四值登记解析。扩展类型不合并任何定义、登记、边界、完整性或解析权威。

边界与聚合记录必须使用已登记账本分区：

```text
Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Required Registered Temporal Governance Contract Registration Resolution IDs and Digests
+ Temporal Record Type
  -> Registered Append-only Temporal Record Partition
```

本修订使用的记录类型封闭为：

```text
TEMPORAL_CORRECTION_COMPETING_BOUNDARY
TEMPORAL_CORRECTION_AGGREGATE_RESOLUTION
TEMPORAL_MIGRATION_COMPETING_BOUNDARY
TEMPORAL_MIGRATION_AGGREGATE_RESOLUTION
```

每种记录类型拥有独立位置子域；位置永久不可复用，失败写形成永久空洞。记录类型不能通过换分区逃离其语义冲突集合。

### TM-R4-04 共用边界登记解析必须失败关闭

边界候选、登记尝试和登记记录必须内容同一。边界登记解析结果封闭为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有唯一内容同一记录、完整边界记录分区和无冲突支持 `REGISTERED`。合格完整空集支持 `NOT_REGISTERED`；读取、位置、边界或完整性未知支持 `INDETERMINATE`；同键异载荷、位置复用或登记冲突支持 `CONFLICTED`。

## 三、时间更正竞争边界

### TM-R4-05 更正竞争边界必须拥有稳定键

```text
Temporal Correction Competing Record Boundary Key =
  Temporal Correction Semantic Conflict Set Key
+ Registered Temporal Correction Ledger Boundary ID and Digest
+ Exact Qualified Correction Registration Resolution Set Digest
+ Required Correction-ledger Completeness Resolution IDs and Digests
+ Registered Temporal Governance Contract Registration Resolution ID and Digest
  (Type = TEMPORAL_CORRECTION_BOUNDARY_RULE)
+ Correction Boundary Rule Version
```

该键禁止包含边界记录 ID、候选结果、请求 ID、执行者、登记时间或所偏好的更正记录 ID。

精确集合必须覆盖同语义域全部候选更正、登记尝试、登记记录、四值登记解析和冲突谱系。只有 `REGISTERED` 更正可以成为确定成员，但其他状态和不利记录不得从边界谱系删除。

### TM-R4-06 更正边界必须形成内容同一登记链

```text
Candidate Temporal Correction Competing Record Boundary
  -> Correction Boundary Registration Attempt
  -> Registered Temporal Correction Competing Record Boundary
  -> Registered Correction Boundary Registration Resolution
```

候选与登记载荷必须固定边界键、精确成员、时间账本边界、空洞、冲突子域、完整性引用和规则版本。

```text
Temporal Correction Boundary Registration Resolution Key =
  Temporal Correction Competing Record Boundary Key
+ Registered Correction-boundary Record Ledger Boundary ID and Digest
+ Required Boundary-record Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

同键异成员集合、异账本边界、异空洞或异冲突子域必须 `CONFLICTED`。

### TM-R4-07 更正边界完整性必须独立

更正执行者、登记者、边界构造者和聚合者不得评价边界完整性。必要维度至少覆盖：

```text
CARRIER
POSITION_OR_EXACT_SET
READABILITY
CONFLICT_SUBDOMAIN
SEMANTIC_DOMAIN_COVERAGE
```

缺少任一必要维度的确定完整解析时，边界登记解析不得支持确定聚合。

## 四、时间更正聚合解析

### TM-R4-08 更正聚合解析必须拥有稳定键

```text
Temporal Correction Aggregate Resolution Key =
  Temporal Correction Semantic Conflict Set Key
+ Registered Correction Boundary Registration Resolution ID and Digest
+ Required Correction-boundary Completeness Resolution IDs and Digests
+ Registered Temporal Governance Contract Registration Resolution ID and Digest
  (Type = TEMPORAL_CORRECTION_AGGREGATE_RULE)
+ Correction Aggregate Rule Version
```

键不得包含候选聚合结果、执行者、登记时间、置信度或所偏好的更正记录 ID。

### TM-R4-09 更正聚合必须形成内容同一登记链

```text
Registered Complete Temporal Correction Competing Boundary
  -> Candidate Temporal Correction Aggregate Resolution
  -> Correction Aggregate Registration Attempt
  -> Registered Temporal Correction Aggregate Resolution Record
  -> Registered Correction Aggregate Registration Resolution
```

```text
Temporal Correction Aggregate Registration Resolution Key =
  Temporal Correction Aggregate Resolution Key
+ Registered Correction-aggregate Record Ledger Boundary ID and Digest
+ Required Aggregate-record Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

最终登记解析使用：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有 `REGISTERED` 登记解析中的内容同一语义结果可以被当前重述消费。同聚合键异结果、异采用成员或异更正载荷必须 `CONFLICTED`。

### TM-R4-10 更正语义结果保持封闭

```text
APPLIED
NOT_APPLIED
INDETERMINATE
CONFLICTED
```

- 唯一合格更正或多个内容同一更正、完整边界和无冲突支持 `APPLIED`；
- 完整边界证明没有合格已应用更正支持 `NOT_APPLIED`；
- 边界、成员、证据、规则、读取或完整性未知支持 `INDETERMINATE`；
- 不兼容时区、格式、精度、区间、目标字段、载荷或登记结果支持 `CONFLICTED`。

请求时间、登记位置、置信度或“最新”不能选择赢家。

## 五、时间迁移竞争边界

### TM-R4-11 迁移竞争边界必须拥有稳定键

```text
Temporal Migration Competing Record Boundary Key =
  Temporal Migration Semantic Conflict Set Key
+ Registered Temporal Migration Ledger Boundary ID and Digest
+ Exact Qualified Migration Registration Resolution Set Digest
+ Required Migration-ledger Completeness Resolution IDs and Digests
+ Registered Temporal Governance Contract Registration Resolution ID and Digest
  (Type = TEMPORAL_MIGRATION_BOUNDARY_RULE)
+ Migration Boundary Rule Version
```

该键禁止包含边界记录 ID、候选结果、迁移决定 ID、目标合同 ID、执行者、登记时间或所偏好的迁移记录 ID。

精确集合必须覆盖同语义域全部候选迁移、登记尝试、登记记录、四值登记解析和冲突谱系。不同目标合同必须留在同一竞争集合。

### TM-R4-12 迁移边界必须形成内容同一登记链

```text
Candidate Temporal Migration Competing Record Boundary
  -> Migration Boundary Registration Attempt
  -> Registered Temporal Migration Competing Record Boundary
  -> Registered Migration Boundary Registration Resolution
```

```text
Temporal Migration Boundary Registration Resolution Key =
  Temporal Migration Competing Record Boundary Key
+ Registered Migration-boundary Record Ledger Boundary ID and Digest
+ Required Boundary-record Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

候选和登记载荷必须固定完整边界键、成员集合、账本边界、空洞、冲突子域、完整性及规则。登记解析使用 R4-04 的四值语义。

### TM-R4-13 迁移边界完整性必须独立

迁移执行者、登记者、边界构造者和聚合者不得评价迁移边界完整性。必要维度与 R4-07 相同，并必须证明全部同域目标合同成员已覆盖。

未知目标合同登记状态、读取失败或冲突子域不完整时，不能产生确定迁移结果。

## 六、时间迁移聚合解析

### TM-R4-14 迁移聚合解析必须拥有稳定键

```text
Temporal Migration Aggregate Resolution Key =
  Temporal Migration Semantic Conflict Set Key
+ Registered Migration Boundary Registration Resolution ID and Digest
+ Required Migration-boundary Completeness Resolution IDs and Digests
+ Registered Temporal Governance Contract Registration Resolution ID and Digest
  (Type = TEMPORAL_MIGRATION_AGGREGATE_RULE)
+ Migration Aggregate Rule Version
```

键不得包含候选聚合结果、目标合同 ID、决定 ID、执行者、登记时间或所偏好的迁移记录 ID。

### TM-R4-15 迁移聚合必须形成内容同一登记链

```text
Registered Complete Temporal Migration Competing Boundary
  -> Candidate Temporal Migration Aggregate Resolution
  -> Migration Aggregate Registration Attempt
  -> Registered Temporal Migration Aggregate Resolution Record
  -> Registered Migration Aggregate Registration Resolution
```

```text
Temporal Migration Aggregate Registration Resolution Key =
  Temporal Migration Aggregate Resolution Key
+ Registered Migration-aggregate Record Ledger Boundary ID and Digest
+ Required Aggregate-record Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

最终登记解析使用：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同聚合键异目标合同、异成员、异迁移作用域或异结果载荷必须 `CONFLICTED`。

### TM-R4-16 迁移语义结果保持封闭

```text
MIGRATED
NOT_MIGRATED
INDETERMINATE
CONFLICTED
```

- 唯一目标合同和内容同一迁移、完整边界及无冲突支持 `MIGRATED`；
- 完整边界证明没有合格迁移支持 `NOT_MIGRATED`；
- 边界、合同、成员、决定资格、读取或完整性未知支持 `INDETERMINATE`；
- 多个目标合同、不兼容作用域、区间、载荷或登记结果支持 `CONFLICTED`。

决定时间、登记位置或“最新目标合同”不能选择赢家。

## 七、更正迁移的历史边界与分权

### TM-R4-17 当前重述只能消费已登记聚合

当前重述必须固定：

```text
Registered Correction Aggregate Registration Resolution ID and Digest
Correction Semantic Result = APPLIED or NOT_APPLIED

Registered Migration Aggregate Registration Resolution ID and Digest
Migration Semantic Result = MIGRATED or NOT_MIGRATED
```

`INDETERMINATE | CONFLICTED` 不能支持确定重述。旧时间记录、旧账本边界、旧聚合和旧认识视图不可覆盖；新成员或新证据必须形成新的边界、聚合和当前视图身份。

### TM-R4-18 更正和迁移角色必须逐操作分权

```text
Correction / Migration Boundary Construction Authority Types
Correction / Migration Boundary Registration Authority Types
Correction / Migration Boundary Completeness Authority Types
Correction / Migration Aggregate Execution Authority Types
Correction / Migration Aggregate Registration Authority Types
Correction / Migration Aggregate Registration Resolution Authority Types
```

更正与迁移互不继承。边界、完整性、聚合执行和登记互不传播，也不能取得原始断言、规范值、查询坐标或制度冻结权威。

## 八、来源完整性聚合消费接口

### TM-R4-19 R4 覆盖旧的完整性评价输入字段

本规则对 R2 的 `Completeness Requirement Evaluation Key` 形成窄覆盖。以下旧字段不再是合格的直接消费输入：

```text
Exact Registered Source Completeness Record Set Digest
```

底层来源完整性记录集合只可作为来源聚合解析的只读谱系存在，不能被时间评价选择或直接作为满足证据。

### TM-R4-20 每个必要维度必须映射到精确来源聚合元组

```text
Required Source Completeness Aggregate Resolution Tuple =
  Required Dimension ID and Version
+ Source Completeness Semantic Domain Key and Digest
+ Registered Source Completeness Aggregate Resolution ID and Digest
+ Source Completeness Aggregate Result
+ Registered Source Completeness Evaluation Boundary ID and Digest
+ Required Evaluation-boundary Completeness Resolution IDs and Digests
```

有效要求集合中的每个必要维度必须与恰好一个适用元组一一对应。重复维度、遗漏维度、多对一歧义、作用域不匹配或额外替代元组均不合格。

元组集合按规范字节序排列并形成：

```text
Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
```

### TM-R4-21 完整性要求评价键必须固定聚合解析集合

R2 的评价键由本规则收紧为：

```text
Completeness Requirement Evaluation Key =
  Registered Requirement Set ID and Digest
+ Registered Source Boundary ID and Digest
+ Registered Source Snapshot ID and Digest
+ Exact Query Scope Digest
+ Boundary Shape
+ Exact Required Source Completeness Semantic Domain Key Set Digest
+ Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
+ Completeness Evaluation Rule Version
```

要求集合、边界、快照、作用域、形态、必要语义域、任一聚合解析 ID、摘要、结果、评价边界或规则变化，必须形成新的评价身份。

时间评价不能以相同字面结果替代不同聚合解析身份。

### TM-R4-22 评价候选—登记链必须消费已登记聚合

R2 的输入链由本规则收紧为：

```text
Registered QUALIFIED Requirement Set
+ Registered Source Boundary and Snapshot
+ Exact Required Source Completeness Aggregate Resolution Tuple Set
  -> Candidate Completeness Requirement Evaluation
  -> Completeness Evaluation Registration Attempt
  -> Registered Completeness Requirement Evaluation Resolution
```

每个元组中的来源聚合解析必须已登记、内容同一、适用于同一来源边界与精确查询作用域，并固定其完整评价边界及完整性解析。

候选、登记尝试和登记解析必须共同固定完整元组集合、逐维度资格、结果及全部来源聚合谱系。

### TM-R4-23 时间完整性评价结果必须按来源聚合失败关闭

时间评价仍使用：

```text
SATISFIED
NOT_SATISFIED
INDETERMINATE
CONFLICTED
```

映射规则为：

```text
all required tuples COMPLETE and compatible
  -> may support SATISFIED

at least one required tuple INCOMPLETE,
all tuple identities and boundaries complete,
and no conflict
  -> NOT_SATISFIED

any required tuple INDETERMINATE,
missing, unreadable, scope-unknown or registration-unknown
  -> INDETERMINATE

any required tuple CONFLICTED,
duplicate or incompatible tuple mapping,
or same evaluation key with incompatible payload
  -> CONFLICTED
```

空集合、选取单一 `COMPLETE` 底层记录、遗漏不利聚合或读取失败均不能产生 `SATISFIED`。

### TM-R4-24 认识边界消费规则保持但输入更强

认识边界仍只可消费：

```text
Registered Completeness Requirement Evaluation Resolution ID and Digest
Resolution Result = SATISFIED
Registered QUALIFIED Requirement Set ID and Digest
Effective Required Dimension Set Digest
Exact Required Source Completeness Aggregate Resolution Tuple Set Digest
```

来源聚合解析变化、评价边界变化或必要维度变化必须形成新的时间评价和认识边界身份。认识边界不能沿用旧 `SATISFIED` 结果覆盖新的来源冲突。

### TM-R4-25 来源与时间权威边界保持分离

来源侧继续独占：

```text
Source Completeness Evidence Evaluation
Source Completeness Evaluation Boundary
Source Completeness Aggregate Resolution
```

时间侧只验证已登记来源聚合解析的身份、适用性、覆盖和结果，并据此形成时间要求评价。时间评价权不能重算、修正或登记来源聚合结果；来源聚合权也不能产生时间认识边界。

## 九、非法状态与回归

### TM-R4-26 新增非法状态必须失败关闭

- 更正或迁移边界缺少稳定键、精确成员集合或必要完整性；
- 请求 ID、决定 ID、目标合同或结果载荷隔离语义冲突；
- 边界构造者或聚合者自证边界完整；
- 聚合按登记位置、置信度或“最新”选赢家；
- 当前重述消费单一候选、未登记边界或未登记聚合；
- 时间完整性评价直接选择来源底层完整性记录；
- 必要维度没有与来源聚合解析一一对应；
- `INDETERMINATE | CONFLICTED` 来源聚合支持 `SATISFIED`；
- 旧认识边界覆盖新来源聚合冲突；
- 候选、自检或文件存在替代已登记解析。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`，不得静默升级为确定时间真值。

### TM-R4-27 已通过主干不得回归

```text
Temporal Governance Contract Roots: PRESERVED
Canonical Temporal Value Identity: PRESERVED
Mapping Semantic Conflict Aggregation: PRESERVED
Coordinate Registry Boundary Identity: PRESERVED
Raw Assertion Provider Identity: PRESERVED
Temporal-ledger Append-only Boundary: PRESERVED
Knowledge Boundary Type Closure: PRESERVED
Historical / Current View Separation: PRESERVED
Four-stage Acyclicity: PRESERVED
WS-01 Reference Direction: PRESERVED
```

## 十、候选级闭合声明

### TM-R4-28 R4 只声明两个阻断候选闭合

```text
TM-R3-B1 Correction / Migration Boundary and Aggregate Identity: CLOSED_AS_DRAFT
XREG-B1 Source Completeness Aggregate Resolution Consumption: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R4 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R3-B1 + XREG-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R5` 执行交叉接口回归审查。R4 自检不能独立证明两个阻断关闭。
