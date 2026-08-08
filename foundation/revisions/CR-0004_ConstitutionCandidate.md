# 制度注册表与冻结引用支持宪制候选

## 候选信息

```text
Proposal ID: CR-0004-CONSTITUTION-CANDIDATE
Title: Institution Registry and Freeze Reference Support
Workstream: WS-01
Status: CONSISTENCY_REVIEW_REQUIRED
Authority: NONE
Executable: NO
Consolidation Type: SEMANTIC_CONSOLIDATION
Consolidates: CR-0004 + CR-0004-R1 + CR-0004-R2 + CR-0004-R3 + CR-0004-R4 + CR-0004-R5
Review Basis: CR-0004-R5-FINAL-CLOSURE-REVIEW
Proposal Form: SINGLE_CONSTITUTION_CANDIDATE
Proposer: Codex under user-authorized consolidation
Independent Consistency Review Required: YES
External Approval Required: NO
Institution Freeze Created: NO
Freeze ID Created: NO
Freeze Authority Created: NO
Freeze Decision Created: NO
Registry Created: NO
Runtime Authority Created: NO
Depends On: IF-0001 Authority Model
Depends On: IF-0006 Evidence Model
Depends On: IF-0007 Institution Model
Compatibility Reference: CR-0002-CONSTITUTION-CANDIDATE
Compatibility Reference: CR-0003-CONSTITUTION-CANDIDATE-R2
```

> 本文件是 `CR-0004` 的单一宪制候选，不是冻结制度。它不创建制度注册表、冻结账本、冻结标识、冻结决定、启动模式或运行时权威，也不能授权任何运行时写入。基础稿、R1 至 R5 及其审查记录继续作为不可覆盖的治理历史保存。

## 候选目的

本候选只定义一项基础治理能力：使合法冻结的制度可以在分权、追加、可验证且失败关闭的边界中登记，并使消费者可以通过稳定冻结引用，在明确有效时间、认识时间、来源边界和解析模式下验证制度资格与适用性。

```text
Legally Frozen Institution
+ Registered Freeze ID Allocation
+ Protected Content-identical Institution Commit
  -> Freeze Ledger Entry
  + Institution Registry Entry
  + Institution Commit Attribution Record
  -> Registered Institution Commit Resolution
  -> Institution Freeze Reference
  -> Registered Freeze Reference Resolution
```

注册表只记录已经成立的制度冻结事实，不创造冻结资格；冻结引用只证明精确制度版本的资格和适用性，不授权业务行动。

## 规范边界

本候选中的“必须”“不得”和“只能”是待一致性审查及后续冻结的不变量候选。当前状态下，它们只约束候选审查。

本候选不定义：

- 制度内容本身；
- 决策事实或提交模型的通用语义；
- 通用证明资格、权威适用性或依赖闭包模型；
- 具体数据库、事务、消息、存储或摘要实现；
- 视频领域规则或提供者规则；
- 制度冻结权威及本候选的冻结决定；
- `WS-02` 至 `WS-09` 的外部治理职责。

## 合并解释与覆盖顺序

### IR-CC-001 最终语义必须由显式覆盖关系确定

本候选按下列覆盖关系解释来源，不按文件名、记录时间或文本顺序猜测优先级：

```text
CR-0004-R1 -> closes CR-0004 review blockers B1 through B4
CR-0004-R2 -> closes CR-0004-R1 residual blockers R1-B1 through R1-B3
CR-0004-R3 -> closes CR-0004-R2 blockers R2-B1 through R2-B3
CR-0004-R4 -> replaces raw multi-value seal and unreachable terminal entrance
CR-0004-R5 -> replaces every direct terminal-to-mode or observation-to-mode projection
```

未被后续有界修订显式覆盖的基础规则继续保留。历史阻断描述、自检状态和阶段性 `Consolidation: BLOCKED` 不进入最终规范语义。

### IR-CC-002 候选不得扩张 WS-01

合并只消除重复、应用显式覆盖并统一身份、权威、边界和解析契约。任何需要通用来源注册、时间映射、资格、权威适用性、证明与豁免、依赖闭包或发布审计的能力仍由相邻工作流提供。

## 一、统一对象与单一目的

### IR-CC-003 制度身份、版本、内容和冻结事实必须分离

```text
Institution ID
  -> stable institution identity

Institution Version ID
  -> one immutable semantic version

Frozen Content Digest
  -> exact canonical artifact content

Freeze ID
  -> one committed freeze fact
```

```text
(Institution ID, Institution Version ID)
  -> exactly one Frozen Content Digest

Freeze ID
  -> exactly one Institution ID and Version
  -> exactly one Frozen Content Digest
  -> exactly one Freeze Decision Reference
```

内容定位符、文件路径、仓库提交和媒体位置不能替代内容身份。摘要相同不证明制度合法冻结；摘要算法或规范字节契约变化必须版本化。

### IR-CC-004 注册表、冻结账本和分配账本必须分工

| 载体 | 唯一目的 | 不得创建 |
|---|---|---|
| `Institution Registry` | 制度身份、版本、内容和生命周期关系 | 冻结资格、提案或知识 |
| `Freeze Ledger` | 冻结行为、决定、权威、证据和提交谱系 | 制度内容或引用适用性 |
| `Freeze ID Allocation Ledger` | 冻结标识分配、保留和退役历史 | 冻结事实 |
| 各解析账本 | 已登记候选解析及其历史 | 被解析的原始事实 |

每个载体必须追加式、不可变、独立定位并拥有独立认识边界。

### IR-CC-005 时间字段不得互换

下列字段表达不同坐标，不得互相补推：

```text
Institution Effective At
Institution Expires At
Freeze Decided At
Institution Committed At
Registry Recorded At
Evidence Observed At
Valid At
Known At
Knowledge Boundary Position
```

历史认识视图只消费 `Recorded At <= Known At` 的来源；当前重述不得覆盖历史当时认识。

## 二、权威与候选—登记拓扑

### IR-CC-006 每项操作必须使用精确权威类型

至少分离下列权威族：

