# 来源注册表接口有界修订 R8

## 修订信息

```text
Proposal ID: CR-0005-R8
Title: Lifecycle Consumption Boundary-context Eligibility Closure
Workstream: WS-02
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0005-R7 QUALIFIED EMPTY REQUIRED-PURPOSE CONSUMPTION CLOSURE
Repair Basis: CR-0005-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: SR-R7-B1 only
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
Compatibility Reference: CR-0006-R7
Compatibility Reference: CR-0004-CONSTITUTION-CANDIDATE-R1
```

> 本文件只修复 `SR-R7-B1`：为生命周期消费建立已登记视图上下文，并证明目的资格聚合覆盖该上下文边界中的全部适用候选。它不覆盖基础稿或 R1 至 R7 的历史正文，不创建注册表、生命周期解析、制度冻结或运行时权威。

## 一、修订边界

### SR-R8-01 R8 只覆盖一个边界上下文阻断

```text
SR-R7-B1 Lifecycle Qualification Boundary-context Eligibility
```

R7 已通过的裸标记退场、共同资格前缀、合格空集和非空跨目的消费继续有效。

### SR-R8-02 视图上下文不能反向创建生命周期记录

```text
Lifecycle Consumption View Context
  -/-> create purpose qualification candidates
  -/-> create cross-purpose aggregates
  -/-> modify lifecycle registry boundary
  -/-> create temporal coordinate truth
```

视图上下文只选择并固定已登记边界，不取得被选择边界的构造、登记或完整性权威。

## 二、生命周期消费视图上下文

### SR-R8-03 视图上下文语义键必须排除候选边界

```text
Lifecycle Consumption View Context Semantic Conflict Set Key =
  Registered Lifecycle Registry Reference Aggregate Registration Resolution ID and Digest
+ Source Applicability Change Conflict Set Key
+ Registered Source Applicability Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Lifecycle View Mode
+ Registered Lifecycle Consumption View Rule Contract Payload Digest
+ View Context Semantic Rule Version
```

`Lifecycle View Mode` 只允许：

```text
HISTORICAL_AS_OF_LIFECYCLE_BOUNDARY
CURRENT_RESTATEMENT_AT_LIFECYCLE_BOUNDARY
```

候选生命周期注册表边界、位置、登记时间、执行者和“最新”不得进入语义键。

### SR-R8-04 视图上下文候选载荷必须完整

```text
Lifecycle Consumption View Context Candidate Payload =
  Lifecycle Consumption View Context Semantic Conflict Set Key
+ Registered Lifecycle Resolution Registry Boundary ID and Digest
+ Required Lifecycle Registry Boundary Completeness Resolution IDs and Digests
+ Boundary Cut Shape and Position Range or Exact Record Set Digest
+ Governed View-selection Evidence Boundary ID and Digest
+ Evidence Boundary Completeness Resolution ID and Digest
+ Candidate View Context Result
+ Candidate Canonicalization Rule Version
```

边界必须属于同一已登记生命周期解析注册表引用，覆盖精确查询主体和变化集合的适用解析记录域。

### SR-R8-05 视图上下文候选必须拥有稳定键

```text
Lifecycle Consumption View Context Candidate Key =
  Lifecycle Consumption View Context Semantic Conflict Set Key
+ Candidate View Context Payload Digest
+ Candidate Identity Rule Version
```

候选 ID 与键一对一且不可复用。不同候选边界继续进入同一视图上下文语义冲突集合。

## 三、视图上下文登记与聚合

### SR-R8-06 候选视图上下文必须登记

```text
Candidate Lifecycle Consumption View Context
  -> View Context Registration Attempt
  -> Registered View Context Candidate Record
  -> Registered View Context Candidate Registration Resolution
```

记录进入已登记生命周期解析注册表的 `LIFECYCLE_CONSUMPTION_VIEW_CONTEXT` 类型子域，并共享该注册表全局位置规则。

