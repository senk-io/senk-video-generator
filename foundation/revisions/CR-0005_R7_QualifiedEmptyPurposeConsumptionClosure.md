# 来源注册表接口有界修订 R7

## 修订信息

```text
Proposal ID: CR-0005-R7
Title: Qualified Empty Required-purpose Consumption Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R6 REGISTRY REFERENCE AND CROSS-PURPOSE CONSISTENCY CLOSURE
Repair Basis: CR-0005-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R6-B1 only
Draft Repair Scope Lock: LOCKED
Scope Lock Basis: User-approved before proposal construction
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
Compatibility Reference: CR-0006-R6
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R6-B1`：删除裸“无需生命周期解析”标记，并使空目的与非空目的消费共同固定已登记必要目的资格。`Draft Repair Scope Lock` 只锁定本草案修复口径，不是制度冻结，不创建冻结标识、注册表、生命周期解析或运行时权威。

## 一、修复口径锁

### SR-R7-01 本轮修复命题已经锁定

本轮唯一命题为：

```text
Every lifecycle consumption branch
  -> pins one registered required-purpose qualification aggregate

Empty branch
  -> QUALIFIED + EMPTY_SET + complete purpose boundary

Nonempty branch
  -> QUALIFIED + NONEMPTY_SET + registered cross-purpose aggregate
```

R7 不重新设计注册表引用、逐目的解析、跨目的聚合或来源适用性状态集合。

### SR-R7-02 口径锁不产生制度权威

```text
Draft Repair Scope Lock
  -/-> Institution Freeze
  -/-> Freeze ID
  -/-> Registry Authority
  -/-> Runtime Authority
```

任何制度冻结仍必须经过独立复审、交叉接口回归和适用的外部冻结流程。

## 二、裸标记退场

### SR-R7-03 裸无需解析标记永久失去消费资格

以下值不再是合法 `Lifecycle Resolution Consumption Reference`：

```text
LIFECYCLE_RESOLUTION_NOT_REQUIRED
```

历史 R5/R6 文本保留，但该裸标记在 R7 复合候选语义中必须被解释为：

```text
INADMISSIBLE_BARE_MARKER
```

读取到裸标记必须失败关闭，不能自动升级、迁移或推断为空目的资格。

### SR-R7-04 所有消费分支必须使用共同资格前缀

```text
Lifecycle Required-purpose Qualification Consumption Prefix =
  Registered Required Purpose Aggregate Registration Resolution ID and Digest
+ Registration Result = REGISTERED
+ Lifecycle Required Purpose Qualification Aggregate Resolution ID and Digest
+ Required Purpose Semantic Result = QUALIFIED
+ Registered Purpose Qualification Competing Boundary Resolution ID and Digest
+ Required Purpose-boundary Completeness Resolution IDs and Digests
+ Exact Required Lifecycle Resolution Purpose Set Digest
+ Registered Lifecycle Resolution Rule Contract Payload Digest
```

缺少任一字段、摘要不一致、外层非 `REGISTERED`、内层非 `QUALIFIED` 或边界完整性未知时，不得形成消费引用。

## 三、消费引用稳定身份

### SR-R7-05 消费引用必须拥有稳定键

```text
Lifecycle Resolution Consumption Reference Key =
  Cross-purpose Lifecycle Consistency Semantic Conflict Set Key
+ Lifecycle Required-purpose Qualification Consumption Prefix Digest
+ Derived Consumption Mode
+ Cross-purpose Consumption Component Digest
+ Consumption Reference Rule Version
```

`Derived Consumption Mode` 不是调用者输入，必须由已登记精确目的集合唯一派生：

```text
EMPTY_SET     -> QUALIFIED_EMPTY_REQUIRED_PURPOSES
NONEMPTY_SET  -> QUALIFIED_NONEMPTY_REQUIRED_PURPOSES
```

未知集合、非规范集合或集合摘要与资格载荷不一致时，不能派生消费模式。

### SR-R7-06 消费引用是内容同一投影而非新权威对象

```text
Lifecycle Resolution Consumption Reference Digest =
  CanonicalDigest(
    Lifecycle Resolution Consumption Reference Key
    + Complete Consumption Payload
  )
```

引用只投影已登记资格和组合解析，不创建新的注册表、解析或权威根。引用键、载荷和摘要随来源适用性变化聚合候选内容同一登记。

