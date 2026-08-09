# CR-0007-R2 与 CR-0002／CR-0003 消费接口兼容审查

## 审查信息

```text
Review ID: CR-0007-R2-CR-0002-CR-0003-CONSUMER-INTERFACE-COMPATIBILITY-REVIEW
Review Type: Independent Decision and Commit Consumer Interface Compatibility Review
Status: COMPLETED
Result: BLOCKED
Reviewed Qualification Composite: CR-0007 + CR-0007-R1 + CR-0007-R2
Reviewed Decision Consumer: CR-0002-CONSTITUTION-CANDIDATE
Reviewed Commit Consumer: CR-0003-CONSTITUTION-CANDIDATE-R2
Commit Compatibility Basis: CR-0003-R7 QUALIFICATION COMPATIBILITY CLOSURE
Upstream Interface Basis: CR-0007-R2-CR-0005-R11-CR-0006-R10-FINAL-UPSTREAM-CROSS-INTERFACE-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: CR-0007 interface declarations and all proposal self-checks were ignored
External Approval Required: NO
Proposal Revision Created: NO
Independent Qualification Model Review Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Qualification Registry Created: NO
Runtime Authority Created: NO
Decision Basis Qualification Interface Result: PASS
Proof Qualification Interface Result: BLOCKED
Blocking Finding Count: 3
Next Authorized Stage: CR-0007-R3 bounded consumer-interface repair
```

> 本文件只审查资格提供方与决策、提交候选模型的消费接口兼容性。它不修改任何提案，不执行资格、适用性、提交或投影，不创建制度冻结，也不裁决 `CR-0007` 内部模型已经完整。

## 一、审查命题

本轮独立回答：

1. `CR-0007` 能否提供 `CR-0002 DM-C-06` 的三值依据资格接口；
2. 四值资格是否在单条历史记录和聚合投影之间保持层级分离；
3. `CR-0003` 的精确提交契约／兼容域作用域是否被资格治理完整建模；
4. 兼容域成员是否固定精确提交契约版本及其资格规则绑定；
5. 资格前向解释是否固定候选证明、提交键和契约作用域；
6. 重新资格计算是否保持旧记录、适用性和闭包分离；
7. 是否可以进入独立资格模型审查。

## 二、总体裁决

`CR-0007` 对 `CR-0002` 的依据资格三值接口拥有安全、单向、失败关闭适配；`CONFLICTED` 被降为 `INDETERMINATE` 并保留冲突引用，没有把冲突伪装成 `NOT_QUALIFIED`。

证明资格接口尚不兼容：

```text
Decision Basis Qualification Interface: PASS
Qualification / Applicability Separation: PASS
Requalification Downstream Rebuild Boundary: PASS
Atomic Historical Qualification Algebra: BLOCKED
Commit-contract Scope Mode Compatibility: BLOCKED
Proof / Commit Identity Preservation in Forward Interpretation: BLOCKED
Residual Consumer Interface Blockers: 3
Overall Result: BLOCKED
```

## 三、`CR-0002` 依据资格接口通过

### 字段覆盖

`CR-0002 DM-C-06` 要求：

```text
Resolution ID
Basis ID and Version
Decision Type
Decision Object Scope
Qualification Outcome
Effective At
As Of
Resolved At
Qualification Rule Version
Institution Version
Source Registry Snapshot References
Source Set Digest
Coverage or Completeness Proof Reference
Evidence References
Correction View Reference
Registration Authority Grant Reference
```

`CR-0007 QG-C-58` 与 R1/R2 收紧后的输入身份能够提供上述字段，并额外固定四值坐标主体、完整性聚合元组和精确更正集合。

### 三值适配安全

```text
QUALIFIED -> QUALIFIED
DISQUALIFIED -> NOT_QUALIFIED
INDETERMINATE -> INDETERMINATE
CONFLICTED -> INDETERMINATE + Qualification Conflict References
```

只有 `QUALIFIED` 可以支持正向准入。冲突、未知、来源不完整或坐标非登记单例均不能产生 `QUALIFIED`。

```text
CR-0002 Basis Field Coverage: PASS
Three-value Mapping Totality: PASS
Conflict Failure Closure: PASS
Decision Admissibility Authority Leakage: NONE_FOUND
```

## 四、阻断 `XQG-CONS-B1`：单条历史资格与四值冲突投影混层

### 消费方层级

