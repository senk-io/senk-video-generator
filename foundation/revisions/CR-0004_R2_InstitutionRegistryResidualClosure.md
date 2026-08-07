# 制度注册表残余阻断有界修订 R2

## 修订信息

```text
Proposal ID: CR-0004-R2
Title: Institution Registry Residual Model Closure R2
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0004-R1
Repair Basis: CR-0004-R1-LOCAL-REVIEW
Repair Scope: R1-B1 + R1-B2 + R1-B3 only
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

> 本文件只修复 `CR-0004-R1-LOCAL-REVIEW` 的三个残余阻断。它不是制度冻结，不创建冻结标识、注册表、账本、提交解析或运行时权威，也不修改 `CR-0004`、`CR-0004-R1` 或既有审查记录的历史正文。

## 一、修订解释边界

### IR-R2-01 R2 只覆盖三个残余阻断

```text
R1-B1 Freeze ID Allocation Resolution Record and Stable Identity
R1-B2 Lifecycle Competing-decision Conflict Domain
R1-B3 Bootstrap Control Identity and Sole Closure Source
```

R1 已通过的受保护登记、注册表外提交、外部锚、内部启动提交和三模式冻结引用解析继续作为合并来源。R2 不重新打开 `CR-0004-R1-LOCAL-REVIEW` 已判定通过的 B4。

### IR-R2-02 后续合并必须使用显式覆盖关系

R2 与基础稿或 R1 在本修订范围内冲突时，以 R2 作为后续合并候选语义。该优先关系只约束未来合并，不修改历史文件，也不使 R2 自身取得规范权威。

本 R2 明确细化或覆盖：

```text
IR-R1-06 allocation result semantics
IR-R1-09 allocation consumption requirement
IR-R1-19 lifecycle stable-key interpretation
IR-R1-20 lifecycle applicability input
IR-R1-34 bootstrap manifest identity
IR-R1-38 bootstrap window and premature closure semantics
IR-R1-39 bootstrap commit resolution identity
IR-R1-40 bootstrap commit truth table
IR-R1-41 bootstrap mode projection
IR-C-50 Bootstrap Closed Record write semantics
IR-C-54 Bootstrap Closed Record closure semantics
```

未列出的规则仅在与上述覆盖无冲突时继续成立。

### IR-R2-03 R2 不扩张 WS-01

R2 不定义通用决策、通用证明资格、业务资格、通用生命周期权威、业务投影或执行载体。新增对象和权威类型只服务于制度注册表、冻结标识解析、制度生命周期效果解析和一次性启动控制。

## 二、R1-B1：冻结标识分配解析身份

### IR-R2-04 分配事实与分配解析必须分离

```text
Freeze ID Allocation Record
  = registered positive allocation fact

Registered Freeze ID Allocation Resolution Record
  = authoritative result for one attempt and one observed allocation boundary
```

存在分配记录不自动产生 `ALLOCATED`；未找到分配记录不产生 `NOT_ALLOCATED`。任何自由计算、缓存、文件路径或执行者声明都不是已登记分配解析。

### IR-R2-05 分配解析必须拥有独立权威

新增：

```text
Freeze ID Allocation Resolution Execution Authority Type
Freeze ID Allocation Resolution Registration Authority Type
```

解析执行者只能读取分配尝试、分配账本、命名空间边界完整性记录和合格否定证明，并生成候选解析。解析登记者只能登记内容相同且合格的候选。

```text
Allocation Authority
  -/-> resolve allocation state

Allocation Resolution Execution Authority
  -/-> register resolution

Allocation Resolution Registration Authority
  -/-> allocate Freeze ID
  -/-> alter candidate resolution
```

### IR-R2-06 分配解析必须拥有稳定键

```text
Freeze ID Allocation Resolution Key =
  Allocation Attempt ID
+ Freeze ID Allocation Key
+ Freeze ID Allocation Ledger Boundary ID and Position or Exact Record Set
+ Freeze ID Allocation Ledger Boundary Digest
+ Namespace Boundary Reference and Digest
+ Registered Namespace Boundary Completeness Record ID and Digest
+ Allocation Resolution Rule Version
```

`Freeze ID Allocation Key` 继续按 R1 定义为命名空间与候选冻结标识的组合。键中任一边界、完整性记录或规则版本变化，都必须形成新的解析身份。

### IR-R2-07 分配解析必须形成候选—登记链

```text
Freeze ID Allocation Attempt
  -> Candidate Freeze ID Allocation Resolution Record
  -> Freeze ID Allocation Resolution Registration Attempt
  -> Registered Freeze ID Allocation Resolution Record