```text
Institution Identity Allocation
Institution Proposal Registration
Institution Review Decision
Institution Freeze Decision
Freeze ID Allocation Execution and Registration
Institution Commit Coordination
Freeze Ledger Entry Registration
Institution Registry Entry Registration
Institution Commit Attribution Registration
Institution Commit Resolution Execution and Registration
Lifecycle Decision, Projection, Registration and Resolution
Registry Correction Qualification and Registration
Pre-registry Commit Coordination and Registration
Bootstrap Manifest, External Anchor, Window and Internal Commit
Source Boundary Completeness Qualification and Registration
Freeze Reference Resolution Execution and Registration
Bootstrap Evidence, Seal State, Progress, Terminal Presence and Mode Resolution
```

同一主体可以持有多项独立授权，但一项授权不得隐式产生另一项授权。

### IR-CC-007 每个授权实例必须声明完整边界

```text
Authority Grant ID
Authority Type
Holder ID
Allowed Object Types and IDs
Allowed Input Source Types
Allowed Output Record Types
Allowed Registry and Ledger IDs
Allowed Rule Versions
Effective At and Expires At
Can Change
Cannot Change
Granting Authority Reference
Revocation and Supersession References
Evidence References
```

任一授权缺失、冲突、过期或作用域不匹配都失败关闭。

### IR-CC-008 计算、登记、协调和最终资格不得自证

候选执行者只能形成候选；登记者只能登记内容相同且合格的候选；保护协调者只能消费完整授权包；完整性计算者不能登记自身结论；解析者不能创建来源事实；冻结权威不能验证自身最终有效性。

所有候选—登记链必须满足：

```text
Candidate Payload Digest = Registered Payload Digest
```

同键同载荷幂等；同键不同载荷必须拒绝第二登记、追加冲突证据并保持历史。

## 三、冻结标识分配

### IR-CC-009 分配必须先形成不可变尝试

`Freeze ID Allocation Attempt` 至少绑定：

```text
Allocation Attempt ID
Freeze ID Namespace
Candidate Freeze ID
Intended Institution ID and Version
Intended Frozen Content Digest
Intended Registration Mode
Intended Freeze Basis Mode
Allocation Origin Mode
Allocation Authority Reference
Freeze ID Allocation Ledger ID
Namespace Boundary Reference
Idempotency Key
Attempted At
Evidence References
```

尝试不是分配事实、冻结决定或冻结事实。

### IR-CC-010 冻结标识必须永久唯一且不得复用

```text
Freeze ID Allocation Key =
  Freeze ID Namespace
+ Candidate Freeze ID
```

一个键只能映射一个制度版本、内容摘要、登记模式和冻结依据模式。标识在提交失败、放弃、过期或退役后仍不得重新分配。

```text
NATIVE_FREEZE -> NATIVE_NEW
PROSPECTIVE_BOOTSTRAP_RECOGNITION -> NATIVE_NEW
PRESERVED_PRE_REGISTRY_FREEZE -> BOOTSTRAP_RESERVED_EXISTING
```

`BOOTSTRAP_RESERVED_EXISTING` 只把旧标识纳入当前唯一性边界，不追溯声称当前账本在历史原冻结时完成了分配。

### IR-CC-011 分配事实与分配解析必须分离

`Freeze ID Allocation Record` 是登记事实；其候选结果必须进入独立 `Freeze ID Allocation Resolution Ledger`：

```text
Freeze ID Allocation Resolution Key =
  Allocation Attempt ID
+ Freeze ID Allocation Key
+ Allocation Ledger Boundary ID and Digest
+ Registered Allocation Boundary Completeness Record ID and Digest
+ Namespace Boundary Reference and Digest
+ Registered Namespace Boundary Completeness Record ID and Digest
+ Allocation Resolution Rule Version
```

值域：

```text
ALLOCATED | NOT_ALLOCATED | INDETERMINATE | CONFLICTED
```

精确单一内容同一分配和两个 `COMPLETE` 边界支持 `ALLOCATED`；合格、适用、完整的未分配证明支持 `NOT_ALLOCATED`；不兼容分配支持 `CONFLICTED`；来源缺失、任一边界不完整或读取失败支持 `INDETERMINATE`。

### IR-CC-012 冻结决定只能消费已登记 ALLOCATED

正常冻结和前瞻启动识别只能消费来源为 `NATIVE_NEW` 的精确已登记 `ALLOCATED`；保留既有冻结只能消费来源为 `BOOTSTRAP_RESERVED_EXISTING` 的精确已登记 `ALLOCATED`。分配解析不创建冻结事实。

退役只能追加生命周期记录，不删除历史、不回收标识、不改变已成立冻结事实。

## 四、正常冻结决定与受保护提交

### IR-CC-013 审查、冻结决定和提交必须分离

```text
Registered Institution Proposal
  -> Independent Review Decision
  -> IF-0007 Evidence Qualification
  -> Compatibility and Migration Review
  -> Applicable Freeze Authority Resolution
  -> Observable Freeze Decision Act
  -> Freeze Decision Record
  -> Protected Institution Commit
```

审查值、冻结决定值和提交结果不得互换。预分配冻结标识不能提前获得冻结事实地位。

### IR-CC-014 冻结决定必须固定全部输入

`Freeze Decision Record` 至少绑定制度身份和版本、精确内容摘要、提案、审查、兼容性和迁移引用、证据包、适用冻结权威、有效作用域、有效区间、决定值、决定时间和证据。

只有 `FREEZE_AUTHORIZED` 可以进入制度提交；`FREEZE_REJECTED` 和 `FREEZE_DEFERRED` 均不得提交。

### IR-CC-015 提交前必须固定候选写集和授权包

正常提交必须在尝试前建立：

```text
Candidate Freeze Ledger Entry
Candidate Institution Registry Entry
Candidate Institution Commit Attribution Record
Candidate Institution Commit Write-set Digest
Institution Commit Authority Bundle
```

授权包必须分别绑定协调、冻结账本登记、注册表登记和归因登记授权，以及精确分配记录、候选记录、载体、作用域和有效窗口。

### IR-CC-016 制度提交尝试必须先于提交点

`Institution Commit Attempt` 至少固定：

```text
Institution Commit Attempt ID
Freeze ID Allocation Record ID and Digest
Institution ID and Version
Frozen Content Digest
Freeze Decision and Authority References
Institution Commit Authority Bundle ID and Digest
Candidate Freeze Ledger Entry ID and Digest
Candidate Institution Registry Entry ID and Digest
Candidate Attribution Record ID and Digest
Declared Write-set Digest
Idempotency Key
Attempted At
Evidence References
```

