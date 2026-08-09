# CR-0008-R1 复合独立模型审查

## 审查信息

```text
Review ID: CR-0008-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Authority Applicability Governance Model Review
Status: COMPLETED
Result: BLOCKED
Reviewed Composite: CR-0008 + CR-0008-R1
Upstream Basis: CR-0008-R1-CR-0005-R11-CR-0006-R10-FINAL-UPSTREAM-CROSS-INTERFACE-REVIEW
Consumer Basis: CR-0008-R1-CR-0002-CONSUMER-INTERFACE-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-checks and CLOSED_AS_DRAFT declarations were ignored
Institution Freeze Created: NO
Runtime Authority Created: NO
Blocking Finding Count: 4
Next Authorized Stage: CR-0008-R2 bounded internal topology repair
```

> 本文件审查复合模型自身的授予引用、规则、登记、边界、授权、撤销和消费解析拓扑。接口通过不证明内部提供方存在或登记闭合。

## 一、总体裁决

模型已正确建立三值决策消费、来源四值冲突保留、完整决策坐标、资格／适用性分离和历史不可变，但四类内部拓扑仍不完整。

```text
Grant / Applicability Separation: PASS
Coordinate Completeness: PASS
Source Applicability Consumption: PASS
CR-0002 Three-value Consumer Interface: PASS
Authority Grant Reference Provider Topology: BLOCKED
Applicability Rule Registration Boundary: BLOCKED
Revocation / Supersession Consumption Topology: BLOCKED
Consumer Resolution Content-identical Registration: BLOCKED
Residual Internal Blockers: 4
Overall Result: BLOCKED
```

## 二、`AAG-IM-B1`：权威授予引用的提供方拓扑不存在

`AAG-C-06/07` 假定存在：

```text
Authority Grant ID and Version
Grant Registry ID and Version
Grant Registration Resolution
Exact Grant Payload Digest
```

但 `IF-0001` 只冻结权威先于执行、边界、不传播、生命周期和历史不可变原则，没有定义通用授予注册表或四值登记解析。当前模型不能把这些字段作为已存在上游接口，也不能用适用性计算创建授予事实。

```text
Finding ID: AAG-IM-B1
Severity: BLOCKING
Result: OPEN
```

最低修复：建立不创造授予的 `Authority Grant Fact Consumption Reference` 登记拓扑。引用必须固定现有正式授予决策、证据、主体、边界和历史事实，拥有候选、尝试、内容同一登记、完整竞争边界和四值引用解析；引用无效不得修补授予。

## 三、`AAG-IM-B2`：适用性规则竞争边界只有要求没有对象

`AAG-C-22/23` 要求规则进入完整竞争边界，但没有定义边界稳定键、候选、尝试、已登记边界、边界登记解析、独立完整性解析或最终规则解析键。

```text
Finding ID: AAG-IM-B2
Severity: BLOCKING
Result: OPEN
```

最低修复：补齐规则候选—冻结—登记与同键完整竞争边界；最终规则解析必须绑定已登记且完整边界、成功记录、失败尝试和永久空洞集合。

## 四、`AAG-IM-B3`：撤销与取代消费拓扑未闭合

`AAG-C-28/29/44` 使用“没有适用撤销”和“有效已登记撤销或取代”建立正负结果，却没有定义：

```text
Grant Lifecycle Change Semantic Key
Registered Lifecycle Change Reference
Complete Competing Change Boundary
Lifecycle Change Aggregate Resolution
Effective-at-coordinate Evaluation
Empty-set Completeness Proof
```

开放世界下，未观察到撤销不能证明没有撤销；相反撤销也不能只凭单条记录建立，而必须固定完整竞争、时间和取代顺序。

```text
Finding ID: AAG-IM-B3
Severity: BLOCKING
Result: OPEN
```

最低修复：定义只读授予生命周期变化消费包、完整边界和四值聚合；完整空集方可支持“没有适用变化”，冲突和未知必须保持不确定。

## 五、`AAG-IM-B4`：三值消费解析缺少内容同一登记链

模型规定了消费解析字段和登记授权，却没有定义：

```text
Candidate Authority Applicability Consumer Resolution
Consumer Resolution Registration Attempt
Registered Authority Applicability Consumer Resolution
Consumer Resolution Registration Resolution
Consumer Semantic Conflict Set Key
Complete Consumer Competition Boundary
Candidate / Registered Payload Digest Equality
```

因此，内部四值聚合到外部三值适配可能在登记时丢失冲突引用，或同一消费键出现不兼容三值载荷而没有失败关闭。

```text
Finding ID: AAG-IM-B4
Severity: BLOCKING
Result: OPEN
```

最低修复：为消费解析建立候选、尝试、内容同一登记、完整竞争边界、独立完整性和四值登记解析。`CONFLICTED -> INDETERMINATE` 的冲突引用必须进入不可变载荷。

## 六、累计授权缺口

四项修复新增的授予引用边界、规则边界、授予生命周期变化边界／聚合和消费解析边界操作必须加入累计授权目录，逐项固定作用域且互不传播。

该缺口作为 `AAG-IM-B1` 至 `B4` 的横切修复要求，不另计阻断数量。

## 七、已通过部分

```text
Authority Applicability Single Purpose: PASS
Grant Creation by Applicability: PROHIBITED
Qualification / Applicability Separation: PASS
S + RR + Q/K/T/B Coordinate: PASS
R8/R9 Source Lifecycle Consumption: PASS
Atomic Three-value Result: PASS
Internal Four-value Conflict Aggregate: PASS_WITH_REGISTRATION_BLOCKER
CR-0002 DM-C-07 / DM-C-08: PASS
Historical Immutability and New-identity Restatement: PASS
```

## 八、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Blocking Findings: AAG-IM-B1 through AAG-IM-B4
CR-0008-R2 Required: YES
Interface Regression after R2: REQUIRED
Independent Model Re-review after R2: REQUIRED
WS-05 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 `CR-0008-R2`，统一关闭授予事实引用、规则竞争边界、授予生命周期变化消费和三值消费解析登记四项内部阻断。