```

候选和已登记解析至少共同绑定：

```text
Allocation Resolution Record ID
Freeze ID Allocation Resolution Key
Allocation Attempt ID and Digest
Freeze ID Allocation Key
Matched Allocation Record IDs and Digests
Qualified No-allocation Proof Reference when applicable
Allocation Ledger Boundary ID, Position and Digest
Registered Boundary Completeness Record ID and Digest
Namespace Boundary Reference and Digest
Resolution Result
Resolution Rule Version
Resolution Execution Authority Reference
Resolution Registration Authority Reference
Candidate Payload Digest
Registered Payload Digest
Resolved At
Recorded At
Evidence References
```

登记尝试必须固定候选标识、候选摘要、目标解析账本、登记权威、幂等键、尝试时间和证据。

### IR-R2-08 分配解析内容必须同一

```text
Candidate Freeze ID Allocation Resolution Payload Digest
= Registered Freeze ID Allocation Resolution Payload Digest
```

同一解析键同一载荷为幂等；同一解析键出现不同结果、不同匹配记录集或不同否定证明时，必须保留全部记录并把该键解析为 `CONFLICTED`，不得最后写入获胜。

解析登记权威不得修改边界、记录集、结果、规则版本或证据引用。

### IR-R2-09 分配解析使用完整四值真值表

值域继续为：

```text
ALLOCATED
NOT_ALLOCATED
INDETERMINATE
CONFLICTED
```

确定规则：

```text
exactly one registered content-identical allocation record
+ allocation record matches attempt, allocation key, institution version, content digest and modes
+ allocation ledger boundary COMPLETE
+ namespace boundary COMPLETE
+ no incompatible authoritative allocation in the complete boundary
-> ALLOCATED

qualified applicable complete proof of no allocation for the exact attempt and allocation key
+ allocation ledger boundary COMPLETE
+ namespace boundary COMPLETE
+ proof covers the full declared boundary
-> NOT_ALLOCATED

multiple incompatible authoritative allocation records
or same allocation key mapped to different institution version, content digest or modes
or incompatible registered resolutions for the same resolution key
-> CONFLICTED

missing required source
or boundary not COMPLETE
or proof qualification unavailable
or timeout, unavailable carrier or read failure
-> INDETERMINATE
```

缺少通用证明资格治理时不得产生 `NOT_ALLOCATED`。`INDETERMINATE` 不能降级为 `NOT_ALLOCATED`。

### IR-R2-10 冻结决定只能消费已登记 ALLOCATED 解析

R2 细化 `IR-R1-09`：

```text
Registered Freeze ID Allocation Resolution = ALLOCATED
+ exact referenced Freeze ID Allocation Record
+ resolution and record payload identity
+ allocation origin compatible with freeze basis mode
-> allocation input eligible for freeze decision
```

候选解析、自由计算的 `ALLOCATED`、旧解析边界上的结果或没有精确正向分配记录的解析均不能支持冻结决定。

`NOT_ALLOCATED`、`INDETERMINATE` 和 `CONFLICTED` 全部失败关闭。冲突冻结标识不得分配、保留、退役后复用或进入任何启动清单。

### IR-R2-11 分配解析不得创造冻结事实

已登记 `ALLOCATED` 只证明指定分配尝试在指定边界上的分配状态。它不证明：

```text
institution review approved
freeze authorized
freeze commit succeeded
registry entry exists
freeze reference is currently applicable
```

这些结论仍由各自独立权威链和 R1 三模式冻结引用解析决定。

## 三、R1-B2：生命周期竞争集合

### IR-R2-12 关系身份与竞争集合身份必须分离

R1 的 `Lifecycle Relation Key` 继续标识单个决定事实投影出的关系记录。该键中的 `Lifecycle Decision Fact ID` 用于保持谱系，但不得用于隔离语义竞争。

新增：

```text
Lifecycle Applicability Conflict Set
Lifecycle Applicability Conflict Set Key
```

竞争集合只组织已登记生命周期关系，不创建或改变任何生命周期决定事实。

### IR-R2-13 生命周期竞争集合必须拥有稳定键

```text
Lifecycle Applicability Conflict Set Key =
  Source Institution ID and Version
