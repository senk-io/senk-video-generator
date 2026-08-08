# 时间映射治理有界修订 R8

## 修订信息

```text
Proposal ID: CR-0006-R8
Title: Governed Temporal Record-type Catalog Evolution Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R7 CLAIM PROOF AND T-SCOPED COVERAGE CLOSURE
Repair Basis: CR-0006-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R7-B1 only
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
Compatibility Reference: CR-0005-R9
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R7-B1`：把 R5 的封闭时间记录类型映射提升为受治理、可演进、可按边界重放的目录合同，并为 R6/R7 的六种证明记录建立合法映射资格。它不改变账本 ID、账本类型、全局位置键、`B/T/K` 或查询坐标身份，不覆盖基础稿或 R1 至 R7 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订边界

### TM-R8-01 R8 只覆盖一个有界阻断

```text
TM-R7-B1 Temporal Mapping Record Type Catalog Evolution
```

R7 已通过的声明级不利证明共同竞争、`T` 范围全域覆盖、评价子对象和阶段无环方向继续有效。

### TM-R8-02 类型目录不得自授权或改变位置模型

```text
Temporal Record-type Catalog
  -/-> allocate its own governance registry ID
  -/-> register its own governance contract
  -/-> prove its own catalog boundary completeness
  -/-> allocate temporal ledger position
  -/-> create a temporal ledger or ledger type

Record-type Eligibility
  -/-> change Temporal Ledger ID or Version
  -/-> change Temporal Ledger Type
  -/-> change Append Epoch or Position Value
```

目录只解释规范记录判别字段到既有账本类型的映射，不取得记录构造、位置分配、登记、边界或完整性权威。

## 二、目录治理根和演进身份

### TM-R8-03 类型目录必须复用时间治理合同注册表

新增治理合同类型：

```text
Governance Contract Type = TEMPORAL_RECORD_TYPE_CATALOG
```

它复用 R3 已分配 `Temporal Governance Registry`、合同候选—登记链、合同注册表边界和四值合同登记解析。目录合同记录只进入时间治理合同注册表，不进入其所解释的更正、迁移或映射账本。

### TM-R8-04 目录必须拥有稳定谱系根

```text
Temporal Record-type Catalog Lineage Root Key =
  Registered Temporal Governance Registry ID Allocation Resolution ID and Digest
+ Allocated Governance Registry ID and Version
+ Governance Contract Type = TEMPORAL_RECORD_TYPE_CATALOG
+ Exact Governed Temporal Ledger ID-and-type Set Digest
+ Catalog Lineage Rule Version
```

目录合同 ID、版本、候选映射摘要、登记时间、执行者和记录类型集合不得进入谱系根。

### TM-R8-05 每次目录演进必须固定前驱和生效切点

```text
Temporal Record-type Catalog Evolution Semantic Conflict Set Key =
  Temporal Record-type Catalog Lineage Root Key
+ Registered Predecessor Catalog Aggregate Registration Resolution ID and Digest
    or CANONICAL_R5_CATALOG_GENESIS_MARKER
+ Registered Catalog Effective-cut Vector ID and Digest
+ Catalog Evolution Semantic Rule Version
```

同一前驱与生效切点的全部候选目录进入同一语义冲突集合。目录合同 ID／版本、规则文本版本、登记时间或写入者不能隔离冲突。

初始候选只允许规范 R5 基线和 `GENESIS` 标记；后继候选必须固定外层 `REGISTERED` 且内层 `REGISTERED` 的唯一前驱目录聚合解析。

### TM-R8-06 生效切点向量必须覆盖全部受治理账本

```text
Temporal Record-type Catalog Effective-cut Vector Key =
  Temporal Record-type Catalog Lineage Root Key
+ Exact Per-ledger Effective Cut Set
+ Required Cut-boundary Completeness Resolution IDs and Digests
+ Effective-cut Rule Version
```

每个账本切点至少固定：

```text
Temporal Ledger ID and Version
Temporal Ledger Type
Registered Predecessor Ledger Boundary ID and Digest
Last Predecessor Position or Canonical Empty-ledger Marker
First Position Eligible for Successor Catalog
Append Epoch
```

切点候选、登记尝试、完整竞争边界和四值解析必须内容同一。它们位于 `TEMPORAL_RECORD_TYPE_CATALOG` 治理注册表的非账本伴随子域，不进入任何时间账本。目录定义者和记录登记者不能自证切点完整。

### TM-R8-07 目录候选载荷必须完整

