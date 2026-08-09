# 资格治理有界修订 R5：登记竞争边界闭合

## 修订信息

```text
Proposal ID: CR-0007-R5
Title: Registration Competition Boundary Closure
Workstream: WS-04
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0007-R4 INTERNAL REGISTRATION AND AUTHORITY TOPOLOGY CLOSURE
Repair Basis: CR-0007-R4-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Repair Scope: residual QG-IM-B1 + residual QG-IM-B4 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Interface Regression Review Required: YES
Independent Composite Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
```

> 本文件只补齐资格规则与资格治理工件的登记竞争边界、独立完整性和最终解析绑定。它不改变资格输入、结果代数、适用性、决策或提交接口。

## 一、修订边界

### QG-R5-01 R5 只关闭两个残余阻断

```text
QG-IM-B1 residual: Qualification Rule Registration Boundary and Completeness
QG-IM-B4 residual: Governance Artifact Registration Boundary and Completeness
```

### QG-R5-02 R5 累计覆盖 R4 的无边界解析

`QG-R4-08` 和 `QG-R4-24` 的四值对象登记解析必须按本修订固定已登记完整竞争边界。R4 的候选、冻结、尝试、内容同一和消费门继续有效。

## 二、共享竞争边界代数

### QG-R5-03 竞争边界必须固定治理证据边界

每个登记竞争边界必须绑定：

```text
Governed Registration Registry ID and Version
Registration Semantic Conflict Set Key
Governed Evidence Boundary ID and Digest
Evidence Boundary Completeness Resolution ID and Digest
Boundary Observation Cut
Boundary Canonical Byte Contract and Digest Algorithm
Boundary Rule Version
```

登记时间、结果值、观察者或有利记录不得用于换边界。

### QG-R5-04 精确竞争集合必须覆盖三类事实

```text
Exact Successful Registered Record Set and Digest
Exact Failed Registration Attempt Set and Digest
Exact Permanent Registration Hole Set and Digest
Exact Registration Resolution Lineage Set and Digest
```

每类集合都必须提供规范排序、成员证明、非成员反证能力和对受治理证据边界的集合相等证明。

### QG-R5-05 边界自身必须形成内容同一登记链

```text
Candidate Registration Competition Boundary
  -> Competition Boundary Registration Attempt
  -> Registered Registration Competition Boundary
  -> Competition Boundary Registration Resolution
```

候选、尝试载荷、已登记载荷的规范摘要必须相同。登记解析值为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

### QG-R5-06 竞争边界完整性必须独立登记

`Registered Registration Competition Boundary Completeness Resolution` 至少绑定：

```text
Registered Competition Boundary ID and Digest
Registration Semantic Conflict Set Key
Governed Evidence Boundary ID and Digest
Evidence Boundary Completeness Resolution ID and Digest
Expected and Observed Successful Record Set Digests
Expected and Observed Failed Attempt Set Digests
Expected and Observed Permanent Hole Set Digests
Expected and Observed Resolution Lineage Set Digests
Per-set Equality Proof IDs and Digests
Completeness Outcome
Completeness Qualification Authority Reference
Completeness Registration Authority Reference
Candidate and Registered Payload Digests
```

完整性结果为：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

边界构造者、对象登记者、对象解析者和运行消费者都不能自证边界完整。

### QG-R5-07 最终对象解析必须绑定登记完整边界

任何资格规则或治理工件的最终登记解析键都必须包含：

```text
Registration Semantic Conflict Set Key
Registered Competition Boundary ID and Digest
Competition Boundary Registration Resolution ID and Digest
Registered Competition Boundary Completeness Resolution ID and Digest
Exact Successful / Failed / Hole / Lineage Set Digests
Object Registration Resolution Rule Version
```

只有边界登记解析为 `REGISTERED` 且完整性为 `COMPLETE`，才可以产生确定的对象登记解析。

### QG-R5-08 不完整边界只能失败关闭

```text
Boundary Resolution != REGISTERED -> Object Resolution = INDETERMINATE
Boundary Completeness != COMPLETE -> Object Resolution = INDETERMINATE
Set Equality Proof Missing or Invalid -> Object Resolution = INDETERMINATE
Boundary Payload Conflict -> Object Resolution = CONFLICTED
```

不得从局部可见集合推断 `REGISTERED` 或 `NOT_REGISTERED`。

## 三、资格规则登记竞争边界

### QG-R5-09 规则边界使用唯一稳定键

```text
Qualification Rule Registration Competition Boundary Key =
  Rule Semantic Conflict Set Key
+ Qualification Rule Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Boundary Rule Version
```