+ Target Institution ID and Version or NOT_APPLICABLE
+ Query Effective Scope Digest
+ Applicability Valid At Coordinate
+ Lifecycle Semantic Domain
+ Conflict Set Rule Version
```

该键不得包含：

```text
Lifecycle Decision Fact ID
Record ID
Recorded At
Insertion Order
Writer Identity
```

`Lifecycle Semantic Domain` 至少区分：

```text
SOURCE_VERSION_APPLICABILITY
SUCCESSOR_SELECTION
DEPRECATION_SIGNAL
```

键中的目标分量必须按语义域规范化：

```text
SOURCE_VERSION_APPLICABILITY -> NOT_APPLICABLE
DEPRECATION_SIGNAL -> NOT_APPLICABLE
SUCCESSOR_SELECTION -> exact successor target
```

因此 `REVOKES` 与 `SUPERSEDES` 即使原关系目标字段不同，也会在 `SOURCE_VERSION_APPLICABILITY` 域进入同一来源版本竞争集合；不同继任目标则会在来源适用性域先暴露效果竞争，并在 `SUCCESSOR_SELECTION` 域保留各精确目标。不得用目标字段把本应竞争的来源适用性效果分隔到不同集合。

同一已登记关系可以按其规范效果进入一个或多个语义域，但每个成员资格必须由版本化规则确定，不能由查询者临时选择。

### IR-R2-14 竞争集合成员资格必须确定

关系只有同时满足以下条件才能进入指定竞争集合：

```text
registered lifecycle registration resolution = REGISTERED
registered relation payload is content-identical to candidate
source institution and version match
target or NOT_APPLICABLE matches the semantic-domain membership rule
effective scope contains the query scope
Valid From <= Applicability Valid At
Valid Until is absent or Applicability Valid At < Valid Until
Recorded At <= Known At for HISTORICAL_AS_KNOWN
relation exists within the declared complete lifecycle boundary
```

候选关系、登记尝试、未登记关系、边界外记录和认识时间之后的记录不得加入集合。

### IR-R2-15 生命周期效果必须规范化

每个集合成员必须投影为一个 `Normalized Lifecycle Effect`：

```text
Relation Type
Source Applicability Effect
Successor Target or NOT_APPLICABLE
Deprecation Signal
Effective Scope Digest
Valid Interval
Decision Fact ID and Digest
Primary Decision Authority Reference
Explicitly Superseded Decision Fact IDs
Normalization Rule Version
Normalized Effect Digest
```

最低规范效果：

```text
REVOKES
  -> Source Applicability Effect: NOT_APPLICABLE

SUPERSEDES
  -> Source Applicability Effect: NOT_APPLICABLE_FOR_NEW_USE
  -> Successor Target: exact target institution version

DEPRECATES
  -> Source Applicability Effect: APPLICABLE_WITH_DEPRECATION
  -> Deprecation Signal: PRESENT
```

规范化只解释已登记决定效果，不取得生命周期决定权威。

### IR-R2-16 兼容、替代与互斥必须显式

同一竞争集合内：

```text
same normalized effect digest
-> COMPATIBLE

different records explicitly converge on the same source applicability effect and successor target
-> COMPATIBLE

later authoritative decision explicitly lists every displaced Lifecycle Decision Fact ID
+ authority scope covers the same source, target, semantic domain, effective scope and valid coordinate
+ displaced records are present in the complete boundary
-> EXPLICITLY_SUPERSEDED

different source applicability effects
or different successor targets in SUCCESSOR_SELECTION
or claimed supersession without exact prior decision references
or incomparable authority scopes
-> INCOMPATIBLE
```

时间更晚、记录位置更大、版本号更高或写入者不同都不自动建立替代。

### IR-R2-17 显式替代必须保留全部历史

要建立 `EXPLICITLY_SUPERSEDED`，后续 `Institution Lifecycle Decision Fact` 必须显式绑定：

```text
Superseded Lifecycle Decision Fact IDs and Digests
Supersession Semantic Domain
Supersession Effective Scope
Supersession Valid From
Primary Lifecycle Decision Authority Reference
Evidence References
```

该字段只是决定内容的一部分，仍须通过 R1 的决策事实和生命周期登记链成立。被替代记录不得删除、覆盖或改写；历史视图在替代决定进入认识边界前继续显示原效果。

### IR-R2-18 生命周期效果解析必须拥有独立权威

新增：

```text
Lifecycle Effect Resolution Execution Authority Type
Lifecycle Effect Resolution Registration Authority Type
```

解析执行者只能从完整竞争集合生成候选效果；解析登记者只登记内容相同且合格的候选。二者均不得创建决定事实、登记生命周期关系或修改竞争集合成员。

### IR-R2-19 生命周期效果解析必须拥有稳定键

```text
Lifecycle Effect Resolution Key =
  Lifecycle Applicability Conflict Set Key
+ Lifecycle Registry Boundary ID, Position or Exact Record Set
+ Lifecycle Registry Boundary Digest
+ Registered Lifecycle Boundary Completeness Record ID and Digest
+ Valid At
+ Known At
+ View Mode
+ Lifecycle Effect Resolution Rule Version
```

任一边界、时间坐标、视图模式或规则版本变化都形成新解析身份。

### IR-R2-20 生命周期效果必须形成候选—登记链

```text
Registered Lifecycle Relation Records
  -> Lifecycle Applicability Conflict Set
  -> Candidate Lifecycle Effect Resolution Record
  -> Lifecycle Effect Resolution Registration Attempt
  -> Registered Lifecycle Effect Resolution Record
