# 制度注册表与冻结引用支持提案

## 提案信息

```text
Proposal ID: CR-0004
Title: Institution Registry and Freeze Reference Support
Workstream: WS-01
Status: DRAFT
Authority: NONE
Executable: NO
Proposal Form: SINGLE_PURPOSE_GOVERNANCE_MODEL
Planning Basis: CR-0002-EXTERNAL-GOVERNANCE-DEPENDENCY-CLOSURE-PLAN
Proposal Author: Codex
Proposal Authority: User-delegated drafting authority
Independent Model Review Required: YES
Bootstrap Review Required: YES
Interface Compatibility Review Required: YES
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

> 本文件是制度注册表与冻结引用支持的独立提案，不是冻结制度。它不能登记制度、验证冻结引用、授予冻结权威、创建冻结决定或使任何候选规则获得运行时资格。

## 一、单一目的与边界

### IR-C-01 本提案只有一个制度目的

本提案只定义：

> 制度版本如何以不可变身份进入制度注册表和冻结账本，以及消费方如何在明确时间、作用域和认识边界上验证一个 `Institution Freeze Reference`。

### IR-C-02 本提案不拥有相邻治理职责

本提案不定义：

- 某项业务依据是否合格；
- 某项业务权威是否适用；
- 决策是否准入或成立；
- 通用派生记录登记制度；
- 通用依赖闭包制度；
- 业务投影审计和发布制度；
- 具体数据库、哈希算法或部署拓扑；
- 谁自动成为制度冻结权威；
- 哪个制度提案应当获批。

### IR-C-03 注册表记录冻结事实，不创造冻结资格

```text
Legally Frozen Institution
  -> may be registered

Registry Entry
  -/-> create legal freeze
```

制度注册表保存和验证已经由合法治理链建立的制度事实。文件存在、注册成功、查询成功或摘要匹配都不能替代制度提案、审查、冻结权威、冻结决定和成功制度提交。

### IR-C-04 冻结引用只证明制度资格

一个可用的冻结引用只证明指定制度版本在指定作用域和时间坐标上拥有可验证冻结资格。它不证明：

- 该制度适合某个未声明用途；
- 某次资格、解析、提交或投影结果正确；
- 消费方拥有执行该制度的权威；
- 后续制度版本可以追溯改写历史。

## 二、规范对象与唯一目的

### IR-C-05 制度身份和版本必须分离

| 对象 | 类型 | 唯一目的 | 逻辑真源 |
|---|---|---|---|
| `Institution ID` | 稳定标识 | 标识一个持续演化的制度谱系 | 制度身份分配权威 |
| `Institution Version ID` | 不可变版本标识 | 标识制度谱系中的一个精确版本 | 制度版本登记边界 |
| `Institution Content Artifact` | 不可变内容引用 | 保存被审查和冻结的精确内容 | 内容存储与证据账本 |
| `Frozen Content Digest` | 内容身份值 | 绑定冻结内容的精确字节身份 | 摘要计算契约 |
| `Institution Proposal Reference` | 治理引用 | 引用独立制度提案 | 制度提案注册表 |
| `Institution Review Decision Reference` | 决策引用 | 引用独立正式审查决定 | 决策账本 |
| `Freeze Authority Reference` | 权威引用 | 引用适用于精确制度版本的冻结授权 | 权威注册表 |
| `Freeze Decision Reference` | 决策引用 | 引用冻结权威作出的冻结决定 | 决策账本 |
| `Freeze Evidence Package Reference` | 证据集合引用 | 引用支持冻结资格的不可变证据包 | 证据账本 |
| `Institution Commit Attempt` | 不可变尝试记录 | 固定一次制度提交意图和写集 | 制度提交尝试账本 |
| `Institution Commit Attribution Record` | 权威归因记录 | 证明制度登记写入归属于指定尝试和权威 | 受保护提交边界 |
| `Successful Institution Commit Reference` | 复合提交引用 | 绑定一次成功提交的尝试、注册、冻结账本和归因记录 | 受保护提交边界 |
| `Freeze Ledger Entry` | 不可变冻结记录 | 保存冻结行为、决定、权威和证据谱系 | 冻结账本 |
| `Institution Registry Entry` | 不可变注册记录 | 保存制度身份、版本、内容和有效边界 | 制度注册表 |
| `Institution Freeze Reference` | 精确消费引用 | 绑定一个注册制度版本及其冻结链 | 制度注册表和冻结账本 |
| `Freeze Reference Resolution Record` | 派生解析记录 | 记录引用在查询坐标上的验证结果 | 冻结引用解析注册表 |
| `Institution Lifecycle Relation` | 不可变关系记录 | 表达取代、撤销或失效的未来适用关系 | 制度生命周期决策账本 |
| `Institution Registry Correction Record` | 非语义更正记录 | 修复注册表示缺陷并保留原记录 | 更正登记权威 |
| `Institution Current View` | 可重建读投影 | 展示指定认识边界下的当前制度视图 | 制度注册表投影 |
| `Bootstrap Evidence Package` | 不可变启动证据集合 | 绑定启动时观察到的既有冻结制度 | 证据账本 |
| `Bootstrap Freeze Recognition Decision` | 启动冻结识别决定 | 为精确首批集合保留完整旧链或建立仅向未来生效的识别冻结 | 启动冻结识别权威 |
| `Bootstrap Commit Attempt` | 不可变启动尝试 | 固定首批集合、写集、锚和关闭意图 | 启动提交尝试账本 |
| `Bootstrap Anchor Record` | 不可变启动锚 | 固定首次登记集合、边界和关闭条件 | 启动提交边界 |
| `Bootstrap Commit Attribution Record` | 启动归因记录 | 证明首批集合归属于指定启动决定和尝试 | 启动提交边界 |
| `Successful Bootstrap Commit Reference` | 复合启动提交引用 | 绑定启动尝试、锚、首批条目、归因和关闭记录 | 启动提交边界 |
| `Bootstrap Closed Record` | 不可变关闭记录 | 证明一次性启动窗口已经关闭 | 启动提交边界 |

### IR-C-06 一个制度版本只能绑定一个精确内容身份

```text
(Institution ID, Institution Version ID)
  -> exactly one Frozen Content Digest
