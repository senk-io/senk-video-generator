# 制度注册表封印状态与启动终局可达性有界修订 R4

## 修订信息

```text
Proposal ID: CR-0004-R4
Title: Bootstrap Seal State and Closure Reachability R4
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0004-R3
Repair Basis: CR-0004-R3-LOCAL-REVIEW
Repair Scope: R3-B1 only
Proposal Form: BOUNDED_NORMATIVE_OVERLAY
Independent Review Required: YES
Consolidation Required: YES
Institution Freeze Created: NO
Freeze ID Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
```

> 本文件只修复 `CR-0004-R3-LOCAL-REVIEW` 的一个阻断。它不是制度冻结，不创建任何实际载体、注册表、账本、冻结标识、提交解析或运行时权威，也不修改 R3 和既有历史记录。

## 一、修订解释边界

### IR-R4-01 R4 只处理一个阻断

```text
R3-B1 Seal-state Registration and Failure-terminal Reachability
```

R3 已通过的解析载体、分配双完整性、生命周期跨域合成、启动证据冲突集合和三层无环结构继续成立。

### IR-R4-02 R4 显式覆盖不可达入口

R4 在本范围内细化或覆盖：

```text
IR-R3-26 raw seal result semantics
IR-R3-27 late evidence effect
IR-R3-30 closure candidate entrance
IR-R3-31 closure truth table
IR-R3-33 unresolved mode projection
IR-R3-35 bootstrap resolution source vector
```

该覆盖只用于后续合并候选，不赋予 R4 权威。

### IR-R4-03 未决进度与不可变终局必须分离

```text
Bootstrap Closure Progress Resolution
  = boundary-specific registered nonterminal observation

Bootstrap Closure Terminal Resolution
  = single-assignment registered terminal result
```

`INDETERMINATE` 不得写入单赋值终局并永久阻止后续成功封印。它必须作为可版本化的进度解析保存；确定的 `COMMITTED`、`ABORTED` 或 `CONFLICTED` 才能进入终局。

## 二、不可变封印与封印状态分离

### IR-R4-04 原始封印只表达完整封印事实

R4 将 `Bootstrap Commit Evidence Boundary Seal Record` 限定为不可变正向事实：

```text
Seal Fact Result: SEALED_COMPLETE
```

只有精确证据集合、证据解析账本边界 `COMPLETE`、成员资格确定且无迟到证据时，才能登记该记录。

以下不是封印事实：

```text
NOT_SEALED
INDETERMINATE
CONFLICTED
```

它们只能由独立封印状态解析表达。失败的封印尝试、冲突候选和读取失败不得伪装为不可变封印记录。

### IR-R4-05 原始封印键必须受保护单赋值

`Bootstrap Commit Evidence Boundary Seal Ledger` 对 R3 封印键执行：

```text
no registered seal + qualified SEALED_COMPLETE candidate -> register once
same key + same content -> idempotent reference to original seal
same key + different content -> reject and append seal registration conflict evidence
```

不同载荷不能成为第二个封印事实。冲突尝试、迟到证据和越界写入继续进入封印账本冲突子域，并由封印状态解析消费。

## 三、封印状态解析

### IR-R4-06 封印状态解析必须拥有独立载体

新增逻辑载体：

```text
Bootstrap Commit Evidence Seal State Resolution Ledger
```

最低载体字段继续遵循 R3 解析载体契约。该载体只保存封印状态解析，不保存原始封印、证据解析、迟到证据或启动终局。

它必须拥有独立 `Registered Source Boundary Completeness Record`，不能继承证据解析账本或封印账本的完整性。

### IR-R4-07 封印状态解析必须独立分权

新增：

```text
Bootstrap Commit Evidence Seal State Resolution Execution Authority Type
Bootstrap Commit Evidence Seal State Resolution Registration Authority Type
```

执行者只能读取精确证据集合边界、封印事实边界和封印冲突子域，生成候选状态。登记者只能登记内容相同且合格的候选。

二者均不得登记或修改证据解析、封印事实、迟到证据、终局或启动模式。

### IR-R4-08 封印状态输入必须形成无环向量