```

候选和已登记解析至少共同绑定：

```text
Lifecycle Effect Resolution Record ID
Lifecycle Effect Resolution Key
Conflict Set Key and Membership Digest
Member Relation Record IDs and Digests
Normalized Effect Digests
Explicit Supersession References
Lifecycle Registry Boundary and Digest
Registered Boundary Completeness Record and Digest
Valid At, Known At and View Mode
Resolution Result
Resolved Lifecycle Effect or NOT_APPLICABLE
Resolution Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

### IR-R2-21 生命周期效果解析使用四值结果

```text
EFFECTIVE
NOT_EFFECTIVE
INDETERMINATE
CONFLICTED
```

确定规则：

```text
one applicable normalized effect
or multiple compatible effects that converge on one normalized effect
or one exact explicitly superseding effect after removing only its declared displaced effects
+ lifecycle boundary COMPLETE
-> EFFECTIVE

qualified applicable complete proof that the conflict set has no registered applicable relation
+ lifecycle boundary COMPLETE
-> NOT_EFFECTIVE

two or more incompatible non-displaced effects
or incompatible successor targets
or incomplete / circular / unauthorized supersession claim
or incompatible registered resolutions for the same resolution key
-> CONFLICTED

missing source
or lifecycle boundary not COMPLETE
or membership cannot be determined
or proof qualification unavailable
or timeout, unavailable carrier or read failure
-> INDETERMINATE
```

`EFFECTIVE` 必须携带唯一 `Resolved Lifecycle Effect`。`NOT_EFFECTIVE` 只表示在指定完整边界和坐标上没有生命周期效果，不表示制度从未存在或从未冻结。

### IR-R2-22 生命周期效果解析必须内容同一

```text
Candidate Lifecycle Effect Resolution Payload Digest
= Registered Lifecycle Effect Resolution Payload Digest
```

同键不同结果、不同成员集合或不同规范效果必须保留为 `CONFLICTED`。禁止最后写入获胜、按记录顺序选取、忽略不兼容成员或用缓存覆盖已登记冲突。

### IR-R2-23 冻结引用只能消费已登记生命周期效果

R2 细化 R1 的引用适用性输入：

```text
Registered Lifecycle Effect Resolution = EFFECTIVE
  -> apply exact Resolved Lifecycle Effect

Registered Lifecycle Effect Resolution = NOT_EFFECTIVE
  -> apply no lifecycle change at that coordinate

Registered Lifecycle Effect Resolution = INDETERMINATE
  -> freeze reference applicability remains INDETERMINATE

Registered Lifecycle Effect Resolution = CONFLICTED
  -> freeze reference applicability becomes CONFLICTED
```

单个关系记录、自由计算集合或候选效果解析不得直接改变冻结引用适用性。

## 四、R1-B3：启动清单稳定身份

### IR-R2-24 启动清单必须是已登记控制对象

新增对象：

```text
Candidate Bootstrap Manifest Record
Bootstrap Manifest Registration Attempt
Registered Bootstrap Manifest Record
Candidate Bootstrap Manifest Registration Resolution Record
Bootstrap Manifest Registration Resolution Registration Attempt
Registered Bootstrap Manifest Registration Resolution Record
```

新增权威：

```text
Bootstrap Manifest Construction Authority Type
Bootstrap Manifest Registration Authority Type
Bootstrap Manifest Registration Resolution Execution Authority Type
Bootstrap Manifest Registration Resolution Registration Authority Type
```

清单构造者不得登记清单；清单登记者不得改变候选清单；清单登记解析者不得构造、登记或选择清单内容。

### IR-R2-25 启动纪元和清单必须拥有稳定键

一次性初始启动使用：

```text
Bootstrap Epoch Key =
  Target Institution Registry ID
+ GENESIS
```

```text
Bootstrap Manifest Key =
  Bootstrap Epoch Key
```

键不得包含清单记录 ID、清单摘要、启动契约版本、创建时间或写入者。相同注册表的 `GENESIS` 启动纪元只能存在一个规范清单内容；改变契约版本不能产生第二清单键。

候选和已登记清单除 R1 `IR-R1-34` 字段外，还必须绑定：

```text
Bootstrap Manifest Key
Target Institution Registry ID
Bootstrap Epoch Key
Bootstrap Contract Version
Manifest Carrier ID
Manifest Boundary Reference
Construction Authority Reference
Registration Authority Reference
Candidate Payload Digest
Registered Payload Digest
```

