# 时间映射治理提案

## 提案信息

```text
Proposal ID: CR-0006
Title: Temporal Mapping Governance
Workstream: WS-03
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: SINGLE_PURPOSE_GOVERNANCE_MODEL
Planning Basis: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Interface Baseline: CR-0004-CONSTITUTION-CANDIDATE-R1
Interface Baseline Review: CR-0004-CONSTITUTION-CANDIDATE-R1-CONSISTENCY-REVIEW
Parallel Interface Target: CR-0005 SOURCE REGISTRY INTERFACE
Proposal Author: Codex
Proposal Authority: User-delegated drafting authority
Cross-interface Review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Temporal Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件是时间映射治理的独立提案，不是冻结制度，也不是系统时钟或运行时时间服务。它不能创建来源事实、重写历史、决定合法性、产生提交结果或授予任何行动权威。

## 一、单一目的与边界

### TM-C-01 本提案只有一个制度目的

本提案只定义：

> 不同时间字段如何以规范身份保持不可互换，旧字段如何在证据约束下映射为规范时间，以及有效时间、登记时间和认识边界如何形成可审计双时间查询坐标。

### TM-C-02 时间映射只解释时间字段

时间映射可以建立：

- 字段的规范语义类别；
- 原始时间值到规范时间值或区间的可证映射；
- 映射规则、版本、证据、精度和不确定性；
- 历史认识与当前重述的边界；
- 时间更正和迁移历史。

时间映射不得建立：

- 事件、决定、提交、审查或来源事实本身；
- 资格、适用性、合法性或提交结论；
- 来源注册表完整性；
- 制度冻结资格；
- 消费者行动权威。

### TM-C-03 当前知识不得重写历史当时知识

```text
New Temporal Evidence
  -> may create new Mapping Resolution
  -> may create CURRENT_RESTATED view
  -/-> rewrite HISTORICAL_AS_KNOWN view
```

## 二、规范时间对象

### TM-C-04 时间对象必须分层

| 对象 | 类型 | 唯一目的 | 逻辑真源 |
|---|---|---|---|
| `Canonical Temporal Field Registry` | 制度注册表 | 保存规范时间字段定义 | 时间字段登记权威 |
| `Canonical Temporal Field Definition` | 不可变制度记录 | 定义一个字段的语义 | 时间字段注册表 |
| `Raw Temporal Assertion` | 不可变观察 | 保存来源提供的原始时间声明 | 来源或证据载体 |
| `Canonical Temporal Value` | 规范值对象 | 表达一个确定时点或区间 | 已登记映射或规范来源 |
| `Temporal Precision` | 枚举值 | 表达值的精度 | 时间值契约 |
| `Temporal Uncertainty Interval` | 区间值 | 表达不可消除的不确定范围 | 映射记录 |
| `Temporal Mapping Rule` | 版本化制度契约 | 定义允许的字段映射 | 时间映射制度 |
| `Temporal Mapping Record` | 派生登记记录 | 保存一次字段映射结果 | 映射解析账本 |
| `Temporal Query Coordinate` | 复合值对象 | 绑定有效时点、认识边界和视图 | 查询接口 |
| `Knowledge Boundary Vector` | 复合边界值 | 固定各来源注册表的可消费认识截点 | 时间边界账本 |
| `Temporal Correction Record` | 非语义更正 | 修复时间表示缺陷 | 时间更正账本 |
| `Temporal Migration Record` | 迁移记录 | 保存旧时间契约到新契约的演进 | 时间迁移账本 |
| `Temporal View Mode` | 封闭枚举 | 区分历史认识和当前重述 | 时间查询契约 |

### TM-C-05 时间字段身份和值必须分离

```text
Temporal Field ID != Temporal Field Version
Temporal Field Version != Raw Temporal Assertion
Raw Temporal Assertion != Canonical Temporal Value
Canonical Temporal Value != System Clock Reading
Mapping Rule Version != Mapping Result
```

相同字面时间戳不证明字段语义相同。

## 三、规范时间字段注册表

### TM-C-06 每个规范字段必须拥有稳定身份

```text
Canonical Temporal Field Key =
  Temporal Field Registry ID
