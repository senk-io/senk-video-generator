# 来源注册表接口有界修订 R9

## 修订信息

```text
Proposal ID: CR-0005-R9
Title: Lifecycle Record-type Catalog and Post-query Boundary-transition Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R8 LIFECYCLE BOUNDARY CONTEXT ELIGIBILITY CLOSURE
Repair Basis: CR-0005-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Basis: CR-0005-R8-CR-0006-R7-CROSS-INTERFACE-REGRESSION-REVIEW
Repair Scope: SR-R8-B1 + XREG-B1 only
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
Compatibility Reference: CR-0006-R8
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R8-B1` 与 `XREG-B1`：为生命周期记录类型建立受治理、可演进且历史可重放的合同目录，并把生命周期边界推进改为查询坐标之后的视图评价转换。它不修改时间查询坐标身份，不覆盖基础稿或 R1 至 R8 的历史正文，不创建注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订边界

### SR-R9-01 R9 只覆盖两个有界阻断

```text
SR-R8-B1 Lifecycle View-context Record Type Contract Eligibility
XREG-B1 Lifecycle Boundary Expansion Cannot Mint New Query Subject
```

R8 已通过的边界上下文全域资格、空／非空目的消费、历史边界固定和来源适用性身份方向继续有效。

### SR-R9-02 类型目录和视图转换不得自授权

```text
Lifecycle Record-type Catalog
  -/-> allocate its own registry ID
  -/-> register its own source registry contract
  -/-> prove its own catalog boundary completeness

Lifecycle View Evaluation
  -/-> create or modify B, T, K
  -/-> create a Temporal Query Coordinate
  -/-> change its selected lifecycle boundary
  -/-> select latest registration time or position
```

目录合同只复用 R4 的来源注册表合同登记根。视图评价只消费已登记查询主体和生命周期边界，不取得其构造、登记或完整性权威。

## 二、生命周期记录类型目录合同

### SR-R9-03 类型目录必须拥有稳定谱系根

```text
Lifecycle Record-type Catalog Lineage Root Key =
  Registered Source Registry ID Allocation Resolution ID and Digest
+ Allocated Lifecycle Resolution Registry ID and Version
+ Registry Domain = LIFECYCLE_RESOLUTION
+ Catalog Lineage Rule Version
```

目录 ID、目录版本、候选载荷摘要、登记时间、执行者和允许类型集合不得进入谱系根。它们不能用来隔离同一注册表的目录冲突。

### SR-R9-04 每次目录演进必须固定前驱和生效锚点

```text
Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key =
  Lifecycle Record-type Catalog Lineage Root Key
+ Registered Predecessor Catalog Aggregate Registration Resolution ID and Digest
    or CANONICAL_CATALOG_GENESIS_MARKER
+ Registered Catalog Effective-boundary Anchor ID and Digest
+ Catalog Evolution Semantic Rule Version
```

同一前驱和生效锚点的全部候选目录必须进入同一语义冲突集合。目录版本、合同版本、写入者或登记时间不能分割竞争域。

初始目录只允许使用规范 `GENESIS` 标记；非初始目录必须固定外层 `REGISTERED` 且内层 `REGISTERED` 的唯一前驱目录聚合解析。

### SR-R9-05 R9 目录载荷必须明确记录角色映射

```text
Lifecycle Record-type Catalog Candidate Payload =
  Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key
+ Registered Base Source Registry Contract Registration Resolution ID and Digest
+ Contract-bound Lifecycle Registry ID, Version, Domain and Scope Digest
+ Exact Lifecycle Record Role-to-type Mapping Set
+ Exact Permitted Lifecycle Record Type Set Digest
+ Predecessor Mapping Set Digest or CANONICAL_GENESIS_MAPPING_DIGEST
+ Append-only Evolution Proof Digest
+ Catalog Effective-boundary Payload
+ Catalog Canonicalization Rule Version
```

R6 的既有六类记录继续有效。R8 的视图记录角色由本规则明确收紧为：

