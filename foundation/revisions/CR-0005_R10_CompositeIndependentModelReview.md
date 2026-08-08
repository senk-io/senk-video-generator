# CR-0005-R10 来源注册表复合模型独立复审

## 审查信息

```text
Review ID: CR-0005-R10-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Review Type: Independent Composite Model Re-review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Composite: CR-0005 + CR-0005-R1 through CR-0005-R10
Repair Basis: CR-0005-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Workstream: WS-02
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: R10 self-check and candidate-level closure declaration were ignored
External Approval Required: NO
Proposal Revision Created: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Lifecycle Resolution Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0005-R10` 的目录后继槽、引用世代对齐和生效锚点联合选择。它不修改被审提案，不审查 `CR-0006-R9`，不执行联合接口回归，也不创建制度冻结、注册表、生命周期解析或运行时权威。

## 审查命题

本轮独立回答：

1. 同一前驱的全部目录映射和生效锚点是否进入一个后继槽；
2. 唯一聚合是否不可分割地选择目录内容与锚点；
3. 后续演进是否只能使用已选择后继作为新前驱；
4. 引用世代是否只能消费唯一目录后继解析；
5. 类型资格、视图记录和历史边界是否固定同一目录谱系；
6. 后继槽中的新增治理根是否拥有可验证登记资格；
7. `WS-02` 是否满足独立模型退出门。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0004-CONSTITUTION-CANDIDATE-R1
CR-0005 SOURCE REGISTRY INTERFACE
CR-0005-R1 through CR-0005-R9
CR-0005-R10 CATALOG SUCCESSOR-SLOT CLOSURE
CR-0005-R9-COMPOSITE-INDEPENDENT-MODEL-REVIEW
Local repository state at review time
```

规则数量、文件存在、自检和候选级关闭声明均不作为通过依据。

## 总体裁决

R10 已关闭候选锚点分割后继槽的问题：

```text
Predecessor-only Catalog Successor Slot: PASS
Effective Anchor Excluded from Slot Key: PASS
Mapping + Anchor Combined Candidate: PASS
Complete Cross-anchor Competition: PASS
Unique Joint Successor Selection: PASS
Registered Outer Successor Resolution: PASS
Selected Successor as Next Predecessor: PASS
Reference Generation Alignment: PASS
Record-type Eligibility Pinning: PASS
Post-query View Evaluation Preservation: PASS
Historical Catalog / Reference Replay: PASS
L0 through L6 Acyclicity: PASS
```

但后继槽键新增 `Registered Catalog Lineage Governance Root ID and Digest`，引用后继槽又新增 `Registered Reference Lineage Governance Root ID and Digest`。R10 只声明这些根不可变，没有定义根候选、分配／登记、完整竞争边界或四值聚合解析。不同裸治理根可以再次把同一谱系和前驱分到多个互不可见的后继槽。

因此：

```text
SR-R9-B1 Successor-slot Subject: CLOSED
Catalog / Reference Lineage Governance-root Registration: FAIL_WITH_BOUNDED_BLOCKER
Independent Model Re-review: FAIL
CR-0005-R11 Required: YES
WS-02 Model Exit: BLOCKED
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

## 一、已通过：同前驱统一竞争和联合选择

R10 的目录后继槽固定目录谱系根和唯一前驱，明确排除：

```text
Effective Anchor
Catalog ID or Version
Exact Type-set Digest
Role-to-type Mapping Digest
Candidate Contract Version
Registration Time and Writer
```

目录内容、锚点、合同和演进证明只进入候选载荷。竞争边界固定全部候选锚点、映射、登记记录、空洞和冲突谱系。

唯一聚合同时选择目录内容和生效锚点，多个不兼容合格组合必须 `CONFLICTED`。后续演进必须使用已选择后继作为新前驱，不能继续从旧前驱登记较晚平行后继。

```text
Same Predecessor / Different Anchors: COMMON_COMPETITION_DOMAIN
Caller-selected Effective Anchor: PROHIBITED
Parallel Later Successor from Old Predecessor: CONFLICTED
SR-R9-B1 Candidate-field Partition: CLOSED
```

## 二、已通过：引用世代、类型资格和历史边界

引用后继槽固定唯一目录后继解析，不再把所选锚点作为独立分域字段。候选引用载荷验证目录映射、锚点、注册表作用域和规则载荷内容同一。

类型资格及视图记录进一步固定：