+ Temporal Field ID
+ Temporal Field Version
```

字段定义至少固定：

```text
Semantic Category
Allowed Subject Types
Allowed Source Types
Value Shape
Clock Scale
Timezone Contract
Precision Contract
Uncertainty Contract
Inclusivity and Exclusivity Rules
Null and NOT_APPLICABLE Rules
Mapping Eligibility Rules
Correction Rules
Authority and Evidence References
Institution Freeze Reference
```

### TM-C-07 最低规范字段必须不可互换

```text
VALID_AT
VALID_FROM
VALID_UNTIL
OBSERVED_AT
RECORDED_AT
REVIEWED_AT
DECIDED_AT
COMMITTED_AT
MAPPED_AT
CORRECTED_AT
SYSTEM_CLOCK_READING_AT
```

字段名称相似、值相等或来自同一时钟都不能建立语义等价。

### TM-C-08 字段类别必须封闭

```text
VALID_TIME
EVENT_OBSERVATION_TIME
TRANSACTION_TIME
REVIEW_ACT_TIME
DECISION_ACT_TIME
COMMIT_TIME
MAPPING_TIME
CORRECTION_TIME
SYSTEM_TIME
```

字段定义必须精确属于一个主要类别；复合时间必须由多个字段组成，不能创建含混的“通用时间”。

### TM-C-09 字段定义演进必须版本化

语义类别、精度、时区、区间边界、允许来源或映射资格变化时必须产生新字段版本和迁移记录。不得原地修改定义并追溯解释旧值。

## 四、权威与分权

### TM-C-10 时间治理必须分离权威

```text
Temporal Field Definition Authority Type
Temporal Field Registration Authority Type
Temporal Mapping Rule Definition Authority Type
Temporal Mapping Rule Registration Authority Type
Temporal Mapping Execution Authority Type
Temporal Mapping Registration Authority Type
Temporal Query Resolution Authority Type
Knowledge Boundary Construction Authority Type
Knowledge Boundary Registration Authority Type
Temporal Correction Qualification Authority Type
Temporal Correction Registration Authority Type
Temporal Migration Decision Authority Type
Temporal Migration Registration Authority Type
```

### TM-C-11 权威不得隐式传播

字段定义者不能登记自身定义；映射规则制定者不能执行或登记映射；映射执行者不能创建来源事实；认识边界构造者不能证明来源注册表完整；更正权威不能修改原始时间事实；迁移权威不能建立业务结论。

### TM-C-12 授权实例必须完整边界化

```text
Authority Grant ID
Authority Type
Holder ID
Allowed Temporal Field IDs and Versions
Allowed Subject and Source Types
Allowed Input Registry and Snapshot IDs
Allowed Output Record Types
Allowed Rule Versions
Effective At and Expires At
Can Change
Cannot Change
Granting Authority Reference
Revocation and Supersession References
Evidence References
```

## 五、规范时间值

### TM-C-13 规范时间值必须携带解释上下文

```text
Canonical Temporal Value ID
Canonical Temporal Field ID and Version
Subject ID and Version
Instant or Interval
Clock Scale
Timezone or UTC Normalization
Precision
Uncertainty Interval
Leap-second and Calendar Contract
Source Assertion References
Mapping Record Reference or NATIVE_CANONICAL
Value Digest
```

没有字段身份和解释上下文的裸时间戳不能成为规范时间值。

### TM-C-14 区间边界必须显式

```text
Inclusive Start
Exclusive End
```

除非字段契约另有冻结定义，有效区间默认采用半开区间。未知终点必须显式为 `UNBOUNDED` 或 `INDETERMINATE`，不得用当前时间或最大值补齐。

### TM-C-15 精度和不确定性不得伪装为确定时点

日期、分钟级时间或带测量误差的观察必须保留精度和不确定区间。映射不得通过填零、默认时区或取区间中点提高确定性。

### TM-C-16 系统时间只是观察来源

```text
System Clock Reading
  -> may support RECORDED_AT or MAPPED_AT evidence
  -/-> prove VALID_AT, OBSERVED_AT, REVIEWED_AT, DECIDED_AT or COMMITTED_AT
