# CR-0003-R3 独立制度审查

## 审查信息

```text
Review ID: CR-0003-R3-LOCAL-REVIEW
Review Type: Independent Foundation Model Review
Status: COMPLETED
Result: PASS_WITH_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0003-R3
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Evidence Scope: Local frozen institutions, proposal history and object graph
External Approval Required: NO
Institution Freeze Created: NO
```

> 本文件是本地独立审查记录，不是制度冻结。历史对话和外部模型回复只作为问题发现材料，不构成审查权威或结论依据。

## 审查范围

本轮检查：

1. 提交尝试身份是否确实先于目标权威写入；
2. 候选记录和登记记录是否内容同一；
3. 字段存在性是否能够失败关闭；
4. 当前解析投影是否仍会覆盖历史；
5. 每项运行时行为是否拥有适用权威；
6. `ABORTED` 的证明资格是否具有合法登记边界；
7. 解析序列在并发下是否唯一、可重建；
8. 跨规则版本投影是否具有确定语义；
9. 提案是否满足正式冻结门槛。

## 总体裁决

`CR-0003-R3` 已经正确解决第二修订版留下的六项精确化问题：

- 尝试初始化先于提交点；
- 完成观察不再承担结果真源；
- 规范字段区分具体值、不适用和未解析；
- 候选解析持久且不可变；
- 登记记录只能增加内容相同的授权外壳；
- 当前投影是可重建派生读面；
- `CONFLICTED` 只属于投影层；
- `ABORTED` 不自动授权重试。

这些修改全部通过。

但本轮发现四项模型阻断：

1. 候选解析、目标读取、状态解析和投影构建缺少完整执行授权类型；
2. `Non-application Proof Bundle` 缺少资格角色、资格权威和资格记录；
3. 解析序列缺少并发唯一性、分支和账本位置不变量；
4. 投影规则缺少跨解析规则版本的兼容性契约。

此外存在两个独立冻结门槛：

1. 依赖的 `CR-0002-R1 Decision Model` 尚未冻结；
2. 尚未建立满足 `IF-0007` 的制度冻结证据包和冻结权威记录。

因此：

```text
Model Direction: PASS
Freeze Review Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 已通过一：尝试身份顺序

```text
Commit Attempt Initiation Record
  -> Commit-point Preconditions
  -> Protected Authoritative Write
```

权威迁移记录只能引用已经登记的尝试身份。初始化记录失败会阻断提交点和受保护写入。

完成观察被拆成独立 `Commit Attempt Completion Record`，即使完成记录缺失，初始化记录和权威迁移记录仍允许后续对账。

```text
Attempt Identity Ordering: PASS
History Preservation: PASS
```

## 已通过二：字段存在性

```text
VALUE(value)
NOT_APPLICABLE(reason)
UNRESOLVED(reason)
```

三种语义已经明确分离，并被纳入规范化摘要。静默省略、`VALUE(null)`、不适用和未解析不会被压缩成同一空值。

```text
Field Presence Semantics: PASS
Fail-closed Semantics: PASS
```

## 已通过三：候选与登记内容同一性

候选记录持久保存在未登记解析账本。登记记录引用候选记录，并要求：

```text
Candidate Content Digest
= Registered Content Digest
```

摘要覆盖同一规范化解析本体，不覆盖授权外壳。登记器不能把候选结果重写为另一结果。

```text
Candidate Persistence: PASS
Registration Content Identity: PASS
```

## 已通过四：当前解析投影

当前投影被正确分类为可重建派生读面，不是正式事实、历史记录或最后写入获胜字段。

```text
Single Resolution Outcome:
  COMMITTED | ABORTED | INDETERMINATE

Current Commit Resolution Projection:
  COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

`CONFLICTED` 没有污染单次提交结果模型。投影缓存可以重建，不能修改来源解析历史。

```text
Projection Type Boundary: PASS
Single-result Three-value Model: PASS
```

## 已通过五：重试权威分离

```text
Commit Outcome = ABORTED
-/-> Retry Authorized
```

是否重试仍由策略根据决策效力、契约、源版本、预算、冲突行为和历史独立决定。

```text
Commit / Policy Separation: PASS
```

## 阻断一：运行时执行授权覆盖不完整

### 问题

提案明确了：

