# 资格治理有界修订 R2：资格与适用性重新分离

## 修订信息

```text
Proposal ID: CR-0007-R2
Title: Qualification and Applicability Reseparation
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0007-R1 UPSTREAM CONSUMPTION IDENTITY CLOSURE
Repair Basis: CR-0007-R1-CR-0005-R11-CR-0006-R10-UPSTREAM-CROSS-INTERFACE-REREVIEW
Repair Scope: XQG-R1-B1 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Upstream Cross-interface Re-review Required: YES
Decision and Commit Interface Compatibility Review Required: YES_AFTER_UPSTREAM_PASS
Independent Model Review Required: YES_AFTER_INTERFACE_PASS
Institution Freeze Created: NO
Freeze ID Created: NO
Source Registry Created: NO
Temporal Registry Created: NO
Qualification Registry Created: NO
Qualification Resolution Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Depends On: CR-0005-R11 Source Registry Interface Composite
Depends On: CR-0006-R10 Temporal Mapping Governance Composite
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
```

> 本文件只删除 `CR-0007-R1` 当前资格重述对来源适用性变化和来源当前适用性读面的消费，把当前重述收紧为当前认识边界内的来源内容与非语义更正。它不修改来源生命周期模型，不创建适用性结果，不覆盖 R1 已关闭的其他三项阻断，也不创建资格或冻结事实。

## 一、修订边界

### QG-R2-01 R2 只关闭一个累计接口阻断

```text
XQG-R1-B1 Qualification / Applicability Reabsorption and Lifecycle Aggregate Bypass
```

### QG-R2-02 R2 覆盖 R1 的当前来源读面部分

以下 R1 条款中与当前来源读面相关的部分由 R2 覆盖：

```text
QG-R1-04 Current Source View Consumption Tuple
QG-R1-21 CURRENT_SOURCE_VIEW mode
QG-R1-23
QG-R1-24
QG-R1-25
QG-R1-26
QG-R1-27
QG-R1-28
QG-R1-29
QG-R1-31
QG-R1-32
QG-R1-36
QG-R1-37
QG-R1-38
Current Decision
```

R1 的四值坐标主体、来源完整性聚合元组、`SR-C-16` 只读引用包和历史更正集合规则继续有效。

### QG-R2-03 两个字段永久失去资格输入资格

```text
Current Source View Consumption Tuple
Exact Registered Source Applicability Change Record ID-and-digest Set Digest
```

它们不得保留为别名、可选谱系、证据注释或兼容字段。

## 二、当前重述对象

### QG-R2-04 当前重述只定义内容与更正消费元组

R1 的 `Current Source View Consumption Tuple` 替换为：

```text
Current-restated Source Correction Consumption Tuple
```

唯一目的：

> 固定当前 `B/K/Q` 认识边界内的来源内容和非语义更正集合，使资格可以按当前知识重新计算，但不读取来源生命周期或适用性结果。

### QG-R2-05 来源表示模式保持互斥二选一

```text
HISTORICAL_SOURCE_CORRECTION_SET
CURRENT_RESTATED_SOURCE_CORRECTION_SET
```

`CURRENT_SOURCE_VIEW` 不再是资格表示模式。

## 三、当前重述消费契约

### QG-R2-06 当前重述元组必须固定精确内容与更正谱系

`Current-restated Source Correction Consumption Tuple` 至少绑定：

```text
Temporal View Mode = CURRENT_RESTATED
Qualification Temporal Coordinate Consumption Tuple Digest
Registered Source Boundary Vector B ID and Digest
Exact Registered Source Snapshot IDs and Digests
Exact Registered Source Record ID-and-digest Set
Exact Registered Source Record Set Digest
Exact Registered Source Correction Record ID-and-digest Set
Exact Registered Source Correction Record Set Digest
Exact B-membership Proof for Source Record Set
Exact B/K-membership Proof for Correction Record Set
Qualification Source Completeness Consumption Bundle Digest covering source and correction semantic domains
Source Correction Key and Lineage References
Correction Conflict References or NOT_APPLICABLE
Current-restatement Construction Rule Version
Current-restatement Canonical Byte Contract ID and Version
Current-restatement Digest Algorithm ID and Version
Current-restatement Payload Digest
Current-restatement Lineage Set Equality Proof Reference
Tuple Canonical Digest
```

