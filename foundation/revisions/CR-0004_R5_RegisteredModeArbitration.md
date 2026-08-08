# 制度注册表已登记启动模式仲裁有界修订 R5

## 修订信息

```text
Proposal ID: CR-0004-R5
Title: Registered Bootstrap Mode Arbitration R5
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0004-R4
Repair Basis: CR-0004-R4-LOCAL-REVIEW
Repair Scope: R4-B1 only
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

> 本文件只修复 `CR-0004-R4-LOCAL-REVIEW` 的一个模式仲裁阻断。它不是制度冻结，不创建任何实际载体、注册表、账本、冻结标识、模式解析或运行时权威，也不修改 R4 和既有历史记录。

## 一、修订解释边界

### IR-R5-01 R5 只处理当前模式仲裁

```text
R4-B1 Registered Mode Arbitration and Post-terminal Conflict Projection
```

R4 已通过的原始封印、四值封印状态、进度／终局分载体和终局单赋值继续成立。

### IR-R5-02 R5 覆盖自由模式投影

R5 在本范围内细化或覆盖：

```text
IR-R4-19 direct Bootstrap Mode projection
IR-R4-20 bootstrap source-vector additions
IR-R3-33 direct terminal-to-mode projection
IR-R3-34 sole mode source interpretation
IR-R3-35 bootstrap reference source vector
```

终局、进度和封印状态从“直接模式来源”降为模式仲裁输入。只有 R5 已登记模式解析可以投影当前 `Bootstrap Mode`。

### IR-R5-03 R5 不重写终局历史

R5 不修改、撤销或覆盖既有终局记录。迟到冲突只在新的认识边界上形成新的模式解析；更早 `HISTORICAL_AS_KNOWN` 视图继续保留当时已知模式。

## 二、终局存在解析

### IR-R5-04 终局存在性必须独立登记

新增逻辑载体：

```text
Bootstrap Terminal Presence Resolution Ledger
```

新增：

```text
Bootstrap Terminal Presence Resolution Execution Authority Type
Bootstrap Terminal Presence Resolution Registration Authority Type
```

存在解析执行者只能读取终局账本、终局登记冲突子域和边界完整性，生成候选。存在解析登记者只能登记内容相同且合格的候选。

二者均不得登记终局、进度、封印状态、模式解析或修改任何输入边界。

### IR-R5-05 终局存在输入必须形成无环向量

```text
Bootstrap Terminal Presence Input Vector =
  Bootstrap Commit Resolution Conflict Set Key
+ Terminal Closure Ledger ID and Domain
+ Terminal Closure Ledger Boundary ID and Digest
+ Registered Terminal Ledger Boundary Completeness Record ID and Digest
+ Terminal Registration Conflict Subdomain Boundary ID and Digest
+ Registered Conflict-subdomain Boundary Completeness Record ID and Digest
+ Valid At
+ Known At
+ View Mode
+ Presence Input Rule Version
+ Vector Digest
```

向量明确禁止包含：

```text
Bootstrap Terminal Presence Resolution Ledger
current presence candidate or registered presence record
Bootstrap Closure Mode Resolution Ledger
current mode candidate or registered mode record
```

### IR-R5-06 终局存在解析必须拥有稳定键

```text
Bootstrap Terminal Presence Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Terminal Presence Input Vector Digest
+ Terminal Presence Rule Version
```

边界、认识时间、视图或规则变化形成新的历史解析身份。不得覆盖旧存在解析，也不得用“最新记录”替代精确边界。

### IR-R5-07 终局存在必须形成候选—登记链

```text
Bootstrap Terminal Presence Input Vector
  -> Candidate Bootstrap Terminal Presence Resolution Record
  -> Bootstrap Terminal Presence Resolution Registration Attempt
  -> Registered Bootstrap Terminal Presence Resolution Record
```

候选和已登记记录至少共同绑定：

```text
Presence Resolution Record ID
Presence Resolution Key
Conflict Set Key
Input Vector ID and Digest
Matched Terminal Record ID and Digest when applicable
Terminal Registration Conflict Record IDs and Digests
Terminal Ledger Boundary and Completeness References
Presence Result
Qualified Terminal Absence Proof Reference when applicable
Resolution Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

```text
Candidate Terminal Presence Resolution Payload Digest
= Registered Terminal Presence Resolution Payload Digest
```

### IR-R5-08 终局存在使用完整四值

```text
PRESENT
ABSENT
INDETERMINATE
CONFLICTED
```

确定规则：

