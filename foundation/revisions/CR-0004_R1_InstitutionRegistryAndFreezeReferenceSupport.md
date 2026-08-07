# 制度注册表与冻结引用支持有界修订 R1

## 修订信息

```text
Proposal ID: CR-0004-R1
Title: Institution Registry and Freeze Reference Support Bounded Closure R1
Status: DRAFT
Authority: NONE
Executable: NO
Amends: CR-0004
Repair Basis: CR-0004-LOCAL-REVIEW
Repair Scope: B1 + B2 + B3 + B4 only
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

> 本文件只修复 `CR-0004-LOCAL-REVIEW` 的四项阻断。它不是冻结制度，不创建冻结标识、注册表、账本、提交解析或运行时权威，也不覆盖 `CR-0004` 和独立审查的历史文本。

## 一、修订解释边界

### IR-R1-01 R1 只覆盖四个阻断簇

```text
B1 Freeze ID and Protected Registration Authority Topology
B2 Lifecycle and Correction Registration Causality
B3 Pre-registry Commit and External Bootstrap Anchor Protocol
B4 Mode-specific Freeze Reference Resolution Contract
```

`CR-0004` 中与这些阻断无冲突的规则继续作为合并来源。R1 与基础稿冲突时，仅在上述范围内以 R1 为后续合并候选语义。

### IR-R1-02 R1 不扩张 WS-01 单一目的

R1 不定义通用决策、通用提交、通用资格、业务权威适用性、通用依赖闭包或业务投影。R1 新增的分配、登记、解析和启动角色只适用于制度注册表与冻结引用支持。

## 二、B1：冻结标识分配权威

### IR-R1-03 冻结标识必须由独立分配权威产生

新增：

```text
Freeze ID Allocation Authority Type
Freeze ID Allocation Execution Authority Type
Freeze ID Allocation Registration Authority Type
Freeze ID Allocation Retirement Authority Type
```

冻结决定、制度提交、注册表登记和启动识别权威都不自动拥有冻结标识分配权。

分配记录的唯一逻辑真源是追加式 `Freeze ID Allocation Ledger`。该账本只持有标识分配、旧标识保留和退役历史，不创建制度冻结事实；其边界必须独立于制度注册表和冻结账本。

### IR-R1-04 分配必须先形成不可变尝试

`Freeze ID Allocation Attempt` 至少包含：

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

分配尝试不是冻结事实、冻结决定或已分配标识记录。

### IR-R1-05 分配结果必须独立登记

分配执行者只能生成候选结果，分配登记者只登记内容相同的合格候选。

`Freeze ID Allocation Record` 至少包含：

```text
Allocation Record ID
Allocation Attempt ID
Freeze ID Namespace
Allocated Freeze ID
Institution ID and Version
Frozen Content Digest
Registration Mode
Freeze Basis Mode
Allocation Origin Mode
Freeze ID Allocation Ledger ID and Position
Namespace Boundary Reference and Digest
Allocation Authority Reference
Candidate Payload Digest
Registered Payload Digest
Allocated At
Recorded At
Evidence References
```

`Allocation Origin Mode` 值域：

```text
NATIVE_NEW
BOOTSTRAP_RESERVED_EXISTING
```

`NATIVE_NEW` 表示在当前命名空间中新分配标识；`BOOTSTRAP_RESERVED_EXISTING` 只把已由完整注册表外冻结链使用的旧标识纳入当前唯一性边界，不声称该标识在历史原冻结时已经由本分配账本产生。

### IR-R1-06 分配结果使用四值解析

```text
ALLOCATED
NOT_ALLOCATED
INDETERMINATE
CONFLICTED
```

规则：

```text
exactly one registered content-identical allocation -> ALLOCATED
qualified complete proof of no allocation for matched attempt -> NOT_ALLOCATED
multiple incompatible authoritative allocations -> CONFLICTED
missing, incomplete boundary or read failure -> INDETERMINATE
```

`NOT_ALLOCATED` 不能由未找到记录、超时或缓存缺失推断。

### IR-R1-07 冻结标识在命名空间内永久唯一且不得复用

稳定键：

```text
Freeze ID Allocation Key =
  Freeze ID Namespace
+ Candidate Freeze ID
```

一个键只能映射一个制度版本、内容摘要、登记模式和冻结依据模式。同键不同内容为 `CONFLICTED`。

已分配标识即使提交失败、被放弃、过期或退役，也不得分配给其他制度版本或摘要。

合法来源组合：

```text
NATIVE_FREEZE -> NATIVE_NEW
PROSPECTIVE_BOOTSTRAP_RECOGNITION -> NATIVE_NEW
PRESERVED_PRE_REGISTRY_FREEZE -> BOOTSTRAP_RESERVED_EXISTING
```

旧标识保留记录必须引用完整注册表外冻结链、原标识赋值证据和当前启动审查，不得把 `Recorded At` 冒充原始分配时间。

### IR-R1-08 退役只追加生命周期记录

`Freeze ID Retirement Record` 必须引用原分配记录、退役权威、原因、证据、有效时间和记录时间。

退役只禁止未来使用，不删除分配历史，不把标识恢复到可分配池，也不改变任何已成立冻结事实。

### IR-R1-09 冻结决定只能消费已登记分配

正常 `NATIVE` 冻结决定和 `PROSPECTIVE_BOOTSTRAP_RECOGNITION` 启动决定必须引用状态为 `ALLOCATED` 且来源为 `NATIVE_NEW` 的精确 `Freeze ID Allocation Record`。

`PRESERVED_PRE_REGISTRY_FREEZE` 启动决定必须引用来源为 `BOOTSTRAP_RESERVED_EXISTING` 的精确保留记录；原注册表外冻结决定不被追溯要求引用后来建立的分配记录。

```text
Freeze Decision Maker
  -/-> allocate Freeze ID

