# CR-0004-R4 独立封印状态与启动模式复审

## 审查信息

```text
Review ID: CR-0004-R4-LOCAL-REVIEW
Review Type: Independent Seal State, Progress and Mode Arbitration Review
Status: COMPLETED
Result: PASS_WITH_ONE_BOUNDED_BLOCKER
Executable: NO
Reviewed Proposal: CR-0004-R4
Reviewed Workstream: WS-01
Repair Basis: CR-0004-R3-LOCAL-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-check ignored; separate immutable review record; not an external freeze review
External Approval Required: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0004-R4` 是否关闭 R3 审查的一个阻断。它不修改基础稿、R1 至 R4 或既有审查记录，不创建制度冻结、冻结标识、注册表、账本、提交解析或运行时权威。

## 审查命题

本轮独立回答：

1. 原始完整封印是否与四值封印状态明确分离；
2. `SEALED_COMPLETE | NOT_SEALED | INDETERMINATE | CONFLICTED` 是否都拥有已登记状态路径；
3. 冲突状态是否能形成已登记冲突终局；
4. 未封印或未知状态是否能形成不会锁死未来终局的已登记进度；
5. 状态、进度和终局载体是否无摘要自引用；
6. 当前启动模式是否由唯一已登记仲裁事实产生；
7. 终局不存在是否拥有合格否定证明；
8. 已有终局之后出现迟到冲突时，当前模式是否确定；
9. R4 是否达到合并候选门槛。

## 审查依据

```text
AGENTS.md
IF-0001 Authority Model
IF-0006 Evidence Model
IF-0007 Institution Model
CR-0002-CONSTITUTION-CANDIDATE
CR-0003-CONSTITUTION-CANDIDATE-R2
CR-0004
CR-0004-R1
CR-0004-R2
CR-0004-R3
CR-0004-R3-LOCAL-REVIEW
CR-0004-R4
Local repository state at review time
```

R4 自检、作者身份和历史讨论全部忽略，不作为通过依据。

## 总体结论

R4 已完整修复 R3 审查指出的封印状态与失败分支不可达问题：

```text
Raw Seal / Seal State Separation: PASS
Four-value Seal State Registration: PASS
CONFLICTED Terminal Candidate Reachability: PASS
INDETERMINATE Progress Reachability: PASS
Progress / Terminal Key Separation: PASS
Progress Does Not Consume Terminal Slot: PASS
Seal-state Input Acyclicity: PASS
Progress Input Acyclicity: PASS
New Carrier Boundary Integration: PASS
```

但进度与终局之间的当前模式仲裁仍有一个有界缺口：

```text
R4-B1 Registered Mode Arbitration and Post-terminal Conflict Projection: BLOCKED
```

因此：

```text
Proposal Structure: PASS
R3-B1 Original Repair: PASS
Seal-state Reachability: PASS
Progress / Terminal Separation: PASS
Mode Arbitration Closure: FAIL
Consolidation Eligibility: FAIL
WS-01 Exit Eligibility: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_ONE_BOUNDED_BLOCKER
```

该缺口可在一个严格有界 `CR-0004-R5` 中修复，不需要重写 R4 的四值封印状态、进度／终局分载体或 R3 的启动证据集合。

## 一、通过项

### 原始封印与四值状态

R4 将原始封印记录限定为正向 `SEALED_COMPLETE` 事实，失败、未知和冲突只由独立状态解析表达。

封印状态输入向量不包含状态解析账本、进度账本或终局账本，因此：

```text
Raw Seal Fact Self-reference: ABSENT
Seal State Resolution Self-reference: ABSENT
Missing Seal != NOT_SEALED: PASS
Late Evidence -> Seal State CONFLICTED: REACHABLE
```

### 冲突终局与未知进度

R4 让已登记 `CONFLICTED` 封印状态进入冲突终局候选，让 `NOT_SEALED` 或 `INDETERMINATE` 进入独立进度载体。

进度键包含状态解析和认识边界，终局键继续只绑定冲突集合。因此较早未知不会占用终局单赋值键。

```text
Registered CONFLICTED State -> Terminal Candidate: PASS
Registered INDETERMINATE State -> Progress Candidate: PASS
Progress / Terminal Type Separation: PASS
Later Terminal after Earlier Progress: ALLOWED
Progress Opens NATIVE: PROHIBITED
```

### 新增载体边界

封印状态解析账本和关闭进度解析账本均被加入启动来源向量，且分别要求独立完整性。

```text
New Carrier Identity: PASS
Independent Completeness: PASS
Completeness Propagation: PROHIBITED
```

## 二、阻断 R4-B1：当前模式仲裁缺少已登记权威事实

### 终局不存在仍是自由否定

`IR-R4-19` 允许：

```text
no registered terminal closure
+ terminal closure ledger boundary COMPLETE
+ exact Registered Closure Progress = INDETERMINATE
-> COMMIT_UNRESOLVED
```

但 R4 没有定义：

```text
Qualified Terminal Absence Proof
Bootstrap Terminal Presence Resolution Key
Registered Terminal Presence Resolution Record
Terminal Presence Resolution Authority
```