提交执行者不得替换候选载荷或重新计算不同写集。

### IR-CC-017 三项权威记录必须在一个保护边界内成立

```text
Freeze Ledger Entry
+ Institution Registry Entry
+ Institution Commit Attribution Record
= one indivisible protected boundary
```

三个最终载荷必须分别与候选内容同一并共同归属于同一尝试、冻结标识、制度版本、摘要、决定和保护边界。协调权威不能替代任一登记权威，也不能执行部分写入。

### IR-CC-018 提交结果必须独立四值解析

```text
Institution Commit Resolution Key =
  Institution Commit Attempt ID
+ Institution Registry Boundary
+ Freeze Ledger Boundary
+ Attribution Boundary
+ Resolution Rule Version
```

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

三个内容同一权威记录及完整边界支持 `COMMITTED`；合格、适用、完整的无写入证明支持 `ABORTED`；部分写入或不兼容记录支持 `CONFLICTED`；缺失、不完整或读取失败支持 `INDETERMINATE`。完成观察不能替代解析；通用证明治理不可用时不得产生 `ABORTED`。

只有内容同一的已登记 `COMMITTED` 解析可以形成 `Successful Institution Commit Reference`。

## 五、生命周期与更正

### IR-CC-019 生命周期关系必须由独立决策事实授权

每个 `SUPERSEDES`、`REVOKES` 或 `DEPRECATES` 关系必须引用精确 `Institution Lifecycle Decision Fact`。决定事实、候选关系、登记尝试、已登记关系及关系登记解析必须形成完整谱系。

```text
Lifecycle Relation Key =
  Source Institution ID and Version
+ Target Institution ID and Version or NOT_APPLICABLE
+ Lifecycle Relation Type
+ Effective Scope Digest
+ Valid From
+ Lifecycle Decision Fact ID
```

关系只从声明的 `Valid From` 向未来影响适用性，不能追溯证明旧版本从未冻结或从未适用。

### IR-CC-020 生命周期竞争集合必须按语义域确定

最低域成员规则：

```text
SOURCE_VERSION_APPLICABILITY -> REVOKES and SUPERSEDES
SUCCESSOR_SELECTION -> SUPERSEDES
DEPRECATION_SIGNAL -> DEPRECATES
```

所有满足精确来源版本、作用域、双时间坐标、完整边界和已登记 `REGISTERED` 关系解析的成员必须进入集合；候选、边界外记录和认识时间之后的记录不得进入。

同效果或明确收敛于同效果为兼容；只有显式列出全部被替代决定事实且权威作用域相容时才构成显式替代；记录更晚、位置更大或版本号更高不自动获胜。

### IR-CC-021 生命周期效果必须独立四值解析

```text
Lifecycle Effect Resolution Key =
  Lifecycle Applicability Conflict Set Key
+ Lifecycle Registry Boundary and Digest
+ Registered Boundary Completeness Record and Digest
+ Valid At
+ Known At
+ View Mode
+ Lifecycle Effect Resolution Rule Version
```

```text
EFFECTIVE | NOT_EFFECTIVE | INDETERMINATE | CONFLICTED
```

一个规范效果或兼容收敛效果支持 `EFFECTIVE`；合格完整的空集合证明支持 `NOT_EFFECTIVE`；不兼容非替代效果支持 `CONFLICTED`；来源、成员资格或完整性未知支持 `INDETERMINATE`。

### IR-CC-022 继任目标必须先进入无目标父集合

```text
Successor Selection Conflict Set Key =
  Source Institution ID and Version
+ ALL_SUCCESSOR_TARGETS
+ Query Effective Scope Digest
+ Valid At
+ Known At
+ View Mode
+ Successor Conflict Set Rule Version
```

所有适用 `SUPERSEDES` 关系不论目标为何都进入同一父集合。独立聚合结果为：

```text
UNIQUE_SUCCESSOR | NO_SUCCESSOR | INDETERMINATE | CONFLICTED
```

不同且未被显式替代的继任目标必须为 `CONFLICTED`，不得通过按目标分键逃逸。

### IR-CC-023 生命周期域必须形成稳定向量和复合适用性

`Lifecycle Domain Resolution Vector` 必须精确绑定来源版本、作用域、`Valid At`、`Known At`、`View Mode`、三个域结果、生命周期原事实与解析账本边界、独立完整性记录、规则版本和向量摘要。

没有关系的域必须通过已登记否定结果表达，不能省略。

复合值域：

```text
APPLICABLE
APPLICABLE_WITH_DEPRECATION
INAPPLICABLE_SUPERSEDED
INAPPLICABLE_REVOKED
INDETERMINATE
CONFLICTED
```

冲突优先于未知；未知优先于确定结果；撤销产生 `INAPPLICABLE_REVOKED`；一致替代与唯一继任产生 `INAPPLICABLE_SUPERSEDED`；无撤销或替代时，弃用产生 `APPLICABLE_WITH_DEPRECATION`，否则产生 `APPLICABLE`。

只有内容同一的已登记复合适用性解析及全部 `COMPLETE` 来源边界可以改变冻结引用适用性。

### IR-CC-024 注册表更正只能修复非语义表示缺陷

```text
Correction Request and Evidence
  -> Candidate Correction Qualification
  -> Registered Correction Qualification
  -> Candidate Registry Correction
  -> Correction Registration Attempt
  -> Registered Registry Correction
```

资格值域为 `QUALIFIED | DISQUALIFIED | INDETERMINATE | CONFLICTED`。只有精确已登记且适用的 `QUALIFIED` 可以支持内容同一登记。

制度身份、版本、内容摘要、冻结标识、冻结决定或权威、证据包、作用域、有效区间、登记模式、冻结依据模式和生命周期语义不得通过更正改变。更正只追加，不覆盖原记录；后来更正不得进入更早的历史认识视图。

## 六、冻结引用与三模式解析

### IR-CC-025 冻结引用必须固定身份、定位和模式

最低兼容字段：

```text
Freeze ID
Institution ID and Version
Frozen Content Digest
Freeze Decision Reference
Freeze Authority Reference
Freeze Evidence Package Reference
Effective Scope
Validity Interval
```

