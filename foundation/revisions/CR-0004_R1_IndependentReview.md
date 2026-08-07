# CR-0004-R1 独立模型与启动闭环复审

## 审查信息

```text
Review ID: CR-0004-R1-LOCAL-REVIEW
Review Type: Independent Bounded Repair and Bootstrap Closure Review
Status: COMPLETED
Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0004-R1
Reviewed Workstream: WS-01
Repair Basis: CR-0004-LOCAL-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Separate review task contract and immutable review record; not an external freeze review
External Approval Required: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只复审 `CR-0004-R1` 是否完整关闭 `CR-0004-LOCAL-REVIEW` 的四项阻断。它不修改 `CR-0004` 或 R1 历史正文，不创建制度冻结、冻结标识、注册表、账本、提交解析或运行时权威。

## 审查命题

本轮独立回答：

1. 冻结标识分配是否拥有独立、可登记且可确定解析的权威拓扑；
2. 受保护登记是否固定候选载荷并消费互不传播的精确授权；
3. 生命周期与更正是否形成完整的决定、候选、登记、内容同一和适用性链；
4. 注册表外提交、外部锚和内部启动提交是否拥有稳定身份与四值终局；
5. 启动清单、启动窗口和启动关闭事实是否只有一个规范来源；
6. 三种登记／冻结依据模式是否拥有边界完整且可复算的冻结引用解析；
7. R1 是否达到合并为后续制度候选的退出门槛。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-CONSTITUTION-CANDIDATE
CR-0003-CONSTITUTION-CANDIDATE-R2
CR-0004
CR-0004-LOCAL-REVIEW
CR-0004-R1
Local repository state at review time
```

R1 自述、历史讨论和作者身份只作为定位信息，不作为通过依据。

## 总体结论

R1 已实质修复原四项阻断的大部分结构：

```text
Original B1 Authority Topology: PASS_WITH_ONE_RESIDUAL_BLOCKER
Original B2 Lifecycle and Correction Causality: PASS_WITH_ONE_RESIDUAL_BLOCKER
Original B3 Bootstrap Protocol: PASS_WITH_ONE_RESIDUAL_BLOCKER
Original B4 Mode-specific Freeze Reference Resolution: PASS
```

已通过的核心边界包括：

```text
Freeze ID Allocation Authority Separation: PASS
Protected Commit Authority Bundle: PASS
Candidate / Registered Payload Identity: PASS
Lifecycle and Correction Registration Chain: PASS
Pre-registry Commit Four-value Resolution: PASS
External Anchor Four-value Resolution: PASS
Bootstrap Internal Commit Four-value Resolution: PASS
Source Boundary Completeness: PASS
Three-mode Freeze Reference Resolution: PASS
Historical Non-retroactivity: PASS
```

但仍有三个有界缺口：

```text
R1-B1 Freeze ID Allocation Resolution Record and Stable Identity: BLOCKED
R1-B2 Lifecycle Competing-decision Conflict Domain: BLOCKED
R1-B3 Bootstrap Control Identity and Sole Closure Source: BLOCKED
```

因此：

```text
Proposal Structure: PASS
Bounded Repair Progress: PASS
Original Four-blocker Closure: PASS_WITH_RESIDUAL_BLOCKERS
Consolidation Eligibility: FAIL
WS-01 Exit Eligibility: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
```

三个缺口可以在一个有界 `CR-0004-R2` 中修复，不需要扩大 `WS-01`，也不需要重写 R1 已通过的三模式解析模型。

## 一、已通过项

### 冻结标识分配与受保护提交

R1 将冻结标识分配从冻结决定、提交协调、注册表登记和启动识别权威中分离，并建立：

```text
Freeze ID Allocation Attempt
Freeze ID Allocation Record
Freeze ID Allocation Ledger
NATIVE_NEW
BOOTSTRAP_RESERVED_EXISTING
permanent non-reuse rule
```

正常提交和启动内部提交都要求固定候选载荷、候选摘要、权威包和声明写集。协调者只能组织边界，不能取得各登记权威。

```text
Authority Non-propagation: PASS
Allocation Origin Separation: PASS
Candidate Payload Fixing: PASS
Protected Write Authorization: PASS
```

### 生命周期与更正登记链

R1 为生命周期关系和表示更正分别建立决定事实、候选记录、登记尝试、登记记录、内容同一和独立登记权威。更正不改变原记录、原摘要、原有效时间或原认识时间。

```text
Decision / Registration Separation: PASS
Candidate / Registered Identity: PASS
Append-only Correction: PASS
Bitemporal Preservation: PASS
```

### 注册表外提交与启动提交

R1 为注册表外提交、外部锚和内部启动提交定义稳定键、候选与登记解析、四值结果和失败关闭规则。外部锚核心摘要不包含其自身登记结果，因而没有重新引入自证循环。

