# 权威适用性治理有界修订 R3：精确边界与授权目录闭合

## 修订信息

```text
Proposal ID: CR-0008-R3
Title: Exact Boundary and Authority Catalog Closure
Workstream: WS-05
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0008-R2 INTERNAL PROVIDER AND REGISTRATION TOPOLOGY CLOSURE
Repair Basis: CR-0008-R2-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Repair Scope: AAG-R2-B1 + AAG-R2-B2 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Interface Regression Review Required: YES
Independent Composite Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 一、共享精确载荷

### AAG-R3-01 三类边界载荷必须固定共同全集

每类边界载荷均包含：

```text
Type-specific Competition Boundary Key
Governed Evidence Boundary ID and Digest
Evidence Boundary Completeness Resolution ID and Digest
Exact Candidate Set and Digest
Exact Successful Registered Record Set and Digest
Exact Failed Registration Attempt Set and Digest
Exact Permanent Registration Hole Set and Digest
Exact Prior Registration Resolution Lineage Set and Digest
Per-set Canonical Ordering and Equality Proof IDs and Digests
Boundary Construction Authority Reference
Canonical Byte Contract and Digest Algorithm
Candidate Boundary Payload Digest
```

### AAG-R3-02 边界登记链必须内容同一

```text
Candidate Boundary
  -> Boundary Registration Attempt
  -> Registered Boundary
  -> Boundary Registration Resolution
```

候选、尝试和已登记载荷摘要必须相等；解析为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### AAG-R3-03 边界完整性必须独立登记

每类 `Registered Boundary Completeness Resolution` 固定边界、证据边界、预期／观察四类集合摘要、集合相等证明、结果、资格授权、登记授权和候选／登记摘要。结果为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。

### AAG-R3-04 最终对象解析必须绑定完整边界

最终解析键固定语义冲突键、已登记边界及摘要、边界登记解析、独立完整性解析、四类精确集合摘要和对象解析规则版本。只有 `REGISTERED + COMPLETE` 支持确定对象解析。

## 二、授予事实引用边界

### AAG-R3-05 授予引用边界键必须稳定

```text
Grant Fact Reference Competition Boundary Key =
  Grant Fact Reference Semantic Conflict Set Key
+ Grant Reference Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Grant Reference Boundary Rule Version
```

引用载荷、结果、事实时间和登记者不得换键。

### AAG-R3-06 授予引用边界载荷固定正式事实链

除共同全集外，候选集合每个成员必须固定正式授予事实链摘要、授予边界摘要和历史承诺引用；边界还固定正式事实链验证集合及其完整性证明。

### AAG-R3-07 授予引用最终解析真值表

唯一内容同一且正式事实链有效的成功引用为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；同一正式事实异主体、异作用域、异历史载荷或矛盾解析为 `CONFLICTED`；其他为 `INDETERMINATE`。

## 三、授予生命周期变化引用边界

### AAG-R3-08 变化引用边界键必须稳定

```text
Grant Lifecycle Change Reference Competition Boundary Key =
  Grant Lifecycle Change Semantic Conflict Set Key
+ Lifecycle Change Reference Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Lifecycle Change Reference Boundary Rule Version
```

变化类型、结果、记录时间和写入者不得换键。

### AAG-R3-09 变化引用边界载荷固定变化事实链

除共同全集外，固定每个变化候选的正式决策事实链、目标授予、作用域、有效坐标、前驱／后继和时间映射摘要，以及事实链验证集合和完整性。

### AAG-R3-10 变化引用最终解析真值表

唯一内容同一且事实链有效的变化引用为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；同键异变化、异作用域、异坐标、异前驱／后继或矛盾事实链为 `CONFLICTED`；其他为 `INDETERMINATE`。

### AAG-R3-11 变化集合边界与引用边界必须分层

引用竞争边界只解析单一变化事实引用；`Registered Grant Lifecycle Change Set Boundary` 聚合同一授予坐标下全部已解析变化。两者拥有不同稳定键、注册表和完整性，不得复用同一边界记录。

## 四、三值消费解析边界

### AAG-R3-12 消费解析边界键必须稳定

```text
Authority Applicability Consumer Resolution Competition Boundary Key =
  Authority Applicability Consumer Resolution Semantic Key