可验证定位字段还必须绑定注册表及冻结账本 ID、精确记录及摘要、边界位置、提交引用、规范字节契约、摘要算法、登记模式、冻结依据模式和签发时间。

```text
Institution Freeze Reference Key =
  Freeze ID
+ Institution ID
+ Institution Version ID
+ Frozen Content Digest
+ Effective Scope Digest
+ Validity Interval
+ Registration Mode
+ Freeze Basis Mode
+ Registry Entry ID
+ Freeze Ledger Entry ID
+ Registration Commit Reference Digest
```

### IR-CC-026 只允许三种模式组合

```text
NATIVE + NATIVE_FREEZE
BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

三种模式都必须消费精确已登记 `ALLOCATED` 分配解析、复合生命周期适用性解析以及各自全部原事实和解析来源的独立 `COMPLETE` 边界。模式、制度版本、摘要、冻结标识和来源必须内容同一。

### IR-CC-027 查询坐标必须稳定且来源完备

解析请求至少固定：

```text
Institution Freeze Reference Key
Requested Consumer Contract
Requested Effective Scope
Valid At
Known At
View Mode
Institution Resolution Boundary Vector
Resolver Authority Reference
Resolution Rule Version
```

`Institution Resolution Boundary Vector` 必须按顺序包含每个被消费的原事实来源和解析来源，分别绑定载体、域、位置或精确记录集、边界摘要、独立完整性记录、所需记录、认识截点和条目摘要。未进入向量的来源不得消费；向量变化必须产生新解析身份。

### IR-CC-028 冻结链资格、引用适用性和可用性必须分离

```text
Freeze Chain Qualification:
  VERIFIED | REJECTED | INDETERMINATE | CONFLICTED

Reference Applicability:
  APPLICABLE | INAPPLICABLE | INDETERMINATE | CONFLICTED

Reference Usability:
  USABLE | NOT_USABLE | INDETERMINATE | CONFLICTED
```

```text
VERIFIED + APPLICABLE -> USABLE
REJECTED + any non-conflicted applicability -> NOT_USABLE
VERIFIED + INAPPLICABLE -> NOT_USABLE
any CONFLICTED -> CONFLICTED
otherwise -> INDETERMINATE
```

缺失、空查询、超时、缓存未命中和不完整边界不能构成否定证明。

### IR-CC-029 解析必须形成内容同一登记和可重建投影

```text
Freeze Reference + Query Coordinate + Boundary Vector
  -> Candidate Freeze Reference Resolution
  -> Resolution Registration Attempt
  -> Registered Freeze Reference Resolution
  -> Rebuildable Usability Projection
```

解析记录必须绑定稳定键、匹配记录、全部边界和完整性记录、资格、适用性、可用性、规则版本、候选和登记摘要、双时间、权威与证据。投影可删除和重建，不得成为正式事实或行动授权。

## 七、注册表外冻结与启动控制对象

### IR-CC-030 CR-0004 的注册表外冻结必须使用专用一次性链

```text
Exact CR-0004 Artifact
+ Applicable Pre-registry Freeze Authority
+ Freeze Evidence Package
+ Pre-registry Freeze Decision
  -> Pre-registry Commit Attempt
  -> Protected Pre-registry Freeze and Attribution Records
  -> Registered Pre-registry Commit Resolution
  -> Successful Pre-registry Institution Commit Reference
```

该链只适用于建立本注册表模型所需的一次性自举，不得成为通用旁路。

### IR-CC-031 注册表外提交必须四值且失败关闭

```text
Pre-registry Commit Resolution Key =
  Pre-registry Commit Attempt ID
+ Protected Carrier Boundary ID and Position
+ Resolution Rule Version
```

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

完整内容同一保护记录和完整载体支持 `COMMITTED`；合格、适用、完整的无写入证明支持 `ABORTED`；部分或不兼容写入支持 `CONFLICTED`；缺失、不完整或读取失败支持 `INDETERMINATE`。只有已登记 `COMMITTED` 可以形成成功引用。

### IR-CC-032 启动清单必须是唯一已登记控制对象

```text
Bootstrap Epoch Key = Target Institution Registry ID + GENESIS
Bootstrap Manifest Key = Bootstrap Epoch Key
```

同一注册表只有一个 `GENESIS` 清单键。清单必须在任何内部写入前固定精确首批集合、分配记录、预分配内部标识、候选摘要、窗口核心、证据、审查、识别决定、权威包、规范化契约和清单摘要；不得包含尚未产生的外部锚或最终内部锚摘要。

清单必须经过候选、登记尝试、已登记清单、候选登记解析及已登记登记解析。登记解析值域为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

只有精确已登记 `REGISTERED` 及 `COMPLETE` 清单载体边界可以进入外部锚和内部提交。

### IR-CC-033 外部启动锚必须单向承诺清单

外部锚必须由独立权威、独立载体和独立四值提交解析建立。锚核心不包含外部锚引用；外部锚单向绑定已登记清单摘要；最终内部锚再绑定锚核心和外部锚引用，禁止摘要自引用。

外部锚只承诺精确清单，不证明内部注册表写入、启动关闭或未来 `NATIVE` 准入。

### IR-CC-034 启动窗口必须拥有唯一稳定身份

```text
Bootstrap Window Definition Key =
  Bootstrap Epoch Key
+ BOOTSTRAP_WINDOW
```

窗口键不得包含清单摘要、窗口摘要或契约版本。窗口核心在清单摘要前建立；最终窗口从已登记清单、清单绑定核心及已登记外部锚构造，并固定唯一允许内部尝试、精确首批集合、允许记录、提交解析核心键和禁止第二首批集合规则。

同键不同清单、外部锚、尝试、首批集合、记录集或解析核心必须为 `CONFLICTED`。窗口不能证明启动成功或关闭。

### IR-CC-035 旧 Bootstrap Closed Record 没有规范语义

```text
Bootstrap Closed Record
  -> LEGACY_NON_NORMATIVE_BOOTSTRAP_CLOSURE_ASSERTION