```text
exactly one registered terminal closure record for the conflict set
+ terminal ledger boundary COMPLETE
+ terminal conflict-subdomain boundary COMPLETE
+ no terminal registration conflict evidence
-> PRESENT

qualified applicable complete proof of no registered terminal closure for the exact conflict set
+ terminal ledger boundary COMPLETE
+ terminal conflict-subdomain boundary COMPLETE
+ no terminal registration conflict evidence
-> ABSENT

terminal ledger boundary completeness = CONFLICTED
or terminal registration conflict evidence exists
or multiple incompatible physical terminal records
or incompatible registered presence resolutions for the same key
-> CONFLICTED

missing required source
or any required boundary not COMPLETE
or absence proof qualification unavailable
or timeout, unavailable carrier or read failure
-> INDETERMINATE
```

`ABSENT` 不能由空查询、未找到记录或超时推断。

### IR-R5-09 存在解析账本必须保持历史

同一存在解析键同载荷幂等；同键不同载荷必须拒绝第二登记、追加存在解析登记冲突证据，并使存在解析账本完整性为 `CONFLICTED`。

较早 `ABSENT` 不阻止较晚边界形成 `PRESENT`；较早 `PRESENT` 也不阻止较晚边界因终局登记冲突形成 `CONFLICTED`。它们通过不同输入向量摘要保留为不同历史认识。

### IR-R5-10 终局记录不能自行证明 PRESENT

原始终局记录、终局账本位置、进度记录或缓存均不能直接建立 `PRESENT` 或 `ABSENT`。模式仲裁只能消费精确已登记终局存在解析及其独立完整边界。

## 三、启动模式源向量

### IR-R5-11 模式仲裁必须固定全部来源

```text
Bootstrap Closure Mode Source Vector =
  Bootstrap Commit Resolution Conflict Set Key
+ Registered Seal State Resolution ID and Digest
+ Registered Terminal Presence Resolution ID and Digest
+ Registered Terminal Closure Record ID and Digest or NOT_APPLICABLE
+ Registered Closure Progress Resolution ID and Digest or NOT_APPLICABLE
+ Seal State Resolution Ledger Boundary ID and Digest
+ Terminal Presence Resolution Ledger Boundary ID and Digest
+ Terminal Closure Ledger Boundary ID and Digest
+ Closure Progress Ledger Boundary ID and Digest
+ Terminal Registration Conflict Subdomain Boundary ID and Digest
+ Independent Source Completeness Record IDs and Digests
+ Valid At
+ Known At
+ View Mode
+ Mode Arbitration Contract Version
+ Vector Digest
```

每个可选记录必须使用显式 `NOT_APPLICABLE`，不得通过字段缺失表达否定或未知。

### IR-R5-12 模式源向量必须满足组合约束

```text
Presence = PRESENT
  -> exact terminal record required
  -> progress record is historical-only or NOT_APPLICABLE

Presence = ABSENT
  -> terminal record must be NOT_APPLICABLE
  -> exact progress record required only for COMMIT_UNRESOLVED candidate

Presence = CONFLICTED
  -> terminal and progress records cannot override conflict

Presence = INDETERMINATE
  -> no deterministic mode candidate permitted
```

终局记录、进度记录、封印状态和存在解析必须绑定同一冲突集合。任一集合、边界、认识时间或载荷摘要不一致都使向量为 `CONFLICTED`。

### IR-R5-13 模式源向量不得引用模式解析自身

禁止向量包含：

```text
Bootstrap Closure Mode Resolution Ledger Boundary
current Candidate Bootstrap Closure Mode Resolution
current Registered Bootstrap Closure Mode Resolution
Mode Resolution Record ID or Digest
```

模式输入只终止于封印状态、存在解析、进度、终局及其独立来源边界。

## 四、已登记模式仲裁

### IR-R5-14 模式解析必须拥有独立载体和权威

新增逻辑载体：

```text
Bootstrap Closure Mode Resolution Ledger
```

新增：

```text
Bootstrap Closure Mode Resolution Execution Authority Type
Bootstrap Closure Mode Resolution Registration Authority Type
```

执行者只能读取精确模式源向量并生成候选。登记者只能登记内容相同且合格的候选。二者均不得登记或修改封印状态、存在解析、进度、终局或任何源完整性记录。

### IR-R5-15 模式解析必须拥有稳定身份

```text
Bootstrap Closure Mode Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Closure Mode Source Vector Digest
+ Bootstrap Mode Arbitration Rule Version
```

该键表示指定认识边界上的模式结论，不是跨时间单赋值终局。边界和认识时间变化必须产生新键，保留历史视图。

### IR-R5-16 模式解析必须形成候选—登记链

```text
Bootstrap Closure Mode Source Vector
  -> Candidate Bootstrap Closure Mode Resolution Record
  -> Bootstrap Closure Mode Resolution Registration Attempt
  -> Registered Bootstrap Closure Mode Resolution Record
```

候选和已登记记录至少共同绑定：

