# CR-0002 外部治理依赖闭合计划

## 计划信息

```text
Plan ID: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Plan Type: Non-authoritative External Governance Dependency Closure Plan
Status: COMPLETED
Result: PLAN_ESTABLISHED
Executable: NO
Authority: NONE
Planning Basis: CR-0002-FREEZE-DEPENDENCY-READINESS-AUDIT
Target Candidate: CR-0002-CONSTITUTION-CANDIDATE
Workstream Count: 9
Planner: Codex
Planning Authority: User-delegated planning authority
External Approval Required: NO
Dependency Institution Created: NO
Compatibility Decision Created: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
Next Authorized Stage: WS-01 proposal drafting only after explicit continuation
```

> 本文件只组织九类外部治理依赖的提案、审查、实现证据与冻结准备工作。它不是任何依赖制度的提案正文，不创建兼容性事实，不授予运行时或冻结权威，也不改变 `CR-0002` 当前的 `NOT_READY_FOR_FREEZE` 结论。

## 一、计划目标

本计划把冻结准备度审计中的九类缺失依赖转化为有顺序、有边界、有退出条件的工作流：

```text
Missing Dependency
  -> Bounded Workstream
  -> Independent Proposal
  -> Independent Model Review
  -> Compatibility Review
  -> Governed Implementation Evidence
  -> IF-0007 Evidence Review
  -> Applicable Freeze Process
```

本阶段只完成工作流设计，不执行后六个阶段。

### 完成条件

计划只有同时满足以下条件才算建立：

- 九类依赖全部拥有唯一工作流标识；
- 每个工作流均声明对象、输入、输出、权威边界和禁止职责；
- 依赖先后关系不存在循环；
- 制度注册表的启动闭环被显式处理；
- 每个工作流均有独立退出门槛；
- 提案通过、接口兼容、运行证据和制度冻结保持分离；
- 不通过计划文本制造任何现行制度或运行事实。

### 非目标

- 不建立新的 `CR-0002` 修订覆盖层；
- 不修改决策模型候选正文；
- 不把九类依赖合并为一个拥有混合权威的超级制度；
- 不在本轮建立实现、运行样本或经验性证据；
- 不指定冻结权威或作出冻结决定；
- 不创建 `foundation/07_Decision.md`。

## 二、统一工作流规则

### 工作流不是制度

工作流标识只用于计划和追踪：

```text
WS-01 ... WS-09
```

它们不是提案编号、制度版本、冻结标识或运行时注册表标识。后续每个正式提案必须另行分配唯一提案编号，并在元数据中声明：

```text
Status: DRAFT or PROPOSAL
Authority: NONE
Executable: NO
Institution Freeze Created: NO
```

### 每个工作流必须保持的分离

```text
Proposal Completeness
!= Model Consistency
!= Interface Compatibility
!= Implementation Compatibility
!= Runtime Evidence Sufficiency
!= Institution Freeze Eligibility
!= Institution Freeze
```

任一前项通过都不得反向推断后项已经成立。

### 每个提案的最低结构

每个工作流提案至少必须定义：

1. 单一制度目的和明确非目标；
2. 权威对象、权威来源、作用域和有效窗口；
3. 规范输入、规范输出与稳定身份；
4. 登记、计算、发布、审查和更正的分权；
5. 状态代数、未知、冲突和失败关闭行为；
6. 时间坐标、双时间边界和版本演进；
7. 内容同一、不可变历史、更正与失效；
8. 证据要求、完整性证明和禁止自证；
9. 与 `IF-0001`、`IF-0006`、`IF-0007` 的兼容关系；
10. 与 `CR-0002`、`CR-0003` 及相邻依赖的接口映射；
11. 迁移、替代和历史保留方式；
12. 非法状态与独立审查门槛。

### 合并限制

九类依赖是九个独立审计门槛，不等于必须生成九个物理文件。只有独立审查证明以下条件全部成立时，两个工作流才可共享一个提案载体：