```

新流程不得写入该对象。历史对象只可作为不可变输入，不能关闭窗口、建立模式、开放 `NATIVE`、替代解析或证明完整性；与新控制链不一致时只能增加冲突证据。

## 八、启动证据、封印和终局

### IR-CC-036 启动证据解析必须只消费外部输入边界

`Bootstrap Commit Input Boundary Vector` 必须绑定已登记清单、清单解析、外部锚、窗口、内部注册表、内部冻结账本、内部归因及其独立完整性记录。

它不得包含证据解析账本、封印账本、封印状态账本、进度账本、终局账本、模式账本或任何当前候选。

```text
Bootstrap Commit Evidence Resolution Key =
  Bootstrap Commit Resolution Core Key
+ Registered Bootstrap Window Definition Record ID and Digest
+ Bootstrap Commit Attempt ID and Digest
+ Bootstrap Commit Input Boundary Vector Digest
+ Bootstrap Evidence Resolution Rule Version
```

证据解析值域 `COMMITTED | ABORTED | INDETERMINATE | CONFLICTED` 只作为后续输入，不能直接产生启动模式。

### IR-CC-037 所有证据边界变体必须进入同一冲突集合

```text
Bootstrap Commit Resolution Conflict Set Key =
  Bootstrap Epoch Key
+ Bootstrap Manifest Key
+ Bootstrap Window Definition Key
+ Allowed Bootstrap Commit Attempt ID
```

键不得包含证据结果、输入向量、规则版本、账本位置或时间。所有匹配控制身份的证据解析均进入该集合；声称另一实际尝试的记录仍进入授权尝试集合并作为不兼容成员。

### IR-CC-038 原始封印只表达 SEALED_COMPLETE

`Bootstrap Commit Evidence Boundary Seal Record` 是受保护单赋值的不可变正向事实：

```text
Seal Fact Result: SEALED_COMPLETE
```

只有精确冲突集合、`COMPLETE` 证据解析边界、成员资格确定且无迟到证据时可以登记。`NOT_SEALED`、`INDETERMINATE` 和 `CONFLICTED` 不是原始封印事实。

同键同内容幂等；同键不同内容、越界写入和封印后迟到证据必须拒绝并追加冲突证据。原封印不得改写、扩展或重封。

### IR-CC-039 封印状态必须独立四值解析

`Bootstrap Evidence Seal State Input Vector` 必须绑定冲突集合、证据解析边界、原始封印边界、封印冲突子域、双时间、视图模式和各自独立完整性记录，且不得引用封印状态、进度或终局载体。

```text
Bootstrap Commit Evidence Seal State Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Evidence Seal State Input Vector Digest
+ Seal State Resolution Rule Version
```

```text
SEALED_COMPLETE | NOT_SEALED | INDETERMINATE | CONFLICTED
```

单一内容同一封印、精确集合、全部完整且无冲突支持 `SEALED_COMPLETE`；合格、适用、完整的无封印证明支持 `NOT_SEALED`；封印、登记或迟到证据冲突支持 `CONFLICTED`；缺失、不完整、资格不可用或读取失败支持 `INDETERMINATE`。

状态解析必须经过候选—登记链并保留不同边界和认识时间的历史。

### IR-CC-040 非终局未知必须进入独立进度载体

```text
Bootstrap Closure Progress Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Registered Seal State Resolution ID and Digest
+ Seal State Resolution Ledger Boundary ID and Digest
+ Known At
+ Closure Progress Rule Version
```

进度值只能是 `INDETERMINATE`。已登记封印状态 `NOT_SEALED` 或 `INDETERMINATE` 且状态账本边界 `COMPLETE` 时可产生进度；它不得占用终局键、开放 `NATIVE`、声称关闭或阻止后来终局。

### IR-CC-041 只有确定封印状态可以形成终局

```text
Bootstrap Closure Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
```

终局值域：

```text
COMMITTED | ABORTED | CONFLICTED
```

已登记 `SEALED_COMPLETE`、精确封印集合、全部证据收敛 `COMMITTED` 且所有来源完整，产生候选 `COMMITTED`；全部证据收敛 `ABORTED`、存在合格适用完整的无保护写入证明且所有来源完整，产生候选 `ABORTED`；封印状态、证据、控制链、登记或迟到证据冲突，产生候选 `CONFLICTED`。

终局必须独立执行、内容同一登记并按冲突集合键受保护单赋值。同键不同载荷只能追加终局登记冲突，使终局载体失败关闭，不能形成第二终局。

## 九、终局存在与当前模式仲裁

### IR-CC-042 终局存在性必须独立四值解析

`Bootstrap Terminal Presence Input Vector` 必须绑定终局载体及边界、终局冲突子域及边界、各自独立完整性记录、双时间和视图模式，且不得引用存在解析或模式解析载体。

```text
Bootstrap Terminal Presence Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Terminal Presence Input Vector Digest
+ Terminal Presence Rule Version
```

```text
PRESENT | ABSENT | INDETERMINATE | CONFLICTED
```

精确单一终局、全部边界完整且无冲突支持 `PRESENT`；合格、适用、完整的精确无终局证明支持 `ABSENT`；终局登记或物理载体冲突支持 `CONFLICTED`；缺失、不完整、资格不可用或读取失败支持 `INDETERMINATE`。终局记录不能自行证明 `PRESENT`，空查询不能证明 `ABSENT`。

### IR-CC-043 模式源向量必须固定全部来源且无自引用

`Bootstrap Closure Mode Source Vector` 至少绑定：

```text
Bootstrap Commit Resolution Conflict Set Key
Registered Seal State Resolution ID and Digest
Registered Terminal Presence Resolution ID and Digest
Registered Terminal Closure ID and Digest or NOT_APPLICABLE
Registered Closure Progress ID and Digest or NOT_APPLICABLE
Seal State, Presence, Terminal, Progress and Conflict Boundaries
Independent Source Completeness Record IDs and Digests
Valid At
Known At
View Mode
Mode Arbitration Contract Version
Vector Digest
```

`PRESENT` 必须携带精确终局且进度只作历史；`ABSENT` 必须把终局标记为 `NOT_APPLICABLE`，只有形成未决候选时才要求精确进度；`CONFLICTED` 不允许终局或进度覆盖冲突；`INDETERMINATE` 不允许确定模式。

向量不得包含模式解析账本、当前模式候选或当前模式记录。

### IR-CC-044 当前启动模式必须由已登记五值仲裁唯一产生

```text
Bootstrap Closure Mode Resolution Key =
  Bootstrap Commit Resolution Conflict Set Key