不得包含来源适用性变化、生命周期评价、来源适用性聚合或“当前可用来源”过滤结果。

### QG-R2-07 当前重述集合必须受当前认识边界限制

```text
Every Source Record
  -> inside exact Registered B

Every Source Correction Record
  -> registered
  -> references a Source Record inside exact B
  -> available inside exact current K/Q knowledge boundary

No later or unbounded record
  -> may enter tuple
```

当前系统时间、最大注册表位置或“最新”不能替代 `B/K/Q`。

### QG-R2-08 当前重述不得改变来源事实或语义字段

只允许消费上游已经判定为非语义更正的 `Source Correction Record`。任何改变来源身份、版本、规范载荷、现实绑定、适用性语义或原始时间事实的记录都不具备当前重述资格。

### QG-R2-09 当前重述完整性必须继续使用 R1 聚合元组包

来源内容和更正两个必要语义域都必须映射到 R1 定义的精确已登记来源完整性聚合元组，并通过集合相等证明。

```text
Any required source or correction tuple != COMPLETE
  -> Current-restated Representation Eligibility = INDETERMINATE
  -> Qualification Outcome = INDETERMINATE
```

当前重述元组不能凭记录数量、查询成功或载荷摘要自证完整。

## 四、资格／适用性严格分离

### QG-R2-10 来源适用性对象不得进入资格稳定身份

以下对象不得进入 `Qualification Resolution Key`、`Qualification Input Package`、候选资格、登记资格或资格重述元组：

```text
Source Applicability Change Record
Source Applicability Change Conflict Set
Registered Source Applicability Change Set Boundary
Source Applicability Change Aggregate Resolution
Post-query Lifecycle View Evaluation
Boundary-context Eligibility
Source Applicability Resolution
Source Applicability Aggregate
Source Applicability Input
```

### QG-R2-11 生命周期变化不得改变资格内容输入

```text
Same Source Record Set
+ Same Source Correction Set
+ Same Qualification Rule and Temporal Coordinate
+ Different Source Applicability History
  -> Same Qualification Source Representation Tuple
  -> Same Qualification Input Identity
```

适用性历史变化必须形成后续适用性身份，不能形成新的资格身份。

### QG-R2-12 当前重述资格不等于当前来源适用性视图

```text
CURRENT_RESTATED_QUALIFICATION
!= CURRENT_SOURCE_APPLICABILITY_VIEW
```

当前重述只回答“按当前认识边界中的内容和非语义更正，主体是否满足资格规则”。它不回答该来源、证明、豁免或资格现在是否可消费。

### QG-R2-13 资格结果和适用性结果保持独立组合

```text
Registered Qualification Resolution
+ independent Registered Source / Proof / Exemption Applicability Resolution
  -> downstream consumption eligibility
```

```text
QUALIFIED + CONFLICTED Applicability
  -> historical Qualification remains QUALIFIED
  -> downstream current use remains CONFLICTED or INDETERMINATE
```

## 五、R2 收紧后的表示元组和输入包

### QG-R2-14 表示消费元组必须按视图模式内容同一

```text
HISTORICAL_AS_KNOWN
  -> Historical Source Correction Consumption Tuple

CURRENT_RESTATED
  -> Current-restated Source Correction Consumption Tuple
```

```text
Representation Tuple.View Mode
= Qualification Temporal Coordinate Consumption Tuple.View Mode
= K.View Mode
= Q.View Mode in REGISTERED_SINGLETON branch
```

### QG-R2-15 表示元组摘要变化边界

只有以下变化可以改变资格来源表示元组摘要：

```text
Source Record Set or Digest
Source Correction Record Set or Digest
Source or Correction Membership Proof
Source Completeness Consumption Bundle
Correction Conflict References
B/K/Q Temporal Consumption Tuple
Current-restatement Construction Rule
Canonical Byte or Digest Contract
```

来源生命周期或适用性对象变化不得改变该摘要。