```

同一制度版本出现不同摘要时必须保留冲突并失败关闭。不得通过覆盖内容、重新计算后静默替换摘要或选择“最新文件”消除冲突。

### IR-C-07 一个冻结标识只能归属于一个冻结事实

```text
Freeze ID
  -> one Institution ID
  -> one Institution Version ID
  -> one Frozen Content Digest
  -> one Freeze Decision Reference
```

一个冻结标识映射到多个版本、摘要或决定时，全部相关引用解析必须保持 `CONFLICTED`，直到独立治理决定处理未来适用性；原冲突历史不得删除。

### IR-C-08 注册表位置与业务时间不得混用

至少分离：

```text
Institution Effective At
Institution Expires At
Freeze Decided At
Institution Committed At
Registry Recorded At
Evidence Observed At
Knowledge Boundary Position
```

登记顺序不能证明制度在更早业务时间已经有效，当前观察不能伪装成历史当时知识。

## 三、权威类型与分权

### IR-C-09 每项操作必须拥有精确权威类型

```text
Institution Identity Allocation Authority Type
Institution Proposal Registration Authority Type
Institution Review Decision Authority Type
Institution Freeze Decision Authority Type
Institution Commit Execution Authority Type
Freeze Ledger Registration Authority Type
Institution Registry Entry Registration Authority Type
Freeze Reference Resolution Execution Authority Type
Freeze Reference Resolution Registration Authority Type
Institution Lifecycle Decision Authority Type
Institution Registry Correction Registration Authority Type
Bootstrap Evidence Assembly Authority Type
Bootstrap Independent Review Authority Type
Bootstrap Freeze Recognition Decision Authority Type
Bootstrap Commit Execution Authority Type
```

### IR-C-10 权威不得隐式传播

拥有任一权威不自动获得另一项权威：

```text
Proposal != Review
Review != Freeze Decision
Freeze Decision != Commit Execution
Commit Execution != Registry Registration
Registry Registration != Reference Resolution
Reference Resolution != Resolution Registration
Bootstrap Assembly != Bootstrap Review
Bootstrap Review != Bootstrap Freeze Recognition Decision
Bootstrap Freeze Recognition Decision != Bootstrap Commit Execution
```

同一主体可以持有多项独立授权，但必须使用不同任务契约、输入范围、执行身份和证据记录。

### IR-C-11 每个授权实例必须声明完整边界

最低字段：

```text
Authority Grant ID
Authority Type
Holder ID
Institution ID and Version Scope
Allowed Operation
Allowed Registry and Ledger IDs
Effective At
Expires At
Can Change
Cannot Change
Granting Authority Reference
Revocation and Supersession References
Evidence References
```

缺失、过期、冲突、作用域不匹配或无法解析时，相关操作必须失败关闭。

### IR-C-12 冻结权威必须适用于精确提案版本

冻结权威不能只声明“可冻结制度”。它必须绑定制度标识、候选版本、内容摘要或可验证摘要计算输入、适用作用域、有效窗口和允许决定值。

冻结权威不得由提案作者、审查结果、证据质量、注册表解析器或最终文件存在反向产生。

### IR-C-13 权威不能验证自己的最终有效性

提案者不能批准自身提案；审查者不能创建冻结权威；冻结决策者不能单独证明写入成功；提交执行者不能登记自己的最终解析；注册表登记者不能修改候选载荷以使其通过。

## 四、内容身份与摘要契约

### IR-C-14 冻结内容必须是不可变精确工件

冻结对象至少绑定：

```text
Artifact ID
Artifact Media Type
Artifact Byte Length
Artifact Storage Reference
Canonical Byte Contract ID and Version
Digest Algorithm ID and Version
Frozen Content Digest
Content Observed At
Evidence Reference
```

实现可以使用不同存储和摘要算法，但冻结引用必须携带足以重新计算和比较摘要的完整算法及规范字节契约。

### IR-C-15 摘要不等于合法性

摘要只能证明两个精确输入在适用算法下的内容身份关系。摘要匹配不证明内容经过审查、制度有效、权威适用或冻结提交成功。

### IR-C-16 摘要算法或规范字节契约变化必须版本化

更换摘要算法、字符编码、换行规范、序列化或规范化规则时，必须追加新的摘要声明和兼容映射。不得静默重新计算并覆盖原摘要。

算法被证明不再适用时，旧摘要仍保留为历史；未来使用资格由新治理决定和证据确定。

### IR-C-17 内容定位和内容身份必须分离

文件路径、网址、仓库位置或对象存储键只能定位内容，不能单独证明内容身份。位置变化不要求新制度版本；内容变化必须形成新制度版本或明确非法冲突。

## 五、正常制度冻结链

### IR-C-18 冻结链必须完整且可追踪

一个正常模式冻结至少绑定：

```text
Registered Institution Proposal
Approved Institution Review Decision
Compatibility Review Evidence
Migration or Supersession Plan
Repeated and Stable Evidence
Cross-provider Evidence
Cross-project and Cross-domain Evidence
Applicable Freeze Authority Resolution
Observable Freeze Decision Act
Freeze Decision Record
Institution Commit Attempt
Protected Institution Commit
Institution Commit Attribution Record
Freeze Ledger Entry
Institution Registry Entry
```

任何缺失不得由模型推断、用户口头同意、文件元数据或后续成功补齐。

### IR-C-19 审查决定与冻结决定必须分离

制度审查决定值至少区分：

```text
APPROVED_FOR_FREEZE_REVIEW
RETURNED_FOR_REVISION
REJECTED
INDETERMINATE
```

`APPROVED_FOR_FREEZE_REVIEW` 只允许进入冻结权威和冻结决定门槛，不创建冻结事实。

冻结决定至少区分：

```text
FREEZE_AUTHORIZED
FREEZE_REJECTED
FREEZE_DEFERRED
```

只有适用冻结权威可以作出冻结决定；`FREEZE_AUTHORIZED` 仍必须经过受保护制度提交才形成注册冻结事实。

### IR-C-20 冻结决定必须固定全部提交输入

最低字段：

```text
Freeze Decision ID
Institution ID and Version
Frozen Content Digest
Institution Proposal Reference
Institution Review Decision Reference
Compatibility Review Reference
Migration or Supersession Plan Reference
Freeze Evidence Package Reference
Freeze Authority Reference
Effective Scope
Validity Interval
Decision Disposition
Decision At
Evidence References
```

提交执行者不得改变这些输入。

### IR-C-21 冻结标识可以预分配但不能提前取得事实地位

`Freeze ID` 可以在提交尝试中预分配以支持幂等和原子写入，但在受保护提交成功前只是候选标识：

```text
Preallocated Freeze ID
  -/-> Frozen Institution Fact
