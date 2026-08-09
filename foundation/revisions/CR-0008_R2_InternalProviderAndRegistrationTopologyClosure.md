# 权威适用性治理有界修订 R2：内部提供方与登记拓扑闭合

## 修订信息

```text
Proposal ID: CR-0008-R2
Title: Internal Provider and Registration Topology Closure
Workstream: WS-05
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0008-R1 SOURCE APPLICABILITY CONSUMPTION IDENTITY CLOSURE
Repair Basis: CR-0008-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Scope: AAG-IM-B1 through AAG-IM-B4 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Interface Regression Review Required: YES
Independent Composite Model Re-review Required: YES
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 一、共同登记边界

### AAG-R2-01 四类修复对象共享完整登记拓扑

```text
Candidate Object
  -> Registration Attempt
  -> Registered Object
  -> Registered Complete Competition Boundary
  -> Independent Boundary Completeness Resolution
  -> Object Registration Resolution
```

最终解析值为 `REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED`。

### AAG-R2-02 竞争边界必须覆盖全部事实

每个边界固定语义冲突键、目标注册表、受治理证据边界、全部候选、成功记录、失败尝试、永久空洞、既有解析谱系、逐集合规范摘要和集合相等证明。

### AAG-R2-03 只有登记完整边界支持确定解析

边界登记解析非 `REGISTERED`、完整性非 `COMPLETE` 或集合相等证明无效时，对象解析必须 `INDETERMINATE`；同键异内容、异冻结载荷或矛盾终局必须 `CONFLICTED`。

### AAG-R2-04 内容同一必须端到端保持

```text
Candidate Payload Digest
= Attempted Payload Digest
= Registered Payload Digest
```

需要制度冻结的规则还必须等于精确冻结内容摘要。

## 二、授予事实消费引用

### AAG-R2-05 引用不创建授予

`Authority Grant Fact Consumption Reference` 只规范化并登记一个已经由 `IF-0001` 允许的正式授予历史事实。候选必须固定：

```text
Formal Grant Decision Fact Reference and Digest
Authority -> Decision -> Evidence -> Formal Fact Chain Digest
Granting Authority Identity and Scope
Holder Identity or Role
Can Change and Cannot Change
Authority Type and Object Scope
Allowed Decision / Disposition / Transition Types
Effective and Expiry Coordinates
Delegation Constraints
Historical Commitment Reference
Institution and Evidence References
Canonical Grant Fact Payload Digest
```

引用登记不能补写缺失授予决策、证据或正式事实。

### AAG-R2-06 授予引用使用稳定语义键

```text
Grant Fact Reference Semantic Conflict Set Key =
  Formal Grant Decision Fact ID and Version
+ Grant Authority Type
+ Holder Identity or Role
+ Canonical Grant Scope Identity
```

载荷、结果、登记者和时间不得换键。

### AAG-R2-07 授予引用必须拥有完整竞争边界

候选引用、尝试、已登记引用、竞争边界、边界登记解析、独立完整性和最终引用解析均按共同拓扑建立。同一正式授予事实异主体、异作用域或异历史载荷必须 `CONFLICTED`。

### AAG-R2-08 授予引用解析门

只有 `REGISTERED` 单例且正式事实链完整可以进入适用性计算。`NOT_REGISTERED` 只允许完整边界证明没有成功引用；它不表示授予不存在或不适用。

## 三、规则竞争边界

### AAG-R2-09 规则边界稳定键

```text
Applicability Rule Competition Boundary Key =
  Authority Applicability Rule Semantic Conflict Set Key
+ Rule Registry ID and Version
+ Governed Evidence Boundary ID and Digest
+ Boundary Observation Cut
+ Boundary Rule Version
```

### AAG-R2-10 规则边界固定候选、冻结和登记全集

边界除共同字段外，必须固定候选规则集合、制度冻结引用解析集合、登记记录集合及内容同一证明。边界完整性由规则定义、登记、计算和消费之外的独立权威登记。

### AAG-R2-11 规则解析使用封闭真值表

已登记完整边界内，唯一内容同一成功且精确冻结有效为 `REGISTERED`；完整零成功为 `NOT_REGISTERED`；异载荷、异冻结内容或矛盾结果为 `CONFLICTED`；其他为 `INDETERMINATE`。

## 四、授予生命周期变化消费

### AAG-R2-12 生命周期变化只引用正式外部事实

`Grant Lifecycle Change Consumption Reference` 固定撤销、暂停、取代、恢复或终止的正式决策事实链、目标授予、作用域、有效坐标、前驱／后继、证据和规范摘要。引用不能创建变化事实。

### AAG-R2-13 生命周期变化语义键排除记录事实

```text
Grant Lifecycle Change Semantic Conflict Set Key =
  Grant Fact Reference Semantic Conflict Set Key