```text
Bootstrap Evidence Seal State Input Vector =
  Bootstrap Commit Resolution Conflict Set Key
+ Evidence Resolution Ledger Boundary ID and Digest
+ Registered Evidence Ledger Boundary Completeness Record ID and Digest
+ Boundary Seal Ledger Boundary ID and Digest
+ Registered Seal Ledger Boundary Completeness Record ID and Digest
+ Covered Seal Conflict Subdomain Boundary
+ Valid At
+ Known At
+ View Mode
+ Seal State Input Rule Version
+ Vector Digest
```

该向量禁止包含：

```text
Bootstrap Commit Evidence Seal State Resolution Ledger
current candidate seal-state resolution
Bootstrap Closure Progress Resolution Ledger
Bootstrap Closure Resolution Ledger
current closure progress or terminal record
```

因此状态解析不能通过自身载体证明自身输入完整。

### IR-R4-09 封印状态解析必须拥有稳定键

```text
Bootstrap Commit Evidence Seal State Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Evidence Seal State Input Vector Digest
+ Seal State Resolution Rule Version
```

边界、认识时间、视图模式或规则变化必须形成新的历史状态解析身份；不得覆盖旧状态。

### IR-R4-10 封印状态必须形成候选—登记链

```text
Bootstrap Evidence Seal State Input Vector
  -> Candidate Bootstrap Commit Evidence Seal State Resolution Record
  -> Bootstrap Commit Evidence Seal State Resolution Registration Attempt
  -> Registered Bootstrap Commit Evidence Seal State Resolution Record
```

候选和已登记记录至少共同绑定：

```text
Seal State Resolution Record ID
Seal State Resolution Key
Conflict Set Key
Input Vector ID and Digest
Matched SEALED_COMPLETE Seal Record ID and Digest when applicable
Seal Registration Conflict Record IDs and Digests
Late Evidence Conflict Record IDs and Digests
Covered Evidence Set Digest when available
Seal State Result
Resolution Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

```text
Candidate Seal State Resolution Payload Digest
= Registered Seal State Resolution Payload Digest
```

### IR-R4-11 封印状态使用完整四值

```text
SEALED_COMPLETE
NOT_SEALED
INDETERMINATE
CONFLICTED
```

确定规则：

```text
exactly one registered content-identical SEALED_COMPLETE seal fact
+ exact covered evidence set
+ evidence resolution ledger boundary COMPLETE
+ seal ledger boundary COMPLETE
+ no seal-registration conflict
+ no late evidence conflict
-> SEALED_COMPLETE

qualified applicable complete proof of no registered seal fact
+ evidence resolution ledger boundary COMPLETE
+ seal ledger boundary COMPLETE
+ no conflict evidence
-> NOT_SEALED

multiple incompatible seal facts or candidates
or seal registration conflict evidence
or late evidence conflict
or seal covered set differs from conflict-set membership
or incompatible registered seal-state resolutions for the same key
-> CONFLICTED

missing required source
or any required boundary not COMPLETE
or proof qualification unavailable
or timeout, unavailable carrier or read failure
-> INDETERMINATE
```

`NOT_SEALED` 不能由空查询、未找到、读取失败或不完整边界推断。

### IR-R4-12 封印状态解析账本保持历史而不锁死进度

状态解析键包含输入向量摘要，因此较早的 `NOT_SEALED` 或 `INDETERMINATE` 不阻止较晚边界形成 `SEALED_COMPLETE`。

同一状态解析键同载荷幂等；同键不同载荷必须拒绝第二登记、追加状态登记冲突证据，并使状态解析账本边界完整性为 `CONFLICTED`。

消费者必须使用精确 `Known At` 和边界向量选择状态，不能用“最新”或记录顺序覆盖历史。

## 四、启动关闭进度解析

### IR-R4-13 非终局未知必须进入独立进度载体

新增逻辑载体：

```text
Bootstrap Closure Progress Resolution Ledger
```

新增：

```text
Bootstrap Closure Progress Resolution Execution Authority Type
Bootstrap Closure Progress Resolution Registration Authority Type
```

进度解析只表达：

```text
INDETERMINATE
```

它不是提交成功、提交中止、冲突终局或关闭事实。

### IR-R4-14 进度解析必须拥有边界化身份

```text
Bootstrap Closure Progress Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Registered Seal State Resolution ID and Digest
+ Seal State Resolution Ledger Boundary ID and Digest
+ Known At
+ Closure Progress Rule Version
```

```text
Registered Seal State = NOT_SEALED or INDETERMINATE
  -> Candidate Bootstrap Closure Progress Resolution Record
  -> Bootstrap Closure Progress Resolution Registration Attempt
  -> Registered Bootstrap Closure Progress Resolution Record
