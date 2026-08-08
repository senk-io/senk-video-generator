# 来源注册表接口有界修订 R2

## 修订信息

```text
Proposal ID: CR-0005-R2
Title: Coordinate Registration Resolution Pinning
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R1 RAW TEMPORAL ASSERTION AND COORDINATE CLOSURE
Repair Basis: CR-0005-R1-CR-0006-R2-CROSS-INTERFACE-REVIEW
Repair Scope: R2-B1 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Parallel Interface Baseline: CR-0006-R2
Cross-interface Final Re-review Required: YES
Independent Model Review Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复第二次交叉接口复审的唯一残余阻断 `R2-B1`。它不覆盖 `CR-0005`、`CR-0005-R1`、`CR-0006-R2` 或复审记录的历史文本，不创建来源记录、查询坐标、登记解析、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R2-01 R2 只固定坐标登记解析消费身份

本修订只覆盖 `CR-0005-R1` 的 `SR-R1-10`、`SR-R1-11`、`SR-R1-12`、`SR-R1-13`、`SR-R1-14`、`SR-R1-15`、`SR-R1-16` 及当前状态中与下列事项冲突的部分：

```text
R2-B1 Consumer Coordinate Registration Resolution Pinning
```

未被本修订显式覆盖的 `CR-0005` 与 `CR-0005-R1` 规则继续作为合并候选语义。`CR-0006-R2` 不需要修订。

### SR-R2-02 R2 不改变已通过的来源—时间接口

本修订不得改变：

```text
Registered Raw Temporal Assertion handoff
Known At := Registered Knowledge Boundary Vector ID and Digest
Registered Temporal Query Coordinate whole-coordinate consumption
OPEN_WORLD qualified-absence prohibition
Source Applicability four-value result
B -> temporal records -> T -> K -> Q causality
```

坐标登记解析引用只证明精确坐标在精确完整注册边界中的消费资格，不创建坐标、时间值、来源适用性变化决定或业务资格。

## 二、坐标登记解析的规范消费引用

### SR-R2-03 来源侧必须消费精确坐标登记解析

`CR-0006-R2` 提供的规范消费证明为：

```text
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Resolution Result = REGISTERED
Normative Temporal Query Coordinate ID and Payload Digest
Temporal Query Coordinate Registry Boundary ID and Digest
Required Coordinate Registry Completeness Resolution IDs and Digests
Coordinate Registration Resolution Rule Version
```

来源侧只能验证和引用该解析，不能构造解析、改变结果、替换注册边界或选择另一组完整性记录。

### SR-R2-04 坐标与登记解析必须内容同一

每次来源适用性解析必须验证：

```text
Consumed Temporal Query Coordinate ID
= Coordinate Registration Resolution.Coordinate ID

Consumed Temporal Query Coordinate Payload Digest
= Coordinate Registration Resolution.Normative Coordinate Payload Digest

Coordinate Registration Resolution.Result
= REGISTERED
```

并验证登记解析自身位于其已登记解析账本边界内、候选与登记载荷内容同一、必要坐标注册表完整性均为 `COMPLETE`。

解析引用缺失、未登记、摘要不一致、坐标不一致或结果不是 `REGISTERED` 时，不得把坐标标记为可消费。

### SR-R2-05 登记解析引用不得被旁路证据替代

下列信息均不能替代精确解析 ID 和摘要：

```text
Coordinate ID alone
Coordinate Payload Digest alone
Coordinate Registration Attempt
Coordinate Registry Boundary alone
Evidence References alone
Current Coordinate Lookup Result
Cache Hit or Prior Successful Consumption
```

验证包和证据引用只用于复核已固定解析，不能在稳定键之外选择另一登记历史。

## 三、来源适用性稳定身份修订

### SR-R2-06 来源适用性解析键必须固定坐标登记解析

以本规则覆盖 `SR-R1-10` 的稳定键：

```text
Source Applicability Resolution Key =
  Source Identity and Version