+ Change Semantic Domain
+ Effective Scope Digest
+ Canonical Effective Coordinate
+ Lifecycle Rule Version
```

变化事实 ID、记录 ID、位置、时间和写入者不得换键。

### AAG-R2-14 变化引用必须内容同一登记

每个变化引用按共同拓扑形成候选、尝试、记录、完整竞争边界、独立完整性和四值引用解析。非 `REGISTERED` 引用不能成为确定变化成员。

### AAG-R2-15 变化集合边界必须完整

`Registered Grant Lifecycle Change Set Boundary` 固定同一语义键下全部变化引用解析、失败尝试、永久空洞、顺序／取代证明、时间映射、边界完整性和精确集合摘要。完整空集必须被显式证明。

### AAG-R2-16 生命周期聚合使用四值控制面

```text
EFFECTIVE
NOT_EFFECTIVE
INDETERMINATE
CONFLICTED
```

在授予有效区间内、完整空变化集或唯一有效恢复链可支持 `EFFECTIVE`；有效撤销、暂停、取代、终止或区间外可支持 `NOT_EFFECTIVE`；集合、顺序、时间或证据未知为 `INDETERMINATE`；不兼容变化为 `CONFLICTED`。

### AAG-R2-17 开放世界否定必须失败关闭

未找到变化不等于完整空集。只有登记完整边界和独立空集证明可以支持“没有适用变化”；记录时间、“最新”或单一有利成员不能解决冲突。

### AAG-R2-18 适用性真值表消费生命周期聚合

`AAG-C-28/29` 中关于未撤销、到期、撤销和取代的判断，统一改为消费登记的生命周期聚合。`EFFECTIVE` 可参与正向链，`NOT_EFFECTIVE` 可在完整证据下支持确定否定，其余只支持 `INDETERMINATE` 并保留冲突。

## 五、三值消费解析登记

### AAG-R2-19 消费解析必须拥有稳定语义键

```text
Authority Applicability Consumer Resolution Semantic Key =
  Atomic Authority Applicability Semantic Key
+ Registered Atomic Evaluation Boundary ID and Digest
+ Atomic Boundary Completeness Resolution ID and Digest
+ Atomic or Aggregate Source Kind
+ Consumer Adaptation Rule Version
+ CR-0002 Consumer Contract Version
```

结果值、记录 ID、登记者和时间不得换键。

### AAG-R2-20 候选消费载荷固定三值适配证据

至少保存 C41 全部字段、原子或聚合来源、内部四值结果、三值输出、冲突引用、适配逐项证明、候选摘要、构造授权和证据。

### AAG-R2-21 消费解析登记保持内容同一

候选、尝试、已登记消费解析必须摘要相等，并按共同拓扑进入完整竞争边界。同键异三值结果、异来源或丢失冲突引用必须 `CONFLICTED`。

### AAG-R2-22 冲突适配不可逆

```text
Internal CONFLICTED
  -> Consumer INDETERMINATE
  + exact mandatory Conflict References
```

任何缺少冲突引用的候选都不得登记；后续解释不能恢复为确定结果。

## 六、累计授权与非法状态

### AAG-R2-23 累计授权目录必须增加新操作

新增授予引用构造／登记／边界／完整性／解析、规则边界／完整性／解析、生命周期引用／边界／完整性／聚合、消费解析构造／登记／边界／完整性／解析授权类型。

### AAG-R2-24 新授权逐项限界且互不传播

每项授权使用 `AAG-C-50` 完整作用域，并固定允许语义键、证据边界、集合证明和规则版本。引用权威不取得授予或变化事实权威；登记、完整性、聚合和解析互不传播。

### AAG-R2-25 以下状态必须失败关闭

- 从授予引用或变化引用创建正式权威事实；
- 引用缺少 `Authority -> Decision -> Evidence -> Formal Fact` 链；
- 规则或引用解析没有登记完整竞争边界；
- 从未找到变化推断完整空集；
- 生命周期冲突按时间或位置选赢家；
- 消费解析登记修改适配结果或删除冲突引用；
- 对象登记者、聚合者或消费者自证边界完整；
- 新授权从旧权威隐式继承。

## 七、回归和候选声明

### AAG-R2-26 已通过接口不得回归

```text
WS-02 / WS-03 Upstream Interface: PRESERVED
Qualification / Applicability Separation: PRESERVED
Atomic Three-value Result: PRESERVED
Internal Four-value Aggregate: PRESERVED
CR-0002 Three-value Consumer Contract: PRESERVED
Historical Immutability: PRESERVED
```

### AAG-R2-27 四项阻断只在候选层关闭

```text
AAG-IM-B1 Grant Fact Reference Provider Topology: CLOSED_AS_DRAFT
AAG-IM-B2 Rule Registration Boundary: CLOSED_AS_DRAFT
AAG-IM-B3 Lifecycle Change Consumption Topology: CLOSED_AS_DRAFT
AAG-IM-B4 Consumer Resolution Registration: CLOSED_AS_DRAFT
Interface Regression Review: REQUIRED
Independent Model Re-review: REQUIRED
```

## 当前决定

```text
CR-0008-R2 Status: DRAFT
Authority: NONE
Executable: NO
Proposal Revision Created: YES
WS-05 Model Exit: BLOCKED_PENDING_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须执行接口回归和独立复合模型复审；R2 自检不能证明 `WS-05` 闭合。
