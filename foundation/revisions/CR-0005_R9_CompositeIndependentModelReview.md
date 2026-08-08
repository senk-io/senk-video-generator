# CR-0005-R9 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 through CR-0005-R9
Repair Basis: CR-0005-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Repair Basis: CR-0005-R8-CR-0006-R7-CROSS-INTERFACE-REGRESSION-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R9 self-check and candidate-level closure declarations were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0005-R9` 的生命周期记录类型目录、注册表引用世代和查询后边界转换。它不修改被审提案，不审查 `CR-0006-R8`，不执行联合接口回归，也不创建制度冻结、注册表、生命周期解析或运行时权威。

## 审查命题

本轮独立回答：

1. 生命周期视图候选、竞争边界和聚合记录是否获得精确类型合同资格；
2. 目录合同是否在生命周期注册表之外登记并避免自举循环；
3. 目录后继是否相对同一前驱形成唯一竞争槽；
4. 注册表引用是否可按目录后继形成历史可重放世代；
5. 生命周期边界推进是否改为查询后的评价身份而不生成新查询坐标；
6. 当前后继和历史重放是否固定完整竞争域；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 through CR-0005-R8
CR-0005-R9 LIFECYCLE TYPE CATALOG AND POST-QUERY TRANSITION CLOSURE
CR-0005-R8-COMPOSITE-INDEPENDENT-MODEL-REVIEW
CR-0005-R8-CR-0006-R7-CROSS-INTERFACE-REGRESSION-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级关闭声明均不作为通过依据。

## 总体裁决

R9 已完成大部分主体修复：

```text
Lifecycle Record Role-to-type Mapping: PASS
Exact Permitted Type-set Contract: PASS
Catalog Registration outside Lifecycle Registry: PASS
Catalog Candidate / Boundary / Aggregate Chain: PASS
Record-type Eligibility: PASS
View Record Registration Pinning: PASS
Registry Reference Generation: PASS_IN_PRINCIPLE
Temporal Query Coordinate Identity Preservation: PASS
Post-query View Evaluation Subject: PASS
Current Predecessor-anchored Transition: PASS
Historical Explicit-boundary Replay: PASS
L0 through L6 Acyclicity: PASS
```

但目录演进语义键包含候选生效锚点。同一前驱目录只要选择不同锚点，就进入不同语义冲突集合，彼此不出现在同一目录竞争边界。两个平行后继可以分别得到 `REGISTERED`，随后又分别形成不同注册表引用世代。这与 R9 声称的“同一前驱多个不兼容后继必须冲突”不具备可执行的同域基础。

因此：

```text
SR-R8-B1 Record Contract Eligibility Subject: CLOSED
Lifecycle Catalog Successor-slot Identity: FAIL_WITH_BOUNDED_BLOCKER
XREG-B1 Query Subject Identity Repair: CLOSED
Independent Model Re-review: FAIL
CR-0005-R10 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：视图记录类型合同和登记资格

R9 将 R8 的通用家族标签收紧为三种精确角色映射：

```text
VIEW_CONTEXT_CANDIDATE_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_CANDIDATE

VIEW_CONTEXT_COMPETING_BOUNDARY_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_COMPETING_BOUNDARY

VIEW_CONTEXT_AGGREGATE_RESOLUTION_RECORD
  -> LIFECYCLE_CONSUMPTION_VIEW_CONTEXT_AGGREGATE_RESOLUTION
```

目录候选固定精确角色映射、允许类型全集、前驱摘要、追加演进证明和生效载荷。候选、完整竞争边界、四值聚合及外层登记解析均有稳定键。

目录治理记录位于来源契约注册表而非生命周期解析注册表，因此目录不要求先许可自身。每个视图记录登记又固定：

```text
Registered Catalog Aggregate Registration Resolution
Exact Record-type Eligibility
Eligibility Result = PERMITTED
Effective-boundary Anchor
```

```text
Bare Type String Authorization: CLOSED
Generic View-context Family as Record Type: PROHIBITED
Catalog Self-bootstrap through Lifecycle Registry: NONE_FOUND
SR-R8-B1 Type Qualification Subject: PASS
```

## 二、已通过：查询后评价和查询坐标恒等保持

R9 明确覆盖 R8 的新查询主体要求：生命周期边界推进不能创建或修改 `B/T/K`，也不能生成新的 `Registered Temporal Query Coordinate Subject Reference`。

查询后的视图评价以封闭锚点联合类型区分：

