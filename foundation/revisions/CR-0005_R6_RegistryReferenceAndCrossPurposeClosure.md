# 来源注册表接口有界修订 R6

## 修订信息

```text
Proposal ID: CR-0005-R6
Title: Lifecycle Registry Reference and Cross-purpose Consistency Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R5 LIFECYCLE ORDERING AND SUPERSESSION RESOLUTION IDENTITY CLOSURE
Repair Basis: CR-0005-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R5-B1 + SR-R5-B2 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Independent Model Re-review Required: YES
Cross-interface Regression Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0006-R5
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R5-B1` 与 `SR-R5-B2`：闭合生命周期解析注册表引用根身份，并建立跨解析目的的完整组合冲突聚合。它不覆盖基础稿或 R1 至 R5 的历史正文，不创建注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R6-01 R6 只覆盖两个有界阻断

```text
SR-R5-B1 Lifecycle Resolution Registry Reference Identity
SR-R5-B2 Cross-purpose Lifecycle Resolution Aggregation
```

R5 已通过的候选解析、同目的竞争边界、聚合登记、历史不可覆盖与来源适用性失败关闭方向继续有效。

### SR-R6-02 根引用与组合解析不得自授权

```text
Registry Reference Candidate
  -/-> allocate its own registry ID
  -/-> register its own source registry contract
  -/-> prove its own bootstrap boundary completeness

Cross-purpose Resolution
  -/-> create per-purpose lifecycle claims
  -/-> create temporal coordinate truth
  -/-> omit an unfavorable required purpose
```

所有授权必须来自 R4 已登记来源注册表合同及适用的 `IF-0006`、`IF-0007` 外部边界。

## 二、生命周期解析注册表引用语义根

### SR-R6-03 注册表引用语义键必须排除引用载荷

```text
Lifecycle Resolution Registry Reference Semantic Conflict Set Key =
  Registered Source Registry ID Allocation Resolution ID and Digest
+ Allocated Candidate Source Registry ID and Version
+ Lifecycle Registry Role = LIFECYCLE_RESOLUTION_REGISTRY
+ Registry Reference Semantic Rule Version
```

该键禁止包含合同 ID、作用域、记录类型集合、引用记录 ID、位置、登记时间或执行者。对同一已分配注册表 ID 的不同合同或作用域声称必须进入同一冲突集合。

### SR-R6-04 分配解析必须与生命周期注册表 ID 内容同一

候选引用的最低资格不变量为：

```text
Allocation Resolution Result = ALLOCATED
Allocation Resolution.Candidate Source Registry ID and Version
  = Lifecycle Resolution Registry ID and Version
Allocation Resolution.Intended Registry Domain
  = LIFECYCLE_RESOLUTION
```

任一字段不等、解析非 `ALLOCATED`、摘要不匹配或分配边界未知时，候选不得进入确定引用登记。

### SR-R6-05 候选引用载荷必须完整

```text
Lifecycle Resolution Registry Reference Candidate Payload =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Registered Source Registry Contract Registration Resolution ID and Digest
+ Contract-bound Registry ID and Version
+ Contract-bound Registry Domain
+ Lifecycle Resolution Registry Scope Digest
+ Exact Permitted Lifecycle Record Type Set Digest
+ Lifecycle Resolution Rule Contract Payload Digest
+ Bootstrap Authority Instance IDs and Scope Digests
+ Candidate Canonicalization Rule Version
```

合同登记解析必须为 `REGISTERED`，合同中的注册表 ID、版本、域和作用域必须与分配解析及候选载荷内容同一。合同允许的记录类型至少封闭覆盖：

```text
LIFECYCLE_REGISTRY_REFERENCE
LIFECYCLE_CANDIDATE_RESOLUTION
LIFECYCLE_COMPETING_BOUNDARY
LIFECYCLE_AGGREGATE_RESOLUTION
LIFECYCLE_REQUIRED_PURPOSE_QUALIFICATION
LIFECYCLE_CROSS_PURPOSE_RESOLUTION
```

