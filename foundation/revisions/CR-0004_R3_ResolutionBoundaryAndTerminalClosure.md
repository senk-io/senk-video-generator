# 制度注册表解析边界与终局闭合有界修订 R3

## 修订信息

```text
Proposal ID: CR-0004-R3
Title: Institution Registry Resolution Boundary and Terminal Closure R3
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0004-R2
Repair Basis: CR-0004-R2-LOCAL-REVIEW
Repair Scope: R2-B1 + R2-B2 + R2-B3 only
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

> 本文件只修复 `CR-0004-R2-LOCAL-REVIEW` 的三个阻断。它不是制度冻结，不创建冻结标识、注册表、账本、提交解析或运行时权威，也不修改基础稿、R1、R2 和既有审查记录的历史正文。

## 一、修订解释边界

### IR-R3-01 R3 只覆盖三个阻断

```text
R2-B1 New Resolution Carriers and Boundary-vector Integration
R2-B2 Cross-domain Lifecycle Applicability Composition
R2-B3 Bootstrap Resolution-set Identity and Non-self-referential Closure
```

R2 已通过的分配解析身份、生命周期域内成员与效果规则、清单唯一键、窗口核心、最终窗口、旧关闭记录退场继续成立。

### IR-R3-02 R3 使用显式后续覆盖

R3 在本修订范围内细化或覆盖：

```text
IR-R1-43 required resolution sources
IR-R1-45 institution boundary vector entries
IR-R1-48 through IR-R1-50 mode-required sources
IR-R1-52 lifecycle applicability input
IR-R2-06 allocation resolution completeness bindings
IR-R2-13 SUCCESSOR_SELECTION grouping
IR-R2-23 lifecycle result consumption
IR-R2-30 final bootstrap resolution key
IR-R2-32 sole closure projection
IR-R2-33 unresolved bootstrap state
```

该覆盖只作为后续合并候选，不赋予 R3 规范权威。

### IR-R3-03 R3 不扩张 WS-01

R3 只定义制度注册表解析载体、生命周期复合适用性和启动终局解析。它不定义通用账本框架、通用决策、通用证明资格、业务资格、业务投影或运行时实现。

## 二、R2-B1：解析载体拓扑

### IR-R3-04 新增解析必须拥有独立载体

新增逻辑载体：

```text
Freeze ID Allocation Resolution Ledger
Lifecycle Effect Resolution Ledger
Composite Lifecycle Applicability Resolution Ledger
Bootstrap Commit Evidence Resolution Ledger
Bootstrap Commit Evidence Boundary Seal Ledger
Bootstrap Closure Resolution Ledger
```

`Bootstrap Manifest Registration Resolution Record` 归入既有 `Bootstrap Resolution Ledger` 的独立子域：

```text
BOOTSTRAP_MANIFEST_REGISTRATION_RESOLUTION
```

该子域拥有独立位置范围、边界摘要和完整性记录。它不能用其他启动解析子域的完整性证明自身完整。

### IR-R3-05 每个解析载体必须有稳定身份和追加边界

每个载体至少绑定：

```text
Resolution Carrier ID and Version
Resolution Domain
Allowed Record Types
Registration Authority Type
Append-only Position Contract
Canonicalization and Digest Contract
Boundary Rule Version
Carrier Authority Reference
Effective At
Evidence References
```

解析载体只保存其声明类型的已登记解析或边界封印，不创建被解析的原始事实。一个载体的登记权威不得隐式取得另一载体或原始事实载体的登记权威。

### IR-R3-06 每个解析来源必须独立证明完整

R3 将下列来源加入 R1 `IR-R1-43` 的最低来源集合：

```text
Freeze ID Allocation Resolution Ledger
Lifecycle Effect Resolution Ledger
Composite Lifecycle Applicability Resolution Ledger
Bootstrap Manifest Registration Resolution subdomain
Bootstrap Commit Evidence Resolution Ledger
Bootstrap Commit Evidence Boundary Seal Ledger
Bootstrap Closure Resolution Ledger
```

每个来源必须提供独立 `Registered Source Boundary Completeness Record`，继续使用 R1 的：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

一个解析账本的完整性不能由原事实账本、其他解析账本、共享时间戳或“已读取最新”证明。

### IR-R3-07 分配解析必须绑定两个完整性记录

R3 细化 `IR-R2-06`：

```text
Freeze ID Allocation Resolution Key =
  Allocation Attempt ID