```

提交失败或未知时，不得重新使用该标识指向其他制度版本。

## 六、受保护制度提交

本节定义启动完成后的 `NATIVE` 制度登记。既有制度的启动识别和 `CR-0004` 自身的注册表外冻结分别适用第十一节，不能被本节反向要求已经存在注册表。

### IR-C-22 制度提交尝试必须先固定

进入提交点前必须追加 `Institution Commit Attempt`，至少包含：

```text
Institution Commit Attempt ID
Preallocated Freeze ID
Institution ID and Version
Frozen Content Digest
Freeze Decision Reference
Freeze Authority Reference
Declared Registry ID
Declared Freeze Ledger ID
Declared Write-set Digest
Idempotency Key
Attempted At
Evidence References
```

### IR-C-23 冻结事实必须通过不可分割写入成立

受保护提交必须在同一不可分割边界建立内容同一的：

```text
Freeze Ledger Entry
+ Institution Registry Entry
+ Institution Commit Attribution Record
```

任一部分缺失都不能宣布制度注册冻结成功。

### IR-C-24 写入必须保持完全归因

三个权威记录必须共同绑定同一提交尝试、冻结标识、制度版本、内容摘要、冻结决定、冻结权威、证据包、作用域、有效区间和写集摘要。

同一键不同内容为非法冲突；同一键同一内容可以幂等返回已有事实，但不得创建第二个冻结事实。

`Successful Institution Commit Reference` 必须复合绑定：

```text
Institution Commit Attempt ID and Digest
Freeze Ledger Entry ID and Digest
Institution Registry Entry ID and Digest
Institution Commit Attribution Record ID and Digest
Protected Boundary ID
Committed At
```

任一引用缺失、内容不一致或不属于同一保护边界时，不能作为成功制度提交引用。

### IR-C-25 完成观察不能替代权威记录

接口成功、文件写入、提交日志、仓库提交或执行者声明只能成为观察证据。只有受保护边界中的权威记录集合能够建立制度注册事实。

### IR-C-26 提交结果未知时不得推断成功或失败

```text
Protected Commit Observation Missing or Conflicted
  -> INDETERMINATE
  -> no reusable Freeze Reference
```

未知期间不得换键重试、补写结果或把预分配冻结标识授予其他制度版本。

### IR-C-27 提交解析必须与执行分权

若实现使用独立提交解析，解析者只能读取获准权威来源并生成候选解析；登记者只能登记内容相同的合格候选。解析结果不得反向创建冻结账本或注册表记录。

本条只定义制度提交所需最小边界，未来通用提交实现必须另行通过与兼容提交模型的接口审查。

## 七、制度注册表与冻结账本

### IR-C-28 注册表和冻结账本必须分工

```text
Institution Registry
  -> institution identity, version, content and lifecycle relations