规则载荷、候选摘要、登记结果、失败数量或登记时间不得用于换键。

### QG-R5-10 候选规则边界必须固定完整集合

`Candidate Qualification Rule Registration Competition Boundary` 除共享字段外至少绑定：

```text
Rule Boundary Key
Exact Candidate Rule Record Set and Digest
Exact Rule Registration Attempt Set and Digest
Exact Registered Rule Record Set and Digest
Exact Permanent Rule Registration Hole Set and Digest
Exact Prior Rule Registration Resolution Lineage Set and Digest
Institution Freeze Reference Resolution Set and Digest
Per-set Membership and Equality Proofs
Candidate Boundary Payload Digest
Boundary Construction Authority Reference
```

### QG-R5-11 规则边界登记必须保留全部尝试

规则边界登记尝试至少保存目标边界注册表、候选摘要、尝试摘要、登记授权、时间和失败证据。失败、冲突和永久空洞不得删除或被后续成功覆盖。

### QG-R5-12 已登记规则边界必须内容同一

```text
Candidate Rule Boundary Payload Digest
= Attempted Rule Boundary Payload Digest
= Registered Rule Boundary Payload Digest
```

任何不等都使规则边界登记解析为 `CONFLICTED` 或 `INDETERMINATE`，不得进入规则对象解析。

### QG-R5-13 规则边界完整性使用独立授权

规则边界完整性资格和登记权威必须与以下权威分离：

```text
Rule Definition Authority
Rule Registration Authority
Rule Boundary Construction Authority
Rule Boundary Registration Authority
Rule Registration Resolution Authority
Qualification Computation Authority
```

### QG-R5-14 规则对象解析使用封闭真值表

在已登记且完整的规则竞争边界内：

```text
Exactly one successful content identity
+ valid exact-payload Institution Freeze Reference
+ no contradictory registered resolution
  -> REGISTERED

Zero successful registered records
+ complete attempts, holes and lineage
  -> NOT_REGISTERED

More than one non-content-identical successful record
or divergent frozen content
or contradictory terminal registration resolution
  -> CONFLICTED

Otherwise
  -> INDETERMINATE
```

内容同一的重复物理副本不能制造多个语义赢家，但必须全部留在边界中并解析为同一规范记录身份。

### QG-R5-15 资格计算门必须固定规则边界

资格计算除 R4 条件外，还必须保存：

```text
Rule Registration Resolution ID and Digest
Registered Rule Competition Boundary ID and Digest
Rule Boundary Registration Resolution ID and Digest
Registered Rule Boundary Completeness Resolution ID and Digest
Exact Rule Competition Set Digests
```

任一引用漂移都要求新的资格计算键，不能复用旧结果。

## 四、治理工件登记竞争边界

### QG-R5-16 工件边界按类型和稳定键隔离

```text
Governance Artifact Registration Competition Boundary Key =
  Artifact Type
+ Artifact Stable Key
+ Artifact Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Boundary Rule Version
```

不同工件类型不得共享边界或相互消解冲突。

### QG-R5-17 候选工件边界必须固定完整集合

`Candidate Governance Artifact Registration Competition Boundary` 除共享字段外至少绑定：

```text
Artifact Boundary Key
Exact Candidate Artifact Set and Digest
Exact Artifact Registration Attempt Set and Digest
Exact Registered Artifact Set and Digest
Exact Permanent Artifact Registration Hole Set and Digest
Exact Prior Artifact Registration Resolution Lineage Set and Digest
Institution Freeze Reference Resolution Set and Digest
Per-set Membership and Equality Proofs
Candidate Boundary Payload Digest
Boundary Construction Authority Reference
```

### QG-R5-18 工件边界登记必须保留全部尝试

工件边界登记尝试保存候选、目标注册表、登记授权、尝试载荷摘要、时间及失败证据；异类型、异成员、异映射和异重新资格范围都不能在登记前被折叠。

### QG-R5-19 已登记工件边界必须内容同一

```text
Candidate Artifact Boundary Payload Digest
= Attempted Artifact Boundary Payload Digest
= Registered Artifact Boundary Payload Digest
```

工件边界更正只能追加；语义变化产生新的边界观察切口或规则版本，不能覆盖原边界。

### QG-R5-20 工件边界完整性使用独立授权

工件边界完整性资格和登记权威必须与工件构造、对象登记、边界构造、边界登记、对象解析、冻结和运行消费权威分离。

### QG-R5-21 工件对象解析使用封闭真值表