+ Freeze ID Allocation Key
+ Freeze ID Allocation Ledger Boundary ID and Position or Exact Record Set
+ Freeze ID Allocation Ledger Boundary Digest
+ Registered Allocation Ledger Boundary Completeness Record ID and Digest
+ Namespace Boundary Reference and Digest
+ Registered Namespace Boundary Completeness Record ID and Digest
+ Allocation Resolution Rule Version
```

候选和已登记分配解析必须分别保存两个完整性记录引用。任一缺失、来源混淆或非 `COMPLETE` 都产生 `INDETERMINATE`，不能产生 `ALLOCATED` 或 `NOT_ALLOCATED`。

### IR-R3-08 认识边界向量必须包含被消费的解析来源

R3 细化 `Institution Resolution Boundary Vector`：

```text
Institution Resolution Boundary Vector =
  ordered Original Fact Source Boundary Entries
+ ordered Resolution Source Boundary Entries
+ Vector Scope
+ Valid At
+ Known At
+ View Mode
+ Vector Rule Version
+ Vector Digest
```

每个解析来源条目必须绑定：

```text
Resolution Carrier ID and Domain
Boundary Position or Exact Record Set
Boundary Digest
Registered Source Boundary Completeness Record ID and Digest
Required Resolution Record IDs and Digests
Recorded-at Cutoff
Entry Digest
```

引用解析不能消费未进入向量的解析记录。向量摘要变化必须形成新的冻结引用解析身份。

### IR-R3-09 三模式必须消费分配解析

R3 对 R1 三模式来源作以下增量：

```text
NATIVE + NATIVE_FREEZE
  -> exact Registered ALLOCATED Freeze ID Allocation Resolution
  -> exact NATIVE_NEW Allocation Record

BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
  -> exact Registered ALLOCATED Freeze ID Allocation Resolution
  -> exact BOOTSTRAP_RESERVED_EXISTING Allocation Record

BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
  -> exact Registered ALLOCATED Freeze ID Allocation Resolution
  -> exact NATIVE_NEW Bootstrap Allocation Record
```

每个模式都必须包含分配事实账本、分配解析账本和命名空间边界的独立 `COMPLETE` 记录。模式、制度版本、内容摘要、冻结标识和分配来源必须内容同一。

### IR-R3-10 三模式必须消费复合生命周期解析

三种模式都必须引用：

```text
Exact Registered Composite Lifecycle Applicability Resolution Record
Lifecycle Domain Resolution Vector
Lifecycle Effect Resolution Ledger Boundary
Composite Lifecycle Applicability Resolution Ledger Boundary
Independent COMPLETE Records for both boundaries
```

单个生命周期关系、单一语义域结果或未登记复合结果不得直接成为冻结引用适用性输入。

## 三、R2-B2：生命周期跨目标聚合

### IR-R3-11 生命周期域成员资格必须互不重叠且覆盖完整

R3 固定最低域成员规则：

```text
SOURCE_VERSION_APPLICABILITY
  -> registered REVOKES and SUPERSEDES relations

SUCCESSOR_SELECTION
  -> registered SUPERSEDES relations

DEPRECATION_SIGNAL
  -> registered DEPRECATES relations
```

`DEPRECATES` 不进入来源不适用域；`REVOKES` 不进入继任目标域。每条关系进入哪些域由规则版本确定，查询者不得临时增删。

### IR-R3-12 继任目标必须先进入无目标父集合

R3 覆盖 R2 中 `SUCCESSOR_SELECTION` 使用精确目标分键的语义。新增：

```text
Successor Selection Conflict Set Key =
  Source Institution ID and Version