### SR-R6-06 候选引用必须拥有稳定键

```text
Lifecycle Resolution Registry Reference Candidate Key =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Candidate Reference Payload Digest
+ Candidate Identity Rule Version
```

候选引用 ID 与候选键一对一且不可复用。载荷变化必须产生新候选，但仍进入同一引用语义冲突集合。

## 三、引用引导登记和冲突聚合

### SR-R6-07 引用候选允许唯一引导登记路径

```text
Registered ALLOCATED Source Registry ID Resolution
+ Registered Source Registry Contract Registration Resolution
+ Candidate Lifecycle Resolution Registry Reference
  -> Bootstrap Reference Registration Attempt
  -> Registered Bootstrap Reference Record
```

引导登记仅允许写入 `LIFECYCLE_REGISTRY_REFERENCE` 记录，不依赖尚未成立的注册表引用解析。它必须在已分配注册表中原子取得不可复用位置；失败写形成永久空洞。

除该受限引导记录外，任何生命周期候选、边界、聚合或组合记录都必须先固定最终 `REGISTERED` 引用解析。

### SR-R6-08 单一引用候选登记必须四值化

```text
Lifecycle Registry Reference Candidate Registration Resolution Key =
  Lifecycle Resolution Registry Reference Candidate Key
+ Registered Bootstrap Source Boundary ID and Digest
+ Required Bootstrap-boundary Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

唯一内容同一引导记录和完整边界支持 `REGISTERED`；完整合格空集支持 `NOT_REGISTERED`；读取、位置、边界或完整性未知支持 `INDETERMINATE`；同候选键异载荷、ID 复用或登记冲突支持 `CONFLICTED`。

### SR-R6-09 引用竞争边界必须覆盖全部同根候选

```text
Lifecycle Registry Reference Competing Boundary Key =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Registered Bootstrap Source Boundary ID and Digest
+ Exact Reference Candidate Registration Resolution Set Digest
+ Required Bootstrap Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界必须覆盖同分配解析下的全部合同、作用域、记录类型和规则载荷候选及其冲突谱系。边界形成候选、登记尝试、内容同一记录和四值边界登记解析。

引用候选构造者、引导登记者和最终引用聚合者不得评价该边界完整性。

### SR-R6-10 最终注册表引用解析必须拥有稳定键

```text
Lifecycle Resolution Registry Reference Aggregate Resolution Key =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Registered Reference Competing Boundary Registration Resolution ID and Digest
+ Required Reference-boundary Completeness Resolution IDs and Digests
+ Registry Reference Aggregate Rule Version
```

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

唯一内容同一候选或多个内容同一候选支持 `REGISTERED`；完整空集支持 `NOT_REGISTERED`；集合、读取、合同或完整性未知支持 `INDETERMINATE`；异合同、异作用域、异记录类型、异规则载荷或同键异结果支持 `CONFLICTED`。

最终解析形成候选—登记链并固定聚合载荷摘要；同聚合键异载荷必须进入聚合记录冲突边界。

```text
Lifecycle Registry Reference Aggregate Registration Resolution Key =
  Lifecycle Resolution Registry Reference Aggregate Resolution Key
+ Registered Reference Aggregate-record Source Boundary ID and Digest
+ Required Aggregate-record Boundary Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

外层登记解析结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。下游只可消费外层 `REGISTERED` 且其内层引用语义结果同样为 `REGISTERED` 的内容同一载荷。

### SR-R6-11 所有生命周期对象必须固定最终引用解析

R5 的以下对象键由本规则收紧，必须新增：

```text
Registered Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
Registration Result = REGISTERED
Registry Reference Semantic Result = REGISTERED
Registered Lifecycle Resolution Registry Reference Payload Digest
```

适用对象包括候选解析、候选登记解析、竞争边界、聚合解析、聚合登记解析、必要目的资格和跨目的组合解析。裸分配解析、裸合同解析或引导记录不能替代最终引用解析。

## 四、父级生命周期一致性语义域

### SR-R6-12 父级语义键必须排除解析目的

```text
Cross-purpose Lifecycle Consistency Semantic Conflict Set Key =
  Source Applicability Change Conflict Set Key