Freeze Ledger
  -> freeze act, authority, decision, evidence and commit lineage
```

注册表不能单独证明冻结链；冻结账本不能代替制度身份和版本注册表。冻结引用必须绑定两者。

### IR-C-29 每个账本必须提供独立认识边界

至少包括：

```text
Registry or Ledger ID
Scope
Boundary Position or Exact Record Set
Boundary Digest
Recorded At
Boundary Authority Reference
```

一个账本的位置或摘要不能证明另一个账本完整。

### IR-C-30 登记记录必须不可变并追加

制度版本、冻结账本、提交尝试、归因、解析、更正、取代和启动记录一经登记不得覆盖或删除。

当前视图可以变化，但必须由指定认识边界内的不可变记录重建。

### IR-C-31 注册表不得吸收提案或知识职责

制度注册表只持有已登记制度事实及其谱系引用。制度提案仍属于提案注册表，模式与知识仍属于各自层级，证据仍属于证据账本。

## 八、冻结引用契约

### IR-C-32 冻结引用必须绑定最低兼容字段

`Institution Freeze Reference` 至少包含：

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

该字段集合与 `CR-0002` 和 `CR-0003` 的消费接口保持一致。

### IR-C-33 冻结引用必须增加可验证定位字段

为避免只凭显示值验证，引用还必须绑定：

```text
Institution Registry ID
Institution Registry Entry ID and Digest
Institution Registry Boundary Position
Freeze Ledger ID
Freeze Ledger Entry ID and Digest
Freeze Ledger Boundary Position
Registration Commit Reference
Canonical Byte Contract ID and Version
Digest Algorithm ID and Version
Registration Mode
Freeze Basis Mode
Reference Issued At
```

`Registration Mode` 值域：

```text
NATIVE
BOOTSTRAP_RECOGNIZED
```

两种模式必须使用不同验证路径，不能静默互换。

`Freeze Basis Mode` 值域：

```text
NATIVE_FREEZE
PRESERVED_PRE_REGISTRY_FREEZE
PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

`Registration Commit Reference` 必须按模式绑定：

```text
NATIVE
  -> Successful Institution Commit Reference

BOOTSTRAP_RECOGNIZED
  -> Successful Bootstrap Commit Reference
```

合法组合只有：

```text
NATIVE + NATIVE_FREEZE
BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE
BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION
```

其他组合必须失败关闭。

### IR-C-34 冻结引用必须拥有稳定身份

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

任一字段变化都形成新引用身份。

## 九、冻结引用解析

### IR-C-35 解析请求必须固定查询坐标

最低输入：

```text
Institution Freeze Reference Key
Requested Consumer Contract
Requested Effective Scope
Valid At
Known At
Institution Registry Boundary
Freeze Ledger Boundary
Correction Boundary
Lifecycle Boundary
Resolver Authority Reference
```

缺少任何必需边界时不能产生终局可用结论。

### IR-C-36 冻结链资格与引用适用性必须分离

冻结链资格值域：

```text
VERIFIED
REJECTED
INDETERMINATE
CONFLICTED
```

引用适用性值域：

```text
APPLICABLE
INAPPLICABLE
INDETERMINATE
CONFLICTED
```

`VERIFIED` 只表示冻结链、摘要和提交记录在认识边界内完整匹配；`APPLICABLE` 只表示引用作用域和有效时间覆盖当前请求。二者不得互相替代。

### IR-C-37 缺失不得被解释为否定证明

只有正向权威证据证明摘要错误、冻结决定拒绝、提交未成立或作用域不覆盖时，才能产生 `REJECTED` 或 `INAPPLICABLE`。

未找到、读取失败、边界不完整、记录延迟或解析器故障必须产生 `INDETERMINATE`。存在互斥权威记录时必须产生 `CONFLICTED`。

### IR-C-38 可用性投影必须保留冲突

引用可用性值域：

```text
USABLE
NOT_USABLE
INDETERMINATE
CONFLICTED
```

规则：

```text
VERIFIED + APPLICABLE -> USABLE
REJECTED + any non-conflicted applicability -> NOT_USABLE
VERIFIED + INAPPLICABLE -> NOT_USABLE
any CONFLICTED -> CONFLICTED
otherwise -> INDETERMINATE
```

`USABLE` 仍不授权任何业务行动；消费方必须另行验证自身权威、契约和全部业务前置条件。

### IR-C-39 解析计算与登记必须分权

解析执行者生成候选解析记录，解析登记者只登记内容相同且通过结构资格的候选。两者都不能修改制度、冻结账本、注册表、生命周期关系或消费方结果。

### IR-C-40 解析记录必须可复现

最低字段：

```text
Resolution ID
Institution Freeze Reference Key
Query Coordinate
Registry and Ledger Boundaries
Freeze Chain Qualification
Reference Applicability
Reference Usability
Matched Record IDs and Digests
Correction and Lifecycle References
Rule Version
Candidate and Registered Payload Digests
Resolved At
Recorded At
Evidence References
```

## 十、生命周期、取代与更正

### IR-C-41 新版本不得覆盖旧冻结版本

制度升级必须形成新的 `Institution Version ID`、内容摘要、提案、审查、冻结决定和提交记录。旧版本仍保持历史冻结事实。

### IR-C-42 取代和撤销只改变未来适用性