+ ALL_SUCCESSOR_TARGETS
+ Query Effective Scope Digest
+ Applicability Valid At
+ Known At
+ View Mode
+ Successor Conflict Set Rule Version
```

键不得包含继任目标、决定事实标识、关系记录标识、记录时间或写入顺序。

所有满足查询作用域和双时间边界的已登记 `SUPERSEDES` 关系，不论目标为何，都必须进入同一父集合。精确目标保留在成员载荷中用于冲突比较。

### IR-R3-13 继任目标聚合必须独立登记

新增：

```text
Successor Selection Aggregate Resolution Execution Authority Type
Successor Selection Aggregate Resolution Registration Authority Type
```

```text
Registered SUPERSEDES Relation Set
  -> Candidate Successor Selection Aggregate Resolution Record
  -> Successor Selection Aggregate Resolution Registration Attempt
  -> Registered Successor Selection Aggregate Resolution Record
```

稳定键：

```text
Successor Selection Aggregate Resolution Key =
  Successor Selection Conflict Set Key
+ Lifecycle Registry Boundary ID and Digest
+ Registered Lifecycle Boundary Completeness Record ID and Digest
+ Successor Aggregate Rule Version
```

值域：

```text
UNIQUE_SUCCESSOR
NO_SUCCESSOR
INDETERMINATE
CONFLICTED
```

### IR-R3-14 继任目标聚合真值必须确定

```text
exactly one non-displaced successor target
or multiple compatible relations converging on the same exact target
+ lifecycle boundary COMPLETE
-> UNIQUE_SUCCESSOR

qualified applicable complete proof of no registered applicable SUPERSEDES relation
+ lifecycle boundary COMPLETE
-> NO_SUCCESSOR

two or more different non-displaced successor targets
or incomplete / circular explicit displacement
or incompatible aggregate resolutions for the same key
-> CONFLICTED

missing source
or lifecycle boundary not COMPLETE
or proof qualification unavailable
or read failure
-> INDETERMINATE
```

`UNIQUE_SUCCESSOR` 必须绑定精确继任制度版本、成员集合摘要和规范效果摘要。

## 四、R2-B2：生命周期域向量与复合适用性

### IR-R3-15 生命周期域结果必须形成稳定向量

```text
Lifecycle Domain Resolution Vector =
  Source Institution ID and Version
+ Query Effective Scope Digest
+ Valid At
+ Known At
+ View Mode
+ Registered SOURCE_VERSION_APPLICABILITY Resolution ID and Digest
+ Registered SUCCESSOR_SELECTION Aggregate Resolution ID and Digest
+ Registered DEPRECATION_SIGNAL Resolution ID and Digest
+ Lifecycle Registry Boundary ID and Digest
+ Lifecycle Effect Resolution Ledger Boundary ID and Digest
+ Independent Boundary Completeness Record IDs and Digests
+ Domain Vector Rule Version
+ Vector Digest
```

三个域结果都是必需条目。没有适用关系的域必须通过已登记否定结果表达，不能通过省略条目表达。

### IR-R3-16 复合适用性解析必须独立分权

新增：

```text
Composite Lifecycle Applicability Resolution Execution Authority Type
Composite Lifecycle Applicability Resolution Registration Authority Type
```

执行者只能读取已登记域向量并生成候选；登记者只能登记内容相同且合格的候选。二者均不得创建生命周期决定、关系、域内解析或继任目标聚合。

### IR-R3-17 复合适用性必须拥有稳定身份

```text
Composite Lifecycle Applicability Resolution Key =
  Source Institution ID and Version
+ Query Effective Scope Digest
+ Valid At
+ Known At
+ View Mode
+ Lifecycle Domain Resolution Vector Digest
+ Composite Applicability Rule Version
```

```text
Lifecycle Domain Resolution Vector
  -> Candidate Composite Lifecycle Applicability Resolution Record
  -> Composite Lifecycle Applicability Resolution Registration Attempt
  -> Registered Composite Lifecycle Applicability Resolution Record
```

候选和已登记记录至少共同绑定：

```text
Composite Resolution Record ID
Composite Lifecycle Applicability Resolution Key
Lifecycle Domain Resolution Vector ID and Digest
All Domain Resolution IDs and Digests
All Source Boundary and Completeness References
Composite Result
Resolved Successor Target or NOT_APPLICABLE
Deprecation Annotation
Composite Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

### IR-R3-18 复合结果使用完整值域