+ Registered Source Applicability Change Set Boundary ID and Digest
+ Registered Change-boundary Completeness Resolution IDs and Digests
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Registered Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
+ Registered Source Registry Contract Registration Resolution ID and Digest
+ Cross-purpose Semantic Rule Version
```

该键禁止包含 `Lifecycle Resolution Purpose`、逐目的结果、目的集合载荷、证据集合、记录 ID、位置、执行者和登记时间。

R5 的逐目的语义键继续作为子域键，但不能直接支持来源适用性确定结果。

## 五、必要目的集合资格

### SR-R6-13 必要目的资格语义键必须稳定

```text
Lifecycle Required Purpose Qualification Semantic Key =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Registered Lifecycle Resolution Rule Contract Payload Digest
+ Purpose Qualification Rule Version
```

必要目的集合不得进入该语义键；不同目的集合声称必须在同一资格语义域竞争。

### SR-R6-14 必要目的候选必须由完整变化集合确定

```text
Candidate Lifecycle Required Purpose Qualification Payload =
  Lifecycle Required Purpose Qualification Semantic Key
+ Exact Applicable Change Type Set Digest
+ Exact Required Lifecycle Resolution Purpose Set Digest
+ Purpose Applicability Proof Digest
+ Candidate Qualification Result
+ Candidate Payload Rule Version
```

目的集合必须从完整变化集合和已登记规则合同确定。最低约束包括：

```text
SUPERSEDED present
  -> EFFECT_INTERVAL_ORDERING + UNIQUE_SUCCESSOR + SUPERSESSION_TARGET required

REVOKED present with another effect
  -> EFFECT_INTERVAL_ORDERING + REVOCATION_PRECEDENCE required

multiple temporally comparable effects
  -> EFFECT_INTERVAL_ORDERING required
```

查询者不能省略不利目的或临时添加目的改变结果。

### SR-R6-15 必要目的资格必须完整聚合

候选资格取得：

```text
Lifecycle Required Purpose Qualification Candidate Key =
  Lifecycle Required Purpose Qualification Semantic Key
+ Candidate Purpose Qualification Payload Digest
+ Candidate Identity Rule Version
```

并形成：

```text
Candidate Purpose Qualification
  -> Purpose Qualification Registration Attempt
  -> Registered Purpose Qualification Candidate Record
  -> Purpose Qualification Candidate Registration Resolution
```

候选登记解析键固定候选键、已登记生命周期注册表边界、必要完整性和登记解析规则版本，结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

全部同语义域候选进入：

```text
Lifecycle Required Purpose Qualification Competing Boundary Key =
  Lifecycle Required Purpose Qualification Semantic Key
+ Registered Lifecycle Registry Boundary ID and Digest
+ Exact Qualified Purpose Candidate Resolution Set Digest
+ Required Purpose-boundary Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

最终资格聚合键为：

```text
Lifecycle Required Purpose Qualification Aggregate Resolution Key =
  Lifecycle Required Purpose Qualification Semantic Key
+ Registered Purpose Qualification Competing Boundary Resolution ID and Digest
+ Required Purpose-boundary Completeness Resolution IDs and Digests
+ Registered Lifecycle Resolution Rule Contract Payload Digest
+ Purpose Qualification Aggregate Rule Version
```

聚合形成候选—登记链，最终语义结果为：

```text
QUALIFIED
NOT_QUALIFIED
INDETERMINATE
CONFLICTED
```