```text
Commit Execution Authority
Commit Resolution Registration Authority
Target State Resolution Registration Authority
```

但以下运行时行为仍只有角色和能力，没有独立适用授权：

```text
Commit Resolver -> computes and persists candidate resolution
Target Reader -> reads target authority and creates read record
Target State Resolver -> computes and persists candidate state resolution
Projection Builder -> computes or materializes current projection
```

`A-01` 要求任何执行先有对应权威；登记权威不能反向授权候选计算和读取，提交执行权威也不能隐式传播给解析器和投影器。

```text
Registration Authority
-/-> Resolution Execution Authority

Commit Execution Authority
-/-> Read or Projection Authority
```

### 必须补充

提交契约或适用制度必须分别声明：

```text
Commit Resolution Execution Authority Type
Target Read Authority Type
Target State Resolution Execution Authority Type
Resolution Projection Execution Authority Type
```

每项授权必须限定主体、输入来源、对象范围、规则版本、允许产生的候选记录或派生读面、有效期和禁止行为。

### 裁决

```text
Authority Completeness: FAIL
Risk Level: HIGH
Required Action: CR-0003-R4
```

## 阻断二：未应用证明缺少资格边界

### 问题

`Non-application Proof Bundle` 被描述为引用“合格证据”的值对象，但模型没有定义：

- 谁组装候选证明；
- 谁判断证明符合具体提交契约；
- 哪项权威允许登记资格结论；
- 资格结论保存在哪里；
- 资格记录如何绑定证明类型、版本、封闭范围和完整性保证。

```text
Evidence References
-/-> Qualified Non-application Proof
```

如果解析器自行认定证据合格，它会同时计算结果并为自身输入提供资格证明，违反权威不得自证和候选计算不得自动成为正式依据的边界。

### 必须补充

需要建立或显式依赖：

```text
Non-application Proof Assembler = execution role
Candidate Non-application Proof Bundle = candidate value/record
Non-application Proof Qualifier = qualification role
Non-application Proof Qualification Authority = authority grant
Non-application Proof Qualification Record = immutable qualification record
```

资格记录只判断证明包是否满足指定提交契约的准入要求，不证明目标迁移“客观不存在”，也不直接产生 `ABORTED`。提交解析器只能引用已获得适用资格的证明包。

该边界可以由未来通用 `Evidence Qualification Model` 提供，但在其冻结以前，`Commit Model` 必须至少冻结接口和失败关闭行为。

### 裁决

```text
Evidence Qualification Boundary: FAIL
Self-verification Protection: FAIL
Risk Level: HIGH
Required Action: CR-0003-R4 or frozen dependency
```

## 阻断三：解析序列缺少并发唯一性不变量

### 问题

当前登记记录保存：

```text
Registration Sequence
Prior Resolution Record Reference
Resolution Sequence
Resolution Relationship
```

但没有说明：

- 序列号在什么作用域内唯一；
- 谁原子分配序列号；
- 两个并发登记是否允许引用同一个前序记录；
- 分支如何获得稳定身份；
- 投影如何区分账本顺序和语义细化关系；
- `Highest Included Resolution Sequence` 在分支图中如何定义。

一个简单全局递增数字不能同时表达登记账本位置和解析语义谱系。

### 必须拆分

候选模型至少需要：

```text
Resolution Ledger Position
  -> unique within Resolution Ledger Scope
  -> assigned atomically by resolution ledger

Prior Resolution Record References
  -> zero, one or multiple semantic parents

Resolution Relationship
  -> INITIAL
   | REFINES
   | REAFFIRMS
   | CONFLICTS_WITH

Resolution Lineage ID
  -> stable semantic branch identity
```

登记账本位置只表达追加顺序，谱系关系表达认识演化。二者不能共用一个 `Resolution Sequence`。

投影必须引用纳入记录集合或账本水位，不得用单一“最高序号”假装所有分支都已完整读取。

### 裁决

```text
Concurrent Registration Determinism: FAIL
Projection Rebuildability: FAIL_WITH_BLOCKER
Risk Level: HIGH
Required Action: CR-0003-R4
```

## 阻断四：跨规则版本投影缺少兼容性契约

### 问题

候选解析绑定 `Resolution Rule Version`，投影绑定 `Projection Rule Version`，但当前没有规定投影规则可以消费哪些解析规则版本。