```text
Candidate Bootstrap Manifest Record
  -> Bootstrap Manifest Registration Attempt
  -> Registered Bootstrap Manifest Record
  -> Candidate Bootstrap Manifest Registration Resolution Record
  -> Bootstrap Manifest Registration Resolution Registration Attempt
  -> Registered Bootstrap Manifest Registration Resolution Record
```

每一步必须拥有稳定身份、权威引用、载荷摘要、时间和证据。清单登记解析登记尝试必须固定候选解析 ID、候选摘要、目标解析账本、登记权威和幂等键。

### IR-R2-26 清单登记解析必须稳定且四值化

```text
Bootstrap Manifest Registration Resolution Key =
  Bootstrap Manifest Key
+ Manifest Carrier Boundary ID, Position or Exact Record Set
+ Manifest Carrier Boundary Digest
+ Registered Manifest Boundary Completeness Record ID and Digest
+ Manifest Registration Resolution Rule Version
```

值域：

```text
REGISTERED
NOT_REGISTERED
INDETERMINATE
CONFLICTED
```

规则：

```text
exactly one registered content-identical manifest
+ manifest carrier boundary COMPLETE
-> REGISTERED

qualified applicable complete proof of no registered manifest for the exact key
+ manifest carrier boundary COMPLETE
-> NOT_REGISTERED

multiple manifest contents for the same key
or different first-entry sets, window definitions, authority bundles or canonicalization contracts
or incompatible registered manifest resolutions for the same resolution key
-> CONFLICTED

missing source
or boundary not COMPLETE
or proof qualification unavailable
or read failure
-> INDETERMINATE
```

```text
Candidate Bootstrap Manifest Payload Digest
= Registered Bootstrap Manifest Payload Digest

Candidate Manifest Registration Resolution Payload Digest
= Registered Manifest Registration Resolution Payload Digest
```

只有已登记 `REGISTERED` 解析及其精确清单可以进入外部锚和内部启动提交。其他结果全部失败关闭。

## 五、R1-B3：启动窗口稳定身份

### IR-R2-27 启动窗口必须拥有稳定键

```text
Bootstrap Window Definition Key =
  Bootstrap Epoch Key
+ BOOTSTRAP_WINDOW
```

键不得包含清单记录 ID、清单摘要、窗口记录 ID、窗口摘要或契约版本；这些值只能作为载荷进入冲突检查，不能用于换键逃避唯一性。

为消除清单与窗口摘要的循环依赖，R2 将 R1 `IR-R1-34` 中的：

```text
Bootstrap Window Definition Record ID and Digest
```

细化为：

```text
Bootstrap Window Definition Core ID and Digest
```

`Candidate Bootstrap Window Definition Core` 必须在清单摘要固定前构造，只绑定窗口键、目标注册表、启动纪元、预分配内部尝试 ID、精确首批集合、允许的候选内部记录集、禁止第二首批集合规则、规则版本、权威和证据，不得绑定清单记录 ID、清单摘要、外部锚记录或最终窗口记录摘要。

清单登记成功且外部锚已登记后，窗口执行者从“已登记清单 + 清单所绑定的精确窗口核心 + 已登记外部锚”构造最终 `Candidate Bootstrap Window Definition Record`。内部启动尝试只能消费该精确候选。

`Candidate Bootstrap Window Definition Record` 和已登记记录至少共同绑定：

```text
Bootstrap Window Definition Record ID
Bootstrap Window Definition Key
Registered Bootstrap Manifest Record ID and Digest
Registered Manifest REGISTERED Resolution ID and Digest
External Anchor Commitment Key
Registered External Anchor Commitment Record ID and Digest
Registered External Anchor COMMITTED Resolution ID and Digest
Allowed Bootstrap Commit Attempt ID
Exact First-entry Membership and Digest
Allowed Candidate Internal Record IDs and Digests
Allowed Bootstrap Commit Resolution Core Key
No-second-first-entry-set Rule Version
Window Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Created At and Recorded At
Evidence References
```

R1 已定义的 `Bootstrap Window Definition Registration Authority Type` 继续适用；新增：

```text
Bootstrap Window Definition Execution Authority Type
```

执行者只能从已登记清单构造候选，登记者只能在内部保护边界中登记内容相同的候选。

### IR-R2-28 启动窗口必须唯一且内容同一

```text
Candidate Bootstrap Window Definition Payload Digest
= Registered Bootstrap Window Definition Payload Digest
```

同一窗口键同一载荷为幂等；同一窗口键不同清单、外部锚、内部尝试、首批集合、允许解析键或内部记录集为 `CONFLICTED`。

下列状态也必须进入启动提交解析的冲突分支：

```text
more than one registered window for the Bootstrap Epoch Key
window key not bound to the sole REGISTERED manifest
window core not equal to the manifest-bound core
window record not equal to the content-identical final candidate
window allows more than one internal attempt
window omits any first-entry or protected internal record
```