+ Exact Registered Change Set Digest
+ Source Lifecycle Boundary ID and Digest
+ Registered Boundary Completeness Record IDs and Digests
+ Registered Temporal Query Coordinate ID and Payload Digest
+ Registered Temporal Query Coordinate Registration Resolution ID and Digest
+ Applicability Rule Version
```

坐标登记解析 ID 或摘要变化必须形成新的来源适用性解析身份，即使坐标 ID、规范载荷、有效时间、认识边界和适用性规则均未变化。

### SR-R2-07 候选与登记适用性记录必须共同绑定解析谱系

候选和已登记来源适用性解析至少共同绑定：

```text
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Coordinate Registration Resolution Result
Normative Temporal Query Coordinate ID and Payload Digest
Coordinate Registry Boundary ID and Digest
Required Coordinate Registry Completeness Resolution IDs and Digests
Coordinate Resolution Rule Version
Candidate Applicability Payload Digest
Registered Applicability Payload Digest
```

```text
Candidate Applicability Payload Digest
= Registered Applicability Payload Digest
```

来源适用性执行者不能创建坐标登记解析；来源适用性登记者不能修改候选、坐标、登记解析或注册边界。任何授权缺失、冲突、过期或跨域必须失败关闭。

### SR-R2-08 最小消费接口必须输出精确解析引用

以本规则覆盖 `SR-R1-12` 的坐标登记部分。`Source Applicability Input` 至少绑定：

```text
Source Identity and Version
Applicability Result
Registered Temporal Query Coordinate ID and Payload Digest
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Coordinate Registration Resolution Result
Canonical Valid At Value ID and Digest
Registered Knowledge Boundary Vector ID and Digest
Temporal View Mode
Source Registry Snapshot References
Source Boundary Completeness References
Source Applicability and Correction Record References
Applicability Rule Version
Registered Source Applicability Resolution ID and Digest
Evidence References
```

当 `Applicability Result` 为确定 `APPLICABLE` 或 `INAPPLICABLE` 时，`Coordinate Registration Resolution Result` 必须为 `REGISTERED`。当坐标解析为其他值时，最小接口仍必须保留该值和精确解析引用，以输出相应 `INDETERMINATE` 或 `CONFLICTED` 来源适用性；不得丢弃失败记录。

下游必须整体消费坐标与其登记解析，不能只保留坐标 ID、只保留结果字面值或换用当前查询结果。

## 四、登记解析演进与双时间历史

### SR-R2-09 登记解析边界演进必须形成新适用性身份

```text
Coordinate Registration Resolution RR0 = REGISTERED at Boundary CQ0
  -> Source Applicability Resolution Key includes RR0
  -> Historical Source Applicability SA0

Later incompatible coordinate at Boundary CQ1
  -> Coordinate Registration Resolution RR1 = CONFLICTED
  -> RR1 != RR0
  -> new Source Applicability Resolution identity
```

`SA0` 保留在其历史认识视图中，不被 `RR1` 覆盖。当前视图消费 `RR1` 时必须失败关闭，不能复用包含 `RR0` 的适用性身份。

坐标边界变化但规范坐标仍获得新的 `REGISTERED` 解析时，也必须形成新的来源适用性键；内容相同可以在新键下重申结果，但不能把新认识伪装成旧历史。

### SR-R2-10 坐标解析结果必须确定来源适用性失败上限

```text
REGISTERED + content-identical coordinate + complete source inputs
  -> may support APPLICABLE or INAPPLICABLE

NOT_REGISTERED
  -> INDETERMINATE source applicability

INDETERMINATE
  -> INDETERMINATE source applicability

CONFLICTED
  -> CONFLICTED source applicability
```

`NOT_REGISTERED` 只说明坐标没有取得合格登记，不证明来源不适用。任何非 `REGISTERED` 结果都不能支持确定 `APPLICABLE` 或 `INAPPLICABLE`。

同一完整 `Source Applicability Resolution Key` 出现不兼容候选、坐标解析、结果或登记载荷时必须 `CONFLICTED`。

## 五、无环与非法状态

### SR-R2-11 精确解析消费不得引入反向依赖

规范路径为：

```text
B -> temporal records -> T -> K -> Q
Q -> Coordinate Registry Boundary -> Coordinate Registration Resolution RR
Q + RR -> Source Applicability Resolution
```

`RR` 不能进入或修改 `B`、`T`、`K`、`Q` 的身份；来源适用性也不能修改坐标注册表边界或登记解析。后续 `RR1` 只形成新的适用性身份，不回写 `RR0` 或旧适用性记录。

### SR-R2-12 新增非法状态必须失败关闭

- 只凭坐标 ID 或摘要产生确定来源适用性；
- 以证据引用代替精确坐标登记解析 ID 和摘要；
- 坐标与登记解析指向不同规范载荷；
- `NOT_REGISTERED` 被解释为来源 `INAPPLICABLE`；
- `INDETERMINATE` 或 `CONFLICTED` 坐标解析支持确定适用性；
- 坐标登记解析变化却复用旧来源适用性键；
- 当前冲突覆盖历史 `REGISTERED` 解析或历史适用性；
- 来源侧构造、修改或重新登记坐标解析；
- 下游拆分坐标与解析后换用当前查询结果。

## 六、闭合声明

### SR-R2-13 本修订只声明候选级残余阻断关闭

```text
R2-B1 Consumer Coordinate Resolution Pinning: CLOSED_AS_DRAFT
Coordinate / Resolution Content Identity: CLOSED_AS_DRAFT
Historical / Current Applicability Identity Separation: CLOSED_AS_DRAFT
Raw Assertion Interface Regression: NONE_FOUND
Knowledge-time Type Regression: NONE_FOUND
Open-world Absence Safety Regression: NONE_FOUND
Four-stage Acyclicity Regression: NONE_FOUND
Cross-interface Final Re-review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R2 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R2-B1 only
Cross-interface Final Re-review with CR-0006-R2: REQUIRED
Independent Model Review: BLOCKED_PENDING_CROSS_REVIEW
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须使用 `CR-0005-R2 + CR-0006-R2` 执行最终独立交叉接口复审。自检、文件存在或单次 `REGISTERED` 查询不能独立证明接口已经闭合。
