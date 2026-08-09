# CR-0009-R1 复合独立模型复审

## 复审信息

```text
Review ID: CR-0009-R1-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Review Type: Independent Composite Proof and Exemption Applicability Governance Model Re-review
Status: COMPLETED
Result: BLOCKED
Reviewed Composite: CR-0009 + CR-0009-R1
Initial Review Basis: CR-0009-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Interface Regression Basis: CR-0009-R1-INTERFACE-REGRESSION-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: CR-0009-R1 self-check and CLOSED_AS_DRAFT declarations were ignored
Institution Freeze Created: NO
Runtime Authority Created: NO
Closed Original Finding Count: 1
Residual Original Finding Count: 3
New Blocking Finding Count: 1
Residual Blocking Finding Count: 4
Next Authorized Stage: CR-0009-R2 bounded exact registration and rank-zero repair
```

> 本文件审查 R1 自身的类型、规则、完整性、适用性聚合和授权拓扑。已通过的接口结果不用于推定内部对象完整。

## 一、总体裁决

R1 已闭合证明／豁免类型注册表，并建立严格降阶的完整性依赖方向；但零阶准入、适用性聚合登记和授权类型仍不具备精确可登记身份。复审还发现适用性规则虽然要求冻结登记，却缺少规则自身的稳定注册拓扑。

```text
PEAG-IM-B1 Type Registry Topology: CLOSED
PEAG-IM-B2 Completeness Recursion Termination: BLOCKED
PEAG-IM-B3 Applicability Registration Boundaries: BLOCKED
PEAG-IM-B4 Cumulative Authority Catalog: BLOCKED
Applicability Rule Registration Topology: BLOCKED
Residual Internal Blockers: 4
Overall Result: BLOCKED
```

## 二、`PEAG-IM-B1`：类型注册拓扑已闭合

R1 已为证明和豁免类型建立域隔离稳定键、精确候选合同、冻结—尝试—登记摘要相等、完整竞争边界、独立完整性、四值最终解析和追加式更正／取代。

```text
Finding ID: PEAG-IM-B1
Result: CLOSED
Free-form Type String Consumption: PROHIBITED
Same-key Divergent Type Contract: CONFLICTED
```

## 三、`PEAG-IM-B2`：零阶完整性准入仍可由调用方自称

R1 建立了自然数阶、严格降阶、依赖图和环检测，已经消除显式自环；但 `PEAG-R1-09` 使用“已登记原子证据”和“不可再分的提供方边界”作为零阶输入，没有定义谁以及依据什么合同判定一个对象是原子或不可再分。

缺失：

```text
Rank-zero Evidence Type Registry
Rank-zero Eligibility Semantic Key
Candidate / Attempt / Registered Eligibility Record
Complete Rank-zero Eligibility Competition Boundary
Independent Eligibility Boundary Completeness
Four-value Rank-zero Eligibility Resolution
Provider Boundary Contract and Payload Digest Pinning
```

反例：一个实际依赖高阶完整性证明的对象被调用方标记为“不可再分提供方边界”，即可绕过严格降阶规则。

```text
Finding ID: PEAG-IM-B2
Severity: BLOCKING
Result: REMAINS_OPEN
Residual Scope: Rank-zero eligibility and provider contract only
```

最低修复：建立封闭的零阶证据类型／提供方合同注册表及独立资格解析；零阶叶必须固定已登记合同、精确载荷和无高阶依赖证明。

## 四、`PEAG-IM-B3`：适用性原子边界已建立，但聚合身份不完整

R1 已为证明和豁免适用性分别定义稳定原子语义键、候选、登记、完整竞争边界和独立完整性，域间隔离通过。

但 `PEAG-R1-18/21` 只描述聚合真值与“聚合候选、尝试、记录和四值登记解析”，没有定义：

```text
Proof Applicability Aggregate Semantic Key
Exemption Applicability Aggregate Semantic Key
Aggregate Candidate Payload Contract
Aggregate Competition Boundary Key and Payload
Aggregate Boundary Registration Resolution
Aggregate Boundary Completeness Resolution
Aggregate Registration Resolution Key
Exact Atomic Registration Resolution Set Digest
```

实现仍可按结果选择原子子集，或让一个聚合候选直接成为投影输入。

```text
Finding ID: PEAG-IM-B3
Severity: BLOCKING
Result: REMAINS_OPEN
Residual Scope: Per-domain aggregate identity and registration only
```

## 五、`PEAG-IM-B4`：授权目录仍是不可登记简称

R1 使用：

```text
Type Candidate Construction / Type Registration
Completeness Dependency Graph Construction / Registration
Proof candidate computation, boundary, aggregate, projection envelope operations
```

并声明斜线两侧独立，但这些是人类可读操作组合，不是稳定 `Authority Type` 名称。证明和豁免操作仍以段落描述，没有完整枚举各自的授权类型标识。

因此不能证明授权实例具体绑定哪个操作，也不能可靠验证跨域、跨边界或跨登记阶段的权限传播。

```text
Finding ID: PEAG-IM-B4
Severity: BLOCKING
Result: REMAINS_OPEN
```

最低修复：逐项给出唯一 `... Authority Type` 名称；证明与豁免类型必须分域枚举，并固定允许稳定键、注册表、边界、输入输出、规则、阶数和证据。

## 六、`PEAG-R1-B1`：适用性规则登记拓扑未定义

CR-0009 规定适用性规则需要候选、冻结、登记和完整竞争边界；R1 只补充了相关授权简称，没有定义：

```text
Proof Applicability Rule Semantic Conflict Set Key
Exemption Applicability Rule Semantic Conflict Set Key
Candidate Rule Payload Contracts
Rule Registration Attempts and Registered Records
Per-domain Rule Competition Boundary Keys
Independent Rule Boundary Completeness
Four-value Rule Registration Resolution Keys
Candidate / Frozen / Registered Payload Equality
```

证明与豁免规则可能共享未分域边界，或同规则版本异载荷按登记时间选赢家。

```text
Finding ID: PEAG-R1-B1
Severity: BLOCKING
Result: OPEN
```

最低修复：分别为证明适用性和豁免适用性规则建立内容同一冻结登记、完整竞争边界、独立完整性和四值解析。

## 七、已通过部分

```text
Type Registry Domain Separation: PASS
Natural-number Rank: PASS
Strictly-lower-rank Dependency: PASS
Explicit Cycle Detection: PASS
Proof / Exemption Atomic Boundary Separation: PASS
Atomic Qualification Three-value: PASS
ABORTED / EXEMPT Interface Regression: PASS
Historical Immutability: PASS
```

## 八、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Closed Findings: PEAG-IM-B1
Residual Blocking Findings:
  PEAG-IM-B2
  PEAG-IM-B3
  PEAG-IM-B4
  PEAG-R1-B1
Residual Blocking Finding Count: 4
CR-0009-R2 Required: YES
Interface Regression after R2: REQUIRED
Independent Model Re-review after R2: REQUIRED
WS-06 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 `CR-0009-R2`，只修复零阶准入、适用性聚合、显式授权类型和适用性规则登记四项残余阻断。
