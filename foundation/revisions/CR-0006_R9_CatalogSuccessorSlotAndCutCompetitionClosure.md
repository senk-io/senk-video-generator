# 时间映射治理有界修订 R9

## 修订信息

```text
Proposal ID: CR-0006-R9
Title: Temporal Catalog Successor-slot and Effective-cut Competition Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006-R8 GOVERNED TEMPORAL RECORD-TYPE CATALOG EVOLUTION CLOSURE
Repair Basis: CR-0006-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: TM-R8-B1 only
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
Compatibility Reference: CR-0005-R10
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `TM-R8-B1`：把同一前驱目录的全部映射和生效切点组合放入一个后继竞争槽，并让唯一聚合一次性选择目录内容与切点。它不改变 R8 的十三类记录映射、账本类型、全局位置键、`B/T/K` 或查询坐标身份，不覆盖基础稿或 R1 至 R8 的历史正文，不创建时间制度对象、账本、制度冻结或运行时权威。

## 一、修订边界

### TM-R9-01 R9 只覆盖一个有界阻断

```text
TM-R8-B1 Temporal Catalog Successor-slot and Effective-cut Competition
```

R8 已通过的精确十三类目录、治理注册表分离、类型资格、账本边界目录谱系和 `T` 继承方向继续有效。

### TM-R9-02 候选映射和切点不得分割后继槽

```text
Effective-cut Vector ID or Digest
Exact Per-ledger Effective Cut Set
Catalog Contract ID or Version
Exact Type-to-ledger Mapping Set Digest
Candidate Rule Contract Version
Registration Time
Writer or Authority Holder
```

以上字段不得进入目录后继槽语义键。它们必须作为同一后继槽中的候选载荷共同竞争。

## 二、时间目录唯一后继槽

### TM-R9-03 后继槽只固定谱系根和唯一前驱

R8 `TM-R8-05` 的目录演进语义键由本规则覆盖为：

```text
Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key =
  Temporal Record-type Catalog Lineage Root Key
+ Registered Predecessor Catalog Aggregate Registration Resolution ID and Digest
    or CANONICAL_R5_CATALOG_GENESIS_MARKER
+ Registered Catalog Lineage Governance Root ID and Digest
+ Catalog Successor-slot Semantic Rule ID
```

治理根是谱系创建时固定的不可变语义根，不是候选合同版本或候选演进规则版本。`Catalog Successor-slot Semantic Rule ID` 是治理根载荷的固定成员，不能由候选提供或换 ID 分域。

同一目录谱系和同一前驱只能形成一个后继槽。生效切点、类型映射、目录合同和候选摘要不得进入该键。

### TM-R9-04 初始 R5 目录也必须共同竞争

初始目录使用：

```text
Predecessor = CANONICAL_R5_CATALOG_GENESIS_MARKER
```

所有声称承接 R5 七种规范映射的初始目录候选，无论生效切点、合同 ID 或载荷如何，都进入同一个 `GENESIS` 后继槽。

### TM-R9-05 生效切点改为后继候选子对象

R8 的 `Temporal Record-type Catalog Effective-cut Vector Key` 不再是可独立分割目录语义域的键，改为：

```text
Temporal Catalog Successor Effective-cut Candidate Key =
  Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Candidate Exact Per-ledger Effective Cut Set Digest
+ Candidate Cut Evidence Payload Digest
+ Cut Candidate Identity Rule Version
```

精确切点集合变化产生新的切点候选，但全部候选仍属于同一个后继槽。

切点候选不是时间账本记录，不独立产生可被类型资格选择的最终切点解析。它只作为目录后继候选的不可变子对象，由唯一后继聚合一起选择。

### TM-R9-06 每个候选切点载荷必须完整

```text
Temporal Catalog Successor Effective-cut Candidate Payload =
  Temporal Catalog Successor Effective-cut Candidate Key
+ Exact Per-ledger Effective Cut Set
+ Registered Predecessor Ledger Boundary Set Digest
+ Required Cut-boundary Completeness Resolution IDs and Digests
+ Cut Position Continuity Proof Set Digest
+ No-overlap and No-gap Claim Digest
+ Candidate Cut Result
+ Cut Canonicalization Rule Version
```

每个账本切点继续固定账本 ID、版本、类型、前驱边界、末位置、首个后继位置和追加纪元。

候选结果为：

```text
QUALIFIED_CUT
NOT_QUALIFIED_CUT
INDETERMINATE
CONFLICTED
```

切点评价权威不能定义目录映射、登记目录合同或分配记录位置。

### TM-R9-07 目录后继候选必须绑定一个精确切点候选

```text
Temporal Catalog Successor Candidate Payload =
  Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Temporal Governance Contract Key and Candidate Payload Digest