```text
Lifecycle Required Purpose Aggregate Registration Resolution Key =
  Lifecycle Required Purpose Qualification Aggregate Resolution Key
+ Registered Purpose Aggregate-record Registry Boundary ID and Digest
+ Required Purpose Aggregate-record Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

外层登记解析结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。只有外层 `REGISTERED` 且内层语义结果 `QUALIFIED` 可以进入跨目的组合。

同键异必要目的集合必须 `CONFLICTED`。只有 `QUALIFIED` 可以进入跨目的组合。

## 六、跨目的候选与竞争边界

### SR-R6-16 跨目的候选必须覆盖全部必要目的

```text
Cross-purpose Lifecycle Resolution Candidate Payload =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Registered Required Purpose Aggregate Registration Resolution ID and Digest
+ Required Purpose Semantic Result = QUALIFIED
+ Exact Required Purpose Set Digest
+ Exact Per-purpose Aggregate Resolution Tuple Set Digest
+ Cross-purpose Consistency Proof Digest
+ Claimed Combined Effective State or NOT_ESTABLISHED
+ Claimed Combined Successor ID and Digest or NOT_APPLICABLE or NOT_ESTABLISHED
+ Candidate Payload Rule Version
```

每个元组固定目的、逐目的聚合登记解析 ID 与摘要、聚合载荷摘要和语义结果。每个必要目的必须恰好一个元组；不得重复、遗漏或使用非 `REGISTERED` 聚合。

### SR-R6-17 跨目的候选必须拥有稳定键和登记解析

```text
Cross-purpose Lifecycle Resolution Candidate Key =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Candidate Cross-purpose Payload Digest
+ Candidate Identity Rule Version
```

候选形成登记尝试、内容同一记录和四值候选登记解析。候选 ID 不可复用；同候选键异载荷必须 `CONFLICTED`。

```text
Cross-purpose Lifecycle Candidate Registration Resolution Key =
  Cross-purpose Lifecycle Resolution Candidate Key
+ Registered Lifecycle Registry Boundary ID and Digest
+ Required Candidate-record Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

登记解析结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`；只有 `REGISTERED` 候选可以进入组合竞争集合。

### SR-R6-18 跨目的竞争边界必须覆盖全部组合候选

```text
Cross-purpose Lifecycle Resolution Competing Boundary Key =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Registered Lifecycle Registry Boundary ID and Digest
+ Exact Cross-purpose Candidate Registration Resolution Set Digest
+ Required Cross-purpose Boundary Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖全部组合候选、登记尝试、记录、候选解析和冲突谱系，并形成内容同一的四值边界登记解析。组合构造者和最终聚合者不能自证边界完整。

```text
Cross-purpose Competing Boundary Registration Resolution Key =
  Cross-purpose Lifecycle Resolution Competing Boundary Key
+ Registered Cross-purpose Boundary-record Registry Boundary ID and Digest
+ Required Boundary-record Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

同键异成员、异空洞或异冲突子域必须 `CONFLICTED`。

## 七、跨目的聚合解析

### SR-R6-19 跨目的聚合必须拥有稳定键

```text
Cross-purpose Lifecycle Aggregate Resolution Key =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Registered Required Purpose Aggregate Registration Resolution ID and Digest
+ Required Purpose Semantic Result = QUALIFIED
+ Registered Cross-purpose Competing Boundary Registration Resolution ID and Digest
+ Required Cross-purpose Boundary Completeness Resolution IDs and Digests
+ Registered Lifecycle Resolution Rule Contract Payload Digest
+ Cross-purpose Aggregate Rule Version
```

聚合键不得包含候选结果、所偏好的目的或候选 ID。

### SR-R6-20 跨目的聚合必须形成登记解析

```text
Registered Complete Cross-purpose Competing Boundary
  -> Candidate Cross-purpose Lifecycle Aggregate Resolution
  -> Cross-purpose Aggregate Registration Attempt
  -> Registered Cross-purpose Lifecycle Aggregate Resolution Record
  -> Registered Cross-purpose Aggregate Registration Resolution
```

最终登记解析键固定聚合键、已登记聚合记录边界、必要完整性和登记规则版本，结果为：

```text
Cross-purpose Aggregate Registration Resolution Key =
  Cross-purpose Lifecycle Aggregate Resolution Key
+ Registered Cross-purpose Aggregate-record Registry Boundary ID and Digest
+ Required Aggregate-record Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

