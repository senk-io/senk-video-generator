# 来源注册表接口有界修订 R3

## 修订信息

```text
Proposal ID: CR-0005-R3
Title: Four-value Coordinate Subject Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R2 COORDINATE REGISTRATION RESOLUTION PINNING
Repair Basis: CR-0005-R2-CR-0006-R2-FINAL-CROSS-INTERFACE-REVIEW
Repair Scope: F1 + F2 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Parallel Interface Baseline: CR-0006-R2
Terminal Cross-interface Re-review Required: YES
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

> 本文件只修复终局交叉接口复审的 F1 与 F2。它不覆盖 `CR-0005`、R1、R2、`CR-0006-R2` 或复审记录的历史文本，不创建查询坐标、登记解析、来源记录、注册表、账本、制度冻结或运行时权威。

## 一、修订解释边界

### SR-R3-01 R3 只修正四值消费主体

本修订只覆盖 `CR-0005-R2` 的 `SR-R2-03`、`SR-R2-04`、`SR-R2-05`、`SR-R2-06`、`SR-R2-07`、`SR-R2-08`、`SR-R2-10`、`SR-R2-12`、`SR-R2-13` 及当前状态中与下列事项冲突的部分：

```text
F1 Undefined Coordinate-resolution Ledger Boundary
F2 Four-value Coordinate Subject Reference Totality
```

未被本修订显式覆盖的 `CR-0005`、R1 与 R2 规则继续作为合并候选语义。`CR-0006-R2` 不需要修订。

### SR-R3-02 R3 保持解析固定和历史分离

本修订不得改变：

```text
Coordinate Registration Resolution ID and Digest in Source Applicability identity
RR0 and RR1 create distinct Source Applicability identities
Known At := Registered Knowledge Boundary Vector ID and Digest
Registered Raw Temporal Assertion handoff
OPEN_WORLD qualified-absence prohibition
B -> temporal records -> T -> K -> Q -> RR -> Source Applicability causality
```

R3 只改变四值共有主体的表达方式，不降低任何 `REGISTERED` 资格或内容同一要求。

## 二、F1：删除未定义解析账本边界要求

### SR-R3-03 消费方只能验证提供方已经定义的解析链

以本规则覆盖 `SR-R2-04` 中“登记解析自身位于解析账本边界”的要求。来源侧必须验证：

```text
Candidate Coordinate Registration Resolution
  -> Coordinate Resolution Registration Attempt
  -> Registered Temporal Query Coordinate Registration Resolution

Candidate Resolution Payload Digest
= Registered Resolution Payload Digest

Resolution.Coordinate Registry Boundary ID and Digest
= consumed Coordinate Registry Boundary ID and Digest

Resolution.Required Registry Completeness Resolution IDs and Digests
= consumed Registry Completeness Resolution IDs and Digests
```

来源侧不得要求或假定：

```text
Coordinate Registration Resolution Ledger Boundary
Coordinate Resolution Ledger Boundary Key
Coordinate Resolution Ledger Completeness Resolution
```

这些对象未由 `CR-0006-R2` 定义，也不是验证已登记解析所必需。坐标注册表边界是解析输入，不能同时包含依赖它形成的解析。

### SR-R3-04 解析注册事实与坐标注册边界不得互换

```text
Registered Coordinate Registration Resolution
  != Coordinate Registry Boundary
  != Coordinate Registry Completeness Resolution
  != Registered Temporal Query Coordinate
```

解析注册事实由其候选—尝试—内容同一登记链证明；坐标注册边界及完整性只证明解析输入集合可重放。任何一项都不能替代另一项。

## 三、F2：四值共有查询坐标主体

### SR-R3-05 查询坐标解析主体必须使用封闭状态

新增消费值对象：

```text
Temporal Query Coordinate Subject Reference
```

主体状态值域：

```text
REGISTERED_SINGLETON
QUALIFIED_NOT_REGISTERED
INDETERMINATE_SUBJECT
CONFLICTED_SUBJECT
```

主体状态只复述精确登记解析的对象状态，不自行改变解析结果。

### SR-R3-06 四值共有主体引用必须拥有稳定结构

```text
Temporal Query Coordinate Subject Reference =
  Temporal Query Coordinate Key