候选登记解析键固定候选键、注册表边界、必要完整性和登记规则版本，结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

```text
Lifecycle View Context Candidate Registration Resolution Key =
  Lifecycle Consumption View Context Candidate Key
+ Registered Lifecycle View-context Record Registry Boundary ID and Digest
+ Required View-context Record Completeness Resolution IDs and Digests
+ Candidate Registration Resolution Rule Version
```

### SR-R8-07 视图上下文竞争边界必须完整

```text
Lifecycle Consumption View Context Competing Boundary Key =
  Lifecycle Consumption View Context Semantic Conflict Set Key
+ Registered Lifecycle Resolution Registry Boundary ID and Digest
+ Exact View Context Candidate Registration Resolution Set Digest
+ Required View-context Conflict-subdomain Completeness Resolution IDs and Digests
+ Boundary Rule Version
```

边界覆盖同语义域全部候选边界声称、登记记录、候选解析和冲突谱系。视图选择者和上下文聚合者不能自证该边界完整。

```text
Candidate View Context Competing Boundary
  -> View Context Boundary Registration Attempt
  -> Registered View Context Competing Boundary Record
  -> Registered View Context Boundary Registration Resolution
```

```text
Lifecycle View Context Boundary Registration Resolution Key =
  Lifecycle Consumption View Context Competing Boundary Key
+ Registered View-context Boundary-record Registry Boundary ID and Digest
+ Required Boundary-record Completeness Resolution IDs and Digests
+ Boundary Registration Resolution Rule Version
```

同键异成员集合、异空洞或异冲突子域必须 `CONFLICTED`。

### SR-R8-08 视图上下文聚合必须拥有稳定键

```text
Lifecycle Consumption View Context Aggregate Resolution Key =
  Lifecycle Consumption View Context Semantic Conflict Set Key
+ Registered View Context Competing Boundary Resolution ID and Digest
+ Required View-context Boundary Completeness Resolution IDs and Digests
+ Registered Lifecycle Consumption View Rule Contract Payload Digest
+ View Context Aggregate Rule Version
```

聚合结果为：

```text
SELECTED
NOT_SELECTED
INDETERMINATE
CONFLICTED
```

唯一内容同一候选边界支持 `SELECTED`；完整空集支持 `NOT_SELECTED`；边界或证据未知支持 `INDETERMINATE`；同语义键多个不兼容边界或结果支持 `CONFLICTED`。

### SR-R8-09 视图上下文聚合必须形成外层登记解析

```text
Registered Complete View Context Competing Boundary
  -> Candidate Lifecycle Consumption View Context Aggregate Resolution
  -> View Context Aggregate Registration Attempt
  -> Registered View Context Aggregate Record
  -> Registered View Context Aggregate Registration Resolution
```

外层登记解析键固定聚合键、聚合记录边界、必要完整性和登记规则版本，结果为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

```text
Lifecycle View Context Aggregate Registration Resolution Key =
  Lifecycle Consumption View Context Aggregate Resolution Key
+ Registered View-context Aggregate-record Registry Boundary ID and Digest
+ Required Aggregate-record Completeness Resolution IDs and Digests
+ Aggregate Registration Resolution Rule Version
```

只有外层 `REGISTERED` 且内层 `SELECTED` 可以进入生命周期消费。

## 四、目的资格聚合的边界上下文资格

### SR-R8-10 边界上下文资格必须拥有稳定键

```text
Purpose Qualification Aggregate Boundary-context Eligibility Key =
  Lifecycle Consumption View Context Semantic Conflict Set Key
+ Registered View Context Aggregate Registration Resolution ID and Digest
+ Selected Lifecycle Registry Boundary ID and Digest
+ Registered Required Purpose Aggregate Registration Resolution ID and Digest
+ Lifecycle Required Purpose Qualification Semantic Key
+ Boundary-context Eligibility Rule Version
```

该键固定被消费资格聚合和外层生命周期边界，不能只验证资格聚合自己的历史子边界。