```text
Registered Selected Lifecycle Catalog Successor Resolution
Selected Effective-boundary Anchor
Canonical Lifecycle Record Position Subject
Registered Lifecycle Registry Reference Successor Resolution
Record-type Eligibility Result = PERMITTED
```

旧目录和旧引用继续解释锚点前历史记录；新后继只作用于锚点后记录。查询后生命周期评价和时间查询坐标恒等关系没有回归。

```text
Direct Candidate Catalog Consumption: PROHIBITED
Historical Record Reinterpretation: PROHIBITED
Lifecycle Boundary in Query Coordinate Key: PROHIBITED
Reference / Catalog Successor Alignment: PASS
```

## 三、有界阻断 SR-R10-B1：目录与引用治理根缺少登记拓扑

目录后继槽包含：

```text
Registered Catalog Lineage Governance Root ID and Digest
Catalog Successor-slot Semantic Rule ID
```

目录聚合键再次固定该治理根。引用后继槽则包含：

```text
Registered Reference Lineage Governance Root ID and Digest
Reference Successor-slot Semantic Rule ID
```

R10 规定规则 ID 是治理根载荷的固定成员，但没有定义：

```text
Governance Root Semantic Conflict Set Key
Root Candidate Payload and Stable Candidate Key
Root ID Allocation / Registration Attempt
Registered Root Record
Complete Same-lineage Root Competing Boundary
Root Boundary Completeness
Four-value Root Aggregate Registration Resolution
```

R9 仅定义 `Lifecycle Record-type Catalog Lineage Root Key`，并未产出 R10 所引用的两个 `Registered ... Governance Root` 解析。

### 反例

同一目录谱系根和同一前驱 `C0` 下，两个参与者声称：

```text
Governance Root G1 with Rule ID S1
Governance Root G2 with Rule ID S2
```

由于没有根竞争边界或登记解析，二者都可以被文字上标记为 `Registered`。随后：

```text
Successor Slot Key(C0, G1) != Successor Slot Key(C0, G2)
```

两个目录后继边界互不可见，各自可以选择一个目录—锚点组合。引用侧可用 `RG1/RG2` 重复同样分域。

```text
Expected: one governed root per lineage, with alternatives competing
Current: registered root is referenced but never qualified
Result: SR-R10-B1 reproduced
```

### 关闭条件

`CR-0005-R11` 必须二选一：

1. 删除新增目录／引用治理根字段，直接使用既有已登记来源合同根和不可变谱系根确定固定规则 ID；或
2. 定义治理根语义键，排除候选根 ID、规则 ID、合同版本和载荷摘要；
3. 为目录根和引用根建立候选、ID 分配、登记尝试、内容同一记录、完整竞争边界和四值聚合解析；
4. 同一生命周期注册表谱系的所有根候选必须共同竞争，唯一外层 `REGISTERED` 且内层唯一结果才可消费；
5. 规则 ID 和聚合规则必须来自该唯一已登记根载荷，不能由后继候选提供；
6. 目录和引用后继槽固定精确根聚合解析，而不是裸 `Registered ... ID and Digest`；
7. 根解析变化或冲突必须使后继槽、类型资格和引用世代失败关闭；
8. 根登记位于既有来源契约治理域，不写入生命周期注册表，避免自举循环。

```text
SR-R10-B1 Catalog and Reference Lineage Governance-root Registration: BLOCKED
Closure Owner: CR-0005-R11
```

## 四、回归与退出判定

未发现 R10 对以下既有方向造成其他内部回归：

```text
Lifecycle Record Role-to-type Mapping: PASS
Catalog Registration outside Lifecycle Registry: PASS
Catalog Successor Anchor Competition: PASS
Registry Reference Generation: PASS_WITH_ROOT_BLOCKER
Post-query View Evaluation Subject: PASS
Temporal Query Coordinate Identity: PASS
Purpose Qualification Boundary-context Eligibility: PASS
Authority Non-propagation: PASS
Institution Freeze Separation: PASS
```

当前决定：

```text
CR-0005-R10 Independent Model Re-review: COMPLETED
Original Successor-slot Blocker: CLOSED
Residual Bounded Blockers: 1
CR-0005-R11 Required: YES
Cross-interface Regression Review: STILL_REQUIRED
WS-02 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Freeze ID: NOT_CREATED
Lifecycle Resolution Registry: NOT_CREATED
Runtime Authority: NOT_CREATED
```
