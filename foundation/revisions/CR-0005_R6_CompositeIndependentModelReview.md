# CR-0005-R6 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 + CR-0005-R2 + CR-0005-R3 + CR-0005-R4 + CR-0005-R5 + CR-0005-R6
Repair Basis: CR-0005-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R6 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0005-R6` 对注册表引用根身份和跨目的生命周期聚合的修复。它不修改被审提案，不审查 `CR-0006-R5`，也不创建注册表、生命周期解析、制度冻结或运行时权威。

## 审查命题

本轮独立回答：

1. 生命周期解析注册表引用是否与分配解析、合同、作用域和记录类型内容同一；
2. 引导登记是否无环且不能扩大授权；
3. 必要目的集合是否具有决定独立的资格竞争域；
4. 所有必要目的是否进入父级组合竞争和冲突聚合；
5. “无需生命周期解析”是否拥有与非空必要目的同等级的完整证明；
6. 来源适用性是否只能消费完整、已登记且上下文同一的组合解析；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 through CR-0005-R5
CR-0005-R6 REGISTRY REFERENCE AND CROSS-PURPOSE CONSISTENCY CLOSURE
CR-0005-R5-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、作者身份和候选级闭合声明均不作为通过依据。

## 总体裁决

R6 已实质关闭上一轮两个阻断的主体：

```text
Registry Reference Semantic Conflict Key: PASS
Allocation Candidate ID Equality Binding: PASS
Bootstrap Registration Acyclicity: PASS
Reference Candidate Registration: PASS
Reference Competing Boundary: PASS
Reference Aggregate Registration Resolution: PASS
Downstream Reference Pinning: PASS
Parent Cross-purpose Semantic Key: PASS
Required Purpose Qualification Conflict Domain: PASS
Per-purpose Coverage Vector: PASS
Cross-purpose Competing Boundary: PASS
Cross-purpose Aggregate Registration: PASS
Cross-purpose Conflict-first Semantics: PASS
```

但来源适用性消费仍允许裸 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`。该标记没有固定已登记必要目的资格解析、完整空目的集合及其边界完整性，所以只能形成规范禁止，不能形成可重放证明。非空必要目的集合可以被该标记绕过。

因此：

```text
SR-R5-B1 Registry Reference Identity: CLOSED
SR-R5-B2 Cross-purpose Aggregation: CLOSED_WITH_ONE_EMPTY_QUALIFICATION_RESIDUAL
Registered Non-empty Purpose Consumption: PASS
Qualified Empty-purpose Consumption: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0005-R7 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：注册表引用根身份

R6 把注册表引用拆为语义冲突键、候选载荷、候选键、引导登记、候选登记解析、完整竞争边界、引用聚合和外层登记解析。

```text
Lifecycle Resolution Registry Reference Semantic Conflict Set Key
Lifecycle Resolution Registry Reference Candidate Key
Lifecycle Registry Reference Candidate Registration Resolution Key
Lifecycle Registry Reference Competing Boundary Key
Lifecycle Resolution Registry Reference Aggregate Resolution Key
Lifecycle Registry Reference Aggregate Registration Resolution Key
```

分配解析中的候选注册表 ID、版本和域必须与生命周期解析注册表内容同一。合同、作用域、记录类型和规则载荷留在候选载荷而不进入语义冲突键，因此同根异载荷会共同竞争。

引导登记只允许写入注册表引用记录，其他生命周期记录必须等待最终外层 `REGISTERED` 引用解析，未发现根引用身份循环。

```text
Unbound Allocation Resolution: PROHIBITED
Scope / Contract Key Escape: CLOSED
Bootstrap Privilege Expansion: PROHIBITED
Same-root Incompatible Reference: CONFLICTED
SR-R5-B1 Result: CLOSED
```

## 二、已通过：必要目的资格与跨目的聚合

父级语义键明确排除 `Lifecycle Resolution Purpose`，逐目的解析只作为子域输入。

必要目的集合通过候选、登记解析、完整竞争边界、资格聚合和外层登记解析确定；同键异目的集合必须冲突。

组合候选固定：

```text
Registered Required Purpose Aggregate Registration Resolution
Exact Required Purpose Set Digest
Exact Per-purpose Aggregate Resolution Tuple Set Digest
Cross-purpose Consistency Proof Digest
Combined State and Successor
```

每个必要目的必须恰好一个已登记逐目的聚合。全部组合候选进入跨目的竞争边界，最终聚合保持：

```text
CONSISTENT_RESOLVED
NOT_RESOLVED
INDETERMINATE
CONFLICTED
```

```text
Purpose-key Isolation: CLOSED
Unfavorable Required-purpose Omission: PROHIBITED_FOR_NONEMPTY_VECTOR
Cross-purpose Incompatible State / Successor: CONFLICTED
Single-purpose Direct Applicability Consumption: PROHIBITED
```

## 三、有界阻断 SR-R6-B1：无需解析标记缺少合格空目的证明

R6-22 仍定义：

```text
Lifecycle Resolution Consumption Reference =
  Registered Cross-purpose Aggregate Registration Resolution ID and Digest