### QG-R2-16 输入包字段由 R2 收紧

`Qualification Input Package` 的来源表示部分只能是：

```text
Qualification Source Representation Consumption Tuple:
  Historical Source Correction Consumption Tuple
  or Current-restated Source Correction Consumption Tuple

Qualification Source Representation Consumption Tuple Digest
```

R1 其余输入字段继续有效。任何来源适用性字段出现都使输入包不合格。

### QG-R2-17 候选和登记资格必须证明未吸收适用性

候选和登记资格记录除复制表示元组摘要外，还必须绑定：

```text
Source Applicability Input Field Presence = NONE
Source Lifecycle Input Field Presence = NONE
Qualification / Applicability Separation Rule Version
Separation Verification Evidence Reference
```

候选与登记载荷必须内容同一；登记者不能加入当前来源适用性结果。

## 六、反例闭合

### QG-R2-18 生命周期冲突不改变资格反例

```text
Source Record R and Correction Set C unchanged
Qualification(R, C) = QUALIFIED

Lifecycle Candidates = ACTIVE + SUSPENDED
Source Applicability Aggregate = CONFLICTED

Expected:
  Qualification Representation Digest unchanged
  Qualification remains historical QUALIFIED
  Current Applicability = CONFLICTED or INDETERMINATE
```

### QG-R2-19 当前更正改变当前重述反例

```text
Q0/K0 excludes Correction C1
Q1/K1 CURRENT_RESTATED includes registered non-semantic C1

Expected:
  Current-restated Tuple 0 Digest != Tuple 1 Digest
  Qualification Key 0 != Qualification Key 1
  Historical Qualification at Q0 remains unchanged
```

### QG-R2-20 适用性变化但内容不变反例

```text
Applicability A0 = APPLICABLE
Applicability A1 = INAPPLICABLE
Same R/C/B/K/Q qualification-content coordinate

Expected:
  Qualification Input Identity 0 = Qualification Input Identity 1
  Applicability Identity 0 != Applicability Identity 1
```

## 七、非法状态增补

### QG-R2-21 以下状态必须失败关闭

- 当前资格重述消费来源适用性变化记录；
- 当前资格重述消费来源适用性聚合或最小接口；
- 资格输入通过生命周期状态过滤来源；
- 同内容和更正集合仅因适用性变化形成新资格键；
- 当前重述使用未进入 `K/Q` 的更正；
- 语义变化伪装为非语义更正进入当前重述；
- 当前重述摘要自证来源或更正集合完整；
- 当前重述与历史视图模式混用；
- 资格登记者补入来源适用性字段；
- 通过固定完整适用性聚合来保留资格对适用性的依赖。

## 八、候选级闭合声明

### QG-R2-22 R2 只声明新阻断已具备候选修复

```text
XQG-R1-B1 Qualification / Applicability Reseparation: CLOSED_AS_DRAFT
Source Applicability Inputs in Qualification Identity: NONE
Current-restated Content and Correction Boundary: ESTABLISHED_AS_DRAFT
Original XQG-B1 through XQG-B4 Repairs: PRESERVED
B -> T -> K -> Q -> Qualification Direction: PRESERVED
Upstream Cross-interface Re-review: REQUIRED
CR-0002 / CR-0003 Consumer Compatibility Review: BLOCKED_PENDING_UPSTREAM_REVIEW
Independent Qualification Model Review: BLOCKED_PENDING_INTERFACE_REVIEWS
Institution Freeze Eligibility: FAIL
```

该声明只是修订自检，不能替代独立复审。

## 当前决定

```text
CR-0007-R2 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: XQG-R1-B1 only
Proposal Revision Created: YES
Upstream Cross-interface Re-review: REQUIRED
CR-0002 / CR-0003 Consumer Compatibility Review: NOT_READY
Independent Qualification Model Review: NOT_READY
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Qualification Registry: NOT_CREATED
Qualification Resolution: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须使用 `CR-0007 + R1 + R2` 对 `CR-0005-R11 + CR-0006-R10` 再次执行独立上游交叉接口复审。只有残余阻断为零，才能进入决策和提交模型消费接口审查。