窗口记录只固定允许的尝试和关闭条件，不证明启动成功，也不产生任何关闭状态。

## 六、R1-B3：唯一启动关闭真源

### IR-R2-29 Bootstrap Closed Record 退出规范语义

R2 明确覆盖基础稿 `IR-C-50` 和 `IR-C-54`：

```text
Bootstrap Closed Record
  -> LEGACY_NON_NORMATIVE_BOOTSTRAP_CLOSURE_ASSERTION
```

新的启动流程不得写入该对象。若迁移或历史证据中发现该对象，它只能作为不可变历史输入保留，不能：

```text
close bootstrap window
establish ACTIVE_CLOSED
establish ABORTED_CLOSED
authorize NATIVE registration
replace Bootstrap Commit Resolution
prove first-entry-set completeness
```

它与已登记清单、窗口或提交解析不一致时，只能增加冲突证据，不能覆盖新模型的权威结果。

### IR-R2-30 启动提交解析键必须绑定唯一控制对象

为避免窗口载荷与最终解析键互相包含摘要，先定义不含最终窗口记录摘要和内部提交结果边界的核心键：

```text
Bootstrap Commit Resolution Core Key =
  Bootstrap Manifest Key
+ Registered Bootstrap Manifest Record ID and Digest
+ Registered Manifest REGISTERED Resolution ID and Digest
+ Registered External Anchor Commitment Record ID and Digest
+ Registered External Anchor COMMITTED Resolution ID and Digest
+ Bootstrap Window Definition Key
+ Allowed Bootstrap Commit Attempt ID
+ Bootstrap Resolution Rule Version
```

窗口记录只绑定该核心键。R2 再细化 `IR-R1-39` 的最终键：

```text
Bootstrap Commit Resolution Key =
  Bootstrap Commit Resolution Core Key
+ Registered Bootstrap Window Definition Record ID and Digest
+ Bootstrap Commit Attempt ID and Digest
+ Internal Registry Boundary ID and Digest
+ Internal Freeze Ledger Boundary ID and Digest
+ Internal Attribution Boundary ID and Digest
+ Bootstrap Resolution Ledger Boundary ID and Digest
```

最终键不得反向写入窗口记录、清单或外部锚。解析候选和已登记记录必须精确引用上述控制对象。任一引用变化都形成新解析身份；同一启动纪元出现多个不兼容解析键时，启动模式只能是 `CONFLICTED`。

### IR-R2-31 启动提交真值表必须同时验证唯一性

R2 在 `IR-R1-40` 的基础上增加：

```text
exactly one Bootstrap Manifest Key for the GENESIS epoch
+ registered Manifest Registration Resolution = REGISTERED
+ exact registered manifest content identity
+ registered External Anchor Resolution = COMMITTED
+ exact registered window content identity
+ exactly one allowed internal commit attempt
+ exact internal anchor
+ exact complete first registry set
+ exact complete recognition ledger set
+ exact attribution
+ all candidate and registered digests match manifest and window
+ all required boundaries COMPLETE
-> COMMITTED

qualified applicable complete proof of no internal protected write
+ exact registered manifest, external anchor and window
+ all required boundaries COMPLETE
-> ABORTED

multiple manifest contents for one manifest key
or multiple windows for one bootstrap epoch
or manifest / window / anchor / attempt mismatch
or partial protected write
or more than one first-entry set
or incompatible registered resolutions
or legacy Bootstrap Closed Record contradicts authoritative control objects
-> CONFLICTED

missing control object
or manifest resolution not terminal
or required boundary not COMPLETE
or unavailable carrier, timeout or read failure
-> INDETERMINATE
```

`ABORTED` 仍要求通用证明资格与适用性治理；缺失时只能是 `INDETERMINATE`。

### IR-R2-32 已登记提交解析是唯一规范关闭来源

```text
registered content-identical Bootstrap Commit Resolution = COMMITTED
  -> Bootstrap Mode: ACTIVE_CLOSED

registered content-identical Bootstrap Commit Resolution = ABORTED
  -> Bootstrap Mode: ABORTED_CLOSED

registered content-identical Bootstrap Commit Resolution = CONFLICTED
  -> Bootstrap Mode: CONFLICTED

registered content-identical Bootstrap Commit Resolution = INDETERMINATE
or internal attempt without a terminal registered resolution
  -> Bootstrap Mode: COMMIT_UNRESOLVED
```

只有 `ACTIVE_CLOSED` 开放正常 `NATIVE` 登记。没有已登记 `COMMITTED` 提交解析时，任何清单、外部锚、窗口、内部记录、观察结果或旧关闭断言都不能开放该路径。

