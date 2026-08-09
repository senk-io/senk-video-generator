# 证明与豁免适用性治理有界修订 R1：内部拓扑与良基完整性闭合

## 修订信息

```text
Proposal ID: CR-0009-R1
Title: Internal Topology and Well-founded Completeness Closure
Workstream: WS-06
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0009 PROOF AND EXEMPTION APPLICABILITY GOVERNANCE
Repair Basis: CR-0009-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: PEAG-IM-B1 through PEAG-IM-B4 only
Interface Regression Review Required: YES
Independent Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 一、类型注册拓扑

### PEAG-R1-01 类型稳定键按域隔离

```text
Proof Type Semantic Key = Proof Type Registry ID and Version + Proof Type ID and Version
Exemption Type Semantic Key = Exemption Type Registry ID and Version + Exemption Type ID and Version
```

域、载荷、结果、登记者和登记时间不得换键。

### PEAG-R1-02 类型候选固定精确合同

候选固定稳定键、允许对象／要求／槽位／迁移、资格规则绑定、适用性规则、完整性、失效、演进、规范字节合同、候选摘要、制定授权和证据。

### PEAG-R1-03 类型登记保持冻结内容同一

```text
Candidate Type Payload Digest
= Frozen Content Digest
= Attempted Payload Digest
= Registered Type Payload Digest
```

### PEAG-R1-04 类型竞争边界必须完整

边界键固定类型语义键、类型注册表、证据边界、观察切口和规则版本；载荷固定全部候选、成功、失败、永久空洞、解析谱系和集合相等证明。

### PEAG-R1-05 类型边界独立登记完整性

候选边界、尝试、已登记边界和四值边界解析内容同一；独立完整性结果为 `COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED`。

### PEAG-R1-06 类型最终解析使用封闭真值表

登记完整边界上的唯一冻结内容单例为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；异合同、规则绑定或冻结内容为 `CONFLICTED`；其他为 `INDETERMINATE`。

### PEAG-R1-07 类型更正与取代只追加

非语义更正追加记录；语义变化产生新类型版本并绑定取代关系。旧类型、失败、空洞和冲突永久保留。

## 二、良基完整性

### PEAG-R1-08 完整性依赖必须拥有自然数阶

```text
Completeness Proof Rank = non-negative integer
```

每个完整性证明、资格、适用性和边界固定阶数及依赖图摘要。

### PEAG-R1-09 零阶只消费原子外部边界

零阶允许的输入仅为已登记原子证据、不可再分的提供方边界、其独立读取完整性及规范集合相等证明；不得依赖任何完整性证明适用性记录。

### PEAG-R1-10 高阶只能依赖严格低阶

```text
For every edge Pn -> Pm: rank(m) < rank(n)
```

同阶、升阶、自包含或回边全部非法。

### PEAG-R1-11 完整性依赖图必须登记

候选依赖图固定节点、边、阶数、根、叶、规范摘要和无环证明；登记尝试和记录内容同一，并进入完整竞争边界和独立完整性。

### PEAG-R1-12 环检测结果必须封闭

```text
ACYCLIC | CYCLIC | INDETERMINATE | CONFLICTED
```

只有登记的 `ACYCLIC` 图可支持完整性计算；`CYCLIC` 确定支持 `INCOMPLETE`，未知或冲突失败关闭。

### PEAG-R1-13 终止合同必须可重放

从根到零阶叶的每条路径必须有限、严格降阶并固定全部边。运行深度限制、超时或缓存不能替代良基证明。

### PEAG-R1-14 完整性计算者不得构造依赖图或自证

图构造、图登记、无环资格、无环登记、完整性计算和完整性登记权威互不传播。

## 三、证明适用性登记边界

### PEAG-R1-15 证明适用性语义键必须稳定

```text
Proof Applicability Semantic Conflict Set Key =
  Registered Proof Qualification Record ID and Digest
+ Candidate Proof ID and Payload Digest
+ Commit Key and Attempt ID and Decision Key
+ Qualification Scope Mode and Contract Scope Digest
+ Validity As Of and K/S/RR
+ Projection View Mode
+ Source Applicability Package Set Digest
+ Completeness Dependency Graph ID and Digest
+ Proof Applicability Rule ID, Version and Payload Digest
```

结果、记录、登记者和时间不得换键。

### PEAG-R1-16 证明适用性候选与登记内容同一

候选固定完整输入、逐谓词、四值结果、冲突、完整性、执行授权和摘要；尝试与登记载荷摘要必须相等。

### PEAG-R1-17 证明适用性竞争边界完整

边界键固定语义键、注册表、证据边界、观察切口和规则；载荷覆盖全部候选、成功、失败、空洞、谱系和集合相等证明，并独立登记完整性。

### PEAG-R1-18 证明适用性聚合与登记

登记完整边界上，内容同一确定结果支持对应四值；`APPLICABLE + INAPPLICABLE` 或同键异载荷为 `CONFLICTED`；未知输入为 `INDETERMINATE`。聚合候选、尝试、记录和四值登记解析内容同一。

## 四、豁免适用性登记边界

### PEAG-R1-19 豁免适用性语义键必须稳定

```text
Exemption Applicability Semantic Conflict Set Key =
  Registered Exemption Qualification Resolution ID and Digest