Bootstrap Freeze Recognition Decision Maker
  -/-> allocate Freeze ID
```

决定中的制度版本、摘要和模式必须与分配记录内容同一。

## 三、B1：受保护登记权威拓扑

### IR-R1-10 每个权威写入拥有独立授权

新增：

```text
Institution Commit Coordination Authority Type
Freeze Ledger Entry Registration Authority Type
Institution Registry Entry Registration Authority Type
Institution Commit Attribution Registration Authority Type
Institution Commit Resolution Execution Authority Type
Institution Commit Resolution Registration Authority Type
Bootstrap Internal Commit Coordination Authority Type
Bootstrap Anchor Registration Authority Type
Bootstrap Freeze Ledger Recognition Registration Authority Type
Bootstrap Institution Entry Registration Authority Type
Bootstrap Commit Attribution Registration Authority Type
Bootstrap Window Definition Registration Authority Type
```

协调权威只能组织同一保护边界，不能创建、继承或扩大任何登记权威。

### IR-R1-11 提交前必须固定候选权威载荷

正常制度提交必须在提交尝试前建立：

```text
Candidate Freeze Ledger Entry
Candidate Institution Registry Entry
Candidate Institution Commit Attribution Record
```

每个候选记录必须拥有稳定身份、完整载荷和独立摘要。三个候选共同形成 `Candidate Institution Commit Write-set Digest`。

### IR-R1-12 提交授权包必须完整

`Institution Commit Authority Bundle` 至少绑定：

```text
Commit Coordination Authority Grant
Freeze Ledger Registration Authority Grant
Institution Registry Entry Registration Authority Grant
Commit Attribution Registration Authority Grant
Allowed Institution ID and Version
Allowed Freeze ID Allocation Record
Allowed Registry and Ledger IDs
Allowed Candidate Record IDs and Digests
Effective At and Expires At
Bundle Digest
```

任一授权缺失、冲突、过期或作用域不匹配时不得进入保护边界。

### IR-R1-13 制度提交尝试必须绑定分配、授权和逐记录摘要

在 `IR-C-22` 字段基础上增加：

```text
Freeze ID Allocation Record ID and Digest
Institution Commit Authority Bundle ID and Digest
Candidate Freeze Ledger Entry ID and Digest
Candidate Institution Registry Entry ID and Digest
Candidate Attribution Record ID and Digest
Candidate Institution Commit Write-set Digest
```

提交执行者不得替换候选记录或重新计算出不同写集。

### IR-R1-14 保护协调者只消费授权

保护协调者验证全部授权和候选摘要后，可以把三个内容同一载荷置入同一不可分割边界。它不得：

- 分配冻结标识；
- 创建冻结决定；
- 修改候选载荷；
- 以协调权威代替任一登记权威；
- 在部分授权下执行降级写入。

### IR-R1-15 每个最终记录必须分别内容同一

```text
Candidate Freeze Ledger Entry Digest
= Registered Freeze Ledger Entry Payload Digest

Candidate Institution Registry Entry Digest
= Registered Institution Registry Entry Payload Digest

Candidate Attribution Record Digest
= Registered Attribution Record Payload Digest
```

三个等式全部成立且属于同一保护边界，才能构造 `Successful Institution Commit Reference`。

任一不等、缺失或跨边界组合都为 `CONFLICTED` 或 `INDETERMINATE`，不得宣布成功。

正常制度提交解析键：

```text
Institution Commit Resolution Key =
  Institution Commit Attempt ID
+ Institution Registry Boundary
+ Freeze Ledger Boundary
+ Attribution Boundary
+ Resolution Rule Version
```

值域：

```text
COMMITTED | ABORTED | INDETERMINATE | CONFLICTED
```

三个内容同一权威记录全部存在且边界完整时为 `COMMITTED`；已登记合格且适用的完整未写入证明支持 `ABORTED`；部分写入或不兼容权威记录为 `CONFLICTED`；缺失、边界不完整或读取失败为 `INDETERMINATE`。

解析执行和解析登记必须分权。`Successful Institution Commit Reference` 必须引用已登记的精确 `COMMITTED` 解析；在通用证明治理缺失时不得产生 `ABORTED`。

```text
Candidate Institution Commit Resolution Record
  -> Institution Commit Resolution Registration Attempt
  -> Registered Institution Commit Resolution Record

Candidate Institution Commit Resolution Payload Digest
= Registered Institution Commit Resolution Payload Digest
```

## 四、B2：制度生命周期登记因果

### IR-R1-16 生命周期关系必须由独立决策事实授权

每个 `SUPERSEDES`、`REVOKES` 或 `DEPRECATES` 关系必须引用一个精确 `Institution Lifecycle Decision Fact`。

该决策事实必须通过兼容决策模型的准入和受保护写入成立；本 R1 不自行创建决策事实。

最低决策谱系必须引用：

```text
Observable Lifecycle Decision Act
Lifecycle Decision Attempt Record
Candidate Lifecycle Decision Record
Registered Admissibility Record
Protected Lifecycle Decision Write
Authoritative Lifecycle Decision Record
Institution Lifecycle Decision Fact
```

任一环节缺失时不得构建候选生命周期关系。

新增专用权威：

```text
Lifecycle Relation Projection Execution Authority Type
Lifecycle Relation Registration Authority Type
Lifecycle Relation Registration Resolution Execution Authority Type
Lifecycle Relation Registration Resolution Registration Authority Type
```

### IR-R1-17 生命周期决定必须固定精确边界

最低字段：

```text
Lifecycle Decision Fact ID and Digest
Primary Lifecycle Decision Authority Reference
Source Institution ID and Version
Target Institution ID and Version when applicable
Lifecycle Relation Type
Effective Scope
Valid From and Valid Until
Decision At
Evidence References
Governing Institution References
```

每个决定实例只能引用一个主要生命周期决定权威。

### IR-R1-18 生命周期登记必须先形成候选和尝试

```text
Institution Lifecycle Decision Fact
  -> Candidate Lifecycle Relation Record
  -> Lifecycle Relation Registration Attempt
  -> Registered Lifecycle Relation Record
