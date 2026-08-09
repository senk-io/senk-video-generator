# 权威适用性治理有界修订 R1：来源适用性消费身份闭合

## 修订信息

```text
Proposal ID: CR-0008-R1
Title: Source Applicability Consumption Identity Closure
Workstream: WS-05
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0008 AUTHORITY APPLICABILITY GOVERNANCE
Repair Basis: CR-0008-CR-0005-R11-CR-0006-R10-UPSTREAM-CROSS-INTERFACE-REVIEW
Repair Scope: XAA-B1 + XAA-B2 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Institution Freeze Created: NO
Runtime Authority Created: NO
```

> 本修订只纠正来源适用性提供方对象身份，不改变适用性结果、规则、决策坐标或消费合同。

## 一、覆盖边界

### AAG-R1-01 删除虚构的上游解析对象

`AAG-C-13` 中：

```text
Boundary-context Eligibility Resolution ID and Digest
```

立即废止。`CR-0008` 不得声明该上游对象存在。

### AAG-R1-02 边界上下文资格按真实子对象消费

消费包必须固定：

```text
Purpose Qualification Aggregate Boundary-context Eligibility Key
Purpose Qualification Boundary-context Eligibility Payload Digest
Boundary-context Eligibility Result
Selected Boundary Membership Proof Digest
Candidate-set Equality Proof Digest
Selected Boundary Completeness Resolution IDs and Digests
```

这些字段作为已登记来源适用性变化聚合的内容同一子对象消费，不建立独立登记或解析权威。

## 二、只读来源适用性消费封装

### AAG-R1-03 消费封装是 WS-05 本地只读对象

```text
Authority Applicability Source Consumption Package
```

只封装提供方已登记事实和证明，不宣称上游创建同名注册表对象。封装构造权威不能创建、修改、登记或解析来源事实。

### AAG-R1-04 消费包必须固定四值主体和来源身份

```text
Source Identity and Version
Source Applicability Change Conflict Set Key
Registered Source Applicability Change Set Boundary ID and Digest
Registered Temporal Query Coordinate Subject Reference ID and Digest
Coordinate Subject State
Coordinate Registration Resolution ID, Digest and Result
Temporal Query Coordinate Key
Registered Knowledge Boundary Vector ID and Digest
Temporal View Mode
```

### AAG-R1-05 消费包必须固定 R8 保留视图身份

```text
Registered View Context Aggregate Registration Resolution ID and Digest
View Context Registration Result = REGISTERED
View Context Semantic Result = SELECTED
Selected Lifecycle Resolution Registry Boundary ID and Digest
Required Selected-boundary Completeness Resolution IDs and Digests
Purpose Qualification Aggregate Boundary-context Eligibility Key
Purpose Qualification Boundary-context Eligibility Payload Digest
Boundary-context Eligibility Result
Lifecycle Resolution Consumption Reference Key and Payload Digest
```

### AAG-R1-06 消费包必须固定 R9 新增评价身份

```text
Registered Post-query Lifecycle View Evaluation Subject Resolution ID and Digest
Selected Target Lifecycle Registry Boundary ID and Digest
Registered Lifecycle Record-type Catalog Aggregate Resolution Set Digest
Post-query View Evaluation Semantic Conflict Set Key
Registered View Evaluation Competing Boundary Registration Resolution ID and Digest
Required Evaluation-boundary Completeness Resolution IDs and Digests
```

### AAG-R1-07 消费包必须固定终局聚合

```text
Source Applicability Change Aggregate Resolution Key
Registered Source Applicability Change Aggregate Resolution ID and Digest
Source Applicability Aggregate Payload Digest
Applicability Result = APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED
Source Registry Snapshot References
Source Boundary Completeness References
Source Applicability and Correction Record References
Evidence References
```

### AAG-R1-08 子对象与聚合必须内容同一

边界上下文资格键、载荷、结果，视图上下文，查询后评价，目标边界，生命周期消费引用和四值来源结果必须与已登记聚合载荷逐字段内容同一。任何不等使消费包无效。

### AAG-R1-09 规范摘要必须覆盖全部累计字段

```text
Authority Applicability Source Consumption Package Digest =
  canonical digest of AAG-R1-04 through AAG-R1-08 fields
```

该摘要进入 `Authority Applicability Input Package`、原子语义键、候选、登记记录、评价边界和消费解析。

### AAG-R1-10 必要来源集合证明保持独立

多个来源消费包仍按 `AAG-C-15/16` 形成必要集合、规范排序、集合相等证明和独立完整性。调用方不能从单一适用来源推断全部必要来源适用。

## 三、失败关闭和回归

### AAG-R1-11 以下状态必须失败关闭

- 使用已废止的虚构边界上下文资格解析 ID；
- 只固定 R9 目标边界而遗漏 R8 视图、资格或生命周期消费身份；
- 从子对象结果反向推断上游登记解析；
- 消费包字段与已登记来源聚合载荷不一致；
- 用终局审查简称替代规范聚合键、解析和载荷；
- 来源生命周期推进覆盖旧消费包；
- 消费包构造取得来源写入、聚合或登记权威。

### AAG-R1-12 已通过接口不得回归

```text
B/T/K/Q/S/RR Consumption: PRESERVED
Four-value Source Applicability: PRESERVED
Historical / Current Separation: PRESERVED
Qualification / Applicability Separation: PRESERVED
CR-0002 Three-value Consumer Contract: UNCHANGED
```

### AAG-R1-13 候选级修复声明

```text
XAA-B1 Boundary-context Eligibility Provider Topology: CLOSED_AS_DRAFT
XAA-B2 Source Applicability Aggregate Identity Pinning: CLOSED_AS_DRAFT
Upstream Cross-interface Re-review: REQUIRED
CR-0002 Consumer Interface Review: BLOCKED_PENDING_UPSTREAM_REREVIEW
Independent Model Review: NOT_READY
```

## 当前决定

```text
CR-0008-R1 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Revision Created: YES
Upstream Cross-interface Re-review: REQUIRED
WS-05 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须复审 `CR-0008 + R1` 与 `CR-0005-R11`／`CR-0006-R10` 的累计上游接口。