+ Exemption Basis ID and Version
+ Requirement Contract ID and Version and Slot ID
+ Requirement Mode
+ Target Object ID and Version and Transition Type
+ Frozen Exemption Rule ID, Version and Payload Digest
+ Validity As Of and K/S/RR
+ Projection View Mode
+ Source Applicability Package Set Digest
+ Completeness Dependency Graph ID and Digest
+ Exemption Applicability Rule ID, Version and Payload Digest
```

### PEAG-R1-20 豁免候选和登记必须内容同一

候选固定完整坐标、资格、来源、完整性、逐谓词、四值结果、冲突、授权和摘要；尝试与登记载荷不得修改任何字段。

### PEAG-R1-21 豁免竞争边界和聚合必须独立

豁免使用与证明相同的完整边界代数，但拥有不同注册表、边界类型、完整性和聚合记录；两域不能共享边界或互相消解冲突。

### PEAG-R1-22 投影输入信封必须固定登记聚合

证明／豁免投影分别固定适用性聚合登记解析、登记完整竞争边界、独立完整性、底层原子记录集、资格冲突、适用性冲突和证据引用。

## 五、累计授权目录

### PEAG-R1-23 类型和规则授权逐项列出

```text
Type Candidate Construction / Type Registration
Type Boundary Construction / Registration
Type Boundary Completeness Qualification / Registration
Type Resolution Execution / Registration
Applicability Rule Candidate Construction / Registration
Rule Boundary Construction / Registration
Rule Boundary Completeness Qualification / Registration
Rule Resolution Execution / Registration
```

每个斜线两侧均为独立授权类型。

### PEAG-R1-24 完整性图和评价授权逐项列出

```text
Completeness Dependency Graph Construction / Registration
Graph Boundary Construction / Registration
Graph Boundary Completeness Qualification / Registration
Acyclicity Qualification / Registration
Completeness Proof Qualification Execution / Registration
Completeness Proof Applicability Execution / Registration
Completeness Evaluation / Registration
```

### PEAG-R1-25 证明适用性授权逐项列出

证明候选计算、原子登记、竞争边界构造／登记、边界完整性资格／登记、聚合执行／登记、聚合边界／完整性／解析、投影输入信封构造／登记全部为独立授权类型。

### PEAG-R1-26 豁免适用性授权逐项列出

豁免拥有与证明相同但类型隔离的全部授权；证明授权不能在豁免域使用，反之亦然。

### PEAG-R1-27 授权作用域完整且不传播

每项授权固定允许类型、规则、稳定键、注册表、边界、输入输出、阶数、证据、有效窗口、`Can Change`、`Cannot Change` 和授予事实；全部互不传播。

## 六、失败关闭和候选声明

### PEAG-R1-28 以下状态必须失败关闭

- 类型使用未登记自由字符串；
- 完整性依赖图自包含、同阶、升阶或成环；
- 超时或最大深度替代良基证明；
- 证明与豁免共享竞争边界；
- 候选适用性直接冒充登记聚合；
- 不完整边界支持确定投影；
- 泛化授权跨类型或跨操作传播。

### PEAG-R1-29 已通过接口不得回归

```text
WS-04 / WS-05 Compatibility: PRESERVED
CR-0002 / CR-0003 Consumer Compatibility: PRESERVED
ABORTED / EXEMPT Positive Chains: PRESERVED
Atomic Qualification Three-value: PRESERVED
```

### PEAG-R1-30 四项阻断只在候选层关闭

```text
PEAG-IM-B1 Type Registry Topology: CLOSED_AS_DRAFT
PEAG-IM-B2 Completeness Recursion Termination: CLOSED_AS_DRAFT
PEAG-IM-B3 Applicability Registration Boundaries: CLOSED_AS_DRAFT
PEAG-IM-B4 Cumulative Authority Catalog: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0009-R1 Status: DRAFT
Authority: NONE
Executable: NO
WS-06 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行 R1 接口回归和独立复合模型复审。
