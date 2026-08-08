# 时间映射治理有界修订 R1

## 修订信息

```text
Proposal ID: CR-0006-R1
Title: Knowledge Boundary and Temporal Ledger Closure
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0006 TEMPORAL MAPPING GOVERNANCE
Repair Basis: CR-0005-CR-0006-CROSS-INTERFACE-REVIEW
Repair Scope: B1 + B2 + B3 + B4 + B5 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Parallel Revision Target: CR-0005-R1
Cross-interface Re-review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Temporal Ledger Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复交叉接口审查的 B1 至 B5。它不覆盖 `CR-0006` 或审查记录的历史文本，不创建规范时间字段、映射记录、时间账本、认识边界、制度冻结或运行时权威。

## 一、修订解释边界

### TM-R1-01 R1 只覆盖五项交叉接口阻断

本修订只覆盖 `CR-0006` 的 `TM-C-04`、`TM-C-20` 至 `TM-C-25`、`TM-C-29` 至 `TM-C-32`、`TM-C-43` 至 `TM-C-46`、`TM-C-49` 及相应自检和当前状态中与下列事项冲突的部分：

```text
B1 Registered Raw Temporal Assertion Consumption
B2 Query-specific Completeness Requirements
B3 Knowledge-time Type Closure
B4 Temporal-derived Ledger Historical Boundary
B5 Temporal Query Coordinate Content Identity
```

未被本修订显式覆盖的 `CR-0006` 规则继续作为合并候选语义。`CR-0005-R1` 提供 B1、B3 和 B5 的来源侧交接契约。

### TM-R1-02 R1 保持来源先于时间的单向所有权

```text
Registered Base Source Boundary Vector
  -> Registered Temporal Mapping / Correction / Migration Records
  -> Registered Temporal Governance Boundary Vector
  -> Registered Knowledge Boundary Vector
  -> Registered Temporal Query Coordinate
```

时间治理不能创建原始时间断言、来源记录、来源边界、快照或来源完整性。来源治理不能创建规范时间值、时间派生账本边界、认识边界或查询坐标。

## 二、B1：只消费已登记原始时间断言

### TM-R1-03 原始时间断言的提供方身份必须保持不透明

`Raw Temporal Assertion` 的来源身份和载荷由 `CR-0005-R1` 登记。时间治理只能验证并消费：

```text
Registered Raw Temporal Assertion ID and Payload Digest
Parent Registered Source Record ID and Digest
Source Temporal Field ID and Version
Subject ID and Version
Raw Value Shape and Digest
Assertion Evidence References
Registered Source Boundary and Snapshot References
```

时间治理不能改变断言字段、主体、原始值、精度、不确定性或证据，也不能从父载荷重新抽取未登记断言。

### TM-R1-04 映射输入必须绑定来源侧内容同一

以本规则收紧 `TM-C-29` 和 `TM-C-30`：

```text
Temporal Mapping Input Record Key =
  Registered Raw Temporal Assertion ID and Payload Digest
+ Parent Registered Source Record ID and Digest
+ Registered Base Source Boundary Vector ID and Digest
+ Source Temporal Field ID and Version
+ Target Canonical Temporal Field ID and Version
+ Subject ID and Version
+ Temporal Mapping Rule ID and Version
+ Supporting Evidence Set Digest
```

输入记录必须验证原始断言位于所引用来源边界和快照摘要内。断言、父记录、边界向量、目标字段、规则或证据变化必须形成新映射输入身份。

```text
Unregistered or non-identical assertion -> INDETERMINATE
Same mapping input key with incompatible payload -> CONFLICTED
```

缺失断言不能通过重新解析文本、文件元数据、数据库默认值或系统当前时间补齐。

## 三、B2：按查询目的选择完整性门槛

### TM-R1-05 必须登记查询所需完整性维度集合

新增对象：

```text
Temporal Consumption Completeness Requirement Set
```

稳定键为：

```text
Requirement Set Key =
  Query Purpose
+ Source Registry ID and Version
+ Registry Scope Digest
+ World Boundary Mode
+ Exact Query Scope Digest
+ Absence Claim Mode
+ Required Completeness Dimension Set
+ Requirement Rule Version
```

候选与已登记要求集合必须内容同一。要求集合制定、资格计算和登记权威必须分离，且不能由查询者临时删减必要维度。

```text
Temporal Consumption Requirement Definition Authority Type
Temporal Consumption Requirement Registration Authority Type
Completeness Requirement Evaluation Execution Authority Type
Completeness Requirement Evaluation Registration Authority Type
```

要求制定者不能登记自身要求，评价执行者不能修改要求集合或来源完整性记录，评价登记者不能修改候选。

### TM-R1-06 查询目的和缺失声明必须封闭

```text
Query Purpose =
  EXACT_KNOWN_SET_REPLAY