+ Coordinate Subject State
+ Registered Normative Coordinate Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
+ Observed Candidate Normative Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
+ Coordinate Conflict Set Digest or NOT_APPLICABLE or NOT_ESTABLISHED
+ Registered Coordinate Registration Resolution ID and Digest
+ Coordinate Subject Reference Rule Version
```

其中：

- `Temporal Query Coordinate Key` 始终存在，固定有效时间值、认识边界和查询规则；
- 已登记载荷集合与候选载荷集合必须分开，不能用候选存在冒充登记成功；
- `EMPTY_SET` 表示完整边界证明集合为空，`NOT_ESTABLISHED` 表示尚不能建立完整集合，两者不得互换；
- 冲突集合摘要覆盖坐标载荷、登记记录、注册边界或解析载荷冲突；无冲突时使用 `NOT_APPLICABLE`，冲突边界本身未知时使用 `NOT_ESTABLISHED`；
- 精确登记解析 ID 和摘要始终存在，并决定主体状态。

主体引用是消费侧对提供方解析载荷的内容同一投影，不创建第二个坐标或解析身份。

### SR-R3-07 主体状态必须与登记解析四值一一对应

```text
REGISTERED
  -> REGISTERED_SINGLETON

NOT_REGISTERED
  -> QUALIFIED_NOT_REGISTERED

INDETERMINATE
  -> INDETERMINATE_SUBJECT

CONFLICTED
  -> CONFLICTED_SUBJECT
```

不允许跨值映射、默认 `REGISTERED_SINGLETON` 或由来源适用性执行者选择状态。

同一登记解析 ID 和摘要投影出不同主体状态、查询键或载荷集合摘要时必须 `CONFLICTED`。

## 四、四个分支的完整消费契约

### SR-R3-08 REGISTERED 分支必须绑定唯一已登记坐标

```text
Coordinate Subject State = REGISTERED_SINGLETON
Resolution Result = REGISTERED
Registered Normative Coordinate Payload Set Cardinality = 1
Coordinate Conflict Set = NOT_APPLICABLE
```

该分支额外必须绑定：

```text
Registered Temporal Query Coordinate ID and Payload Digest
```

并验证：

```text
Registered Coordinate.Key
= Subject Reference.Temporal Query Coordinate Key

Registered Coordinate.Payload Digest
= the only digest in Subject Reference.Registered Payload Set

Registered Coordinate ID and Digest
= Resolution.Registered Coordinate ID and Digest
```

只有该分支可以支持确定 `APPLICABLE` 或 `INAPPLICABLE`。

### SR-R3-09 NOT_REGISTERED 分支不得伪造坐标

```text
Coordinate Subject State = QUALIFIED_NOT_REGISTERED
Resolution Result = NOT_REGISTERED
Registered Normative Coordinate Payload Set = EMPTY_SET
```

该分支必须绑定查询坐标键、空注册集合证明、已观察候选载荷集合摘要或 `EMPTY_SET`、精确坐标注册边界、必要完整性解析及登记解析 ID 和摘要；不得填写 `Registered Temporal Query Coordinate ID`。

它只能使来源适用性为 `INDETERMINATE`，不能证明来源 `INAPPLICABLE`。

### SR-R3-10 INDETERMINATE 分支必须保留已知与未知边界

```text
Coordinate Subject State = INDETERMINATE_SUBJECT
Resolution Result = INDETERMINATE
```

该分支必须分别绑定已登记载荷集合和已观察候选载荷集合的可用摘要、`EMPTY_SET` 或 `NOT_ESTABLISHED`，并保存未知原因、边界和完整性引用以及登记解析 ID 和摘要。

如果尚不能证明存在唯一已登记坐标，不得填写 `Registered Temporal Query Coordinate ID`。该分支只能产生 `INDETERMINATE` 来源适用性。

### SR-R3-11 CONFLICTED 分支必须保留全部可用冲突谱系

```text
Coordinate Subject State = CONFLICTED_SUBJECT
Resolution Result = CONFLICTED
```

该分支必须分别绑定已登记载荷集合、候选载荷集合和坐标冲突集合摘要，并保存全部可用逐候选、逐登记坐标、冲突注册边界、必要完整性及解析载荷冲突引用。如果边界冲突使任一集合不能完整建立，必须使用 `NOT_ESTABLISHED`，不能伪装为空集。

冲突可以来自多个规范载荷，也可以来自同一规范载荷的不兼容登记、边界或解析载荷；因此不得仅按载荷数量决定冲突。不得选择其中一个对象作为唯一 `Registered Temporal Query Coordinate`。该分支必须产生 `CONFLICTED` 来源适用性。

## 五、来源适用性稳定键与最小输出

### SR-R3-12 来源适用性键必须使用四值共有主体引用

以本规则覆盖 `SR-R2-06` 的坐标字段：

```text
Source Applicability Resolution Key =
  Source Identity and Version
