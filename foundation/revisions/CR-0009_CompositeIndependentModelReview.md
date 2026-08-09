# CR-0009 复合独立模型审查

## 审查信息

```text
Review ID: CR-0009-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Proof and Exemption Applicability Governance Model Review
Status: COMPLETED
Result: BLOCKED
Reviewed Proposal: CR-0009 PROOF AND EXEMPTION APPLICABILITY GOVERNANCE
Interface Basis: CR-0009-PROVIDER-AND-CONSUMER-INTERFACE-COMPATIBILITY-REVIEW
Reviewer: Codex
Review Independence: Proposal self-check declarations were ignored
Institution Freeze Created: NO
Runtime Authority Created: NO
Blocking Finding Count: 4
Next Authorized Stage: CR-0009-R1 bounded internal topology repair
```

## 一、总体裁决

模型的职责、结果分层和正向消费链正确，但类型、完整性、适用性登记和授权仍停留在要求级描述，没有形成完整可登记拓扑。

```text
Qualification / Applicability Separation: PASS
ABORTED Positive Chain: PASS
EXEMPT Positive Chain: PASS
WS-04 / WS-05 Compatibility: PASS
Type Registry Topology: BLOCKED
Completeness Recursion Termination: BLOCKED
Applicability Registration Boundaries: BLOCKED
Cumulative Authority Catalog: BLOCKED
Residual Internal Blockers: 4
Overall Result: BLOCKED
```

## 二、`PEAG-IM-B1`：类型注册表拓扑不完整

`PEAG-C-07/08` 要求类型候选、冻结、登记和竞争边界，但没有定义：

```text
Proof / Exemption Type Stable Keys
Type Candidate Payloads
Type Registration Attempts
Type Competition Boundary Keys and Payloads
Independent Type Boundary Completeness
Type Registration Resolution Keys
Correction / Supersession Lineage
```

证明类型初始枚举也不能替代已登记类型合同。

```text
Finding ID: PEAG-IM-B1
Severity: BLOCKING
Result: OPEN
```

## 三、`PEAG-IM-B2`：完整性资格与适用性存在递归自举

模型要求“完整性证明也必须资格与适用性分离”，但没有定义递归终止：完整性证明的适用性若再次要求一个合格且适用的完整性证明，会产生无限链。

缺少：

```text
Completeness Proof Rank or Well-founded Dependency Order
Rank-zero Atomic Evidence Boundary
No-self-membership Rule
Strictly-lower-rank Dependency Rule
Cycle Detection and Registration
Terminal Completeness Evaluation Contract
```

```text
Finding ID: PEAG-IM-B2
Severity: BLOCKING
Result: OPEN
```

最低修复：建立良基层级。零阶只允许外部原子证据边界和独立完整性评价；高阶完整性只能依赖严格更低阶，任何自包含或环依赖必须 `CONFLICTED` 或 `INDETERMINATE`。

## 四、`PEAG-IM-B3`：证明与豁免适用性登记边界不完整

`PEAG-C-33` 至 `C-36` 只说明应有语义键和完整边界，没有分别定义：

```text
Proof Applicability Semantic Conflict Set Key
Exemption Applicability Semantic Conflict Set Key
Candidate / Attempt / Registered Record Payloads
Per-domain Competition Boundary Keys
Boundary Registration Resolution
Independent Boundary Completeness Resolution
Four-value Aggregate and Registration Resolution
Projection Input Envelope
```

两域可能在实现中共享边界、按结果分域或直接用候选冒充登记聚合。

```text
Finding ID: PEAG-IM-B3
Severity: BLOCKING
Result: OPEN
```

## 五、`PEAG-IM-B4`：累计授权目录不可登记

`PEAG-C-42` 使用合并描述，没有逐项列出稳定授权类型，也未明确区分规则、类型、原子计算、登记、竞争边界、完整性、聚合、适配信封和投影构建。

```text
Finding ID: PEAG-IM-B4
Severity: BLOCKING
Result: OPEN
```

最低修复：逐操作枚举授权类型，并固定允许类型／规则／稳定键／注册表／边界／输入输出／证据／有效窗口及 `Can Change`、`Cannot Change`；全部互不传播。

## 六、已通过部分

```text
Type Name != Qualification: PASS
Atomic Qualification Three-value: PASS
Aggregate Qualification Four-value: PASS
Proof Applicability Four-value: PASS
Exemption Applicability Four-value: PASS
Missing Source Safety: PASS
Historical Immutability: PASS
Forward Certainty Non-amplification: PASS
CR-0002 / CR-0003 Consumer Interfaces: PASS
```

## 七、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Blocking Findings: PEAG-IM-B1 through PEAG-IM-B4
CR-0009-R1 Required: YES
Interface Regression after R1: REQUIRED
Independent Model Re-review after R1: REQUIRED
WS-06 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 `CR-0009-R1`，关闭类型注册、完整性良基终止、适用性登记边界和累计授权四项内部阻断。