- 制度目的没有混合；
- 权威对象没有合并；
- 写入和计算权威没有传播；
- 状态代数没有被压缩；
- 版本、时间和证据边界可分别审计；
- 任一工作流可独立拒绝、修订或迁移。

否则必须保持独立提案。

## 三、工作流总表

| 工作流 | 依赖门槛 | 核心产物 | 直接上游 | 当前状态 |
|---|---|---|---|---|
| `WS-01` | `Institution Registry and Freeze Reference Support` | 制度注册表、冻结账本和引用验证制度提案 | `IF-0001`、`IF-0006`、`IF-0007` | `PLANNED` |
| `WS-02` | `Source Registry Interface` | 来源注册表及快照完整性接口提案 | `WS-01` 接口基线 | `PLANNED` |
| `WS-03` | `Temporal Mapping Governance` | 规范时间和双时间映射治理提案 | `WS-01` 接口基线 | `PLANNED` |
| `WS-04` | `Qualification Governance` | 资格规则、兼容域与演进治理提案 | `WS-02`、`WS-03` | `PLANNED` |
| `WS-05` | `Authority Applicability Governance` | 权威和来源适用性解析治理提案 | `WS-02`、`WS-03` | `PLANNED` |
| `WS-06` | `Proof and Exemption Applicability Governance` | 证明与豁免资格、适用性治理提案 | `WS-04`、`WS-05` | `PLANNED` |
| `WS-07` | `Derived Record Registration Governance` | 逐类型登记授权和内容同一治理提案 | `WS-01`、`WS-02`、`WS-03`、`WS-06` | `PLANNED` |
| `WS-08` | `Dependency Closure Governance` | 闭包、完整性、根解析和摘要治理提案 | `WS-02`、`WS-03`、`WS-07` | `PLANNED` |
| `WS-09` | `Projection Audit and Publication Interface` | 投影审计登记与发布接口提案 | `WS-03`、`WS-07`、`WS-08` | `PLANNED` |

`PLANNED` 只表示本文件定义了工作边界，不表示提案已经创建、审查通过、兼容或冻结。

## 四、WS-01 制度注册表与冻结引用支持

### 目的

建立能够验证制度身份、版本、摘要、冻结决定、冻结权威、证据包、有效作用域和有效时间的权威接口。

### 必须定义

```text
Institution Identity and Version
Institution Registry Authority
Freeze Ledger Authority
Frozen Content Digest Contract
Freeze Evidence Package Reference
Freeze Authority Reference
Freeze Decision Reference
Effective Scope and Validity Interval
Freeze Reference Resolver
Revocation, Supersession and Correction History
```

### 启动闭环

该工作流不能假设注册表已经存在来证明注册表制度自身的合法性。提案必须明确一个受 `IF-0007` 约束的启动路径：

```text
Existing Frozen Institution Documents
  -> Immutable Bootstrap Evidence Package
  -> Independent Bootstrap Review
  -> Applicable Bootstrap Freeze Authority
  -> Bootstrap Freeze Decision
  -> First Registry Entry Set
  -> Normal Registry-governed Evolution
```

启动路径不得：

- 事后伪造 `IF-0001` 至 `IF-0007` 的历史；
- 把文件路径或 `Status: FROZEN` 单独当作可验证冻结引用；
- 让注册表解析器创建冻结决定或冻结权威；
- 让制度自登记、自审查和自冻结。

### 退出门槛

```text
Proposal Completeness: PASS
Bootstrap Closure: PASS
Authority Separation: PASS
History Preservation: PASS
Independent Model Review: PASS
CR-0002 / CR-0003 Interface Compatibility: PASS
Institution Freeze: NOT_INFERRED
```

## 五、WS-02 来源注册表接口

### 目的

建立来源身份、作用域、快照、完整性和变化历史的权威提供侧制度，使 `CR-0002` 不再只拥有消费字段。

### 必须定义