`SUPERSEDES`、`REVOKES` 或 `DEPRECATES` 必须由新的适用生命周期决定建立，并声明有效时间、作用域、依据和证据。

这些关系不能删除旧版本，也不能使旧版本有效期间的合法历史变成从未合法。

### IR-C-43 表示更正不得改变制度语义

注册表记录中的路径、编码、显示名称或非语义字段错误只能通过追加 `Institution Registry Correction Record` 修复。更正至少绑定原记录、更正字段、原值、新值、理由、证据、有效时间和记录时间。

内容、规则、权威作用域或有效区间的语义变化必须走新制度版本或新生命周期决定，不能伪装成更正。

### IR-C-44 当前制度视图必须可删除和重建

`Institution Current View` 只能消费指定认识边界内的注册记录、冻结账本、生命周期关系和更正记录。投影可以删除并重建，不得成为冻结事实真源。

## 十一、一次性启动闭环

### IR-C-45 启动模式只解决注册表不存在时的首次登记

启动模式适用于：

```text
Existing Legally Frozen Institution Documents
+ This Registry Institution after legal pre-registry freeze
-> First Registry Entry Set
```

它不允许把普通草案、历史提案或当前模型判断提升为冻结制度。

### IR-C-46 本提案必须先在注册表外合法冻结

如果本提案未来满足 `IF-0007`，其首次冻结必须依赖现有文件型制度治理和独立证据链完成：

```text
CR-0004 Proposal
  -> Independent Model and Compatibility Review
  -> IF-0007 Evidence Package
  -> Applicable Pre-registry Freeze Authority
  -> Pre-registry Freeze Decision
  -> Successful Pre-registry Institution Commit
```

注册表不存在不能降低冻结门槛。该路径成功后，`CR-0004` 才能进入启动登记集合；启动登记不反向创造其冻结资格。

本提案在冻结前没有规范权威，因此不能用自身规则授权自身冻结。注册表外冻结必须直接依据既有 `IF-0001`、`IF-0006`、`IF-0007`，由外部适用权威、独立审查和可追踪证据成立。

`Successful Pre-registry Institution Commit` 至少必须不可变绑定：

```text
Exact CR-0004 Artifact and Version
Frozen Content Digest and Computation Contract
Approved Review Decision
Applicable Freeze Authority Reference
Pre-registry Freeze Decision
Freeze Evidence Package Reference
Effective Scope and Validity Interval
Commit Attribution and Committed At
Immutable Repository or Equivalent History Reference
```

普通文件写入或仓库提交本身不能证明成功；独立审查必须验证上述内容同一和历史持久性。该记录随后作为启动锚的外部终止依据，不能依赖尚未建立的注册表解析器。

### IR-C-47 启动证据包必须枚举精确对象

`Bootstrap Evidence Package` 至少包含：

```text
Bootstrap Package ID and Version
Exact Institution Document Set
Declared Freeze IDs and Versions
Observed Artifact References
Bootstrap-observed Content Digests
Digest Algorithm and Canonical Byte Contract
Declared Source Conversation and Turn References if present
Available Original Freeze Evidence References
Historical Evidence Coverage per Institution
Proposed Freeze Basis Mode per Institution
Prospective Bootstrap Freeze ID when required
Missing and Conflicting Evidence
Observed At
Assembler Authority Reference
Immutable Package Digest
```

启动时计算的摘要必须明确命名为 `Bootstrap-observed Content Digest`，不得冒充原始冻结时已经存在的摘要。

### IR-C-48 历史证据覆盖必须显式分级

```text
COMPLETE
PARTIAL
INDETERMINATE
CONFLICTED
```

`PARTIAL` 或 `INDETERMINATE` 不得被美化为完整。启动审查必须逐制度说明哪些事实由原始证据支持，哪些只由当前冻结声明和当前内容观察支持。

### IR-C-49 启动审查必须独立

启动审查者不得是证据包组装者、注册表提交执行者或引用解析者。审查至少验证：

- 对象集合完整且没有静默新增；
- 每个制度身份、版本和声明冻结标识唯一；
- 当前内容摘要可复现；
- 原始与当前证据没有被混合；
- 缺失和冲突被保留；
- 既有制度历史没有被追溯改写；
- 本提案已经通过注册表外合法冻结。

### IR-C-50 启动冻结识别决定和启动提交必须分离

适用启动冻结识别权威基于独立启动审查作出 `Bootstrap Freeze Recognition Decision`。该决定必须逐制度选择一种且仅一种依据：

```text
PRESERVED_PRE_REGISTRY_FREEZE
  -> retain an exact, complete and independently verified pre-registry freeze chain

PROSPECTIVE_BOOTSTRAP_RECOGNITION
  -> allocate a new Bootstrap Freeze ID
  -> establish a new freeze qualification effective no earlier than bootstrap commit
```

第二种依据不声称原始冻结链完整，不复用原声明冻结标识，也不改变原制度的历史。它只在 `IF-0007` 证据、适用启动冻结识别权威和启动决定全部成立时，为当前精确内容建立向未来生效的注册表可验证冻结资格。

独立启动提交执行者依据该决定固定 `Bootstrap Commit Attempt` 并执行首批提交。决定者不得执行提交，提交者不得改变获批集合、摘要、锚、边界或关闭条件。