+ Bootstrap Closure Mode Source Vector Digest
+ Bootstrap Mode Arbitration Rule Version
```

```text
ACTIVE_CLOSED
ABORTED_CLOSED
COMMIT_UNRESOLVED
CONFLICTED
INDETERMINATE
```

冲突具有最高优先级：任一封印状态冲突、终局存在冲突、来源完整性冲突、终局登记冲突、身份不一致或同键模式解析冲突都产生 `CONFLICTED`。

无冲突且 `PRESENT + COMMITTED + SEALED_COMPLETE + 全部边界 COMPLETE` 产生 `ACTIVE_CLOSED`；无冲突且 `PRESENT + ABORTED + SEALED_COMPLETE + 全部边界 COMPLETE` 产生 `ABORTED_CLOSED`；`PRESENT + CONFLICTED` 产生 `CONFLICTED`；无冲突且 `ABSENT + 精确 INDETERMINATE 进度 + NOT_SEALED 或 INDETERMINATE 封印状态 + 全部边界 COMPLETE` 产生 `COMMIT_UNRESOLVED`；其他缺失、不完整或读取失败产生 `INDETERMINATE`。

### IR-CC-045 只有已登记模式可以产生 Bootstrap Mode

```text
Registered Bootstrap Closure Mode Resolution
+ Mode Resolution Ledger Boundary COMPLETE
+ exact Mode Source Vector
+ all referenced source boundaries COMPLETE
  -> Bootstrap Mode at Valid At / Known At / View Mode
```

候选模式、原始终局、进度、封印、文件存在性、自由观察和旧关闭断言均不能直接产生模式。

只有精确已登记 `ACTIVE_CLOSED`、模式账本边界 `COMPLETE` 及当前制度解析边界向量可以开放正常 `NATIVE` 登记。其他四值全部失败关闭。

### IR-CC-046 迟到冲突必须改变当前认识而不改写历史

```text
Historical Known At T1:
  Registered Mode = ACTIVE_CLOSED

Current Known At T2:
  late conflict registered
  -> Registered Mode = CONFLICTED
```

历史 `ACTIVE_CLOSED` 保留为历史认识；它不得作为当前重述覆盖迟到冲突。任何当前模式变化都必须产生新的来源向量和已登记模式解析历史。

## 十、载体完整性与无环终止

### IR-CC-047 每个被消费来源必须独立证明完整

每个原事实、解析、冲突子域、封印、进度、终局、存在和模式载体必须提供自己的 `Registered Source Boundary Completeness Record`：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

一个载体、共享时间戳、“已读取最新”或下游终局不能证明另一来源完整。确定正向或否定结果要求全部适用来源为 `COMPLETE`；冲突不得降级为未知或确定结果。

### IR-CC-048 启动解析图必须单向终止

```text
Original Bootstrap Input Carriers
  -> Input Boundary Vector
  -> Evidence Resolution Ledger
  -> Raw Seal Ledger
  -> Seal State Resolution Ledger
  -> Progress Ledger or Terminal Closure Ledger
  -> Terminal Presence Resolution Ledger
  -> Mode Source Vector
  -> Mode Resolution Ledger
  -> Bootstrap Mode
  -> NATIVE admission or failure-closed result
```

任何键不得引用自身载体、当前候选或当前记录；任何投影不得反向创建或修改来源。模式账本边界不可用时只产生外层安全失败，不得递归建立新的模式解析来证明自身失败。

## 十一、证据、投影和历史

### IR-CC-049 冻结证据包必须不可变、精确且不自证完整

证据包必须绑定提案和审查内容、精确证据项及摘要、现实绑定、提供者/项目/领域绑定、观察与记录时间、重复稳定证据、兼容性和迁移证据、完整性资格及包摘要。

空白、计划、模型审查、文件存在或路径不能替代现实证据。证据包组装者不能证明自身完整，解析结果也不能提升证据权威。

### IR-CC-050 生命周期、更正、退役和投影必须保留历史

新制度版本不得覆盖旧冻结版本；取代、撤销、退役和更正只追加事实并按声明时间改变未来适用性。当前读面和可用性投影必须具有稳定身份、可删除和可重建，不能反向修改注册表、账本或历史解析。

## 十二、规范因果路径

### IR-CC-051 正常冻结登记路径

```text
Proposal
  -> Independent Review
  -> IF-0007 Evidence and Compatibility Qualification
  -> Applicable Freeze Authority
  -> Freeze Decision
  -> Registered ALLOCATED Freeze ID Resolution
  -> Fixed Candidate Write Set and Authority Bundle
  -> Institution Commit Attempt
  -> Protected Content-identical Write
  -> Registered Institution Commit Resolution
  -> Institution Freeze Reference
```

### IR-CC-052 生命周期和更正路径

```text
Lifecycle Decision Fact
  -> Registered Lifecycle Relation
  -> Domain Conflict Sets
  -> Registered Domain Resolutions
  -> Lifecycle Domain Resolution Vector
  -> Registered Composite Lifecycle Applicability
  -> Freeze Reference Applicability

Correction Request
  -> Registered Correction Qualification
  -> Registered Non-semantic Correction
  -> Boundary-aware Read Projection
```

### IR-CC-053 一次性启动路径

```text
Successful Pre-registry CR-0004 Commit
+ Existing Legally Frozen Institutions
  -> Registered Genesis Manifest
  -> Registered External Anchor
  -> Registered Bootstrap Window
  -> Protected Internal Bootstrap Commit
  -> Evidence Resolution Conflict Set
  -> Raw Seal Fact
  -> Registered Seal State
  -> Registered Progress or Terminal
  -> Registered Terminal Presence
  -> Registered Five-value Mode
  -> ACTIVE_CLOSED only
  -> NATIVE admission
```

启动提交之后不得建立第二首批集合、第二窗口或新的 `BOOTSTRAP_RECOGNIZED` 制度条目。

### IR-CC-054 冻结引用解析路径

```text
Institution Freeze Reference
+ Query Coordinate
+ Complete Institution Resolution Boundary Vector
+ Registered Allocation Resolution
+ Registered Composite Lifecycle Applicability
+ Mode-specific Bootstrap Sources when applicable
  -> Candidate Freeze Reference Resolution
  -> Content-identical Registration
  -> Qualification + Applicability + Usability
  -> Rebuildable Projection
