# 来源注册表接口有界修订 R10

## 修订信息

```text
Proposal ID: CR-0005-R10
Title: Lifecycle Catalog Successor-slot Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R9 LIFECYCLE RECORD-TYPE CATALOG AND POST-QUERY BOUNDARY-TRANSITION CLOSURE
Repair Basis: CR-0005-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R9-B1 only
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
Compatibility Reference: CR-0006-R9
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R9-B1`：把同一前驱目录的所有候选内容和生效锚点放入同一个后继竞争槽，并让目录聚合一次性选择内容与锚点。它不修改 R9 的查询后视图评价模型，不改变查询坐标身份，不覆盖基础稿或 R1 至 R9 的历史正文，不创建注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订边界

### SR-R10-01 R10 只覆盖一个有界阻断

```text
SR-R9-B1 Lifecycle Catalog Successor-slot Identity
```

R9 已通过的精确记录角色映射、目录外部登记、类型资格、引用世代、查询后视图评价和历史／当前分离继续有效。

### SR-R10-02 后继槽不得由候选字段分域

```text
Catalog Effective Anchor
Catalog ID or Version
Exact Permitted Type-set Digest
Role-to-type Mapping Digest
Candidate Contract ID or Version
Registration Time
Writer or Authority Holder
```

以上字段不得进入目录后继槽语义键，也不能授予候选自行选择竞争边界的能力。

## 二、唯一目录后继槽

### SR-R10-03 目录后继槽只固定谱系根和前驱

R9 `SR-R9-04` 的目录演进语义键由本规则覆盖为：

```text
Lifecycle Record-type Catalog Successor-slot Semantic Conflict Set Key =
  Lifecycle Record-type Catalog Lineage Root Key
+ Registered Predecessor Catalog Aggregate Registration Resolution ID and Digest
    or CANONICAL_CATALOG_GENESIS_MARKER
+ Registered Catalog Lineage Governance Root ID and Digest
+ Catalog Successor-slot Semantic Rule ID
```

治理根必须是目录谱系创建时固定的不可变语义根，不是某个候选合同版本。`Catalog Successor-slot Semantic Rule ID` 是该治理根载荷的固定成员，不能由候选提供或换 ID 分域。演进规则合同版本、规则载荷和登记解析只进入候选载荷并在同槽竞争。

同一目录谱系根和同一前驱只能产生一个后继槽。后继槽键禁止包含生效锚点、候选映射或目录版本。

### SR-R10-04 初始目录也必须使用唯一后继槽

初始目录使用：

```text
Predecessor = CANONICAL_CATALOG_GENESIS_MARKER
```

同一谱系根只能有一个 `GENESIS` 后继槽。不同初始映射、不同初始生效锚点或不同合同候选必须共同竞争，不能各自形成初始目录。

### SR-R10-05 后继候选载荷必须同时固定内容与锚点

```text
Lifecycle Catalog Successor Candidate Payload =
  Lifecycle Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Registered Base Source Registry Contract Registration Resolution ID and Digest
+ Candidate Catalog Contract ID and Version
+ Registered Catalog Evolution Rule Contract Registration Resolution ID and Digest
+ Exact Lifecycle Record Role-to-type Mapping Set
+ Exact Permitted Lifecycle Record Type Set Digest
+ Predecessor Mapping Set Digest or CANONICAL_GENESIS_MAPPING_DIGEST
+ Append-only Mapping Evolution Proof Digest
+ Candidate Effective-boundary Anchor ID and Digest
+ Candidate Effective-boundary Payload Digest
+ Required Anchor-boundary Completeness Resolution IDs and Digests
+ Candidate Catalog Result
+ Candidate Canonicalization Rule Version
```

候选结果只允许：

```text
QUALIFIED_SUCCESSOR
NOT_QUALIFIED_SUCCESSOR
INDETERMINATE
CONFLICTED
```

目录内容和生效锚点是同一个不可分割候选载荷。不能先选择目录内容、再由调用方选择锚点。

### SR-R10-06 后继候选必须拥有稳定键

```text
Lifecycle Catalog Successor Candidate Key =
  Lifecycle Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Candidate Successor Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。相同前驱下锚点、类型映射、合同载荷或演进证明任一变化都产生新候选，但仍进入同一个后继槽。

### SR-R10-07 后继候选继续在来源契约注册表登记

```text
Candidate Lifecycle Catalog Successor Contract
  -> Source Contract Registration Attempt
  -> Registered Source Contract Record
  -> Source Registry Contract Registration Resolution
```

合同类型继续为 `LIFECYCLE_RECORD_TYPE_CATALOG`。候选和登记载荷必须内容同一；合同登记解析非 `REGISTERED` 时，候选不能成为确定后继。

目录合同、后继竞争边界和聚合记录仍位于来源契约治理注册表，不进入生命周期解析注册表。

## 三、完整竞争和唯一后继聚合

### SR-R10-08 后继竞争边界必须覆盖全部候选锚点

```text
Lifecycle Catalog Successor Competing Boundary Key =
  Lifecycle Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Registered Source Contract Registry Boundary ID and Digest