“边界完整且查询未找到记录”没有被显式提升为合格、适用、已登记的否定证明。R4 自身还声明进度记录不能证明终局不存在。

因此 `COMMIT_UNRESOLVED` 仍依赖消费者对“没有终局”的自由判断。

### 终局后冲突无法形成新的规范模式

R4 的终局键是单赋值：

```text
Bootstrap Closure Resolution Key = Conflict Set Key
```

如果已经登记 `COMMITTED` 或 `ABORTED`，之后发现迟到证据，封印状态会变为 `CONFLICTED`，并产生新的 `CONFLICTED` 终局候选。

但单赋值规则会拒绝该不同载荷，只把终局账本完整性变为 `CONFLICTED`：

```text
existing COMMITTED terminal
+ later registered Seal State = CONFLICTED
+ new CONFLICTED terminal candidate rejected
-> terminal ledger completeness CONFLICTED
```

`IR-R4-19` 在终局账本不完整时落入：

```text
BOOTSTRAP_CLOSURE_STATE_PENDING
```

而不是已登记 `CONFLICTED` 当前模式。于是同一事实集仍可能被解释为“旧成功终局失效后的安全等待”或“当前冲突”，缺少唯一规范结论。

### 仲裁层缺失

当前模型有多个已登记输入：

```text
Seal State Resolution
Closure Progress Resolution
Terminal Closure Resolution
Terminal Ledger Conflict Evidence
Source Boundary Completeness Records
```

但没有：

```text
Bootstrap Closure Mode Source Vector
Candidate Bootstrap Closure Mode Resolution Record
Registered Bootstrap Closure Mode Resolution Record
Mode Resolution Execution Authority
Mode Resolution Registration Authority
Mode Resolution Ledger
```

`ACTIVE_CLOSED`、`ABORTED_CLOSED`、`COMMIT_UNRESOLVED`、`CONFLICTED` 与安全未知仍由自由投影选择。

### 风险

当前结构不会错误开放 `NATIVE`，但会在以下场景失去唯一当前状态：

```text
qualified progress + terminal absence
old terminal + new seal-state conflict
terminal carrier conflict
progress carrier conflict
incomplete current boundary
```

这不满足“已登记终局／模式是唯一规范来源”的原始审查目标。

### 有界修复要求

`CR-0004-R5` 必须补充：

1. 稳定 `Bootstrap Closure Mode Source Vector`，绑定封印状态、进度、终局、终局登记冲突证据、全部来源边界和完整性记录；
2. 已登记 `Terminal Presence Resolution`，或等价的合格终局存在／不存在解析，值域至少区分 `PRESENT | ABSENT | INDETERMINATE | CONFLICTED`；
3. 独立候选／登记的 `Bootstrap Closure Mode Resolution` 及执行／登记权威和独立载体；
4. 模式结果至少包含 `ACTIVE_CLOSED | ABORTED_CLOSED | COMMIT_UNRESOLVED | CONFLICTED | INDETERMINATE`；
5. 迟到证据、封印状态冲突、终局登记冲突或终局载体完整性冲突必须支配旧 `COMMITTED/ABORTED`，形成已登记 `CONFLICTED` 模式解析；
6. 只有合格已登记终局不存在解析与精确已登记进度共同成立时，才能产生 `COMMIT_UNRESOLVED`；
7. 任一必需来源缺失或边界不完整必须产生 `INDETERMINATE`，不得自由选择旧终局或进度；
8. 只有已登记模式解析可以投影实际 `Bootstrap Mode`；
9. 模式输入向量不得包含模式解析账本自身，模式解析账本必须作为下游启动引用的独立完整来源。

```text
Finding R4-B1: BLOCKING
Repair Scope: registered current-mode arbitration and post-terminal conflict projection only
```

## 三、非阻断观察

以下仍是外部冻结治理依赖，不是本轮新增阻断：

```text
IF-0007 authoritative institution freeze
WS-02 through WS-08 completion
Provider-source reality-bound evidence
Independent external approval where required
Runtime carrier implementation and migration
```

R4 和本审查均无权威且不可执行，不创建任何注册表、账本、冻结标识、冻结事实或运行时权威。

## 四、阻断矩阵

| 阻断 | R4 已完成 | 残余缺口 | R5 最小退出条件 |
|---|---|---|---|
| R4-B1 | 封印四值状态、未知进度、冲突终局均可登记 | 终局不存在和终局后冲突仍无唯一已登记模式仲裁 | 建立存在解析、模式源向量和已登记模式解析 |

```text
Bounded Blocker Count: 1
Scope Expansion Required: NO
Rewrite of Seal-state Model Required: NO
Rewrite of Progress / Terminal Separation Required: NO
Historical Record Mutation Required: NO
```

## 五、阶段判定

```text
CR-0004-R4 Independent Review: COMPLETED
Review Result: PASS_WITH_ONE_BOUNDED_BLOCKER
CR-0004-R4 Consolidation: BLOCKED
CR-0004-R5 Required: YES
CR-0004-R5 Scope: R4-B1 only
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只需建立 `CR-0004-R5`，补齐已登记终局存在解析和当前模式仲裁。R5 完成后仍须独立复审；复审通过前不得合并或声称 `WS-01` 已完成。