```

## 十三、非法状态总表

### IR-CC-055 下列状态必须拒绝或失败关闭

- 由注册表条目、摘要、文件或提案反推合法冻结；
- 未经已登记 `ALLOCATED` 分配解析创建冻结决定或提交；
- 冻结标识复用、同键不同内容或退役后回收；
- 候选载荷与登记载荷不一致；
- 协调权威替代登记权威或部分保护写入；
- 用完成观察、缺失、空查询、超时或缓存未命中推断 `COMMITTED`、`ABORTED`、`NOT_ALLOCATED`、`ABSENT` 或 `NOT_SEALED`；
- 让生命周期关系、单域效果或自由计算直接改变引用适用性；
- 让不同继任目标通过分键逃逸冲突；
- 更正语义字段、覆盖历史或把后来认识投射到更早历史；
- 第二 `GENESIS` 清单、第二窗口、第二首批集合或窗口重开；
- 把 `Bootstrap Closed Record`、原始封印、证据解析、进度或终局直接投影为模式；
- 把 `INDETERMINATE` 写入终局单赋值键；
- 忽略迟到冲突、最后写入获胜或使用历史成功覆盖当前冲突；
- 任一解析键或边界向量引用自身载体、当前候选或当前记录；
- 用一个来源的完整性证明另一个来源完整；
- 候选或未登记模式开放 `NATIVE`；
- 把冻结引用解析、投影或模式结果解释为业务行动权威。

## 十四、权威操作矩阵

| 操作 | 所需独立权威 | 输出 | 明确禁止 |
|---|---|---|---|
| 分配冻结标识 | 分配执行 + 分配登记 | 分配事实及解析 | 创建冻结事实 |
| 作出冻结决定 | 冻结决定 | 冻结决定记录 | 分配标识或提交 |
| 正常制度提交 | 协调 + 三项登记 | 三项内容同一权威记录 | 部分写入或修改候选 |
| 生命周期登记 | 决定 + 投影 + 登记 + 解析 | 关系及域解析 | 按时间或顺序选赢家 |
| 注册表更正 | 资格执行/登记 + 更正登记 | 非语义更正 | 修改制度语义 |
| 注册表外提交 | 专用协调、登记和解析 | 一次性冻结链 | 通用旁路 |
| 启动控制登记 | 清单、锚、窗口、内部提交各自权威 | 唯一控制链 | 重开窗口 |
| 封印与终局 | 封印、状态、进度、终局各自权威 | 追加解析历史 | 原始事实自证状态 |
| 模式仲裁 | 存在执行/登记 + 模式执行/登记 | 已登记五值模式 | 直接投影或开放来源写权 |
| 冻结引用解析 | 解析执行 + 解析登记 | 已登记资格/适用性/可用性 | 创建制度或行动权威 |

## 十五、来源谱系与语义差异

### IR-CC-056 基础来源覆盖映射

| 来源范围 | 候选规则 | 合并处理 |
|---|---|---|
| `IR-C-01..04` | `IR-CC-002..004` | 保留单一目的、资格边界和注册表非创设性 |
| `IR-C-05..08` | `IR-CC-003..005` | 统一身份、内容、冻结事实和时间 |
| `IR-C-09..17` | `IR-CC-006..008`、`IR-CC-049` | 保留分权、内容身份和摘要契约 |
| `IR-C-18..31` | `IR-CC-013..018`、`IR-CC-004` | 由 R1/R2 补全分配、候选写集和解析拓扑 |
| `IR-C-32..40` | `IR-CC-025..029` | 由 R1/R3 补全三模式和解析来源边界 |
| `IR-C-41..44` | `IR-CC-019..024`、`IR-CC-050` | 由 R2/R3 覆盖为域合成及追加更正 |
| `IR-C-45..54` | `IR-CC-030..046` | 由 R1-R5 全量覆盖为无环启动与已登记模式 |
| `IR-C-55..58` | `IR-CC-047..050` | 保留证据和完整性边界 |

### IR-CC-057 修订来源覆盖映射

| 来源范围 | 候选规则 | 最终语义 |
|---|---|---|
| `IR-R1-03..15` | `IR-CC-009..018` | 分配、授权包、逐记录内容同一和提交解析 |
| `IR-R1-16..27` | `IR-CC-019..024` | 生命周期与更正因果 |
| `IR-R1-28..42` | `IR-CC-030..035` | 注册表外提交、外部锚和窗口 |
| `IR-R1-43..55` | `IR-CC-025..029`、`IR-CC-047` | 来源完整性、三模式和确定解析 |
| `IR-R2-04..11` | `IR-CC-011..012` | 分配事实与解析分离及双完整性 |
| `IR-R2-12..23` | `IR-CC-020..023` | 竞争集合、效果解析和复合适用性 |
| `IR-R2-24..34` | `IR-CC-032..037` | 清单、窗口、旧关闭退场和唯一控制链 |
| `IR-R3-04..10` | `IR-CC-026..029`、`IR-CC-047` | 独立解析载体进入边界向量 |
| `IR-R3-11..20` | `IR-CC-020..023` | 跨目标聚合和跨域合成 |
| `IR-R3-21..37` | `IR-CC-036..041`、`IR-CC-048` | 证据、冲突集合、封印和终局无环分层 |
| `IR-R4-04..21` | `IR-CC-038..041`、`IR-CC-047..048` | 原始封印单值、四值状态、进度与终局分离 |
| `IR-R5-04..26` | `IR-CC-042..048` | 四值存在、稳定模式向量、五值仲裁和迟到冲突 |

阶段边界、自检、非法状态增量和阻断映射分别合并到候选元数据、`IR-CC-055`、闭合矩阵及当前决定，不作为独立运行时规则重复保留。

### IR-CC-058 关键语义覆盖必须明确

```text
Old direct Bootstrap Closed Record authority
  -> removed; legacy non-normative input only

Old Bootstrap Commit Resolution direct-to-mode projection
  -> removed; evidence -> seal state -> terminal presence -> registered mode