```

时钟漂移、同步状态、时区和精度必须作为证据保存。

## 六、有效时间、登记时间和认识时间

### TM-C-17 有效时间表达现实适用坐标

`VALID_AT`、`VALID_FROM` 和 `VALID_UNTIL` 只表达事实或规则在所声明现实中的适用坐标，不表达何时被系统观察或登记。

### TM-C-18 登记时间表达权威载体追加坐标

`RECORDED_AT` 只表达记录进入指定权威载体的时间。它不证明事件在该时点发生，也不证明系统在此前不知情。

### TM-C-19 观察、审查、决定和提交时间必须分离

```text
OBSERVED_AT -> observation act or evidence observation
REVIEWED_AT -> review act
DECIDED_AT -> decision act
COMMITTED_AT -> protected authoritative commit
```

四者不得互相默认映射。一次流程可以拥有多个不同字段和值。

### TM-C-20 认识时间必须由来源边界表达

`Known At` 不是单一墙钟时间戳。规范认识边界必须绑定每个来源注册表的精确已登记边界和快照。

```text
Knowledge Boundary Vector
  = Registered Multi-registry Source Boundary Vector Reference
  + Canonical Known At Value
  + Per-registry Recorded-at Cutoffs
  + Required Snapshot and Completeness References
  + Temporal View Mode
  + Vector Rule Version
  + Vector Digest
```

### TM-C-21 双时间查询坐标必须稳定

```text
Temporal Query Coordinate Key =
  Valid At Canonical Temporal Value ID and Digest
+ Knowledge Boundary Vector ID and Digest
+ Temporal View Mode
+ Temporal Query Rule Version
```

有效时间、认识边界、视图或规则变化必须形成新查询坐标。

## 七、来源注册表接口

### TM-C-22 认识边界只能消费已登记来源向量

```text
Registered Multi-registry Source Boundary Vector from WS-02
  -> Candidate Knowledge Boundary Vector
  -> Knowledge Boundary Registration Attempt
  -> Registered Knowledge Boundary Vector
```

时间治理不能构造不存在的来源边界，也不能把向量摘要当作来源完整性证明。

### TM-C-23 每个来源边界必须独立验证时间可消费性

每个向量条目至少绑定：

```text
Source Registry ID and Version
Source Boundary and Snapshot IDs and Digests
Registered Boundary Completeness Records
Recorded Temporal Field Definition
Maximum Consumable Recorded-at Value or Exact Record Set
Temporal Mapping References when needed
Entry Digest
```

任一边界完整性非 `COMPLETE`、记录时间未规范化或来源冲突时，相关认识边界不得产生确定结果。

### TM-C-24 来源向量和认识向量不得循环

```text
WS-02 Multi-registry Source Boundary Vector
  -/-> Knowledge Boundary Vector
  -/-> Temporal Mapping Result

WS-03 Knowledge Boundary Vector
  -> references WS-02 vector
  -/-> mutate WS-02 vector or source records
```

## 八、视图模式

### TM-C-25 时间视图模式必须封闭

```text
HISTORICAL_AS_KNOWN
CURRENT_RESTATED
```

`HISTORICAL_AS_KNOWN` 只消费 `Recorded At <= Known At` 且在 `Valid At` 适用的记录。`CURRENT_RESTATED` 可以消费当前完整认识边界中的后续映射、更正和冲突，但必须形成独立投影。

### TM-C-26 相邻模型视图名称必须显式兼容

兼容别名只能由版本化接口契约建立：

```text
CR-0003 HISTORICAL_KNOWLEDGE_VIEW
  -> HISTORICAL_AS_KNOWN

CR-0003 CURRENT_RESTATEMENT_VIEW
  -> CURRENT_RESTATED
```

别名只映射名称，不改变有效时间、认识边界、来源集合或投影身份。

### TM-C-27 当前重述不能伪装成历史认识

任何当前重述必须绑定新的查询坐标、当前来源向量、使用的后续映射和更正，并明确标记 `CURRENT_RESTATED`。不得覆盖历史投影或复用历史投影摘要。

## 九、时间映射规则

### TM-C-28 每项映射规则必须拥有稳定身份

```text
Temporal Mapping Rule Key =
  Mapping Rule ID
+ Mapping Rule Version
+ Source Temporal Field ID and Version
+ Target Canonical Temporal Field ID and Version
+ Subject Type
+ Semantic Domain
```

规则至少声明允许来源、前置证据、转换算法、时区、精度、不确定性、失败值、冲突规则、禁止推断和制度冻结引用。

### TM-C-29 映射输入必须不可变

```text
Temporal Mapping Input Record
  = Raw Temporal Assertion ID and Digest
  + Source Registry Snapshot and Boundary References
  + Source Boundary Completeness References
  + Subject ID and Version
  + Source Field Identity
  + Target Field Identity
  + Mapping Rule Reference
  + Supporting Evidence Set Digest
```

输入不得包含当前映射候选、映射结果或映射账本边界。

### TM-C-30 映射解析必须拥有稳定键

```text
Temporal Mapping Resolution Key =
  Temporal Mapping Input Record ID and Digest