`Bootstrap Anchor Record` 至少绑定：

```text
Bootstrap Anchor ID and Version
Exact First-entry Membership and Digest
Freeze Basis Mode per Institution
Preserved Pre-registry Freeze References
Prospective Bootstrap Freeze IDs
Bootstrap Evidence Package Reference and Digest
Bootstrap Review Decision Reference
Bootstrap Freeze Recognition Decision Reference
Bootstrap Freeze Recognition Authority Reference
Bootstrap Commit Attempt ID and Write-set Digest
External Immutable Anchor Commitment Reference
Committed At
Closed At
```

外部不可变锚承诺必须允许不依赖制度注册表本身重新定位启动决定、首批集合摘要、保护边界和提交证据。只存在于待验证注册表内部的锚不能终止自证循环。

启动提交必须原子建立：

```text
Bootstrap Anchor Record
+ First Institution Registry Entry Set
+ Corresponding Freeze Ledger Recognition Entry Set
+ Bootstrap Commit Attribution Record
+ Bootstrap Closed Record
```

任一部分缺失时，启动状态为 `INDETERMINATE`，不得进入正常模式。

`Successful Bootstrap Commit Reference` 必须复合绑定启动尝试、启动锚、外部不可变锚承诺、全部首批注册条目和冻结账本识别条目、启动归因、关闭记录、保护边界及提交时间。任一内容不一致时不能作为成功启动引用。

### IR-C-51 启动识别必须使用独立登记模式

既有冻结制度进入首批集合时使用：

```text
Registration Mode: BOOTSTRAP_RECOGNIZED
```

该记录必须同时保存原声明冻结信息、启动观察摘要、历史证据覆盖、冻结依据模式和启动决定。它不得伪装成 `NATIVE`，也不得把注册表上线时间写成原制度冻结时间。

字段绑定规则：

```text
PRESERVED_PRE_REGISTRY_FREEZE
  Freeze ID -> verified pre-registry Freeze ID
  Freeze Decision Reference -> verified pre-registry decision
  Freeze Authority Reference -> verified pre-registry authority
  Freeze Evidence Package Reference -> verified pre-registry evidence package

PROSPECTIVE_BOOTSTRAP_RECOGNITION
  Freeze ID -> newly allocated Bootstrap Freeze ID
  Freeze Decision Reference -> Bootstrap Freeze Recognition Decision
  Freeze Authority Reference -> applicable bootstrap freeze recognition authority
  Freeze Evidence Package Reference -> Bootstrap Evidence Package
  Validity Start -> no earlier than successful bootstrap commit
```

原声明冻结标识和原声明时间始终作为独立历史字段保存，不能在第二种模式下冒充当前引用的冻结标识或有效起点。

### IR-C-52 启动认识只能从启动提交时向前成立

除非可验证原始证据明确支持，更早时间的注册表认识必须保持未知：

```text
Registry-known At < Bootstrap Commit At
  -> INDETERMINATE
```

既有制度在项目中的原始权威地位不由本注册表重新创造；本规则只限制注册表能够声称自己何时知道并验证该事实。

### IR-C-53 启动引用解析必须终止于启动锚

`BOOTSTRAP_RECOGNIZED` 引用的验证路径终止于不可变 `Bootstrap Anchor Record`，并按冻结依据模式继续到完整注册表外冻结记录或启动冻结识别决定；不得递归要求本注册表先验证自身引用。

```text
PRESERVED_PRE_REGISTRY_FREEZE
  -> Bootstrap Anchor
  -> Verified Pre-registry Freeze Evidence, Authority, Decision and Commit
  -> terminal verification boundary

PROSPECTIVE_BOOTSTRAP_RECOGNITION
  -> Bootstrap Anchor
  -> Bootstrap Evidence, Authority, Recognition Decision and Commit
  -> terminal verification boundary
```

解析器不能通过调用自身生成循环证明。

### IR-C-54 启动窗口必须一次性关闭

`Bootstrap Closed Record` 成立后：

```text
New BOOTSTRAP_RECOGNIZED Entry -> PROHIBITED
New Institution Entry -> NATIVE path only
```

任何扩大启动集合的需要都必须形成新的制度修订和独立审查，不得重开原启动窗口或覆盖启动锚。

## 十二、证据与完整性

### IR-C-55 冻结证据包必须是不可变清单

最低字段：

```text
Evidence Package ID and Version
Proposal and Reviewed Content References
Evidence Item IDs and Digests
Evidence Type and Reality Binding
Provider, Project and Domain Bindings
Observed At and Recorded At
Repeated and Stable Pattern References
Compatibility Review Reference
Migration Evidence Reference
Completeness Qualification Reference
Package Digest
```

### IR-C-56 证据包不得自证完整

证据组装者只能形成候选清单。完整性必须由独立资格权威依据精确规则、来源边界和证据产生候选判断，并由独立登记权威保存。

在通用资格和登记治理尚未冻结时，本提案只能声明接口要求，不能自己制造完整性事实。

`CR-0004` 的一次性注册表外冻结可以由 `IF-0007` 下显式授权的独立冻结审查，对这个精确提案和精确证据包作出有界充分性决定。该决定不得复用为通用资格规则、资格注册权威或其他制度的自动通过依据，并必须完整进入启动证据包。

