# 依赖闭包治理有界修订 R1：精确传播事实接口闭合

## 修订信息

```text
Proposal ID: CR-0011-R1
Title: Exact Propagation Fact Interface Closure
Workstream: WS-08
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0011 DEPENDENCY CLOSURE GOVERNANCE
Repair Basis: CR-0011-PROVIDER-AND-CONSUMER-INTERFACE-REVIEW
Repair Scope: XDC-B1 only
```

### DCG-R1-01 泛化传播事实名称废止

`Committed Applicability Change Fact` 不得作为可直接消费类型。

### DCG-R1-02 类型化传播事实导入元组

```text
Propagation Fact Import Tuple =
  Provider Workstream and Composite Version
+ Exact Provider Fact Type ID and Version
+ Formal Fact Record ID, Version and Payload Digest
+ Fact Stable Key
+ Fact Scope and Effective Coordinate
+ Commit Key and Commit Attempt ID
+ Registered Commit Resolution ID and Digest
+ Commit Resolution Outcome = COMMITTED
+ Authoritative Registry and Boundary References
+ Evidence and Institution References
+ Import Tuple Digest
```

### DCG-R1-03 允许传播事实类型必须封闭登记

初始允许：

```text
Committed Invalidation Decision Fact
Committed Provider-specific Applicability Change Fact explicitly imported
Registered Correction whose applicability-changing decision fact is COMMITTED
```

每种类型必须拥有精确提供方合同，不能靠父类型或字符串匹配。

### DCG-R1-04 普通记录明确排除

```text
Candidate Applicability Change
Registered Applicability Resolution without committed change fact
Applicability Projection
Source Applicability Aggregate alone
Review or Suspicion Record
Missing Source Observation
```

以上均不能进入传播输入边界。

### DCG-R1-05 导入必须内容同一登记

导入候选、尝试和登记载荷摘要相等，并进入同事实键完整竞争边界和独立完整性。提供方事实、提交解析或作用域不一致必须 `CONFLICTED`。

### DCG-R1-06 传播输入边界固定精确事实集

固定允许类型合同、全部登记导入解析、事实集合摘要、作用域成员证明、提交结果证明、排除集合、冲突集合和集合相等证明。

### DCG-R1-07 传播输入边界不执行传播

边界登记只证明哪些已提交事实可作为下游传播输入，不创建传播执行、失效决定、重建结果或投影发布。

### DCG-R1-08 候选级关闭声明

```text
XDC-B1 Exact Propagation Trigger Provider Identity: CLOSED_AS_DRAFT
Interface Re-review: REQUIRED
Independent Model Review: BLOCKED_PENDING_INTERFACE
```

## 当前决定

```text
CR-0011-R1 Status: DRAFT
Authority: NONE
Executable: NO
WS-08 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行接口复审和独立模型审查。