### SR-R8-11 边界上下文资格载荷必须固定全域集合

```text
Purpose Qualification Boundary-context Eligibility Payload =
  Purpose Qualification Aggregate Boundary-context Eligibility Key
+ Exact All Applicable Purpose Qualification Candidate Resolution Set Digest within Selected Boundary
+ Selected Aggregate.Competing Purpose Candidate Resolution Set Digest
+ Candidate-set Equality Proof Digest
+ Selected Boundary Membership Proof Digest
+ Selected Boundary Completeness Resolution IDs and Digests
+ Boundary-context Eligibility Result
+ Eligibility Payload Rule Version
```

“全部适用候选”必须按目的资格语义键、查询主体、变化集合、注册表引用和合同确定，不能由消费方过滤。

### SR-R8-12 边界上下文资格结果必须封闭

```text
ELIGIBLE
NOT_ELIGIBLE
INDETERMINATE
CONFLICTED
```

- 两个候选集合摘要内容同一，全部记录位于已选择完整边界内且上下文一致时支持 `ELIGIBLE`；
- 完整边界证明存在被聚合竞争边界遗漏的适用候选支持 `NOT_ELIGIBLE`；
- 边界、成员、读取、完整性或上下文未知支持 `INDETERMINATE`；
- 同键异集合证明、异边界归属、异资格载荷或异结果支持 `CONFLICTED`。

### SR-R8-13 边界上下文资格随来源适用性登记

资格不是新的生命周期注册表记录，不进入其所验证的已选择边界。它作为来源适用性变化聚合候选的不可变子对象内容同一登记。

```text
Selected Lifecycle Registry Boundary
  -> Boundary-context Eligibility
  -> Source Applicability Change Aggregate Resolution
```

来源适用性登记键固定资格逻辑键；资格载荷和结果保存在候选载荷中。同键异资格结果必须 `CONFLICTED`。

## 五、空目的与非空目的消费再次收紧

### SR-R8-14 所有消费引用必须固定视图上下文

R7 的资格消费前缀新增：

```text
Registered View Context Aggregate Registration Resolution ID and Digest
View Context Registration Result = REGISTERED
View Context Semantic Result = SELECTED
Selected Lifecycle Resolution Registry Boundary ID and Digest
Required Selected-boundary Completeness Resolution IDs and Digests
Purpose Qualification Aggregate Boundary-context Eligibility Key
Boundary-context Eligibility Result = ELIGIBLE
```

### SR-R8-15 空目的分支只接受上下文完整空集

```text
QUALIFIED + EMPTY_SET
+ Boundary-context Eligibility = ELIGIBLE
  -> may form QUALIFIED_EMPTY_REQUIRED_PURPOSES
```

若已选择边界中存在任何未被旧资格聚合覆盖的适用非空候选，旧空资格必须 `NOT_ELIGIBLE` 或 `CONFLICTED`。

### SR-R8-16 非空目的分支必须固定同边界组合解析

非空消费的跨目的聚合及其全部逐目的输入必须位于已选择生命周期注册表边界内，并与同一个必要目的资格聚合内容同一。

边界外组合记录、旧子边界组合或上下文不等不能支持确定来源适用性。

## 六、来源适用性稳定键和历史／当前

### SR-R8-17 来源适用性聚合键必须固定视图和资格逻辑键

R7 的来源适用性变化聚合键由本规则收紧为：

```text
Source Applicability Change Aggregate Resolution Key =
  Source Applicability Change Conflict Set Key
+ Registered Change Set Boundary ID and Digest
+ Registered Temporal Query Coordinate Subject Reference Digest
+ Registered View Context Aggregate Registration Resolution ID and Digest
+ Purpose Qualification Aggregate Boundary-context Eligibility Key
+ Lifecycle Resolution Consumption Reference Key
+ Aggregate Rule Version
```

视图上下文、选择边界、资格逻辑键或消费引用变化必须形成新的聚合身份。资格载荷结果变化在同一逻辑键下必须登记冲突。