+ Source Registry Boundary Vector Digest
+ Mapping Rule ID and Version
+ Target Canonical Temporal Field ID and Version
+ Mapping Resolution Rule Version
```

不同来源边界、规则、目标字段或输入必须形成新解析身份。

### TM-C-31 映射必须形成候选—登记链

```text
Temporal Mapping Input Record
  -> Candidate Temporal Mapping Record
  -> Temporal Mapping Registration Attempt
  -> Registered Temporal Mapping Record
```

候选和登记记录至少共同绑定映射键、输入、规则、输出值或区间、精度、不确定性、证据、执行和登记权威、候选与登记摘要、解析和登记时间。

```text
Candidate Temporal Mapping Payload Digest
= Registered Temporal Mapping Payload Digest
```

### TM-C-32 映射结果使用完整四值

```text
MAPPED(Canonical Temporal Value)
NOT_MAPPABLE(Qualified Reason)
INDETERMINATE
CONFLICTED(Conflicting Mapping References)
```

- 唯一规则、充分证据、完整来源和唯一规范值支持 `MAPPED`；
- 合格、适用、完整的不可映射证明支持 `NOT_MAPPABLE`；
- 来源、规则、证据、精度或边界未知支持 `INDETERMINATE`；
- 多个可比较不兼容值、规则或登记载荷支持 `CONFLICTED`。

缺失、空值、超时、解析错误或默认值不能产生 `NOT_MAPPABLE` 或 `MAPPED`。

### TM-C-33 映射置信度不得提升确定性

置信度只是证据注释，不能把 `INDETERMINATE` 提升为 `MAPPED`，不能在冲突映射中选赢家，也不能缩小没有证据支持的不确定区间。

### TM-C-34 映射规则前向解释不得放大语义

新规则可以在冻结兼容契约允许时重申相同规范值或降低为不确定。产生不同值、缩小区间或提高精度必须形成新的映射输入、候选和登记历史。

## 十、旧字段映射

### TM-C-35 旧字段必须逐字段映射

一个旧的复合时间戳不能同时填充多个规范字段，除非每个目标字段都有独立规则、证据和已登记映射。

```text
Legacy Field
  -> one Candidate Mapping per Target Field
  -> one Registered Mapping per Target Field
```

### TM-C-36 Review As Of 不等于认识边界

```text
Review As Of
  -/-> Knowledge Boundary Vector
```

只有能够重建精确多注册表边界、快照、完整性和每来源登记截点时，旧字段才能作为认识边界证据之一；单一时间戳不能替代向量。

### TM-C-37 Reviewed At 只在有证据时映射审查行为

```text
Reviewed At
  -> REVIEWED_AT only when source contract proves review-act time
  -/-> RECORDED_AT
  -/-> Knowledge Boundary Vector
  -/-> VALID_AT
```

### TM-C-38 旧系统时间不得冒充现实时间

`Created At`、`Updated At`、文件修改时间、提交时间或数据库默认时间只在精确来源契约支持时映射到 `RECORDED_AT` 或 `SYSTEM_CLOCK_READING_AT`。它们不得默认映射为观察、审查、决定、提交或有效时间。

## 十一、更正与迁移

### TM-C-39 时间更正只能修复表示缺陷

允许更正时区标签、格式、编码、精度标注或明确的抄录错误。不得通过更正改变原始事件、观察、审查、决定、提交或有效时间语义。

### TM-C-40 时间更正必须追加双时间历史

```text
Temporal Correction Key =
  Original Temporal Record ID and Digest
+ Corrected Field Set Digest
+ Correction Request ID
+ Correction Effective Temporal Reference
```

更正必须形成资格、候选、登记尝试和内容同一记录，并分别保存更正适用时间、观察时间、登记时间和进入认识边界的时间。

### TM-C-41 时间迁移必须版本化且可回放

```text
Temporal Migration Key =
  Source Temporal Contract ID and Version
+ Target Temporal Contract ID and Version
+ Migration Decision ID
+ Migration Scope Digest
```

迁移不得覆盖旧映射。历史查询继续使用当时规则和认识边界；当前重述使用新规则时必须生成新映射和投影身份。

### TM-C-42 映射冲突不能由迁移静默消除

迁移发现旧值与新值不兼容时必须登记冲突谱系。只有新的权威决定和充分证据可以建立后续映射；旧冲突记录永久保留。

## 十二、规范因果路径

### TM-C-43 规范来源时间路径

```text
Canonical Field Definition
  -> Native Canonical Temporal Assertion
  -> Registered Source Record in WS-02
  -> Registered Source Boundary and Snapshot
  -> Registered Knowledge Boundary Vector
  -> Temporal Query Coordinate