```text
VIEW_CONTEXT_CANDIDATE_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_CANDIDATE

VIEW_CONTEXT_COMPETING_BOUNDARY_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_COMPETING_BOUNDARY

VIEW_CONTEXT_AGGREGATE_RESOLUTION_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_AGGREGATE_RESOLUTION
```

R8 中未分角色的 `LIFECYCLE_CONSUMPTION_VIEW_CONTEXT` 只保留为记录家族标签，不再是可登记的规范记录类型。

R9 目标目录的精确允许集合至少包含：

```text
LIFECYCLE_REGISTRY_REFERENCE
LIFECYCLE_CANDIDATE_RESOLUTION
LIFECYCLE_COMPETING_BOUNDARY
LIFECYCLE_AGGREGATE_RESOLUTION
LIFECYCLE_REQUIRED_PURPOSE_QUALIFICATION
LIFECYCLE_CROSS_PURPOSE_RESOLUTION
LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_CANDIDATE
LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_COMPETING_BOUNDARY
LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_AGGREGATE_RESOLUTION
```

候选载荷必须保存精确全集和摘要，不能把“至少包含”当作开放世界许可。

### SR-R9-06 目录候选必须拥有稳定键

```text
Lifecycle Record-type Catalog Candidate Key =
  Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key
+ Candidate Catalog Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。同一演进语义域内不同类型映射、不同有效锚点载荷或不同前驱证明形成竞争候选，不得按目录版本选赢家。

### SR-R9-07 目录合同必须在生命周期注册表之外登记

目录候选作为 R4 `Source Registry Contract` 的 `LIFECYCLE_RECORD_TYPE_CATALOG` 合同子类型，复用已分配来源契约注册表及其登记链。候选固定的是已经登记的基础注册表合同，不是自身尚未产生的目录合同解析：

```text
Candidate Lifecycle Record-type Catalog Contract
  -> Source Contract Registration Attempt
  -> Registered Source Contract Record
  -> Source Registry Contract Registration Resolution
```

候选和登记载荷必须内容同一。目录合同记录不得写入其所治理的生命周期解析注册表，因而不要求目录先许可自身。

### SR-R9-08 目录竞争边界必须覆盖全部同域候选

```text
Lifecycle Record-type Catalog Competing Boundary Key =
  Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key
+ Registered Source Contract Registry Boundary ID and Digest
+ Exact Catalog Contract Registration Resolution Set Digest
+ Required Catalog Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖候选、合同登记尝试、登记记录、解析、永久空洞、前驱不一致和类型映射冲突谱系。目录定义者、合同登记者和目录聚合者不能评价该边界完整。

边界自身必须形成候选、登记尝试、内容同一记录和四值登记解析。

### SR-R9-09 目录聚合必须形成四值外层登记解析

```text
Lifecycle Record-type Catalog Aggregate Resolution Key =
  Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key
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

唯一内容同一且合同登记为 `REGISTERED` 的候选支持 `REGISTERED`；完整空集支持 `NOT_REGISTERED`；边界、读取、前驱或完整性未知支持 `INDETERMINATE`；同域异映射、多个不兼容后继、类型重映射或同键异结果支持 `CONFLICTED`。

```text
Registered Complete Catalog Competing Boundary
  -> Candidate Catalog Aggregate Resolution
  -> Catalog Aggregate Registration Attempt
  -> Registered Catalog Aggregate Record
  -> Catalog Aggregate Registration Resolution
```

外层结果同样为四值。目录竞争边界、聚合记录和登记解析均位于来源契约治理注册表的目录合同子域，不进入生命周期解析注册表。下游只可消费外层 `REGISTERED` 且内层 `REGISTERED` 的目录载荷。

### SR-R9-10 目录演进只能追加类型且不得重映射

非初始目录必须证明：

```text
Successor Exact Mapping Set
  = Predecessor Exact Mapping Set
  + Newly Permitted Role-to-type Mappings

Every predecessor record type
  -> same role semantics
  -> same lifecycle registry domain
