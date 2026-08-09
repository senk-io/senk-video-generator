# CR-0007-R4 复合独立模型复审

## 复审信息

```text
Review ID: CR-0007-R4-COMPOSITE-INDEPENDENT-MODEL-REREVIEW
Review Type: Independent Composite Qualification Governance Model Re-review
Status: COMPLETED
Result: BLOCKED
Reviewed Composite: CR-0007 + CR-0007-R1 + CR-0007-R2 + CR-0007-R3 + CR-0007-R4
Repair Basis: CR-0007-R3-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Interface Regression Basis: CR-0007-R4-UPSTREAM-AND-CONSUMER-INTERFACE-REGRESSION-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: CR-0007-R4 self-check and CLOSED_AS_DRAFT declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
Reviewed Findings: QG-IM-B1 through QG-IM-B4
Closed Finding Count: 2
Residual Blocking Finding Count: 2
Next Authorized Stage: CR-0007-R5 bounded registration-boundary repair
```

> 本文件独立复验 `R4` 对四项内部阻断的修复。接口回归通过只作为边界事实，不用于推定内部登记解析完整。

## 一、总体裁决

`R4` 已补齐累计授权目录，并为原子评价记录建立了登记完整边界、独立完整性解析和集合相等约束。规则与治理工件也已具备候选、冻结、尝试、内容同一和四值解析链，但两类四值解析都没有固定“全部竞争登记记录、失败尝试和永久空洞”的已登记边界及其独立完整性，因此仍无法证明 `NOT_REGISTERED` 或排除隐藏冲突。

```text
QG-IM-B1 Rule Registration Topology: BLOCKED
QG-IM-B2 Composite Authority Catalog: CLOSED
QG-IM-B3 Atomic Evaluation Boundary and Completeness: CLOSED
QG-IM-B4 Governance Artifact Content-identical Registration: BLOCKED
Upstream and Consumer Interface Regression: PASS
Residual Internal Blockers: 2
Overall Result: BLOCKED
```

## 二、`QG-IM-B1`：规则登记解析缺少完整竞争边界

### 已关闭部分

`R4` 已定义：

```text
Rule Semantic Conflict Set Key
Candidate Qualification Rule Record
Qualification Rule Registration Attempt
Registered Qualification Rule Record
Candidate / Frozen / Registered Payload Digest Equality
Four-value Qualification Rule Registration Resolution
Registered Singleton Consumption Gate
```

### 残余阻断

`QG-R4-06` 的 `Expected Registry Boundary` 只是登记尝试字段；`QG-R4-08` 使用“完整边界”支持 `NOT_REGISTERED`，但复合模型没有定义：

```text
Qualification Rule Registration Boundary Stable Key
Candidate Rule Registration Boundary
Boundary Registration Attempt
Registered Rule Registration Boundary
Exact Competing Attempt and Record Set Digest
Permanent Hole Set Digest
Rule Boundary Registration Resolution
Independent Rule Boundary Completeness Resolution
Rule Registration Resolution Key bound to the registered complete boundary
```

反例：同一规则语义冲突键下，观察到内容 `A` 的成功登记，但另一个分区存在内容 `B` 的成功登记或未纳入的失败尝试。当前四值解析可以只依据 `A` 宣称 `REGISTERED`，不能证明竞争集合完备。

```text
Finding ID: QG-IM-B1
Result: REMAINS_OPEN
Severity: BLOCKING
Residual Scope: Rule Registration Boundary and Completeness only
```

## 三、`QG-IM-B2`：累计授权目录已闭合

`QG-R4-10` 已累计列出输入组装、映射证明、完整性包、原子计算与登记、边界构造与登记、完整性资格与登记、冲突聚合、消费信封和治理工件操作。`QG-R4-11` 固定完整作用域，`QG-R4-12` 禁止权威传播。

```text
Finding ID: QG-IM-B2
Result: CLOSED
Implicit Authority Inheritance: PROHIBITED
Missing / Expired / Conflicted Authority: FAIL_CLOSED
```

## 四、`QG-IM-B3`：原子评价边界及完整性已闭合

`R4` 已建立：

```text
Atomic Qualification Evaluation Semantic Key
Atomic Qualification Record Evaluation Boundary Key
Candidate / Attempt / Registered Boundary / Four-value Resolution
Registered Atomic Evaluation Boundary Completeness Resolution
Expected and Observed Set Digests
Failed Attempt and Hole Coverage Proofs
Qualification Conflict Aggregate Key bound to registered complete boundary
INVALID_SUBSET failure
```

完整边界覆盖成功、失败、永久空洞和冲突谱系；边界构造者、聚合者和资格计算者不能自证完整。

```text
Finding ID: QG-IM-B3
Result: CLOSED
Favorable Subset Selection: PROHIBITED
Aggregate over Incomplete Boundary: FAIL_CLOSED
```

## 五、`QG-IM-B4`：治理工件登记解析缺少完整竞争边界

### 已关闭部分

`R4` 已为四类治理工件建立封闭类型、逐类型稳定键、统一候选信封、先冻结后登记、内容同一摘要、四值解析、追加式更正和登记冻结单例消费门。

### 残余阻断

工件四值解析仍缺少逐稳定键的已登记完整竞争边界。模型没有定义：

```text
Governance Artifact Registration Boundary Stable Key
Candidate Artifact Registration Boundary
Boundary Registration Attempt
Registered Artifact Registration Boundary
Exact Competing Artifact Attempt and Record Set Digest
Permanent Hole Set Digest
Artifact Boundary Registration Resolution
Independent Artifact Boundary Completeness Resolution
Artifact Registration Resolution Key bound to the registered complete boundary
```

仅规定“同键异内容必须 `CONFLICTED`”不足以证明已观察到全部同键登记。兼容域成员、兼容分类、前向映射或重新资格范围的隐藏竞争记录仍可能被遗漏。

```text
Finding ID: QG-IM-B4
Result: REMAINS_OPEN
Severity: BLOCKING
Residual Scope: Governance Artifact Registration Boundary and Completeness only
```

## 六、最小修复边界

下一版只需为规则登记和治理工件登记补齐同构的竞争边界拓扑：

1. 固定边界稳定键和规范边界载荷；
2. 保留候选、登记尝试、已登记边界和四值边界登记解析；
3. 精确覆盖成功记录、失败尝试和永久空洞；
4. 由独立完整性权威登记四值完整性解析；
5. 最终对象登记解析必须固定已登记且完整的边界；
6. 禁止解析者、登记者或消费者自选竞争子集。

不得修改已经通过的上游消费、原子三值、聚合四值、提交契约作用域或证明身份。

## 七、当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
Closed Findings: QG-IM-B2 + QG-IM-B3
Residual Blocking Findings: QG-IM-B1 + QG-IM-B4
Residual Blocking Finding Count: 2
CR-0007-R5 Required: YES
Interface Regression after R5: REQUIRED
Independent Composite Model Re-review after R5: REQUIRED
WS-04 Model Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 `CR-0007-R5`，只关闭规则与治理工件登记竞争边界及独立完整性。