结果为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

同聚合键异采用目的、异组合状态、异后继或异载荷必须 `CONFLICTED`。

### SR-R6-21 组合语义结果必须封闭且冲突优先

```text
CONSISTENT_RESOLVED
NOT_RESOLVED
INDETERMINATE
CONFLICTED
```

- 全部必要目的已覆盖，逐目的解析均兼容且唯一支持同一状态和后继时，可以 `CONSISTENT_RESOLVED`；
- 完整集合证明无法建立确定组合且不存在未知或冲突时，可以 `NOT_RESOLVED`；
- 目的资格、逐目的解析、组合候选、边界或证据未知时必须 `INDETERMINATE`；
- 顺序、区间、后继、替代目标、撤销优先、必要目的集合或组合载荷不兼容时必须 `CONFLICTED`。

不同目的分别 `RESOLVED` 不足以证明组合一致。

## 八、来源适用性消费收紧

### SR-R6-22 来源适用性只能消费跨目的聚合

R5 的 `Lifecycle Resolution Consumption Reference` 由本规则覆盖为：

```text
Lifecycle Resolution Consumption Reference =
  Registered Cross-purpose Aggregate Registration Resolution ID and Digest
+ Registered Cross-purpose Aggregate Payload Digest
or
  LIFECYCLE_RESOLUTION_NOT_REQUIRED
```

存在任何必要生命周期解析目的时，不允许 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`。

```text
CONSISTENT_RESOLVED -> may support uniquely proven effective state
NOT_RESOLVED       -> CONFLICTED
INDETERMINATE      -> INDETERMINATE
CONFLICTED         -> CONFLICTED
```

逐目的聚合、单一有利目的或裸后继声明不能直接进入来源适用性解析。

### SR-R6-23 历史组合解析不可覆盖

必要目的集合、逐目的解析、组合候选、规则、证据或边界变化必须形成新的资格、组合聚合和来源适用性身份。历史对象继续固定旧注册表引用、目的资格和组合解析。

## 九、权威和失败关闭

### SR-R6-24 新增角色必须逐操作分权

引导引用登记、引用边界构造、引用完整性、引用聚合、目的资格、组合构造、组合边界、组合完整性、组合聚合和组合登记权威必须分别授权。任何角色都不能取得来源记录、时间坐标、制度冻结或运行时权威。

### SR-R6-25 非法状态必须失败关闭

- 分配解析中的候选 ID 与生命周期注册表 ID 不同；
- 引用候选扩大已登记合同作用域或记录类型；
- 普通生命周期记录绕过最终引用解析；
- 解析目的进入父级一致性键；
- 必要目的集合由查询者临时选择；
- 组合候选遗漏或重复必要目的；
- 不兼容逐目的结果产生 `CONSISTENT_RESOLVED`；
- 来源适用性消费单一逐目的解析；
- 当前组合覆盖历史解析；
- 候选、自检或文件存在替代已登记聚合解析。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`。

## 十、回归与候选级闭合声明

### SR-R6-26 已通过主干不得回归

```text
Registry Root Allocation and Contract Registration: PRESERVED
Lifecycle Candidate and Same-purpose Aggregation: PRESERVED
Source Version Conflict Aggregation: PRESERVED
Source Completeness Aggregate Resolution: PRESERVED
Applicability Change Conflict Set: PRESERVED
Boundary / Snapshot Reproducibility: PRESERVED
Four-value Coordinate Subject Totality: PRESERVED
Historical / Current Separation: PRESERVED
Cross-interface Acyclicity: PRESERVED
```

### SR-R6-27 R6 只声明两个阻断候选闭合

```text
SR-R5-B1 Lifecycle Resolution Registry Reference Identity: CLOSED_AS_DRAFT
SR-R5-B2 Cross-purpose Lifecycle Resolution Aggregation: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R6 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R5-B1 + SR-R5-B2 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R5` 执行交叉接口回归审查。R6 自检不能独立证明两个阻断关闭。