```text
APPLICABLE
APPLICABLE_WITH_DEPRECATION
INAPPLICABLE_SUPERSEDED
INAPPLICABLE_REVOKED
INDETERMINATE
CONFLICTED
```

R1 的适用性四值投影为：

```text
APPLICABLE -> APPLICABLE
APPLICABLE_WITH_DEPRECATION -> APPLICABLE with deprecation annotation
INAPPLICABLE_SUPERSEDED -> INAPPLICABLE
INAPPLICABLE_REVOKED -> INAPPLICABLE
INDETERMINATE -> INDETERMINATE
CONFLICTED -> CONFLICTED
```

### IR-R3-19 跨域合成真值必须确定

优先规则：

```text
any required domain result = CONFLICTED
or successor aggregate = CONFLICTED
or incompatible registered composite results for the same key
-> CONFLICTED

no CONFLICTED
+ any required domain result = INDETERMINATE
or successor aggregate = INDETERMINATE
or any required boundary not COMPLETE
-> INDETERMINATE

SOURCE_VERSION_APPLICABILITY = EFFECTIVE / REVOKES
-> INAPPLICABLE_REVOKED

SOURCE_VERSION_APPLICABILITY = EFFECTIVE / SUPERSEDES
+ SUCCESSOR_SELECTION = UNIQUE_SUCCESSOR
+ normalized successor target matches source-domain effect
-> INAPPLICABLE_SUPERSEDED

SOURCE_VERSION_APPLICABILITY = EFFECTIVE / SUPERSEDES
+ SUCCESSOR_SELECTION != UNIQUE_SUCCESSOR
-> CONFLICTED

SOURCE_VERSION_APPLICABILITY = EFFECTIVE / REVOKES
+ SUCCESSOR_SELECTION = UNIQUE_SUCCESSOR
-> CONFLICTED

SOURCE_VERSION_APPLICABILITY = NOT_EFFECTIVE
+ SUCCESSOR_SELECTION = UNIQUE_SUCCESSOR
-> CONFLICTED

SOURCE_VERSION_APPLICABILITY = NOT_EFFECTIVE
+ DEPRECATION_SIGNAL = EFFECTIVE
+ SUCCESSOR_SELECTION = NO_SUCCESSOR
-> APPLICABLE_WITH_DEPRECATION

SOURCE_VERSION_APPLICABILITY = NOT_EFFECTIVE
+ DEPRECATION_SIGNAL = NOT_EFFECTIVE
+ SUCCESSOR_SELECTION = NO_SUCCESSOR
-> APPLICABLE

otherwise
-> INDETERMINATE
```

撤销或替代使来源版本不适用时，弃用结果仍可作为注释保存，但不得把不适用版本重新变为适用。

### IR-R3-20 只有复合结果可以改变冻结引用适用性

```text
Registered Composite Lifecycle Applicability Resolution
+ exact Lifecycle Domain Resolution Vector
+ Composite Resolution Ledger Boundary COMPLETE
+ all referenced source boundaries COMPLETE
-> eligible lifecycle applicability input
```

单域 `EFFECTIVE`、继任目标聚合、自由计算、缓存或未登记复合结果均不得改变冻结引用适用性。

`Composite Lifecycle Applicability Resolution Ledger` 对复合解析键使用受保护单赋值登记：同键同载荷幂等；同键不同载荷必须拒绝第二次登记、追加登记冲突证据，并使复合解析账本完整性变为 `CONFLICTED`。不得最后写入获胜，也不得继续消费原结果形成确定适用性。

## 五、R2-B3：启动解析载体分层

### IR-R3-21 启动证据解析与终局解析必须分离

R3 将 R2 的 `Bootstrap Commit Resolution Record` 细化为：

```text
Bootstrap Commit Evidence Resolution Record
```

它只解析一个控制链和一个内部输入边界，不再直接产生启动模式。

新增最终对象：

```text
Bootstrap Commit Evidence Boundary Seal Record
Bootstrap Closure Resolution Record
```

逻辑载体分离：

```text
Bootstrap Commit Evidence Resolution Ledger
Bootstrap Commit Evidence Boundary Seal Ledger
Bootstrap Closure Resolution Ledger
```