同一引用键异载荷或异摘要必须使来源适用性聚合登记 `CONFLICTED`。

## 四、合格空目的消费

### SR-R7-07 空目的分支必须固定已登记完整空集

```text
Qualified Empty Required-purpose Consumption Payload =
  Lifecycle Required-purpose Qualification Consumption Prefix
+ Derived Consumption Mode = QUALIFIED_EMPTY_REQUIRED_PURPOSES
+ Exact Required Lifecycle Resolution Purpose Set Digest = CANONICAL_EMPTY_SET_DIGEST
+ Required Purpose Set Cardinality = 0
+ Cross-purpose Aggregate Registration Resolution = NOT_APPLICABLE
+ Empty-purpose Consumption Rule Version
```

空集必须由 R6 的完整目的资格竞争边界和已登记资格聚合证明。零条查询结果、未读取目的记录或调用者声称“不需要”均不能替代该空集。

### SR-R7-08 空目的资格必须与完整变化集合内容同一

空目的资格载荷必须证明：

```text
Qualification.Source Applicability Change Set Boundary ID and Digest
= Consumption.Cross-purpose Semantic Key.Change Set Boundary ID and Digest

Qualification.Temporal Query Coordinate Subject Reference Digest
= Consumption.Cross-purpose Semantic Key.Query Subject Digest

Qualification.Registry Reference and Contract
= Consumption.Cross-purpose Semantic Key.Registry Reference and Contract
```

资格解析与消费上下文不等时必须 `CONFLICTED`，不能解释为另一查询或另一变化集合的空目的证明。

### SR-R7-09 空目的分支不能自行决定来源适用性

`QUALIFIED_EMPTY_REQUIRED_PURPOSES` 只证明“不需要跨目的生命周期消歧”，不证明来源为 `APPLICABLE` 或 `INAPPLICABLE`。

确定结果仍必须来自 R4/R5 已闭合的完整变化集合语义：

```text
single effect or multiple content-identical effects
  -> may support corresponding lifecycle state

NO_APPLICABLE_CHANGE
  -> INDETERMINATE

incompatible effects despite empty-purpose claim
  -> CONFLICTED
```

## 五、合格非空目的消费

### SR-R7-10 非空目的分支必须固定跨目的聚合

```text
Qualified Nonempty Required-purpose Consumption Payload =
  Lifecycle Required-purpose Qualification Consumption Prefix
+ Derived Consumption Mode = QUALIFIED_NONEMPTY_REQUIRED_PURPOSES
+ Exact Required Lifecycle Resolution Purpose Set Digest
+ Required Purpose Set Cardinality > 0
+ Registered Cross-purpose Aggregate Registration Resolution ID and Digest
+ Cross-purpose Registration Result = REGISTERED
+ Registered Cross-purpose Aggregate Payload Digest
+ Cross-purpose Semantic Result
+ Nonempty-purpose Consumption Rule Version
```

逐目的聚合、单一有利目的、裸后继或未登记组合不能替代跨目的聚合。

### SR-R7-11 跨目的聚合必须固定同一个资格解析

```text
Cross-purpose Aggregate.Required Purpose Aggregate Registration Resolution ID and Digest
= Consumption Prefix.Required Purpose Aggregate Registration Resolution ID and Digest

Cross-purpose Aggregate.Exact Required Purpose Set Digest
= Consumption Prefix.Exact Required Purpose Set Digest

Cross-purpose Aggregate.Cross-purpose Semantic Conflict Set Key
= Consumption Reference.Cross-purpose Semantic Conflict Set Key
```

任一不等、目的遗漏、重复或上下文漂移必须 `CONFLICTED`。

### SR-R7-12 非空分支结果必须失败关闭

```text
CONSISTENT_RESOLVED -> may support uniquely proven lifecycle state
NOT_RESOLVED       -> CONFLICTED
INDETERMINATE      -> INDETERMINATE
CONFLICTED         -> CONFLICTED
```

只有外层跨目的登记解析 `REGISTERED` 且内层语义 `CONSISTENT_RESOLVED` 可以支持确定生命周期状态。

## 六、空集与非空集冲突优先

### SR-R7-13 消费模式必须由资格集合唯一决定