```text
Temporal Record-type Catalog Candidate Payload =
  Temporal Record-type Catalog Evolution Semantic Conflict Set Key
+ Temporal Governance Contract Key and Payload Digest
+ Exact Temporal Record Type-to-ledger Mapping Set
+ Exact Governed Ledger ID, Version and Type Set
+ Predecessor Mapping Set Digest or CANONICAL_R5_MAPPING_DIGEST
+ Append-only Mapping Evolution Proof Digest
+ Registered Effective-cut Vector Resolution ID and Digest
+ Canonical Record Discriminator Rule Version
+ Catalog Canonicalization Rule Version
```

候选载荷保存精确全集，不采用开放世界类型许可。

### TM-R8-08 初始目录必须内容同一承接 R5

规范初始目录精确包含：

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

其映射集合摘要必须与 `TM-R5-04` 的规范映射内容同一。不同基线候选必须在 `GENESIS` 演进域内竞争，不能并列成为多个初始目录。

### TM-R8-09 后继目录必须精确追加 R6 和 R7 类型

R8 目标后继目录在 R5 初始目录上只追加：

```text
REQUIRED_DIMENSION_MAPPING_PROOF_QUALIFICATION
  -> Temporal Ledger Type = MAPPING

REQUIRED_DIMENSION_MAPPING_PROOF_BOUNDARY
  -> Temporal Ledger Type = MAPPING

REQUIRED_DIMENSION_MAPPING_PROOF_AGGREGATE
  -> Temporal Ledger Type = MAPPING

MAPPING_CLAIM_PROOF_QUALIFICATION
  -> Temporal Ledger Type = MAPPING

MAPPING_CLAIM_PROOF_BOUNDARY
  -> Temporal Ledger Type = MAPPING

MAPPING_CLAIM_PROOF_AGGREGATE
  -> Temporal Ledger Type = MAPPING
```

后继精确全集因此为 R5 七种记录加 R6/R7 六种记录。证明和声明级证明类型共享既有 `MAPPING` 全局位置域，不创建新账本、分区、位置命名空间或追加纪元。

### TM-R8-10 目录候选必须拥有稳定键

```text
Temporal Record-type Catalog Candidate Key =
  Temporal Record-type Catalog Evolution Semantic Conflict Set Key
+ Candidate Catalog Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。同一演进域内异映射、异前驱载荷、异切点载荷或异受治理账本集合必须竞争。

## 三、目录登记、竞争和聚合

### TM-R8-11 目录合同必须形成内容同一登记链

```text
Registered ALLOCATED Temporal Governance Registry ID
+ Candidate Temporal Record-type Catalog Contract
  -> Temporal Governance Contract Registration Attempt
  -> Registered Temporal Governance Contract Record
  -> Temporal Governance Contract Registration Resolution
```

合同类型必须是 `TEMPORAL_RECORD_TYPE_CATALOG`。候选目录载荷摘要必须等于登记合同载荷摘要；同合同键异载荷依 R3 为 `CONFLICTED`。

### TM-R8-12 目录竞争边界必须覆盖全部同域合同

```text
Temporal Record-type Catalog Competing Boundary Key =
  Temporal Record-type Catalog Evolution Semantic Conflict Set Key
+ Registered Temporal Governance Contract Registry Boundary ID and Digest
+ Exact Catalog Contract Registration Resolution Set Digest
+ Required Catalog Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖全部候选、登记尝试、合同记录、四值合同解析、永久空洞、前驱分叉、切点冲突和类型映射冲突谱系。不得按合同版本、登记时间或偏好映射过滤候选。

边界必须形成候选、登记尝试、内容同一记录和四值边界登记解析。

### TM-R8-13 目录聚合必须四值化并外层登记

```text
Temporal Record-type Catalog Aggregate Resolution Key =
  Temporal Record-type Catalog Evolution Semantic Conflict Set Key
+ Registered Catalog Competing Boundary Registration Resolution ID and Digest
+ Required Catalog-boundary Completeness Resolution IDs and Digests
+ Catalog Aggregate Rule Version
```

内层语义结果为：

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

唯一内容同一且合同解析为 `REGISTERED` 的目录支持 `REGISTERED`；完整空集支持 `NOT_REGISTERED`；边界、前驱、切点或完整性未知支持 `INDETERMINATE`；同前驱多后继、同类型异账本映射、删除／重映射旧类型或同键异结果支持 `CONFLICTED`。

```text
Registered Complete Catalog Competing Boundary
  -> Candidate Catalog Aggregate Resolution
  -> Catalog Aggregate Registration Attempt
  -> Registered Catalog Aggregate Record
  -> Catalog Aggregate Registration Resolution
```

外层解析同样四值化。目录竞争边界、聚合记录和登记解析均位于 `TEMPORAL_RECORD_TYPE_CATALOG` 治理注册表的合同治理子域，不进入更正、迁移或映射账本。下游只可消费外层 `REGISTERED` 且内层 `REGISTERED` 的目录载荷。