### IR-C-57 空白、计划和模型审查不能替代现实证据

知识文件、验证模板、计划文档、逻辑一致性审查和一次受控成功都不能单独满足 `IF-0007` 的重复、稳定、跨提供者、跨项目、跨领域和迁移要求。

### IR-C-58 注册表边界完整性必须独立证明

引用解析使用的每个注册表和账本边界必须由其所属权威提供完整性证据。一个摘要、时间戳或水位不能自动覆盖其他账本。

## 十三、规范因果路径

### 正常制度注册路径

```text
Institution Proposal
  -> Registered Proposal
  -> Independent Institution Review Decision
       -> RETURNED / REJECTED / INDETERMINATE
            -> No Freeze Decision Eligibility
       -> APPROVED_FOR_FREEZE_REVIEW
            -> IF-0007 Evidence Qualification
            -> Compatibility and Migration Review
            -> Applicable Freeze Authority Resolution
            -> Observable Freeze Decision Act
            -> Freeze Decision Record
                 -> FREEZE_REJECTED / FREEZE_DEFERRED
                      -> No Institution Commit
                 -> FREEZE_AUTHORIZED
                      -> Institution Commit Attempt
                      -> Protected Institution Commit
                           -> Freeze Ledger Entry
                           + Institution Registry Entry
                           + Institution Commit Attribution Record
                      -> Reusable Institution Freeze Reference may be issued
```

### 正常冻结引用解析路径

```text
Institution Freeze Reference
+ Query Coordinate
+ Registry and Ledger Boundaries
+ Correction and Lifecycle Boundaries
-> Candidate Freeze Reference Resolution
-> Independent Content-identical Registration
-> Freeze Chain Qualification
+ Reference Applicability
-> Reference Usability Projection
```

### 一次性启动路径

```text
Existing Frozen Institution Documents
+ Legally Pre-registry-frozen CR-0004
-> Bootstrap Evidence Package
-> Independent Bootstrap Review
-> Bootstrap Freeze Recognition Decision
-> Protected Atomic Bootstrap Commit
     -> Bootstrap Anchor Record
     + First Registry Entry Set
     + Freeze Ledger Recognition Entry Set
     + Bootstrap Commit Attribution Record
     + Bootstrap Closed Record
-> Normal NATIVE Registration Mode
```

## 十四、操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Institution Proposal Registrar` | 登记内容同一的提案 | 审查、冻结或修改提案 |
| `Institution Reviewer` | 基于证据作出独立审查决定 | 创建冻结权威、提交制度 |
| `Institution Freeze Decision Maker` | 在适用冻结权威下作出冻结决定 | 证明自身写入成功、修改证据 |
| `Institution Committer` | 固定尝试并履行受保护写入 | 改变冻结决定、扩大写集、自行重试 |
| `Freeze Ledger Registrar` | 在受保护边界登记冻结谱系 | 创建冻结决定或冻结权威 |
| `Institution Registry Registrar` | 登记内容同一的制度版本 | 修改制度内容、审查或冻结 |
| `Freeze Reference Resolver` | 在固定坐标验证引用 | 创建制度、冻结决定或业务结果 |
| `Freeze Reference Resolution Registrar` | 登记内容同一解析候选 | 重新解析、提高确定性或修改引用 |
| `Institution Lifecycle Decision Maker` | 作出未来取代、撤销或弃用决定 | 删除或改写历史冻结事实 |
| `Institution Registry Corrector` | 追加非语义表示更正 | 修改制度语义或原记录 |
| `Bootstrap Evidence Assembler` | 组装精确启动证据集合 | 审查自身证据或登记制度 |
| `Bootstrap Reviewer` | 独立审查启动集合与证据覆盖 | 修改证据、执行启动提交 |
| `Bootstrap Freeze Recognition Decision Maker` | 为精确首批集合选择冻结依据、分配必要的新识别冻结标识并授权关闭条件 | 执行提交、修改审查、复用旧标识拼接新链 |
| `Bootstrap Committer` | 固定尝试、原子登记获批集合并关闭窗口 | 改变获批集合、追加未获批对象、重新冻结既有制度 |

## 十五、非法状态候选

未来冻结时必须明确禁止：

- 用文件路径、文件存在或 `Status: FROZEN` 单独生成冻结引用；
- 注册表登记反向创造冻结资格；
- 摘要匹配替代提案、审查、冻结权威、决定或提交；
- 同一制度版本绑定多个未保留冲突的内容摘要；
- 同一冻结标识复用于多个制度版本、摘要或决定；
- 提案者批准自身提案；
- 审查者创建冻结权威；
- 冻结决策者单独证明提交成功；
- 提交执行者改变冻结决定输入或扩大写集；
- 只写注册表或只写冻结账本就宣布成功；
- 用接口成功、仓库提交或最终文件代替受保护制度提交；
- 提交未知时换键重试或复用冻结标识；
- 解析者创建冻结决定、冻结权威或业务结果；
- 缺失、读取失败或边界延迟被解释为 `REJECTED`；
- 把 `CONFLICTED` 压缩为未知或任意终局；
- 一个账本边界证明其他账本完整；
- 更正记录修改制度语义；
- 新版本覆盖、删除或伪造旧冻结历史；
- 启动摘要冒充原始冻结时摘要；
- 启动登记把既有制度伪装成 `NATIVE`；
- 使用未定义或不合法的登记模式与冻结依据模式组合；
- 用原冻结标识拼接新的启动决定、权威或证据包；
- 把向未来生效的启动识别冻结伪装成原始历史冻结；
- 注册表通过递归调用自身验证自身合法性；
- 启动窗口关闭后继续追加 `BOOTSTRAP_RECOGNIZED` 条目；
- 用部分历史证据声称完整冻结谱系；
- 用计划、模板、模型审查或单次成功替代 `IF-0007` 经验性证据。