```text
Pre-registry Commit Resolution: PASS
External Anchor Resolution: PASS
Bootstrap Internal Resolution: PASS
Self-reference Termination: PASS
Retry-based Window Reopening Prevention: PASS
```

### 三模式冻结引用解析

R1 明确每个来源的独立边界完整性记录，建立稳定的冻结引用解析键，并按三种合法组合分别固定必需来源集合：

```text
NATIVE + NATIVE_FREEZE
BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

解析只能从已登记权威来源和完整边界产生，缺失、冲突与否定证明被区分，历史旧链和向未来生效的新识别链不会拼接。

```text
Original B4 Closure: PASS
Mode-specific Source Vector: PASS
Registered Resolution Requirement: PASS
Legacy / Prospective Chain Separation: PASS
```

## 二、阻断 R1-B1：冻结标识分配解析没有稳定记录身份

### 本地事实

`IR-R1-06` 定义：

```text
ALLOCATED
NOT_ALLOCATED
INDETERMINATE
CONFLICTED
```

`IR-R1-07` 又定义 `Freeze ID Allocation Key`，但该键只标识候选冻结标识在命名空间内的分配对象。R1 没有定义：

```text
Freeze ID Allocation Resolution Key
Candidate Freeze ID Allocation Resolution Record
Freeze ID Allocation Resolution Registration Attempt
Registered Freeze ID Allocation Resolution Record
Freeze ID Allocation Resolution Execution Authority Type
Freeze ID Allocation Resolution Registration Authority Type
Allocation Resolution Rule Version
```

`Freeze ID Allocation Record` 只能承载已分配的正向事实，不能为 `NOT_ALLOCATED`、`INDETERMINATE` 或 `CONFLICTED` 提供同等稳定、可登记和可复算的解析身份。

### 风险

当前冻结决定要求消费状态为 `ALLOCATED` 的精确分配记录，但 `ALLOCATED` 本身仍可能只是对账本的自由计算结果。不同读取边界、命名空间完整性证明或规则版本可能对同一分配键产生不同结论，而没有权威解析记录保存差异。

```text
Registered allocation fact != registered allocation resolution
Missing record != qualified NOT_ALLOCATED proof
Free computation != authoritative ALLOCATED state
```

### 有界修复要求

`CR-0004-R2` 必须补充：

1. 稳定 `Freeze ID Allocation Resolution Key`，至少绑定分配尝试、分配键、分配账本边界、命名空间完整性记录和解析规则版本；
2. 候选解析、解析登记尝试、已登记解析和各自载荷摘要；
3. 独立解析执行权威与解析登记权威；
4. 四值结果对正向记录、合格否定证明、边界不完整和冲突记录的完整真值表；
5. 只有已登记且内容同一的 `ALLOCATED` 解析能够支持冻结决定，解析必须精确引用对应分配记录。

```text
Finding R1-B1: BLOCKING
Repair Scope: allocation resolution identity and registration only
```

## 三、阻断 R1-B2：生命周期竞争决定缺少冲突域

### 本地事实

R1 的 `Lifecycle Relation Key` 包含 `Lifecycle Decision Fact ID`。因此，两个针对同一来源版本、同一目标、同一作用域和同一有效时间的相反生命周期决定，会自然落入不同键。

R1 后续适用性规则要求冲突生命周期记录产生 `CONFLICTED`，但没有定义：

```text
Lifecycle Applicability Conflict Set Key
Lifecycle Semantic Compatibility Rule
Competing Decision Membership Rule
Registered Lifecycle Effect Resolution Record
Lifecycle Effect Resolution Rule Version
```

同键不同载荷冲突规则不能捕获不同决定事实标识下的语义竞争。

### 风险

如果一个决定声明版本在某作用域被撤销，另一个决定声明同一时空范围仍可适用，解析器无法确定二者是否属于同一竞争集合，也无法证明当前效果是有效、无效、未知还是冲突。

最后写入获胜、按记录顺序隐式优先或丢弃其中一条，都会破坏追加历史和冲突保留。

### 有界修复要求

`CR-0004-R2` 必须补充：

1. 不含 `Lifecycle Decision Fact ID` 的生命周期竞争集合稳定键，至少绑定来源版本、目标或不适用值、作用域、有效时间坐标和关系语义域；
2. 已登记生命周期关系加入竞争集合的确定规则；
3. 关系兼容、明确替代、互斥和不可比较规则；
4. 稳定生命周期效果解析键，绑定竞争集合、生命周期注册表边界、边界完整性记录、视图坐标和规则版本；
5. 已登记的 `EFFECTIVE | NOT_EFFECTIVE | INDETERMINATE | CONFLICTED` 解析或等价完整值域；
6. 禁止最后写入获胜，冲突记录必须保留并显式解析。

```text
Finding R1-B2: BLOCKING
Repair Scope: lifecycle conflict-set identity and effect resolution only
```

## 四、阻断 R1-B3：启动控制身份与关闭真源没有唯一化

### 本地事实

R1 要求 `Bootstrap Manifest` 绑定首批集合、摘要、外部锚和内部写集，但没有定义：

```text
Bootstrap Manifest Key
Candidate Bootstrap Manifest Record
Bootstrap Manifest Registration Authority Type
Registered Bootstrap Manifest Record
Single-manifest Conflict Rule
```

`IR-R1-38` 的 `Bootstrap Window Definition Record` 规定同键不同窗口定义为 `CONFLICTED`，却没有给出该窗口键的字段构成和登记身份。

更关键的是，`IR-R1-38` 只明确取代基础稿 `IR-C-50` 中提前写入的 `Bootstrap Closed Record`；基础稿 `IR-C-54` 仍把 `Bootstrap Closed Record` 当作一次性窗口关闭事实。与此同时，`IR-R1-41` 又规定只有已登记 `Bootstrap Commit Resolution = COMMITTED` 才能产生 `ACTIVE_CLOSED` 并开放 `NATIVE` 路径。

```text
Base IR-C-54 -> Bootstrap Closed Record closes window
R1 IR-R1-41 -> registered COMMITTED resolution closes window
```

R1 没有明确覆盖 `IR-C-54`，于是合并时存在两个竞争的规范关闭来源。

### 风险

多个清单、多个窗口定义或旧 `Bootstrap Closed Record` 与新提交解析不一致时，系统可能无法确定唯一首批集合、唯一允许尝试或唯一正常模式入口。一个提前存在的关闭记录还可能绕过 R1 已建立的外部锚和内部四值解析。

### 有界修复要求

`CR-0004-R2` 必须补充：

1. 稳定 `Bootstrap Manifest Key`、候选清单、清单登记尝试、已登记清单、内容摘要及独立登记权威；
2. 单启动纪元内唯一清单规则，以及多清单或同键不同内容的 `CONFLICTED` 结果；
3. 稳定 `Bootstrap Window Definition Key`、候选／登记记录和内容同一规则；
4. 明确同时覆盖基础稿 `IR-C-50` 与 `IR-C-54` 的旧关闭语义；
5. 将 `Bootstrap Closed Record` 降为非规范历史载荷或明确退场，不得再独立开放 `NATIVE`；
6. 唯一规范关闭来源必须是已登记 `Bootstrap Commit Resolution` 对 `ACTIVE_CLOSED` 或失败关闭状态的投影；
7. 清单、窗口和终局解析之间必须相互绑定，任一不一致都产生 `CONFLICTED`，不得择一接受。

```text
Finding R1-B3: BLOCKING
Repair Scope: manifest/window identity and sole bootstrap closure source only
```

## 五、非阻断观察

以下事项仍是 `CR-0002` 冻结前的外部治理依赖，但不构成本轮对 R1 的新增模型阻断：

```text
IF-0007 authoritative institution freeze
WS-02 through WS-08 completion
Provider-source reality-bound evidence
Independent external approval where required
Runtime carrier implementation and migration
```

R1 及本审查均为 `Authority: NONE` 的提案层记录，不能据此创建注册表、账本、冻结标识、冻结事实或运行时权威。

## 六、阻断矩阵

| 阻断 | 原阻断归属 | R1 已完成 | 残余缺口 | R2 最小退出条件 |
|---|---|---|---|---|
| R1-B1 | B1 | 分配权威、尝试、正向记录、唯一性和不可复用 | 四值分配解析没有稳定登记身份 | 建立解析键、权威、候选／登记记录和真值表 |
| R1-B2 | B2 | 生命周期决定、候选、登记和更正链 | 不同决定标识下的语义竞争没有冲突域 | 建立竞争集合与已登记效果解析 |
| R1-B3 | B3 | 注册表外提交、外部锚、内部提交四值终局 | 清单／窗口身份不完整且存在两个关闭真源 | 唯一化控制对象并只允许已登记提交解析关闭窗口 |

```text
Bounded Blocker Count: 3
Scope Expansion Required: NO
Rewrite of Passed B4 Model Required: NO
Historical Record Mutation Required: NO
```

## 七、阶段判定

```text
CR-0004-R1 Independent Review: COMPLETED
Review Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
CR-0004-R1 Consolidation: BLOCKED
CR-0004-R2 Required: YES
CR-0004-R2 Scope: R1-B1 + R1-B2 + R1-B3 only
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只能建立 `CR-0004-R2`，并且只处理本审查列出的三个残余阻断。R2 完成后仍必须独立复审；在复审通过和后续合并完成前，不得声称 `WS-01` 已退出或任何制度已经冻结。