| QUALIFIED_ABSENCE_CHECK
| EXHAUSTIVE_SCOPE_RESOLUTION

Absence Claim Mode =
  NO_ABSENCE_CLAIM
| QUALIFIED_ABSENCE_REQUIRED
| EXHAUSTIVE_MEMBERSHIP_REQUIRED
```

- `EXACT_KNOWN_SET_REPLAY` 只重放精确边界内的已登记成员，不声明边界外不存在其他成员；
- `QUALIFIED_ABSENCE_CHECK` 必须绑定适用的关闭或独立否定证明；
- `EXHAUSTIVE_SCOPE_RESOLUTION` 必须证明查询作用域成员穷尽。

查询目的不能靠输出为空、调用方名称或投影用途推断。

### TM-R1-07 确定性只要求已登记必要维度完整

对每个来源向量条目：

```text
Registered Requirement Set
+ Registered Source Completeness Records
  -> Completeness Requirement Evaluation
```

评价值域：

```text
SATISFIED
NOT_SATISFIED
INDETERMINATE
CONFLICTED
```

只有要求集合中每个必要维度均有适用、已登记、无冲突的 `COMPLETE` 记录，才支持 `SATISFIED`。非必要维度的非完整状态必须保存，不能传播为查询范围内的穷尽否定，也不能无条件阻断精确已知集合重放。

同一要求集合和边界产生不兼容评价时必须 `CONFLICTED`。

### TM-R1-08 开放世界只能支持无缺失声明的精确重放

```text
OPEN_WORLD
+ EXACT_KNOWN_SET_REPLAY
+ NO_ABSENCE_CLAIM
+ satisfied query-required dimensions
  -> may support determinate Knowledge Boundary
```

```text
OPEN_WORLD
+ QUALIFIED_ABSENCE_REQUIRED or EXHAUSTIVE_MEMBERSHIP_REQUIRED
  -> INDETERMINATE
  -/-> qualified absence
```

`CLOSED_WORLD` 与 `PARTITIONED_CLOSED_WORLD` 只有在 `CR-0005` 所要求的关闭契约、精确分区和独立成员完整性均适用时，才能支持缺失或穷尽声明。

### TM-R1-09 认识边界条目必须固定完整性评价身份

每个认识边界条目必须绑定：

```text
Source Registry ID and Version
Source Boundary and Snapshot IDs and Digests
World Boundary Mode and Exact Query Scope Digest
Registered Requirement Set ID and Digest
Registered Completeness Requirement Evaluation ID and Digest
Required Source Completeness Record IDs and Digests
Preserved Non-required Incompleteness References
Per-registry Recorded-at Cutoff or Exact Record Set
Eligible Temporal Mapping References
Entry Digest
```

因此，查询目的、必要维度或缺失声明模式变化必然形成新的认识边界条目和向量身份。

## 四、B3：认识时间只有一个规范对象

### TM-R1-10 认识边界向量是唯一规范 Known At 坐标

在所有接口中：

```text
Known At
  := Registered Knowledge Boundary Vector ID and Digest
```

`Known At` 是兼容名称，不是规范时间字段，也不属于 `Canonical Temporal Value`。因此不新增 `KNOWN_AT` 字段，不允许单一时间戳、公共上限或显示标签替代认识边界向量。

可以提供非规范 `Knowledge Cutoff Display Label`，但它只能由向量派生，不能进入解析、完整性或查询身份，也不能证明各注册表截点相等。

### TM-R1-11 认识边界向量键必须固定全部来源和时间边界

以本规则覆盖 `TM-C-20` 中的 `Canonical Known At Value` 路径：

```text
Knowledge Boundary Vector Key =
  Registered Base Multi-registry Source Boundary Vector ID and Digest
+ Registered Temporal Governance Boundary Vector ID and Digest
+ Ordered Per-registry Cutoff or Exact-record-set Entry Digests
+ Ordered Completeness Requirement Evaluation IDs and Digests
+ Temporal View Mode
+ Knowledge Boundary Rule Version
```

```text
Knowledge Boundary Vector Digest
= canonical digest of the complete keyed payload
```

向量不得以单一墙钟时间作为身份替代项。来源向量、时间治理向量、任一截点、完整性评价、视图或规则版本变化必须形成新身份。

## 五、B4：时间派生账本的历史边界

### TM-R1-12 时间派生记录必须进入独立追加账本

新增逻辑对象：

```text
Temporal Mapping Ledger
Temporal Correction Ledger
Temporal Migration Ledger
Temporal Derived Record Position
Temporal Derived Ledger Boundary
Temporal Derived Ledger Completeness Record
Temporal Governance Boundary Vector
```

这些对象只固定时间治理派生记录的登记历史，不取得来源、业务事实、合法性、资格、提交、闭包或投影权威。

新增逐操作权威类型：

```text
Temporal Derived Position Allocation Authority Type
Temporal Derived Boundary Construction Authority Type
Temporal Derived Boundary Registration Authority Type
Temporal Derived Completeness Qualification Authority Type
Temporal Derived Completeness Registration Authority Type
Temporal Governance Vector Construction Authority Type
Temporal Governance Vector Registration Authority Type
```

记录登记、位置分配、边界构造、边界登记、完整性资格、完整性登记和向量登记权威不得互相传播。每个授权实例必须限定账本身份、账本类型、输入和输出记录类型、边界域及规则版本。

### TM-R1-13 时间派生位置和边界必须稳定且不可复用

每个映射、更正或迁移记录登记时必须在对应账本原子取得追加位置：

```text
Temporal Derived Record Position Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ Append Epoch
+ Position Value
```

位置不得复用、重排或覆盖。失败登记可以留下不可回收空洞。

```text
Temporal Derived Ledger Boundary Key =
  Temporal Ledger ID and Version