三个载体的登记权威、位置范围和完整性记录互不传播。

### IR-R3-22 启动证据解析只能引用外部输入边界

新增：

```text
Bootstrap Commit Input Boundary Vector =
  Registered Manifest Boundary Entry
+ Registered Manifest Resolution Boundary Entry
+ External Anchor Boundary Entry
+ Window Definition Boundary Entry
+ Internal Registry Boundary Entry
+ Internal Freeze Ledger Boundary Entry
+ Internal Attribution Boundary Entry
+ Valid At and Known At
+ Input Boundary Rule Version
+ Vector Digest
```

每个条目必须绑定独立 `COMPLETE` 记录。

该向量明确禁止包含：

```text
Bootstrap Commit Evidence Resolution Ledger
Bootstrap Commit Evidence Boundary Seal Ledger
Bootstrap Closure Resolution Ledger
current candidate evidence resolution record
current candidate boundary seal
current candidate closure resolution
```

### IR-R3-23 证据解析键必须无自引用

R3 覆盖 `IR-R2-30` 的最终键：

```text
Bootstrap Commit Evidence Resolution Key =
  Bootstrap Commit Resolution Core Key
+ Registered Bootstrap Window Definition Record ID and Digest
+ Bootstrap Commit Attempt ID and Digest
+ Bootstrap Commit Input Boundary Vector Digest
+ Bootstrap Evidence Resolution Rule Version
```

键中不得包含证据解析账本、封印账本或终局账本的边界、位置或摘要。

候选和已登记证据解析继续使用 R1/R2 的内容同一和四值：

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

但这些值只是终局解析输入，不能直接开放 `NATIVE` 或产生任何关闭状态。

## 六、R2-B3：跨键证据集合与边界封印

### IR-R3-24 所有边界变体必须进入同一冲突集合

```text
Bootstrap Commit Resolution Conflict Set Key =
  Bootstrap Epoch Key
+ Bootstrap Manifest Key
+ Bootstrap Window Definition Key
+ Allowed Bootstrap Commit Attempt ID
```

键不得包含：

```text
Evidence Resolution Record ID or Digest
Evidence Resolution Result
Input Boundary Vector Digest
Evidence Resolution Rule Version
Ledger Position
Observed At
```

所有匹配启动纪元、清单键、窗口键和允许尝试 ID 的已登记证据解析，不论输入边界或规则版本为何，都必须进入同一集合。

冲突集合使用窗口记录中的 `Allowed Bootstrap Commit Attempt ID`，不得使用证据解析所声称的实际尝试 ID 换键。任何同纪元、同清单、同窗口但声称另一实际尝试的证据解析，仍加入原授权尝试的集合，并作为不兼容成员处理。

### IR-R3-25 证据集合必须先封印再形成终局

新增权威：

```text
Bootstrap Commit Evidence Boundary Seal Execution Authority Type
Bootstrap Commit Evidence Boundary Seal Registration Authority Type
```

```text
Bootstrap Commit Resolution Conflict Set
  -> Candidate Bootstrap Commit Evidence Boundary Seal Record
  -> Bootstrap Commit Evidence Boundary Seal Registration Attempt
  -> Registered Bootstrap Commit Evidence Boundary Seal Record
```

稳定键：

```text
Bootstrap Commit Evidence Boundary Seal Key =
  Bootstrap Commit Resolution Conflict Set Key
+ COMMIT_EVIDENCE_SET
```

键不得包含封印记录 ID、封印摘要、证据集合摘要或封印时间。

### IR-R3-26 封印载荷必须覆盖精确证据集合

封印记录至少绑定：

```text
Boundary Seal Record ID
Boundary Seal Key
Conflict Set Key
Evidence Resolution Ledger ID and Domain
First and Last Covered Positions or Exact Record Set
Covered Evidence Resolution IDs and Digests
Covered Set Digest
Registered Evidence Ledger Boundary Completeness Record ID and Digest
Late-write Prohibition Rule Version
Seal Result
Execution and Registration Authority References
Candidate and Registered Payload Digests
Sealed At and Recorded At
Evidence References
```

值域：

```text
SEALED_COMPLETE
INDETERMINATE
CONFLICTED
```