`CR-0003 CM-C-15` 明确规定单条历史证明资格：

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
```

`CR-0003 CM-C-21` 和 `CM-C-41` 才在相同稳定键下聚合适用、可比较的多条历史资格：

```text
QUALIFIED only -> Qualification Projection = QUALIFIED
DISQUALIFIED only -> Qualification Projection = DISQUALIFIED
QUALIFIED + DISQUALIFIED -> Qualification Projection = CONFLICTED
```

因此：

```text
Atomic Registered Proof Qualification != Qualification Projection
Atomic Algebra = three-value
Projection Algebra = four-value
```

### 提供方当前混层

`CR-0007 QG-C-23` 把以下四值定义为一个规范资格结果：

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED
```

`QG-C-22` 至 `QG-C-30` 又让一次计算候选直接登记为 `Registered Qualification Resolution`。当前没有区分：

```text
Atomic Candidate / Registered Qualification Resolution
Registered Qualification Conflict Aggregate
Qualification Current Projection
```

这允许单个资格计算者写出 `CONFLICTED`，或者让登记者把多个相反历史结果压缩成单条资格记录，违反 `CR-0003` 的历史不可变与投影分层。

### `CR-0002` 证明接口不能消除该冲突

`CR-0002 DM-C-25` 把证明资格消费值写为四值，但同时要求候选和登记载荷内容同一。兼容提供方必须显式说明四值 `CONFLICTED` 来自独立已登记聚合，而不是来自单次资格计算。

当前 `CR-0007` 没有提供这种带来源种类判别的适配。

### 阻断判定

```text
Finding ID: XQG-CONS-B1
Severity: BLOCKING
Type: ATOMIC_QUALIFICATION_AND_CONFLICT_PROJECTION_LAYER_COLLAPSE
Result: OPEN
```

### 最低修复要求

后续修订必须分离：

```text
Atomic Candidate / Registered Qualification Outcome:
  QUALIFIED | DISQUALIFIED | INDETERMINATE

Registered Qualification Aggregate / Projection Outcome:
  QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED
```

并为 `CR-0002` 四值证明消费接口提供判别字段：

```text
Qualification Result Source Kind =
  ATOMIC_REGISTERED_QUALIFICATION
  or REGISTERED_QUALIFICATION_AGGREGATE
```

`CONFLICTED` 只能来自第二类，并必须保存全部相反原子记录、适用性、兼容性、闭包和聚合规则引用。

## 五、阻断 `XQG-CONS-B2`：兼容域按资格规则版本而非提交契约版本建模

### 消费方作用域模式

`CR-0003` 的合法模式只有：

```text
EXACT_CONTRACT_VERSION
COMPATIBILITY_DOMAIN_SNAPSHOT
```

精确模式固定一个 `Commit Contract Version`；兼容域快照至少固定：

```text
Exact Member Commit Contract Versions
Membership Digest
Membership Rule Version
Governing Institution and Freeze Reference
Validity As Of
Knowledge Boundary Vector
```

### 提供方当前作用域模式

`CR-0007 QG-C-43` 定义：

```text
EXACT_QUALIFICATION_RULE_VERSION
QUALIFICATION_COMPATIBILITY_DOMAIN_SNAPSHOT
```

其兼容域快照只固定：

```text
Exact Member Qualification Rule IDs and Versions
Exact Member Rule Digests
```

资格规则版本和提交契约版本是不同身份。多个提交契约可以引用同一资格规则，同一提交契约也可能在治理演进中绑定不同资格规则版本。只固定规则成员集合不能证明候选证明位于 `CR-0003` 的精确契约作用域。

### 反例

```text
Commit Contract C1 -> Qualification Rule Q1
Commit Contract C2 -> Qualification Rule Q1

CR-0007 rule-domain snapshot = {Q1}
  -/-> distinguish C1 from C2
  -/-> prove C1 and C2 are qualification-scope compatible
```

### 阻断判定

```text
Finding ID: XQG-CONS-B2
Severity: BLOCKING
Type: COMMIT_CONTRACT_SCOPE_AND_RULE_DOMAIN_IDENTITY_COLLAPSE
Result: OPEN
```

### 最低修复要求

通用资格规则兼容域可以保留，但 `PROOF_QUALIFICATION` 消费配置必须另行固定：

```text
Qualification Scope Mode = EXACT_CONTRACT_VERSION
  -> Exact Commit Contract ID and Version
  -> Exact Qualification Rule ID and Version bound by that contract

Qualification Scope Mode = COMPATIBILITY_DOMAIN_SNAPSHOT
  -> Exact Member Commit Contract IDs and Versions
  -> Exact Per-member Qualification Rule Binding Set
  -> Exact Directional Qualification Compatibility Records
  -> Contract Membership Digest
  -> Rule Binding Digest
```