+ Temporal Ledger Type
+ First and Last Position or Exact Record Set Digest
+ Boundary Rule Version
```

边界必须形成候选、登记尝试和内容同一的已登记记录，并保存记录身份与摘要、空洞、冲突子域、候选与登记摘要、权威、登记时间和证据。

### TM-R1-14 时间派生账本完整性不得自证

每个时间派生边界至少分别评价：

```text
CARRIER_INTEGRITY
POSITION_CONTINUITY
READ_COMPLETENESS
CONFLICT_SUBDOMAIN_COMPLETENESS
```

完整性记录必须由不能登记被评价时间记录、修改边界或排除冲突的独立权威形成候选—登记链，并使用：

```text
COMPLETE
INCOMPLETE
INDETERMINATE
CONFLICTED
```

边界摘要、记录数量、时间过滤、读取成功或时间治理自身均不能证明完整。

### TM-R1-15 时间治理边界向量必须固定三类账本

```text
Temporal Governance Boundary Vector Key =
  Ordered Mapping / Correction / Migration Ledger Boundary Digests
+ Required Temporal-ledger Completeness Record IDs and Digests
+ Eligible Base Source Boundary Vector IDs and Digests
+ Temporal Governance Vector Rule Version
```

候选、登记尝试和已登记向量必须内容同一。向量必须保存遗漏、空洞和冲突子域，不能选择“最新”或高置信度记录消除冲突。

对于没有记录的账本，确定空集必须由合格关闭边界和完整性证明支持；空查询或零记录不能自证完整。

### TM-R1-16 来源、时间账本和认识边界必须分阶段无环构造

规范阶段为：

```text
Stage 1: Registered Base Source Boundary Vector B
Stage 2: Registered Temporal Records whose inputs reference B
Stage 3: Registered Temporal Governance Boundary Vector T over those records
Stage 4: Registered Knowledge Boundary Vector K referencing B + T
```

禁止：

```text
Temporal Mapping Input -> K being constructed
Temporal Governance Boundary T -> K -> record included back into the same T
Knowledge Boundary K -> mutate B or T
Later Temporal Record -> rewrite prior B, T or K
```

后续映射、更正、迁移或冲突只能形成新的时间账本边界 `T2` 和认识边界 `K2`。

### TM-R1-17 历史视图必须同时受来源和时间账本边界约束

`HISTORICAL_AS_KNOWN` 只能消费：

```text
records inside Registered Base Source Boundary Vector B
+ temporal mappings, corrections and migrations inside Registered Temporal Governance Boundary Vector T
+ per-ledger and per-registry cutoffs fixed by Knowledge Boundary K
```

记录时间早于显示标签但不位于 `B` 或 `T` 内的记录不得被消费。`CURRENT_RESTATED` 必须绑定新的当前 `B`、`T` 和 `K`，生成新查询及投影身份，不得覆盖历史视图。

## 六、B5：查询坐标与消费内容同一

### TM-R1-18 查询坐标只继承认识边界的视图

以本规则覆盖 `TM-C-21` 的重复视图键：

```text
Temporal Query Coordinate Key =
  Canonical Valid At Value ID and Digest
+ Registered Knowledge Boundary Vector ID and Digest
+ Temporal Query Rule Version
```

`Temporal View Mode` 由认识边界向量继承。查询记录可以重复保存视图用于审计，但必须满足：

```text
Temporal Query Coordinate.View Mode
= Knowledge Boundary Vector.View Mode
```

视图变化先形成新认识边界，再形成新查询坐标；不得只修改查询记录中的重复字段。

### TM-R1-19 查询坐标必须形成候选—登记链和内容同一

```text
Canonical Valid At Value
+ Registered Knowledge Boundary Vector
+ Temporal Query Rule
  -> Candidate Temporal Query Coordinate
  -> Temporal Query Coordinate Registration Attempt
  -> Registered Temporal Query Coordinate