```

删除旧类型、把旧角色改映射到新类型、让同一类型承担不兼容角色、改变注册表 ID／域／作用域，或跳过已登记前驱，必须 `CONFLICTED`。

### SR-R9-11 生效边界必须保持历史解释

目录有效锚点固定生命周期注册表的已登记边界、下一可用追加位置或精确后继记录集合起点，并由独立完整性证明支持。

```text
record position before successor effective anchor
  -> interpreted only by pinned predecessor catalog

record position at or after successor effective anchor
  -> may use pinned successor catalog
```

新目录不能重解释、重登记或覆盖旧边界中的记录。跨目录生命周期边界必须固定其成员实际使用的精确目录聚合解析集合摘要。

### SR-R9-12 记录类型资格必须四值化

```text
Lifecycle Record-type Eligibility Key =
  Registered Catalog Aggregate Registration Resolution ID and Digest
+ Lifecycle Registry ID and Version
+ Lifecycle Record Role
+ Lifecycle Record Type
+ Record Position Candidate or Allocated Position Reference
+ Record-type Eligibility Rule Version
```

结果为：

```text
PERMITTED
NOT_PERMITTED
INDETERMINATE
CONFLICTED
```

只有目录外层和内层均 `REGISTERED`、角色到类型唯一内容同一且记录位置位于目录有效范围时支持 `PERMITTED`。类型缺失支持 `NOT_PERMITTED`；目录或有效边界未知支持 `INDETERMINATE`；同角色多类型、同类型不兼容角色或同键异结果支持 `CONFLICTED`。

任何非 `PERMITTED` 结果都不能产生确定记录登记。

### SR-R9-13 注册表引用必须拥有可演进世代身份

R6 的 `Lifecycle Resolution Registry Reference Semantic Conflict Set Key` 继续作为不可变引用谱系根，但不再直接聚合全部历史合同世代。

```text
Lifecycle Registry Reference Generation Semantic Conflict Set Key =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Registered Predecessor Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
    or CANONICAL_REFERENCE_GENESIS_MARKER
+ Registered Lifecycle Record-type Catalog Aggregate Registration Resolution ID and Digest
+ Registered Catalog Effective-boundary Anchor ID and Digest
+ Reference Generation Semantic Rule Version
```

相同前驱引用、后继目录和生效锚点的全部引用候选共同竞争。不同后继世代保持在同一谱系根内追加，但不与合法前驱重新竞争。

目录版本、引用版本、登记时间、“最新”或执行者不能替代前驱引用解析。相同前驱存在多个不兼容后继目录或引用载荷时必须 `CONFLICTED`。

### SR-R9-14 引用载荷必须固定已登记目录而非裸集合

R6 的引用候选载荷由本规则收紧：

```text
Lifecycle Registry Reference Generation Candidate Payload =
  Lifecycle Registry Reference Generation Semantic Conflict Set Key
+ Registered Base Source Registry Contract Registration Resolution ID and Digest
+ Registered Lifecycle Record-type Catalog Aggregate Registration Resolution ID and Digest
+ Exact Permitted Lifecycle Record Type Set Digest from Registered Catalog
+ Catalog Effective-boundary Anchor ID and Digest
+ Contract-bound Registry ID, Version, Domain and Scope
+ Lifecycle Resolution Rule Contract Payload Digest
+ Candidate Canonicalization Rule Version
```

裸 `Exact Permitted Lifecycle Record Type Set Digest` 不再能单独授权记录类型。载荷中的集合摘要必须与已登记目录内容同一。

R6 的候选登记、竞争边界和聚合解析继续适用，但其语义范围改为精确引用世代键。只有外层 `REGISTERED` 且内层 `REGISTERED` 的后继引用才能授权生效锚点之后的新记录；旧引用继续解释其历史边界。

```text
Predecessor Reference + Registered Successor Catalog
  -> Candidate Successor Reference Generation
  -> Complete Same-generation Competing Boundary
  -> Registered Successor Reference Aggregate Resolution