```

候选和已登记进度必须内容同一，并绑定精确封印状态、状态解析账本完整性、冲突集合、认识时间、规则版本、权威和证据。

### IR-R4-15 未决进度不得占用终局单赋值键

`Bootstrap Closure Progress Resolution Key` 与 R3 `Bootstrap Closure Resolution Key` 是不同类型和不同载体。

较早 `INDETERMINATE` 进度不得：

```text
consume terminal single-assignment slot
block later COMMITTED, ABORTED or CONFLICTED terminal
open NATIVE
claim bootstrap closed
overwrite later progress or history
```

## 五、所有封印状态进入关闭解析

### IR-R4-16 终局候选入口必须消费已登记封印状态

R4 覆盖 R3 仅接受原始 `SEALED_COMPLETE` 的入口：

```text
Registered Bootstrap Commit Evidence Seal State Resolution
  -> Closure Branch Selection
```

分支：

```text
SEALED_COMPLETE -> terminal closure candidate evaluation
CONFLICTED -> terminal CONFLICTED candidate
NOT_SEALED -> nonterminal INDETERMINATE progress candidate
INDETERMINATE -> nonterminal INDETERMINATE progress candidate
```

原始封印事实不能绕过状态解析直接进入终局。

终局候选或进度候选必须绑定：

```text
Registered Seal State Resolution ID and Digest
Seal State Resolution Ledger Boundary ID and Digest
Registered Seal State Resolution Ledger Completeness Record ID and Digest
Exact Raw Seal Fact ID and Digest when state is SEALED_COMPLETE
```

状态解析账本边界非 `COMPLETE` 时，任何关闭候选都不合格。

### IR-R4-17 确定封印状态形成终局

以下所有分支都要求精确已登记封印状态解析及其状态解析账本边界 `COMPLETE`：

```text
Registered Seal State = SEALED_COMPLETE
+ exact seal fact and covered evidence set
+ every applicable evidence result converges on COMMITTED
+ all source boundaries COMPLETE
-> Candidate Terminal Result: COMMITTED

Registered Seal State = SEALED_COMPLETE
+ exact seal fact and covered evidence set
+ every applicable evidence result converges on ABORTED
+ qualified applicable complete proof of no protected write
+ all source boundaries COMPLETE
-> Candidate Terminal Result: ABORTED

Registered Seal State = SEALED_COMPLETE
+ sealed evidence results or control chains conflict
-> Candidate Terminal Result: CONFLICTED

Registered Seal State = CONFLICTED
-> Candidate Terminal Result: CONFLICTED
```

终局候选继续使用 R3 的：

```text
Bootstrap Closure Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
```

终局值域缩减为：

```text
COMMITTED | ABORTED | CONFLICTED
```

并继续使用受保护单赋值登记。

### IR-R4-18 非确定封印状态形成已登记进度

```text
Registered Seal State = NOT_SEALED
or Registered Seal State = INDETERMINATE
+ Seal State Resolution Ledger Boundary COMPLETE
-> Registered Bootstrap Closure Progress Resolution = INDETERMINATE
```

缺失封印状态解析或封印状态解析账本边界非 `COMPLETE` 时，不得自由推断进度；只能保持非规范安全状态 `BOOTSTRAP_SEAL_STATE_RESOLUTION_PENDING`，失败关闭所有写入。

### IR-R4-19 启动模式投影使用互斥优先级

```text
exact Registered Terminal Closure = COMMITTED
+ terminal ledger boundary COMPLETE
-> ACTIVE_CLOSED

exact Registered Terminal Closure = ABORTED
+ terminal ledger boundary COMPLETE
-> ABORTED_CLOSED

exact Registered Terminal Closure = CONFLICTED
+ terminal ledger boundary COMPLETE
-> CONFLICTED

