# 来源注册表接口有界修订 R11

## 修订信息

```text
Proposal ID: CR-0005-R11
Title: Minimal Lifecycle Catalog and Reference Lineage-root Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R10 LIFECYCLE CATALOG SUCCESSOR-SLOT CLOSURE
Repair Basis: CR-0005-R10-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R10-B1 only
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
Compatibility Reference: CR-0006-R10
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R10-B1`：删除 R10 新引入但没有登记拓扑的目录／引用治理根字段，以既有已登记注册表分配解析和唯一前驱直接构成最小谱系根。它不新增治理根对象，不修改目录—锚点联合选择或查询后视图评价，不覆盖基础稿或 R1 至 R10 的历史正文，不创建注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订边界

### SR-R11-01 R11 只覆盖一个有界阻断

```text
SR-R10-B1 Catalog and Reference Lineage Governance-root Registration
```

R10 已通过的同前驱统一竞争、目录—锚点联合选择、引用世代对齐、类型资格和历史重放继续有效。

### SR-R11-02 R11 选择删除未登记治理根

以下 R10 字段不再是候选、登记或消费资格字段：

```text
Registered Catalog Lineage Governance Root ID and Digest
Registered Reference Lineage Governance Root ID and Digest
Catalog Successor-slot Semantic Rule ID
Reference Successor-slot Semantic Rule ID
Catalog Successor Aggregate Semantic Rule ID fixed by Governance Root
```

它们不得保留为兼容别名、验证包字段或可选分域字段。历史 R10 正文保留，但以上字段在 R11 复合模型中不具有候选资格。

## 二、目录最小谱系根

### SR-R11-03 目录谱系根只由已登记分配事实确定

R9 的目录谱系根由本规则进一步收紧为：

```text
Canonical Lifecycle Catalog Lineage Key =
  Registered Source Registry ID Allocation Resolution ID and Digest
+ Allocated Lifecycle Resolution Registry ID and Version
+ Registry Domain = LIFECYCLE_RESOLUTION
```

`Catalog Lineage Rule Version` 从谱系根删除。目录规则版本、规则合同、类型映射、锚点、合同 ID、登记时间和执行者只能进入后继候选载荷。

同一已分配生命周期注册表永久只有一个规范目录谱系键。

### SR-R11-04 目录后继槽只固定规范谱系和前驱

R10 `SR-R10-03` 由本规则覆盖为：

```text
Lifecycle Catalog Successor-slot Semantic Conflict Set Key =
  Canonical Lifecycle Catalog Lineage Key
+ Registered Predecessor Catalog Successor Aggregate Registration Resolution ID and Digest
    or CANONICAL_CATALOG_GENESIS_MARKER
```

该键没有治理根 ID、规则 ID、生效锚点、映射摘要、合同版本或候选字段。同一谱系和前驱只能计算出一个后继槽键。

### SR-R11-05 规则合同差异必须作为候选共同竞争

R10 后继候选载荷继续固定：

```text
Registered Base Source Registry Contract Registration Resolution
Registered Catalog Evolution Rule Contract Registration Resolution
Exact Role-to-type Mapping Set
Exact Permitted Type Set
Candidate Effective-boundary Anchor
Append-only Evolution Proof
Candidate Result
```

不同演进规则合同、版本或载荷形成同一后继槽中的不同候选。规则合同不能改变后继槽键，合同解析未知或冲突时候选不得 `QUALIFIED_SUCCESSOR`。

### SR-R11-06 初始目录也不得按规则版本分根

`GENESIS` 后继槽固定：

```text
Canonical Lifecycle Catalog Lineage Key
+ CANONICAL_CATALOG_GENESIS_MARKER
```

不同初始规则合同、映射或生效锚点全部共同竞争。不存在第二个初始目录谱系根。

## 三、最小边界和聚合身份

### SR-R11-07 后继竞争边界不能用规则版本隔离

R10 的后继边界键由本规则收紧为：

```text
Lifecycle Catalog Successor Competing Boundary Semantic Key =
  Lifecycle Catalog Successor-slot Semantic Conflict Set Key
+ Registered Source Contract Registry Boundary ID and Digest
+ Exact Successor Candidate Registration Resolution Set Digest
+ Exact Candidate Effective-anchor Set Digest
+ Required Successor Conflict-subdomain Completeness Resolution IDs and Digests
```

`Boundary Rule Version` 只进入边界候选载荷。相同语义键异边界规则、异成员集合或异结果必须在边界登记解析中 `CONFLICTED`，不能形成平行边界。

### SR-R11-08 唯一后继聚合不再固定裸治理根或规则 ID

R10 的唯一聚合键由本规则覆盖为：

```text
Lifecycle Catalog Unique Successor Aggregate Resolution Key =
  Lifecycle Catalog Successor-slot Semantic Conflict Set Key
+ Registered Successor Boundary Registration Resolution ID and Digest
+ Required Successor-boundary Completeness Resolution IDs and Digests
```

聚合算法由本修订的封闭四值规则和已登记候选规则合同集合共同约束。规则合同集合不唯一或产生不兼容结果时必须 `CONFLICTED`。

聚合结果和外层登记链继续使用 R10 的 `SELECTED | NOT_SELECTED | INDETERMINATE | CONFLICTED` 及四值登记解析。

### SR-R11-09 只有唯一外层登记后继可被消费

```text
Registered Successor Boundary
+ Complete Candidate / Rule-contract Domain
  -> Unique Successor Aggregate
  -> Aggregate Registration Resolution
```