```

目录合同登记本身不依赖后继生命周期引用，因此该顺序不形成自举循环。

### SR-R9-15 所有视图记录登记必须固定目录资格

R8 的候选、竞争边界和聚合记录登记键分别新增：

```text
Registered Lifecycle Record-type Catalog Aggregate Registration Resolution ID and Digest
Exact Lifecycle Record-type Eligibility Key and Payload Digest
Record-type Eligibility Result = PERMITTED
Catalog Effective-boundary Anchor ID and Digest
```

成员记录、位置分配、记录登记、注册表边界和边界完整性解析必须内容同一固定目录解析。只保存类型字符串或投影摘要不能替代目录资格。

## 三、查询后的生命周期视图评价主体

### SR-R9-16 时间查询坐标身份保持不变

R8 的以下要求由本规则明确覆盖：

```text
Lifecycle boundary expansion
  -/-> mint a new Registered Temporal Query Coordinate Subject Reference
```

查询坐标继续只由时间侧规范合同决定。生命周期边界、目录、视图候选、转换证明、登记时间和“当前”不得进入 `Temporal Query Coordinate Key` 或规范载荷。

### SR-R9-17 视图评价锚点必须是封闭联合类型

```text
Lifecycle View Evaluation Anchor =
  HISTORICAL:
    Requested Registered Lifecycle Registry Boundary ID and Digest
    + Required Historical-boundary Completeness Resolution IDs and Digests

  CURRENT_BOOTSTRAP:
    CANONICAL_CURRENT_VIEW_BOOTSTRAP_MARKER

  CURRENT_SUCCESSOR:
    Registered Predecessor Lifecycle View Evaluation Aggregate Registration Resolution ID and Digest
    + Predecessor Selected Lifecycle Registry Boundary ID and Digest
```

三种分支互斥。当前后继不得使用裸边界、任意世代号、目录版本、登记时间或最大位置代替前驱评价解析。

### SR-R9-18 查询后视图评价必须拥有稳定语义键

```text
Post-query Lifecycle View Evaluation Semantic Conflict Set Key =
  Registered Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
+ Source Applicability Change Conflict Set Key
+ Registered Source Applicability Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Lifecycle View Mode
+ Lifecycle View Evaluation Anchor
+ Registered Lifecycle Consumption View Rule Contract Payload Digest
+ View Evaluation Semantic Rule Version
```

当前分支的候选目标生命周期边界不得进入该键。同一查询主体、变化集合、模式和前驱评价下的全部目标边界必须共同竞争。

历史分支由明确请求的历史边界形成独立评价身份，不声称当前选择。

### SR-R9-19 视图评价候选载荷必须固定目标和转换谱系

```text
Post-query Lifecycle View Evaluation Candidate Payload =
  Post-query Lifecycle View Evaluation Semantic Conflict Set Key
+ Candidate Target Lifecycle Registry Boundary ID and Digest
+ Required Target-boundary Completeness Resolution IDs and Digests
+ Exact Target Boundary Position Range or Record Set Digest
+ Registered Lifecycle Record-type Catalog Aggregate Resolution Set Digest
+ Governed Boundary-transition Evidence Boundary ID and Digest
+ Transition Evidence Completeness Resolution ID and Digest
+ Predecessor-to-target Append-only Extension Proof Digest or Historical Equality Proof Digest
+ Candidate Evaluation Result
+ Candidate Canonicalization Rule Version
```

候选结果只允许：

```text
QUALIFIED_TARGET
NOT_QUALIFIED_TARGET
INDETERMINATE
CONFLICTED
```

### SR-R9-20 当前转换必须严格消费前驱

`CURRENT_BOOTSTRAP` 只允许从无前驱的规范起点选择首个完整边界。

`CURRENT_SUCCESSOR` 必须证明：

```text
Target Boundary belongs to same lifecycle registry reference
Target Boundary is an append-only strict successor of predecessor boundary
Predecessor records and positions are preserved content-identically
No intervening registered complete successor candidate is omitted
Transition evidence boundary is independently complete
```

相同前驱下多个不兼容 `QUALIFIED_TARGET` 必须共同进入竞争并导致 `CONFLICTED`。旧边界、平行分叉、回退边界或跳过已知中间后继不能成为确定当前目标。

### SR-R9-21 历史评价只能重放明确边界

历史候选的目标边界必须与历史锚点内容同一。历史评价不要求它是当前最大边界，也不能参与当前后继选择。

```text
Historical anchor = L1 and target = L1: may qualify
Historical anchor = L1 and target = L2: CONFLICTED
Historical result -> current selection: PROHIBITED
```

### SR-R9-22 视图评价复用 R8 的三层登记链

R8 的视图上下文候选、竞争边界和聚合由本规则解释为查询后视图评价的登记实现：

```text
Post-query View Evaluation Candidate
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_CANDIDATE