no registered terminal closure
+ terminal closure ledger boundary COMPLETE
+ exact Registered Closure Progress = INDETERMINATE
+ progress ledger boundary COMPLETE
+ exact applicable seal-state resolution
+ seal-state resolution ledger boundary COMPLETE
-> COMMIT_UNRESOLVED

otherwise
-> BOOTSTRAP_CLOSURE_STATE_PENDING
```

已登记终局存在时，匹配同一冲突集合的旧进度记录只作为历史保留，不能覆盖终局。终局账本或进度账本完整性冲突时，不得产生确定模式或开放 `NATIVE`。

## 六、载体与边界集成

### IR-R4-20 新增状态和进度载体必须进入启动向量

R4 将下列来源加入 R3 启动相关载体集合：

```text
Bootstrap Commit Evidence Seal State Resolution Ledger
Bootstrap Closure Progress Resolution Ledger
```

适用启动边界向量必须分别绑定它们的来源边界、摘要、完整性记录、所需状态或进度记录及认识时间。

一个来源的完整性不得证明另一个来源完整。终局记录不证明封印状态完整；进度记录也不证明封印事实、证据集合或终局不存在。

### IR-R4-21 新增链路必须保持无环

```text
Evidence Resolution Ledger
+ Boundary Seal Ledger
  -> Seal State Input Vector
  -> Seal State Resolution Ledger
  -> Closure Progress Resolution Ledger or Terminal Closure Ledger
  -> Bootstrap Mode projection
```

禁止：

```text
Seal State Input Vector -/-> Seal State Resolution Ledger
Seal State Resolution Key -/-> current state record
Progress Key -/-> Progress Ledger Boundary
Terminal Closure Key -/-> state digest, progress record or observation boundary
Mode Projection -/-> create any source record
```

## 七、R4 非法状态增量

### IR-R4-22 以下状态全部非法或失败关闭

```text
INDETERMINATE or CONFLICTED stored as raw seal fact
Raw seal fact directly creates closure terminal
Seal-state resolution consumes its own ledger boundary
NOT_SEALED inferred from missing or incomplete source
INDETERMINATE progress occupies terminal single-assignment key
Registered Seal State CONFLICTED has no terminal candidate path
Registered Seal State INDETERMINATE has no registered progress path
Old progress overrides a later terminal
Progress record opens NATIVE
Terminal closure created without exact seal-state resolution
Missing seal-state resolution freely becomes COMMIT_UNRESOLVED
```

## 八、阻断闭合映射

### IR-R4-23 R3-B1 闭合映射

| 审查要求 | R4 规则 | 闭合结果 |
|---|---|---|
| 封印事实与封印状态分离 | IR-R4-04 至 IR-R4-12 | 原始封印只表达完整正向事实，四值状态独立登记 |
| 所有状态进入关闭因果链 | IR-R4-16 至 IR-R4-19 | 完整／冲突进入终局，未知／未封印进入已登记进度 |
| 未决状态不锁死后续终局 | IR-R4-03、IR-R4-13 至 IR-R4-15 | 进度和终局分键、分载体 |
| 新载体进入边界且无环 | IR-R4-20 至 IR-R4-21 | 状态与进度来源独立完整并单向流动 |

```text
R3-B1 Repair Coverage: COMPLETE_AS_CANDIDATE
Scope Expansion: NOT_OBSERVED
Independent Review Still Required: YES
```

## 九、R4 自检

### IR-R4-24 自检结果

```text
Raw Seal / Seal State Separation: PASS
Seal State Four-value Registration: PASS
CONFLICTED Closure Branch Reachable: PASS
INDETERMINATE Progress Branch Reachable: PASS
Pending Progress / Terminal Separation: PASS
Terminal Single-assignment Preserved: PASS
Seal-state Self-reference: ABSENT
Progress / Terminal Key Collision: ABSENT
New Carrier Boundary Integration: PASS
R3 Historical Text Modified: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 十、当前决定

### IR-R4-25 R4 仍需独立复审

```text
CR-0004-R4 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R3-B1 only
Internal Self-check: PASS
Independent Review: REQUIRED
Consolidation: BLOCKED
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 R4，验证四值封印状态是否全部可登记、未决进度是否不会占用终局单赋值键，以及状态／进度新增载体是否保持无环。复审通过前不得合并或声称 `WS-01` 已完成。
