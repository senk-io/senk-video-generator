# CR-0004-R2 独立模型与启动闭环复审

## 审查信息

```text
Review ID: CR-0004-R2-LOCAL-REVIEW
Review Type: Independent Residual Model and Bootstrap Closure Review
Status: COMPLETED
Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
Executable: NO
Reviewed Proposal: CR-0004-R2
Reviewed Workstream: WS-01
Repair Basis: CR-0004-R1-LOCAL-REVIEW
Reviewer: Codex
Review Authority: User-delegated proposal review authority
Review Independence: Proposal self-check ignored; separate immutable review record; not an external freeze review
External Approval Required: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
```

> 本文件只独立复审 `CR-0004-R2` 是否完整关闭 `CR-0004-R1-LOCAL-REVIEW` 的三个残余阻断。它不修改基础稿、R1、R2 或既有审查记录，不创建制度冻结、冻结标识、注册表、账本、提交解析或运行时权威。

## 审查命题

本轮独立回答：

1. 分配四值解析是否具有稳定身份、独立权威和可被冻结引用重新验证的完整载体边界；
2. 生命周期竞争集合是否真正捕获不同决定标识、不同继任目标和不同语义域之间的全部竞争；
3. 生命周期域内效果是否能够合成为唯一的引用适用性结论；
4. 启动清单、窗口核心、最终窗口和提交解析之间是否无摘要循环；
5. 启动解析能否在不引用自身登记结果的前提下识别跨键冲突；
6. `ACTIVE_CLOSED`、失败关闭和冲突状态是否只有一个已登记规范来源；
7. R2 是否达到合并候选门槛。

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
CR-0004-R1-LOCAL-REVIEW
CR-0004-R2
Local repository state at review time
```

R2 的自检结论、作者身份和历史讨论全部忽略，不作为通过依据。

## 总体结论

R2 对三个原残余阻断均完成了实质性修复：

```text
Allocation Fact / Resolution Separation: PASS
Allocation Resolution Stable Identity: PASS
Lifecycle Relation / Conflict-set Separation: PASS
Lifecycle Intra-domain Conflict Preservation: PASS
Bootstrap Manifest Single-key Identity: PASS
Bootstrap Window Single-key Identity: PASS
Manifest / Window Digest Cycle Removal: PASS
Window / Final Resolution Key Cycle Removal: PASS
Legacy Bootstrap Closed Record Retirement: PASS
Registered COMMITTED Required for ACTIVE_CLOSED: PASS
```

但独立复算发现三个新的有界集成缺口：

```text
R2-B1 New Resolution Carriers and Boundary-vector Integration: BLOCKED
R2-B2 Cross-domain Lifecycle Applicability Composition: BLOCKED
R2-B3 Bootstrap Resolution-set Identity and Non-self-referential Closure: BLOCKED
```

因此：

```text
Proposal Structure: PASS
Repair Direction: PASS
Original R1-B1 Closure: PASS_WITH_INTEGRATION_BLOCKER
Original R1-B2 Closure: PASS_WITH_COMPOSITION_BLOCKER
Original R1-B3 Closure: PASS_WITH_RESOLUTION_BLOCKER
Consolidation Eligibility: FAIL
WS-01 Exit Eligibility: FAIL
Institution Freeze Eligibility: FAIL
Overall Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
```

三个缺口都能在一个有界 `CR-0004-R3` 中修复，不要求推翻 R2 的分配解析键、窗口核心、清单唯一键或旧关闭记录退场规则。

## 一、已通过项

### 分配事实与解析事实分离

R2 正确区分正向 `Freeze ID Allocation Record` 与四值 `Registered Freeze ID Allocation Resolution Record`，并建立解析执行／登记分权、稳定键、候选—登记链、内容同一和完整真值表。

```text
Missing Allocation Record != NOT_ALLOCATED: PASS
Candidate Resolution != Registered Resolution: PASS
Allocation Authority != Resolution Authority: PASS
Registered ALLOCATED Consumption Gate: PASS
```

### 生命周期域内冲突保留

R2 使 `Lifecycle Decision Fact ID` 只承担谱系身份，不再隔离来源版本的语义竞争。它还定义关系成员资格、规范效果、显式替代和禁止最后写入获胜。

```text
Decision ID Conflict Escape Prevention: PASS
Append-only Displaced History: PASS
Implicit Time-order Precedence: PROHIBITED
Intra-domain Four-value Resolution: PASS
```

### 启动控制对象身份

R2 的 `Bootstrap Manifest Key` 只绑定 `GENESIS` 启动纪元，不能通过清单摘要或契约版本换键。窗口键同样不含清单、窗口摘要或契约版本。

窗口核心在清单摘要前形成，最终窗口在清单与外部锚登记后形成；窗口只绑定不含最终窗口摘要的提交解析核心键。因此：

```text
Manifest -> Window Core: ACYCLIC
Registered Manifest + External Anchor -> Final Window: ACYCLIC
Final Window -> Commit Resolution Core Key: ACYCLIC
Final Resolution Key -> Registered Window: FORWARD_ONLY
```

原 `Bootstrap Closed Record` 已明确降为非规范历史断言，不能开放 `NATIVE`。

```text
Single Manifest Key: PASS
Single Window Key: PASS
Known R1 Digest Cycles: CLOSED
Legacy Closure Bypass: CLOSED
```

## 二、阻断 R2-B1：新增解析载体没有接入边界向量

### 本地事实

R2 新增并要求消费：

```text
Registered Freeze ID Allocation Resolution Record
Registered Lifecycle Effect Resolution Record
Registered Bootstrap Manifest Registration Resolution Record
```

分配解析登记尝试还引用“目标解析账本”，但 R2 没有定义该解析账本的稳定来源身份、追加边界和完整性记录。

R1 `IR-R1-43` 的最低来源仍只有：

```text
Freeze ID Allocation Ledger
Lifecycle Registry
Bootstrap Manifest Carrier
Bootstrap Resolution Ledger
```

它没有明确包含：

```text
Freeze ID Allocation Resolution Ledger
Lifecycle Effect Resolution Ledger
Bootstrap Manifest Registration Resolution Ledger
```

R1 `IR-R1-48` 至 `IR-R1-50` 的三模式必需来源仍只要求分配记录和“适用生命周期记录”，没有要求 R2 新增的已登记分配解析、生命周期效果解析及其独立完整边界。

### 分配边界内部缺口

`IR-R2-06` 的分配解析键绑定分配账本边界与“命名空间边界完整性记录”，但没有分别绑定：

```text
Registered Allocation Ledger Boundary Completeness Record
Registered Namespace Boundary Completeness Record
```

`IR-R2-09` 又同时要求两个边界均为 `COMPLETE`。当前候选字段中只有一个未指明来源的 `Registered Boundary Completeness Record`，无法证明两个不同边界分别完整。

### 风险

一个冻结决定可以引用已登记 `ALLOCATED`，但后续冻结引用解析的 `Institution Resolution Boundary Vector` 不一定包含该解析记录的载体或完整性边界。生命周期效果也可能被引用适用性直接消费，却没有独立解析账本边界进入认识向量。

这允许：

```text
registered resolution exists
+ resolution carrier omitted from boundary vector
-> downstream cannot prove completeness or detect competing registered resolutions
```

一个来源的完整性记录不能证明另一个来源完整；因此不能把分配账本、生命周期注册表或启动清单载体的完整性隐式传播给解析载体。

### 有界修复要求

`CR-0004-R3` 必须补充：

1. 明确定义 `Freeze ID Allocation Resolution Ledger` 与 `Lifecycle Effect Resolution Ledger` 的稳定身份、追加语义和登记边界；
2. 明确清单登记解析使用独立账本，或规范声明其属于现有 `Bootstrap Resolution Ledger` 的精确子域；
3. 为每个新增解析来源建立独立 `Registered Source Boundary Completeness Record`；
4. 将这些来源加入 `Institution Resolution Boundary Vector` 的模式相关必需条目；
5. `NATIVE` 与 `PROSPECTIVE` 模式必须引用精确已登记 `ALLOCATED` 解析及其完整边界；
6. 三种模式都必须引用用于当前适用性结论的生命周期解析来源及其完整边界；
7. 分配解析键必须分别绑定分配账本和命名空间两个完整性记录，不得用一个模糊记录证明两个边界。

```text
Finding R2-B1: BLOCKING
Repair Scope: resolution carrier identity and boundary-vector integration only
```

## 三、阻断 R2-B2：生命周期域内结论没有唯一合成

### 本地事实

R2 定义三个语义域：

```text
SOURCE_VERSION_APPLICABILITY
SUCCESSOR_SELECTION
DEPRECATION_SIGNAL
```

每个域都可以产生自己的：

```text
EFFECTIVE
NOT_EFFECTIVE
INDETERMINATE
CONFLICTED
```

但 `IR-R2-23` 直接规定“已登记生命周期效果解析”进入冻结引用适用性，没有定义：

```text
Lifecycle Domain Resolution Vector
Composite Lifecycle Applicability Resolution Key
Candidate Composite Lifecycle Applicability Resolution Record
Registered Composite Lifecycle Applicability Resolution Record
Cross-domain precedence and conflict truth table
```

同一来源版本在同一查询坐标上可以同时得到：

```text
SOURCE_VERSION_APPLICABILITY -> EFFECTIVE / NOT_APPLICABLE_FOR_NEW_USE
DEPRECATION_SIGNAL -> EFFECTIVE / APPLICABLE_WITH_DEPRECATION
SUCCESSOR_SELECTION -> EFFECTIVE / exact successor
```

R2 没有说明这些结果如何形成 R1 所需的唯一 `APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED` 结论。

### 继任目标冲突逃逸

`SUCCESSOR_SELECTION` 的竞争集合键包含精确继任目标。因此两个不同继任目标会形成两个不同竞争集合，各自都可能解析为 `EFFECTIVE`。

R2 文本要求“不兼容继任目标”产生 `CONFLICTED`，但没有一个排除目标字段的父集合或合成键把两个目标放入同一权威比较边界。

```text
successor A -> conflict set A -> EFFECTIVE
successor B -> conflict set B -> EFFECTIVE
no registered parent aggregation -> conflict not authoritatively resolved
```

来源适用性域虽然可以观察到两个规范效果携带不同目标，但域内兼容规则没有取代缺失的跨域和跨目标合成记录。

### 风险

不同消费者可能选择不同域结果、不同继任目标或不同应用顺序。`REVOKES`、`SUPERSEDES` 与 `DEPRECATES` 同时存在时，当前模型没有权威规则确定撤销是否压倒弃用、继任目标是否唯一，以及任一域未知或冲突是否支配总结果。

### 有界修复要求

`CR-0004-R3` 必须补充：

1. 排除精确继任目标的 `Successor Selection Conflict Set Key`，或建立覆盖全部目标成员的父聚合键；
2. 稳定 `Lifecycle Domain Resolution Vector`，绑定三个必需语义域的精确已登记结果、边界、`Valid At`、`Known At`、视图模式和规则版本；
3. 独立候选／登记的复合生命周期适用性解析及执行／登记权威；
4. 完整合成真值表，至少明确撤销、替代、弃用、多个继任目标、域未知和域冲突的优先关系；
5. 任一必需域为 `CONFLICTED` 时总结果为 `CONFLICTED`，任一必需域无法证明完整时不得产生确定适用结论；
6. 只有已登记复合结果可以进入 R1 冻结引用适用性，单一域结果不得直接成为最终输入。

```text
Finding R2-B2: BLOCKING
Repair Scope: cross-target and cross-domain lifecycle composition only
```

## 四、阻断 R2-B3：启动解析集合存在终局自引用与自由冲突投影

### 已通过的无环部分

R2 成功消除了：

```text
manifest digest <-> final window digest
final window digest <-> final commit resolution key
```

该部分不构成阻断。

### 新的终局边界循环

`IR-R2-30` 的最终 `Bootstrap Commit Resolution Key` 包含：

```text
Bootstrap Resolution Ledger Boundary ID and Digest
```

同时，待登记的 `Registered Bootstrap Commit Resolution Record` 自身将写入该解析账本。

R2 没有声明该边界是：

```text
strictly pre-registration input boundary
candidate-excluding boundary
immutable exact prior record set
```

如果边界包含当前解析记录，则：

```text
resolution record payload
  -> resolution key
  -> resolution ledger boundary digest
  -> resolution record payload