```text
Source Registry ID and Authority
Source Identity and Stable Position
Registry Scope
Open-world or Closed-world Boundary
Snapshot Coordinate and Digest
Snapshot Completeness
Source Applicability Change Record
Multi-registry Boundary
Version and Temporal Semantics
```

来源注册表只能证明来源集合、位置、作用域和快照事实，不得决定资格、权威适用性、提交结果或投影结论。

### 退出门槛

```text
Authoritative Provider-side Contract: PASS
Completeness Non-self-proof: PASS
Snapshot Reproducibility: PASS
Multi-registry Conflict Preservation: PASS
WS-01 Reference Compatibility: PASS
Independent Model Review: PASS
```

## 六、WS-03 时间映射治理

### 目的

建立规范事件时间、知识时间、记录时间、审查时间和系统时间的不可互换边界，以及旧字段进入规范字段的版本化映射。

### 必须定义

```text
Canonical Temporal Field Registry
Valid-time and Transaction-time Semantics
Knowledge Boundary
Observed At / Recorded At / Reviewed At Separation
Legacy Field Mapping Rule
Mapping Rule Version
Mapping Evidence and Confidence
Indeterminate and Conflict Behavior
Temporal Correction and Migration
```

时间映射权威只能登记可证映射，不得用当前知识重写历史当时知识，也不得把映射结果升级为合法性或提交结论。

### 退出门槛

```text
Canonical Time Separation: PASS
Bitemporal Append-only Semantics: PASS
Legacy Mapping Determinism: PASS
Historical Knowledge Boundary: PASS
WS-01 Reference Compatibility: PASS
Independent Model Review: PASS
```

## 七、WS-04 资格治理

### 目的

建立依据、证明和豁免所消费的资格规则、资格计算、规则兼容域和演进边界。

### 必须定义

```text
Qualification Rule Identity and Version
Allowed Subject and Basis Types
Qualification Computation Authority
Qualification Registration Authority
Qualification Result Algebra
Semantic Compatibility Record
Compatibility Domain Snapshot
Forward Interpretation Contract
Rule Change and Requalification Boundary
Institutional Source Exclusion Basis
```

资格治理不得决定权威是否适用、决策是否准入、提交是否成功或目标是否迁移。

### 退出门槛

```text
Qualification / Applicability Separation: PASS
Four-value Proof-facing Compatibility: PASS
Forward Interpretation Safety: PASS
Rule Evolution and Requalification: PASS
WS-02 / WS-03 Compatibility: PASS
Independent Model Review: PASS
```

## 八、WS-05 权威适用性治理

### 目的

建立权威在特定对象、版本、作用域和时间坐标上的适用性解析，以及来源适用性变化的权威边界。

### 必须定义

```text
Authority Grant Reference
Authority Scope and Version
Object and Decision Coordinates
Applicability Computation Authority
Applicability Registration Authority
Applicability Result Algebra
Source Applicability Input
Conflict Preservation
Change, Revocation and Expiry
```

适用性治理不得创建权威授予、扩张权威作用域、代替资格判断或创建决策事实。

### 退出门槛

```text
Grant / Applicability Separation: PASS
Authority Non-propagation: PASS
Coordinate Completeness: PASS
Conflict Preservation: PASS
WS-02 / WS-03 Compatibility: PASS
Independent Model Review: PASS
```

## 九、WS-06 证明与豁免适用性治理

### 目的

闭合未应用证明和豁免的资格、适用性、完整性、冲突、失效与规则演进，使 `ABORTED` 和 `EXEMPT` 只能由完整正向链支持。

### 必须定义

```text
Proof Type and Exemption Type Registry
Proof Qualification Rule
Proof Applicability Rule
Exemption Qualification Rule
Exemption Applicability Rule
Applicability Scope and Coordinate
Completeness Authority and Evidence
Rule Version and Evolution
Conflict, Revocation and Expiry
Forward Interpretation Boundary
```

该制度不得让类型名称直接证明资格，不得让缺失来源等同于未应用，不得让一个权威同时自证证明内容和完整性。