```text
exact conflict-set membership
+ evidence ledger boundary COMPLETE
+ no unresolved membership ambiguity
-> SEALED_COMPLETE

incompatible seal candidates
or evidence record outside declared membership rules
or attempted late evidence registration after seal
-> CONFLICTED

missing source
or evidence ledger boundary not COMPLETE
or read failure
-> INDETERMINATE
```

封印记录存储在独立封印账本，不属于其覆盖的证据解析集合，因此不形成摘要自引用。

### IR-R3-27 完整封印后禁止新增集合成员

`SEALED_COMPLETE` 登记后，证据解析登记权威必须拒绝同一冲突集合的新成员。

被拒绝尝试、越界写入或发现的晚到成员必须形成追加 `Bootstrap Commit Evidence Late Registration Conflict Record`，登记在封印账本的冲突子域，并使封印账本的来源边界完整性变为 `CONFLICTED`。原 `SEALED_COMPLETE` 记录保持不可变，不得被改写成另一结果。

封印账本完整性为 `CONFLICTED` 时，任何终局候选都只能是 `CONFLICTED`；不得扩展原封印、重新封印或静默忽略。

恢复只能通过新的制度修订和迁移决定进行，原冲突集合、封印和迟到证据必须永久保留。

## 七、R2-B3：唯一已登记启动终局

### IR-R3-28 启动终局必须独立分权

新增：

```text
Bootstrap Closure Resolution Execution Authority Type
Bootstrap Closure Resolution Registration Authority Type
```

执行者只能消费精确已登记封印及其覆盖集合，生成候选终局。登记者只能登记内容相同且合格的候选。二者均不得登记清单、外部锚、窗口、内部记录、证据解析或边界封印。

### IR-R3-29 启动终局使用不逃逸的稳定键

```text
Bootstrap Closure Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
```

键不得包含终局结果、终局记录 ID、终局摘要、封印摘要、输入边界、规则版本、时间或账本位置。

规则版本和封印只进入载荷；因此不同规则或观察边界无法通过换键产生多个独立终局。

### IR-R3-30 启动终局必须形成候选—登记链

```text
Registered SEALED_COMPLETE Evidence Boundary Seal
  -> Candidate Bootstrap Closure Resolution Record
  -> Bootstrap Closure Resolution Registration Attempt
  -> Registered Bootstrap Closure Resolution Record
```

候选和已登记记录至少共同绑定：

```text
Bootstrap Closure Resolution Record ID
Bootstrap Closure Resolution Key
Conflict Set Key
Registered Boundary Seal Record ID and Digest
Covered Evidence Resolution IDs and Digests
Covered Set Digest
Normalized Manifest, Window and Attempt Identity
Closure Result
Closure Rule Version
Execution and Registration Authority References
Candidate and Registered Payload Digests
Resolved At and Recorded At
Evidence References
```

```text
Candidate Bootstrap Closure Resolution Payload Digest
= Registered Bootstrap Closure Resolution Payload Digest
```

### IR-R3-31 启动终局真值必须确定

```text
registered seal = SEALED_COMPLETE
+ exact covered set
+ one normalized manifest / window / attempt control chain
+ every applicable evidence resolution converges on COMMITTED
+ all referenced input boundaries COMPLETE
+ seal ledger boundary COMPLETE
-> COMMITTED

registered seal = SEALED_COMPLETE
+ exact covered set
+ every applicable evidence resolution converges on ABORTED
+ qualified applicable complete proof of no protected write
+ seal ledger boundary COMPLETE
-> ABORTED

registered seal = CONFLICTED
or seal ledger boundary completeness = CONFLICTED
or different evidence results in the sealed set
or different normalized control chains
or more than one manifest, window or allowed attempt
or any evidence result = CONFLICTED
or late evidence registration after seal
or legacy closure assertion contradicts the control chain
-> CONFLICTED

seal missing or INDETERMINATE
or covered set unavailable
or any evidence result = INDETERMINATE
or any required source boundary not COMPLETE
-> INDETERMINATE
```

值域：

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

### IR-R3-32 终局账本必须单键单赋值

