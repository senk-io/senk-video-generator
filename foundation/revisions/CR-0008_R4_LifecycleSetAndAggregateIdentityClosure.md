# 权威适用性治理有界修订 R4：生命周期集合与聚合身份闭合

## 修订信息

```text
Proposal ID: CR-0008-R4
Title: Lifecycle Set and Aggregate Identity Closure
Workstream: WS-05
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0008-R3 EXACT BOUNDARY AND AUTHORITY CATALOG CLOSURE
Repair Basis: CR-0008-R3-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Repair Scope: AAG-R3-B1 only
Institution Freeze Created: NO
Runtime Authority Created: NO
```

### AAG-R4-01 变化集合边界使用稳定键

```text
Grant Lifecycle Change Set Boundary Key =
  Grant Fact Reference Semantic Conflict Set Key
+ Exact Authority Applicability Coordinate Digest
+ Grant Lifecycle Change Semantic Domain
+ Lifecycle Change Reference Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Change Set Boundary Rule Version
```

变化类型、结果、成员数量、记录时间和写入者不得换键。

### AAG-R4-02 候选集合边界固定完整成员

```text
Candidate Grant Lifecycle Change Set Boundary Payload =
  Change Set Boundary Key
+ Exact Registered Change Reference Resolution Set and Digest
+ Exact Failed Reference Attempt Set and Digest
+ Exact Permanent Hole Set and Digest
+ Exact Ordering / Supersession Proof Set and Digest
+ Exact Temporal Mapping Resolution Set and Digest
+ Required Conflict-subdomain Completeness Resolution Set and Digest
+ Per-set Equality Proofs
+ Canonical Byte Contract and Candidate Payload Digest
```

### AAG-R4-03 集合边界形成内容同一登记链

```text
Candidate Set Boundary
  -> Set Boundary Registration Attempt
  -> Registered Set Boundary
  -> Set Boundary Registration Resolution
```

候选、尝试和已登记摘要必须相等；解析为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### AAG-R4-04 集合边界完整性独立登记

完整性解析固定预期／观察变化引用、失败、空洞、顺序和时间映射集合摘要及集合相等证明，结果为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。引用构造者、边界构造者、聚合者和适用性计算者不能自证完整。

### AAG-R4-05 完整空集必须是登记事实

`NO_APPLICABLE_CHANGE` 只能由登记边界、`COMPLETE` 完整性、精确空变化引用集合、完整失败／空洞覆盖和有效时间映射共同支持。查询未返回记录不能替代该链。

### AAG-R4-06 生命周期聚合使用稳定语义键

```text
Grant Lifecycle Aggregate Semantic Key =
  Grant Fact Reference Semantic Conflict Set Key
+ Exact Authority Applicability Coordinate Digest
+ Registered Change Set Boundary ID and Digest
+ Change Set Boundary Registration Resolution ID and Digest
+ Change Set Boundary Completeness Resolution ID and Digest
+ Exact Change Reference Resolution Set Digest
+ Lifecycle Aggregate Rule Version
```

聚合结果不得进入键。

### AAG-R4-07 聚合候选固定逐成员评价

候选至少固定聚合语义键、全部变化引用解析、顺序／取代证明、有效区间评价、逐成员效果、完整空集证明或不适用标记、四值结果、执行授权、证据和候选摘要。

### AAG-R4-08 聚合形成内容同一登记链

```text
Candidate Lifecycle Aggregate
  -> Lifecycle Aggregate Registration Attempt
  -> Registered Lifecycle Aggregate
  -> Lifecycle Aggregate Registration Resolution
```

候选、尝试、登记摘要必须相等；外层解析为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### AAG-R4-09 内层四值保持封闭

```text
EFFECTIVE | NOT_EFFECTIVE | INDETERMINATE | CONFLICTED
```

唯一有效效果或内容同一效果支持确定值；集合、顺序、时间或证明未知为 `INDETERMINATE`；不兼容变化、顺序、目标或同键异载荷为 `CONFLICTED`。

### AAG-R4-10 同键聚合竞争必须完整

同一聚合语义键的全部候选、尝试和记录进入完整聚合竞争边界；该边界按 R3 共同载荷登记并独立证明完整。不得按结果、执行者或时间选择候选。

### AAG-R4-11 适用性计算只消费登记聚合单例

只有外层聚合登记解析为 `REGISTERED` 且唯一内容同一时，内层结果才可进入原子适用性计算。其他外层结果一律使适用性 `INDETERMINATE`。

### AAG-R4-12 集合与聚合必须分权

R3 的集合边界构造／登记／完整性与聚合执行／登记授权继续逐项使用。聚合竞争边界新增：

```text
Grant Lifecycle Aggregate Competition Boundary Construction Authority Type
Grant Lifecycle Aggregate Competition Boundary Registration Authority Type
Grant Lifecycle Aggregate Boundary Completeness Qualification Authority Type
Grant Lifecycle Aggregate Boundary Completeness Registration Authority Type
Grant Lifecycle Aggregate Resolution Execution Authority Type
Grant Lifecycle Aggregate Resolution Registration Authority Type
```

以上授权均使用 AAG-C-50 完整作用域且互不传播。

### AAG-R4-13 历史聚合不可变

新变化、时间映射、顺序证明、证据边界或规则产生新集合边界和聚合身份；旧集合、聚合、失败、空洞和冲突永久保留。

### AAG-R4-14 以下状态必须失败关闭

- 变化类型或结果分割集合边界；
- 从查询空结果建立完整空集；
- 聚合消费未登记或不完整集合边界；
- 聚合候选直接冒充已登记聚合；
- 同键异聚合按时间或执行者选赢家；
- 聚合执行者自证集合或竞争边界完整；
- 新变化覆盖历史集合或聚合。

### AAG-R4-15 已通过接口不得回归

```text
WS-02 / WS-03 Interface: PRESERVED
CR-0002 Three-value Consumer: PRESERVED
Grant / Applicability Separation: PRESERVED
Qualification / Applicability Separation: PRESERVED
```

### AAG-R4-16 候选级关闭声明

```text
AAG-R3-B1 Lifecycle Set and Aggregate Registration Identity: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Final Model Review: REQUIRED
WS-05 Model Exit: BLOCKED_PENDING_REVIEW
```

## 当前决定

```text
CR-0008-R4 Status: DRAFT
Authority: NONE
Executable: NO
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行接口回归和终局独立模型复审。
