# 时间映射治理有界修订 R10

## 修订信息

```text
Proposal ID: CR-0006-R10
Title: Minimal Temporal Catalog Lineage-root Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R9 TEMPORAL CATALOG SUCCESSOR-SLOT AND EFFECTIVE-CUT COMPETITION CLOSURE
Repair Basis: CR-0006-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R9-B1 only
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
Compatibility Reference: CR-0005-R11
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R9-B1`：删除 R9 新引入但没有登记拓扑的目录治理根字段，以既有已登记时间治理注册表分配解析、受治理账本作用域和唯一前驱直接构成最小目录谱系。它不新增治理根对象，不修改目录—切点联合选择、规范位置主体或十三类记录映射，不覆盖基础稿或 R1 至 R9 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订边界

### TM-R10-01 R10 只覆盖一个有界阻断

```text
TM-R9-B1 Temporal Catalog Lineage Governance-root Registration
```

R9 已通过的同前驱联合竞争、映射—切点一次性选择、规范位置内容同一、账本谱系和 `T` 继承方向继续有效。

### TM-R10-02 R10 删除未登记治理根

以下 R9 字段不再是候选、登记或消费资格字段：

```text
Registered Catalog Lineage Governance Root ID and Digest
Catalog Successor-slot Semantic Rule ID
Catalog Successor Aggregate Semantic Rule ID fixed by Governance Root
```

它们不得作为兼容别名、验证包字段或可选分域字段。历史 R9 正文保留，但这些字段在 R10 复合模型中不具有候选资格。

## 二、时间目录最小谱系根

### TM-R10-03 目录谱系根只固定已登记注册表和账本作用域

R8 的目录谱系根由本规则收紧为：

```text
Canonical Temporal Catalog Lineage Key =
  Registered Temporal Governance Registry ID Allocation Resolution ID and Digest
+ Allocated Governance Registry ID and Version
+ Governance Contract Type = TEMPORAL_RECORD_TYPE_CATALOG
+ Exact Governed Temporal Ledger ID-and-type Set Digest
```

受治理账本集合必须与既有已登记时间账本分配／合同作用域内容同一，不能由目录候选临时提供。

`Catalog Lineage Rule Version`、目录合同、映射、切点、规则版本、登记时间和执行者不进入规范谱系键。同一治理注册表和既有账本作用域永久只有一个目录谱系键。

### TM-R10-04 后继槽只固定规范谱系和前驱

R9 `TM-R9-03` 由本规则覆盖为：

```text
Temporal Catalog Successor-slot Semantic Conflict Set Key =
  Canonical Temporal Catalog Lineage Key
+ Registered Predecessor Catalog Successor Aggregate Registration Resolution ID and Digest
    or CANONICAL_R5_CATALOG_GENESIS_MARKER
```

该键不包含治理根、规则 ID、切点、类型映射、合同版本或候选摘要。同一规范谱系和前驱只能计算出一个后继槽。

### TM-R10-05 初始目录不得按规则或账本声明分根

初始 R5 目录后继槽为：

```text
Canonical Temporal Catalog Lineage Key
+ CANONICAL_R5_CATALOG_GENESIS_MARKER
```

不同初始规则合同、映射载荷或生效切点全部共同竞争。候选声称的账本集合与规范谱系作用域不等时必须 `CONFLICTED`，不能形成另一个初始根。

### TM-R10-06 规则合同变化必须作为候选共同竞争

R9 目录—切点联合候选继续固定：

```text
Registered Catalog Evolution Rule Contract Registration Resolution
Exact Temporal Record Type-to-ledger Mapping Set
Exact Per-ledger Effective Cut Set
Append-only Mapping Evolution Proof
Cut Completeness and Continuity Proofs
Candidate Result
```

不同规则合同版本或载荷形成同一后继槽中的候选。规则合同解析未知、冲突或与规范账本作用域不等时，候选不得成为 `QUALIFIED_SUCCESSOR`。

## 三、最小边界和聚合身份

### TM-R10-07 后继边界不能用规则版本分域

R9 的后继竞争边界键由本规则收紧为：

```text
Temporal Catalog Successor Competing Boundary Semantic Key =
  Temporal Catalog Successor-slot Semantic Conflict Set Key
+ Registered Temporal Governance Contract Registry Boundary ID and Digest
+ Exact Successor Candidate Registration Resolution Set Digest
+ Exact Candidate Effective-cut Set Digest
+ Exact Candidate Mapping Set Digest
+ Required Successor Conflict-subdomain Completeness Resolution IDs and Digests
```

`Boundary Rule Version` 只进入边界候选载荷。相同语义键异规则、异成员、异切点集合或异结果必须在边界登记解析中 `CONFLICTED`，不能形成平行边界。

### TM-R10-08 唯一后继聚合不再固定裸治理根或规则 ID

R9 的唯一后继聚合键由本规则覆盖为：

```text
Temporal Catalog Unique Successor Aggregate Resolution Key =
  Temporal Catalog Successor-slot Semantic Conflict Set Key
+ Registered Successor Boundary Registration Resolution ID and Digest
+ Required Successor-boundary Completeness Resolution IDs and Digests
```

聚合结果继续为：