```text
QUALIFIED + EMPTY_SET
  -> only QUALIFIED_EMPTY_REQUIRED_PURPOSES

QUALIFIED + NONEMPTY_SET
  -> only QUALIFIED_NONEMPTY_REQUIRED_PURPOSES

NOT_QUALIFIED | INDETERMINATE
  -> INDETERMINATE

CONFLICTED
  -> CONFLICTED
```

同一资格解析不能同时支持空和非空模式。

### SR-R7-14 空集与非空集不兼容必须冲突

以下组合必须失败关闭：

```text
EMPTY_SET qualification + cross-purpose aggregate reference
NONEMPTY_SET qualification + NOT_APPLICABLE cross-purpose component
EMPTY_SET payload + nonzero cardinality
NONEMPTY_SET payload + zero cardinality
same qualification semantic key + incompatible purpose sets
same consumption reference key + incompatible payloads
```

资格边界或集合完整性未知时只能 `INDETERMINATE`，不能偏好空集。

## 七、来源适用性聚合消费收紧

### SR-R7-15 来源适用性变化聚合键必须固定引用键与摘要

R6 的消费字段由本规则覆盖为：

```text
Source Applicability Change Aggregate Resolution Key =
  Source Applicability Change Conflict Set Key
+ Registered Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Lifecycle Resolution Consumption Reference Key and Digest
+ Aggregate Rule Version
```

裸标记、缺失引用、只含模式字符串或只含跨目的聚合 ID 均不合格。

### SR-R7-16 来源适用性聚合登记必须保存完整资格谱系

候选、登记尝试和已登记来源适用性变化聚合必须保存：

```text
Required Purpose Qualification Aggregate and Registration Resolutions
Purpose Competing Boundary and Completeness Resolutions
Exact Required Purpose Set Digest and Cardinality
Derived Consumption Mode
Cross-purpose Aggregate Registration Resolution or NOT_APPLICABLE
Consumption Reference Key, Payload and Digest
```

候选与登记载荷必须内容同一。同来源适用性聚合键异资格、集合、模式或组合载荷必须 `CONFLICTED`。

## 八、历史、权威和非法状态

### SR-R7-17 目的资格变化必须形成新的适用性身份

目的候选、资格边界、资格聚合、精确目的集合、跨目的聚合、规则或查询上下文变化，必须形成新的消费引用和来源适用性聚合身份。

历史对象继续固定旧资格和组合解析；当前重述不能用新的空目的资格覆盖历史非空解析，也不能沿用旧空集绕过当前非空资格。

### SR-R7-18 消费引用构造权不得传播

消费引用构造者只能投影已登记输入，不能构造目的资格、跨目的聚合、来源变化、时间坐标或制度冻结。引用构造与来源适用性聚合执行、登记和完整性权威必须分离。

### SR-R7-19 新增非法状态必须失败关闭

- 读取或写入裸 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`；
- 空目的分支缺少已登记资格聚合或完整边界；
- 非空目的分支缺少已登记跨目的聚合；
- 消费模式由调用者提供而不是从目的集合派生；
- 空目的资格来自不同变化集合、查询坐标或合同；
- 空资格自行证明来源适用；
- 空集与非空集不兼容载荷被选择赢家；
- 当前重述沿用旧空集绕过新非空目的；
- 消费引用自授权或创建第二解析根；
- 候选、自检或文件存在替代已登记资格和聚合解析。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`。

## 九、回归与候选级闭合声明

### SR-R7-20 已通过主干不得回归

```text
Lifecycle Registry Reference Identity: PRESERVED
Required Purpose Qualification Identity: PRESERVED
Per-purpose and Cross-purpose Aggregation: PRESERVED
Source Applicability Change Conflict Set: PRESERVED
Source Completeness Aggregate Resolution: PRESERVED
Boundary / Snapshot Reproducibility: PRESERVED
Four-value Coordinate Subject Totality: PRESERVED
Historical / Current Separation: STRENGTHENED
Cross-interface Acyclicity: PRESERVED
```

### SR-R7-21 R7 只声明一个阻断候选闭合

```text
SR-R6-B1 Qualified Empty Required-purpose Consumption: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R7 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R6-B1 only
Draft Repair Scope Lock: LOCKED
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并在 `CR-0006-R6` 独立复审完成后执行交叉接口回归审查。R7 自检不能独立证明阻断关闭。