+ Exact Successor Candidate Registration Resolution Set Digest
+ Exact Candidate Effective-anchor Set Digest
+ Required Successor Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖同一前驱下所有目录合同、类型映射、生效锚点、演进规则载荷、候选、登记尝试、永久空洞和冲突谱系。

目录版本、锚点位置、登记时间、候选结果或写入者不能过滤边界成员。构造候选或登记合同的权威不能评价边界完整性。

### SR-R10-09 后继边界必须形成四值登记解析

```text
Candidate Successor Competing Boundary
  -> Boundary Registration Attempt
  -> Registered Successor Competing Boundary Record
  -> Successor Boundary Registration Resolution
```

边界登记结果为：

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

同边界键异候选集合、异锚点集合、遗漏永久空洞或异完整性谱系必须 `CONFLICTED`。

### SR-R10-10 唯一后继聚合必须同时选择目录和锚点

```text
Lifecycle Catalog Unique Successor Aggregate Resolution Key =
  Lifecycle Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Registered Successor Boundary Registration Resolution ID and Digest
+ Required Successor-boundary Completeness Resolution IDs and Digests
+ Registered Catalog Lineage Governance Root ID and Digest
+ Catalog Successor Aggregate Semantic Rule ID fixed by Governance Root
```

结果为：

```text
SELECTED
NOT_SELECTED
INDETERMINATE
CONFLICTED
```

- 唯一 `QUALIFIED_SUCCESSOR` 或多个内容同一候选支持 `SELECTED`；
- 完整空集或全部确定不合格支持 `NOT_SELECTED`；
- 边界、候选、锚点或完整性未知支持 `INDETERMINATE`；
- 多个不兼容合格后继、同映射异锚点、同锚点异映射或同键异结果支持 `CONFLICTED`。

`SELECTED` 载荷必须同时保存所选目录映射和所选生效锚点。

### SR-R10-11 后继聚合必须形成外层登记解析

```text
Registered Complete Successor Competing Boundary
  -> Candidate Unique Successor Aggregate Resolution
  -> Successor Aggregate Registration Attempt
  -> Registered Successor Aggregate Record
  -> Successor Aggregate Registration Resolution
```

外层结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。只有外层 `REGISTERED` 且内层 `SELECTED` 的内容同一载荷才是：

```text
Registered Selected Lifecycle Catalog Successor Resolution
```

类型资格、引用世代和记录登记只能消费该解析，不能直接消费某个候选目录合同。

### SR-R10-12 后续演进必须使用已选择后继作为新前驱

目录 `C1` 从 `C0` 的后继槽被选择后，下一次演进必须形成：

```text
Predecessor = Registered Selected Catalog Successor Resolution(C1)
```

禁止继续以 `C0` 为前驱、仅换一个较晚锚点登记所谓第二后继。该状态属于同一旧后继槽的遗漏候选或平行分叉，必须 `CONFLICTED`。

## 四、注册表引用世代与类型资格对齐

### SR-R10-13 引用世代键只能固定唯一后继解析

R9 `SR-R9-13` 的引用世代键由本规则收紧为：

```text
Lifecycle Registry Reference Successor-slot Semantic Conflict Set Key =
  Lifecycle Resolution Registry Reference Semantic Conflict Set Key
+ Registered Predecessor Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
    or CANONICAL_REFERENCE_GENESIS_MARKER
+ Registered Selected Lifecycle Catalog Successor Resolution ID and Digest
+ Registered Reference Lineage Governance Root ID and Digest
+ Reference Successor-slot Semantic Rule ID
```

所选生效锚点已包含在唯一目录后继解析载荷中，不再作为引用世代语义键的独立字段。`Reference Successor-slot Semantic Rule ID` 同样由不可变引用治理根固定，不能由引用候选选择。

目录后继解析不是外层 `REGISTERED + SELECTED` 时，不得构造确定引用世代。

### SR-R10-14 引用世代候选载荷必须验证目录内容同一

```text
Lifecycle Registry Reference Successor Candidate Payload =
  Lifecycle Registry Reference Successor-slot Semantic Conflict Set Key
+ Registered Base Source Registry Contract Registration Resolution ID and Digest
+ Selected Catalog Mapping Set Digest
+ Selected Catalog Effective-boundary Anchor ID and Digest
+ Contract-bound Registry ID, Version, Domain and Scope
+ Lifecycle Resolution Rule Contract Payload Digest
+ Candidate Reference Result
+ Candidate Canonicalization Rule Version
```

目录映射、锚点、注册表作用域或规则载荷不等形成同引用后继槽内的竞争候选，不能用引用版本隔离。