+ Consumer Resolution Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Consumer Boundary Rule Version
```

三值结果、来源种类、冲突引用、登记时间和登记者不得换键。

### AAG-R3-13 消费解析边界载荷固定适配证明

除共同全集外，每个候选固定内部原子或聚合来源、内部结果、三值输出、完整冲突引用集合、适配证明摘要和 `CR-0002` 合同版本。

### AAG-R3-14 消费解析最终真值表

唯一内容同一且适配证明有效的成功解析为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；同键异三值结果、异内部来源、异冲突引用或异适配证明为 `CONFLICTED`；其他为 `INDETERMINATE`。

### AAG-R3-15 运行消费只允许登记单例

决策准入只能消费最终登记解析为 `REGISTERED` 的唯一内容同一三值解析，并固定其完整竞争边界和独立完整性；其他结果全部失败关闭。

## 五、逐项累计授权目录

### AAG-R3-16 授予引用操作授权

```text
Grant Fact Reference Construction Authority Type
Grant Fact Reference Registration Authority Type
Grant Fact Reference Boundary Construction Authority Type
Grant Fact Reference Boundary Registration Authority Type
Grant Fact Reference Boundary Completeness Qualification Authority Type
Grant Fact Reference Boundary Completeness Registration Authority Type
Grant Fact Reference Resolution Execution Authority Type
Grant Fact Reference Resolution Registration Authority Type
```

### AAG-R3-17 规则边界操作授权

```text
Applicability Rule Boundary Construction Authority Type
Applicability Rule Boundary Registration Authority Type
Applicability Rule Boundary Completeness Qualification Authority Type
Applicability Rule Boundary Completeness Registration Authority Type
Applicability Rule Resolution Execution Authority Type
Applicability Rule Resolution Registration Authority Type
```

### AAG-R3-18 生命周期引用操作授权

```text
Grant Lifecycle Change Reference Construction Authority Type
Grant Lifecycle Change Reference Registration Authority Type
Grant Lifecycle Change Reference Boundary Construction Authority Type
Grant Lifecycle Change Reference Boundary Registration Authority Type
Grant Lifecycle Change Reference Boundary Completeness Qualification Authority Type
Grant Lifecycle Change Reference Boundary Completeness Registration Authority Type
Grant Lifecycle Change Reference Resolution Execution Authority Type
Grant Lifecycle Change Reference Resolution Registration Authority Type
```

### AAG-R3-19 生命周期集合与聚合授权

```text
Grant Lifecycle Change Set Boundary Construction Authority Type
Grant Lifecycle Change Set Boundary Registration Authority Type
Grant Lifecycle Change Set Completeness Qualification Authority Type
Grant Lifecycle Change Set Completeness Registration Authority Type
Grant Lifecycle Aggregate Execution Authority Type
Grant Lifecycle Aggregate Registration Authority Type
```

### AAG-R3-20 消费解析操作授权

```text
Consumer Resolution Construction Authority Type
Consumer Resolution Registration Authority Type
Consumer Resolution Boundary Construction Authority Type
Consumer Resolution Boundary Registration Authority Type
Consumer Resolution Boundary Completeness Qualification Authority Type
Consumer Resolution Boundary Completeness Registration Authority Type
Consumer Resolution Execution Authority Type
Consumer Resolution Final Registration Authority Type
```

### AAG-R3-21 授权作用域必须可登记

每个授权实例固定允许对象类型、语义键、注册表、证据边界、规则版本、输入输出、集合证明、有效窗口、`Can Change`、`Cannot Change`、授予权威和证据引用。

### AAG-R3-22 授权严格不传播

构造、对象登记、边界构造、边界登记、完整性资格、完整性登记、解析执行、解析登记、聚合执行和聚合登记全部互不传播，也不取得授予事实、变化事实、决策、提交或制度冻结权威。

## 六、并发和失败关闭

### AAG-R3-23 并发必须汇入同一逐类型边界

相同语义冲突键下的并发候选、成功、失败和空洞必须进入同一类型边界。先到、最后写入、最大版本或调用者选择不能决定结果。

### AAG-R3-24 更正必须追加

边界或解析的非语义更正追加记录；语义键、证据边界、集合或规则变化产生新边界身份。旧边界、失败、空洞、冲突和解析永久保留。

### AAG-R3-25 以下状态必须失败关闭

- 三类对象共享无类型边界或注册表；
- 边界键包含结果、写入者或登记时间；
- 边界缺少任一候选、成功、失败、空洞或谱系集合；
- 对象解析未固定边界登记和独立完整性；
- 生命周期引用边界替代变化集合边界；
- 冲突消费解析因三值适配丢失引用；
- 泛化授权替代逐项授权；
- 任一授权隐式取得相邻操作或正式事实权威。

## 七、回归与候选声明

### AAG-R3-26 已通过接口和规则边界不得回归

```text
WS-02 / WS-03 Interface: PRESERVED
CR-0002 Three-value Consumer: PRESERVED
Qualification / Applicability Separation: PRESERVED
Applicability Rule Boundary Closure: PRESERVED
Historical Immutability: PRESERVED
```

### AAG-R3-27 残余阻断只在候选层关闭

```text
AAG-R2-B1 Exact Per-type Competition Boundary Identity: CLOSED_AS_DRAFT
AAG-R2-B2 Explicit Cumulative Authority Catalog: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0008-R3 Status: DRAFT
Authority: NONE
Executable: NO
WS-05 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 R3 接口回归和终局独立复合模型复审。