### IR-R2-33 提交前启动状态不得冒充关闭

R2 细化 `IR-R1-41`：

```text
Bootstrap Mode =
  UNINITIALIZED
  | PREPARATION_UNRESOLVED
  | MANIFEST_REGISTERED
  | PREPARED
  | PREPARATION_ABORTED
  | PREPARATION_CONFLICTED
  | COMMIT_UNRESOLVED
  | ACTIVE_CLOSED
  | ABORTED_CLOSED
  | CONFLICTED
```

```text
qualified complete proof of no registered manifest
  -> UNINITIALIZED

no terminal registered Manifest Registration Resolution
or external anchor attempt without terminal registered resolution
  -> PREPARATION_UNRESOLVED

registered Manifest Resolution = REGISTERED
+ no external anchor commitment attempt
  -> MANIFEST_REGISTERED

registered External Anchor Resolution = COMMITTED
+ no internal commit attempt
  -> PREPARED

registered External Anchor Resolution = ABORTED
+ no internal commit attempt
  -> PREPARATION_ABORTED

internal commit attempt
+ no terminal registered Bootstrap Commit Resolution
  -> COMMIT_UNRESOLVED

registered Manifest Resolution = CONFLICTED
or manifest/window admission conflict before internal attempt
  -> PREPARATION_CONFLICTED
```

`PREPARATION_UNRESOLVED`、`MANIFEST_REGISTERED`、`PREPARED`、`PREPARATION_ABORTED` 和 `PREPARATION_CONFLICTED` 都不是关闭事实。`PREPARATION_ABORTED` 和 `PREPARATION_CONFLICTED` 失败关闭所有启动写入，但不能声称已经完成或终止了一个内部提交。

`UNINITIALIZED` 不能由简单缺失、空查询、超时或不完整清单载体推断。

### IR-R2-34 清单、窗口和终局解析必须互相绑定

```text
Registered Manifest
  -> exact External Anchor Commitment
  -> exact Candidate Window Definition
  -> exact Registered Window Definition
  -> exact Bootstrap Commit Attempt
  -> exact Candidate Internal Record Set
  -> exact Registered Bootstrap Commit Resolution
```

任何链路中摘要、标识、首批集合、边界、规则版本或权威包不一致时，不得择一接受、重算后覆盖或换键重试。

R1 的窗口不可重开规则继续成立。恢复只能通过新的制度修订、恢复决定和迁移证据进行，并保留原启动纪元的全部冲突和未决历史。

## 七、修订后的规范因果路径

### 冻结标识分配解析

```text
Freeze ID Allocation Attempt
  -> Freeze ID Allocation Record or qualified no-allocation proof
  -> COMPLETE allocation and namespace boundaries
  -> Candidate Allocation Resolution
  -> Registered Allocation Resolution
  -> exact ALLOCATED result
  -> eligible input to independent Freeze Decision
```

### 生命周期效果解析

```text
Authoritative Lifecycle Decision Facts
  -> Registered Lifecycle Relation Records
  -> deterministic Conflict Set membership
  -> Normalized Lifecycle Effects
  -> Candidate Lifecycle Effect Resolution
  -> Registered Lifecycle Effect Resolution
  -> Freeze Reference applicability input
```

### 一次性启动关闭

```text
Candidate Bootstrap Manifest
  -> Registered Manifest
  -> Registered REGISTERED Manifest Resolution
  -> Registered COMMITTED External Anchor Resolution
  -> exact Candidate Window
  -> one Bootstrap Commit Attempt
  -> content-identical Registered Window and protected internal records
  -> Registered Bootstrap Commit Resolution
  -> ACTIVE_CLOSED or failure-closed mode
```

不存在从 `Bootstrap Closed Record`、文件存在性、缓存、自由计算或协调者声明到关闭状态的旁路。

## 八、权威操作矩阵增量

| 操作 | 执行权威 | 登记权威 | 明确禁止 |
|---|---|---|---|
| 构建分配解析 | 分配解析执行权威 | 无 | 分配标识、登记解析 |
| 登记分配解析 | 无 | 分配解析登记权威 | 修改候选、创建分配事实 |
| 构建生命周期效果 | 生命周期效果解析执行权威 | 无 | 创建决定、登记关系 |
| 登记生命周期效果 | 无 | 生命周期效果解析登记权威 | 修改成员集合、最后写入获胜 |
| 构建启动清单 | 启动清单构造权威 | 无 | 登记清单、关闭启动 |
| 登记启动清单 | 无 | 启动清单登记权威 | 修改候选、选择另一首批集合 |
| 解析清单登记 | 清单登记解析执行权威 | 清单登记解析登记权威 | 构造清单、忽略冲突 |
| 构建启动窗口 | 启动窗口执行权威 | 无 | 登记窗口、关闭启动 |
| 登记启动窗口 | 无 | R1 启动窗口登记权威 | 修改清单或内部尝试 |
| 关闭启动 | 启动提交解析执行权威 | 启动提交解析登记权威 | 用旧关闭断言或观察结果替代解析 |