```

`Lifecycle Relation Registration Attempt` 至少绑定候选 ID、候选摘要、登记权威、目标注册表、幂等键、尝试时间和证据。

候选和已登记关系至少共同绑定生命周期决定事实、关系键、源和目标版本、关系类型、作用域、有效区间、主要决定权威、候选载荷摘要、已登记载荷摘要、建立时间、登记时间和证据。

### IR-R1-19 生命周期关系必须拥有稳定键

```text
Lifecycle Relation Key =
  Source Institution ID and Version
+ Target Institution ID and Version or NOT_APPLICABLE
+ Lifecycle Relation Type
+ Effective Scope Digest
+ Valid From
+ Lifecycle Decision Fact ID
```

同键同载荷幂等；同键不同载荷必须保留 `CONFLICTED`。

### IR-R1-20 生命周期计算和登记不得互相继承权威

```text
Lifecycle Relation Projection Authority
  -> may build candidate from Decision Fact
  -/-> register relation

Lifecycle Relation Registration Authority
  -> may register content-identical qualified candidate
  -/-> create Decision Fact or change candidate
```

只有已登记、内容同一且位于查询生命周期边界内的关系可以影响引用适用性。

```text
Candidate Lifecycle Relation Payload Digest
= Registered Lifecycle Relation Payload Digest
```

生命周期登记解析键绑定登记尝试、关系键、注册表边界和规则版本，值域为：

```text
REGISTERED | NOT_REGISTERED | INDETERMINATE | CONFLICTED
```

精确内容同一记录和完整边界支持 `REGISTERED`；合格适用的完整未登记证明支持 `NOT_REGISTERED`；不兼容权威记录支持 `CONFLICTED`；缺失或边界不完整支持 `INDETERMINATE`。只有已登记的 `REGISTERED` 解析可以让关系进入引用适用性计算。

### IR-R1-21 生命周期关系不能追溯删除历史适用性

关系只从声明的 `Valid From` 向未来影响适用性。历史认识视图仍按当时有效时间和认识边界解析。

任何试图让新关系证明旧版本“从未冻结”或“从未适用”的载荷必须拒绝登记。

## 五、B2：制度注册表更正因果

### IR-R1-22 更正资格计算和登记必须分权

新增：

```text
Institution Registry Correction Qualification Execution Authority Type
Institution Registry Correction Qualification Registration Authority Type
Institution Registry Correction Registration Authority Type
```

更正请求者、资格计算者、资格登记者和更正登记者不得隐式继承彼此权威。

### IR-R1-23 更正资格使用四值

```text
QUALIFIED
DISQUALIFIED
INDETERMINATE
CONFLICTED
```

只有精确 `QUALIFIED` 且在更正提交坐标上适用的已登记资格记录可以支持更正登记。缺失、读取失败或边界不完整必须保持 `INDETERMINATE`。

### IR-R1-24 更正必须形成完整候选—登记链

```text
Correction Request and Evidence
  -> Candidate Correction Qualification Record
  -> Registered Correction Qualification Record
  -> Candidate Institution Registry Correction Record
  -> Correction Registration Attempt
  -> Registered Institution Registry Correction Record
```

每一步必须拥有独立身份、内容摘要、时间、权威和证据引用。

### IR-R1-25 更正必须拥有稳定键和内容同一

```text
Institution Registry Correction Key =
  Original Record ID and Digest
