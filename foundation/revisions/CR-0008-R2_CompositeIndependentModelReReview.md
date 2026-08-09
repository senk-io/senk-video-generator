# CR-0008-R2 复合独立模型复审

## 复审信息

```text
Review ID: CR-0008-R2-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Review Type: Independent Composite Authority Applicability Governance Model Re-review
Status: COMPLETED
Result: BLOCKED
Reviewed Composite: CR-0008 + CR-0008-R1 + CR-0008-R2
Initial Review Basis: CR-0008-R1-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Interface Basis: CR-0008-R2-INTERFACE-REGRESSION-REVIEW
Reviewer: Codex
Review Independence: CR-0008-R2 self-check declarations were ignored
Institution Freeze Created: NO
Runtime Authority Created: NO
Closed Original Finding Count: 1
Partially Closed Original Finding Count: 3
Residual Blocking Finding Count: 2
Next Authorized Stage: CR-0008-R3 exact boundary and authority catalog repair
```

## 一、总体裁决

R2 已正确建立不创造授予的正式事实引用路径，并闭合规则竞争边界。授予生命周期和消费解析也具备语义键及共同拓扑，但共同拓扑没有形成逐类型稳定边界键；累计授权使用合并描述，不能证明每项新增操作拥有可登记授权类型。

```text
AAG-IM-B1 Grant Fact Reference Provider: PARTIAL
AAG-IM-B2 Rule Registration Boundary: CLOSED
AAG-IM-B3 Lifecycle Change Consumption: PARTIAL
AAG-IM-B4 Consumer Resolution Registration: PARTIAL
Exact Per-type Competition Boundary Identity: BLOCKED
Explicit Cumulative Authority Catalog: BLOCKED
Residual Internal Blockers: 2
Overall Result: BLOCKED
```

## 二、已关闭：规则登记边界

规则拥有稳定竞争边界键、候选／冻结／登记全集、独立完整性和封闭真值表。唯一冻结内容单例、完整零成功、异内容冲突和未知分支均已区分。

```text
Finding ID: AAG-IM-B2
Result: CLOSED
```

## 三、`AAG-R2-B1`：三类对象缺少逐类型边界身份

共同拓扑只规定“每个边界固定语义冲突键、注册表、证据边界和集合”，但没有给以下三类边界定义精确稳定键和载荷：

```text
Grant Fact Reference Competition Boundary
Grant Lifecycle Change Reference Competition Boundary
Authority Applicability Consumer Resolution Competition Boundary
```

缺失字段包括边界键、观察切口、候选／成功／失败／空洞／谱系集合摘要、边界候选和登记载荷摘要、边界登记解析键及完整性解析键。通用文字不能防止实现按结果、记录类型或时间形成不同边界。

```text
Finding ID: AAG-R2-B1
Severity: BLOCKING
Result: OPEN
Impacts: residual AAG-IM-B1 + AAG-IM-B3 + AAG-IM-B4
```

最低修复：逐类型定义边界键、规范载荷、候选—尝试—登记链、独立完整性和最终对象解析绑定。

## 四、`AAG-R2-B2`：累计授权目录不可登记

`AAG-R2-23` 用“构造／登记／边界／完整性／解析”合并描述授权，没有列出稳定授权类型名称，也未区分：

```text
Boundary Construction
Boundary Registration
Boundary Completeness Qualification
Boundary Completeness Registration
Object Resolution Execution
Object Resolution Registration
Lifecycle Aggregate Execution
Lifecycle Aggregate Registration
```

`AAG-C-50` 的作用域格式不能替代授权类型本身。实现仍可能把构造、登记、完整性、聚合和解析合并到一个泛化授权。

```text
Finding ID: AAG-R2-B2
Severity: BLOCKING
Result: OPEN
Cross-cutting Impact: AAG-IM-B1 through AAG-IM-B4
```

最低修复：逐项枚举授权类型，并固定允许对象、稳定键、边界、注册表、输入输出、规则、证据和不可变字段；所有授权互不传播。

## 五、已通过部分

```text
Formal Grant Fact Non-creation: PASS
Authority -> Decision -> Evidence -> Formal Fact Chain: PASS
Open-world Revocation Absence Safety: PASS
Lifecycle Four-value Aggregate: PASS_WITH_BOUNDARY_BLOCKER
Three-value Consumer Adaptation: PASS_WITH_BOUNDARY_BLOCKER
Upstream Interface Regression: PASS
CR-0002 Consumer Regression: PASS
```

## 六、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Residual Blocking Findings: AAG-R2-B1 + AAG-R2-B2
CR-0008-R3 Required: YES
Interface Regression after R3: REQUIRED
Independent Model Re-review after R3: REQUIRED
WS-05 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 R3，精确补齐三类边界身份和累计授权目录。