任何一行都不传播到另一行，协调权威不自动取得执行或登记权威。

## 九、R2 非法状态增量

以下状态一律非法或失败关闭：

```text
Freeze Decision consumes Allocation Record without registered ALLOCATED resolution
NOT_ALLOCATED inferred from missing allocation record
Allocation resolution omits ledger or namespace completeness record
Lifecycle relations separated only because Decision Fact IDs differ
Lifecycle conflict resolved by latest write, record order or writer identity
Lifecycle effect applied without registered effect resolution
Bootstrap manifest used without registered REGISTERED manifest resolution
Bootstrap Manifest Key includes Manifest Digest to evade uniqueness conflict
Bootstrap window has no stable key or differs from manifest-bound candidate
More than one manifest content exists for one GENESIS epoch
More than one window or internal attempt exists for one bootstrap epoch
Bootstrap Closed Record opens NATIVE registration
Bootstrap mode becomes ACTIVE_CLOSED without registered COMMITTED resolution
Legacy closure assertion overrides manifest, window or commit conflict
Preparation conflict is presented as successful bootstrap closure
```

## 十、残余阻断闭合映射

| 审查阻断 | R2 规则 | 闭合结果 |
|---|---|---|
| R1-B1 分配解析没有稳定登记身份 | IR-R2-04 至 IR-R2-11 | 分配事实与四值解析分离，解析具备稳定键、分权、候选／登记链和消费门槛 |
| R1-B2 生命周期竞争决定没有冲突域 | IR-R2-12 至 IR-R2-23 | 决定标识不再隔离竞争，成员、规范效果、显式替代和四值解析确定 |
| R1-B3 启动控制身份与关闭真源未唯一化 | IR-R2-24 至 IR-R2-34 | 清单和窗口唯一化，旧关闭记录退场，已登记提交解析成为唯一规范关闭来源 |

```text
R1-B1 Repair Coverage: COMPLETE_AS_CANDIDATE
R1-B2 Repair Coverage: COMPLETE_AS_CANDIDATE
R1-B3 Repair Coverage: COMPLETE_AS_CANDIDATE
Scope Expansion: NOT_OBSERVED
Independent Review Still Required: YES
```

## 十一、R2 自检

### 身份检查

```text
Allocation Fact / Allocation Resolution Separation: PASS
Allocation Resolution Stable Key: PASS
Lifecycle Relation / Conflict Set Separation: PASS
Lifecycle Effect Resolution Stable Key: PASS
Bootstrap Manifest Stable Key: PASS
Bootstrap Window Stable Key: PASS
Bootstrap Commit Resolution Refined Key: PASS
```

### 权威检查

```text
Allocation Resolution Execution / Registration Separation: PASS
Lifecycle Effect Execution / Registration Separation: PASS
Manifest Construction / Registration Separation: PASS
Window Execution / Registration Separation: PASS
Bootstrap Closure Authority Non-propagation: PASS
```

### 否定与未知检查

```text
Missing Allocation Record != NOT_ALLOCATED: PASS
Missing Lifecycle Relation != NOT_EFFECTIVE: PASS
Missing Manifest != UNINITIALIZED: PASS
Incomplete Boundary -> INDETERMINATE: PASS
Proof Qualification Unavailable -> no negative terminal result: PASS
```

### 启动唯一性检查

```text
Single GENESIS Manifest Content: PASS
Single Manifest-bound Window: PASS
Single Allowed Internal Attempt: PASS
Bootstrap Closed Record Normative Authority: REMOVED_AS_CANDIDATE
Registered Bootstrap Commit Resolution as Sole Closure Source: PASS
NATIVE Admission only after ACTIVE_CLOSED: PASS
```

### 历史与边界检查

```text
CR-0004 Historical Text Modified: NO
CR-0004-R1 Historical Text Modified: NO
Prior Review Text Modified: NO
Existing Conflict Records Deleted: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 十二、当前决定

```text
CR-0004-R2 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R1-B1 + R1-B2 + R1-B3 only
Internal Self-check: PASS
Independent Review: REQUIRED
Consolidation: BLOCKED
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须对本 R2 进行独立模型与启动闭环复审，验证三个残余阻断是否真正关闭，并特别检查新增解析记录是否产生新的自引用、冲突逃逸键或竞争关闭来源。复审通过前不得合并为 `CR-0004` 制度候选，也不得声称 `WS-01` 已完成。