+ Corrected Field Set Digest
+ Correction Request ID
+ Effective At
```

```text
Candidate Correction Payload Digest
= Registered Correction Payload Digest
```

同键不同载荷为 `CONFLICTED`，不得最后写入获胜。

### IR-R1-26 更正范围必须是非语义字段白名单

允许字段必须由版本化更正契约显式列举。以下字段不得通过更正改变：

```text
Institution ID or Version
Frozen Content Digest
Freeze ID
Freeze Decision or Authority Reference
Freeze Evidence Package Reference
Effective Scope
Validity Interval
Registration Mode
Freeze Basis Mode
Lifecycle Semantics
```

这些字段变化只能走新制度版本、生命周期决定或独立治理修复。

### IR-R1-27 只有已登记更正可以进入解析

候选、资格结果、登记尝试和未登记更正不得影响制度当前视图或冻结引用解析。

更正进入历史认识视图时还必须满足 `Recorded At <= Known At`；后来的更正不能伪装成过去当时已知。

## 六、B3：注册表外制度提交

### IR-R1-28 注册表外提交使用专用对象和权威

新增对象：

```text
Pre-registry Institution Commit Attempt
Pre-registry Freeze ID Assignment Record
Candidate Pre-registry Freeze Record
Candidate Pre-registry Commit Attribution Record
Pre-registry Protected Commit Record
Pre-registry Institution Commit Resolution Record
Successful Pre-registry Institution Commit Reference
```

新增权威：

```text
Pre-registry Commit Coordination Authority Type
Pre-registry Freeze ID Assignment Authority Type
Pre-registry Freeze Record Registration Authority Type
Pre-registry Attribution Registration Authority Type
Pre-registry Commit Resolution Execution Authority Type
Pre-registry Commit Resolution Registration Authority Type
```

这些对象和权威只允许用于 `CR-0004` 的一次性注册表外冻结。

### IR-R1-29 注册表外提交尝试必须固定完整写集

`Pre-registry Commit Authority Bundle` 至少绑定协调授权、冻结记录登记授权、归因登记授权、允许的保护载体、精确候选记录及摘要、有效窗口和包摘要。协调者不得继承登记权威。

最低字段：

```text
Pre-registry Commit Attempt ID
Pre-registry Freeze ID Assignment Record ID and Digest
Exact CR-0004 Artifact ID, Version and Digest
Pre-registry Freeze Decision Reference
Applicable Freeze Authority Reference
Freeze Evidence Package Reference
Candidate Pre-registry Freeze Record ID and Digest
Candidate Pre-registry Attribution Record ID and Digest
Protected Governance History Carrier ID
Declared Write-set Digest
Authority Bundle ID and Digest
Idempotency Key
Attempted At
Evidence References
```

`Pre-registry Freeze ID Assignment Record` 必须由既有 `IF-0001`、`IF-0007` 下的外部适用赋值权威建立，绑定命名空间、标识、精确 `CR-0004` 版本和摘要、权威、赋值时间及证据。它不是后来 `Freeze ID Allocation Ledger` 的历史分配记录。

启动准备时必须据此建立 `BOOTSTRAP_RESERVED_EXISTING` 保留记录，并保持原赋值时间与保留登记时间分离。

### IR-R1-30 注册表外保护边界必须建立内容同一记录

受保护治理历史载体必须不可分割建立：

```text
Pre-registry Protected Commit Record
+ Registered Pre-registry Freeze Record
+ Registered Pre-registry Commit Attribution Record
```

每个最终记录必须分别与候选摘要相同，并共同绑定同一尝试、冻结标识、制度版本、内容摘要、决定、权威、证据包、作用域和有效区间。

### IR-R1-31 注册表外提交解析拥有稳定键和四值

```text
Pre-registry Commit Resolution Key =
  Pre-registry Commit Attempt ID
+ Protected Carrier Boundary ID and Position
+ Resolution Rule Version
```

值域：

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

### IR-R1-32 注册表外提交解析必须失败关闭

```text
all required content-identical protected records found
+ complete carrier boundary
-> COMMITTED

qualified applicable complete proof of no protected write
-> ABORTED

incompatible authoritative records or partial atomic write
-> CONFLICTED

missing record, incomplete boundary, timeout or read failure
-> INDETERMINATE
```

在证明资格和适用性治理不可用时，不能产生 `ABORTED`，只能保持 `INDETERMINATE`。

```text
Candidate Pre-registry Commit Resolution Payload Digest
= Registered Pre-registry Commit Resolution Payload Digest
```

只有已登记的内容同一解析可以支持成功引用或终局未提交结论。

### IR-R1-33 成功注册表外提交引用必须绑定已登记 COMMITTED

`Successful Pre-registry Institution Commit Reference` 至少绑定：

```text
Pre-registry Commit Attempt ID and Digest
Registered Pre-registry Freeze Record ID and Digest
Registered Attribution Record ID and Digest
Pre-registry Protected Commit Record ID and Digest
Registered COMMITTED Resolution ID and Digest
Protected Carrier Boundary
Committed At
```

自由文本、文件路径、仓库提交或执行者声明不得替代该引用。

## 七、B3：外部启动锚与内部启动提交

### IR-R1-34 启动清单必须在任何写入前固定且不自引用

`Bootstrap Manifest` 至少包含：

```text
Bootstrap Manifest ID and Version
Exact First-entry Membership
Allocated Freeze IDs and Allocation Record Digests
Preallocated Internal Record IDs
Candidate Institution Entry Digests
Candidate Freeze Ledger Recognition Entry Digests
Bootstrap Anchor Core Payload Digest
Candidate Bootstrap Attribution Payload Digest
Bootstrap Window Definition Record ID and Digest
Bootstrap Evidence and Review References
Bootstrap Freeze Recognition Decision Reference
Bootstrap Authority Bundle Reference
Canonicalization and Digest Contract
Manifest Created At
Manifest Digest
```

`Bootstrap Anchor Core Payload Digest` 只覆盖首批集合、模式、标识、决定、证据、权威和内部预分配标识，不包含外部锚引用。

清单不得包含尚未产生的外部锚记录 ID、摘要或最终内部锚摘要。外部锚单向绑定清单摘要；外部锚登记后再构造绑定“锚核心 + 外部锚引用”的最终候选内部锚，从而避免摘要自引用。

### IR-R1-35 外部启动锚必须拥有独立对象和权威

新增：

```text
External Bootstrap Anchor Commitment Candidate
External Bootstrap Anchor Commitment Record
External Anchor Commitment Registration Attempt
External Anchor Commitment Resolution Record
```

新增权威：

```text
External Bootstrap Anchor Commitment Execution Authority Type
External Bootstrap Anchor Commitment Registration Authority Type
External Anchor Commitment Resolution Execution Authority Type
External Anchor Commitment Resolution Registration Authority Type
```

### IR-R1-36 外部锚只承诺启动清单

`External Bootstrap Anchor Commitment Record` 至少绑定：

```text
External Anchor Commitment ID
Bootstrap Manifest ID and Digest
External Immutable Carrier ID
Carrier Position and Boundary
Commit Authority Reference
Candidate and Registered Payload Digests
Committed At
Recorded At
Evidence References
```

外部锚不包含内部启动锚摘要，不声称内部提交已经成功，也不关闭启动窗口。

稳定键：

```text
External Bootstrap Anchor Commitment Key =
  External Anchor Commitment ID
+ Bootstrap Manifest ID and Digest
+ External Immutable Carrier ID
```

同键同载荷幂等；同键不同载荷必须保留冲突。候选和已登记外部锚载荷摘要必须相同。

```text
External Anchor Commitment Resolution Key =
  External Anchor Commitment ID