+ Registered Catalog Evolution Rule Contract Registration Resolution ID and Digest
+ Exact Temporal Record Type-to-ledger Mapping Set
+ Exact Governed Ledger ID, Version and Type Set
+ Predecessor Mapping Set Digest or CANONICAL_R5_MAPPING_DIGEST
+ Append-only Mapping Evolution Proof Digest
+ Temporal Catalog Successor Effective-cut Candidate Key and Payload Digest
+ Candidate Catalog Successor Result
+ Candidate Canonicalization Rule Version
```

候选目录内容和候选切点不可分割。相同映射配不同切点、不同映射配相同切点或规则合同不等，都形成同一后继槽中的不同候选。

### TM-R9-08 后继候选必须拥有稳定键

```text
Temporal Catalog Successor Candidate Key =
  Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Candidate Catalog Successor Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。候选映射、切点、证据或结果变化不能改变后继槽归属。

### TM-R9-09 后继候选继续通过时间治理合同登记

```text
Candidate Temporal Catalog Successor Contract
  -> Temporal Governance Contract Registration Attempt
  -> Registered Temporal Governance Contract Record
  -> Temporal Governance Contract Registration Resolution
```

合同类型继续为 `TEMPORAL_RECORD_TYPE_CATALOG`。候选与登记载荷必须内容同一；合同登记非 `REGISTERED` 时不能成为确定后继。

候选、切点子对象、后继边界和聚合记录全部位于目录治理注册表，不进入任何时间账本。

## 三、完整竞争和目录—切点联合选择

### TM-R9-10 后继竞争边界必须覆盖全部切点与映射组合

```text
Temporal Catalog Successor Competing Boundary Key =
  Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key
+ Registered Temporal Governance Contract Registry Boundary ID and Digest
+ Exact Successor Candidate Registration Resolution Set Digest
+ Exact Candidate Effective-cut Set Digest
+ Exact Candidate Mapping Set Digest
+ Required Successor Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖同一前驱下全部目录合同、类型映射、切点候选、证据、登记尝试、永久空洞、前驱分叉和冲突谱系。

按切点、合同版本、候选结果、登记时间或偏好类型映射过滤成员必须失败关闭。

### TM-R9-11 后继边界必须形成四值登记解析

```text
Candidate Temporal Catalog Successor Competing Boundary
  -> Boundary Registration Attempt
  -> Registered Successor Competing Boundary Record
  -> Successor Boundary Registration Resolution
```

结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。同边界键异候选组合、异切点集合、异映射集合或遗漏空洞必须 `CONFLICTED`。

边界构造者和目录合同登记者不能评价该边界完整性。

### TM-R9-12 唯一后继聚合必须联合选择目录与切点

```text
Temporal Catalog Unique Successor Aggregate Resolution Key =
  Temporal Record-type Catalog Successor-slot Semantic Conflict Set Key
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

- 唯一内容同一 `QUALIFIED_CUT + QUALIFIED_SUCCESSOR` 组合支持 `SELECTED`；
- 完整无合格组合支持 `NOT_SELECTED`；
- 映射、切点、证据、边界或完整性未知支持 `INDETERMINATE`；
- 同前驱多个不兼容映射／切点组合、同映射异合格切点或同切点异合格映射支持 `CONFLICTED`。

所选载荷必须同时保存精确十三类映射和精确每账本生效切点。

### TM-R9-13 后继聚合必须形成外层登记解析

```text
Registered Complete Successor Competing Boundary
  -> Candidate Unique Successor Aggregate Resolution
  -> Successor Aggregate Registration Attempt
  -> Registered Successor Aggregate Record
  -> Successor Aggregate Registration Resolution
```

外层结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。只有外层 `REGISTERED` 且内层 `SELECTED` 的内容同一载荷才是：

```text
Registered Selected Temporal Catalog Successor Resolution
```

类型资格、位置分配、记录登记和账本边界只能消费该解析，不能独立选择目录合同或切点候选。

### TM-R9-14 后续目录演进必须使用已选择后继作为前驱

目录 `C1` 从 `C0` 后继槽被选择后，后续演进必须固定：

```text
Predecessor = Registered Selected Temporal Catalog Successor Resolution(C1)
```

禁止继续以 `C0` 为前驱，仅使用较晚切点形成第二后继。该状态属于旧槽遗漏候选或平行分叉，必须 `CONFLICTED`。

## 四、规范位置主体和类型资格

### TM-R9-15 位置候选与已分配位置必须共享规范主体键

R8 `TM-R8-16` 中的“候选位置或已分配位置引用”由本规则收紧为：

```text
Canonical Temporal Position Qualification Subject Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

候选位置声称和最终已分配位置必须投影同一个规范主体键。位置分配尝试、分配解析和记录登记载荷保存内容同一证明。

候选阶段可以评价目录切点范围，但最终记录登记必须重新验证已分配位置主体与候选主体完全相等。不同则 `CONFLICTED`，不能沿用候选资格。

### TM-R9-16 类型资格必须固定唯一后继和所选切点

```text
Temporal Record-type Eligibility Key =
  Registered Selected Temporal Catalog Successor Resolution ID and Digest