### 退出门槛

```text
Qualification / Applicability Separation: PASS
Proof / Completeness Authority Separation: PASS
ABORTED Positive Chain: PASS
EXEMPT Positive Chain: PASS
Conflict and Evolution Contract: PASS
WS-04 / WS-05 Compatibility: PASS
Independent Model Review: PASS
```

## 十、WS-07 派生记录登记治理

### 目的

建立逐记录类型授权、登记尝试、候选载荷与已登记载荷内容同一、幂等和更正边界。

### 必须定义

```text
Derived Record Type Registry
Per-type Registration Authority Instance
Authority Scope and Validity Window
Registration Attempt Record
Candidate Payload Digest
Registered Payload Digest
Content Identity Verification
Stable Registration Key
Idempotency and Duplicate Handling
Correction and Supersession Boundary
```

通用登记接口不得传播具体记录类型权威；登记者不得修改候选载荷，不得把登记升级为决策、提交或发布。

### 退出门槛

```text
Per-type Authority Topology: PASS
Registration Attempt Preservation: PASS
Content Identity: PASS
Idempotency: PASS
Correction History: PASS
WS-01 / WS-02 / WS-03 / WS-06 Compatibility: PASS
Independent Model Review: PASS
```

## 十一、WS-08 依赖闭包治理

### 目的

建立根解析、必需边、注册表作用域、闭包摘要、完整性登记和变化传播边界。

### 必须定义

```text
Closure Root and Coordinate
Required Edge Rule and Version
Registry Scope Set
Closure Computation Authority
Closure Completeness Authority
Registered Closure Identity
Closure Digest
Missing Edge and Conflict Behavior
Incremental Rebuild and Invalidation
Propagation Input Boundary
```

闭包计算不得自证完整，摘要不得替代已登记完整性，传播只能消费已提交的适用性变化事实。

### 退出门槛

```text
Computation / Completeness Separation: PASS
Root and Required-edge Determinism: PASS
Registry Scope Completeness: PASS
Missing and Conflict Preservation: PASS
Rebuild and Invalidation: PASS
WS-02 / WS-03 / WS-07 Compatibility: PASS
Independent Model Review: PASS
```

## 十二、WS-09 投影审计与发布接口

### 目的

建立候选投影、审计登记、内容同一发布、当前视图删除与重建、失效和更正感知边界。

### 必须定义

```text
Projection Type and Contract Scope
Projection Stable Key
View Mode
Input Closure Reference
Candidate Projection Record
Projection Audit Registration Authority
Publication Authority
Published Payload Digest
Content Identity Verification
Correction and Invalidation Consumption
Deletion and Rebuild Contract
```

投影不得创建决策事实、提交结果、失效决定或行动权威；发布者不得修改已审计载荷。

### 退出门槛

```text
Projection / Fact Separation: PASS
Audit / Publication Authority Separation: PASS
Content-identical Publication: PASS
Closure Completeness Consumption: PASS
Correction-aware Rebuild: PASS
WS-03 / WS-07 / WS-08 Compatibility: PASS
Independent Model Review: PASS
```

## 十三、执行波次与并行边界

### 波次 0：当前计划

```text
Closure Plan -> COMPLETED
Institutions Created -> 0
```

### 波次 1：启动基础

```text
WS-01 Institution Registry and Freeze Reference Support
```

`WS-01` 必须先闭合模型级启动路径。没有该路径时，后续提案可以起草，但不得宣称拥有可验证冻结引用。

### 波次 2：共同坐标

```text
WS-02 Source Registry Interface
WS-03 Temporal Mapping Governance
```

两者可以并行起草，必须在独立审查前执行交叉接口检查。

### 波次 3：解析治理

```text
WS-04 Qualification Governance
WS-05 Authority Applicability Governance
```

两者可以并行，但必须保持资格和适用性分权，并共同消费已审查的来源与时间接口。

### 波次 4：证明与登记