+ Bootstrap Manifest Digest
+ External Carrier Boundary
+ Resolution Rule Version
```

解析值域为 `COMMITTED | ABORTED | INDETERMINATE | CONFLICTED`。精确内容同一锚记录和完整外部边界支持 `COMMITTED`；合格适用的完整未写入证明支持 `ABORTED`；不同清单摘要或多个不兼容权威锚记录为 `CONFLICTED`；缺失、边界不完整或读取失败为 `INDETERMINATE`。解析执行和登记必须分权。

### IR-R1-37 内部启动提交只能消费已登记外部锚

`Bootstrap Internal Authority Bundle` 至少绑定：

```text
Bootstrap Internal Commit Coordination Grant
Bootstrap Anchor Registration Grant
Bootstrap Freeze Ledger Recognition Registration Grant
Bootstrap Institution Entry Registration Grants
Bootstrap Commit Attribution Registration Grant
Bootstrap Window Definition Registration Grant
Allowed Bootstrap Manifest and External Anchor Digests
Allowed Candidate Internal Record IDs and Digests
Effective At and Expires At
Bundle Digest
```

协调者不得用自身权威代替任一登记授权。

`Bootstrap Commit Attempt` 必须绑定：

```text
Bootstrap Manifest ID and Digest
Registered External Anchor Commitment ID and Digest
External Anchor COMMITTED Resolution Reference
All Freeze ID Allocation Record References
Bootstrap Internal Authority Bundle
All Candidate Internal Record IDs and Digests
Declared Internal Write-set Digest
Idempotency Key
Attempted At
```

外部锚未知、冲突或未提交时不得进入内部保护边界。

### IR-R1-38 内部启动写入不得提前产生关闭事实

内部保护边界原子建立：

```text
Bootstrap Anchor Record
+ First Institution Registry Entry Set
+ Freeze Ledger Recognition Entry Set
+ Bootstrap Commit Attribution Record
+ Bootstrap Window Definition Record
```

R1 用 `Bootstrap Window Definition Record` 取代 `IR-C-50` 中提前写入的 `Bootstrap Closed Record`。该记录只固定一次性尝试和关闭条件，不证明启动已经成功。

`Bootstrap Window Definition Record` 至少绑定唯一允许的清单摘要、外部锚、内部尝试、首批集合摘要、允许的终局解析键、禁止第二首批集合规则和证据。任何同键不同窗口定义为 `CONFLICTED`。

### IR-R1-39 启动提交解析必须独立且四值化

新增：

```text
Bootstrap Commit Resolution Execution Authority Type
Bootstrap Commit Resolution Registration Authority Type
```

解析执行者只能读取清单、外部锚和内部权威来源并生成候选；解析登记者只能登记内容相同的合格候选。

```text
Candidate Bootstrap Commit Resolution Payload Digest
= Registered Bootstrap Commit Resolution Payload Digest
```

只有已登记的内容同一解析可以决定启动模式；候选解析、自由计算结果或缓存不得关闭窗口。

```text
Bootstrap Commit Resolution Key =
  Bootstrap Manifest Digest
+ External Anchor Commitment Record ID and Digest
+ Bootstrap Commit Attempt ID
+ Internal Registry Boundary
+ Internal Freeze Ledger Boundary
+ Bootstrap Resolution Rule Version
```

值域：

```text
COMMITTED
ABORTED
INDETERMINATE
CONFLICTED
```

### IR-R1-40 启动提交真值表必须确定

```text
registered external anchor COMMITTED
+ exact internal anchor
+ exact complete first registry set
+ exact complete recognition ledger set
+ exact attribution
+ exact window definition
+ all content digests match manifest
+ all internal boundaries complete
-> COMMITTED

qualified applicable complete proof of no internal protected write
-> ABORTED

partial atomic write
or incompatible manifest / anchor / entry / attribution records
or more than one first-entry set
-> CONFLICTED

missing source, incomplete boundary, unavailable carrier or read failure
-> INDETERMINATE
```

### IR-R1-41 启动模式由已登记解析决定

```text
Bootstrap Mode =
  UNINITIALIZED
  | PREPARED
  | COMMIT_UNRESOLVED
  | ACTIVE_CLOSED
  | ABORTED_CLOSED
  | CONFLICTED
```

规则：

```text
no manifest -> UNINITIALIZED
manifest + external anchor COMMITTED, no internal attempt -> PREPARED
internal attempt, no terminal registered resolution -> COMMIT_UNRESOLVED
registered Bootstrap Commit Resolution = COMMITTED -> ACTIVE_CLOSED
registered Bootstrap Commit Resolution = ABORTED -> ABORTED_CLOSED
registered resolution or first-set conflict -> CONFLICTED
```

只有 `ACTIVE_CLOSED` 允许正常 `NATIVE` 登记。其他状态全部失败关闭。

### IR-R1-42 启动窗口不得通过重试重开

`ABORTED_CLOSED`、`CONFLICTED` 或长期 `COMMIT_UNRESOLVED` 均不授权换键重试、修改首批集合或重开启动窗口。

任何恢复必须建立新的制度修订、恢复决定和迁移证据，并保留原清单、外部锚、尝试、部分写入和解析历史。

## 八、B4：边界完整性与解析身份

### IR-R1-43 每个解析来源必须有独立完整性记录

最低来源：

```text
Institution Registry
Freeze Ledger
Commit Resolution Ledger
Lifecycle Registry
Correction Registry
Bootstrap Manifest Carrier
External Anchor Carrier
Freeze ID Allocation Ledger
Bootstrap Resolution Ledger
Pre-registry Governance History Carrier when applicable
```

每个来源必须提供 `Registered Source Boundary Completeness Record`，绑定来源 ID、作用域、包含位置或精确记录集、边界摘要、完整性规则版本、资格权威、登记权威、有效时间、认识时间和证据。

一个来源的完整性记录不能证明另一个来源完整。

完整性值域：

```text
COMPLETE | INCOMPLETE | INDETERMINATE | CONFLICTED
```

`INCOMPLETE` 必须由正向边界证据证明仍有未纳入必需记录；缺失、读取失败或未知前沿只能是 `INDETERMINATE`。

### IR-R1-44 完整性计算和登记必须分权

新增：

```text
Source Boundary Completeness Qualification Execution Authority Type
Source Boundary Completeness Registration Authority Type
```

来源完整性计算者只能生成候选完整性；完整性登记者只登记内容相同的合格候选。任一来源没有精确 `COMPLETE` 记录时，依赖该来源的终局解析必须保持 `INDETERMINATE`。

候选和已登记完整性载荷必须内容同一，并绑定同一来源、作用域、位置、规则版本和边界摘要。

### IR-R1-45 认识边界必须形成稳定向量

```text
Institution Resolution Boundary Vector =
  ordered Source Boundary Entries