```text
SELECTED
NOT_SELECTED
INDETERMINATE
CONFLICTED
```

聚合算法由本修订封闭规则和完整候选规则合同集合共同约束。规则合同集合不唯一、相同前驱存在不兼容映射／切点组合或同键异结果时必须 `CONFLICTED`。

### TM-R10-09 只有唯一外层登记后继可以进入账本资格

```text
Registered Complete Successor Boundary
  -> Unique Mapping-and-cut Successor Aggregate
  -> Aggregate Registration Resolution
```

只有外层 `REGISTERED` 且内层 `SELECTED` 的内容同一载荷才是 `Registered Selected Temporal Catalog Successor Resolution`。

类型资格、位置分配、记录登记、账本边界和 `T` 只能消费该解析。裸治理根、规则 ID、目录合同或切点候选不能替代。

### TM-R10-10 后续演进继续固定已选择后继

目录 `C1` 被唯一选择后，下一后继槽必须使用：

```text
Predecessor = Registered Selected Temporal Catalog Successor Resolution(C1)
```

继续从 `C0` 提交较晚规则版本、映射或切点属于旧槽候选遗漏或平行分叉，必须 `CONFLICTED`。

## 四、规范位置、类型资格和账本谱系

### TM-R10-11 规范位置主体保持唯一

R9 的位置主体继续为：

```text
Canonical Temporal Position Qualification Subject Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

候选位置到已分配位置的内容同一证明、最终资格重验和永久空洞规则继续有效。目录谱系最小化不改变位置身份。

### TM-R10-12 类型资格只能固定规范谱系和唯一后继

类型资格、六种证明记录及其他时间记录登记固定：

```text
Canonical Temporal Catalog Lineage Key
Registered Selected Temporal Catalog Successor Resolution
Selected Exact Effective-cut Payload
Canonical Allocated Position Qualification Subject
Record-type Eligibility Result = PERMITTED
```

R9 已废止治理根和规则 ID 不得保留在资格键、验证包或兼容字段中。

### TM-R10-13 账本边界必须拒绝混入废止根

跨目录账本边界继续固定前驱目录、已选择后继、精确切点、成员到目录归属和位置主体。

成员使用 R9 已废止治理根字段、同一位置存在多个规范谱系归属或目录规则版本改变成员根时，边界必须 `INDETERMINATE` 或 `CONFLICTED`。

### TM-R10-14 历史位置和 T 继承保持不变

```text
position before selected successor cut
  -> predecessor catalog

position at or after selected successor cut
  -> registered selected successor catalog
```

后继不能重解释旧位置。`T` 继续通过已登记映射账本边界继承目录谱系，不取得规则、根、目录或切点选择权。

## 五、阶段、权威和失败关闭

### TM-R10-15 阶段必须无环

```text
G0 Registered Governance Registry Allocation and Existing Ledger Scope
G1 Canonical Temporal Catalog Lineage Key
G2 Mapping / Cut / Rule-contract Successor Candidates
G3 Registered Complete Boundary and Selected Successor
M0 Canonical Position / Type Eligibility / Record Registration
M1 Registered Complete Ledger Boundary
M2 T -> Coverage / Evaluation -> K
```

规范谱系键只由 `G0` 已登记事实计算，不需要新增治理根登记。`G2` 以后对象不得反向改变 `G0/G1`。

### TM-R10-16 权威不得传播

计算规范目录谱系键不授予规则合同登记、目录候选、切点评价、边界、完整性、聚合、位置分配、记录登记、账本边界、`T` 或 `K` 权威。

目录合同、后继聚合、位置分配和账本完整性权威继续逐操作分离。

### TM-R10-17 非法状态必须失败关闭

- 使用 R9 已废止治理根或规则 ID 分割后继槽；
- `Catalog Lineage Rule Version` 进入规范谱系键；
- 候选账本集合创建第二个目录谱系；
- 不同规则合同版本不共同竞争；
- 边界规则版本形成平行边界；
- 聚合键固定裸治理根、规则 ID、目录合同或切点候选；
- 类型资格或记录登记继续消费废止字段；
- 同一位置属于多个规范目录谱系；
- `T` 自行选择规则合同或目录后继；
- 规范谱系键计算取得任何登记或写入权威；
- 候选、自检或文件存在替代完整竞争与登记解析。

以上状态必须拒绝、`NOT_SELECTED`、`NOT_PERMITTED`、`NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED`。

### TM-R10-18 已通过主干不得回归

```text
Exact Thirteen-type Catalog: PRESERVED
Mapping + Effective-cut Joint Selection: PRESERVED
Canonical Position Identity: PRESERVED
Candidate-to-allocated Position Equality: PRESERVED
Ledger Boundary Catalog Lineage: PRESERVED
T-scoped Aggregate Coverage: PRESERVED
Temporal Governance Boundary Vector T: PRESERVED
Knowledge Boundary K: PRESERVED
Authority Non-propagation: PRESERVED
```

### TM-R10-19 R10 只声明一个阻断候选闭合

```text
TM-R9-B1 Temporal Catalog Lineage Governance-root Registration: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R10 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R9-B1 only
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

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R11` 执行联合交叉接口回归。R10 自检不能独立证明阻断关闭。