```text
Mode Resolution Record ID
Mode Resolution Key
Conflict Set Key
Mode Source Vector ID and Digest
Seal State Resolution ID and Digest
Terminal Presence Resolution ID and Digest
Terminal Record or NOT_APPLICABLE
Progress Record or NOT_APPLICABLE
All Source Boundary and Completeness References
Mode Resolution Result
Mode Arbitration Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

```text
Candidate Bootstrap Closure Mode Resolution Payload Digest
= Registered Bootstrap Closure Mode Resolution Payload Digest
```

### IR-R5-17 模式解析使用完整五值

```text
ACTIVE_CLOSED
ABORTED_CLOSED
COMMIT_UNRESOLVED
CONFLICTED
INDETERMINATE
```

`INDETERMINATE` 是已登记的模式解析结果，但不开放任何写入，也不声称启动已经关闭。

### IR-R5-18 冲突必须拥有最高优先级

```text
Seal State Resolution = CONFLICTED
or Terminal Presence Resolution = CONFLICTED
or any required source completeness = CONFLICTED
or terminal registration conflict evidence exists
or mode source vector identities mismatch
or incompatible registered mode resolutions for the same key
-> CONFLICTED
```

该规则适用于终局登记前和终局登记后。旧 `COMMITTED` 或 `ABORTED` 终局不能覆盖当前认识边界中的冲突。

### IR-R5-19 已登记终局只有在当前来源一致时才能关闭

```text
no conflict
+ Terminal Presence Resolution = PRESENT
+ exact Terminal Closure = COMMITTED
+ Seal State Resolution = SEALED_COMPLETE
+ terminal payload binds the exact seal-state resolution lineage
+ all required source boundaries COMPLETE
-> ACTIVE_CLOSED

no conflict
+ Terminal Presence Resolution = PRESENT
+ exact Terminal Closure = ABORTED
+ Seal State Resolution = SEALED_COMPLETE
+ terminal payload binds the exact seal-state resolution lineage
+ all required source boundaries COMPLETE
-> ABORTED_CLOSED

no conflict
+ Terminal Presence Resolution = PRESENT
+ exact Terminal Closure = CONFLICTED
+ all required source boundaries COMPLETE
-> CONFLICTED
```

终局存在但当前封印状态为 `NOT_SEALED`、`INDETERMINATE` 或与终局谱系不一致时，结果为 `CONFLICTED`，不得选择旧关闭状态。

### IR-R5-20 已登记未决必须依赖合格 ABSENT

```text
no conflict
+ Terminal Presence Resolution = ABSENT
+ exact Registered Closure Progress = INDETERMINATE
+ Seal State Resolution = NOT_SEALED or INDETERMINATE
+ all required source boundaries COMPLETE
-> COMMIT_UNRESOLVED
```

没有已登记 `ABSENT` 存在解析时，进度记录不能产生 `COMMIT_UNRESOLVED`。

### IR-R5-21 未知来源必须保持 INDETERMINATE

```text
Terminal Presence Resolution = INDETERMINATE
or required source missing
or required source boundary INCOMPLETE or INDETERMINATE
or applicable mode source record unavailable
or read failure
-> INDETERMINATE
```

若终局存在解析为 `ABSENT`，但没有精确合格进度；或封印状态为 `SEALED_COMPLETE`、终局尚未登记，则结果也为 `INDETERMINATE`，不能自由推断成功、中止或未决。

## 五、当前模式唯一投影

### IR-R5-22 只有已登记模式解析可以产生 Bootstrap Mode

R5 覆盖 R3/R4 的直接模式投影：

```text
Registered Bootstrap Closure Mode Resolution
+ Bootstrap Closure Mode Resolution Ledger Boundary COMPLETE
+ exact Mode Source Vector
+ all referenced source boundaries COMPLETE
-> authoritative Bootstrap Mode at Valid At / Known At / View Mode
```

封印状态、终局存在解析、进度、终局、终局账本完整性或自由计算均不能独立产生 `Bootstrap Mode`。

### IR-R5-23 ACTIVE_CLOSED 是 NATIVE 的唯一入口

```text
Registered Mode Resolution = ACTIVE_CLOSED
+ exact mode-resolution ledger boundary COMPLETE
+ exact current Institution Resolution Boundary Vector
-> NATIVE registration admission eligible
```

其他四种结果全部失败关闭。候选模式解析、旧认识边界上的 `ACTIVE_CLOSED` 或模式解析账本边界非 `COMPLETE` 均不得开放 `NATIVE`。

### IR-R5-24 迟到冲突必须形成新的已登记当前模式

```text
Historical Known At T1:
  terminal presence PRESENT
  terminal COMMITTED
  no conflict
  -> Registered Mode Resolution ACTIVE_CLOSED

