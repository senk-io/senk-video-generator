# CR-0005-R7 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 through CR-0005-R7
Repair Basis: CR-0005-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R7 self-check, scope lock and candidate-level closure declaration were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0005-R7` 对合格空必要目的消费阻断的修复。它不修改被审提案，不审查 `CR-0006-R6`，也不创建制度冻结、注册表、生命周期解析或运行时权威。

## 审查命题

本轮独立回答：

1. 裸无需解析标记是否彻底失去消费资格；
2. 空目的与非空目的分支是否共同固定已登记必要目的资格；
3. 空集是否只能由完整目的资格边界证明；
4. 非空集是否强制消费上下文同一的跨目的聚合；
5. 空／非空不兼容载荷是否冲突优先；
6. 历史和当前消费是否固定适用的生命周期注册表边界上下文；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 through CR-0005-R6
CR-0005-R7 QUALIFIED EMPTY REQUIRED-PURPOSE CONSUMPTION CLOSURE
CR-0005-R6-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检、草案口径锁和候选级闭合声明均不作为通过依据。

## 总体裁决

R7 已关闭裸标记旁路主体：

```text
Bare LIFECYCLE_RESOLUTION_NOT_REQUIRED: INADMISSIBLE
Common Registered Qualification Prefix: PASS
Qualified Empty-purpose Payload: PASS
Qualified Nonempty-purpose Payload: PASS
Purpose-set-derived Consumption Mode: PASS
Empty / Nonempty Conflict Rules: PASS
Cross-purpose Context Equality: PASS
Source Applicability Reference Key and Digest: PASS
Scope Lock / Institution Freeze Separation: PASS
```

但当前重述仍缺少生命周期资格的外层边界上下文。消费前缀固定的是被选择的目的资格竞争边界和聚合解析，却没有固定查询声明的生命周期注册表治理边界或证明该聚合覆盖该边界内全部适用目的候选。因此旧 `QUALIFIED + EMPTY_SET` 在后续非空资格出现后仍可被选择。

因此：

```text
SR-R6-B1 Bare Empty-purpose Bypass: CLOSED
Registered Empty-purpose Qualification: PASS
Current Lifecycle Boundary Eligibility: FAIL_WITH_BOUNDED_BLOCKER
Historical Pinning Direction: PASS
Current Restatement Enforcement: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0005-R8 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：裸标记退场和共同资格前缀

R7 明确把：

```text
LIFECYCLE_RESOLUTION_NOT_REQUIRED
```

降为 `INADMISSIBLE_BARE_MARKER`，禁止读取、写入、自动升级或迁移为空目的资格。

空／非空分支共同固定：

```text
Registered Required Purpose Aggregate Registration Resolution
Registration Result = REGISTERED
Required Purpose Semantic Result = QUALIFIED
Purpose Qualification Competing Boundary Resolution
Required Purpose-boundary Completeness Resolutions
Exact Required Purpose Set Digest
Registered Lifecycle Resolution Rule Contract Payload Digest
```

```text
Bare Marker Bypass: CLOSED
Missing Qualification Prefix: FAIL_CLOSED
Unknown Purpose Boundary: INDETERMINATE
Conflicted Qualification: CONFLICTED
```

## 二、已通过：空集、非空集和上下文内容同一

空分支必须同时满足：

```text
QUALIFIED_EMPTY_REQUIRED_PURPOSES
CANONICAL_EMPTY_SET_DIGEST
Cardinality = 0
Cross-purpose Aggregate = NOT_APPLICABLE
```

非空分支必须同时满足：

```text
QUALIFIED_NONEMPTY_REQUIRED_PURPOSES
Cardinality > 0
Registered Cross-purpose Aggregate Registration Resolution
Same Required Purpose Qualification Resolution
Same Cross-purpose Semantic Conflict Set Key
```

消费模式由已登记目的集合派生，调用者不能提供。空资格也不能自行决定来源适用性。

```text
Zero-query-as-empty: PROHIBITED
Empty Qualification as Applicability Proof: PROHIBITED
Nonempty without Cross-purpose Aggregate: PROHIBITED
Empty / Nonempty Incompatible Payload: CONFLICTED
SR-R6-B1 Subject Repair: CLOSED
```

## 三、有界阻断 SR-R7-B1：消费未固定外层生命周期边界上下文

R7 消费前缀固定一个已登记目的资格聚合及其竞争边界，但没有定义：

```text
Lifecycle Resolution Consumption Boundary Context Key
Registered Lifecycle Resolution Registry Boundary ID and Digest
Required Lifecycle Registry Boundary Completeness Resolution IDs and Digests
Lifecycle View Mode = HISTORICAL_AS_OF_BOUNDARY | CURRENT_RESTATEMENT_AT_BOUNDARY
Purpose Qualification Aggregate Eligibility under Boundary Context
Boundary-context Membership and Coverage Proof
```

R7-17 以规范语句禁止当前重述沿用旧空集，但消费引用键没有外层当前／历史边界输入，无法证明所选资格聚合覆盖当前声明边界内的全部同语义域目的候选。

### 反例

生命周期解析注册表边界 `L1` 中只有空目的候选，聚合得到：

```text
QUALIFIED + EMPTY_SET
```

注册表扩展到完整边界 `L2` 后，新增 `SUPERSEDED` 相关资格候选，当前目的集合为非空或冲突。`L1` 的空资格聚合仍是合法已登记历史对象。

当前来源适用性消费可以继续固定 `L1` 聚合，因为 R7 只验证该聚合自身边界完整，不要求它对当前声明的 `L2` 有资格。

```text
Expected: old empty aggregate is not eligible under current L2 context
Current: selected aggregate boundary is self-contained but outer context is absent
Result: SR-R7-B1 reproduced
```

### 关闭条件

`CR-0005-R8` 必须：

1. 定义生命周期消费边界上下文稳定键，固定已登记生命周期注册表边界、完整性、查询主体和视图模式；
2. 定义目的资格聚合对该上下文的资格证明；
3. 证明资格聚合的竞争边界覆盖外层上下文中全部同语义域适用候选，而不只是其历史子边界；
4. 历史消费显式固定历史边界，当前重述显式固定新的已登记完整边界；
5. 旧空集在新边界出现非空或冲突候选时必须 `NOT_ELIGIBLE` 或 `CONFLICTED`；
6. 边界上下文变化必须形成新的消费引用和来源适用性身份。

```text
SR-R7-B1 Lifecycle Qualification Boundary-context Eligibility: BLOCKED
```

## 四、回归与退出判定

未发现 R7 对以下既有方向造成其他回归：

```text
Lifecycle Registry Reference Identity: PASS
Required Purpose Qualification Identity: PASS
Per-purpose and Cross-purpose Aggregation: PASS
Source Applicability Change Conflict Set: PASS
Source Completeness Aggregate Resolution: PASS
Boundary / Snapshot Reproducibility: PASS
Four-value Coordinate Subject Totality: PASS
Authority Non-propagation: PASS
Scope Lock / Institution Freeze Separation: PASS
```

当前决定：

```text
CR-0005-R7 Independent Model Re-review: COMPLETED
Original Residual Blocker: CLOSED_WITH_ONE_BOUNDARY_CONTEXT_RESIDUAL
Residual Bounded Blockers: 1
CR-0005-R8 Required: YES
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