`Bootstrap Closure Resolution Ledger` 对 `Bootstrap Closure Resolution Key` 使用受保护单赋值登记：

```text
no registered payload + qualified candidate -> register once
same key + same payload -> idempotent reference to original record
same key + different payload -> reject registration and record conflict evidence
```

不同载荷不得成为第二个已登记终局。冲突登记尝试必须使终局账本完整性记录成为 `CONFLICTED`，从而禁止消费既有终局；它不能覆盖原记录，也不能通过另一个键重试。

终局账本完整性为 `CONFLICTED` 时只是载体安全失败，不声称任何提交已经完成或关闭。

### IR-R3-33 只有已登记终局可以投影启动模式

```text
Registered Bootstrap Closure Resolution = COMMITTED
+ Bootstrap Closure Resolution Ledger Boundary COMPLETE
-> ACTIVE_CLOSED

Registered Bootstrap Closure Resolution = ABORTED
+ Bootstrap Closure Resolution Ledger Boundary COMPLETE
-> ABORTED_CLOSED

Registered Bootstrap Closure Resolution = CONFLICTED
+ Bootstrap Closure Resolution Ledger Boundary COMPLETE
-> CONFLICTED

Registered Bootstrap Closure Resolution = INDETERMINATE
+ Bootstrap Closure Resolution Ledger Boundary COMPLETE
-> COMMIT_UNRESOLVED
```

内部尝试存在但尚无已登记终局时，只能进入非规范安全状态：

```text
BOOTSTRAP_CLOSURE_RESOLUTION_PENDING
```

该状态失败关闭所有写入，但不是 `Bootstrap Mode` 终局，也不能开放 `NATIVE`。

### IR-R3-34 自由观察不能改变启动模式

R3 覆盖 R2 中“观察到多个不兼容解析键直接把模式设为 `CONFLICTED`”的语义。

多个证据解析键只能：

```text
join one Bootstrap Commit Resolution Conflict Set
-> enter one registered boundary seal
-> enter one registered Bootstrap Closure Resolution
```

缓存、自由计算、文件存在性、旧 `Bootstrap Closed Record`、证据解析记录或封印记录都不能独立投影启动模式。

## 八、启动与引用边界集成

### IR-R3-35 启动相关载体必须进入适用边界向量

启动识别模式必须在其边界向量中包含：

```text
Bootstrap Manifest Carrier
Bootstrap Manifest Registration Resolution subdomain
External Anchor Carrier
Bootstrap Window Definition Carrier
Bootstrap Commit Evidence Resolution Ledger
Bootstrap Commit Evidence Boundary Seal Ledger
Bootstrap Closure Resolution Ledger
Institution Registry
Freeze Ledger
Commit Attribution Carrier
```

每个条目必须拥有独立 `COMPLETE` 记录。只有精确已登记 `COMMITTED` 启动终局及完整终局账本边界可以支持 `ACTIVE_CLOSED` 和启动识别冻结引用。

### IR-R3-36 终局载体不证明输入载体完整

```text
Bootstrap Closure Resolution Ledger COMPLETE
  -/-> Bootstrap Commit Evidence Resolution Ledger COMPLETE
  -/-> Bootstrap Manifest Carrier COMPLETE
  -/-> Internal Registry COMPLETE
  -/-> Internal Freeze Ledger COMPLETE
```

终局记录必须引用输入封印和全部源完整性，但不能把自身载体完整性传播给输入来源。

## 九、无环证明

### IR-R3-37 三层启动解析图必须单向

```text
Original Bootstrap Input Carriers
  -> Bootstrap Commit Input Boundary Vector
  -> Bootstrap Commit Evidence Resolution
  -> Evidence Resolution Ledger Boundary
  -> Boundary Seal stored in separate Seal Ledger
  -> Bootstrap Closure Resolution stored in separate Closure Ledger
  -> Bootstrap Mode projection
```

禁止反向引用：

```text
Evidence Resolution Key -/-> Evidence Resolution Ledger Boundary
Boundary Seal Covered Set -/-> Boundary Seal Record or Seal Ledger Boundary
Closure Resolution Key -/-> Closure Record, Seal Digest, Rule Version or Closure Ledger Boundary
Bootstrap Mode -/-> create or modify any resolution record
```