Current Known At T2:
  late evidence conflict registered
  seal state CONFLICTED
  terminal presence CONFLICTED or terminal carrier conflict
  -> Registered Mode Resolution CONFLICTED
```

T2 结果不删除或改写 T1；`CURRENT_RESTATED` 使用 T2，`HISTORICAL_AS_KNOWN` 在 `Known At = T1` 继续使用 T1。

## 六、载体边界与终止条件

### IR-R5-25 新增载体必须进入启动引用边界

R5 将以下来源加入适用启动边界向量：

```text
Bootstrap Terminal Presence Resolution Ledger
Bootstrap Closure Mode Resolution Ledger
```

每个来源必须拥有独立 `Registered Source Boundary Completeness Record`。一个来源的完整性不得证明另一个来源或任何上游载体完整。

启动识别冻结引用必须绑定精确已登记模式解析、模式解析账本完整性、模式源向量及其全部上游来源边界。

### IR-R5-26 模式解析图必须单向终止

```text
Terminal Closure Ledger + Terminal Conflict Subdomain
  -> Terminal Presence Input Vector
  -> Terminal Presence Resolution Ledger

Seal State + Presence + Progress + Terminal + Source Boundaries
  -> Mode Source Vector
  -> Mode Resolution Ledger
  -> Bootstrap Mode
  -> NATIVE admission or failure-closed result
```

禁止：

```text
Presence Input Vector -/-> Presence Resolution Ledger
Mode Source Vector -/-> Mode Resolution Ledger
Mode Resolution Key -/-> current mode record or mode-ledger boundary
Bootstrap Mode -/-> create or modify any source record
NATIVE admission -/-> retroactively validate mode sources
```

模式解析账本是本模型的最后权威投影载体。其载体完整性失败只产生外层安全失败，不由自由计算改写为另一 `Bootstrap Mode`，也不会开放 `NATIVE`。

## 七、R5 非法状态增量

### IR-R5-27 以下状态非法或失败关闭

```text
Terminal ABSENT inferred from no query result
Progress directly creates COMMIT_UNRESOLVED
Terminal directly creates ACTIVE_CLOSED or ABORTED_CLOSED
Old terminal overrides current seal-state conflict
Terminal registration conflict falls back to BOOTSTRAP_CLOSURE_STATE_PENDING
Mode source vector omits terminal conflict evidence
Mode source vector contains mode-resolution ledger boundary
Mode resolution consumes source from another conflict set
Candidate mode resolution opens NATIVE
Historical ACTIVE_CLOSED used as CURRENT_RESTATED after current conflict
Mode-resolution ledger incompleteness downgraded to a positive mode
```

## 八、阻断闭合映射

### IR-R5-28 R4-B1 闭合映射

| 审查要求 | R5 规则 | 闭合结果 |
|---|---|---|
| 合格终局存在／不存在解析 | IR-R5-04 至 IR-R5-10 | 四值存在解析独立登记，`ABSENT` 需要合格完整证明 |
| 稳定模式来源 | IR-R5-11 至 IR-R5-13 | 状态、进度、终局、冲突与完整性组成无环向量 |
| 已登记当前模式仲裁 | IR-R5-14 至 IR-R5-23 | 五值模式独立登记，只有模式解析可以投影当前模式 |
| 终局后冲突压倒旧终局 | IR-R5-18、IR-R5-24 | 新认识边界登记 `CONFLICTED`，历史旧状态不被改写 |
| 新载体边界与终止 | IR-R5-25 至 IR-R5-26 | 存在和模式解析载体独立完整，模式图单向终止 |

```text
R4-B1 Repair Coverage: COMPLETE_AS_CANDIDATE
Scope Expansion: NOT_OBSERVED
Independent Review Still Required: YES
```

## 九、R5 自检

### IR-R5-29 自检结果

```text
Qualified Terminal ABSENT: PASS
Terminal Presence Four-value Registration: PASS
Mode Source Vector Stable Identity: PASS
Registered Five-value Mode Resolution: PASS
Post-terminal Conflict Dominance: PASS
Historical / Current View Separation: PASS
Direct Terminal-to-mode Projection: REMOVED
Presence Self-reference: ABSENT
Mode Self-reference: ABSENT
New Carrier Boundary Integration: PASS
R4 Historical Text Modified: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 十、当前决定

### IR-R5-30 R5 仍需独立复审

```text
CR-0004-R5 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R4-B1 only
Internal Self-check: PASS
Independent Review: REQUIRED
Consolidation: BLOCKED
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须独立复审 R5，验证终局 `ABSENT` 是否只来自合格否定证明、终局后冲突是否稳定压倒旧终局，以及模式解析是否真正成为唯一当前模式来源。复审通过前不得合并或声称 `WS-01` 已完成。