+ Selected Exact Effective-cut Payload Digest
+ Canonical Temporal Position Qualification Subject Key
+ Temporal Record Type
+ Canonical Record Payload Discriminator Digest
+ Record-type Eligibility Rule Version
```

目录后继非外层 `REGISTERED + SELECTED`、切点不唯一、位置主体位于生效范围外或类型映射不等时，不得 `PERMITTED`。

候选位置资格与最终已分配位置资格共享同一逻辑键；载荷或结果不等必须使记录登记 `CONFLICTED`。

### TM-R9-17 位置分配和记录登记必须固定内容同一证明

R8 的原子登记载荷新增：

```text
Candidate Position Subject Key
Registered Allocated Position Subject Key
Candidate-to-allocated Position Equality Proof Digest
Registered Selected Catalog Successor Resolution
Selected Effective-cut Payload Digest
Final Record-type Eligibility Result = PERMITTED
```

位置分配完成前的资格不能单独授权记录登记。最终 `PERMITTED` 必须基于已分配位置重新确认，且不改变 `Temporal Derived Record Position Key`。

### TM-R9-18 六种证明记录统一消费所选后继

R6/R7 六种证明记录的候选、边界和聚合登记共同固定：

```text
Registered Selected Temporal Catalog Successor Resolution
Selected Mapping-ledger Effective Cut
Canonical Allocated Position Subject
Record-type Eligibility Result = PERMITTED
```

只固定 R8 目录候选、独立切点候选或类型投影摘要不能形成确定登记。

## 五、账本边界、历史、T 和阶段

### TM-R9-19 账本边界必须固定唯一后继归属

每个时间账本边界继续保存成员到目录谱系的精确映射，但新成员只可引用已选择目录后继。

跨目录边界固定：

```text
Predecessor Catalog Resolution Set
Registered Selected Successor Resolution Set
Selected Effective-cut Payload Set
Exact Member-to-catalog Assignment
Exact Member Position Qualification Subject Set
```

同一位置存在多个目录归属、成员位于所选切点错误一侧或目录后继非唯一时必须 `INDETERMINATE` 或 `CONFLICTED`。

### TM-R9-20 历史位置和 T 继承保持不变

```text
position before selected successor cut
  -> predecessor catalog

position at or after selected successor cut
  -> exact selected successor catalog
```

后继目录不能重解释旧位置。`T` 继续通过已登记映射账本边界继承目录谱系，不取得目录或切点选择权。

目录后继、切点或成员归属变化必须产生新的账本边界、`T`、评价和 `K` 身份，不能覆盖历史对象。

### TM-R9-21 阶段必须保持无环

```text
G0 Allocated Temporal Governance Registry and Catalog Lineage Root
G1 Catalog Successor Mapping / Effective-cut Combined Candidates
G2 Registered Complete Successor Boundary
G3 Registered Selected Catalog Successor
M0 Canonical Position Subject / Allocation / Type Eligibility
M1 Registered Temporal Records and Complete Ledger Boundary
M2 Temporal Governance Boundary Vector T
M3 T-scoped Coverage and Temporal Eligibility
M4 Completeness Evaluation and Knowledge Boundary K
```

`G1` 至 `G3` 不写入时间账本；`M0` 以后对象不得反向改变目录候选、所选切点或前驱目录。

### TM-R9-22 新增权威必须逐操作分离

后继槽定义、映射候选、切点候选、合同登记、边界、完整性、唯一后继聚合、位置分配、类型资格、记录登记、账本边界、`T` 和评价权威不得互相传播。

目录后继被选择不授予记录写入或位置分配权威。

### TM-R9-23 非法状态必须失败关闭

- 生效切点、目录版本或映射摘要进入目录后继槽键；
- 同一前驱的不同切点进入不同竞争边界；
- 独立切点解析绕过目录—切点联合聚合；
- 先选择目录映射再由调用方选择切点；
- 同一前驱多个不兼容组合仍选择其一；
- 已选择 `C1` 后继续从 `C0` 登记较晚平行后继；
- 类型资格消费目录候选或切点候选而非唯一后继解析；
- 候选位置与已分配位置主体不等仍沿用 `PERMITTED`；
- 新目录重解释切点之前的旧位置；
- 目录类型创建新账本、分区、追加纪元或位置键；
- `T` 或覆盖子对象自行选择目录切点；
- 候选、自检或文件存在替代完整竞争和登记解析。

以上状态必须拒绝、`NOT_SELECTED`、`NOT_PERMITTED`、`NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED`。

### TM-R9-24 已通过主干不得回归

```text
R5 Seven-type Baseline Catalog: PRESERVED
R6 / R7 Six Proof Record Mappings: PRESERVED
Exact Thirteen-type Successor Catalog: PRESERVED
Global Temporal Position Identity: PRESERVED
Ledger Boundary Catalog Lineage: STRENGTHENED
T-scoped Aggregate Coverage: PRESERVED
Temporal Governance Boundary Vector T: PRESERVED
Knowledge Boundary K: PRESERVED
Authority Non-propagation: PRESERVED
```

### TM-R9-25 R9 只声明一个阻断候选闭合

```text
TM-R8-B1 Temporal Catalog Successor-slot and Effective-cut Competition: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R9 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: TM-R8-B1 only
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

下一阶段必须独立复审 `CR-0006` 复合模型，并与 `CR-0005-R10` 执行交叉接口回归审查。R9 自检不能独立证明阻断关闭。