+ Vector Scope
+ Valid At
+ Known At
+ Vector Rule Version
+ Vector Digest
```

每个条目绑定来源 ID、边界位置或精确集合、完整性记录和摘要。单一时间戳、单一水位或“最新”不能替代该向量。

### IR-R1-46 解析必须声明视图模式

```text
HISTORICAL_AS_KNOWN
CURRENT_RESTATED
```

`HISTORICAL_AS_KNOWN` 只消费 `Recorded At <= Known At` 且在 `Valid At` 适用的记录。

`CURRENT_RESTATED` 可以消费当前完整认识边界中的后续更正和生命周期关系，但必须以独立投影呈现，不能覆盖或伪装成历史当时认识。

### IR-R1-47 冻结引用解析必须拥有稳定键

```text
Freeze Reference Resolution Key =
  Institution Freeze Reference Key
+ Valid At
+ Known At
+ Institution Resolution Boundary Vector Digest
+ View Mode
+ Freeze Reference Resolution Rule Version
```

任一字段变化必须形成新解析身份和新候选记录。

## 九、B4：三模式必需来源

### IR-R1-48 NATIVE 模式必须验证正常冻结全链

`NATIVE + NATIVE_FREEZE` 必需来源：

```text
Exact Institution Content Artifact and Digest
Registered Freeze ID Allocation Record
Registered Institution Proposal
Approved Institution Review Decision
Freeze Evidence Package
Applicable Freeze Authority Record
FREEZE_AUTHORIZED Decision Record
Institution Commit Attempt
Registered Freeze Ledger Entry
Registered Institution Registry Entry
Registered Commit Attribution Record
Registered COMMITTED Institution Commit Resolution
Successful Institution Commit Reference
Applicable Lifecycle and Correction Records
COMPLETE Boundary Records for every source
```

### IR-R1-49 PRESERVED 模式必须同时验证旧冻结链和启动登记链

`BOOTSTRAP_RECOGNIZED + PRESERVED_PRE_REGISTRY_FREEZE` 必需来源：

```text
Exact Institution Content Artifact and Bootstrap-observed Digest
Exact Complete Pre-registry Freeze Evidence Package
Verified Pre-registry Freeze ID, Authority and Decision
Registered COMMITTED Pre-registry Commit Resolution
Successful Pre-registry Institution Commit Reference
Bootstrap Manifest and COMMITTED External Anchor
Bootstrap Freeze Recognition Decision selecting PRESERVED mode
Registered COMMITTED Bootstrap Commit Resolution
Exact Bootstrap Registry and Recognition Ledger Entries
Applicable Lifecycle and Correction Records
COMPLETE Boundary Records for every source
```

启动决定只能确认使用完整旧链，不能替换旧链中的冻结决定、权威、证据或提交。

### IR-R1-50 PROSPECTIVE 模式必须验证新启动识别冻结链

`BOOTSTRAP_RECOGNIZED + PROSPECTIVE_BOOTSTRAP_RECOGNITION` 必需来源：

```text
Exact Institution Content Artifact and Bootstrap-observed Digest
Bootstrap Evidence Package
Independent Bootstrap Review Decision
Registered New Bootstrap Freeze ID Allocation Record
Applicable Bootstrap Freeze Recognition Authority
Bootstrap Freeze Recognition Decision selecting PROSPECTIVE mode
Bootstrap Manifest and COMMITTED External Anchor
Registered COMMITTED Bootstrap Commit Resolution
Exact Bootstrap Registry and Recognition Ledger Entries
Validity Start no earlier than Bootstrap COMMITTED At
Applicable Lifecycle and Correction Records
COMPLETE Boundary Records for every source
```

原声明冻结标识和时间只作为历史字段，不得进入新冻结引用的 `Freeze ID` 或有效起点。

## 十、B4：确定性解析规则

### IR-R1-51 冻结链资格按模式使用统一优先级

```text
known mutually incompatible authoritative records
  -> CONFLICTED

all mode-required sources COMPLETE
+ all exact identities and digests match
+ all required decisions and commit resolutions positive
  -> VERIFIED

all proof-required boundaries COMPLETE
+ qualified applicable positive rejection or non-commit proof
+ no authoritative conflict
  -> REJECTED

otherwise
  -> INDETERMINATE
```

缺失、未找到、边界不完整、外部载体不可用、超时或读取失败不得产生 `REJECTED`。

### IR-R1-52 引用适用性必须确定性解析

```text
conflicting lifecycle, correction, scope or validity records
  -> CONFLICTED

