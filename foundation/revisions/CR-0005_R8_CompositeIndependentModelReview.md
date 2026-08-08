# CR-0005-R8 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 through CR-0005-R8
Repair Basis: CR-0005-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R8 self-check and candidate-level closure declaration were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0005-R8` 对生命周期资格边界上下文的修复。它不修改被审提案，不审查 `CR-0006-R7`，也不创建制度冻结、注册表、生命周期解析或运行时权威。

## 审查命题

本轮独立回答：

1. 生命周期消费视图上下文是否拥有稳定语义键、候选、登记、完整竞争边界和聚合解析；
2. 目的资格聚合是否相对已选择生命周期边界证明全域候选集合相等；
3. 空目的和非空目的消费是否共同固定该边界上下文资格；
4. 历史重放与当前重述是否保持边界身份分离；
5. 新增视图上下文记录是否获得既有生命周期注册表合同许可；
6. 阶段和权威是否保持无环及不传播；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 through CR-0005-R7
CR-0005-R8 LIFECYCLE BOUNDARY CONTEXT ELIGIBILITY CLOSURE
CR-0005-R7-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级闭合声明均不作为通过依据。

## 总体裁决

R8 已关闭原边界上下文语义缺口：

```text
Lifecycle View-context Semantic Domain: PASS
View-context Candidate Identity: PASS
Candidate Registration Resolution: PASS
Complete Competing Boundary: PASS
Aggregate Registration Resolution: PASS
Purpose Qualification Boundary-context Eligibility: PASS
Exact Applicable Candidate-set Coverage: PASS
Qualified Empty / Nonempty Consumption: PASS
Historical Boundary Pinning: PASS
Current Boundary Re-evaluation: PASS
Source Applicability Identity Pinning: PASS
L0 through L5 Acyclicity: PASS
```

但 R8 把新增视图上下文候选、竞争边界和聚合记录写入既有生命周期解析注册表时，没有证明已登记不可变注册表合同的精确允许记录类型集合覆盖这些记录角色，也没有定义合同目录的受治理演进。一个只允许 R6 最低六类记录的合法合同仍能被 R8 引用，随后却被写入 `LIFECYCLE_CONSUMPTION_VIEW_CONTEXT`，形成合同外记录。

因此：

```text
SR-R7-B1 Lifecycle Qualification Boundary-context Eligibility: CLOSED
Lifecycle View-context Record Contract Eligibility: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0005-R9 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：视图上下文登记与冲突聚合

R8 的视图上下文语义键固定注册表引用、变化集合、查询主体、视图模式和已登记规则合同，并明确排除候选边界、位置、登记时间和“最新”。候选边界变化保持在同一语义冲突集合内。

候选、边界和聚合分别形成：

```text
Candidate -> Registration Attempt -> Registered Record -> Four-value Resolution
Competing Boundary -> Boundary Registration -> Four-value Resolution
Aggregate -> Aggregate Registration -> Four-value Resolution
```

聚合仅在外层 `REGISTERED` 且内层 `SELECTED` 时可进入消费；未知、遗漏和同域不兼容边界均失败关闭。

```text
Candidate-selected Latest Boundary: PROHIBITED
Self-certified Completeness: PROHIBITED
Same Semantic Key / Incompatible Boundary: CONFLICTED
```

## 二、已通过：目的资格的外层边界覆盖

边界上下文资格同时固定：

```text
Selected Lifecycle Registry Boundary
Exact All Applicable Purpose Qualification Candidate Resolution Set
Selected Aggregate Competing Candidate Set
Candidate-set Equality Proof
Boundary Membership and Completeness Proof
```

因此“旧聚合全部成员仍位于新边界内”不再足够；只有旧聚合集合与所选边界全域集合内容同一时才可 `ELIGIBLE`。

R7 的空／非空共同消费前缀也已收紧为固定已登记视图上下文、所选边界和资格逻辑键。旧 `QUALIFIED + EMPTY_SET` 遇到新边界中的非空或冲突候选时不能继续支持当前来源适用性。