```text
WS-06 Proof and Exemption Applicability Governance
  -> WS-07 Derived Record Registration Governance
```

`WS-07` 可提前起草通用登记骨架，但逐类型授权和载荷契约必须等待 `WS-06` 类型闭合后完成。

### 波次 5：闭包与投影

```text
WS-08 Dependency Closure Governance
  -> WS-09 Projection Audit and Publication Interface
```

终局投影只能消费已登记且完整的闭包，因此两者不得倒置。

### 波次 6：联合兼容性审查

九个工作流模型审查通过后，必须执行一次联合接口审查：

```text
Nine Dependency Proposals
+ CR-0002-CONSTITUTION-CANDIDATE
+ CR-0003 Compatible Commit Candidate
-> Cross-model Interface Compatibility Review
```

联合审查必须检查类型同名异义、稳定键、时间字段、状态代数、摘要算法、权威传播和失败关闭是否一致。

## 十四、各阶段状态推进

每个工作流只能沿以下状态推进：

```text
PLANNED
  -> DRAFTED
  -> MODEL_REVIEW_REQUIRED
  -> MODEL_CONSISTENT
  -> INTERFACE_REVIEW_REQUIRED
  -> INTERFACE_COMPATIBLE
  -> IMPLEMENTATION_EVIDENCE_REQUIRED
  -> IMPLEMENTATION_COMPATIBLE
  -> IF-0007_EVIDENCE_REQUIRED
  -> FREEZE_REVIEW_ELIGIBLE
```

`FREEZE_REVIEW_ELIGIBLE` 仍不是 `FROZEN`。冻结必须由适用冻结权威依据独立冻结审查、冻结决定和成功制度提交另行成立。

任一阶段失败时：

```text
Preserve Evidence
Preserve Review History
Create Bounded Revision
Do Not Advance Downstream Gate
```

## 十五、证据计划

### 模型与接口证据

每个工作流至少保存：

- 提案版本和不可变摘要；
- 规则到审查发现的映射；
- 相邻接口字段与状态代数映射；
- 独立审查者、审查范围和结论；
- 未解决阻断及其有界修订记录。

### 实现证据

只有九类模型兼容后，才进入受控实现。运行证据至少绑定：

```text
Execution ID
Implementation Version
Institution Proposal Version
Input and Output References
Authority and Scope References
Observed At and Recorded At
Immutable Evidence Digest
Expected and Observed Behavior
Failure-closed Result
```

### IF-0007 证据

运行样本必须支持独立评估：

```text
Repeated
Stable
Cross Provider
Cross Project
Cross Domain
Migration
```

计划、模板、模拟字段和模型审查不能替代这些现实证据。

## 十六、计划级验证矩阵

```text
Nine Workstreams Identified: PASS
Unique Workstream Boundaries: PASS
Dependency Order Defined: PASS
Dependency Cycle Observed: NO
Bootstrap Closure Explicit: PASS
Parallel Boundaries Defined: PASS
Per-workstream Exit Gates Defined: PASS
Proposal / Compatibility / Evidence / Freeze Separation: PASS
CR-0002 Model Expansion Required: NO
Dependency Proposals Created: NO
Compatibility Decisions Created: NO
Runtime Evidence Created: NO
Institution Freeze Created: NO
CR-0002 Freeze Readiness Changed: NO
Plan Result: PLAN_ESTABLISHED
```

## 当前决定

1. 接受九类外部治理依赖为九个独立审计工作流；
2. 接受 `WS-01` 至 `WS-09` 的先后顺序和并行边界；
3. 不把工作流标识当作提案编号、制度版本或冻结标识；
4. 不创建任何兼容性、运行证据或冻结事实；
5. 不修改 `CR-0002` 候选及其历史审查；
6. 下一阶段只起草 `WS-01` 制度注册表与冻结引用支持提案；
7. `WS-01` 必须优先闭合启动路径、分权、摘要、历史和验证接口；
8. `WS-01` 未通过独立模型审查前，不进入后续工作流的正式兼容性判断。