两个作用域模式名称和互斥语义必须与 `CR-0003` 内容同一。

## 六、阻断 `XQG-CONS-B3`：前向解释未固定候选证明与提交键

### 消费方不可变作用域

`CR-0003-R7 QC-05` 要求资格前向解释保持：

```text
Same Candidate Proof ID
Same Commit Key
Same Qualification Scope Mode
Same exact contract version or same compatibility domain snapshot
Same Validity As Of
Same Knowledge Boundary Vector
```

### 提供方当前字段不足

`CR-0007 QG-C-46` 只固定：

```text
Same Qualification Purpose and Semantic Domain
Same Qualification Subject ID and Version
Same Qualification Basis ID and Version
Same Qualification Scope Mode
Same Exact Rule Version or Same Compatibility Domain Snapshot
Same Validity As Of
Same Knowledge Boundary Vector
Same Temporal View Mode
```

一般主体和依据引用不能替代 `Candidate Proof ID` 与 `Commit Key`。当前契约也只固定资格规则版本，没有固定精确提交契约或契约兼容域。

因此，两个证明依据内容相同但属于不同提交尝试或提交键时，可能被错误解释为同一资格作用域。

### 阻断判定

```text
Finding ID: XQG-CONS-B3
Severity: BLOCKING
Type: PROOF_AND_COMMIT_SCOPE_IDENTITY_OMISSION
Result: OPEN
```

### 最低修复要求

`PROOF_QUALIFICATION` 的前向解释契约、候选、登记记录和稳定键必须显式固定：

```text
Candidate Proof ID and Payload Digest
Commit Key
Commit Attempt ID
Decision Key when required by consumer contract
Qualification Scope Mode
Exact Commit Contract ID and Version or exact Compatibility Domain Snapshot
Validity As Of
Knowledge Boundary Vector
Temporal View Mode
Source and Target Qualification Rule Versions
```

任一项变化必须要求新投影键或 `REQUIRES_RERESOLUTION + REQUALIFICATION`，不得仅靠一般主体同一继续解释。

## 七、已通过的其他消费边界

### 资格与适用性保持分离

R2 已删除资格输入中的来源适用性。`CR-0003 CM-C-16` 至 `CM-C-18` 的后续适用性链可以独立消费历史资格，不会反向改写资格记录。

### 重新资格计算保持追加

`CR-0007 QG-C-49` 至 `QG-C-51` 要求提高确定性、跨终局或改变作用域时执行新的资格计算、候选和独立登记，并在之后重建适用性、闭包和投影。

```text
Requalification Append-only History: PASS
Applicability Rebuild after Requalification: PASS
Closure Rebuild after Requalification: PASS
ABORTED Direct Inference: PROHIBITED
```

### 前向解释非放大映射本身兼容

`QG-C-45` 的映射值域与 `CR-0003 CM-C-45` 内容同一。阻断在作用域身份，不在映射真值表。

## 八、阻断关系与修复顺序

三个阻断应由一个 `CR-0007-R3` 有界修订共同修复：

```text
First: split atomic three-value history from four-value aggregate
Then: establish commit-contract qualification scope profiles
Then: bind proof / commit identities into forward interpretation
```

如果先保留单条四值记录，后续作用域固定仍会把冲突历史压缩；如果只修复结果层而不固定契约和提交键，跨契约解释仍不安全。

## 九、审查结论

### 发现清单

| 发现 | 主题 | 状态 |
|---|---|---|
| `XQG-CONS-B1` | 单条资格与四值冲突投影混层 | `OPEN` |
| `XQG-CONS-B2` | 提交契约作用域与资格规则域混同 | `OPEN` |
| `XQG-CONS-B3` | 前向解释缺少证明和提交键身份 | `OPEN` |

### 当前决定

```text
Review Status: COMPLETED
Review Result: BLOCKED
CR-0002 Basis Qualification Interface: PASS
CR-0002 / CR-0003 Proof Qualification Interface: FAIL
Blocking Findings: 3
CR-0007-R3 Required: YES
Independent Qualification Model Review: NOT_READY
WS-04 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须建立 `CR-0007-R3`，分离单条三值资格与四值聚合投影，建立提交契约作用域配置，并把候选证明和提交键加入前向解释稳定身份。修订后必须重新执行本消费接口兼容审查。