```text
Manifest / Window Cycle: ABSENT
Window / Evidence Resolution Cycle: ABSENT
Evidence Record / Evidence Ledger Boundary Cycle: ABSENT
Seal / Covered Set Cycle: ABSENT
Closure Key / Closure Record Cycle: ABSENT
```

## 十、R3 非法状态增量

以下状态非法或失败关闭：

```text
Resolution record consumed without its carrier boundary in the vector
One completeness record proves both allocation-ledger and namespace boundaries
Single lifecycle domain result directly changes freeze-reference applicability
Different successor targets separated into different parent conflict sets
Composite applicability omits any required domain result
Evidence resolution key includes its own ledger boundary
Boundary seal stored inside its covered evidence set
Closure resolution key includes seal digest, result, rule version or observation boundary
Multiple evidence keys directly set Bootstrap Mode
Unregistered closure computation opens NATIVE
Second different closure payload registered under another key
Late evidence silently extends a sealed set
Closure ledger completeness substitutes for any input-source completeness
```

## 十一、阻断闭合映射

| 审查阻断 | R3 规则 | 闭合结果 |
|---|---|---|
| R2-B1 新解析载体与边界向量未集成 | IR-R3-04 至 IR-R3-10、IR-R3-35 至 IR-R3-36 | 解析载体独立、完整性独立，并进入三模式认识向量 |
| R2-B2 生命周期跨域适用性缺失 | IR-R3-11 至 IR-R3-20 | 不同目标进入父集合，三个域形成稳定向量和唯一已登记复合结论 |
| R2-B3 启动终局自引用与自由冲突投影 | IR-R3-21 至 IR-R3-34、IR-R3-37 | 证据、封印、终局三层分载体，稳定冲突集和已登记终局成为唯一模式来源 |

```text
R2-B1 Repair Coverage: COMPLETE_AS_CANDIDATE
R2-B2 Repair Coverage: COMPLETE_AS_CANDIDATE
R2-B3 Repair Coverage: COMPLETE_AS_CANDIDATE
Scope Expansion: NOT_OBSERVED
Independent Review Still Required: YES
```

## 十二、R3 自检

### 载体与边界

```text
Allocation Resolution Carrier: EXPLICIT
Lifecycle Effect Resolution Carrier: EXPLICIT
Composite Lifecycle Carrier: EXPLICIT
Bootstrap Evidence / Seal / Closure Carriers: SEPARATED
Independent Completeness per Source: REQUIRED
Institution Boundary Vector Integration: COMPLETE_AS_CANDIDATE
```

### 生命周期合成

```text
All Successor Targets in One Parent Set: PASS
Three Required Domains: EXPLICIT
Domain Vector Stable Identity: PASS
Composite Resolution Candidate / Registration Chain: PASS
Cross-domain Conflict Dominance: PASS
Single-domain Direct Consumption: PROHIBITED
```

### 启动终局

```text
Evidence Key Self-reference: ABSENT
Seal Covered-set Self-reference: ABSENT
Closure Key Escape Fields: ABSENT
Cross-key Evidence Membership: COMPLETE_AS_CANDIDATE
Registered Closure as Sole Mode Source: PASS
Legacy Closure Authority: NONE
```

### 历史与权限

```text
CR-0004 Historical Text Modified: NO
CR-0004-R1 Historical Text Modified: NO
CR-0004-R2 Historical Text Modified: NO
Prior Review Text Modified: NO
Institution Freeze Created: NO
Runtime Authority Created: NO
```

## 十三、当前决定

```text
CR-0004-R3 Status: DRAFT
Authority: NONE
Executable: NO
Repair Scope: R2-B1 + R2-B2 + R2-B3 only
Internal Self-check: PASS
Independent Review: REQUIRED
Consolidation: BLOCKED
WS-01 Exit: BLOCKED
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段必须对 R3 进行独立模型、边界与启动终局复审，重点验证解析载体是否完整进入模式向量、生命周期合成是否无目标逃逸，以及封印与终局账本是否真正终止自引用。复审通过前不得合并为 `CR-0004` 制度候选，也不得声称 `WS-01` 已完成。