### TM-R8-14 目录演进必须单调且保留原映射

```text
Successor Mapping Set
  = Predecessor Mapping Set
  + New Record Type-to-ledger Mappings
```

以下状态必须 `CONFLICTED`：

- 删除前驱类型；
- 把前驱类型改映射到另一账本类型；
- 把同一规范类型同时映射到多个账本类型；
- 改变前驱账本 ID、版本或全局位置模型；
- 跳过已登记前驱或在同一前驱上登记多个不兼容后继；
- 让后继目录在已登记生效切点之前解释记录。

### TM-R8-15 历史目录解释必须不可变

每个时间记录保存其登记时目录聚合解析和类型资格。目录后继不能回填或覆盖该引用。

```text
record position before successor cut
  -> predecessor catalog only

record position at or after successor cut
  -> exact pinned catalog resolution
```

历史账本边界继续固定成员原目录谱系；当前扩展边界可以跨多个目录，但必须保存精确目录解析集合和每个成员的归属证明。

## 四、记录类型资格与时间账本登记

### TM-R8-16 记录类型资格必须拥有稳定键

```text
Temporal Record-type Eligibility Key =
  Registered Temporal Record-type Catalog Aggregate Registration Resolution ID and Digest
+ Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Temporal Record Type
+ Canonical Record Payload Discriminator Digest
+ Record Position Candidate or Allocated Position Reference
+ Record-type Eligibility Rule Version
```

记录业务语义结果、证明结果、登记时间、执行者和所偏好目录版本不得进入键。

### TM-R8-17 类型资格结果必须封闭

```text
PERMITTED
NOT_PERMITTED
INDETERMINATE
CONFLICTED
```

- 外层和内层目录均 `REGISTERED`、类型唯一映射到请求账本类型、位置位于目录有效范围且判别载荷一致时支持 `PERMITTED`；
- 完整目录不含该类型或映射到另一账本类型时支持 `NOT_PERMITTED`；
- 目录、切点、位置、读取或完整性未知时支持 `INDETERMINATE`；
- 同键异映射、同类型多账本、位置范围重叠冲突或同键异结果支持 `CONFLICTED`。

非 `PERMITTED` 结果不能取得位置或形成确定记录登记。

### TM-R8-18 位置分配和记录登记必须原子固定目录资格

R5 的全局位置分配载荷和每个时间记录登记载荷新增：

```text
Registered Temporal Record-type Catalog Aggregate Registration Resolution ID and Digest
Temporal Record-type Eligibility Key and Payload Digest
Record-type Eligibility Result = PERMITTED
Catalog Effective-cut Vector Resolution ID and Digest
```

位置分配、记录 ID、规范载荷摘要、记录类型、账本类型、目录资格和登记尝试必须原子内容同一。失败登记继续留下永久空洞。

`Temporal Derived Record Position Key` 保持：

```text
Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

目录、记录类型和资格摘要不得进入位置键，也不能创建类型分区。

### TM-R8-19 R6 证明记录登记键必须固定目录资格

以下三种 R6 登记解析：

```text
REQUIRED_DIMENSION_MAPPING_PROOF_QUALIFICATION
REQUIRED_DIMENSION_MAPPING_PROOF_BOUNDARY
REQUIRED_DIMENSION_MAPPING_PROOF_AGGREGATE
```

除既有映射账本边界、类型投影和完整性字段外，必须新增精确已登记目录聚合解析、`PERMITTED` 类型资格和生效切点解析。只引用投影摘要不能替代目录资格。

### TM-R8-20 R7 声明级证明记录登记键必须固定目录资格

以下三种 R7 登记解析：

```text
MAPPING_CLAIM_PROOF_QUALIFICATION
MAPPING_CLAIM_PROOF_BOUNDARY
MAPPING_CLAIM_PROOF_AGGREGATE
```

同样必须固定精确已登记目录聚合解析、`PERMITTED` 类型资格和生效切点解析。目录资格变化必须形成新的登记解析身份；同键异目录谱系必须 `CONFLICTED`。

### TM-R8-21 T 范围覆盖仍是非账本子对象

R7 的：

```text
T-scoped Mapping Aggregate Coverage
Mapping Aggregate Temporal Eligibility
```

继续作为 `Candidate Completeness Requirement Evaluation` 的不可变子对象，不是 `Temporal Mapping Ledger` 独立记录，因此不分配新的 `Temporal Record Type`。

若未来把它们提升为独立时间记录，必须经过新的已登记目录后继，不能以本修订默示授权。

## 五、账本边界、完整性和 T 的目录谱系

### TM-R8-22 每个时间账本边界必须固定精确目录集合

R5 的全局账本边界和后续更正、迁移、映射账本边界新增：

```text
Exact Registered Temporal Record-type Catalog Aggregate Resolution Set Digest
Exact Member Record-to-catalog Resolution Mapping Digest
Exact Member Record-type Eligibility Resolution Set Digest
Required Catalog-lineage Completeness Resolution IDs and Digests
```

边界可以跨目录生效切点，但每个成员只能绑定其位置适用的唯一目录。目录集合遗漏、成员归属未知或同位置适用多个不兼容目录必须 `INDETERMINATE` 或 `CONFLICTED`。

### TM-R8-23 账本完整性必须覆盖目录子域

时间账本完整性评价新增：

```text
CATALOG_CARRIER_INTEGRITY
CATALOG_EFFECTIVE_CUT_COMPLETENESS
RECORD_TO_CATALOG_MEMBERSHIP_COMPLETENESS
RECORD_TYPE_MAPPING_CONFLICT_SUBDOMAIN_COMPLETENESS
```

账本边界摘要、连续位置、零新记录或目录合同存在不能自证以上维度完整。目录权威、记录登记权威和账本完整性权威必须分离。

### TM-R8-24 T 通过映射账本边界固定目录谱系

`Temporal Governance Boundary Vector T` 继续固定已登记映射账本边界及其完整性解析。该边界现已内容同一携带精确目录解析集合，因此 `T` 不新增反向目录选择权。

```text
Registered Mapping Ledger Boundary
  -> exact catalog lineage
  -> T
  -> T-scoped coverage
  -> K