### SR-R10-15 引用后继竞争必须完整且冲突优先

R6 的引用候选登记、竞争边界和聚合链继续适用，但语义根替换为精确引用后继槽。

完整边界覆盖同一前驱引用和唯一目录后继下的全部引用候选。唯一内容同一候选可支持 `REGISTERED`；多个不兼容引用载荷必须 `CONFLICTED`。

旧引用继续解释旧边界；新引用只授权所选目录生效锚点之后的记录。引用后继不得重写前驱载荷。

### SR-R10-16 类型资格必须固定所选后继及其锚点

R9 的 `Lifecycle Record-type Eligibility Key` 由本规则新增：

```text
Registered Selected Lifecycle Catalog Successor Resolution ID and Digest
Selected Effective-boundary Anchor ID and Digest
Canonical Lifecycle Record Position Subject Key and Digest
```

记录位置、所选目录锚点和角色到类型映射必须内容同一。直接固定候选目录、未选择锚点或平行后继不能产生 `PERMITTED`。

### SR-R10-17 视图记录必须消费同一引用和目录后继

视图候选、竞争边界和聚合记录登记共同固定：

```text
Registered Lifecycle Registry Reference Successor Aggregate Resolution
Registered Selected Lifecycle Catalog Successor Resolution
Selected Effective-boundary Anchor
Record-type Eligibility Result = PERMITTED
```

四项谱系任一不等、未知或冲突时不得形成确定登记。生命周期注册表边界及完整性解析必须保存成员到所选目录后继的精确映射。

## 五、查询后评价、历史和阶段

### SR-R10-18 查询后视图评价模型保持不变

R9 的：

```text
HISTORICAL
CURRENT_BOOTSTRAP
CURRENT_SUCCESSOR
```

锚点联合类型、前驱评价解析、同前驱目标边界竞争和查询主体内容同一继续有效。

目录后继槽只治理记录类型合同演进，不创建时间查询坐标，也不替代视图评价的生命周期边界转换证明。

### SR-R10-19 历史目录和引用世代必须可重放

```text
Historical record before selected successor anchor
  -> predecessor catalog and predecessor reference

Record at or after selected successor anchor
  -> exact selected successor catalog and successor reference
```

跨锚点生命周期边界必须固定精确目录后继集合及成员归属。新后继不能重解释、回填或覆盖历史记录。

### SR-R10-20 目录与视图阶段必须无环

```text
L0 Allocated Lifecycle Registry and Base Source Contract
L1 Registered Complete Predecessor Lifecycle Boundary
L2 Catalog Successor Candidates under One Predecessor Slot
L3 Registered Selected Catalog Successor and Reference Successor
L4 View Evaluation Candidate / Boundary / Aggregate Records
L5 Boundary-context Eligibility
L6 Source Applicability Aggregate
```

`L2/L3` 不读取 `L4` 结果；`L4` 至 `L6` 不得反向改变目录后继、引用后继、生命周期边界、`B/T/K` 或查询坐标。

### SR-R10-21 新增权威必须逐操作分离

后继槽定义、目录候选、合同登记、边界、完整性、唯一后继聚合、引用后继、类型资格、记录登记、视图评价和来源适用性权威不得互相传播。

目录后继被选择不授予在其生效锚点写入记录的权威。

### SR-R10-22 非法状态必须失败关闭

- 生效锚点、目录版本或映射摘要进入目录后继槽键；
- 同一前驱的不同锚点进入不同竞争边界；
- 先选择目录内容再由调用方选择生效锚点；
- 同一前驱多个不兼容后继仍选择其一；
- 已选择 `C1` 后继续从 `C0` 登记较晚平行后继；
- 引用世代直接消费目录候选而不是唯一后继解析；
- 引用世代把所选锚点再次用作分域字段；
- 非 `REGISTERED + SELECTED` 目录后继支持 `PERMITTED`；
- 新目录或引用重解释旧边界；
- 目录、视图或来源对象修改查询坐标；
- 候选、自检或文件存在替代完整竞争和登记解析。

以上状态必须拒绝、`NOT_SELECTED`、`NOT_PERMITTED`、`NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED`。

### SR-R10-23 已通过主干不得回归

```text
Lifecycle Record Role-to-type Mapping: PRESERVED
Catalog Registration outside Lifecycle Registry: PRESERVED
Registry Reference Generation: STRENGTHENED
Post-query View Evaluation Subject: PRESERVED
Temporal Query Coordinate Identity: PRESERVED
Purpose Qualification Boundary-context Eligibility: PRESERVED
Historical / Current Separation: PRESERVED
Authority Non-propagation: PRESERVED
```

### SR-R10-24 R10 只声明一个阻断候选闭合

```text
SR-R9-B1 Lifecycle Catalog Successor-slot Identity: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R10 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R9-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R9` 执行交叉接口回归审查。R10 自检不能独立证明阻断关闭。