Old raw seal multi-value record
  -> removed; raw fact only SEALED_COMPLETE

Old INDETERMINATE terminal
  -> removed; stored in progress ledger

Old terminal absence by missing record
  -> removed; requires qualified registered ABSENT resolution

Old terminal result dominating late conflict
  -> removed; current registered mode uses conflict-first arbitration
```

### 最终规则来源谱系

| 最终候选规则 | 主要规范来源 |
|---|---|
| `IR-CC-001..002` | `IR-R1-01..02`、`IR-R2-01..03`、`IR-R3-01..03`、`IR-R4-01..03`、`IR-R5-01..03` |
| `IR-CC-003..005` | `IR-C-03..08`、`IR-C-14..17` |
| `IR-CC-006..008` | `IR-C-09..13`、`IR-R1-10..15` 及后续各解析分权规则 |
| `IR-CC-009..012` | `IR-R1-03..09`、`IR-R2-04..11`、`IR-R3-04..09` |
| `IR-CC-013..018` | `IR-C-18..31`、`IR-R1-10..15` |
| `IR-CC-019..024` | `IR-C-41..44`、`IR-R1-16..27`、`IR-R2-12..23`、`IR-R3-11..20` |
| `IR-CC-025..029` | `IR-C-32..40`、`IR-R1-43..55`、`IR-R3-04..10` |
| `IR-CC-030..035` | `IR-C-45..54`、`IR-R1-28..42`、`IR-R2-24..34` |
| `IR-CC-036..041` | `IR-R2-30..34`、`IR-R3-21..37`、`IR-R4-04..18` |
| `IR-CC-042..046` | `IR-R3-33..37`、`IR-R4-19..21`、`IR-R5-04..24` |
| `IR-CC-047..048` | `IR-C-29`、`IR-C-58`、`IR-R1-43..47`、`IR-R3-04..10`、`IR-R3-35..37`、`IR-R4-20..21`、`IR-R5-25..26` |
| `IR-CC-049..050` | `IR-C-41..44`、`IR-C-55..58`、`IR-R1-21..27` |
| `IR-CC-051..054` | `IR-C-18`、`IR-C-45..54` 及 R1 至 R5 对应规范因果路径 |
| `IR-CC-055` | 基础稿与 R1 至 R5 的全部非法状态集合 |
| `IR-CC-056..058` | `CR-0004-R5-FINAL-CLOSURE-REVIEW` 合并约束及全部显式覆盖声明 |

R4 的 `IR-R4-22..25` 和 R5 的 `IR-R5-27..30` 属于非法状态、自检、阻断闭合及阶段决定，分别进入 `IR-CC-055`、候选自检、历史阻断闭合矩阵和当前决定；没有被遗漏或提升为运行时事实。

## 十六、历史阻断闭合矩阵

| 历史阻断 | 候选闭合规则 | 状态 |
|---|---|---|
| 冻结标识分配四值解析身份 | `IR-CC-009..012`、`IR-CC-047` | CLOSED_AS_CANDIDATE |
| 生命周期决定竞争与继任目标逃逸 | `IR-CC-019..023` | CLOSED_AS_CANDIDATE |
| 启动清单、窗口和唯一关闭来源 | `IR-CC-032..035` | CLOSED_AS_CANDIDATE |
| 新增解析载体未进入来源边界 | `IR-CC-027`、`IR-CC-047` | CLOSED_AS_CANDIDATE |
| 生命周期跨域适用性未唯一合成 | `IR-CC-022..023` | CLOSED_AS_CANDIDATE |
| 启动终局自引用和自由冲突投影 | `IR-CC-036..041`、`IR-CC-048` | CLOSED_AS_CANDIDATE |
| 封印失败分支不可达 | `IR-CC-038..041` | CLOSED_AS_CANDIDATE |
| 当前模式缺少已登记仲裁 | `IR-CC-042..046` | CLOSED_AS_CANDIDATE |
| 终局后迟到冲突无法改变当前模式 | `IR-CC-043..046` | CLOSED_AS_CANDIDATE |

## 十七、冻结前外部依赖

本候选即使通过一致性审查，也仍至少依赖：

```text
IF-0007 authoritative institution freeze process
Applicable freeze authority and observable freeze decision
Digest and canonical byte contract review
Protected commit implementation evidence
Registry, freeze ledger and all resolution carrier implementation evidence
Repeated and stable runtime evidence
Cross-provider, cross-project and cross-domain evidence
Migration evidence
WS-02 through WS-09 external governance closure
```

这些依赖不阻断候选一致性审查，但阻断制度冻结和运行时激活。

## 十八、候选自检状态

```text
Single Purpose: PASS
Source Set Limited to CR-0004 and R1 through R5: PASS
Explicit Overlay Precedence: PASS
Institution Identity / Version / Content Separation: PASS
Freeze ID Allocation Resolution Identity: PASS
Protected Registration Authority Topology: PASS
Lifecycle Cross-target and Cross-domain Composition: PASS
Pre-registry Commit Boundary: PASS
Bootstrap Manifest and Window Stable Identity: PASS
Bootstrap Evidence / Seal / Terminal Separation: PASS
Terminal Presence Four-value Registration: PASS
Registered Five-value Mode Arbitration: PASS
Post-terminal Conflict Dominance: PASS
Unqualified Negative Projection Paths: 0
Unregistered Positive Mode Paths: 0
Unresolved Self-reference Cycles: 0
Open Historical Model Blockers: 0
Independent Consistency Review: REQUIRED
Institution Freeze Eligibility: NOT_ASSESSED
```

## 当前决定

```text
CR-0004 Constitution Candidate: CREATED
Status: CONSISTENCY_REVIEW_REQUIRED
Authority: NONE
Executable: NO
Consolidation: COMPLETED_AS_CANDIDATE
Independent Consistency Review: REQUIRED
WS-01 Exit: BLOCKED_PENDING_CONSISTENCY_REVIEW
Institution Freeze: NOT_CREATED
Runtime Authority: NOT_CREATED
```

下一阶段只能执行 `CR-0004-CONSTITUTION-CANDIDATE` 独立一致性审查。审查通过前不得退出 `WS-01`；审查通过也不等于创建冻结、注册表或运行时权威。