```

目录后继、类型资格或成员归属变化必须产生新的映射账本边界及后续 `T/K` 身份；不能覆盖历史 `T`。

### TM-R8-25 跨目录边界不得重算旧位置身份

目录演进只改变新记录登记资格和边界解释谱系，不改变任何既有：

```text
Temporal Ledger ID and Version
Temporal Ledger Type
Append Epoch
Position Value
Record ID and Canonical Payload Digest
```

旧记录在新边界中被重新读取时仍使用原目录和类型资格。用后继目录重新分类旧记录必须 `CONFLICTED`。

## 六、阶段、权威和失败关闭

### TM-R8-26 阶段必须保持无环

```text
G0 Allocated Temporal Governance Registry and Contract Boundary
G1 Registered Catalog Effective-cut Vector
G2 Registered Record-type Catalog Contract / Boundary / Aggregate
M0 Mapping and Proof Record Position / Registration
M1 Registered Complete Mapping Ledger Boundary with Catalog Lineage
M2 Temporal Governance Boundary Vector T
M3 T-scoped Coverage and Temporal Eligibility Subobjects
M4 Completeness Evaluation and Knowledge Boundary K
```

`G1/G2` 不写入时间账本；目录候选只消费已登记 `G1` 切点，`M0` 以后对象不得反向改变目录合同、目录切点、位置键或前驱目录。

### TM-R8-27 新增角色必须逐操作分权

目录合同定义、治理合同登记、目录边界、目录完整性、目录聚合、切点构造、切点登记、类型资格、位置分配、记录登记、账本边界和账本完整性权威不得互相传播。

目录把类型映射到 `MAPPING` 不授予创建映射候选、证明、边界、聚合、`T` 或 `K` 的权威。

### TM-R8-28 非法状态必须失败关闭

- 目录合同写入其所解释的时间账本；
- 未登记目录或非 `PERMITTED` 类型取得位置；
- R6/R7 证明记录只凭类型投影摘要登记；
- 后继目录删除或重映射前驱类型；
- 同一类型映射到多个账本类型；
- 新目录重解释生效切点前的旧位置；
- 目录类型创建独立位置域、分区或追加纪元；
- 账本边界遗漏成员目录归属或目录冲突子域；
- `T` 或覆盖子对象自行选择目录；
- 覆盖子对象被默认为独立账本记录；
- 候选、自检或文件存在替代目录登记和完整性。

以上状态必须拒绝、`NOT_PERMITTED`、`NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED`。

### TM-R8-29 已通过主干和候选闭合边界

```text
Global Temporal Position Model: PRESERVED
Correction / Migration Record Mapping: PRESERVED
Mapping Candidate / Boundary / Aggregate Identity: PRESERVED
Governed Mapping Proof: PRESERVED
Claim-level Adverse Proof Aggregation: PRESERVED
T-scoped Aggregate Coverage: PRESERVED
Temporal Governance Boundary Vector T: PRESERVED
Knowledge Boundary K: PRESERVED
Cross-interface Acyclicity: PRESERVED
```

```text
TM-R7-B1 Temporal Mapping Record Type Catalog Evolution: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R8 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R7-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Coordinate Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R9` 执行交叉接口回归审查。R8 的候选级闭合声明不能独立证明阻断关闭。