+ Registered Cross-purpose Aggregate Payload Digest
or
  LIFECYCLE_RESOLUTION_NOT_REQUIRED
```

随后只以规范语句规定“存在任何必要生命周期解析目的时，不允许该标记”。但标记分支没有固定：

```text
Registered Required Purpose Aggregate Registration Resolution ID and Digest
Required Purpose Semantic Result = QUALIFIED
Exact Required Purpose Set Digest = EMPTY_SET
Required Purpose Boundary Completeness Resolution IDs and Digests
Empty-purpose Qualification Rule Version
```

因此消费键自身无法证明不存在必要目的，也无法把裸标记与已登记非空目的资格解析置于同一冲突域。

### 反例

完整变化集合含 `ACTIVE + SUPERSEDED`。已登记必要目的资格解析得到：

```text
EFFECT_INTERVAL_ORDERING
UNIQUE_SUCCESSOR
SUPERSESSION_TARGET
```

跨目的解析当前为 `CONFLICTED`。另一执行者在来源适用性键中使用 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`。由于该标记不引用目的资格解析或空集证明，当前键结构没有可重放输入拒绝此分支。

```text
Expected: nonempty qualified purpose set conflicts with NOT_REQUIRED claim
Current: bare marker without registered empty qualification
Result: SR-R6-B1 reproduced
```

### 关闭条件

`CR-0005-R7` 必须：

1. 删除裸 `LIFECYCLE_RESOLUTION_NOT_REQUIRED`，或把它替换为内容同一的已登记空目的资格引用；
2. 所有消费分支都固定必要目的资格外层登记解析 ID、摘要、语义结果和精确目的集合摘要；
3. 只有完整边界下 `QUALIFIED + EMPTY_SET` 可以支持无需组合解析；
4. 非空目的集合必须固定已登记跨目的聚合；
5. 空集、非空集、未知或冲突资格之间的不兼容载荷必须 `CONFLICTED`；
6. 目的资格变化必须形成新的来源适用性身份。

```text
SR-R6-B1 Qualified Empty Required-purpose Consumption: BLOCKED
```

## 四、回归与退出判定

未发现 R6 对以下既有方向造成其他回归：

```text
Source Registry Root Bootstrap: PASS
Lifecycle Same-purpose Aggregation: PASS
Source Version Conflict Aggregation: PASS
Source Completeness Aggregate Resolution: PASS
Applicability Change Conflict Set: PASS
Boundary / Snapshot Reproducibility: PASS
Four-value Coordinate Subject Totality: PASS
Historical / Current Separation: PASS
Authority Non-propagation: PASS
Cross-interface Acyclicity: PASS
```

当前决定：

```text
CR-0005-R6 Independent Model Re-review: COMPLETED
Original Two Blockers: ONE_CLOSED + ONE_CLOSED_WITH_RESIDUAL
Residual Bounded Blockers: 1
CR-0005-R7 Required: YES
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