```

### TM-C-44 旧字段映射路径

```text
Raw Legacy Temporal Assertion
+ Registered WS-02 Source Boundary and Snapshot
+ Mapping Rule
+ Evidence
  -> Temporal Mapping Input Record
  -> Candidate Temporal Mapping Record
  -> Registered Temporal Mapping Record
  -> Canonical Temporal Value
  -> Knowledge Boundary or Query Coordinate when eligible
```

### TM-C-45 当前重述路径

```text
Historical Mapping and Projection
+ Later Evidence, Mapping, Correction or Conflict
  -> New Registered Mapping History
  -> New CURRENT_RESTATED Query Coordinate
  -> New Rebuildable Projection
  -/-> overwrite historical view
```

## 十三、非法状态候选

### TM-C-46 以下状态必须失败关闭

- 使用裸时间戳而不绑定规范字段身份；
- 把 `VALID_AT`、`OBSERVED_AT`、`RECORDED_AT`、`REVIEWED_AT`、`DECIDED_AT` 或 `COMMITTED_AT` 互换；
- 用系统当前时间填充缺失业务时间；
- 用默认时区、填零或区间中点提高确定性；
- 用单一 `Known At` 时间戳替代多注册表认识边界；
- 认识边界引用未登记或不完整来源快照；
- 映射输入引用当前映射结果或映射账本边界；
- 候选或未登记映射被消费；
- 置信度选择冲突赢家；
- `Review As Of` 直接映射认识边界；
- `Reviewed At` 默认映射记录时间或有效时间；
- 更正或迁移覆盖旧时间事实；
- 当前重述复用或覆盖历史投影身份；
- 时间映射创建来源、资格、合法性、提交或冻结事实。

## 十四、接口与退出准备度

### TM-C-47 WS-01 冻结引用接口兼容

本提案为 `CR-0004-R1` 的 `Valid At`、`Known At`、`View Mode` 和 `Institution Resolution Boundary Vector` 提供规范时间值、双视图和认识边界接口，但不创建冻结引用或决定其资格。

```text
WS-01 Reference Compatibility: PASS_AS_DRAFT
```

### TM-C-48 CR-0002 与 CR-0003 消费接口兼容

本提案提供：

```text
Temporal Query Coordinate
Knowledge Boundary Vector
Observed At / Recorded At / Reviewed At Separation
Legality Review Temporal Mapping Contract shape
HISTORICAL_AS_KNOWN / CURRENT_RESTATED
CR-0003 View-mode Alias Mapping
```

时间接口不取得决策、提交、资格、证明、闭包或投影权威。

```text
CR-0002 Interface Compatibility: PASS_AS_DRAFT
CR-0003 Interface Compatibility: PASS_AS_DRAFT
```

### TM-C-49 WS-02 无环兼容

本提案只消费 `CR-0005` 已登记的非时间化来源边界向量，构造认识边界后只返回引用。它不能改变来源向量、快照或完整性。

```text
WS-02 Cross-interface Compatibility: PASS_AS_DRAFT
```

## 十五、提案自检

```text
Single Purpose: PASS
Canonical Time Separation: PASS_AS_DRAFT
Bitemporal Append-only Semantics: PASS_AS_DRAFT
Canonical Field Registry: PASS_AS_DRAFT
Legacy Mapping Determinism: PASS_AS_DRAFT
Mapping Four-value Failure Closure: PASS_AS_DRAFT
Historical Knowledge Boundary: PASS_AS_DRAFT
Current Restatement Separation: PASS_AS_DRAFT
Temporal Correction and Migration: PASS_AS_DRAFT
WS-01 Reference Compatibility: PASS_AS_DRAFT
WS-02 Interface Acyclicity: PASS_AS_DRAFT
Cross-interface Review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0006 Status: DRAFT
Authority: NONE
Executable: NO
Workstream: WS-03
Cross-interface Review with CR-0005: REQUIRED
Independent Model Review: REQUIRED
WS-03 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Temporal Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须先与 `CR-0005` 执行交叉接口检查，再进入独立模型审查。任何通过结论都不能由本提案自检产生。