+ Exact Registered Change Set Digest
+ Source Lifecycle Boundary ID and Digest
+ Registered Boundary Completeness Record IDs and Digests
+ Temporal Query Coordinate Subject Reference Digest
+ Registered Temporal Query Coordinate Registration Resolution ID and Digest
+ Applicability Rule Version
```

`Registered Temporal Query Coordinate ID and Payload Digest` 只进入 `REGISTERED_SINGLETON` 分支的候选与登记载荷，不作为四值共有键中的强制字段。

主体状态、查询键、载荷集合摘要、登记解析或规则变化必须形成新的来源适用性身份。

### SR-R3-13 最小消费接口必须完整保存主体分支

`Source Applicability Input` 至少绑定：

```text
Source Identity and Version
Applicability Result
Temporal Query Coordinate Subject Reference and Digest
Coordinate Subject State
Registered Temporal Query Coordinate Registration Resolution ID and Digest
Coordinate Registration Resolution Result
Temporal Query Coordinate Key
Registered Normative Coordinate Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Observed Candidate Normative Payload Set Digest or EMPTY_SET or NOT_ESTABLISHED
Coordinate Conflict Set Digest or NOT_APPLICABLE or NOT_ESTABLISHED
Registered Temporal Query Coordinate ID and Payload Digest, REGISTERED_SINGLETON only
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

下游必须整体消费主体引用、登记解析和适用性结果。可选已登记坐标字段缺失只在非 `REGISTERED_SINGLETON` 分支合法；在该分支存在则必须与主体和解析内容同一。

## 六、历史演进、无环与非法状态

### SR-R3-14 解析演进必须以主体引用形成新适用性身份

```text
RR0 = REGISTERED
  -> Subject0 = REGISTERED_SINGLETON
  -> Source Applicability Key includes Subject0 + RR0

RR1 = CONFLICTED
  -> Subject1 = CONFLICTED_SUBJECT
  -> Source Applicability Key includes Subject1 + RR1
```

`Subject0 != Subject1` 且 `RR0 != RR1`。历史成功保留，当前冲突形成新身份；不得把冲突集合压缩回旧单一坐标。

规范因果仍为：

```text
B -> temporal records -> T -> K -> Q
Q -> Coordinate Registry Boundary -> RR
RR -> Subject Reference
Subject Reference + RR -> Source Applicability Resolution
```

主体引用不能反向修改 `Q`、`RR`、坐标注册边界或任何上游对象。

### SR-R3-15 新增非法状态必须失败关闭

- 要求坐标登记解析位于未定义的解析账本边界；
- `NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED` 分支伪造唯一已登记坐标；
- `REGISTERED_SINGLETON` 缺少唯一已登记坐标 ID 和摘要；
- 主体状态与登记解析结果不对应；
- 冲突分支选择一个候选或登记对象作为赢家；
- 未知已登记集合、候选集合或冲突集合被表示为空集合；
- `NOT_REGISTERED` 被解释为来源 `INAPPLICABLE`；
- 主体引用变化却复用旧来源适用性键；
- 下游拆分主体、解析和适用性结果后重新组合。

## 七、闭合声明

### SR-R3-16 本修订只声明候选级 F1/F2 闭合

```text
F1 Undefined Resolution-ledger Boundary: CLOSED_AS_DRAFT
F2 Four-value Subject Reference Totality: CLOSED_AS_DRAFT
Coordinate Resolution Pinning Regression: NONE_FOUND
Historical / Current Applicability Separation Regression: NONE_FOUND
Raw Assertion Interface Regression: NONE_FOUND
Knowledge-time Type Regression: NONE_FOUND
Open-world Absence Safety Regression: NONE_FOUND
Four-stage Acyclicity Regression: NONE_FOUND
Terminal Cross-interface Re-review: REQUIRED
Independent Model Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R3 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: F1 + F2 only
Terminal Cross-interface Re-review with CR-0006-R2: REQUIRED
Independent Model Review: BLOCKED_PENDING_CROSS_REVIEW
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Source Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须使用 `CR-0005-R3 + CR-0006-R2` 执行终局独立交叉接口复审。自检、四个分支均有文字或文件存在不能独立证明接口闭合。