Complete Same-anchor Candidate Boundary
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_COMPETING_BOUNDARY

View Evaluation Aggregate
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_AGGREGATE_RESOLUTION
```

三层记录都必须满足 `SR-R9-12` 的目录资格，不能共享未分角色的通用类型。

### SR-R9-23 候选登记必须同时固定评价身份和类型资格

R8 的候选登记解析键由本规则收紧为：

```text
Post-query View Evaluation Candidate Registration Resolution Key =
  Post-query Lifecycle View Evaluation Candidate Key
+ Registered Lifecycle Record-type Catalog Aggregate Registration Resolution ID and Digest
+ Candidate Record-type Eligibility Key and Digest
+ Registered Lifecycle View-context Record Registry Boundary ID and Digest
+ Required Record-boundary Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

候选键由评价语义键、候选载荷摘要和身份规则版本组成。目录资格非 `PERMITTED` 或评价上下文不等时不得 `REGISTERED`。

### SR-R9-24 竞争边界必须固定同锚点全集

```text
Post-query View Evaluation Competing Boundary Key =
  Post-query Lifecycle View Evaluation Semantic Conflict Set Key
+ Registered Lifecycle Resolution Registry Boundary ID and Digest
+ Exact View Evaluation Candidate Registration Resolution Set Digest
+ Registered Boundary-record Type Eligibility Key and Digest
+ Required View-evaluation Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖同锚点全部候选目标、转换证明、登记记录、永久空洞和冲突谱系。按目标边界、结果、登记时间或写入者过滤候选必须失败关闭。

### SR-R9-25 视图评价聚合必须形成注册主体解析

```text
Post-query Lifecycle View Evaluation Aggregate Resolution Key =
  Post-query Lifecycle View Evaluation Semantic Conflict Set Key
+ Registered View Evaluation Competing Boundary Registration Resolution ID and Digest
+ Required Evaluation-boundary Completeness Resolution IDs and Digests
+ Registered Lifecycle Consumption View Rule Contract Payload Digest
+ View Evaluation Aggregate Rule Version
```

内层结果为：

```text
SELECTED
NOT_SELECTED
INDETERMINATE
CONFLICTED
```

唯一 `QUALIFIED_TARGET` 或多个内容同一合格目标支持 `SELECTED`；完整无合格目标支持 `NOT_SELECTED`；边界、转换或完整性未知支持 `INDETERMINATE`；多个不兼容合格目标、同前驱分叉或同键异结果支持 `CONFLICTED`。

聚合记录登记键还必须固定聚合记录类型资格和目录有效锚点。外层结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

只有外层 `REGISTERED` 且内层 `SELECTED` 的聚合解析才是：

```text
Registered Post-query Lifecycle View Evaluation Subject Resolution
```

### SR-R9-26 R8 视图上下文语义键必须固定评价主体

R8 的 `Lifecycle Consumption View Context Semantic Conflict Set Key` 由本规则覆盖为 `Post-query Lifecycle View Evaluation Semantic Conflict Set Key`。

候选目标边界仍位于候选载荷而非当前语义键；当前演进通过前驱已登记评价解析产生新的语义身份，不通过新查询坐标或任意版本号产生。

### SR-R9-27 生命周期边界推进产生新评价而非新查询

R8 `SR-R8-20` 由本规则收紧为：

```text
same Registered Temporal Query Coordinate Subject Reference
+ new Registered Predecessor View Evaluation Resolution
+ new candidate target lifecycle boundary
  -> new Post-query Lifecycle View Evaluation identity
  -> new boundary-context eligibility
  -> new lifecycle consumption reference
  -> new source applicability aggregate identity