在已登记且完整的工件竞争边界内：

```text
Exactly one successful content identity
+ valid exact-payload Institution Freeze Reference
+ no contradictory registered resolution
  -> REGISTERED

Zero successful registered artifacts
+ complete attempts, holes and lineage
  -> NOT_REGISTERED

More than one non-content-identical successful artifact
or divergent type-specific payload
or divergent frozen content
or contradictory terminal registration resolution
  -> CONFLICTED

Otherwise
  -> INDETERMINATE
```

不得按版本号、登记时间、发布者或消费者偏好选择赢家。

### QG-R5-22 工件运行消费门必须固定工件边界

兼容记录、兼容域快照、前向解释契约和重新资格要求的运行消费都必须保存：

```text
Artifact Registration Resolution ID and Digest
Registered Artifact Competition Boundary ID and Digest
Artifact Boundary Registration Resolution ID and Digest
Registered Artifact Boundary Completeness Resolution ID and Digest
Exact Artifact Competition Set Digests
```

边界或完整性变化只能产生新的消费身份和追加历史，不能重写既有消费事实。

## 五、累计授权补充

### QG-R5-23 新边界操作必须拥有显式授权类型

R4 累计授权目录增加：

```text
Qualification Rule Competition Boundary Construction Authority Type
Qualification Rule Competition Boundary Registration Authority Type
Qualification Rule Boundary Completeness Qualification Authority Type
Qualification Rule Boundary Completeness Registration Authority Type
Qualification Rule Registration Resolution Authority Type
Governance Artifact Competition Boundary Construction Authority Type
Governance Artifact Competition Boundary Registration Authority Type
Governance Artifact Boundary Completeness Qualification Authority Type
Governance Artifact Boundary Completeness Registration Authority Type
Governance Artifact Registration Resolution Authority Type
```

### QG-R5-24 新授权继承完整作用域格式但不继承权限

每项授权必须使用 `QG-R4-11` 的完整作用域，并额外固定允许的冲突集键、证据边界类型、边界规则版本和集合证明契约。授权类型之间互不传播。

## 六、并发、纠正与非法状态

### QG-R5-25 并发登记必须汇入同一边界

相同语义冲突键下的并发候选、尝试和成功记录必须汇入同一竞争边界。并发顺序、先到成功、最后写入或重试次数不能改变对象解析。

### QG-R5-26 边界纠正不得删除竞争事实

非语义表示缺陷以追加更正记录修复；集合成员、证据边界、完整性或规则变化必须产生新边界身份。旧边界、失败尝试、永久空洞、冲突和旧解析永久保留。

### QG-R5-27 以下状态必须失败关闭

- 对象解析没有固定已登记竞争边界；
- 边界没有精确覆盖成功、失败、空洞和解析谱系；
- 完整性由边界构造者、对象登记者、解析者或消费者自证；
- 从不完整边界推断 `NOT_REGISTERED`；
- 从局部成功记录推断 `REGISTERED`；
- 规则或工件同键异内容按时间或版本号选赢家；
- 物理重复副本被错误解释为不同语义赢家；
- 边界更正删除失败尝试或隐藏冲突；
- 运行消费未固定边界、完整性和精确集合摘要；
- 对象登记、边界登记或解析创建制度冻结。

## 七、回归和候选级闭合

### QG-R5-28 已通过模型边界必须保持

```text
B/T/K/Q/S/RR Consumption: PRESERVED
Qualification / Applicability Separation: PRESERVED
Atomic Three-value Qualification: PRESERVED
Four-value Conflict Aggregate: PRESERVED
CR-0002 Basis Adapter: PRESERVED
CR-0003 Contract Scope and Proof Identity: PRESERVED
QG-IM-B2 Authority Closure: PRESERVED
QG-IM-B3 Atomic Boundary Closure: PRESERVED
```

### QG-R5-29 两个残余阻断只在候选层声明关闭

```text
QG-IM-B1 Rule Registration Boundary and Completeness: CLOSED_AS_DRAFT
QG-IM-B4 Governance Artifact Registration Boundary and Completeness: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
Institution Freeze Eligibility: FAIL
```

### QG-R5-30 当前决定

```text
CR-0007-R5 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: residual QG-IM-B1 + residual QG-IM-B4
Proposal Revision Created: YES
Interface Regression Review: REQUIRED
Independent Composite Model Re-review: REQUIRED
WS-04 Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行接口回归和独立复合模型终局复审；只有两项均无阻断，`WS-04` 模型工作流才可退出。