```

形成摘要自引用。若边界排除当前记录，R2 又没有定义如何在登记后检测同时或随后出现的同纪元竞争解析。

### 跨键冲突缺少已登记集合解析

R2 规定同一启动纪元出现多个不兼容解析键时，启动模式“只能是 `CONFLICTED`”。但最终解析键包含窗口、尝试和多个边界摘要；不同键不会触发同键不同载荷规则。

当前没有：

```text
Bootstrap Commit Resolution Conflict Set Key
Conflict-set Membership Rule
Candidate Cross-key Bootstrap Closure Resolution Record
Registered Cross-key Bootstrap Closure Resolution Record
```

因此“多个不兼容解析键 -> `CONFLICTED`”仍是自由计算投影，与 `IR-R2-32` 声称只有已登记提交解析可以产生规范关闭状态之间存在竞争语义。

### 风险

一个边界较早的 `COMMITTED` 解析可能开放 `ACTIVE_CLOSED`，而另一边界上的冲突解析只能依赖自由观察将模式改为 `CONFLICTED`。消费者无法确定哪个结果是规范终局，也无法在不引入自引用的情况下证明解析集合完整。

### 有界修复要求

`CR-0004-R3` 必须补充：

1. 将最终解析记录引用的解析账本边界明确为严格前置、排除当前候选的输入边界，或从解析记录内容身份中移除会包含自身的边界摘要；
2. 建立不含结果记录 ID、结果摘要和观察边界的 `Bootstrap Commit Resolution Conflict Set Key`，至少绑定启动纪元、规范清单键、窗口键和允许的内部尝试 ID；
3. 定义所有已登记启动提交解析加入该集合的确定规则，不得通过改变边界或规则结果键逃逸；
4. 建立独立候选／登记的跨键终局解析及其分权、完整边界和内容同一；
5. 只有已登记跨键终局解析可以投影 `ACTIVE_CLOSED | ABORTED_CLOSED | CONFLICTED | COMMIT_UNRESOLVED`；
6. 删除或覆盖“自由观察多个键直接改变模式”的语义，保持唯一规范关闭来源；
7. 明确 `Bootstrap Manifest Registration Resolution`、窗口和跨键终局解析分别使用哪个载体及完整性边界。

```text
Finding R2-B3: BLOCKING
Repair Scope: non-self-referential resolution input boundary and registered cross-key closure only
```

## 五、非阻断观察

以下事项仍是后续冻结治理依赖，不是本轮新增阻断：

```text
IF-0007 authoritative institution freeze
WS-02 through WS-08 completion
Provider-source reality-bound evidence
Independent external approval where required
Runtime carrier implementation and migration
```

R2 及本审查均为无权威、不可执行的提案层记录。任何 `PASS` 项都不创建注册表、账本、冻结标识、冻结事实或运行时权威。

## 六、阻断矩阵

| 阻断 | R2 已完成 | 残余缺口 | R3 最小退出条件 |
|---|---|---|---|
| R2-B1 | 分配与生命周期解析具备稳定记录身份 | 新解析载体及完整边界未进入认识向量和三模式来源 | 定义解析载体、独立完整性并更新模式来源向量 |
| R2-B2 | 域内成员、效果、显式替代和四值解析 | 跨目标、跨域结果没有唯一已登记合成 | 建立域向量、父冲突集和复合适用性解析 |
| R2-B3 | 清单／窗口唯一化并消除两类摘要环 | 终局解析账本边界可能自含，跨键冲突仍是自由投影 | 建立前置输入边界和已登记跨键终局解析 |

```text
Bounded Blocker Count: 3
Scope Expansion Required: NO
Rewrite of Passed Manifest / Window Model Required: NO
Historical Record Mutation Required: NO
```

## 七、阶段判定

```text
CR-0004-R2 Independent Review: COMPLETED
Review Result: PASS_WITH_THREE_BOUNDED_BLOCKERS
CR-0004-R2 Consolidation: BLOCKED
CR-0004-R3 Required: YES
CR-0004-R3 Scope: R2-B1 + R2-B2 + R2-B3 only
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只能建立 `CR-0004-R3`，且只处理新增解析载体的边界集成、生命周期跨域合成和启动跨键终局解析。R3 完成后仍须独立复审；在复审和后续合并通过前，不得声称 `WS-01` 已退出或任何制度已经冻结。