```text
HISTORICAL
CURRENT_BOOTSTRAP
CURRENT_SUCCESSOR
```

当前后继固定已登记前驱评价解析，候选目标边界留在候选载荷，同一前驱下的目标边界共同竞争。聚合只有外层 `REGISTERED` 且内层 `SELECTED` 时成为可消费视图评价主体。

```text
Same Query / New Lifecycle Boundary: new post-query evaluation identity
Lifecycle Boundary in Temporal Query Key: PROHIBITED
Historical Result as Current Selection: PROHIBITED
Arbitrary View Generation Number: PROHIBITED
XREG-B1 Subject Repair: CLOSED
```

这一通过项不证明目录后继本身唯一；目录演进残余见下一节。

## 三、有界阻断 SR-R9-B1：生效锚点分割目录后继竞争槽

R9 的目录演进语义键为：

```text
Lifecycle Record-type Catalog Evolution Semantic Conflict Set Key =
  Lifecycle Record-type Catalog Lineage Root Key
+ Registered Predecessor Catalog Aggregate Registration Resolution
+ Registered Catalog Effective-boundary Anchor
+ Catalog Evolution Semantic Rule Version
```

目录竞争边界和目录聚合键都继承该完整语义键。因此竞争只能覆盖“同一前驱且同一锚点”的候选，不能覆盖“同一前驱但不同锚点”的平行后继。

R9-10 虽规定同一前驱多个不兼容后继必须 `CONFLICTED`，但不同锚点已经把它们分到不同语义域，该冲突规则没有共同边界可消费。

引用世代键随后又固定目录聚合和同一生效锚点；一旦两个目录后继分别登记，两个引用世代也会继续隔离而非竞争。

### 反例

已有唯一目录前驱 `C0`。两个候选均从 `C0` 追加视图记录类型：

```text
C1-A: effective at lifecycle anchor L1
C1-B: effective at lifecycle anchor L2
```

两者可以拥有相同类型映射，也可以携带不兼容的后续角色约束。由于 `L1 != L2`：

```text
Catalog Evolution Key(C1-A) != Catalog Evolution Key(C1-B)
```

两个目录竞争边界互不可见，各自都可能得到内外层 `REGISTERED`。随后：

```text
Reference Generation R1-A pins C1-A + L1
Reference Generation R1-B pins C1-B + L2
```

两个引用世代同样不竞争。某个位置或后续边界可以按有利路径选择其中一条目录谱系。

```text
Expected: all immediate successors of C0 compete in one successor slot
Current: candidate effective anchor partitions the successor slot
Result: SR-R9-B1 reproduced
```

### 关闭条件

`CR-0005-R10` 必须：

1. 定义目录后继槽语义键，只固定谱系根、唯一已登记前驱目录解析、受治理注册表作用域和已登记演进规则合同；
2. 从后继槽语义键排除候选生效锚点、目录 ID／版本、类型集合摘要和候选载荷；
3. 把生效锚点及其完整性证明仅放入候选载荷；
4. 完整竞争边界覆盖同一前驱的全部候选锚点、类型映射和合同载荷；
5. 唯一后继聚合同时选择目录内容和生效锚点；同一前驱多个不兼容后继必须 `CONFLICTED`；
6. 后续合法演进必须以前一已选择后继作为新前驱，不能继续从旧前驱选择另一个较晚锚点；
7. 注册表引用世代只能固定已登记唯一后继目录解析；目录解析非唯一时引用世代必须失败关闭；
8. 历史前驱和已选择后继继续按各自有效边界重放，不能覆盖旧记录。

```text
SR-R9-B1 Lifecycle Catalog Successor-slot Identity: BLOCKED
Closure Owner: CR-0005-R10
```

## 四、回归与退出判定

未发现 R9 对以下既有方向造成其他内部回归：

```text
Bare Marker Retirement: PASS
Qualified Empty / Nonempty Consumption: PASS
Required Purpose Boundary-context Eligibility: PASS
Lifecycle Registry Reference Lineage: PASS_WITH_SUCCESSOR_SLOT_BLOCKER
Source Applicability Identity: PASS
Four-value Coordinate Subject Consumption: PASS
Temporal Query Coordinate Identity: PASS
Authority Non-propagation: PASS
Institution Freeze Separation: PASS
```

当前决定：

```text
CR-0005-R9 Independent Model Re-review: COMPLETED
Original Two Blocker Subjects: CLOSED
Residual Bounded Blockers: 1
CR-0005-R10 Required: YES
Cross-interface Regression Review: STILL_REQUIRED
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