```

从 `L1` 推进到 `L2` 后，`L1` 聚合仍可在历史锚点下重放；当前 `L2` 必须消费以 `L1` 已登记评价解析为前驱的唯一已选择后继。查询主体保持内容同一。

## 四、消费、阶段和失败关闭

### SR-R9-28 来源适用性必须固定查询后评价解析

R8 的来源适用性变化聚合键新增并固定：

```text
Registered Post-query Lifecycle View Evaluation Subject Resolution ID and Digest
Selected Target Lifecycle Registry Boundary ID and Digest
Registered Lifecycle Record-type Catalog Aggregate Resolution Set Digest
```

其余查询主体、边界上下文资格和生命周期消费引用字段继续有效。同一逻辑键下评价主体、目标边界或目录谱系不等必须 `CONFLICTED`。

### SR-R9-29 阶段必须保持无环

```text
L0 Registered Temporal Query Coordinate Subject and Change Set Boundary
L1 Lifecycle Purpose / Per-purpose / Cross-purpose Records
L2 Registered Complete Lifecycle Registry Boundary
L3 Registered Record-type Catalog and Successor Registry Reference Generation
L4 Post-query View Evaluation Candidate / Boundary / Aggregate
L5 Boundary-context Eligibility Subobject
L6 Source Applicability Change Aggregate Resolution
```

`L3` 只治理 `L4` 记录类型，不读取 `L4` 结果。`L4` 至 `L6` 不得反向进入 `B`、`T`、`K`、查询坐标或 `L2` 身份。

### SR-R9-30 新增角色必须逐操作分权

目录合同定义、目录候选构造、来源合同登记、目录边界、目录完整性、目录聚合、类型资格、视图转换证据、视图候选、视图边界、视图聚合、边界上下文资格和来源适用性权威不得互相传播。

目录许可一种记录类型不授予记录构造、登记、边界、完整性或聚合权威。

### SR-R9-31 非法状态必须失败关闭

- 目录合同写入其所治理的生命周期解析注册表；
- 未登记目录、目录不完整或类型未允许却登记视图记录；
- 通用记录家族标签替代精确角色到类型映射；
- 后继目录删除或重映射前驱类型；
- 新目录重解释旧边界或记录位置；
- 后继目录直接改写旧引用载荷或让新旧引用世代重新竞争；
- 缺少已登记前驱引用解析却产生后继引用；
- 生命周期边界、目录或评价摘要进入时间查询坐标键；
- 当前转换缺少已登记前驱评价解析；
- 按目标边界、登记时间、“最新”或写入者过滤同锚点候选；
- 同一前驱存在多个不兼容合格后继却选择其一；
- 历史评价支持当前选择；
- 评价、资格或来源适用性反向修改被消费边界；
- 候选、自检或文件存在替代登记与完整性。

以上状态必须拒绝、`NOT_REGISTERED`、`NOT_PERMITTED`、`NOT_SELECTED`、`INDETERMINATE` 或 `CONFLICTED`。

### SR-R9-32 已通过主干和候选闭合边界

```text
Bare Marker Retirement: PRESERVED
Qualified Empty / Nonempty Consumption: PRESERVED
Lifecycle Registry Reference Identity: PRESERVED
Purpose Qualification Boundary-context Eligibility: PRESERVED
Historical / Current Boundary Separation: STRENGTHENED
Temporal Query Coordinate Identity: PRESERVED
Four-value Coordinate Subject Consumption: PRESERVED
Cross-interface Acyclicity: RESTORED_AS_DRAFT
```

```text
SR-R8-B1 Lifecycle View-context Record Type Contract Eligibility: CLOSED_AS_DRAFT
XREG-B1 Lifecycle Boundary Expansion Cannot Mint New Query Subject: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R9 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R8-B1 + XREG-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R8` 执行交叉接口回归审查。R9 的候选级闭合声明不能独立证明阻断关闭。