### SR-R8-18 历史消费必须显式固定历史边界

`HISTORICAL_AS_OF_LIFECYCLE_BOUNDARY` 只能重放其明确选择的历史边界、目的资格、跨目的聚合和来源适用性结果。

历史边界不能伪装为当前视图，也不能被新边界结果覆盖。

### SR-R8-19 当前重述必须固定新的已选择完整边界

`CURRENT_RESTATEMENT_AT_LIFECYCLE_BOUNDARY` 必须消费该查询上下文下外层 `SELECTED` 的已登记边界。

没有唯一已选择完整边界时必须 `INDETERMINATE` 或 `CONFLICTED`。禁止以登记时间、最大位置或“最新”自行选择边界。

### SR-R8-20 边界扩展必须重新评价资格

边界从 `L1` 扩展到 `L2` 时，必须形成新的视图上下文、边界上下文资格、消费引用和来源适用性身份。

旧 `L1` 聚合仅在历史 `L1` 上可重放；它在 `L2` 下只有重新证明全域候选集合相等才可 `ELIGIBLE`。

当前边界扩展还必须形成新的 `Registered Temporal Query Coordinate Subject Reference`，从而产生新的视图上下文语义键。同一查询主体下同时声称两个不兼容当前边界必须 `CONFLICTED`，不能用任意版本号隔离。

## 七、阶段、权威和非法状态

### SR-R8-21 生命周期消费阶段必须无环

```text
L0 Query Subject and Registered Change Set Boundary
L1 Purpose Qualification / Per-purpose / Cross-purpose Records
L2 Registered Complete Lifecycle Registry Boundary
L3 Registered Lifecycle Consumption View Context
L4 Purpose Qualification Boundary-context Eligibility Subobject
L5 Source Applicability Change Aggregate Resolution
```

`L4`、`L5` 不得反向进入 `L2` 或 `L3` 身份。

### SR-R8-22 新增角色必须逐操作分权

视图候选构造、视图登记、视图边界、视图完整性、视图聚合、边界上下文资格评价、来源适用性聚合和登记权威不得互相传播。

### SR-R8-23 非法状态必须失败关闭

- 视图上下文候选自证生命周期注册表边界完整；
- 候选边界或“最新位置”进入视图语义键；
- 未取得 `REGISTERED + SELECTED` 视图上下文进入消费；
- 旧资格竞争边界遗漏已选择外层边界中的适用候选；
- 只有成员证明而没有全域集合相等证明；
- 当前视图使用历史边界或旧空集；
- 边界上下文资格反向进入被验证生命周期边界；
- `NOT_ELIGIBLE | INDETERMINATE | CONFLICTED` 支持确定来源适用性；
- 候选、自检或文件存在替代已登记视图和资格。

以上状态必须拒绝、`INDETERMINATE` 或 `CONFLICTED`。

## 八、回归与候选级闭合声明

### SR-R8-24 已通过主干不得回归

```text
Bare Marker Retirement: PRESERVED
Qualified Empty / Nonempty Consumption: PRESERVED
Lifecycle Registry Reference Identity: PRESERVED
Required Purpose and Cross-purpose Aggregation: PRESERVED
Source Applicability Change Conflict Set: PRESERVED
Historical / Current Separation: STRENGTHENED
Cross-interface Acyclicity: PRESERVED
```

### SR-R8-25 R8 只声明一个阻断候选闭合

```text
SR-R7-B1 Lifecycle Qualification Boundary-context Eligibility: CLOSED_AS_DRAFT
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
Institution Freeze Eligibility: FAIL
```

## 当前决定

```text
CR-0005-R8 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: SR-R7-B1 only
Independent Model Re-review: REQUIRED
Cross-interface Regression Review: REQUIRED
WS-02 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Lifecycle Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 `CR-0005` 复合模型，并与 `CR-0006-R7` 执行交叉接口回归审查。R8 自检不能独立证明阻断关闭。