```

候选和已登记记录至少共同绑定完整键、有效时间载荷、认识边界载荷、继承视图、规则、候选与登记摘要、构造和登记权威、登记时间及证据。

```text
Candidate Coordinate Payload Digest
= Registered Coordinate Payload Digest
```

查询解析权威不能登记坐标；坐标登记者不能修改候选或来源、时间账本边界。

```text
Temporal Query Coordinate Construction Authority Type
Temporal Query Coordinate Registration Authority Type
```

查询坐标构造、查询解析和坐标登记权威不得互相传播；任一精确授权缺失、冲突、过期或跨域时必须失败关闭。

### TM-R1-20 来源适用性只能消费整体查询坐标

向 `CR-0005-R1` 返回的规范接口为：

```text
Registered Temporal Query Coordinate ID and Digest
  -> Canonical Valid At Value ID and Digest
  -> Registered Knowledge Boundary Vector ID and Digest
  -> inherited Temporal View Mode
```

如果消费记录展开这些字段，全部展开值必须与坐标内容同一。有效时间来自坐标 A、认识边界来自坐标 B 或视图来自坐标 C 的混合必须失败关闭。

```text
Missing or unregistered coordinate -> INDETERMINATE
Digest or expanded-field mismatch -> CONFLICTED
```

## 七、认识边界解析与失败语义

### TM-R1-21 认识边界构造必须拥有四值解析

```text
Knowledge Boundary Resolution Key =
  Registered Base Source Boundary Vector ID and Digest
+ Registered Temporal Governance Boundary Vector ID and Digest
+ Ordered Completeness Requirement Evaluation IDs and Digests
+ Ordered Cutoff or Exact-record-set Entry Digests
+ Temporal View Mode
+ Knowledge Boundary Resolution Rule Version
```

值域：

```text
AVAILABLE
NOT_AVAILABLE
INDETERMINATE
CONFLICTED
```

- 唯一、完整、内容同一且所有必要评价为 `SATISFIED` 支持 `AVAILABLE`；
- 合格、适用、完整的不可用证明支持 `NOT_AVAILABLE`；
- 来源或时间边界、规则、必要完整性、截点、登记或读取未知支持 `INDETERMINATE`；
- 同键不兼容来源向量、时间向量、截点、评价、视图、候选或登记载荷支持 `CONFLICTED`。

只有已登记 `AVAILABLE` 解析及内容同一候选可以产生可消费的已登记认识边界向量。空查询、缺失记录、超时或读取失败不能产生 `NOT_AVAILABLE`。

### TM-R1-22 映射确定性必须同时受来源与时间账本约束

`MAPPED` 或 `NOT_MAPPABLE` 的可消费性不仅要求映射输入来源完整，还要求该已登记映射记录位于所引用时间治理边界中，且该边界的查询必要完整性为 `COMPLETE`。

映射候选可以先于时间账本边界构造，但在进入已登记 `AVAILABLE` 认识边界前不能支持历史确定结论。遗漏、未登记、越界或冲突映射必须分别产生 `INDETERMINATE` 或 `CONFLICTED`，不得按 `MAPPED_AT` 选赢家。

## 八、非法状态与闭合声明

### TM-R1-23 新增非法状态必须失败关闭

- 重新抽取或修改来源侧已登记原始时间断言；
- 把所有完整性维度无条件设为每类查询的必要门槛；
- 在开放世界中从精确已知集合推导穷尽缺失；
- 用单一时间戳或显示标签替代认识边界向量；
- 历史视图不固定时间映射、更正和迁移账本边界；
- 时间派生账本或向量自证完整；
- 映射输入引用正在构造的认识边界；
- 后续时间记录回写旧时间治理边界或认识边界；
- 查询坐标视图与认识边界视图不一致；
- 未登记或内容不一查询坐标被来源适用性消费。

### TM-R1-24 本修订只声明候选级阻断关闭

```text
B1 Temporal-side Raw Assertion Consumption: CLOSED_AS_DRAFT
B2 Query-specific Completeness Compatibility: CLOSED_AS_DRAFT
B3 Knowledge-time Type Closure: CLOSED_AS_DRAFT
B4 Temporal-ledger Historical Boundary: CLOSED_AS_DRAFT
B5 Coordinate Content Identity: CLOSED_AS_DRAFT
Source / Temporal Acyclicity Regression: NONE_FOUND
Cross-interface Re-review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006-R1 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: B1 + B2 + B3 + B4 + B5 only
Cross-interface Re-review with CR-0005-R1: REQUIRED
Independent Model Review: BLOCKED_PENDING_CROSS_REVIEW
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Temporal Ledger: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须与 `CR-0005-R1` 一起接受交叉接口复审。自检、文件存在或规则编号完整都不能独立证明五项阻断已经关闭。