例如：

```text
Resolution R1 under Rule V1 = COMMITTED
Resolution R2 under Rule V2 = INDETERMINATE
Projection under Rule V3 = ?
```

如果规则版本改变了证据资格、字段语义或细化关系，投影不能仅按记录顺序合并。

### 必须补充

每项投影规则必须声明：

```text
Allowed Source Resolution Rule Versions
Compatibility Relation
Canonical Interpretation Version
Migration or Re-resolution Requirement
Incompatible Source Behavior
```

最低行为：

```text
Compatible source versions
  -> project normally

Migratable source versions
  -> create new candidate resolution under new rule
  -> preserve old record

Incompatible or unknown compatibility
  -> Projection = INDETERMINATE
  -> fail closed
```

不得通过当前规则追溯改写旧解析记录。

### 裁决

```text
Cross-version Projection Determinism: FAIL
History Preservation: PASS
Risk Level: HIGH
Required Action: CR-0003-R4
```

## 冻结门槛一：上游决策模型尚未冻结

`CR-0003-R3` 依赖 `CR-0002-R1` 提供：

```text
Decision Fact
Decision Validity for Future Use
Requested Transition Type
Composite Decision Requirements
```

但 `CR-0002-R1` 当前只是宪法候选，尚未成为冻结制度。提交模型不能在关键上游语义仍可能改变时独立冻结。

```text
Dependency Freeze Status: FAIL
```

## 冻结门槛二：缺少 IF-0007 冻结证据包

当前只有逻辑模型和提案审查记录，尚未形成满足 `IF-0007` 的完整证据：

```text
Repeated
Stable
Cross Provider
Cross Project
Compatibility Review
Migration or Supersession Plan
Proposer
Reviewer
Freeze Authority
Freeze Decision
Version Boundary
```

这不否定模型方向，但禁止把“逻辑上接近闭合”直接升级为制度冻结。

```text
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
```

## 与冻结制度兼容性

| 冻结制度 | 结果 | 说明 |
|---|---|---|
| `IF-0001 Authority Model` | `FAIL_WITH_BLOCKER` | 多项运行时执行缺少适用授权；证明资格可能自证 |
| `IF-0006 Evidence Model` | `FAIL_WITH_BLOCKER` | 未应用证明资格记录尚未定义 |
| `IF-0007 Institution Model` | `PASS_AS_PROPOSAL` | 保持草案、提供者独立、历史不覆盖；但冻结证据不足 |
| 五层架构边界 | `PASS` | 制度定义不变量，运行时执行角色，投影保持派生 |

## 完整审查矩阵

```text
Proposal Completeness: PASS
Single Purpose: PASS
Object / Process Separation: PASS
Attempt Identity Ordering: PASS
Decision / Commit Separation: PASS
Commit / Target Fact Causality: PASS
Candidate Persistence: PASS
Candidate / Registration Identity: PASS
Field Presence Semantics: PASS
Commit Outcome / Target State Separation: PASS
Read Outcome / State Resolution Separation: PASS
Retry Authority Separation: PASS
Current Projection Type Boundary: PASS
Resolution Execution Authority: FAIL
Non-application Proof Qualification: FAIL
Concurrent Resolution Lineage: FAIL
Cross-version Projection Compatibility: FAIL
Atomic Attribution: PASS_WITH_IMPLEMENTATION_EVIDENCE_REQUIRED
History Preservation: PASS
Provider Independence: PASS
Domain Portability: PASS
Dependency Freeze Status: FAIL
Institution Freeze Evidence: INSUFFICIENT
Freeze Review Readiness: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_BLOCKERS
```

## 独立决定

1. 不冻结 `CR-0003-R3`；
2. 不把外部模型的正面评价作为冻结证据；
3. 保留 `CR-0003-R3` 为历史草案，不原地修改；
4. 下一步建立 `CR-0003-R4`，只处理四项模型阻断；
5. `CR-0003-R4` 完成后由 Codex 做本地独立复审；
6. 即使模型复审通过，在 `CR-0002-R1` 和 `IF-0007` 冻结门槛闭合前，也只能成为 `CONSTITUTION_CANDIDATE`，不能正式冻结；
7. 不修改现有 `IF-0001` 至 `IF-0007`。