发现任一状态必须失败关闭、保存已有记录和冲突，并进入独立治理处理。

## 十六、相邻模型接口

### 与 IF-0001

本提案实例化权威先于执行、权威不得传播、权威边界显式、权威不得自证和历史不可变；不重新定义权威。

### 与 IF-0006

本提案消费不可变、版本绑定、现实归属、可复现和可审计证据；不让摘要、注册表或主体身份替代证据。

### 与 IF-0007

本提案实现制度提案、审查、冻结和演化的注册与验证支持；不降低制度成立条件，也不使自身绕过 `IF-0007`。

### 与 CR-0002

本提案保留 `CR-0002` 要求的八个冻结引用最低字段，并提供冻结决定、冻结权威、证据包和成功制度提交的验证路径。

本提案不创建决策事实，不替代决策准入、合法性审查或目标迁移。

### 与 CR-0003

本提案提供 `Institution Freeze Reference Resolver` 的制度输入和输出边界，并保持解析器无制度创建权威。

受保护制度提交可以由未来兼容提交实现履行，但本提案不把当前 `CR-0003` 候选当作已冻结依赖。

### 与后续工作流

```text
WS-02 Source Registry
WS-03 Temporal Mapping
WS-04 Qualification
WS-05 Authority Applicability
WS-06 Proof and Exemption Applicability
WS-07 Derived Registration
WS-08 Dependency Closure
WS-09 Projection Audit and Publication
```

后续工作流可以引用本提案的制度身份、冻结引用和解析接口，不得继承冻结、登记或启动权威。

## 十七、提案自检

```text
Single Purpose: PASS
Institution Identity and Version Separation: PASS
Registry / Freeze Ledger Separation: PASS
Proposal / Review / Freeze / Commit Separation: PASS
Authority Non-propagation: PASS
Content Identity Contract: PASS
Protected Commit Boundary: PASS
Freeze Reference Minimum Fields: COMPLETE
Freeze Chain / Applicability Separation: PASS
Missing and Conflict Preservation: PASS
Lifecycle and Correction History: PASS
Bootstrap Closure: PASS
Bootstrap Non-retroactivity: PASS
Bootstrap Recursion Prevention: PASS
Bootstrap Window Closure: PASS
IF-0001 Compatibility: PASS
IF-0006 Compatibility: PASS
IF-0007 Compatibility: PASS_WITH_INDEPENDENT_REVIEW_REQUIRED
CR-0002 Interface Compatibility: PASS_WITH_INDEPENDENT_REVIEW_REQUIRED
CR-0003 Interface Compatibility: PASS_WITH_INDEPENDENT_REVIEW_REQUIRED
Provider Independence: PASS
Cross-domain Portability: PASS
Independent Model Review: REQUIRED
Empirical Institution Evidence: INSUFFICIENT
Applicable Freeze Authority: NOT_ESTABLISHED
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

这些自检只用于发现明显遗漏，不是独立审查结论。

## 冻结前外部依赖

```text
Independent CR-0004 Model Review
Independent Bootstrap Closure Review
CR-0002 Interface Compatibility Review
CR-0003 Interface Compatibility Review
Digest and Canonical Byte Contract Review
Protected Institution Commit Implementation Evidence
Registry and Freeze Ledger Implementation Evidence
Repeated and Stable Runtime Evidence
Cross-provider Evidence
Cross-project and Cross-domain Evidence
Migration Evidence
IF-0007 Freeze Evidence Package
Applicable Pre-registry Freeze Authority
Independent Freeze Review
Pre-registry Freeze Decision
Successful Pre-registry Institution Commit
Independent Bootstrap Evidence Package
Applicable Bootstrap Freeze Recognition Authority
Bootstrap Freeze Recognition Decision
Successful Atomic Bootstrap Commit
```

## 当前决定

1. 将本文件登记为 `CR-0004` 制度注册表与冻结引用支持草案；
2. 接受 `NATIVE` 与 `BOOTSTRAP_RECOGNIZED` 两种可审计登记模式；
3. 接受先在注册表外合法冻结本提案、再执行一次性启动登记的闭环；
4. 不用启动登记追溯改写既有制度；完整旧链可以被保留，旧链不完整时只能建立拥有新标识且向未来生效的启动识别冻结；
5. 不创建制度注册表、冻结账本、冻结引用或任何运行时权威；
6. 不创建冻结标识、冻结权威、冻结决定或制度提交；
7. 不修改 `IF-0001` 至 `IF-0007`、`CR-0002` 或 `CR-0003`；
8. 下一阶段对本提案执行独立模型与启动闭环审查；
9. 独立审查通过前，不进入 `WS-02`、实现或冻结准备阶段。