```text
Old Empty Aggregate under Expanded Boundary: NOT_ELIGIBLE or CONFLICTED
Historical Replay under Explicit Old Boundary: PASS
Current Restatement without Unique Complete Boundary: INDETERMINATE or CONFLICTED
SR-R7-B1 Subject Repair: CLOSED
```

## 三、有界阻断 SR-R8-B1：视图上下文记录缺少合同类型资格

R6 的注册表引用候选载荷固定：

```text
Exact Permitted Lifecycle Record Type Set Digest
Registered Source Registry Contract Registration Resolution ID and Digest
```

R6 明示合同允许的最低封闭类型为：

```text
LIFECYCLE_REGISTRY_REFERENCE
LIFECYCLE_CANDIDATE_RESOLUTION
LIFECYCLE_COMPETING_BOUNDARY
LIFECYCLE_AGGREGATE_RESOLUTION
LIFECYCLE_REQUIRED_PURPOSE_QUALIFICATION
LIFECYCLE_CROSS_PURPOSE_RESOLUTION
```

R8 新增并写入同一注册表：

```text
Registered View Context Candidate Record
Registered View Context Competing Boundary Record
Registered View Context Aggregate Record
Lifecycle Record Type = LIFECYCLE_CONSUMPTION_VIEW_CONTEXT
```

R8 没有要求其引用的已登记合同精确允许该类型，也没有明确边界记录和聚合记录是否共享该类型、使用独立类型，或只是某个既有记录的非登记子对象。其登记解析键固定记录边界和完整性，但没有固定一次允许类型目录演进解析。

### 反例

注册表合同甲的精确允许集合恰好等于 R6 明示的六类记录。该合同满足 R6，注册表引用聚合也可以为 `REGISTERED`。

R8 随后以该引用构造视图上下文，并尝试追加：

```text
LIFECYCLE_CONSUMPTION_VIEW_CONTEXT
```

R8 的现有规则没有产生“不允许该类型”的失败结果，候选仍可能沿登记链成为表面 `REGISTERED`。

```text
Expected: contract-excluded record type cannot enter registry
Current: exact permitted type-set membership is not required by R8 registration
Result: SR-R8-B1 reproduced
```

### 关闭条件

`CR-0005-R9` 必须二选一并保持历史可重放：

1. 定义已登记生命周期记录类型目录合同及稳定版本身份；
2. 明确候选、边界、聚合三种记录角色的规范类型映射；
3. 形成目录候选、登记尝试、完整竞争边界和四值聚合解析；
4. 新记录登记键固定已登记目录解析 ID、摘要和精确类型成员证明；
5. 旧合同继续解释旧边界，新合同只对新边界生效，禁止静默改写旧允许集合；
6. 合同未知、目录不完整、类型未允许或同键异映射时必须 `NOT_REGISTERED`、`INDETERMINATE` 或 `CONFLICTED`；
7. 或者明确把这些对象降为既有合法记录载荷中的非登记子对象，不再声称独立注册表记录。

```text
SR-R8-B1 Lifecycle View-context Record Type Contract Eligibility: BLOCKED
Closure Owner: CR-0005-R9
```

## 四、回归与退出判定

未发现 R8 对以下既有方向造成其他内部回归：

```text
Bare Marker Retirement: PASS
Lifecycle Registry Reference Identity: PASS
Required Purpose and Cross-purpose Aggregation: PASS
Source Applicability Change Conflict Set: PASS
Source Completeness Aggregate Resolution: PASS
Four-value Coordinate Subject Consumption: PASS
Authority Non-propagation: PASS
Scope Lock / Institution Freeze Separation: PASS
```

查询坐标主体在生命周期边界扩展时的跨接口恒等问题不并入本独立阻断，由配套交叉接口回归审查单独裁决。

当前决定：

```text
CR-0005-R8 Independent Model Re-review: COMPLETED
Original Residual Blocker: CLOSED
New Residual Bounded Blockers: 1
CR-0005-R9 Required: YES
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