complete boundaries
+ exact scope excludes request
or validity interval excludes Valid At
or registered lifecycle relation makes version inapplicable at Valid At
  -> INAPPLICABLE

complete boundaries
+ scope includes request
+ validity interval includes Valid At
+ no applicable revocation, supersession or deprecation exclusion
  -> APPLICABLE

otherwise
  -> INDETERMINATE
```

生命周期关系存在不等于历史冻结链被拒绝；它只影响指定坐标的适用性。

### IR-R1-53 可用性投影保持基础四值真值表

```text
VERIFIED + APPLICABLE -> USABLE
REJECTED + APPLICABLE | INAPPLICABLE | INDETERMINATE -> NOT_USABLE
VERIFIED + INAPPLICABLE -> NOT_USABLE
any CONFLICTED -> CONFLICTED
otherwise -> INDETERMINATE
```

当冻结链 `REJECTED` 且适用性 `CONFLICTED` 时仍为 `CONFLICTED`，不得隐藏适用性冲突。

### IR-R1-54 解析候选和登记记录必须完整内容同一

```text
Freeze Reference Resolution Request
  -> Candidate Freeze Reference Resolution Record
  -> Resolution Registration Attempt
  -> Registered Freeze Reference Resolution Record
```

候选和已登记记录至少绑定：

```text
Freeze Reference Resolution Key
Registration and Freeze Basis Modes
Required Source Set Version
Boundary Vector and Digest
Freeze Chain Qualification
Reference Applicability
Reference Usability
Matched and Rejected Record IDs and Digests
Lifecycle and Correction References
Candidate Payload Digest
Registered Payload Digest
Resolved At
Recorded At
Evidence References
```

候选与登记载荷不相同、登记权威不适用或登记边界不完整时，记录不能支持终局投影。

### IR-R1-55 解析结果不得创建制度或行动权威

```text
USABLE
  -> may satisfy only the institution-freeze-reference prerequisite
  -/-> grant consumer authority
  -/-> prove consumer contract compatibility
  -/-> create business fact
  -/-> authorize target transition
```

消费方仍必须独立验证契约兼容、业务权威、资格和全部前置条件。

## 十一、修订后的规范因果路径

### 正常冻结登记

```text
Freeze ID Allocation Attempt
  -> Registered Freeze ID Allocation Record
  -> Freeze Decision consumes exact allocation
  -> Three Candidate Authoritative Records
  -> Institution Commit Authority Bundle
  -> Institution Commit Attempt
  -> Protected Coordinator consumes independent grants
       -> Registered Freeze Ledger Entry
       + Registered Institution Registry Entry
       + Registered Attribution Record
  -> Independent Commit Resolution
  -> Successful Institution Commit Reference
```

### 生命周期与更正

```text
Institution Lifecycle Decision Fact
  -> Candidate Lifecycle Relation
  -> Registration Attempt
  -> Content-identical Registered Lifecycle Relation

Correction Request
  -> Registered QUALIFIED Correction Qualification
  -> Candidate Correction
  -> Registration Attempt
  -> Content-identical Registered Correction
```

### 注册表外冻结

```text
Pre-registry Freeze ID Allocation
  -> Pre-registry Commit Attempt
  -> Protected Governance History Write
  -> Candidate Commit Resolution
  -> Independent Registration
       -> COMMITTED
            -> Successful Pre-registry Institution Commit Reference
       -> ABORTED | INDETERMINATE | CONFLICTED
            -> No Successful Reference
```

### 一次性启动

```text
Exact Bootstrap Manifest without external-anchor self-reference
  -> External Anchor Commitment
  -> Registered External Anchor COMMITTED Resolution
  -> Internal Bootstrap Commit Attempt
  -> Atomic Internal First-set Write
  -> Independent Bootstrap Commit Resolution
       -> COMMITTED -> Bootstrap Mode = ACTIVE_CLOSED -> NATIVE enabled
       -> ABORTED -> ABORTED_CLOSED -> fail closed
       -> INDETERMINATE -> COMMIT_UNRESOLVED -> fail closed
       -> CONFLICTED -> CONFLICTED -> fail closed