只有外层 `REGISTERED` 且内层 `SELECTED` 的解析可以作为 `Registered Selected Lifecycle Catalog Successor Resolution`。

任何裸规则 ID、治理根 ID、目录合同版本或候选锚点都不能替代该解析。

## 四、引用最小谱系根

### SR-R11-10 引用谱系根只继承已登记分配和角色

R6 的引用语义根由本规则收紧为：

```text
Canonical Lifecycle Registry Reference Lineage Key =
  Registered Source Registry ID Allocation Resolution ID and Digest
+ Allocated Lifecycle Resolution Registry ID and Version
+ Lifecycle Registry Role = LIFECYCLE_RESOLUTION_REGISTRY
```

`Registry Reference Semantic Rule Version`、合同、类型集合、引用 ID、登记时间和执行者不进入引用谱系根。

### SR-R11-11 引用后继槽只固定规范根、前驱和所选目录后继

R10 `SR-R10-13` 由本规则覆盖为：

```text
Lifecycle Registry Reference Successor-slot Semantic Conflict Set Key =
  Canonical Lifecycle Registry Reference Lineage Key
+ Registered Predecessor Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
    or CANONICAL_REFERENCE_GENESIS_MARKER
+ Registered Selected Lifecycle Catalog Successor Resolution ID and Digest
```

引用治理根 ID、规则 ID和所选锚点不再独立进入键。锚点只从已选择目录后继载荷内容同一取得。

### SR-R11-12 引用规则和合同变化必须共同竞争

引用候选载荷继续固定基础合同、所选目录映射、所选锚点、注册表作用域和生命周期规则合同。

不同规则合同、合同版本或引用载荷形成同一引用后继槽内的候选。R6 的候选登记、完整竞争边界、聚合和外层登记链继续适用，但所有裸规则版本仅是载荷字段，不能分割引用谱系或后继槽。

### SR-R11-13 目录和引用后继必须内容同一

引用后继只有在以下字段与所选目录后继完全一致时才可 `REGISTERED`：

```text
Lifecycle Registry ID, Version, Domain and Scope
Exact Permitted Lifecycle Record Type Set Digest
Selected Effective-boundary Anchor
Predecessor / Successor Lineage
```

目录后继非唯一、引用候选遗漏某个规则合同或同键异载荷时必须 `INDETERMINATE` 或 `CONFLICTED`。

## 五、下游、阶段和失败关闭

### SR-R11-14 类型资格和视图记录只能固定最小谱系解析

类型资格、位置分配、视图候选／边界／聚合登记及生命周期边界必须固定：

```text
Canonical Lifecycle Catalog Lineage Key
Registered Selected Lifecycle Catalog Successor Resolution
Canonical Lifecycle Registry Reference Lineage Key
Registered Lifecycle Registry Reference Successor Resolution
```

R10 已废止治理根字段不得出现在验证包、身份键或可选兼容字段中。

### SR-R11-15 查询后评价和查询坐标保持不变

目录／引用最小根只治理生命周期记录资格，不进入：

```text
B
T
K
Temporal Query Coordinate Key
Post-query View Evaluation Target Boundary
```

R9/R10 的查询后视图评价、前驱评价锚点和历史／当前分离继续有效。

### SR-R11-16 阶段必须保持无环

```text
L0 Registered Registry ID Allocation and Base Contract
L1 Canonical Catalog / Reference Lineage Keys
L2 Catalog Successor Candidates / Boundary / Aggregate
L3 Selected Catalog Successor and Reference Successor
L4 View Records and Post-query Evaluation
L5 Boundary-context Eligibility and Source Applicability
```

规范谱系键只由 `L0` 已登记事实计算，不需要新增登记对象。`L2` 以后对象不得反向改变 `L0/L1`。

### SR-R11-17 权威不得传播

计算规范谱系键不授予目录候选、合同登记、边界、完整性、聚合、引用、记录写入或视图评价权威。

来源契约登记、目录聚合、引用聚合和生命周期记录登记权威继续逐操作分离。

### SR-R11-18 非法状态必须失败关闭

- 使用 R10 已废止治理根或规则 ID 分割后继槽；
- `Catalog Lineage Rule Version` 或引用规则版本进入规范谱系根；
- 相同分配解析产生多个目录或引用谱系键；
- 不同规则合同版本不共同竞争；
- 边界规则版本形成平行边界；
- 聚合键固定裸治理根、规则 ID 或候选合同；
- 引用锚点与所选目录后继载荷不等；
- 下游继续消费已废止治理根字段；
- 谱系键计算取得任何登记或写入权威；
- 候选、自检或文件存在替代完整竞争与登记解析。

以上状态必须拒绝、`NOT_SELECTED`、`NOT_REGISTERED`、`NOT_PERMITTED`、`INDETERMINATE` 或 `CONFLICTED`。

### SR-R11-19 已通过主干不得回归

```text
Catalog Mapping + Anchor Joint Selection: PRESERVED
Reference Successor Alignment: PRESERVED
Record-type Eligibility: PRESERVED
Post-query View Evaluation: PRESERVED
Temporal Query Coordinate Identity: PRESERVED
Historical / Current Separation: PRESERVED
Authority Non-propagation: PRESERVED
```

### SR-R11-20 R11 只声明一个阻断候选闭合

```text
SR-R10-B1 Catalog and Reference Lineage Governance-root Registration: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R11 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R10-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R10` 执行联合交叉接口回归。R11 自检不能独立证明阻断关闭。