```

### 三模式引用解析

```text
Freeze Reference
+ Query Coordinate
+ COMPLETE Boundary Vector
+ View Mode
+ Mode-specific Required Source Set
-> Stable Resolution Key
-> Candidate Resolution
-> Content-identical Registration
-> Freeze Chain Qualification
+ Reference Applicability
-> Reference Usability
```

## 十二、修订后的权威操作矩阵

| 角色 | 可以 | 不得 |
|---|---|---|
| `Freeze ID Allocator` | 在精确命名空间生成候选分配 | 冻结制度、作出冻结决定、复用标识 |
| `Freeze ID Allocation Registrar` | 登记内容同一合格分配 | 修改分配、决定制度冻结 |
| `Institution Commit Coordinator` | 消费独立授权并组织保护边界 | 创建授权、修改候选、代替登记者 |
| 各权威记录 `Registrar` | 在保护边界写入获授权的内容同一载荷 | 继承协调、决定或其他登记权威 |
| `Lifecycle Relation Projector` | 从决策事实构建候选关系 | 创建决策事实、登记关系 |
| `Lifecycle Relation Registrar` | 登记内容同一合格关系 | 修改关系或创建生命周期决定 |
| `Correction Qualifier` | 计算更正资格候选 | 登记自身结论、修改原记录 |
| `Correction Registrar` | 登记内容同一合格更正 | 改变制度语义、冻结链或历史 |
| `Pre-registry Commit Coordinator` | 执行一次性外部保护写入 | 把文件存在当作成功、解析自身提交 |
| `Pre-registry Commit Resolver` | 解析精确注册表外尝试 | 登记自身解析、补写冻结记录 |
| `External Anchor Committer` | 提交精确启动清单摘要 | 声明内部启动成功、关闭窗口 |
| `Bootstrap Internal Coordinator` | 消费外部锚和独立授权执行内部首批写入 | 修改清单、创建外部锚、关闭窗口 |
| `Bootstrap Commit Resolver` | 对外部锚和内部首批写入作四值解析 | 修改任何来源、授权重试 |
| `Boundary Completeness Qualifier` | 计算一个来源边界完整性 | 证明其他来源完整、修改来源 |
| `Freeze Reference Resolver` | 按模式和稳定坐标构建候选解析 | 省略来源、提高未知、创建制度或行动权威 |
| `Freeze Reference Resolution Registrar` | 登记内容同一合格解析 | 重新解析、折叠冲突或修改候选 |

## 十三、R1 非法状态增量

在 `CR-0004` 非法状态基础上，未来合并时还必须禁止：

- 冻结决定者或启动识别决定者自行分配冻结标识；
- 已分配、退役、失败或未知的冻结标识被复用；
- 协调权威隐式取得冻结账本、注册表或归因登记权威；
- 最终权威记录与提交前候选摘要不相同；
- 未登记生命周期关系改变引用适用性；
- 更正资格计算者登记自身结果；
- 用更正改变摘要、冻结标识、决定、权威、作用域或有效区间；
- 用文件、仓库提交或自由文本替代成功注册表外提交引用；
- 在通用证明治理缺失时把未找到记录解释为 `ABORTED`；
- 启动清单包含自身外部锚摘要并形成循环摘要；
- 外部锚提交成功被解释为内部启动成功；
- 内部首批写入在没有外部锚 `COMMITTED` 时执行；
- 初始内部写入直接创建当前有效的 `Bootstrap Closed Record`；
- 启动解析非 `COMMITTED` 时启用 `NATIVE`；
- 通过换键、重开窗口或删除失败记录重试启动；
- 一个来源完整性记录证明其他来源完整；
- 冻结引用解析省略视图模式、双时间或边界向量；
- 三种模式共享不完整来源集却产生 `VERIFIED`；
- 缺失、读取失败或不完整边界产生 `REJECTED` 或 `INAPPLICABLE`；
- `CONFLICTED` 被压缩为其他终局；
- `USABLE` 被解释为业务权威或契约兼容已经成立。

## 十四、阻断闭合映射

| 审查阻断 | R1 规则 | 自检结论 |
|---|---|---|
| B1 冻结标识分配权威 | `IR-R1-03` 至 `IR-R1-09` | `CANDIDATE_CLOSED` |
| B1 受保护登记权威拓扑 | `IR-R1-10` 至 `IR-R1-15` | `CANDIDATE_CLOSED` |
| B2 生命周期登记因果 | `IR-R1-16` 至 `IR-R1-21` | `CANDIDATE_CLOSED` |
| B2 更正登记因果 | `IR-R1-22` 至 `IR-R1-27` | `CANDIDATE_CLOSED` |
| B3 注册表外提交 | `IR-R1-28` 至 `IR-R1-33` | `CANDIDATE_CLOSED` |
| B3 外部启动锚与内部提交 | `IR-R1-34` 至 `IR-R1-42` | `CANDIDATE_CLOSED` |
| B4 解析边界与稳定身份 | `IR-R1-43` 至 `IR-R1-47` | `CANDIDATE_CLOSED` |
| B4 三模式解析 | `IR-R1-48` 至 `IR-R1-55` | `CANDIDATE_CLOSED` |

`CANDIDATE_CLOSED` 只是 R1 自检，不是独立审查通过。

## 十五、R1 自检

```text
Bounded Repair Scope: PASS
Freeze ID Allocation Authority: DEFINED
Freeze ID Non-reuse: DEFINED
Protected Registration Authority Bundle: DEFINED
Per-record Content Identity: DEFINED
Lifecycle Registration Causality: DEFINED
Correction Qualification and Registration: DEFINED
Pre-registry Commit Contract: DEFINED
Pre-registry Commit Four-value Resolution: DEFINED
Bootstrap Manifest Non-self-reference: DEFINED
External Anchor Authority and Record: DEFINED
Internal Bootstrap Commit Resolution: DEFINED
Bootstrap Activation Gate: DEFINED
Boundary Completeness per Source: DEFINED
Resolution Boundary Vector: DEFINED
Resolution Stable Key: DEFINED
NATIVE Required Source Set: DEFINED
PRESERVED Required Source Set: DEFINED
PROSPECTIVE Required Source Set: DEFINED
Mode-specific Deterministic Resolution: DEFINED
History Preservation: PASS
Provider Independence: PASS
Cross-domain Portability: PASS
Known B1-B4 Mapping: COMPLETE
Independent Review: REQUIRED
Consolidation: BLOCKED_PENDING_REVIEW
Institution Freeze Evidence: INSUFFICIENT
Institution Freeze Eligibility: FAIL
Current Status: DRAFT
```

## 当前决定

1. 将本文件登记为 `CR-0004-R1` 有界修订候选；
2. 保留 `CR-0004` 和 `CR-0004-LOCAL-REVIEW` 作为不可覆盖历史；
3. 不修改 `IF-0001` 至 `IF-0007`、`CR-0002` 或 `CR-0003`；
4. 不创建冻结标识、注册表、账本、生命周期关系、更正、解析或运行时权威；
5. 不进入 `WS-02`、实现、经验性证据采集或冻结准备；
6. 下一阶段只对 R1 执行独立模型与启动闭环复审；
7. 复审通过后才允许建立 `CR-0004` 单一合并候选；
8. 合并候选仍必须另行通过语义差异、接口一致性和冻结依赖准备度审查。
